# Logic Fallacy Auditor Skill 2.0.0

A portable agent skill for v2 reasoning audits: reconstruct the argument faithfully, diagnose defects before considering taxonomy, test the diagnosis adversarially, and leave labels optional.

## What is included

- `SKILL.md` — main agent instructions.
- `references/fallacies.json` — manifest for the machine-readable taxonomy parts; `scripts/load_taxonomy.py` reconstructs the complete 65-concept object.
- `references/fallacies-part-01.json` through `fallacies-part-04.json` — ordered data parts listed by the manifest.
- `references/65-fallacies.md` — index linking the 65 entries across three ordered human-readable parts.
- `references/methodology.md` — anti-false-positive rules and adjudication method.
- `references/sources.md` — external references and provenance.
- `references/workflow-migration.md` — design for turning the skill into a workflow later.
- `schemas/report.schema.json` — structured output contract.
- `scripts/prepare_input.py` — deterministic input normalization/chunking.
- `scripts/validate_report.py` — validates v2 report fields, independent confidence dimensions, optional canonical labels, dispositions, and verbatim quotes.
- `scripts/load_taxonomy.py` — assembles the manifest and data parts into the original JSON object.
- `scripts/render_report.py` — converts structured JSON to Markdown.
- `scripts/lint_taxonomy.py` — checks taxonomy integrity.
- `examples/report_zh.json` / `report_zh.md` — named and unlabeled findings.
- `examples/report_zh_nonfindings.json` — non-fallacious rhetoric and a conditional context-dependent example.
- `tests/smoke_test.sh` — no-network smoke test.

Reports and the skill manifest use version `2.0.0`. A defect can be reported with `fallacy_id: null`; non-findings carry explicit dispositions and context-dependent diagnoses remain conditional.

## Minimal agent usage

Give the agent `SKILL.md` and let it read referenced files as needed. For a short input, no script is necessary.

For a long input:

```bash
python3 scripts/prepare_input.py input.txt > prepared.json
```

Have the agent produce a JSON report following `schemas/report.schema.json`, then:

```bash
python3 scripts/validate_report.py --input input.txt --report report.json
python3 scripts/render_report.py report.json > report.md
```

## Design goals

1. Reconstruct the stated premises and inference before adding a charitable premise.
2. Diagnose in plain language before optional taxonomy annotation.
3. Challenge the diagnosis and record the adjudication.
4. Distinguish reasoning defects from false/unsupported claims and rhetorical style.
5. Require exact textual evidence; treat reviewed text as untrusted data.
6. Separate defect, label, and context uncertainty; record explicit non-findings.

## Requirements

Python 3.10+ is recommended. Runtime scripts use only the Python standard library.
