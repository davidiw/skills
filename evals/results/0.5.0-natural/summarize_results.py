#!/usr/bin/env python3
"""Derive latency/token totals from the retained, sanitized execution receipt."""
import json
import statistics
from pathlib import Path


def summarize(records):
    rows = []
    for record in records:
        result = record.get("result", {})
        usage = record.get("observations", {}).get("usage", [])
        tokens = {key: sum(item.get(key, 0) for item in usage) for key in (
            "input_tokens", "cached_input_tokens", "cache_write_input_tokens",
            "output_tokens", "reasoning_output_tokens")}
        rows.append({
            "case_id": record["case_id"], "arm": record["arm"], "trial": record["trial"],
            "seconds": round(result.get("ended_at", 0) - result.get("started_at", 0), 3),
            "return_code": result.get("return_code"), "timed_out": result.get("timed_out", False),
            "setup_failed": record.get("setup_or_trial_failed", False),
            **tokens,
            "uncached_input_tokens": tokens["input_tokens"] - tokens["cached_input_tokens"],
        })
    arms = {}
    for arm in ("control", "harness"):
        selected = [row for row in rows if row["arm"] == arm]
        arms[arm] = {
            "trials": len(selected),
            "timeouts": sum(row["timed_out"] for row in selected),
            "failures": sum(row["setup_failed"] or row["return_code"] != 0 for row in selected),
            "median_seconds": round(statistics.median(row["seconds"] for row in selected), 3),
            "total_model_seconds": round(sum(row["seconds"] for row in selected), 3),
            **{key: sum(row[key] for row in selected) for key in (
                "input_tokens", "cached_input_tokens", "uncached_input_tokens",
                "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens")},
        }
    return {"arms": arms, "trials": rows}


if __name__ == "__main__":
    root = Path(__file__).parent
    records = json.loads((root / "manifest.json").read_text())
    (root / "metrics.json").write_text(json.dumps(summarize(records), indent=2) + "\n")
