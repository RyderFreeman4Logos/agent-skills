#!/usr/bin/env python3
"""Render structured fallacy-analysis JSON as Markdown."""

from __future__ import annotations
import json
import sys
from pathlib import Path


def esc(s) -> str:
    return str(s).replace("\n", " ").strip()


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} report.json", file=sys.stderr)
        return 2
    report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    findings = report.get("findings", [])
    print("# 逻辑谬误分析报告\n")
    summary = report.get("summary", {})
    print(f"- **总体结论：** {esc(summary.get('overall', ''))}")
    print(f"- **发现数量：** {len(findings)}")
    if summary.get("most_important"):
        print(f"- **最重要的问题：** {esc(summary['most_important'])}")
    print()

    for i, f in enumerate(findings, 1):
        print(f"## {i}. {esc(f.get('name_zh'))}（{esc(f.get('name_en'))}） — {float(f.get('confidence', 0)):.2f}")
        print()
        print(f"> {f.get('evidence_quote', '').strip()}")
        print()
        print(f"**目标/结论：** {esc(f.get('conclusion_or_target', ''))}\n")
        print(f"**论证动作：** {esc(f.get('argumentative_move', ''))}\n")
        print(f"**为什么有问题：** {esc(f.get('why_fallacious', ''))}\n")
        print(f"**最强非谬误解释：** {esc(f.get('strongest_non_fallacious_interpretation', ''))}\n")
        print(f"**裁定：** {esc(f.get('adjudication', ''))}\n")
        print(f"**重要性：** {esc(f.get('centrality', ''))}\n")
        print(f"**需要事实核查：** {'是' if f.get('fact_check_needed') else '否'}\n")
        print(f"**如何修复：** {esc(f.get('repair', ''))}\n")

    non_findings = report.get("important_non_findings", [])
    if non_findings:
        print("## 重要的非谬误项\n")
        for x in non_findings:
            print(f"- {esc(x)}")
        print()

    fact_checks = report.get("fact_checks_needed", [])
    if fact_checks:
        print("## 需要额外事实核查\n")
        for x in fact_checks:
            print(f"- {esc(x)}")
        print()

    caveat = report.get("fallacy_fallacy_caveat")
    if caveat:
        print("## 解释边界\n")
        print(esc(caveat))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
