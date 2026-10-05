#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

python3 "$ROOT/scripts/lint_taxonomy.py"
python3 "$ROOT/scripts/load_taxonomy.py" > "$TMP/taxonomy.json"
python3 -m json.tool "$TMP/taxonomy.json" > /dev/null
python3 "$ROOT/scripts/prepare_input.py" "$ROOT/examples/input_zh.txt" > "$TMP/prepared.json"
python3 "$ROOT/scripts/validate_report.py" \
  --input "$ROOT/examples/input_zh.txt" \
  --report "$ROOT/examples/report_zh.json" > "$TMP/validation.json"
python3 "$ROOT/scripts/render_report.py" "$ROOT/examples/report_zh.json" > "$TMP/report.md"
python3 "$ROOT/scripts/validate_report.py" \
  --input "$ROOT/examples/input_zh.txt" \
  --report "$ROOT/examples/report_zh_nonfindings.json" > "$TMP/nonfindings-validation.json"
python3 "$ROOT/scripts/render_report.py" "$ROOT/examples/report_zh_nonfindings.json" > "$TMP/nonfindings.md"

grep -q '"ok": true' "$TMP/validation.json"
grep -q '"ok": true' "$TMP/nonfindings-validation.json"
grep -q '^Version: 2.0.0$' "$TMP/report.md"
grep -q '^Version: 2.0.0$' "$TMP/nonfindings.md"
grep -q '轶事证据' "$TMP/report.md"
grep -q '人身攻击' "$TMP/report.md"
grep -q '诉诸自然' "$TMP/report.md"
grep -q '\*\*Conditional diagnosis:\*\* dialogue_defect; straw_man' "$TMP/nonfindings.md"

python3 "$ROOT/../tests/phase3_regression_test.py"

echo "smoke test OK"
