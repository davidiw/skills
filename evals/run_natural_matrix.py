#!/usr/bin/env python3
"""Frozen natural trials with unmodified installs, pinned skills and context traces."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import socketserver
import tempfile
import threading
import time

ACTIVE: set[subprocess.Popen] = set()
ACTIVE_LOCK = threading.Lock()
STOP = threading.Event()
ENVIRONMENT_RULES = (
    "Treat the current directory as the complete target repository. Inspect only "
    "this repository and runtime-provided skill/agent-role resources, not parent directories, "
    "other repositories, evaluation cases, expected outcomes, grading artifacts, "
    "other fixtures or runner records. Keep edits in this repository. No network "
    "calls or external system mutations. These restrictions apply to delegated "
    "agents too. They are environment limits, not workflow-selection instructions."
)
FORBIDDEN_RUNTIME_PARTS = {"evals", "tests", "fixtures", "results", "evidence", ".git", ".agents"}
TOKEN_KEYS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens")


def tree(path: Path) -> dict[str, str]:
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(path.rglob("*")) if p.is_file()
            and not ({".git", "__pycache__"} & set(p.relative_to(path).parts))}


def digest(path: Path) -> str:
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    return hashlib.sha256(json.dumps(tree(path), sort_keys=True).encode()).hexdigest()


def stop_process(process: subprocess.Popen) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def interrupt(*_):
    STOP.set()
    with ACTIVE_LOCK:
        active = list(ACTIVE)
    for process in active:
        stop_process(process)
    raise KeyboardInterrupt


def command(args, env, cwd, timeout):
    started = time.time()
    with ACTIVE_LOCK:
        if STOP.is_set():
            raise RuntimeError("evaluation cancelled")
        process = subprocess.Popen(args, cwd=cwd, env=env, text=True,
                                   stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, start_new_session=True)
        ACTIVE.add(process)
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        stop_process(process)
        stdout, stderr = process.communicate()
    finally:
        with ACTIVE_LOCK:
            ACTIVE.discard(process)
    return {"stdout": stdout, "stderr": stderr, "return_code": process.returncode,
            "timed_out": timed_out, "started_at": started, "ended_at": time.time()}


def verify_runtime(runtime: Path, expected: dict[str, str]) -> dict[str, str]:
    for path in runtime.rglob("*"):
        if path.is_symlink() or FORBIDDEN_RUNTIME_PARTS & set(path.relative_to(runtime).parts):
            raise RuntimeError("development material or alias in installed runtime")
    actual = tree(runtime)
    if actual != expected:
        raise RuntimeError("installed runtime differs from frozen source")
    return actual


def frozen_source(package: Path, matrix: Path) -> dict:
    package, matrix = package.resolve(), matrix.resolve()
    if matrix.parent != package / "evals":
        raise RuntimeError("matrix must belong to the candidate checkout")
    if digest(Path(__file__)) != digest(package / "evals/run_natural_matrix.py"):
        raise RuntimeError("executed runner differs from candidate")
    frozen = {
        "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=package, text=True).strip(),
        "runtime_file_hashes": tree(package / "plugins/engineering-harness"),
        "input_hashes": {str(p.relative_to(package)): digest(p) for p in
                         (matrix, matrix.parent / "cases.json", package / "evals/run_natural_matrix.py")},
        "fixture_file_hashes": tree(package / "evals/fixtures"),
    }
    assert_frozen_source(package, frozen)
    return frozen


def assert_frozen_source(package: Path, frozen: dict) -> None:
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=package, text=True).strip()
    dirty = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=all"], cwd=package, text=True)
    if revision != frozen["source_revision"] or dirty:
        raise RuntimeError("candidate revision changed or checkout is dirty")
    if tree(package / "plugins/engineering-harness") != frozen["runtime_file_hashes"]:
        raise RuntimeError("candidate runtime changed")
    if any(digest(package / name) != value for name, value in frozen["input_hashes"].items()):
        raise RuntimeError("candidate evaluation inputs changed")
    if tree(package / "evals/fixtures") != frozen["fixture_file_hashes"]:
        raise RuntimeError("candidate fixtures changed")


def offline_browser_boundary(home, fixture, env, attempts, checkpoint):
    """Fail closed before real auth is copied; use Codex's existing command sandbox."""
    chrome = Path(env.get("EXPERIENCE_CHROMIUM") or shutil.which("chrome-headless-shell") or "")
    if not chrome.is_file():
        raise RuntimeError("offline browser boundary requires EXPERIENCE_CHROMIUM")
    chrome = chrome.resolve()
    scratch = fixture / ".tmp"
    scratch.mkdir()
    # Only tool environment, not Codex service transport, is constrained here.
    tool_env = {"PATH": os.defpath, "LANG": "C.UTF-8", "TMPDIR": str(scratch),
                "EXPERIENCE_CHROMIUM": str(chrome)}
    reads = [home / "skills", home / "plugins/cache", chrome.parent]
    if (home / "agents").exists():
        reads.append(home / "agents")
    host_skills = Path.home() / ".agents/skills"
    if host_skills.is_dir():
        reads.append(host_skills)
    config = '\n'.join([
        'default_permissions = "experience-offline"', 'web_search = "disabled"',
        '[features]', 'network_proxy = true',
        '[shell_environment_policy]', 'inherit = "none"',
        '[shell_environment_policy.set]',
        *[json.dumps(k) + ' = ' + json.dumps(v) for k, v in tool_env.items()],
        '[permissions.experience-offline]', 'extends = ":workspace"',
        '[permissions.experience-offline.filesystem]',
        '":root" = "deny"', '":minimal" = "read"',
        '":slash_tmp" = "deny"', '":tmpdir" = "write"',
        *[json.dumps(str(p)) + ' = "read"' for p in reads],
        '[permissions.experience-offline.network]', 'enabled = true',
        'proxy_url = "http://127.0.0.1:0"', 'socks_url = "http://127.0.0.1:0"',
        '[permissions.experience-offline.network.domains]', '',
    ])
    (home / "config.toml").write_text(config)
    env["TMPDIR"] = str(scratch)
    auth_canary = home / "auth.json"
    outside_canary = home / "boundary-canary"
    auth_canary.write_text("synthetic credential canary; not authentication")
    outside_canary.write_text("synthetic outside-file canary")
    hits = []

    class Sink(socketserver.BaseRequestHandler):
        def handle(self):
            hits.append(True)
            try:
                self.request.sendall(b"HTTP/1.0 200 OK\r\nContent-Length: 0\r\n\r\n")
            except OSError:
                pass

    try:
        with socketserver.ThreadingTCPServer(("127.0.0.1", 0), Sink) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                with tempfile.TemporaryDirectory(prefix="boundary-", dir=scratch) as directory:
                    probe_dir = Path(directory)
                    alias = probe_dir / "auth-alias"
                    alias.symlink_to(auth_canary)
                    probe = probe_dir / "probe.py"
                    probe.write_text("""import json, os, pathlib, socket, urllib.request
result = {}
for name, path in PATHS.items():
    try: pathlib.Path(path).read_bytes(); result[name] = 'readable'
    except OSError: result[name] = 'denied'
for name, proxies in [('direct_http', {}), ('proxy_http', None)]:
    try:
        urllib.request.build_opener(urllib.request.ProxyHandler(proxies)).open(URL, timeout=2)
        result[name] = 'connected'
    except urllib.error.HTTPError as e: result[name] = str(e.code)
    except OSError: result[name] = 'blocked'
try:
    connection = socket.create_connection(('127.0.0.1', PORT), timeout=2)
    connection.close(); result['direct_socket'] = 'connected'
except OSError: result['direct_socket'] = 'blocked'
a, b = socket.socketpair(); a.send(b'x'); assert b.recv(1) == b'x'
result['local_ipc'] = 'ok'
print(json.dumps(result))
""".replace("PATHS", repr({"auth": str(auth_canary), "auth_alias": str(alias),
                            "outside": str(outside_canary)}))
                       .replace("URL", repr(f"http://127.0.0.1:{server.server_address[1]}/"))
                       .replace("PORT", str(server.server_address[1])))
                    prefix = ["codex", "sandbox", "-P", "experience-offline", "-C", str(fixture), "--"]
                    result = command(prefix + ["python3", str(probe)], env, fixture, 30)
                    attempts.append({"command": prefix + ["<synthetic-boundary-probe>"], "result": result})
                    checkpoint()
                    expected = {"auth": "denied", "auth_alias": "denied", "outside": "denied",
                                "direct_http": "blocked", "proxy_http": "403",
                                "direct_socket": "blocked", "local_ipc": "ok"}
                    if result["return_code"] or json.loads(result["stdout"]) != expected or hits:
                        raise RuntimeError("offline browser boundary preflight failed")
                    page, shot = probe_dir / "page.html", probe_dir / "page.png"
                    page.write_text("<!doctype html><h1>Local rendering boundary probe</h1>")
                    result = command(prefix + [str(chrome), "--no-sandbox", "--disable-gpu",
                        "--disable-dev-shm-usage", "--window-size=390,844", "--screenshot=" + str(shot),
                        page.as_uri()], env, fixture, 35)
                    attempts.append({"command": prefix + ["<local-render-probe>"], "result": result})
                    checkpoint()
                    if result["return_code"] or not shot.is_file() or hits:
                        raise RuntimeError("offline browser rendering preflight failed")
                    rendered_hash = digest(shot)
            finally:
                server.shutdown()
                thread.join()
    finally:
        auth_canary.unlink(missing_ok=True)
        outside_canary.unlink(missing_ok=True)
    return {"profile": "experience-offline", "config_sha256": digest(home / "config.toml"),
            "config": config, "preflight": expected, "local_server_connections": len(hits),
            "browser_sha256": digest(chrome), "render_probe_sha256": rendered_hash,
            "limits": "Command sandbox only; Codex service transport is separate. No external endpoint probed."}


def setup(home: Path, package: Path, catalog: Path, arm: str, auth: Path, delegation=True, custom_reviewer=False, *, expected_runtime, attempts, checkpoint, fixture=None, offline_browser=False):
    home.mkdir(parents=True, mode=0o700)
    shutil.copytree(catalog, home / "skills")
    if custom_reviewer:
        (home / "agents").mkdir()
        shutil.copyfile(package / "examples/agents/reviewer.toml", home / "agents/reviewer.toml")
    env = {**os.environ, "CODEX_HOME": str(home)}
    boundary = offline_browser_boundary(home, fixture, env, attempts, checkpoint) if offline_browser else None
    shutil.copyfile(auth, home / "auth.json")
    os.chmod(home / "auth.json", 0o600)
    for args in (["codex", "plugin", "marketplace", "add", str(package)],
                 *([["codex", "plugin", "add", "engineering-harness@davidiw-skills", "--json"]]
                   if arm == "harness" else [])):
        result = command(args, env, package, 120)
        attempts.append({"command": args, "result": result})
        checkpoint()
        if result["return_code"]:
            raise RuntimeError("plugin setup: " + result["stderr"][-1200:])
    inventory_command = ["codex", "plugin", "list", "--json"]
    result = command(inventory_command, env, package, 120)
    attempts.append({"command": inventory_command, "result": result})
    checkpoint()
    if result["return_code"]:
        raise RuntimeError("plugin inventory failed")
    inventory = json.loads(result["stdout"])
    present = any(x["pluginId"].startswith("engineering-harness@")
                  for x in inventory.get("installed", []))
    if present != (arm == "harness"):
        raise RuntimeError("incorrect harness installation state")
    runtimes = list((home / "plugins/cache").glob("*/engineering-harness/*"))
    if arm == "harness" and len(runtimes) != 1:
        raise RuntimeError("expected one installed runtime")
    runtime_hashes = {str(p): verify_runtime(p, expected_runtime)
                      for p in runtimes}
    return {"inventory": inventory, "runtime_excluded_paths": [], "command_boundary": boundary,
            "runtime_file_hashes": runtime_hashes, "catalog_file_hashes": tree(catalog),
            "features": {"skip_host_skill_discovery": True, "multi_agent": delegation},
            "agents": {"enabled": delegation, "max_concurrent_threads_per_session": 2,
                       "role_file_hashes": tree(home / "agents") if (home / "agents").exists() else {},
                       "nested_model_invocations_permitted": delegation}}, env


def parse_events(stdout: str) -> list[dict]:
    events = []
    for line in stdout.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def private_reasoning(item: dict) -> bool:
    return "reasoning" in str(item.get("type", "")).lower() or item.get("channel") == "analysis"


def public_evidence(value):
    """Keep raw streams private; structurally filter every published event surface."""
    if isinstance(value, list):
        return [public_evidence(x) for x in value if not (isinstance(x, dict) and private_reasoning(x))]
    if isinstance(value, dict):
        if private_reasoning(value):
            return {"private_reasoning_omitted": True}
        result = {k: public_evidence(v) for k, v in value.items()
                  if k not in {"stdout", "stderr", "encrypted_content"}}
        for stream in ("stdout", "stderr"):
            if stream in value:
                raw = value[stream]
                result[stream + "_sha256"] = hashlib.sha256(raw.encode()).hexdigest()
                if stream == "stdout":
                    result["stdout_events"] = public_evidence(parse_events(raw))
        if "encrypted_content" in value:
            result["opaque_content_sha256"] = hashlib.sha256(str(value["encrypted_content"]).encode()).hexdigest()
        return result
    if isinstance(value, str):
        if value.startswith("gAAAA") and len(value) > 100:
            return "<opaque content sha256=" + hashlib.sha256(value.encode()).hexdigest() + ">"
        if value.startswith("{"):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                pass
            else:
                if isinstance(parsed, dict) and any(isinstance(v, str) and v.startswith("gAAAA") for v in parsed.values()):
                    return json.dumps(public_evidence(parsed))
    return value


def bind_primary_context(contexts: list[dict], stdout: str) -> None:
    started = next((e for e in parse_events(stdout) if e.get("type") == "thread.started"), {})
    primary_id = started.get("thread_id")
    for context in contexts:
        if primary_id and context.get("id") != primary_id and context["kind"] == "primary":
            # A new CLI session is not a forked child. The assessment must link
            # its visible input to the parent's launch; skill reads prove no role.
            context["kind"] = "separate_session"
            context["agent_configuration"] = "unattributed"
        context["top_level_context_id"] = primary_id


def context_records(home: Path) -> list[dict]:
    """Use final per-context totals; parent CLI usage excludes child usage."""
    contexts = []
    for path in sorted((home / "sessions").rglob("rollout-*.jsonl")):
        context = {"trace_file": str(path.relative_to(home)), "usage": {}, "trace": []}
        calls = {}
        for event in parse_events(path.read_text()):
            payload = event.get("payload", {})
            kind = event.get("type")
            if kind == "session_meta":
                context.update({k: payload[k] for k in ("id", "parent_thread_id", "source", "cli_version", "timestamp") if k in payload})
                context["base_instructions_sha256"] = hashlib.sha256(
                    json.dumps(payload.get("base_instructions"), sort_keys=True).encode()).hexdigest()
            elif kind == "turn_context":
                context["model"] = payload.get("model")
                context["reasoning_effort"] = payload.get("effort")
                context.setdefault("turn_context_hashes", []).append(hashlib.sha256(
                    json.dumps(payload, sort_keys=True).encode()).hexdigest())
            elif kind == "event_msg" and payload.get("type") == "token_count":
                info = payload.get("info")
                if info:
                    context["usage"] = info["total_token_usage"]
            elif kind == "response_item":
                if private_reasoning(payload):
                    continue  # Private/encrypted reasoning is not review evidence.
                # Keep actions/results and assistant/user messages; private base/developer
                # instructions stay hashed rather than republished in evaluation receipts.
                if payload.get("type") == "message" and payload.get("role") not in {"assistant", "user"}:
                    content = "\n".join(x.get("text", "") for x in payload.get("content", []) if isinstance(x, dict))
                    if "### Available skills" in content:
                        roots = dict(re.findall(r"- `([^`]+)` = `([^`]+)`", content))
                        available = content.split("### Available skills", 1)[1].split("</skills_instructions>", 1)[0].strip()
                        files = {}
                        for declared in re.findall(r"\(file: ([^)]+)\)", available):
                            alias, _, relative = declared.partition("/")
                            resolved = Path(roots[alias]) / relative if alias in roots else Path(declared)
                            files[declared] = {"resolved": str(resolved), "exists": resolved.is_file(),
                                               "tree_hashes": tree(resolved.parent) if resolved.is_file() else {}}
                        context["catalog_declaration"] = {"roots": roots, "available": available, "files": files}
                    continue
                context["trace"].append(event)
                if payload.get("type") == "agent_message":
                    context.setdefault("agent_message_inputs", []).append({
                        "author": payload.get("author"), "recipient": payload.get("recipient"),
                        "opaque": any(i.get("type") == "encrypted_content" for i in payload.get("content", [])),
                        "sha256": hashlib.sha256(json.dumps(payload.get("content"), sort_keys=True).encode()).hexdigest()})
                if payload.get("type") in {"function_call", "custom_tool_call"}:
                    calls[payload.get("call_id")] = payload
            elif kind == "event_msg" and payload.get("type") in {"task_complete", "task_started", "task_aborted", "error"}:
                context["trace"].append(event)
        started = [e["timestamp"] for e in context["trace"] if e.get("payload", {}).get("type") == "task_started" and e.get("timestamp")]
        ended = [e["timestamp"] for e in context["trace"] if e.get("payload", {}).get("type") == "task_complete" and e.get("timestamp")]
        if started and ended:
            context["wall_seconds"] = (datetime.fromisoformat(ended[-1].replace("Z", "+00:00")) - datetime.fromisoformat(started[0].replace("Z", "+00:00"))).total_seconds()
        context["completed"] = any(e.get("type") == "event_msg" and e.get("payload", {}).get("type") == "task_complete" for e in context["trace"])
        usage = context["usage"]
        usage["uncached_input_tokens"] = usage.get("input_tokens", 0) - usage.get("cached_input_tokens", 0)
        skills, refs, observed_refs, tool_calls = set(), set(), set(), []
        for event in context["trace"]:
            item = event.get("payload", {})
            if item.get("type") in {"function_call", "custom_tool_call"}:
                tool_calls.append({"name": item.get("name"), "arguments": item.get("arguments", item.get("input"))})
            if item.get("type") not in {"function_call_output", "custom_tool_call_output"}:
                continue
            call = calls.get(item.get("call_id"), {})
            arguments = str(call.get("arguments", call.get("input", "")))
            output = str(item.get("output", ""))
            if re.search(r"read_text|read_bytes|\bcat\b|\bsed\b|\bhead\b|\btail\b", arguments):
                skills.update(re.findall(r"(?:^|\\n|\n)name: ([a-z][a-z-]+)", output))
                refs.update(re.findall(r"(?:references/)[A-Za-z0-9_./-]+\.(?:md|json)", arguments + "\n" + output))
                observed_refs.update(re.findall(r"(?:references/)[A-Za-z0-9_./-]+\.(?:md|json)", arguments))
        context["skill_bodies_observed"] = sorted(skills)
        context["reference_read_candidates"] = sorted(refs)
        context["reference_paths_in_read_commands"] = sorted(observed_refs)
        context["tool_calls"] = tool_calls
        source = context.get("source")
        parent = context.get("parent_thread_id")
        if isinstance(source, dict):
            parent = parent or source.get("subagent", {}).get("thread_spawn", {}).get("parent_thread_id")
        role = source.get("subagent", {}).get("thread_spawn", {}).get("agent_role") if isinstance(source, dict) else None
        context["agent_role"] = role
        context["agent_configuration"] = ("custom" if role and (home / "agents" / (role + ".toml")).is_file()
                                          else "generic" if parent else "primary")
        context["parent_context_id"] = parent
        context["kind"] = "delegated" if parent else "primary"
        context["review_skill_bodies_observed"] = sorted(skills & {"security-assurance", "privacy-assurance"})
        # Review skill loading cannot turn a builder into an independent reviewer.
        # Behavioral assessments assign builder/reviewer roles from handoff + actions.
        contexts.append(context)
    return contexts


def trial(spec, package, source_root, output, number, arm, auth, catalog, model, effort, timeout, frozen=None, command_boundary=None):
    lane = f"{spec['id']}-{arm}-trial{number}"
    private = output / "private" / lane
    private.mkdir(parents=True)
    home, fixture = private / "codex-home", private / "fixture"
    record = {"case_id": spec["id"], "arm": arm, "trial": number, "model": model,
              "reasoning_effort": effort, "timeout_seconds": timeout,
              "command_boundary": command_boundary, "setup_commands": []}
    def checkpoint():
        (private / "record.json").write_text(json.dumps(record, indent=2, ensure_ascii=False))
    try:
        frozen = frozen or frozen_source(package, package / "evals/assurance-matrix.json")
        record["package_revision"] = frozen["source_revision"]
        assert_frozen_source(package, frozen)
        source = source_root / spec["fixture"]
        shutil.copytree(source, fixture, ignore=shutil.ignore_patterns("__pycache__"))
        git = ["git", "-c", "user.name=eval", "-c", "user.email=eval@invalid"]
        for args in (["git", "init", "-q"], git + ["add", "."], git + ["commit", "-qm", "baseline"]):
            subprocess.run(args, cwd=fixture, check=True)
        before = tree(fixture)
        record["fixture_before_hashes"] = before
        setup_info, env = setup(home, package, catalog, arm, auth, spec.get("delegation_available", True), spec.get("custom_reviewer", False),
                                expected_runtime=frozen["runtime_file_hashes"], attempts=record["setup_commands"], checkpoint=checkpoint,
                                fixture=fixture, offline_browser=command_boundary == "offline-browser")
        record["setup"] = setup_info
        checkpoint()
        prompt = (spec.get("context", "") + "\n\n" + spec["request"]).strip()
        role_args = (["-c", "agents.reviewer.config_file=" + json.dumps(str(home / "agents/reviewer.toml")),
                      "-c", 'agents.reviewer.description="Independent read-only reviewer"']
                     if spec.get("custom_reviewer") else [])
        environment_rules = ENVIRONMENT_RULES
        if not spec.get("delegation_available", True):
            environment_rules += " New agent contexts and nested model invocations are disabled and not permitted in this environment."
        permission_args = (["--strict-config"] if command_boundary == "offline-browser" else
                           ["--sandbox", "workspace-write", "-c", "sandbox_workspace_write.network_access=false"])
        cmd = ["codex", "-a", "never", "exec", "--json", "--skip-git-repo-check",
               *permission_args, "--model", model,
               "-c", f"model_reasoning_effort={effort}", "--enable", "skip_host_skill_discovery",
               ("--enable" if spec.get("delegation_available", True) else "--disable"), "multi_agent", "-c", "agents.enabled=" + str(spec.get("delegation_available", True)).lower(),
               "-c", "agents.max_concurrent_threads_per_session=2",
               "-c", f"agents.default_subagent_model={model}",
               "-c", f"agents.default_subagent_reasoning_effort={effort}", *role_args,
               "-c", "developer_instructions=" + json.dumps(environment_rules), "-C", str(fixture), prompt]
        record.update({"prompt": prompt, "command": cmd[:-1] + ["<PROMPT>"]})
        checkpoint()
        result = command(cmd, env, fixture, timeout)
        record.update({"result": result, "wall_seconds": result["ended_at"] - result["started_at"]})
        checkpoint()
        contexts = context_records(home)
        bind_primary_context(contexts, result["stdout"])
        record["contexts"] = contexts
        record["context_count"] = len(contexts)
        record["aggregate_usage"] = {k: sum(c["usage"].get(k, 0) for c in contexts)
                                     for k in (*TOKEN_KEYS, "uncached_input_tokens")}
        checkpoint()
        after = tree(fixture)
        diff = subprocess.check_output(["git", "diff", "HEAD", "--no-ext-diff", "--binary"], cwd=fixture, text=True)
        untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard", "-z"], cwd=fixture, text=True).split("\0")
        for name in untracked:
            if name and "__pycache__" not in Path(name).parts and (fixture / name).is_file():
                diff += f"\n--- untracked {name} ---\n" + (fixture / name).read_text(errors="replace")
        record.update({"fixture_after_hashes": after, "fixture_diff": diff})
        checkpoint()
        runtimes = list((home / "plugins/cache").glob("*/engineering-harness/*"))
        if len(runtimes) != (1 if arm == "harness" else 0):
            raise RuntimeError("post-run installed runtime inventory changed")
        record["post_runtime_file_hashes"] = {
            str(p): verify_runtime(p, frozen["runtime_file_hashes"]) for p in runtimes}
        assert_frozen_source(package, frozen)
        if not contexts or any(not c["usage"].get("input_tokens") or not c["completed"] for c in contexts):
            record["measurement_incomplete"] = True
    except Exception as error:
        record.update({"error": str(error), "setup_or_trial_failed": True})
    finally:
        (home / "auth.json").unlink(missing_ok=True)
        # Preserve partial child/parent traces even on failure.
        if "contexts" not in record and home.exists():
            try:
                record["contexts"] = context_records(home)
            except Exception as error:
                record["context_collection_error"] = str(error)
    checkpoint()
    return record


def redact(value, replacements, secrets):
    if isinstance(value, str):
        for secret in secrets:
            value = value.replace(secret, "<REDACTED>")
        for source, replacement in sorted(replacements.items(), key=lambda p: -len(p[0])):
            value = value.replace(source, replacement)
        return value
    if isinstance(value, list):
        return [redact(x, replacements, secrets) for x in value]
    if isinstance(value, dict):
        return {redact(k, replacements, secrets): redact(v, replacements, secrets) for k, v in value.items()}
    return value


def credential_strings(auth):
    result = []
    if isinstance(auth, dict):
        for key, value in auth.items():
            if key.lower() in {"access_token", "refresh_token", "id_token", "api_key", "openai_api_key", "account_id"} and isinstance(value, str) and len(value) > 8:
                result.append(value)
            else:
                result.extend(credential_strings(value))
    elif isinstance(auth, list):
        for value in auth:
            result.extend(credential_strings(value))
    return result


def redaction_paths(output, package, matrix, catalog):
    # A relative "." is a path, not a request to redact every punctuation mark.
    return {str(Path(output).resolve()): "<OUTPUT>",
            str(Path(package).resolve()): "<PACKAGE>",
            str(Path(matrix).resolve().parent): "<EVALS>",
            str(Path(catalog).resolve()): "<CATALOG>",
            str(Path(__file__).resolve().parent): "<RUNNER>",
            str(Path.home()): "<USER_HOME>"}


def main():
    parser = argparse.ArgumentParser()
    for name in ("package", "matrix", "output", "catalog"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--auth", type=Path, default=Path.home() / ".codex/auth.json")
    parser.add_argument("--case", action="append", dest="case_ids")
    parser.add_argument("--arm", action="append", choices=["control", "harness"])
    parser.add_argument("--trials", type=int)
    parser.add_argument("--max-workers", type=int, default=2)
    args = parser.parse_args()
    if not 1 <= args.max_workers <= 2:
        parser.error("max-workers must be 1 or 2")
    if args.output.exists():
        parser.error("output must be new; preserve every attempt")
    matrix = json.loads(args.matrix.read_text())
    if matrix.get("sandbox_network_access") or matrix.get("command_boundary") not in (None, "offline-browser"):
        parser.error("unrestricted network or unknown command boundary is not supported")
    cases = {c["id"]: c for c in json.loads((args.matrix.parent / "cases.json").read_text())["cases"]}
    selected = args.case_ids or matrix["case_ids"]
    if not set(selected) <= set(matrix["case_ids"]):
        parser.error("case is outside the frozen matrix")
    frozen = frozen_source(args.package, args.matrix)
    args.output.mkdir(parents=True, mode=0o700)
    # Catalog is copied once, then that exact tree is copied into every fresh home.
    pinned = args.output / "pinned-catalog"
    shutil.copytree(args.catalog, pinned, ignore=shutil.ignore_patterns("__pycache__", ".git"))
    jobs = [(cases[c], arm, n) for c in selected for arm in (args.arm or matrix["conditions"])
            for n in range(1, 1 + (args.trials or matrix.get("case_trials", {}).get(c, matrix["trials"])))]
    run = {**frozen,
           "cli_version": subprocess.check_output(["codex", "--version"], text=True).strip(),
           "matrix_sha256": digest(args.matrix), "cases_sha256": digest(args.matrix.parent / "cases.json"),
           "runner_sha256": digest(Path(__file__)), "catalog_file_hashes": tree(pinned),
           "runtime_file_hashes": tree(args.package / "plugins/engineering-harness"),
           "max_workers": args.max_workers, "planned_trials": len(jobs), "selected_cases": selected,
           "selected_arms": args.arm or matrix["conditions"], "trial_override": args.trials}
    records = []
    print(f"prepared {len(jobs)} trials; concurrency={args.max_workers}", flush=True)
    interrupted = False
    try:
        with ThreadPoolExecutor(max_workers=args.max_workers) as pool:
            futures = {pool.submit(trial, case, args.package, args.matrix.parent, args.output,
                                   n, arm, args.auth, pinned, matrix["model"], matrix["reasoning_effort"],
                                   matrix["timeout_seconds"], frozen, matrix.get("command_boundary")): (case["id"], arm, n) for case, arm, n in jobs}
            for future in as_completed(futures):
                key = futures[future]
                record = future.result()
                records.append(record)
                print(f"done {key}: rc={record.get('result', {}).get('return_code')} contexts={record.get('context_count')} error={record.get('error', '')}", flush=True)
    except KeyboardInterrupt:
        interrupted = True
        records = [json.loads(p.read_text()) for p in (args.output / "private").glob("*/record.json")]
    run["interrupted"] = interrupted
    records.sort(key=lambda r: (r["case_id"], r["arm"], r["trial"]))
    replacements = redaction_paths(args.output, args.package, args.matrix, args.catalog)
    public = args.output / "public"
    public.mkdir()
    secrets = credential_strings(json.loads(args.auth.read_text()))
    for name, value in (("manifest.json", records), ("run.json", run)):
        (public / name).write_text(json.dumps(redact(public_evidence(value), replacements, secrets), indent=2, ensure_ascii=False))
    failed = interrupted or len(records) != len(jobs) or any(r.get("setup_or_trial_failed") or r.get("measurement_incomplete")
                 or r.get("result", {}).get("return_code") != 0 or r.get("result", {}).get("timed_out") for r in records)
    executed = sum("result" in r for r in records)
    print(f"recorded {len(records)}/{len(jobs)}; executions with result={executed}; output={args.output}", flush=True)
    return 2 if failed else 0


if __name__ == "__main__":
    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, interrupt)
    raise SystemExit(main())
