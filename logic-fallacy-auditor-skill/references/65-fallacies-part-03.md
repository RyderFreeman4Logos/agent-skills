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
