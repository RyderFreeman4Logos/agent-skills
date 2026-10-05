#!/usr/bin/env python3
"""Render a v2 report while keeping untrusted multiline text inside quotes."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def inline(value) -> str:
    text = str(value if value is not None else "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return html.escape(" ".join(text.splitlines()).strip(), quote=False)


def block_quote(value) -> str:
    text = str(value if value is not None else "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join("> " + html.escape(line, quote=False) for line in text.split("\n"))


def render(report: dict) -> str:
    out = ["# Reasoning Audit", "", f"Version: {inline(report.get('analysis_version'))}", ""]
    summary = report.get("summary", {})
    out.extend(["## Summary", "", inline(summary.get("overall")), "", f"**Most important:** {inline(summary.get('most_important'))}", ""])

    findings = report.get("findings", [])
    out.extend(["## Findings", ""])
    if not findings:
        out.extend(["No material reasoning defect was established.", ""])
    for index, finding in enumerate(findings, 1):
        reconstruction = finding.get("faithful_reconstruction", {})
        out.extend([f"### Finding {index}", "", "**Evidence quote:**", block_quote(finding.get("evidence_quote")), ""])
        out.append("**Faithful reconstruction:**")
        for premise in reconstruction.get("premises", []):
            out.append(f"- Premise: {inline(premise)}")
        out.extend([
            f"- Conclusion: {inline(reconstruction.get('conclusion'))}",
            f"- Inference: {inline(reconstruction.get('inference'))}",
            f"- Target: {inline(finding.get('conclusion_or_target'))}",
            "",
            f"**Reasoning issue ({inline(finding.get('issue_type'))}):** {inline(finding.get('reasoning_defect'))}",
            f"**Why it matters:** {inline(finding.get('why_it_matters'))}",
            f"**Strongest non-fallacious reading:** {inline(finding.get('strongest_non_fallacious_interpretation'))}",
        ])
        if finding.get("rescue_requires_new_premise"):
            out.append(f"**New premise needed to rescue it:** {inline(finding.get('required_new_premise'))}")
        else:
            out.append("**New premise needed to rescue it:** No additional premise identified.")
        out.extend([
            f"**Adversarial review:** {inline(finding.get('adversarial_review'))}",
            f"**Adjudication:** {inline(finding.get('adjudication'))}",
        ])
        if finding.get("fallacy_id") is None:
            out.append("**Narrow taxonomy annotation:** None assigned.")
        else:
            out.append(f"**Narrow taxonomy annotation:** {inline(finding.get('name_zh'))} (`{inline(finding.get('fallacy_id'))}`)")
        label_confidence = finding.get("label_confidence") or "not applicable"
        out.extend([
            f"**Confidence (defect / label / context):** {inline(finding.get('defect_confidence'))} / {inline(label_confidence)} / {inline(finding.get('context_completeness'))}",
            f"**Fact-check needed:** {inline(finding.get('fact_check_needed'))}",
            f"**Minimal repair:** {inline(finding.get('repair'))}",
        ])
        related = finding.get("related_fallacies", [])
        if related:
            out.append(f"**Related taxonomy entries:** {inline(', '.join(related))}")
        out.append("")

    out.extend(["## Non-findings", ""])
    non_findings = report.get("non_findings", [])
    if not non_findings:
        out.extend(["No separate non-finding disposition was recorded.", ""])
    for item in non_findings:
        out.extend([
            f"### {inline(item.get('disposition')).replace('_', ' ')}",
            "",
            "**Evidence quote:**",
            block_quote(item.get("evidence_quote")),
            "",
            inline(item.get("reason")),
        ])
        conditional = item.get("conditional_diagnosis")
        if conditional:
            label = conditional.get("conditional_label_id") or "no narrow label"
            out.extend([
                "",
                f"**Conditional diagnosis:** {inline(conditional.get('conditional_issue_type'))}; {inline(label)}",
                f"**Condition:** {inline(conditional.get('condition'))}",
                f"**Diagnosis if condition holds:** {inline(conditional.get('diagnosis'))}",
            ])
        out.append("")

    checks = report.get("fact_checks_needed", [])
    if checks:
        out.extend(["## Claims needing external fact-check", ""])
        out.extend(f"- {inline(item)}" for item in checks)
        out.append("")
    caveat = report.get("fallacy_fallacy_caveat")
    if caveat:
        out.extend(["## Caveat", "", inline(caveat), ""])
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", help="Validated v2 JSON report")
    args = parser.parse_args()
    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    print(render(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
