# Methodology and false-positive controls

## 1. What counts as a fallacy finding?

A finding should identify a **defect in reasoning or argumentative relevance**, not merely an objectionable statement, a factual mistake, a disliked conclusion, or persuasive language.

Minimum evidence for a finding:

1. an identifiable claim/conclusion or argumentative target;
2. an identifiable premise, reason, rhetorical substitute, or inference;
3. an explanation of why the move fails to support or defeat the target in the way asserted.

If one of these is missing, prefer `unsupported_claim`, `fact_check_needed`, or no finding rather than forcing a fallacy label.

## 2. Charitable reconstruction

Use this order:

1. Literal reading.
2. Contextual reading.
3. Strongest reasonable interpretation consistent with the text.
4. Only then diagnose a fallacy.

Do not invent hidden premises just to make the argument fallacious.

## 3. Fallacy vs. weak evidence

Weak evidence is not always a named fallacy.

Examples:

- One small study may be weak evidence without being an appeal to authority.
- A tentative causal hypothesis based on correlation may be under-supported but not necessarily the categorical `correlation = causation` fallacy.
- A prediction containing a chain of events may be speculative without being a slippery slope if probabilities and mechanisms are explicitly acknowledged.

## 4. Fallacy vs. rhetorical device

Some bundled labels describe rhetorical manipulation rather than strict invalidity. Mark `centrality: rhetorical` when the move mainly changes persuasion, framing, or salience rather than the formal support relation.

Examples include flattery, vividness, spite, fear, ridicule, and some uses of emotional appeal.

## 5. Formal-pattern checks

### Affirming the consequent

Form:

- If P, then Q.
- Q.
- Therefore P.

Invalid because Q may have causes/explanations other than P.

### Denying the antecedent

Form:

- If P, then Q.
- Not P.
- Therefore not Q.

Invalid because Q may occur without P.

### Undistributed middle

Typical form:

- All A are C.
- All B are C.
- Therefore A are B.

Sharing a property does not establish identity or subset relations.

## 6. Causal checks

Before flagging false cause, post hoc, correlation-causation, or ignored common cause, ask:

- Is the claim causal or merely correlational?
- Is temporality established?
- Is there a plausible mechanism?
- Are alternative causes discussed?
- Is there experimental/quasi-experimental evidence?
- Are confounders controlled?
- Is the speaker claiming certainty or only increasing probability?

Do not punish appropriately hedged causal reasoning.

## 7. Authority checks

Authority evidence can be legitimate. Check:

- Is the authority identifiable?
- Is the authority qualified in the relevant domain?
- Is the claim within that domain?
- Is the authority reporting evidence/consensus, or asking for deference?
- Is there meaningful expert disagreement?
- Is the authority being used as the *only* reason when direct evidence is available?

Use `appeal_to_anonymous_authority` when anonymity prevents evaluation. Use `appeal_to_questionable_authority` when qualification/reliability is mismatched. Use `appeal_to_authority` for a broader inappropriate deference pattern.

## 8. Ad hominem checks

Require an inferential substitution:

> Person has trait T → therefore person's claim C is false/should be dismissed.

An insult that does not function as a premise is uncivil rhetoric, not necessarily ad hominem.

`circumstantial_ad_hominem` is narrower: the claim is dismissed solely because the speaker has an interest, affiliation, incentive, or circumstance.

## 9. Generalization checks

Distinguish:

- `hasty_generalization`: sample too small/insufficient.
- `biased_generalization`: sample unrepresentative or selection-biased.
- `spotlight_fallacy`: salient/media-visible cases treated as representative.
- `sweeping_generalization`: a general rule is applied too broadly to exceptional cases.

## 10. Emotion checks

Emotion is not inherently fallacious. Emotional evidence may be relevant to value judgments, harms, preferences, or lived experience.

Flag an emotional appeal when emotion is used **instead of** a needed reason/evidence or is used to obscure the missing inference.

## 11. Missing context

If the input quotes or responds to another speaker but omits the original argument, reduce confidence for straw-man, tu-quoque, loaded-question, and related dialogue-dependent labels.

## 12. Confidence discipline

Confidence should reflect both:

- fit between the observed inference and the fallacy definition;
- completeness of context.

A textbook-looking sentence with missing context may deserve lower confidence than a less obvious pattern with a complete argument.

## 13. Centrality

- `central`: removing the fallacy materially breaks the main conclusion.
- `supporting`: weakens a subsidiary premise or supporting branch.
- `rhetorical`: mainly manipulates framing/emotion/salience and may not be necessary to the inference.

## 14. Repair principle

A repair should preserve the author's goal where possible while replacing the defective inference with:

- direct evidence;
- a narrower conclusion;
- explicit uncertainty/probability;
- a representative sample;
- a valid conditional form;
- a causal mechanism and controls;
- a relevant response to the actual opposing claim;
- a properly qualified expert source.
