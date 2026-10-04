# Migration path: Skill → workflow

The skill is deliberately decomposed so it can later become a multi-stage workflow without changing the taxonomy or output contract.

## Recommended stages

### Stage A — Normalize
Input: raw text/file/transcript
Output: normalized text + stable line numbers
Implementation: `scripts/prepare_input.py`

### Stage B — Argument extraction
LLM task:
- identify conclusions;
- identify explicit/implicit premises;
- identify reply targets;
- mark factual assertions requiring verification;
- produce argument units with source line ranges.

### Stage C — Candidate detection
LLM task:
- compare each argument unit with `references/fallacies.json`;
- propose zero or more candidates;
- include counter-interpretation and confidence.

This stage can be parallelized over chunks.

### Stage D — Global adjudication
LLM task:
- merge duplicates;
- recover cross-chunk context;
- reject candidates invalidated by wider context;
- detect repeated argument patterns;
- assign centrality.

### Stage E — Validation
Deterministic task:
- schema checks;
- taxonomy ID checks;
- evidence quote checks;
- confidence range checks.
Implementation: `scripts/validate_report.py`

### Stage F — Render
Deterministic task:
- JSON → Markdown or downstream event/artifact.
Implementation: `scripts/render_report.py`

## Checkpoint boundaries

Good checkpoint points are after A, B, C, and D. Stages A/E/F are deterministic and cheap to replay. B/C/D contain model judgment and should preserve model/version/prompt metadata for reproducibility.

## Suggested workflow state

```json
{
  "source": {"id": "...", "sha256": "..."},
  "prepared": {},
  "argument_units": [],
  "candidate_findings": [],
  "adjudicated_report": {},
  "validation": {"ok": true, "errors": []}
}
```

## Parallelism

For long documents:
- split with overlap;
- run argument extraction + candidate detection in parallel;
- adjudicate globally once;
- never let chunk-local confidence become final confidence without the global pass.

## Model-routing idea

A cheaper model can do Stage B candidate extraction. Use the stronger model for Stage D global adjudication because the hardest failures are context loss, misrepresentation, and over-labeling.
