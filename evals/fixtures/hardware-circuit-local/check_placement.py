"""Coarse regression for this two-footprint fixture; not a substitute for DRC."""
from pathlib import Path
import math
import re

text = Path('layout.kicad_pcb').read_text()

def position(ref):
    # Inspect the first footprint-level location preceding this reference.
    pattern = (r'\(footprint\s+"[^\"]+"(?:(?!\(footprint\s).)*?'
               r'\(at\s+([\d.\-]+)\s+([\d.\-]+)(?:\s+[^)]*)?\)'
               r'(?:(?!\(footprint\s).)*?\(property\s+"Reference"\s+"'
               + re.escape(ref) + r'"')
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        raise ValueError(f'missing footprint {ref}')
    return tuple(map(float, match.groups()))

u, c = position('U12'), position('C106')
distance = math.dist(u, c)
# Fixture-only center-spacing bound: reject remote placement and overlap.
if not (1.6 <= distance <= 3.0):
    raise SystemExit(f'FAIL: capacitor/gauge center spacing {distance:.2f} mm')
print(f'PASS: center spacing {distance:.2f} mm; full board routing/clearance not checked')
