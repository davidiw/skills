import csv
import json
from pathlib import Path
root = Path(__file__).parent
board = json.loads((root / "board.json").read_text())
rows = {row["ref"]: row for row in csv.DictReader((root / "cpl.csv").open())}
errors = []
for c in board["components"]:
    expected = (c["footprint_rotation"] + c["pad1_offset"]) % 360
    if int(rows[c["ref"]]["rotation"]) != expected:
        errors.append(f"{c['ref']}: rotation must be {expected}")
job = json.loads((root / "job-settings.json").read_text())
if job["min_via_drill_mm"] > board["minimum_drill_mm"]:
    errors.append("job minimum via drill exceeds design")
print("\n".join(errors) if errors else "local checks pass")
raise SystemExit(bool(errors))
