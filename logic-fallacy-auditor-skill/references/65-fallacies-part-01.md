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

## 11. 诉诸后果（Appeal to Consequences of a Belief）

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
