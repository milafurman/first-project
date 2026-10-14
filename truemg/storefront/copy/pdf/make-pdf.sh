#!/bin/bash
# Rebuild TrueMG-store-policies.pdf from policies.html.
#
# Uses headless Chrome, the same route as assets/labels/make_pdfs.py — no
# reportlab, weasyprint, pandoc or wkhtmltopdf is installed in this environment
# (all four checked), and poppler is absent too, so a produced PDF cannot be
# rendered back for inspection. To check it, screenshot the HTML through the
# same engine instead: add --screenshot=_check.png and drop --print-to-pdf.
set -e
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || { echo "Chrome not found at $CHROME"; exit 1; }
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
"$CHROME" --headless --disable-gpu --no-first-run --no-default-browser-check \
  --user-data-dir="$TMP/cd" --no-pdf-header-footer \
  --print-to-pdf="$PWD/TrueMG-store-policies.pdf" "file://$PWD/policies.html" >/dev/null 2>&1
ls -l TrueMG-store-policies.pdf
