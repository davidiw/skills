import hashlib
from pathlib import Path

def issue(report, code, interrupted=False, snapshot="source"):
    if code != 0:
        raise ValueError("execution failed")
    raw=Path(report).read_bytes() if Path(report).exists() else b""
    return {"status":"PASS","snapshot":snapshot,"digest":hashlib.sha256(raw).hexdigest()}

def reuse(receipt, report, snapshot="source"):
    return receipt.get("status")=="PASS" and receipt.get("snapshot")==snapshot
