#!/usr/bin/env python3
"""Validate an LLM-generated fallacy report using only the Python standard library."""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from load_taxonomy import load_taxonomy

REQUIRED_FINDING_FIELDS = {
    "fallacy_id",
    "name_zh",
    "name_en",
    "evidence_quote",
    "conclusion_or_target",
    "argumentative_move",
    "why_fallacious",
    "strongest_non_fallacious_interpretation",
    "adjudication",
    "confidence",
    "centrality",
    "fact_check_needed",
    "repair",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Original UTF-8 text input")
    ap.add_argument("--report", required=True, help="JSON report")
    args = ap.parse_args()

    original = Path(args.input).read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    report = load_json(Path(args.report))
    taxonomy = load_taxonomy()
    by_id = {x["id"]: x for x in taxonomy["fallacies"]}

    errors: list[str] = []
    warnings: list[str] = []

    findings = report.get("findings")
    if not isinstance(findings, list):
        errors.append("top-level 'findings' must be a list")
        findings = []

    seen = set()
    for i, f in enumerate(findings, 1):
        if not isinstance(f, dict):
            errors.append(f"finding {i}: must be an object")
            continue
        missing = REQUIRED_FINDING_FIELDS - set(f)
        if missing:
            errors.append(f"finding {i}: missing fields {sorted(missing)}")

        fid = f.get("fallacy_id")
        if fid != "unclassified_reasoning_issue" and fid not in by_id:
            errors.append(f"finding {i}: unknown fallacy_id {fid!r}")
        elif fid in by_id:
            expected = by_id[fid]
            if f.get("name_zh") != expected["name_zh"]:
                warnings.append(f"finding {i}: name_zh differs from taxonomy")
            if f.get("name_en") != expected["name_en"]:
                warnings.append(f"finding {i}: name_en differs from taxonomy")

        q = f.get("evidence_quote", "")
        if not isinstance(q, str) or not q.strip():
            errors.append(f"finding {i}: evidence_quote must be a non-empty string")
        elif q not in original:
            errors.append(f"finding {i}: evidence_quote not found verbatim in original input")

        c = f.get("confidence")
        if not isinstance(c, (int, float)) or isinstance(c, bool) or not (0 <= c <= 1):
            errors.append(f"finding {i}: confidence must be a number in [0, 1]")

        if f.get("centrality") not in {"central", "supporting", "rhetorical"}:
            errors.append(f"finding {i}: centrality must be central/supporting/rhetorical")

        if not isinstance(f.get("fact_check_needed"), bool):
            errors.append(f"finding {i}: fact_check_needed must be boolean")

        key = (fid, q)
        if key in seen:
            warnings.append(f"finding {i}: duplicate fallacy/evidence pair")
        seen.add(key)

    out = {"ok": not errors, "errors": errors, "warnings": warnings, "finding_count": len(findings)}
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
