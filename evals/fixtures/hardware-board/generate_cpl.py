import csv
import json
from pathlib import Path
root = Path(__file__).parent
board = json.loads((root / "board.json").read_text())
with (root / "cpl.csv").open("w", newline="") as stream:
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["ref", "x", "y", "rotation"])
    for c in board["components"]:
        writer.writerow([c["ref"], c["x"], c["y"], c["footprint_rotation"]])
