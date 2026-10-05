#!/usr/bin/env python3
"""Validate v2 reasoning-audit reports and verbatim source evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from load_taxonomy import load_taxonomy

VERSION = "2.0.0"
ISSUE_TYPES = {
    "invalid_deduction", "weak_induction", "causal_gap", "unsupported_claim",
    "irrelevant_support", "missing_premise", "inconsistency",
    "scope_or_quantifier_error", "ambiguity_or_equivocation",
    "evidence_selection_problem", "dialogue_defect", "rhetorical_substitution",
    "epistemic_problem", "definition_or_category_error", "unclassified_reasoning_issue",
}
CONFIDENCE = {"high", "medium", "low"}
CENTRALITY = {"central", "supporting", "rhetorical"}
DISPOSITIONS = {
    "fact_check_needed", "unsupported_but_not_fallacious", "insufficient_context",
    "value_disagreement", "definition_disagreement", "rhetorical_style_only",
    "no_material_reasoning_problem",
}
REPORT_FIELDS = {
    "analysis_version", "summary", "findings", "non_findings",
    "fact_checks_needed", "fallacy_fallacy_caveat",
}
FINDING_FIELDS = {
    "issue_type", "fallacy_id", "name_zh", "name_en", "evidence_quote",
    "conclusion_or_target", "faithful_reconstruction", "reasoning_defect",
    "why_it_matters", "strongest_non_fallacious_interpretation",
    "rescue_requires_new_premise", "required_new_premise", "adversarial_review",
    "adjudication", "defect_confidence", "label_confidence",
    "context_completeness", "centrality", "fact_check_needed",
    "related_fallacies", "repair",
}
NON_FINDING_FIELDS = {"disposition", "evidence_quote", "reason", "conditional_diagnosis"}


def required(obj: dict, fields: set[str], label: str, errors: list[str]) -> None:
    missing = fields - obj.keys()
    extra = obj.keys() - fields
    if missing:
        errors.append(f"{label}: missing fields {sorted(missing)}")
    if extra:
        errors.append(f"{label}: unexpected fields {sorted(extra)}")


def nonempty(value, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty string")


def string_list(value, label: str, errors: list[str]) -> None:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        errors.append(f"{label} must be an array of strings")


def quoted_in_source(value, label: str, original: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty string")
    elif value not in original:
        errors.append(f"{label} not found verbatim in original input")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Original UTF-8 text input")
    parser.add_argument("--report", required=True, help="v2 JSON report")
    args = parser.parse_args()

    original = Path(args.input).read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in load_taxonomy()["fallacies"]}
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(report, dict):
        errors.append("top-level report must be an object")
        report = {}
    required(report, REPORT_FIELDS, "top-level", errors)
    if report.get("analysis_version") != VERSION:
        errors.append(f"analysis_version must be {VERSION}")
    nonempty(report.get("fallacy_fallacy_caveat"), "fallacy_fallacy_caveat", errors)

    summary = report.get("summary")
    if not isinstance(summary, dict):
        errors.append("summary must be an object")
    else:
        required(summary, {"overall", "most_important"}, "summary", errors)
        for field in ("overall", "most_important"):
            nonempty(summary.get(field), f"summary.{field}", errors)

    fact_checks = report.get("fact_checks_needed")
    string_list(fact_checks, "fact_checks_needed", errors)

    findings = report.get("findings")
    if not isinstance(findings, list):
        errors.append("findings must be an array")
        findings = []
    seen: set[tuple[object, str]] = set()
    for index, finding in enumerate(findings, 1):
        label = f"finding {index}"
        if not isinstance(finding, dict):
            errors.append(f"{label} must be an object")
            continue
        required(finding, FINDING_FIELDS, label, errors)
        if not isinstance(finding.get("issue_type"), str) or finding["issue_type"] not in ISSUE_TYPES:
            errors.append(f"{label}: invalid issue_type")

        fid = finding.get("fallacy_id")
        if fid is None:
            for field in ("name_zh", "name_en", "label_confidence"):
                if finding.get(field) is not None:
                    errors.append(f"{label}: {field} must be null when fallacy_id is null")
        elif not isinstance(fid, str) or fid not in by_id:
            errors.append(f"{label}: unknown fallacy_id {fid!r}")
        else:
            taxonomy_item = by_id[fid]
            if finding.get("name_zh") != taxonomy_item["name_zh"]:
                errors.append(f"{label}: name_zh must match taxonomy")
            if finding.get("name_en") != taxonomy_item["name_en"]:
                errors.append(f"{label}: name_en must match taxonomy")
            if not isinstance(finding.get("label_confidence"), str) or finding["label_confidence"] not in CONFIDENCE:
                errors.append(f"{label}: label_confidence must be high/medium/low")

        quoted_in_source(finding.get("evidence_quote"), f"{label}: evidence_quote", original, errors)
        for field in (
            "conclusion_or_target", "reasoning_defect", "why_it_matters",
            "strongest_non_fallacious_interpretation", "adversarial_review",
            "adjudication", "repair",
        ):
            nonempty(finding.get(field), f"{label}: {field}", errors)

        reconstruction = finding.get("faithful_reconstruction")
        if not isinstance(reconstruction, dict):
            errors.append(f"{label}: faithful_reconstruction must be an object")
        else:
            required(reconstruction, {"premises", "conclusion", "inference"}, f"{label}: faithful_reconstruction", errors)
            string_list(reconstruction.get("premises"), f"{label}: premises", errors)
            nonempty(reconstruction.get("conclusion"), f"{label}: reconstructed conclusion", errors)
            nonempty(reconstruction.get("inference"), f"{label}: reconstructed inference", errors)

        rescue = finding.get("rescue_requires_new_premise")
        if not isinstance(rescue, bool):
            errors.append(f"{label}: rescue_requires_new_premise must be boolean")
        elif rescue:
            nonempty(finding.get("required_new_premise"), f"{label}: required_new_premise", errors)
        elif finding.get("required_new_premise") is not None:
            errors.append(f"{label}: required_new_premise must be null when rescue is false")

        for field in ("defect_confidence", "context_completeness"):
            if not isinstance(finding.get(field), str) or finding[field] not in CONFIDENCE:
                errors.append(f"{label}: {field} must be high/medium/low")
        if not isinstance(finding.get("centrality"), str) or finding["centrality"] not in CENTRALITY:
            errors.append(f"{label}: centrality must be central/supporting/rhetorical")
        if not isinstance(finding.get("fact_check_needed"), bool):
            errors.append(f"{label}: fact_check_needed must be boolean")
        related = finding.get("related_fallacies")
        string_list(related, f"{label}: related_fallacies", errors)
        if isinstance(related, list):
            for related_id in related:
                if not isinstance(related_id, str) or related_id not in by_id:
                    errors.append(f"{label}: unknown related fallacy {related_id!r}")

        quote = finding.get("evidence_quote")
        if isinstance(quote, str):
            key = (fid if isinstance(fid, str) else None, quote)
            if key in seen:
                warnings.append(f"{label}: duplicate issue/evidence pair")
            seen.add(key)

    non_findings = report.get("non_findings")
    if not isinstance(non_findings, list):
        errors.append("non_findings must be an array")
        non_findings = []
    for index, item in enumerate(non_findings, 1):
        label = f"non_finding {index}"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        required(item, NON_FINDING_FIELDS, label, errors)
        disposition = item.get("disposition")
        if not isinstance(disposition, str) or disposition not in DISPOSITIONS:
            errors.append(f"{label}: invalid disposition")
        quoted_in_source(item.get("evidence_quote"), f"{label}: evidence_quote", original, errors)
        nonempty(item.get("reason"), f"{label}: reason", errors)

        diagnosis = item.get("conditional_diagnosis")
        if disposition == "insufficient_context":
            if not isinstance(diagnosis, dict):
                errors.append(f"{label}: insufficient_context requires conditional_diagnosis")
                continue
            diagnosis_fields = {"conditional_issue_type", "conditional_label_id", "condition", "diagnosis"}
            required(diagnosis, diagnosis_fields, f"{label}: conditional_diagnosis", errors)
            if not isinstance(diagnosis.get("conditional_issue_type"), str) or diagnosis["conditional_issue_type"] not in ISSUE_TYPES:
                errors.append(f"{label}: invalid conditional_issue_type")
            conditional_id = diagnosis.get("conditional_label_id")
            if conditional_id is not None and (not isinstance(conditional_id, str) or conditional_id not in by_id):
                errors.append(f"{label}: unknown conditional_label_id {conditional_id!r}")
            nonempty(diagnosis.get("condition"), f"{label}: condition", errors)
            nonempty(diagnosis.get("diagnosis"), f"{label}: diagnosis", errors)
        elif diagnosis is not None:
            errors.append(f"{label}: conditional_diagnosis is only valid for insufficient_context")

    result = {"ok": not errors, "errors": errors, "warnings": warnings, "finding_count": len(findings)}
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
