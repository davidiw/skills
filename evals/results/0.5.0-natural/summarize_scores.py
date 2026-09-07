#!/usr/bin/env python3
"""Normalize retained human/agent assessments without inferring skill reads."""
import json
from pathlib import Path


def summarize(root):
    rows = []
    for source in sorted((root / "assessments").glob("*.json")):
        if source.name == "ordinal-review-probes.json":
            continue
        data = json.loads(source.read_text())
        trials = data if isinstance(data, list) else data["trials"]
        for trial in trials:
            case_id = trial.get("case_id") or data["case_id"]
            rubric = trial.get("rubric", trial.get("rubric_scores", {}))
            total = rubric["total"]
            grade = trial.get("substantive_grade")
            if grade is None:
                grade = "pass" if trial["all_required_outcomes_met"] else "partial"
            passed = trial.get("directional_pass", rubric.get("directional_pass"))
            if passed is None:
                passed = grade == "pass" and total >= 10
            rows.append({
                "case_id": case_id, "arm": trial["arm"], "trial": trial["trial"],
                "substantive_grade": grade, "rubric_total": total,
                "directional_pass": passed,
                "assessment": str(source.relative_to(root)),
            })
    rows.sort(key=lambda row: (row["case_id"], row["arm"], row["trial"]))
    identities = [(row["case_id"], row["arm"], row["trial"]) for row in rows]
    if len(identities) != len(set(identities)):
        raise ValueError("Duplicate trial assessment")
    expected = {(r["case_id"], r["arm"], r["trial"]) for r in json.loads((root / "manifest.json").read_text())}
    if set(identities) != expected:
        raise ValueError("Assessment coverage does not match execution receipt")
    arms = {arm: {
        "trials": sum(row["arm"] == arm for row in rows),
        "directional_passes": sum(row["arm"] == arm and row["directional_pass"] for row in rows),
    } for arm in ("control", "harness")}
    return {"scoring_contract": "Frozen evals/rubric.md plus exact case outcomes; see README for applicability interpretation.",
            "arms": arms, "trials": rows}


if __name__ == "__main__":
    root = Path(__file__).parent
    (root / "scores.json").write_text(json.dumps(summarize(root), indent=2) + "\n")
