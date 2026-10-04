# Logic Fallacy Auditor Skill

A portable agent skill for analyzing whether input text contains logical fallacies, rhetorical fallacies, or reasoning defects.

## What is included

- `SKILL.md` — main agent instructions.
- `references/fallacies.json` — 65-concept bilingual taxonomy.
- `references/65-fallacies.md` — readable reference.
- `references/methodology.md` — anti-false-positive rules and adjudication method.
- `references/sources.md` — external references and provenance.
- `references/workflow-migration.md` — design for turning the skill into a workflow later.
- `schemas/report.schema.json` — structured output contract.
- `scripts/prepare_input.py` — deterministic input normalization/chunking.
- `scripts/validate_report.py` — validates IDs, fields, confidence, and verbatim evidence quotes.
- `scripts/render_report.py` — converts structured JSON to Markdown.
- `scripts/lint_taxonomy.py` — checks taxonomy integrity.
- `examples/` — working Chinese example.
- `tests/smoke_test.sh` — no-network smoke test.

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

1. Diagnose the **inference**, not keywords.
2. Steelman before labeling.
3. Distinguish a false claim from a fallacious argument.
4. Treat expert testimony, emotion, correlation, insults, and risk chains contextually rather than as automatic fallacies.
5. Require exact textual evidence for every structured finding.
6. Include a strongest non-fallacious interpretation for every finding.
7. Preserve a deterministic JSON contract so the skill can later become a multi-stage workflow.

## Requirements

Python 3.10+ is recommended. Runtime scripts use only the Python standard library.
