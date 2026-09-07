#!/usr/bin/env python3
"""Private bounded natural-prompt evaluation runner."""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, signal, subprocess, sys, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ACTIVE = set()
STOP = threading.Event()
ACTIVE_LOCK = threading.Lock()
def kill_active(*_):
    STOP.set()
    with ACTIVE_LOCK:
        active = list(ACTIVE)
    for p in active:
        try: os.killpg(p.pid, signal.SIGTERM)
        except ProcessLookupError: pass
    time.sleep(2)
    for p in active:
        try: os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError: pass
    raise KeyboardInterrupt
signal.signal(signal.SIGINT, kill_active); signal.signal(signal.SIGTERM, kill_active)

def digest(path):
    h=hashlib.sha256()
    if path.is_file(): h.update(path.read_bytes()); return h.hexdigest()
    for p in sorted(path.rglob("*")):
        if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts: h.update(str(p.relative_to(path)).encode()+b"\0"); h.update(p.read_bytes())
    return h.hexdigest()
def tree(path): return {str(p.relative_to(path)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(path.rglob("*")) if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts}
def command(args,env,cwd,timeout):
    started=time.time()
    with ACTIVE_LOCK:
        if STOP.is_set(): raise RuntimeError("evaluation cancelled")
        p=subprocess.Popen(args,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        ACTIVE.add(p)
    timed=False
    try:
        out,err=p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed=True; os.killpg(p.pid,signal.SIGTERM)
        try: out,err=p.communicate(timeout=5)
        except subprocess.TimeoutExpired: os.killpg(p.pid,signal.SIGKILL); out,err=p.communicate()
    finally:
        with ACTIVE_LOCK: ACTIVE.discard(p)
    return {"stdout":out,"stderr":err,"return_code":p.returncode,"timed_out":timed,"started_at":started,"ended_at":time.time()}
def setup(home,package,competing,arm,auth):
    home.mkdir(parents=True,mode=0o700); os.chmod(home,0o700); shutil.copyfile(auth,home/"auth.json"); os.chmod(home/"auth.json",0o600); shutil.copytree(competing.parent,home/"skills"/"diagnosing-bugs"); env={**os.environ,"CODEX_HOME":str(home)}
    r=command(["codex","plugin","marketplace","add",str(package)],env,package,120)
    if r["return_code"]: raise RuntimeError("marketplace add: "+r["stderr"][-1000:])
    if arm=="harness":
        r=command(["codex","plugin","add","engineering-harness@davidiw-skills","--json"],env,package,120)
        if r["return_code"]: raise RuntimeError("plugin add: "+r["stderr"][-1000:])
    r=command(["codex","plugin","list","--json"],env,package,120)
    if r["return_code"]: raise RuntimeError("inventory: "+r["stderr"][-1000:])
    inv=json.loads(r["stdout"]); has=any(x["pluginId"].startswith("engineering-harness@") for x in inv.get("installed",[]))
    if has != (arm=="harness"): raise RuntimeError(f"inventory harness installed={has}, expected={arm=='harness'}")
    cfg=(home/"config.toml").read_text() if (home/"config.toml").exists() else ""; return {"inventory":inv,"config":cfg}
def events(stdout):
    types=[]; usage=[]; reads=[]
    for line in stdout.splitlines():
        try: e=json.loads(line)
        except json.JSONDecodeError: continue
        types.append(e.get("type")); usage += [e["usage"]] if "usage" in e else []; item=e.get("item",{}); kind=item.get("type")
        if kind in {"command_execution","shell_command"} and re.search(r"(?i)(read_text|read_bytes|cat|sed|head|tail)[^\n]*SKILL\.md", str(item.get("command", ""))) and e.get("type") == "item.completed" and item.get("exit_code", 0) == 0: reads.append(e)
    return {"event_types":types,"usage":usage,"skill_read_evidence":reads}
def trial(spec,package,source_root,output,number,arm,auth,competing,model,effort,timeout):
    lane=f"{spec['id']}-{arm}-trial{number}"; private=output/"private"/lane; private.mkdir(parents=True); home=private/"codex-home"; fixture=private/"fixture"; source=source_root/spec["fixture"] if spec.get("fixture") else None; rec={"case_id":spec["id"],"arm":arm,"trial":number,"model":model,"reasoning_effort":effort,"timeout_seconds":timeout}
    try:
        if STOP.is_set(): raise RuntimeError("evaluation cancelled")
        if not source or not source.exists(): raise FileNotFoundError(f"fixture missing: {source}")
        shutil.copytree(source,fixture); subprocess.run(["git","init","-q"],cwd=fixture,check=True); git=["git","-c","user.name=eval","-c","user.email=eval@invalid"]; subprocess.run(git+["add","."],cwd=fixture,check=True); subprocess.run(git+["commit","-qm","baseline"],cwd=fixture,check=True); before=tree(fixture); setup_info=setup(home,package,competing,arm,auth); prompt=(spec.get("context","")+"\n\n"+spec["request"]).strip(); env={**os.environ,"CODEX_HOME":str(home)}; cmd=["codex","-a","never","exec","--ephemeral","--json","--skip-git-repo-check","--sandbox","workspace-write","--model",model,"-c",f"model_reasoning_effort={effort}","-c",'developer_instructions="Treat the current directory as the complete target repository. Inspect only this repository and runtime-provided skill resources; do not inspect parent directories or other repositories. Keep all edits in this repository. Do not make network calls or mutate external systems."',"-C",str(fixture),prompt]; result=command(cmd,env,fixture,timeout); (home/"auth.json").unlink(missing_ok=True); after=tree(fixture); status=subprocess.run(["git","status","--short"],cwd=fixture,text=True,capture_output=True).stdout; diff=subprocess.run(["git","diff","HEAD","--no-ext-diff","--binary"],cwd=fixture,text=True,capture_output=True).stdout; untracked=[fixture/name for name in subprocess.run(["git","ls-files","--others","--exclude-standard","-z"],cwd=fixture,text=True,capture_output=True).stdout.split("\0") if name and "__pycache__" not in Path(name).parts]; diff += "".join(f"\n--- untracked {p.relative_to(fixture)} ---\n{p.read_text(errors='replace')}" for p in untracked if p.is_file()); rev=subprocess.run(["git","-C",str(package),"rev-parse","HEAD"],text=True,capture_output=True,check=True).stdout.strip(); rec.update({"prompt":prompt,"command":cmd[:-1]+["<PROMPT>"],"package_revision":rev,"package_hash":digest(package),"competing_skill_hash":digest(competing),"fixture_before_hashes":before,"fixture_after_hashes":after,"fixture_diff":diff,"fixture_status":status,"setup":setup_info,"result":result,"observations":events(result["stdout"])})
    except Exception as e: rec.update({"error":str(e),"setup_or_trial_failed":True})
    finally:
        (home/"auth.json").unlink(missing_ok=True)
    (private/"record.json").write_text(json.dumps(rec,indent=2,ensure_ascii=False)); return rec
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--package",type=Path,required=True); ap.add_argument("--matrix",type=Path,required=True); ap.add_argument("--output",type=Path,required=True); ap.add_argument("--auth",type=Path,default=Path.home()/".codex/auth.json"); ap.add_argument("--competing-skill",type=Path,default=Path.home()/".agents/skills/diagnosing-bugs/SKILL.md"); ap.add_argument("--trials",type=int); ap.add_argument("--max-workers",type=int,default=2); ns=ap.parse_args()
    if not 1<=ns.max_workers<=2: ap.error("--max-workers must be 1 or 2")
    matrix=json.loads(ns.matrix.read_text()); cases={x["id"]:x for x in json.loads((ns.matrix.parent/"cases.json").read_text())["cases"]}; source_root=ns.matrix.parent; trials=ns.trials or matrix.get("trials",2); model=matrix.get("model","gpt-5.6-luna"); effort=matrix.get("reasoning_effort",matrix.get("effort","medium")); timeout=int(matrix.get("timeout_seconds",240)); ns.output.mkdir(parents=True,exist_ok=True,mode=0o700); os.chmod(ns.output,0o700); jobs=[(cases[x],a,n) for x in matrix["case_ids"] for a in ("control","harness") for n in range(1,trials+1)]; print(f"prepared {len(jobs)} trials; max concurrency {ns.max_workers}",flush=True); records=[]
    try:
        with ThreadPoolExecutor(max_workers=ns.max_workers) as pool:
            fs={pool.submit(trial,c,ns.package,source_root,ns.output,n,a,ns.auth,ns.competing_skill,model,effort,timeout):(c["id"],a,n) for c,a,n in jobs}
            for f in as_completed(fs):
                key=fs[f]
                try: r=f.result()
                except Exception as e: r={"case_id":key[0],"arm":key[1],"trial":key[2],"error":str(e),"setup_or_trial_failed":True}
                records.append(r); print(f"done {key[0]} {key[1]} trial={key[2]} rc={r.get('result',{}).get('return_code','NA')} timeout={r.get('result',{}).get('timed_out','NA')}",flush=True)
    except KeyboardInterrupt: print("interrupted; active process groups terminated",file=sys.stderr)
    records.sort(key=lambda r:(r["case_id"],r["arm"],r["trial"])); private=ns.output/"private"; private.mkdir(exist_ok=True); manifest=json.dumps(records,indent=2,ensure_ascii=False); (private/"manifest.json").write_text(manifest); mapping={str(ns.output):"<OUTPUT>",str(ns.package):"<PACKAGE>",str(ns.matrix.parent.parent):"<REPO>",str(ns.auth.parent):"<AUTH_HOME>",str(ns.competing_skill.parent.parent):"<SKILL_HOME>"}; red=manifest
    mapping[str(Path.home())] = "<USER_HOME>"
    mapping[str(Path(__file__).parent)] = "<RUNNER_HOME>"
    secrets = []
    def collect(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key.lower() in {"access_token", "refresh_token", "id_token", "api_key", "openai_api_key", "account_id"} and isinstance(child, str) and len(child) > 8:
                    secrets.append(child)
                else: collect(child)
        elif isinstance(value, list):
            for child in value: collect(child)
    collect(json.loads(ns.auth.read_text()))
    def redact(value):
        if isinstance(value, str):
            for secret in secrets: value = value.replace(secret, "<REDACTED>")
            for key, replacement in sorted(mapping.items(), key=lambda item: -len(item[0])):
                value = value.replace(key, replacement)
            return value
        if isinstance(value, list): return [redact(item) for item in value]
        if isinstance(value, dict): return {key: redact(item) for key, item in value.items()}
        return value
    red = json.dumps(redact(records), indent=2, ensure_ascii=False); public=ns.output/"public"; public.mkdir(exist_ok=True); (public/"manifest.json").write_text(red); incomplete=len(records)!=len(jobs) or any(r.get("setup_or_trial_failed") or r.get("result",{}).get("timed_out") or r.get("result",{}).get("return_code",1) != 0 for r in records); print(f"completed {len(records)}/{len(jobs)}; output={ns.output}",flush=True); return 2 if incomplete else 0
if __name__=="__main__": sys.exit(main())
