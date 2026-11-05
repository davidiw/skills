from pathlib import Path
import json

def check(root):
    designs = list((root / "designs").glob("*/manifest.json"))
    for path in designs:
        if not json.loads(path.read_text()).get("name"):
            return False
    return True

if __name__ == "__main__":
    raise SystemExit(0 if check(Path(__file__).parent) else 1)
