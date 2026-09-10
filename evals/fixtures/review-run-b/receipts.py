import hashlib,json
from pathlib import Path

def invalid_constant(value):
    raise ValueError("non-JSON constant")

def reject_duplicate_members(pairs):
    result={}
    for key,value in pairs:
        if key in result:
            raise ValueError("duplicate JSON member")
        result[key]=value
    return result

def json_records(raw):
    """Decode JSONL records without treating JSON string characters as delimiters."""
    lines=raw.split(b"\n")
    if raw.endswith(b"\n"):
        lines.pop()
    return [json.loads(line.decode("utf-8"), parse_constant=invalid_constant,
                       object_pairs_hook=reject_duplicate_members)
            for line in lines]

def evidence(report):
    raw=Path(report).read_bytes()
    events=json_records(raw)
    if len(events)<2 or events[0].get("kind")!="start" or events[-1].get("kind")!="done" or events[-1].get("ok") is not True:
        raise ValueError("incomplete report")
    first=events[0];expected=first["expected"]
    if not isinstance(expected,list) or not expected or any(not isinstance(x,str) or not x for x in expected) or len(expected)!=len(set(expected)) or not isinstance(first.get("run_id"),str) or not first["run_id"]:
        raise ValueError("invalid inventory")
    if any(e.get("run_id")!=first["run_id"] for e in events):
        raise ValueError("different run")
    seen=set()
    for e in events[1:-1]:
        if e.get("kind")!="result" or e.get("id") not in expected or e["id"] in seen:
            raise ValueError("invalid result")
        if e.get("status")!="pass" and not (e.get("status")=="skip" and e["id"]=="optional_ui"):
            raise ValueError("failed result")
        seen.add(e["id"])
    if seen!=set(expected):
        raise ValueError("missing result")
    return hashlib.sha256(raw).hexdigest()

def issue(report, code, interrupted=False, snapshot="source"):
    if code!=0 or interrupted:
        raise ValueError("execution failed")
    return {"status":"PASS","snapshot":snapshot,"digest":evidence(report)}

def reuse(receipt, report, snapshot="source"):
    try:
        return receipt.get("status")=="PASS" and receipt.get("snapshot")==snapshot and receipt.get("digest")==evidence(report)
    except (OSError,ValueError,KeyError,TypeError,AttributeError):
        return False
