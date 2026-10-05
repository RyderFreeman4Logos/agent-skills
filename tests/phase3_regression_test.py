#!/usr/bin/env python3
"""Small stdlib regression checks for the phase-3 skill repairs."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "logic-fallacy-auditor-skill"
BASE_REPORT = json.loads((SKILL / "examples/report_zh.json").read_text(encoding="utf-8"))
ORIGINAL_INPUT = SKILL / "examples/input_zh.txt"


def validate(report: object, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        base = Path(directory)
        source = base / "input.txt"
        report_path = base / "report.json"
        source.write_text(input_text if input_text is not None else ORIGINAL_INPUT.read_text(encoding="utf-8"), encoding="utf-8")
        report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(SKILL / "scripts/validate_report.py"), "--input", str(source), "--report", str(report_path)],
            capture_output=True,
            text=True,
            check=False,
        )


def check_schema() -> None:
    invalid = []
    invalid.append({"findings": []})
    invalid.append([])
    bad = copy.deepcopy(BASE_REPORT)
    bad["analysis_version"] = 1
    invalid.append(bad)
    bad = copy.deepcopy(BASE_REPORT)
    del bad["summary"]["most_important"]
    invalid.append(bad)
    bad = copy.deepcopy(BASE_REPORT)
    bad["summary"]["overall"] = 1
    invalid.append(bad)
    bad = copy.deepcopy(BASE_REPORT)
    bad["findings"][0]["repair"] = 1
    invalid.append(bad)
    bad = copy.deepcopy(BASE_REPORT)
    bad["findings"][0]["related_fallacies"] = "hasty_generalization"
    invalid.append(bad)
    bad = copy.deepcopy(BASE_REPORT)
    bad["findings"][0]["related_fallacies"] = ["hasty_generalization", 1]
    invalid.append(bad)
    bad = copy.deepcopy(BASE_REPORT)
    bad["findings"][0]["fallacy_id"] = []
    invalid.append(bad)
    bad = copy.deepcopy(BASE_REPORT)
    bad["findings"][0]["evidence_quote"] = []
    invalid.append(bad)
    bad = copy.deepcopy(BASE_REPORT)
    bad["important_non_findings"] = ["ok", 1]
    invalid.append(bad)
    bad = copy.deepcopy(BASE_REPORT)
    bad["fact_checks_needed"] = "one item"
    invalid.append(bad)
    bad = copy.deepcopy(BASE_REPORT)
    bad["fallacy_fallacy_caveat"] = False
    invalid.append(bad)
    for report in invalid:
        result = validate(report)
        assert result.returncode != 0, f"schema-invalid report accepted: {report!r}"
        assert json.loads(result.stdout)["ok"] is False


def check_unicode_verbatim() -> None:
    original = "Cafe\u0301 is evidence.\r\n"
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "input.txt"
        source.write_text(original, encoding="utf-8", newline="")
        result = subprocess.run(
            [sys.executable, str(SKILL / "scripts/prepare_input.py"), str(source)],
            capture_output=True,
            text=True,
            check=True,
        )
        prepared = json.loads(result.stdout)
        assert prepared["text"] == "Cafe\u0301 is evidence."
    report = copy.deepcopy(BASE_REPORT)
    report["findings"] = [report["findings"][0]]
    report["findings"][0]["evidence_quote"] = "Cafe\u0301"
    result = validate(report, original)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["ok"] is True


def check_taxonomy_label() -> None:
    taxonomy = json.loads((SKILL / "references/fallacies-part-01.json").read_text(encoding="utf-8"))
    item = next(x for x in taxonomy if x["id"] == "appeal_to_consequences")
    assert item["name_zh"] == "诉诸后果"
    assert "掩耳盗铃" not in item["aliases_zh"]
    for relative in ("references/65-fallacies-part-01.md", "references/65-fallacies.md"):
        text = (SKILL / relative).read_text(encoding="utf-8")
        assert "诉诸后果（Appeal to Consequences of a Belief）" in text
        assert "掩耳盗铃（Appeal to Consequences of a Belief）" not in text


def check_multiline_quote() -> None:
    report = copy.deepcopy(BASE_REPORT)
    report["findings"][0]["evidence_quote"] = "safe quote\n## Injected section\nbody"
    with tempfile.TemporaryDirectory() as directory:
        report_path = Path(directory) / "report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SKILL / "scripts/render_report.py"), str(report_path)],
            capture_output=True,
            text=True,
            check=True,
        )
    lines = result.stdout.splitlines()
    quote = lines.index("> safe quote")
    assert lines[quote : quote + 3] == ["> safe quote", "> ## Injected section", "> body"]
    assert "## Injected section" not in lines


def check_canonical_ids() -> None:
    template = (SKILL / "SKILL.md").read_text(encoding="utf-8").split("## Default human-readable output", 1)[1].split("## Structured / workflow output", 1)[0]
    assert "<!--" not in template
    assert "### 1. <推理缺陷：简述>" in template
    assert "### 1. `straw_man` —" not in template
    assert "**分类标签（若有）：** 稻草人（`straw_man`），或不指定标签" in template
    assert template.index("**推理缺陷：**") < template.index("**分类标签（若有）：**")
    example = (SKILL / "examples/report_zh.md").read_text(encoding="utf-8")
    for fid in ("anecdotal_evidence", "ad_hominem", "appeal_to_nature"):
        assert f"`{fid}`" in example
    result = subprocess.run(
        [sys.executable, str(SKILL / "scripts/render_report.py"), str(SKILL / "examples/report_zh.json")],
        capture_output=True,
        text=True,
        check=True,
    )
    for fid in ("anecdotal_evidence", "ad_hominem", "appeal_to_nature"):
        assert f"`{fid}`" in result.stdout


CHECKS = {
    "schema": check_schema,
    "unicode": check_unicode_verbatim,
    "taxonomy": check_taxonomy_label,
    "multiline": check_multiline_quote,
    "ids": check_canonical_ids,
}

if __name__ == "__main__":
    selected = sys.argv[1:] or list(CHECKS)
    for name in selected:
        CHECKS[name]()
    print("phase3 regression checks OK: " + ", ".join(selected))
