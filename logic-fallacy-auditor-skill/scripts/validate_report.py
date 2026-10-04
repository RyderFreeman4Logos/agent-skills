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
REQUIRED_REPORT_FIELDS = {"analysis_version", "summary", "findings", "fallacy_fallacy_caveat"}
FINDING_STRING_FIELDS = REQUIRED_FINDING_FIELDS - {"confidence", "centrality", "fact_check_needed"}


def check_string_list(value, label: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{label} must be an array")
    else:
        for i, item in enumerate(value, 1):
            if not isinstance(item, str):
                errors.append(f"{label} item {i} must be a string")


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

    if not isinstance(report, dict):
        errors.append("top-level report must be an object")
        report = {}
    missing_report = REQUIRED_REPORT_FIELDS - set(report)
    if missing_report:
        errors.append(f"top-level: missing fields {sorted(missing_report)}")
    if not isinstance(report.get("analysis_version"), str):
        errors.append("analysis_version must be a string")

    summary = report.get("summary")
    if not isinstance(summary, dict):
        errors.append("summary must be an object")
        summary = {}
    missing_summary = {"overall", "most_important"} - set(summary)
    if missing_summary:
        errors.append(f"summary: missing fields {sorted(missing_summary)}")
    for field in ("overall", "most_important"):
        if not isinstance(summary.get(field), str):
            errors.append(f"summary.{field} must be a string")

    if not isinstance(report.get("fallacy_fallacy_caveat"), str):
        errors.append("fallacy_fallacy_caveat must be a string")
    for field in ("important_non_findings", "fact_checks_needed"):
        if field in report:
            check_string_list(report[field], field, errors)

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

        for field in FINDING_STRING_FIELDS:
            if not isinstance(f.get(field), str):
                errors.append(f"finding {i}: {field} must be a string")

        fid = f.get("fallacy_id")
        if not isinstance(fid, str):
            errors.append(f"finding {i}: fallacy_id must be a string")
        elif fid != "unclassified_reasoning_issue" and fid not in by_id:
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

        centrality = f.get("centrality")
        if not isinstance(centrality, str) or centrality not in {"central", "supporting", "rhetorical"}:
            errors.append(f"finding {i}: centrality must be central/supporting/rhetorical")

        if not isinstance(f.get("fact_check_needed"), bool):
            errors.append(f"finding {i}: fact_check_needed must be boolean")

        if "related_fallacies" in f:
            check_string_list(f["related_fallacies"], f"finding {i}: related_fallacies", errors)

        if isinstance(fid, str) and isinstance(q, str):
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
