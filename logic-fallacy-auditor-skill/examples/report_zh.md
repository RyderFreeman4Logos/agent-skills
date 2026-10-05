# Reasoning Audit

Version: 2.0.0

## Summary

三项有明确分类标签，另有一项无标签推理缺口；单纯辱骂与缺少对手原话的情形见独立的非发现示例。

**Most important:** 单一个案不足以否定吸烟者总体风险；这削弱的是原文给出的理由，不直接证明相反结论。

## Findings

### Finding 1

**Evidence quote:**
> 我爷爷每天抽两包烟，活到92岁。所以吸烟不会缩短寿命。

**Faithful reconstruction:**
- Premise: 说话者的祖父每天抽两包烟，活到92岁。
- Conclusion: 吸烟不会缩短寿命。
- Inference: 以一个吸烟且长寿的个案否定吸烟对群体寿命的总体风险。
- Target: 吸烟不会缩短寿命。

**Reasoning issue (weak_induction):** 单一个案不足以代表吸烟者总体，也不能抵消群体层面的风险差异。
**Why it matters:** 个体反例至多反驳‘每个吸烟者都会早逝’，不能据此推出吸烟不会缩短寿命。
**Strongest non-fallacious reading:** 说话者可能只想说明吸烟不保证每个个体都会早逝；这比原文的总体结论窄。
**New premise needed to rescue it:** 要由该个案推断总体风险，还需要有代表性样本或群体数据；原文没有提供。
**Adversarial review:** 个案确能反驳‘吸烟必定使每个吸烟者早逝’，但原文结论并非这一较弱命题。
**Adjudication:** 将原文按其总体结论理解时，个案不能支持结论，诊断成立。
**Narrow taxonomy annotation:** 轶事证据 (`anecdotal_evidence`)
**Confidence (defect / label / context):** high / high / high
**Fact-check needed:** False
**Minimal repair:** 比较有代表性的吸烟者与不吸烟者群体数据，并把结论限定为风险或期望寿命差异。
**Related taxonomy entries:** hasty_generalization

### Finding 2

**Evidence quote:**
> 你说吸烟有风险？你只是个没混出名堂的人，你的话当然不可信。

**Faithful reconstruction:**
- Premise: 对方没有混出名堂。
- Conclusion: 对方关于吸烟风险的主张不可信。
- Inference: 以对方的一般社会成就评价否定其事实主张。
- Target: 对方关于吸烟风险的主张不可信。

**Reasoning issue (irrelevant_support):** 个人是否‘混出名堂’与吸烟风险没有建立证据上的关联。
**Why it matters:** 对人的贬低没有回答其主张所依据的研究、数据或因果理由。
**Strongest non-fallacious reading:** 若讨论的是相关专业资质，资质有时能影响证言权重；原文谈的不是专业能力。
**New premise needed to rescue it:** No additional premise identified.
**Adversarial review:** 只有在‘混出名堂’被明确界定为与吸烟风险相关的专业能力时，这项信息才可能相关；文本没有这种联系。
**Adjudication:** 原文以一般地位代替对论据的回应，诊断成立。
**Narrow taxonomy annotation:** 人身攻击 (`ad_hominem`)
**Confidence (defect / label / context):** high / high / high
**Fact-check needed:** False
**Minimal repair:** 直接回应对方使用的证据；若质疑其资质，说明具体资质与该命题的关系。

### Finding 3

**Evidence quote:**
> 再说，天然的东西当然更安全。

**Faithful reconstruction:**
- Premise: 某物是天然的。
- Conclusion: 某物更安全。
- Inference: 仅由天然属性推出安全性。
- Target: 天然来源可以证明某物更安全。

**Reasoning issue (unsupported_claim):** 天然来源本身不能推出低毒性、低风险或适合特定剂量和用途。
**Why it matters:** 安全性取决于具体材料、剂量和暴露方式；‘天然’不是充分证据。
**Strongest non-fallacious reading:** 说话者可能暗指某类具体材料具有已知的安全记录，但文本未给出该证据。
**New premise needed to rescue it:** 需要与具体材料、剂量和用途相关的可靠安全证据；原文没有提供。
**Adversarial review:** 天然属性可能与某些材料的安全特征相关，但若如此，仍须给出具体机制或证据。
**Adjudication:** 文本直接把‘天然’当作安全性的理由，分类成立；实际安全性需另行核查。
**Narrow taxonomy annotation:** 诉诸自然 (`appeal_to_nature`)
**Confidence (defect / label / context):** high / high / high
**Fact-check needed:** True
**Minimal repair:** 提供与具体材料、剂量、暴露途径和使用场景相关的安全数据。

### Finding 4

**Evidence quote:**
> 她按时提交了文件，所以文件符合审批标准。

**Faithful reconstruction:**
- Premise: 她按时提交了文件。
- Conclusion: 文件符合审批标准。
- Inference: 由按时提交推出内容符合标准。
- Target: 文件符合审批标准。

**Reasoning issue (missing_premise):** 按时提交不能单独证明文件内容符合审批标准。
**Why it matters:** 推论需要一条把提交时间与内容合规联系起来的规则或证据。
**Strongest non-fallacious reading:** 按时提交可能只是合规流程中的一项条件，而非内容审查结论。
**New premise needed to rescue it:** 存在一条适用规则，保证按时提交的文件必然符合内容标准；原文没有提供该规则。
**Adversarial review:** 若另有规则明确把按时提交定义为审批合格，结论才可能成立；这需要文本外依据。
**Adjudication:** 文本未给出该规则，推理缺口成立；没有必要强贴某个谬误标签。
**Narrow taxonomy annotation:** None assigned.
**Confidence (defect / label / context):** high / not applicable / high
**Fact-check needed:** False
**Minimal repair:** 补充实际适用的内容审查规则，或把结论收窄为文件已按时提交。

## Non-findings

No separate non-finding disposition was recorded.

## Claims needing external fact-check

- 如需据此作实际安全决策，应核查具体材料、剂量和暴露途径的毒理与安全证据。

## Caveat

这些诊断说明给出的理由不足以建立相应结论；它们本身不证明相反结论必然为真。
