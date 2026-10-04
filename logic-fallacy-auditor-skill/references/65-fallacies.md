# 65-concept fallacy taxonomy

This is the human-readable view of `fallacies.json`. Definitions are written for detection rather than as canonical philosophical definitions.

## 1. 诉诸匿名权威（Appeal to Anonymous Authority）

- **ID:** `appeal_to_anonymous_authority`
- **分组:** `authority`
- **中文别名:** 匿名权威
- **English aliases:** anonymous authority
- **定义:** 用无法识别或核验的‘专家、研究、大家都说’作为关键证据。
- **诊断问题:** 如果去掉这个匿名来源，结论是否仍有可检查的证据支持？
- **防误报:** 匿名并不自动使信息为假；问题在于匿名性是否阻止了对资质、方法或原始证据的核验。

## 2. 诉诸（可疑）权威（Appeal to Questionable Authority）

- **ID:** `appeal_to_questionable_authority`
- **分组:** `authority`
- **中文别名:** 诉诸可疑权威
- **English aliases:** appeal to dubious authority, questionable authority
- **定义:** 把不具备相关领域资质、可靠性不足或利益冲突严重的权威意见当作结论成立的主要理由。
- **诊断问题:** 被引用者是否真的具备与该命题相匹配的专业能力和可靠性？
- **防误报:** 合格专家意见可以是合理证据，尤其当它代表相关领域共识并可追溯到证据时。

## 3. 诉诸常规（Appeal to Common Practice）

- **ID:** `appeal_to_common_practice`
- **分组:** `appeal`
- **中文别名:** 诉诸惯例
- **English aliases:** common practice
- **定义:** 因为某做法很常见，就推断它正确、合理、道德或不会造成问题。
- **诊断问题:** ‘大家都这样做’与待证明的正确性之间有什么独立联系？
- **防误报:** 常见程度有时与可行性或社会规范相关，但不能单独证明事实真伪或道德正当性。

## 4. 诉诸无知（Appeal to Ignorance）

- **ID:** `appeal_to_ignorance`
- **分组:** `evidence`
- **中文别名:** 无知论证
- **English aliases:** argument from ignorance
- **定义:** 因为一个命题尚未被证明为假，就断言它为真；或反之。
- **诊断问题:** 缺少反证为何能够充当正面证据？
- **防误报:** 在某些封闭搜索空间里，‘没有发现’可以构成证据，但需要说明搜索能力和预期可观测性。

## 5. 诉诸怀疑（Personal Incredulity）

- **ID:** `personal_incredulity`
- **分组:** `appeal`
- **中文别名:** 个人怀疑、诉诸难以置信
- **English aliases:** appeal to incredulity, argument from incredulity
- **定义:** 因为自己难以想象、理解或相信某事，就据此否定它。
- **诊断问题:** 个人的理解困难是否被当成了关于世界的证据？
- **防误报:** 指出机制缺失可以是合理批评；仅仅‘我想不通’则不足以否定命题。

## 6. 身价逻辑（Appeal to Money）

- **ID:** `appeal_to_money`
- **分组:** `appeal`
- **中文别名:** 诉诸财富、诉诸价格
- **English aliases:** appeal to wealth, appeal to money
- **定义:** 把价格高、财富多、地位高等经济信号直接当作真实性、质量或正确性的证明。
- **诊断问题:** 财富/价格与当前待证命题之间是否有可靠的因果或统计联系？
- **防误报:** 价格有时包含市场信息，但必须说明为什么该市场信号对当前结论有效。

## 7. 求新逻辑（Appeal to Novelty）

- **ID:** `appeal_to_novelty`
- **分组:** `appeal`
- **中文别名:** 诉诸新颖、诉诸新事物
- **English aliases:** appeal to novelty
- **定义:** 仅因为某事物更新，就推断它更好、更真或更有效。
- **诊断问题:** ‘更新’本身为什么能证明性能、真实性或价值更高？
- **防误报:** 新版本可能确有改进，但需要具体比较或证据。

## 8. 诉诸主流（Bandwagon / Appeal to Popular Belief）

- **ID:** `bandwagon`
- **分组:** `appeal`
- **中文别名:** 乐队花车、从众谬误、诉诸多数
- **English aliases:** bandwagon, appeal to popularity, ad populum
- **定义:** 因为许多人相信或支持某观点，就把人数本身当作它正确的证明。
- **诊断问题:** 多数人的相信是否被用来替代独立证据？
- **防误报:** 群体共识在某些知识聚合场景可以提供概率证据，但需要说明群体的信息质量和独立性。

## 9. 诉诸概率（Appeal to Probability）

- **ID:** `appeal_to_probability`
- **分组:** `probability`
- **中文别名:** 概率诉诸
- **English aliases:** appeal to probability
- **定义:** 因为某事可能发生，就断言它必然、迟早或实际上已经发生。
- **诊断问题:** 从‘可能’到‘必然/已经’的概率跃迁有何依据？
- **防误报:** 高概率预测不是谬误；问题是把非零可能性直接升级为确定性。

## 10. 诉诸传统（Appeal to Tradition）

- **ID:** `appeal_to_tradition`
- **分组:** `appeal`
- **中文别名:** 传统诉诸
- **English aliases:** appeal to tradition
- **定义:** 因为某观念或做法历史悠久，就推断它正确、最佳或应当继续。
- **诊断问题:** 历史延续本身为何证明当前条件下仍然正确？
- **防误报:** 传统可以携带经验信息，但仍需评估其形成条件和当前适用性。

## 11. 掩耳盗铃（Appeal to Consequences of a Belief）

- **ID:** `appeal_to_consequences`
- **分组:** `appeal`
- **中文别名:** 诉诸后果、诉诸信念后果
- **English aliases:** appeal to consequences
- **定义:** 因为相信某命题会导致令人不愿接受的后果，就据此判定命题为假；或因后果令人愉快而判定为真。
- **诊断问题:** 一个命题令人喜欢或害怕的后果，为什么能改变它的事实真值？
- **防误报:** 当论题本身是政策选择或价值判断时，后果当然相关；本谬误针对把后果当作事实真值证据。

## 12. 诉诸恐惧（Appeal to Fear）

- **ID:** `appeal_to_fear`
- **分组:** `emotion`
- **中文别名:** 恐惧诉诸
- **English aliases:** appeal to fear
- **定义:** 用恐惧、威胁或灾难想象替代证明结论所需的证据。
- **诊断问题:** 恐惧反应是否替代了风险概率、机制或证据？
- **防误报:** 真实风险本身可以构成合理理由；应区分有证据的风险分析与单纯恐吓。

## 13. 诉诸谄媚（Appeal to Flattery）

- **ID:** `appeal_to_flattery`
- **分组:** `emotion`
- **中文别名:** 谄媚诉诸
- **English aliases:** appeal to flattery
- **定义:** 通过赞美受众来诱导其接受一个与赞美无关、缺乏支持的主张。
- **诊断问题:** 赞美与结论之间存在什么逻辑联系？
- **防误报:** 礼貌或建立关系不等于谬误；关键是赞美是否承担了证据角色。

## 14. 诉诸自然（Appeal to Nature）

- **ID:** `appeal_to_nature`
- **分组:** `appeal`
- **中文别名:** 自然主义诉诸
- **English aliases:** appeal to nature
- **定义:** 把‘天然/自然’直接等同于更好、更安全、更道德或更真实。
- **诊断问题:** 为什么‘自然’这一属性能够推出所声称的价值或安全性？
- **防误报:** 自然属性可能与某些具体风险相关，但必须给出具体机制，而不是把‘自然’当作价值标签。

## 15. 诉诸同情（Appeal to Pity）

- **ID:** `appeal_to_pity`
- **分组:** `emotion`
- **中文别名:** 同情诉诸
- **English aliases:** appeal to pity, ad misericordiam
- **定义:** 用同情、可怜或个人困境替代对事实、责任或结论的相关证明。
- **诊断问题:** 同情为何能证明当前事实命题或免除与问题相关的标准？
- **防误报:** 在慈善、量刑、资源分配等价值决策中，同情可能是相关考虑；不应机械标注。

## 16. 诉诸荒谬（Appeal to Ridicule）

- **ID:** `appeal_to_ridicule`
- **分组:** `rhetoric`
- **中文别名:** 诉诸嘲笑、嘲笑谬误
- **English aliases:** appeal to ridicule
- **定义:** 把对方观点描述得可笑、荒诞，以嘲弄代替反驳。
- **诊断问题:** 除了让观点显得可笑之外，是否真正指出了前提或推理错误？
- **防误报:** 使用幽默不等于谬误；只有当嘲笑承担反驳功能时才构成问题。

## 17. 诉诸仇恨（Appeal to Spite）

- **ID:** `appeal_to_spite`
- **分组:** `emotion`
- **中文别名:** 诉诸怨恨、诉诸厌恶
- **English aliases:** appeal to spite
- **定义:** 借助对某人或群体的仇恨、厌恶来否定其主张，而不处理主张本身。
- **诊断问题:** 负面情绪是否替代了对论点内容的评估？
- **防误报:** 相关的利益冲突或行为记录可以影响可信度，但需要具体联系。

## 18. 一厢情愿（Wishful Thinking）

- **ID:** `wishful_thinking`
- **分组:** `evidence`
- **中文别名:** 愿望思维
- **English aliases:** wishful thinking, appeal to wishful thinking
- **定义:** 因为希望某事为真（或不希望其为真）而提高其真实性判断。
- **诊断问题:** 愿望本身是否被当成了证据？
- **防误报:** 愿望可以影响目标选择，但不能直接证明事实命题。

## 19. 轶事证据（Anecdotal Evidence）

- **ID:** `anecdotal_evidence`
- **分组:** `evidence`
- **中文别名:** 个案证据、逸闻证据
- **English aliases:** anecdotal fallacy, anecdotal evidence
- **定义:** 用少数个人经历或孤立案例替代更系统、代表性的证据，尤其用来否定统计规律。
- **诊断问题:** 这个个案能否代表目标总体，还是只是一个可能存在的例外？
- **防误报:** 个案可以用于提出假设、证明‘至少存在一个’或揭示机制；其证明力取决于结论范围。

## 20. 合成谬误（Composition）

- **ID:** `composition`
- **分组:** `part_whole`
- **中文别名:** 合成错误
- **English aliases:** fallacy of composition
- **定义:** 因为部分具有某性质，就推断整体必然具有同一性质。
- **诊断问题:** 该性质从部分到整体是否可加、可传递？
- **防误报:** 某些性质确实可从部分合成到整体；必须检查性质类型。

## 21. 分割谬误（Division）

- **ID:** `division`
- **分组:** `part_whole`
- **中文别名:** 分割错误
- **English aliases:** fallacy of division
- **定义:** 因为整体具有某性质，就推断每个组成部分也具有该性质。
- **诊断问题:** 整体性质是否必然分配到每个成员？
- **防误报:** 有些整体性质确实由每个成员共享，但需要额外前提。

## 22. 设计谬误（Design Fallacy）

- **ID:** `design_fallacy`
- **分组:** `rhetoric`
- **中文别名:** 美观谬误、视觉权威谬误
- **English aliases:** design fallacy, aesthetic credibility fallacy
- **定义:** 因为信息、图表或论证呈现得专业、美观、精致，就赋予其额外真实性或可信度。
- **诊断问题:** 视觉设计是否被误当成了数据质量、方法或逻辑正确性的证据？
- **防误报:** 良好设计可提高可读性，但不能替代来源、方法和推理验证。

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

## 45. 相关即因果（Correlation-Causation Fallacy）

- **ID:** `correlation_causation`
- **分组:** `causality`
- **中文别名:** 相关不等于因果、同时发生即因果
- **English aliases:** cum hoc ergo propter hoc, correlation implies causation
- **定义:** 仅因两个变量相关或共同变化，就断言其中一个导致另一个。
- **诊断问题:** 是否排除了反向因果、共同原因、选择偏差和巧合？
- **防误报:** 相关性可以是因果推断的一部分；需要额外设计、机制或控制。

## 46. 否定前件（Denying the Antecedent）

- **ID:** `denying_the_antecedent`
- **分组:** `formal`
- **中文别名:** 否定条件前件
- **English aliases:** denying the antecedent
- **定义:** 从‘如果 P 则 Q’和‘非 P’推出‘非 Q’，忽略 Q 可能由其他路径成立。
- **诊断问题:** P 是 Q 的必要条件，还是仅仅充分条件？
- **防误报:** 若已知 P 当且仅当 Q 或 P 是必要条件，结论才可成立。

## 47. 忽视主因（Ignoring a Common Cause）

- **ID:** `ignoring_common_cause`
- **分组:** `causality`
- **中文别名:** 忽略共同原因、混淆共同原因
- **English aliases:** ignoring a common cause, confounding
- **定义:** 看到 A 与 B 同时变化就认为 A 导致 B，却忽略可能同时导致二者的第三变量 C。
- **诊断问题:** 是否存在一个共同原因能够同时解释 A 与 B？
- **防误报:** 指出潜在混杂并不能自动推翻因果关系；应比较解释和控制证据。

## 48. 前后即因果（Post Hoc Ergo Propter Hoc）

- **ID:** `post_hoc`
- **分组:** `causality`
- **中文别名:** 在此之后因此由于此、先后即因果
- **English aliases:** post hoc ergo propter hoc, post hoc
- **定义:** 因为 B 在 A 之后发生，就断言 A 导致 B。
- **诊断问题:** 除了时间先后，还有什么证据把 A 与 B 的因果机制连接起来？
- **防误报:** 时间先后是因果的必要线索之一，但单独不足。

## 49. 积非成是（Two Wrongs Make a Right）

- **ID:** `two_wrongs_make_a_right`
- **分组:** `relevance`
- **中文别名:** 以错纠错、两个错误变正确
- **English aliases:** two wrongs make a right
- **定义:** 因为别人也做错了或先做错了，就把自己的错误行为说成正当。
- **诊断问题:** 他人的错误为什么能改变当前行为本身的正当性？
- **防误报:** 报复、对等和执法有时存在规范基础，但需要独立原则，而非‘别人也错’本身。

## 50. 人身攻击（Ad Hominem）

- **ID:** `ad_hominem`
- **分组:** `relevance`
- **中文别名:** 诉诸人身
- **English aliases:** ad hominem
- **定义:** 用对人的人格、身份、缺点或侮辱来替代对其论点内容的回应。
- **诊断问题:** 个人特征是否被当作其主张为假的理由？
- **防误报:** 可信度相关事实有时可以合法影响证言权重；应说明与主张的具体关系。

## 51. 举证责任（Burden of Proof）

- **ID:** `burden_of_proof`
- **分组:** `dialogue`
- **中文别名:** 倒置举证责任、转移举证责任
- **English aliases:** burden of proof, shifting the burden of proof
- **定义:** 提出主张的一方拒绝给出应有证据，却要求他人先证明其错误。
- **诊断问题:** 谁提出了需要支持的实质性主张？举证责任是否被无理由转嫁？
- **防误报:** 在既有制度或默认规则中举证责任可以预先分配；需考虑语境。

## 52. 身份主观（Circumstantial Ad Hominem）

- **ID:** `circumstantial_ad_hominem`
- **分组:** `relevance`
- **中文别名:** 处境人身攻击、动机谬误
- **English aliases:** circumstantial ad hominem
- **定义:** 仅因说话者具有利益、身份、隶属或动机，就直接判定其主张错误。
- **诊断问题:** 利益冲突是否仅影响可信度，还是被错误地当成了主张为假的证明？
- **防误报:** 利益冲突确实是评估证言可靠性的相关信息，但不能单独决定事实真值。

## 53. 基因谬误（Genetic Fallacy）

- **ID:** `genetic_fallacy`
- **分组:** `relevance`
- **中文别名:** 来源谬误、起源谬误
- **English aliases:** genetic fallacy
- **定义:** 根据一个观点、信息或事物的来源来判定其内容真伪或价值，而不评估其本身。
- **诊断问题:** 来源信息是否与待评估内容之间存在实际可靠性关系？
- **防误报:** 来源可靠性可影响先验可信度，尤其在无法直接核查时；但不等于内容必真或必假。

## 54. 罪恶关联（Guilt by Association）

- **ID:** `guilt_by_association`
- **分组:** `relevance`
- **中文别名:** 关联定罪、连坐谬误
- **English aliases:** guilt by association
- **定义:** 因为某观点与令人反感的人或群体有关联，就据此否定观点本身。
- **诊断问题:** 关联对象的坏名声为什么能证明该命题错误？
- **防误报:** 真正的组织关系、共同决策或共享证据可能相关，但必须具体说明。

## 55. 稻草人谬误（Straw Man）

- **ID:** `straw_man`
- **分组:** `dialogue`
- **中文别名:** 稻草人
- **English aliases:** straw man, strawman
- **定义:** 歪曲、夸大、弱化或替换对方真实论点，再攻击这个更容易反驳的版本。
- **诊断问题:** 被反驳的版本是否准确代表了对方实际主张？
- **防误报:** 若原话上下文缺失，应降低置信度并避免凭印象指控稻草人。

## 56. 错误归因（False Cause）

- **ID:** `false_cause`
- **分组:** `causality`
- **中文别名:** 虚假因果、错误因果
- **English aliases:** false cause
- **定义:** 在因果证据不足时把一个事件或变量归因为另一个；是比‘相关即因果’和‘前后即因果’更宽的上位诊断。
- **诊断问题:** 因果结论依赖了哪些证据？是否排除了主要替代解释？
- **防误报:** 优先使用更具体的因果谬误标签；只有无法更窄分类时使用本项。

## 57. 诉诸感情（Appeal to Emotion）

- **ID:** `appeal_to_emotion`
- **分组:** `emotion`
- **中文别名:** 诉诸情感、情绪诉诸
- **English aliases:** appeal to emotion
- **定义:** 用情绪反应替代建立结论所需的相关理由或证据。
- **诊断问题:** 情绪是在补充相关价值信息，还是承担了本应由证据承担的证明工作？
- **防误报:** 情绪在价值判断中可能相关；本项是上位标签，能用恐惧/同情等更窄项时优先用更窄项。

## 58. 谬误谬误（Fallacy Fallacy）

- **ID:** `fallacy_fallacy`
- **分组:** `meta`
- **中文别名:** 以谬误否定结论
- **English aliases:** fallacy fallacy, argument from fallacy
- **定义:** 因为支持某结论的一个论证包含谬误，就进一步断言该结论本身必然为假。
- **诊断问题:** 你否定的是这条推理，还是在没有独立证据时把结论也判成了假？
- **防误报:** 发现谬误只能说明该论证未能建立结论；结论仍可能由其他证据支持。

## 59. 诉诸虚伪（Tu Quoque）

- **ID:** `tu_quoque`
- **分组:** `dialogue`
- **中文别名:** 你也一样、诉诸伪善
- **English aliases:** tu quoque, appeal to hypocrisy
- **定义:** 用‘你也这么做/你也不一致’来回避对当前主张、批评或原则的实质回应。
- **诊断问题:** 指出对方不一致是否真正反驳了其主张？
- **防误报:** 伪善信息有时与执行可信度或动机相关，但通常不决定主张真假。

## 60. 片面谬误（Special Pleading）

- **ID:** `special_pleading`
- **分组:** `standards`
- **中文别名:** 特殊辩护、双重标准
- **English aliases:** special pleading
- **定义:** 在没有相关理由的情况下，为自己偏好的案例设立例外或改变评价标准。
- **诊断问题:** 为什么同一规则适用于别人却不适用于这个案例？例外有独立依据吗？
- **防误报:** 合理例外并非谬误；关键是例外条件是否与原则相关且一致适用。

## 61. 诱导性问题（Loaded Question）

- **ID:** `loaded_question`
- **分组:** `dialogue`
- **中文别名:** 复杂问句、预设性问题
- **English aliases:** loaded question, complex question
- **定义:** 问题中夹带未经同意的重要预设，使直接回答看起来等同于接受该预设。
- **诊断问题:** 无论回答‘是/否’，是否都会被迫承认一个尚未证明的前提？
- **防误报:** 问题可以合法包含已共同确认的背景；争议在于预设是否未经建立。

## 62. 语义模糊（Ambiguity）

- **ID:** `ambiguity`
- **分组:** `language`
- **中文别名:** 歧义谬误、偷换词义
- **English aliases:** ambiguity, equivocation
- **定义:** 利用词语、句法或概念的多义性在论证过程中悄然改变含义，从而制造结论。
- **诊断问题:** 关键术语在不同前提或结论中是否保持相同含义？
- **防误报:** 自然语言本就可能模糊；只有歧义承担了推理工作时才是谬误。

## 63. 诉诸权威（Appeal to Authority）

- **ID:** `appeal_to_authority`
- **分组:** `authority`
- **中文别名:** 权威诉诸
- **English aliases:** appeal to authority, argument from authority
- **定义:** 把权威身份本身当作结论成立的决定性理由，而没有足够考虑证据、领域匹配或专家分歧。
- **诊断问题:** 权威意见是可检验证据链的一部分，还是被要求无条件服从？
- **防误报:** 合理依赖专家是现代知识分工的必要部分；只有不恰当的权威替代证据才应标为谬误。

## 64. 没有真正的苏格兰人（No True Scotsman）

- **ID:** `no_true_scotsman`
- **分组:** `definition`
- **中文别名:** 真正的苏格兰人谬误、诉诸纯洁性
- **English aliases:** no true scotsman, appeal to purity
- **定义:** 面对反例时临时收紧群体定义，把反例排除为‘不是真正的 X’，以保护普遍性主张。
- **诊断问题:** 定义是在事前明确，还是在反例出现后为了免疫主张而改变？
- **防误报:** 有些术语本就有规范性定义；若边界标准事前独立成立，则未必是谬误。

## 65. 德克萨斯神枪手（Texas Sharpshooter）

- **ID:** `texas_sharpshooter`
- **分组:** `evidence_selection`
- **中文别名:** 神枪手谬误、事后画靶
- **English aliases:** texas sharpshooter fallacy, texas sharpshooter
- **定义:** 先观察大量数据，再挑出碰巧形成的聚类/模式并把它描述为事先预测，从而忽略选择效应和多重比较。
- **诊断问题:** 模式是事前定义并独立验证，还是看完数据后才画靶？
- **防误报:** 探索性分析可以发现模式，但需要独立数据、预注册或多重比较校正来验证。
