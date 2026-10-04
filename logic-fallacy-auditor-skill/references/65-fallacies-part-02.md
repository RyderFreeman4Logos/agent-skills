## 23. 赌徒谬误（Gambler's Fallacy）

- **ID:** `gamblers_fallacy`
- **分组:** `probability`
- **中文别名:** 赌徒错误
- **English aliases:** gambler's fallacy
- **定义:** 对独立随机事件误以为过去结果会使相反结果‘该出现了’或改变下一次概率。
- **诊断问题:** 这些事件是否独立？过去频率为什么会改变下一次的生成概率？
- **防误报:** 如果抽样不是独立同分布，历史确实可能改变后续概率，需先判断过程。

## 24. 轻率概化（Hasty Generalization）

- **ID:** `hasty_generalization`
- **分组:** `generalization`
- **中文别名:** 草率概括
- **English aliases:** hasty generalisation, hasty generalization
- **定义:** 从过少或信息不足的样本直接推出广泛结论。
- **诊断问题:** 样本量和证据量是否足以支撑结论覆盖的范围？
- **防误报:** 小样本在强效应或确定性反例场景可能足够；要按结论类型判断。

## 25. 妄下定论（Jumping to Conclusions）

- **ID:** `jumping_to_conclusions`
- **分组:** `evidence`
- **中文别名:** 仓促下结论
- **English aliases:** jumping to conclusions
- **定义:** 在容易获得的重要证据尚未考虑前就快速做出确定性判断。
- **诊断问题:** 是否存在明显相关、可获得但被忽略的信息？
- **防误报:** 快速判断在时间受限情境可能合理，但置信度应与证据相匹配。

## 26. 中间立场（Middle Ground）

- **ID:** `middle_ground`
- **分组:** `compromise`
- **中文别名:** 中间道路谬误、折中谬误
- **English aliases:** middle ground, middle ground fallacy
- **定义:** 仅因为两方意见相反，就假定真相或正确方案必定位于两者之间。
- **诊断问题:** 为什么两个主张的中点比任一端点更有证据？
- **防误报:** 折中可以是谈判策略或价值选择；谬误在于把折中位置当作事实正确性的证明。

## 27. 完美主义谬误（Perfectionist Fallacy）

- **ID:** `perfectionist_fallacy`
- **分组:** `comparison`
- **中文别名:** 完美方案谬误、涅槃谬误
- **English aliases:** perfectionist fallacy, nirvana fallacy
- **定义:** 因为方案不能完美解决问题，就断言它没有价值或应被拒绝。
- **诊断问题:** 比较标准是现实替代方案，还是不可达的完美状态？
- **防误报:** 某些任务确实要求接近零失败；此时高标准可能合理。

## 28. 相对论谬误（Relativist Fallacy）

- **ID:** `relativist_fallacy`
- **分组:** `truth`
- **中文别名:** 相对主义谬误
- **English aliases:** relativist fallacy
- **定义:** 仅以‘对你是真的、对我不是真的’回避本可客观评估的事实命题。
- **诊断问题:** 该命题是真正主观/规范性的，还是具有共同事实判准？
- **防误报:** 偏好和某些价值判断可以合法相对化；不要把主观差异误判为谬误。

## 29. 以偏概全（Biased Generalization）

- **ID:** `biased_generalization`
- **分组:** `generalization`
- **中文别名:** 偏差概括、代表性偏差概括
- **English aliases:** biased generalising, biased generalization
- **定义:** 从系统性不具代表性、存在选择偏差的样本推断总体。
- **诊断问题:** 样本是如何产生的？其选择机制会不会偏向某类结果？
- **防误报:** 非随机样本并非必然无效，但需要说明其对目标总体的代表性。

## 30. 一概而论（Sweeping Generalization）

- **ID:** `sweeping_generalization`
- **分组:** `generalization`
- **中文别名:** 扫荡式概括、规则误用
- **English aliases:** sweeping generalisation, sweeping generalization
- **定义:** 把通常成立的规则不加条件地应用到明显存在例外或边界条件的个案。
- **诊断问题:** 这条一般规则是否有相关例外，而当前个案恰好处在例外条件中？
- **防误报:** 一般规则可以支持默认推断，但应允许与证据相符的例外。

## 31. 中词不周延（Undistributed Middle）

- **ID:** `undistributed_middle`
- **分组:** `formal`
- **中文别名:** 中项不周延
- **English aliases:** undistributed middle
- **定义:** 因为两个对象都具有某个共同属性，就错误地推出它们彼此相同、属于同一类或有更强关系。
- **诊断问题:** 共同拥有中间属性 C，为什么能推出 A 与 B 的关系？
- **防误报:** 如果还有包含关系或排他条件等额外前提，结论可能成立。

## 32. 临阵救援（Ad Hoc Rescue）

- **ID:** `ad_hoc_rescue`
- **分组:** `belief_protection`
- **中文别名:** 特设救援、临时补丁谬误
- **English aliases:** ad hoc rescue
- **定义:** 面对反证时不断添加只为保护原结论、且缺乏独立依据的新解释。
- **诊断问题:** 新增假设是否有独立可检验依据，还是只在反证出现后为保住结论而加入？
- **防误报:** 科学理论也会增加辅助假设；关键在于新假设是否独立可检验并提高解释/预测能力。

## 33. 乞求论题（Begging the Question）

- **ID:** `begging_the_question`
- **分组:** `circularity`
- **中文别名:** 窃取论点、预设结论
- **English aliases:** begging the question, petitio principii
- **定义:** 在前提中直接或变相预设了需要证明的结论。
- **诊断问题:** 如果不先接受结论，前提还能独立成立吗？
- **防误报:** 与循环论证高度相关；应指出具体预设，而不只贴标签。

## 34. 一孔之见（Spotlight Fallacy）

- **ID:** `spotlight_fallacy`
- **分组:** `generalization`
- **中文别名:** 聚光灯谬误、显著性样本谬误
- **English aliases:** spotlight fallacy
- **定义:** 把媒体、社交网络或注意力机制高度可见的案例当成总体的典型分布。
- **诊断问题:** 被看到的案例是否因为显著性而过度代表总体？
- **防误报:** 高可见度数据有时是真实趋势的信号，但必须用总体数据校验。

## 35. 确认偏误（Confirmation Bias）

- **ID:** `confirmation_bias_argument`
- **分组:** `evidence_selection`
- **中文别名:** 确认偏差
- **English aliases:** confirmation bias
- **定义:** 只寻找、强调或保留支持既有观点的证据，同时系统性忽略反证。
- **诊断问题:** 是否对支持与反对证据采用了不对称的搜索、采信或评价标准？
- **防误报:** 单次遗漏反证不一定构成模式；最好有证据表明选择机制具有方向性。

## 36. 伪二分法（False Dilemma）

- **ID:** `false_dilemma`
- **分组:** `alternatives`
- **中文别名:** 非黑即白、虚假两难、错误二分
- **English aliases:** false dilemma, false dichotomy, black-or-white
- **定义:** 把两个选项呈现为全部可能性，隐去合理的第三种或连续方案。
- **诊断问题:** 真的只有这两个互斥且穷尽的选项吗？
- **防误报:** 某些系统确实只有两个选项；需证明选项集合是否穷尽。

## 37. 谎言（Lie）

- **ID:** `lie`
- **分组:** `rhetoric`
- **中文别名:** 故意虚假陈述
- **English aliases:** lie
- **定义:** 明知陈述为假仍把它作为事实提出。严格说这不是由逻辑形式本身即可诊断的谬误，而是需要意图证据的欺骗行为。
- **诊断问题:** 是否有证据证明说话者不仅说错了，而且知道其为假？
- **防误报:** 仅凭陈述错误不能断言‘撒谎’；若缺乏意图证据，应改称错误陈述或待核查事实。

## 38. 误导性鲜活个案（Misleading Vividness）

- **ID:** `misleading_vividness`
- **分组:** `rhetoric`
- **中文别名:** 鲜活性谬误、生动性误导
- **English aliases:** misleading vividness
- **定义:** 用极其生动、罕见或情绪强烈的个案制造其普遍或高概率的印象。
- **诊断问题:** 案例的生动程度是否替代了发生率、基准率或总体分布？
- **防误报:** 生动案例可以说明后果形态，但不能单独证明频率。

## 39. 转移注意（Red Herring）

- **ID:** `red_herring`
- **分组:** `relevance`
- **中文别名:** 红鲱鱼、转移话题
- **English aliases:** red herring
- **定义:** 引入看似相关但不能解决当前争点的材料，使讨论偏离原问题。
- **诊断问题:** 新材料是否真正回答了当前主张，还是把注意力转到另一个问题？
- **防误报:** 背景信息可能相关；关键是它是否改变对原争点的证据或推理。

## 40. 滑坡谬误（Slippery Slope）

- **ID:** `slippery_slope`
- **分组:** `causality`
- **中文别名:** 滑坡
- **English aliases:** slippery slope
- **定义:** 声称一个起点会通过一连串步骤不可避免地导致极端结果，却未充分支持关键中间环节或概率。
- **诊断问题:** 链条中的每一步是否有机制和概率支持？为什么会不可避免？
- **防误报:** 有机制、有数据的连锁风险分析不是谬误；问题是不受支持的必然化。

## 41. 隐瞒证据（Suppressed Evidence）

- **ID:** `suppressed_evidence`
- **分组:** `evidence_selection`
- **中文别名:** 压制证据、选择性隐瞒
- **English aliases:** suppressed evidence, cherry-picking by omission
- **定义:** 省略对自身结论显著不利且应纳入判断的重要证据。
- **诊断问题:** 是否存在已知、相关、重要的反证被选择性排除？
- **防误报:** 简短表达不可能列出所有证据；要证明被省略信息足以实质改变判断。

## 42. 无法证伪（Unfalsifiability）

- **ID:** `unfalsifiability`
- **分组:** `testability`
- **中文别名:** 不可证伪
- **English aliases:** unfalsifiability, unfalsifiable claim
- **定义:** 提出一个无论出现什么观察结果都能被解释为正确、没有潜在反证条件的经验性主张。
- **诊断问题:** 什么观察结果会让提出者承认该命题错了？如果没有，经验检验如何进行？
- **防误报:** 数学、公理、价值陈述不以经验可证伪性为同一标准；不要跨领域机械应用。

## 43. 肯定后件（Affirming the Consequent）

- **ID:** `affirming_the_consequent`
- **分组:** `formal`
- **中文别名:** 肯定结果
- **English aliases:** affirming the consequent
- **定义:** 从‘如果 P 则 Q’和‘Q’推出‘P’，忽略 Q 可能由其他原因产生。
- **诊断问题:** Q 是否只能由 P 导致？若不是，为什么观察到 Q 就能推出 P？
- **防误报:** 若额外证明 P 是 Q 的唯一充分解释，则推断可被加强。

## 44. 循环逻辑（Circular Reasoning）

- **ID:** `circular_reasoning`
- **分组:** `circularity`
- **中文别名:** 循环论证
- **English aliases:** circular logic, circular reasoning
- **定义:** 论据的成立最终依赖于待证明的结论，使支持链条绕回自身而缺乏独立根据。
- **诊断问题:** 追踪理由链条后，是否最终又依赖原结论？
- **防误报:** 概念互定义不一定是论证循环；重点是证成关系是否真正独立。
