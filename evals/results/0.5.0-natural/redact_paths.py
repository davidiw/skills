#!/usr/bin/env python3
"""Normalize remaining local path strings and mapping keys in runner receipts.

The runner removes credential values before this step. This tool takes explicit
local-prefix mappings; it does not inspect authentication material.
"""
import argparse
import json
from pathlib import Path


def redact(value, replacements):
    if isinstance(value, str):
        for source, replacement in sorted(replacements.items(), key=lambda item: -len(item[0])):
            value = value.replace(source, replacement)
        return value
    if isinstance(value, list):
        return [redact(item, replacements) for item in value]
    if isinstance(value, dict):
        return {redact(key, replacements): redact(item, replacements) for key, item in value.items()}
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--map", action="append", default=[], metavar="PREFIX=PLACEHOLDER")
    args = parser.parse_args()
    replacements = dict(item.split("=", 1) for item in args.map)
    content = redact(json.loads(args.source.read_text()), replacements)
    args.destination.write_text(json.dumps(content, indent=2) + "\n")
