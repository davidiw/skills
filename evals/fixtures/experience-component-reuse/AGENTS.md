# Repository rules

This is a small, synthetic local web app. DESIGN.md owns accepted product and visual
intent; it is not automatically rewritten when code differs. Use existing files.
No backend, account system, network or build framework is involved.

Review/design requests leave production HTML, CSS and JavaScript unchanged.
They may create a short proposal and local rendering artifacts under renders/.
Implementation requests may edit the bounded existing owner and focused checks.

Run `node test.js` for existing checks. If render.py is present, render the real
page offline with `python3 render.py --width 390 --height 844 --state normal
--output renders/narrow.png`; choose state/width as appropriate. The renderer uses
an available Chromium executable through EXPERIENCE_CHROMIUM or PATH. Open the
resulting image to inspect it. Do not claim rendering from source inspection.
