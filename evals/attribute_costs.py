#!/usr/bin/env python3
"""Read retained matrix traces; report counters and bounded attribution proxies.

Never emits message contents or private reasoning. Does not score behavior.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import statistics


TOKEN_KEYS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens")
ASSURANCE = {"security-assurance", "privacy-assurance"}
ROUTER = "using-engineering-harness"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def native_context(header, primary_id, role_files):
    """Use native identity plus retained configuration evidence, never a role name alone."""
    source = header.get("source")
    subagent = source.get("subagent") if isinstance(source, dict) else None
    spawn = subagent.get("thread_spawn") if isinstance(subagent, dict) else None
    spawn = spawn if isinstance(spawn, dict) else {}
    parent = header.get("parent_thread_id") or spawn.get("parent_thread_id")
    kind = ("delegated" if parent else "primary" if primary_id and header.get("id") == primary_id
            else "separate_session" if primary_id else "unavailable")
    metadata = header if "agent_role" in header else spawn
    role = metadata.get("agent_role")
    definition = role_files.get(role + ".toml") if isinstance(role, str) else None
    configuration = ("primary" if kind == "primary" else "custom" if definition
                     else "generic" if "agent_role" in metadata and role is None
                     else "unavailable")
    return {"kind": kind, "configuration": configuration, "agent_role": role,
            "role_definition_sha256": definition}


def context_completed(events, inherited_turns):
    """An earlier or inherited completion cannot close a later native turn."""
    latest = None
    completed = False
    for event in events:
        if event.get("type") != "event_msg":
            continue
        payload = event.get("payload", {})
        turn = payload.get("turn_id")
        if not turn:
            if payload.get("type") in ("task_started", "task_complete", "turn_aborted", "task_aborted"):
                latest, completed = None, False
            continue
        if turn in inherited_turns:
            continue
        if payload.get("type") == "task_started":
            latest, completed = turn, False
        elif turn == latest and payload.get("type") in ("task_complete", "turn_aborted", "task_aborted"):
            completed = payload["type"] == "task_complete"
    return latest is not None and completed


def usage_sum(rows):
    rows = list(rows)
    for row in rows:
        if any(type(row.get(k, 0)) is not int or row.get(k, 0) < 0 for k in TOKEN_KEYS):
            raise ValueError("Invalid token counter")
        uncached = row.get("input_tokens", 0) - row.get("cached_input_tokens", 0)
        if uncached < 0 or row.get("uncached_input_tokens", uncached) != uncached:
            raise ValueError("Invalid uncached token counter")
    result = {k: sum(r.get(k, 0) for r in rows) for k in TOKEN_KEYS}
    result["uncached_input_tokens"] = result["input_tokens"] - result["cached_input_tokens"]
    return result


def action(item):
    if item["type"] == "message":
        return "final" if item.get("phase") == "final_answer" else "commentary"
    name = item.get("name", "")
    argument = item.get("arguments", item.get("input", ""))
    if "wait" in name or "send_message" in name:
        return "coordination"
    if "spawn" in name:
        return "launch"
    if any(s in argument for s in ("apply_patch", "write_text", "cat >", "mkdir")):
        return "write_artifacts_or_code"
    if any(s in argument for s in ("python", "pytest", "unittest")):
        return "checks"
    return "reads_or_other_tools"


def explicit_reads(item, runtime_files):
    """Recognize literal shell read commands, not links inside generated prose."""
    argument = item.get("arguments", item.get("input", ""))
    commands = re.findall(r'cmd\s*:\s*"((?:\\.|[^"\\])*)"', argument)
    found = []
    for command in commands:
        for segment in re.split(r"&&|;|\\n", command):
            if not re.match(r"\s*(?:cat|sed|head|tail|nl)\s", segment):
                continue
            if re.match(r"\s*cat\s*>", segment):
                continue
            found.extend(p for p in runtime_files if p in segment)
    return found


def context_cost(context, events, runtime_files):
    pending = []
    invocations = []
    reads = Counter()
    read_calls = {}
    loaded = set()
    messages = Counter()
    rounds = Counter()
    seen_responses = {}
    for event in events:
        item = event.get("payload", {})
        kind = item.get("type")
        if event["type"] == "response_item":
            if kind in ("custom_tool_call", "function_call"):
                pending.append(item)
                paths = explicit_reads(item, runtime_files)
                read_calls[item.get("call_id")] = paths
                rounds[item.get("name", "")] += 1
            elif kind in ("custom_tool_call_output", "function_call_output"):
                # These are requested reads whose tool returned, not exact read-byte proof.
                for path in read_calls.pop(item.get("call_id"), []):
                    reads[path] += 1
                    if path.endswith("/SKILL.md"):
                        loaded.add(path.split("/")[-2])
            elif kind == "message" and item.get("role") == "assistant":
                pending.append(item)
                text = "".join(x.get("text", "") for x in item.get("content", [])
                               if x.get("type") == "output_text")
                messages[action(item) + "_bytes"] += len(text.encode())
        if event["type"] != "token_usage_record":
            continue
        response = item["response_id"]
        if response in seen_responses:
            if seen_responses[response] != usage_sum([item["usage"]]):
                raise ValueError("Conflicting duplicate response counters")
            continue
        seen_responses[response] = usage_sum([item["usage"]])
        stage = ("reviewer" if context["kind"] != "primary" or loaded & ASSURANCE else
                 "implementation_owner" if loaded - {ROUTER} else
                 "router" if ROUTER in loaded else "discovery_or_competing_skill")
        invocations.append({"response_id": response, "stage": stage, "action": "+".join(sorted({action(x) for x in pending}))
                            or "unattributed", "usage": item["usage"]})
        pending = []
    measured = usage_sum(x["usage"] for x in invocations)
    expected = usage_sum([context["usage"]])
    if measured != expected:
        raise ValueError(f"Invocation counters do not reconcile for {context['id']}")
    return {"kind": context["kind"], "configuration": context["agent_configuration"],
            "model": context["model"], "effort": context["reasoning_effort"],
            "usage": measured, "wall_seconds": context["wall_seconds"],
            "skills_observed": context["skill_bodies_observed"], "messages": dict(messages),
            "read_requests": dict(reads), "duplicate_read_requests": sum(n - 1 for n in reads.values()),
            "requested_file_bytes": sum(runtime_files[p] * n for p, n in reads.items()),
            "coordination_calls": {k: n for k, n in rounds.items()
                                   if any(s in k for s in ("spawn", "followup", "wait", "send_message"))},
            "invocations": invocations}


def aggregate(trials):
    contexts = [c for t in trials for c in t["contexts"]]
    by_action = defaultdict(list)
    by_stage = defaultdict(list)
    for c in contexts:
        for i in c["invocations"]:
            by_action[i["action"]].append(i["usage"])
            by_stage[i["stage"]].append(i["usage"])
    return {"trials": len(trials), "contexts": len(contexts),
            "usage": usage_sum(c["usage"] for c in contexts),
            "wall_seconds_median": statistics.median(t["wall_seconds"] for t in trials),
            "model_invocations": sum(len(c["invocations"]) for c in contexts),
            "by_action": {k: usage_sum(v) for k, v in by_action.items()},
            "by_stage": {k: usage_sum(v) for k, v in by_stage.items()},
            "skill_bodies_read": sum(len(c["skills_observed"]) for c in contexts),
            "runtime_read_requests": sum(sum(c["read_requests"].values()) for c in contexts),
            "duplicate_read_requests": sum(c["duplicate_read_requests"] for c in contexts),
            "final_message_bytes": sum(c["messages"].get("final_bytes", 0) for c in contexts),
            "commentary_bytes": sum(c["messages"].get("commentary_bytes", 0) for c in contexts)}


def added_artifacts(fixture, before, after):
    """Measure every added format; names are hints, not semantic packet proof."""
    artifacts = {}
    for name, digest in after.items():
        if name in before:
            continue
        data = relative_file(fixture, name).read_bytes()
        if sha(data) != digest:
            raise ValueError(f"Changed retained artifact: {name}")
        artifacts[name] = {"bytes": len(data), "sha256": digest,
                           "packet_name": any(s in Path(name).name.lower()
                                              for s in ("packet", "handoff"))}
    return artifacts


def relative_file(root, name):
    path = Path(name)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Evidence path must remain within its root")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError("Evidence path escapes its root")
    return resolved


def verify_tree(root, expected):
    names = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()
             and not ({".git", "__pycache__"} & set(p.relative_to(root).parts))}
    if names != set(expected):
        raise ValueError("Retained file inventory changed")
    sizes = {}
    for name, digest in expected.items():
        data = relative_file(root, name).read_bytes()
        if sha(data) != digest:
            raise ValueError(f"Changed retained file: {name}")
        sizes[name] = len(data)
    return sizes


def trial_key(record):
    if type(record["trial"]) is not int or record["trial"] < 1:
        raise ValueError("Invalid trial number")
    return record["case_id"], record["arm"], record["trial"]


def analyze(run, runtime, integrity=None, integrity_sha256=None):
    run, runtime = run.resolve(), runtime.resolve()
    if (integrity is None) != (integrity_sha256 is None):
        raise ValueError("Supply both retained integrity inventory and its pinned SHA256")
    expected_digests = None
    if integrity is not None:
        data = integrity.read_bytes()
        if sha(data) != integrity_sha256:
            raise ValueError("Integrity inventory does not match pinned SHA256")
        expected_digests = json.loads(data)
        if not isinstance(expected_digests, dict):
            raise ValueError("Integrity inventory must map relative paths to SHA256 digests")

    def evidence(path):
        name = str(path.relative_to(run))
        data = relative_file(run, name).read_bytes()
        if expected_digests is not None and expected_digests.get(name) != sha(data):
            raise ValueError(f"Evidence absent from or changed since retained inventory: {name}")
        return data

    plan = json.loads(evidence(run / "public/run.json"))
    manifest = json.loads(evidence(run / "public/manifest.json"))
    expected_trials = [trial_key(r) for r in manifest]
    expected_pairs = {(c, a) for c in plan["selected_cases"] for a in plan["selected_arms"]}
    if (plan.get("interrupted") or not expected_trials
            or len(expected_trials) != plan["planned_trials"]
            or len(set(expected_trials)) != len(expected_trials)
            or {k[:2] for k in expected_trials} != expected_pairs):
        raise ValueError("Incomplete or inconsistent planned trial inventory")
    for pair in expected_pairs:
        numbers = sorted(k[2] for k in expected_trials if k[:2] == pair)
        count = plan.get("trial_override") or len(numbers)
        if numbers != list(range(1, count + 1)):
            raise ValueError("Trial numbers do not reconcile with plan")
    sizes = verify_tree(runtime, plan["runtime_file_hashes"])
    files = {name: size for name, size in sizes.items() if name.endswith(".md")}
    trials = []
    revisions = set()
    seen_trials = set()
    seen_contexts = set()
    seen_invocations = set()
    for path in sorted((run / "private").glob("*/record.json")):
        record_data = evidence(path)
        record = json.loads(record_data)
        key = trial_key(record)
        if key in seen_trials or key not in expected_trials:
            raise ValueError("Duplicated or unplanned trial")
        seen_trials.add(key)
        if ("return_code" not in record.get("result", {})
                or record.get("measurement_incomplete") or record.get("setup_or_trial_failed")
                or not record.get("contexts") or any(not c.get("completed") for c in record["contexts"])):
            raise ValueError(f"Incomplete trial evidence: {path.parent.name}")
        if record["package_revision"] != plan["source_revision"]:
            raise ValueError("Trial revision differs from frozen plan")
        if record.get("context_count") != len(record["contexts"]):
            raise ValueError("Context count does not reconcile")
        home = path.parent / "codex-home"
        observed_traces = {str(p.relative_to(home)) for p in (home / "sessions").rglob("rollout-*.jsonl")}
        if observed_traces != {c["trace_file"] for c in record["contexts"]}:
            raise ValueError("Raw context inventory does not reconcile")
        stdout_events = [json.loads(line) for line in record.get("result", {}).get("stdout", "").splitlines()
                         if line.strip().startswith("{")]
        primary_id = next((e.get("thread_id") for e in stdout_events if e.get("type") == "thread.started"), None)
        role_files = record.get("setup", {}).get("agents", {}).get("role_file_hashes", {})
        native_traces = {}
        for trace_name in observed_traces:
            data = evidence(relative_file(home, trace_name))
            events = [json.loads(line) for line in data.splitlines()]
            headers = [e.get("payload", {}) for e in events if e.get("type") == "session_meta"]
            identity = headers[0].get("id") if headers else None
            if not identity or identity in native_traces:
                raise ValueError("Missing or duplicate native context identity")
            native_traces[identity] = (data, events, headers)
        context_total = usage_sum(c["usage"] for c in record["contexts"])
        if "aggregate_usage" not in record or context_total != usage_sum([record["aggregate_usage"]]):
            raise ValueError("Trial counters do not reconcile")
        public_record = next(r for r in manifest if trial_key(r) == key)
        if (public_record.get("context_count") != record["context_count"]
                or usage_sum([public_record["aggregate_usage"]]) != context_total):
            raise ValueError("Public and private trial counters differ")
        revisions.add(record["package_revision"])
        contexts = []
        seen_traces = set()
        for context in record["contexts"]:
            if context["trace_file"] in seen_traces:
                raise ValueError("Missing or duplicate context identity/trace")
            seen_traces.add(context["trace_file"])
            trace = relative_file(path.parent / "codex-home", context["trace_file"])
            trace_data = evidence(trace)
            events = [json.loads(line) for line in trace_data.splitlines()]
            headers = [e.get("payload", {}) for e in events if e.get("type") == "session_meta"]
            # Forked traces can retain ancestor headers. The first header identifies
            # this file; the historical runner flattened later headers into record.id.
            identity = headers[0].get("id") if headers else None
            inherited_turns = set()
            for header in headers[1:]:
                ancestor = header.get("id")
                if ancestor == identity:
                    continue
                if ancestor not in native_traces:
                    raise ValueError("Inherited context history lacks its native trace")
                inherited_turns.update(e.get("payload", {}).get("turn_id")
                                       for e in native_traces[ancestor][1]
                                       if e.get("type") == "event_msg")
            completed = context_completed(events, inherited_turns)
            if not identity or identity in seen_contexts or not completed:
                raise ValueError("Raw context identity or completion does not reconcile")
            if context.get("id") not in {h.get("id") for h in headers}:
                raise ValueError("Recorded context identity is absent from raw headers")
            seen_contexts.add(identity)
            native = native_context(headers[0], primary_id, role_files)
            cost = context_cost({**context, **native}, events, files)
            for invocation in cost["invocations"]:
                if invocation["response_id"] in seen_invocations:
                    raise ValueError("Invocation appears in multiple contexts")
                seen_invocations.add(invocation["response_id"])
            cost["id"] = identity
            cost["recorded_id"] = context.get("id")
            cost["identity_source"] = "first raw session header"
            cost["recorded_kind"] = context.get("kind")
            cost["recorded_configuration"] = context.get("agent_configuration")
            cost.update(native)
            cost["configuration_source"] = "first raw header, top-level thread.started, retained setup role hashes"
            cost["trace_sha256"] = sha(trace_data)
            contexts.append(cost)
        shared = Counter(p for c in contexts for p in c["read_requests"])
        verify_tree(path.parent / "fixture", record["fixture_after_hashes"])
        artifacts = added_artifacts(path.parent / "fixture", record["fixture_before_hashes"],
                                    record["fixture_after_hashes"])
        docs = {name: value for name, value in artifacts.items() if name.endswith(".md")}
        trials.append({"case_id": record["case_id"], "arm": record["arm"], "trial": record["trial"],
                       "record_sha256": sha(record_data), "wall_seconds": record["wall_seconds"],
                       "return_code": record["result"].get("return_code"),
                       "timed_out": record["result"].get("timed_out", False),
                       "measurement_incomplete": False, "setup_or_trial_failed": False,
                       "contexts_completed": True,
                       "contexts": contexts, "added_markdown": docs, "added_artifacts": artifacts,
                       "runtime_paths_read_by_multiple_contexts": {k: n for k, n in shared.items() if n > 1}})
    if seen_trials != set(expected_trials):
        raise ValueError("Retained trials do not match planned inventory")
    arms = {a: aggregate([t for t in trials if t["arm"] == a]) for a in sorted({t["arm"] for t in trials})}
    cases = []
    for case in sorted({t["case_id"] for t in trials}):
        row = {"case_id": case, "arms": {a: aggregate([t for t in trials if t["case_id"] == case and t["arm"] == a]) for a in arms}}
        if set(arms) == {"control", "harness"}:
            row["delta"] = {k: row["arms"]["harness"]["usage"][k] - row["arms"]["control"]["usage"][k]
                            for k in row["arms"]["harness"]["usage"]}
        cases.append(row)
    return {"candidate_shas": sorted(revisions), "arms": arms,
            "analyzer_sha256": sha(Path(__file__).read_bytes()),
            "execution_failure_count": sum(t["return_code"] != 0 or t["timed_out"] for t in trials),
            "integrity": {"status": "verified_against_supplied_inventory" if expected_digests is not None else "unverified",
                          "inventory_sha256": integrity_sha256,
                          "limit": "Caller must pin an independently retained inventory. Without it, hashes are current fingerprints, not proof of original trace/record integrity."},
            "cases_ranked_by_output_delta": sorted(cases, key=lambda x: x.get("delta", {}).get("output_tokens", 0), reverse=True),
            "runtime_markdown_file_bytes": files, "trials": trials,
            "limitations": ["Token counters are measured per invocation/context and reconciled; stage/action labels are observational proxies, not causal attribution to individual instructions.",
                            "Stages include all retained context and tool/schema overhead. File sizes and message/artifact sizes are bytes, not tokenizer counts.",
                            "Read requests recognize literal cat/sed/head/tail/nl commands. Dynamic, partial, failed or mixed commands limit exact read attribution; file-byte totals are full-file upper bounds for recognized requests.",
                            "Duplicate reads across independent contexts may be necessary and are not automatically waste.",
                            "Writing invocations include production code and necessary tests as well as documentation. Their tokens are not all removable verbosity.",
                            "Context wall includes waits and overlapping children. Actual review rounds, late blockers and initial-review misses require the retained behavioral assessments; spawn counts alone do not establish convergence.",
                            "Private reasoning and message contents are not emitted. No behavioral scoring is performed."]}


def export_contexts(receipt_contexts, normalized_contexts):
    """Join a receipt to analyze() results by trace digest, never flattened ID/order.

    Preserve historical identity/kind separately. This updates context metadata
    only; callers retain their source identity, behavioral assessments and costs.
    """
    by_trace = {c["trace_sha256"]: c for c in normalized_contexts}
    ids = [c["id"] for c in normalized_contexts]
    traces = [c["trace_sha256"] for c in receipt_contexts]
    if (len(by_trace) != len(normalized_contexts) or len(set(ids)) != len(ids)
            or not all(ids) or len(set(traces)) != len(traces)
            or set(traces) != set(by_trace)):
        raise ValueError("Receipt/native context inventory does not reconcile")
    exported = []
    for context in receipt_contexts:
        native = by_trace[context["trace_sha256"]]
        if (native.get("identity_source") != "first raw session header"
                or context.get("recorded_id", context.get("id")) != native["recorded_id"]
                or context.get("recorded_kind", context.get("kind")) != native["recorded_kind"]):
            raise ValueError("Receipt context differs from normalized historical metadata")
        exported.append({**context, **{key: native[key] for key in
                         ("id", "recorded_id", "identity_source", "kind", "recorded_kind")}})
    return exported


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("run", "runtime", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--integrity", type=Path, help="Retained run-relative file-to-SHA256 inventory")
    parser.add_argument("--integrity-sha256", help="Independently pinned inventory SHA256")
    args = parser.parse_args()
    report = analyze(args.run, args.runtime, args.integrity, args.integrity_sha256)
    with args.output.open("x") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps({"integrity": report["integrity"]["status"],
                      "execution_failure_count": report["execution_failure_count"],
                      "arms": {a: {k: v for k, v in row.items() if k in ("trials", "contexts", "usage", "model_invocations")}
                               for a, row in report["arms"].items()}}, indent=2))


if __name__ == "__main__":
    main()
