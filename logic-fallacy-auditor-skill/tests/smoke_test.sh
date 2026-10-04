#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

python3 "$ROOT/scripts/lint_taxonomy.py"
python3 "$ROOT/scripts/prepare_input.py" "$ROOT/examples/input_zh.txt" > "$TMP/prepared.json"
python3 "$ROOT/scripts/validate_report.py" \
  --input "$ROOT/examples/input_zh.txt" \
  --report "$ROOT/examples/report_zh.json" > "$TMP/validation.json"
python3 "$ROOT/scripts/render_report.py" "$ROOT/examples/report_zh.json" > "$TMP/report.md"

grep -q '"ok": true' "$TMP/validation.json"
grep -q '轶事证据' "$TMP/report.md"
grep -q '人身攻击' "$TMP/report.md"
grep -q '诉诸自然' "$TMP/report.md"

echo "smoke test OK"
