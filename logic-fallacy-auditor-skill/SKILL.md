---
name: logic-fallacy-auditor
description: Analyze input text for logical fallacies, rhetorical fallacies, and reasoning defects. Reconstruct arguments charitably, map findings to a 65-concept bilingual taxonomy, quote exact evidence, distinguish invalid reasoning from merely false/unsupported claims, and report confidence plus the strongest non-fallacious interpretation.
---

# Logic Fallacy Auditor

Use this skill when the user asks whether a passage, debate, post, transcript, argument, policy claim, article, or conversation contains logical fallacies or defective reasoning.

The skill is designed for **reasoning analysis**, not keyword matching. A fallacy label must be justified by the inferential role that a sentence plays in an argument.

## Core principle

Do **not** ask only “does this sentence resemble a fallacy example?” Ask:

1. What conclusion is being asserted?
2. Which premises or considerations are offered in support of it?
3. What inference connects the premises to the conclusion?
4. Does that inference exhibit a recognizable defect?
5. Is there a stronger, reasonable interpretation under which the argument is not fallacious?

A false conclusion is not automatically a fallacy. A fallacious argument does not automatically make its conclusion false.

## Required references

Before doing a careful analysis, consult:

- `references/methodology.md` — decision procedure and false-positive controls.
- `references/fallacies.json` — manifest for `fallacies-part-01.json` through `fallacies-part-04.json`; run `python3 scripts/load_taxonomy.py` to reconstruct the complete machine-readable taxonomy.
- `references/65-fallacies.md` — index linking the ordered human-readable taxonomy parts; read all parts for a complete taxonomy-wide analysis.
- `references/sources.md` — provenance and external references.

For long inputs, also use `scripts/prepare_input.py` to normalize and line-number the text.

## Analysis procedure

### 1. Segment the input into argument units

Separate:

- claims/conclusions;
- explicit premises;
- implicit premises that are reasonably required by the inference;
- examples or illustrations;
- emotional/rhetorical language;
- factual assertions requiring external verification;
- non-argumentative material such as greetings, insults, jokes, or narration.

Do not force every sentence into an argument.

### 2. Reconstruct charitably

Before assigning a fallacy, state the strongest plausible version of the argument that is consistent with the text. Prefer the interpretation that makes the speaker most rational without inventing new evidence.

This prevents a fallacy detector from itself committing a straw man.

### 3. Test the inference, not the vocabulary

A keyword is never sufficient evidence.

Examples:

- An insult is **not automatically ad hominem**. It is ad hominem when the insult or personal trait is used as a reason to dismiss the person's claim or argument.
- Mentioning fear is **not automatically appeal to fear**. It becomes fallacious when fear substitutes for relevant evidence.
- Citing an expert is **not automatically appeal to authority**. Expertise can be legitimate evidence when the expert is qualified, the field is appropriate, and the claim tracks expert consensus or evidence.
- A sequence of consequences is **not automatically a slippery slope**. It is fallacious only when crucial links are asserted without adequate support or inevitability is overstated.
- Correlation can legitimately support causal inference when backed by design, mechanism, controls, temporality, intervention, or other causal evidence.

### 4. Match against the taxonomy

Prefer the narrowest applicable entry in the complete machine-readable taxonomy assembled by `python3 scripts/load_taxonomy.py`, or use the matching entry in `references/65-fallacies.md` and its linked part.

If multiple labels describe the same defect, choose one primary label and put the others in `related_fallacies`.

If a genuine reasoning defect is not represented in the 65-concept taxonomy, use:

`unclassified_reasoning_issue`

and describe the defect without inventing a standard fallacy name.

### 5. Apply confidence thresholds

Use a numeric confidence from 0.00 to 1.00.

- `0.85–1.00`: clear structure and strong textual evidence.
- `0.70–0.84`: likely, but some context or reconstruction is uncertain.
- `0.45–0.69`: plausible/tentative; report only in exhaustive analysis or clearly mark as tentative.
- `<0.45`: normally omit from findings; mention only as a rejected hypothesis if useful.

Never convert uncertainty into certainty merely because a fallacy label sounds familiar.

### 6. Separate reasoning diagnosis from fact checking

If the defect depends on whether a factual premise is true, write `fact_check_needed: true` and explain what fact would need verification.

Examples:

- “Scientists agree X” may be an anonymous-authority problem if no source is given, but whether X is actually the scientific consensus requires fact checking.
- “A happened before B, therefore A caused B” can be diagnosed structurally as post hoc even before checking whether A and B occurred.

### 7. For every finding, include all of these

- exact evidence quote;
- conclusion being supported/attacked;
- premise or argumentative move;
- canonical fallacy ID and Chinese/English name;
- why the inference is defective;
- strongest non-fallacious interpretation;
- why that interpretation does or does not rescue the argument;
- confidence;
- centrality: `central`, `supporting`, or `rhetorical`;
- fact-check requirement;
- a repaired version of the argument that avoids the fallacy while preserving as much intent as possible.

### 8. Check for the fallacy fallacy

After identifying a fallacy, explicitly avoid the inference:

> “This argument is fallacious, therefore its conclusion is false.”

A better statement is:

> “This reasoning does not establish the conclusion. The conclusion may still be true for independent reasons.”

### 9. Report important non-findings

When a likely accusation would be misleading, say so. Examples:

- “This is harsh rhetoric, but not an ad hominem inference.”
- “This relies on expert evidence, but the appeal is not inherently fallacious.”
- “This is a causal claim with supporting mechanism; correlation alone is not being used as proof.”

This is especially important when analyzing contentious political, scientific, legal, or interpersonal material.

## Default human-readable output

Use the language of the user's input unless asked otherwise.

Recommended structure:

```markdown
## 结论
- 是否存在明显逻辑谬误：是 / 否 / 存在若干可疑项
- 高置信度：N
- 中等置信度：N
- 最影响核心结论的谬误：...

## 逐项分析
### 1. 稻草人（Straw Man） — 置信度 0.92
**原文：** “...”
**它在论证中做什么：** ...
**问题：** ...
**最强非谬误解释：** ...
**判断：** ...
**如何修复：** ...

## 不能仅凭本文判断的事项
- ...

## 总体评价
说明这些问题削弱的是哪些推论，而不是直接宣布整个立场为真或为假。
```

## Structured / workflow output

When the result will be consumed by another agent or workflow, emit JSON conforming to `schemas/report.schema.json`.

Suggested pipeline:

```bash
python3 scripts/prepare_input.py input.txt > prepared.json
# Agent analyzes input and writes report.json
python3 scripts/validate_report.py --input input.txt --report report.json
python3 scripts/render_report.py report.json > report.md
```

`validate_report.py` verifies taxonomy IDs, confidence ranges, required fields, and whether evidence quotes really occur in the original input.

## Long-input strategy

For transcripts/articles longer than the model can analyze reliably in one pass:

1. Normalize and line-number with `prepare_input.py`.
2. Analyze overlapping chunks for candidate fallacies.
3. Merge candidates by argument, not merely by repeated label.
4. Run a global pass over the reconstructed argument graph.
5. Drop local findings that disappear when wider context is considered.
6. Validate quotes against the original text.

Do not treat chunk boundaries as argumentative boundaries.

## Scope note

The bundled 65 concepts are the de-duplicated union used for this skill's initial taxonomy. Some entries are classical logical fallacies; others are informal fallacies, rhetorical manipulation patterns, or reasoning-quality warnings. The taxonomy is a detection vocabulary, **not a claim that every entry has identical status in formal logic**.

For a broader search space, consult the Internet Encyclopedia of Philosophy reference in `references/sources.md`; it catalogs many more named fallacies. Do not automatically import a new label without explaining its definition.
