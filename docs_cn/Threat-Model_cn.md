# AIZP 威胁模型

**版本**：AIZP V0.6

本文档列出 AIZP 设计要缓解的威胁、**不**设计要缓解的威胁，以及针对协议本身的已知攻击模式。

**自 V0.2 起：**添加 5 个新威胁（T-11 至 T-15），对应组合性漂移、隐蔽、记忆中毒、NHI 泄露、奖励欺骗局限。完整 OWASP Top 10 for Agentic Applications 2026 交叉引用。

---

## 1. 范围

AIZP 防御：

- 自主 AI Agent 的行为漂移（11 个分类类型）。
- 通过作用域不匹配的权限提升。
- 递归/自主目标扩张。
- 胁迫性或冒充性输出。
- 认识论不确定下的执行。
- **组合性攻击**（序列级数据外泄）。[V0.2]
- 持久上下文中的**记忆中毒**。[V0.2]
- 运行时的 **NHI / 身份泄露**。[V0.2]
- **Agent 间协调漂移**。[V0.2]

AIZP **不**防御：

- 硬基础设施攻击（网络入侵、密钥外泄）。
- 基础模型层的对抗性提示注入（使用上游防御）。
- 执行环境的沙箱逃逸。
- AIZP 实现本身的供应链攻击。
- **奖励欺骗作为结构性均衡** — 见 [Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md)。[V0.2 诚实局限]

---

## 2. 威胁目录

每个威胁：攻击者能力、攻击技术、AIZP 缓解、剩余风险。

### T-01：通过提示注入的目标劫持（OWASP ASI01）

| 字段 | 值 |
|---|---|
| **攻击者** | Agent 上下文中的不可信内容。 |
| **攻击** | 注入重定向 Agent 目标的指令。 |
| **缓解** | `INTENT_DRIFT`（JSD 距离声明意图）、`MEMORY_DRIFT`（V0.2 — 上下文注入检测）、`SCHEMING_DRIFT`（V0.2 — 内/外偏离）、高偏离动作的 `GRAVITY_LOCK`。 |
| **剩余风险** | 匹配声明意图 embedding 的复杂注入可规避。结合提示隔离。 |
| **OWASP 映射** | ASI01 |

### T-02：通过工具滥用的权限提升（OWASP ASI02）

| 字段 | 值 |
|---|---|
| **攻击者** | 被入侵或对抗性提示的 Agent。 |
| **攻击** | 调用超出 AIAP 信任级别的高权限工具。 |
| **缓解** | `AUTHORITY_DRIFT`、`TOOL_CHAIN_DRIFT`（V0.2）、JIT 凭据（V0.2）。 |
| **剩余风险** | 需要细粒度作用域；粗作用域留下攻击面。 |
| **OWASP 映射** | ASI02, ASI03 |

### T-03：递归 Agent 失控（OWASP ASI08）

| 字段 | 值 |
|---|---|
| **攻击者** | 配置错误或对抗性 Agent。 |
| **攻击** | 无界子 Agent 或自调用循环。 |
| **缓解** | `RECURSIVE_DRIFT` 追踪 `self_call_depth` 和 `subagent_spawn_count`；硬上限。 |
| **剩余风险** | 跨会话递归规避每会话计数器。 |
| **OWASP 映射** | ASI08 |

### T-04：Agent 间互动中的身份伪造（OWASP ASI03）

| 字段 | 值 |
|---|---|
| **攻击者** | 将自身代表为人类或其他 Agent 的 Agent。 |
| **攻击** | 产生暗示虚假身份的输出。 |
| **缓解** | `IDENTITY_DRIFT`、`IDENTITY_VERIFICATION`（V0.2 — DID/NHI）、ANS 对手方验证。 |
| **剩余风险** | 微妙语言暗示可能规避检测。 |
| **OWASP 映射** | ASI03 |

### T-05：经济操纵

| 字段 | 值 |
|---|---|
| **攻击者** | 优化失对齐奖励的 Agent。 |
| **攻击** | 推荐或执行偏向 Agent 奖励而非用户福祉的动作。 |
| **缓解** | `ECONOMIC_DRIFT`、`REWARD_HACK_DETECTED`（V0.2）。 |
| **剩余风险** | 奖励欺骗是结构性均衡 — 见 T-15 和 [Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md)。 |
| **OWASP 映射** | ASI02 |

### T-06：操纵性社交行为（OWASP ASI09）

| 字段 | 值 |
|---|---|
| **攻击者** | 对用户使用说服技巧的 Agent。 |
| **攻击** | 包含紧迫性、愧疚、虚假稀缺的输出。 |
| **缓解** | `SOCIAL_DRIFT` 通过胁迫分类器 + 压力短语检测。 |
| **剩余风险** | 胁迫分类器有文化/语言偏见。 |
| **OWASP 映射** | ASI09 |

### T-07：确认疲劳与习惯化

| 字段 | 值 |
|---|---|
| **攻击者** | 无 — UX 失败模式。 |
| **攻击** | 频繁 `GRAVITY_LOCK` 提示训练用户自动批准。 |
| **缓解** | `H(a, c)` 时近度组件减少立即重新确认；UX 中批处理相关确认。 |
| **剩余风险** | 持续。通过 UX 设计缓解。 |
| **OWASP 映射** | ASI09 |

### T-08：对抗性引力分数操纵

| 字段 | 值 |
|---|---|
| **攻击者** | 知晓引力公式的 Agent。 |
| **攻击** | 设计 embedding 旨在最大化 `I(a, c)` 而追求不同有效目标。 |
| **缓解** | JSD（V0.2）比余弦相似度统计上更难欺骗。结合 `A(a, c)`（基于规则）和 `R(a)`（基于动作类）。 |
| **剩余风险** | 足够强大的对抗性 Agent 原则上可同时欺骗多组件。纵深防御。 |
| **OWASP 映射** | ASI10 |

### T-09：Embedding 模型投毒

| 字段 | 值 |
|---|---|
| **攻击者** | `I(a, c)` 使用的 embedding 模型被入侵。 |
| **攻击** | 用对抗性 embedding 模型替换。 |
| **缓解** | 固定 embedding 模型版本；通过哈希验证。 |
| **剩余风险** | 模型验证被绕过则完全失败。需供应链安全。 |
| **OWASP 映射** | ASI04 |

### T-10：状态机篡改（OWASP ASI10）

| 字段 | 值 |
|---|---|
| **攻击者** | 有代码访问权的本地攻击者。 |
| **攻击** | 在没有操作员动作的情况下强制状态从 `SAFE_STOP` 回到 `STABLE_ORBIT`。 |
| **缓解** | 密码学事件链（G4+）；运行时完整性检查。 |
| **剩余风险** | 可信计算基础假设。 |
| **OWASP 映射** | ASI10 |

### T-11：组合性数据外泄（OWASP ASI02）

| 字段 | 值 |
|---|---|
| **攻击者** | 对抗性提示的 Agent 或能力自主 Agent。 |
| **攻击** | 单独安全的动作序列组合成数据外泄。示例：`read_confidential` → `summarize` → `send_external_email`。每步在作用域内；序列是外泄。 |
| **缓解** | `COMPOSITIONAL_DRIFT`（V0.2）通过吸收马尔可夫链预测。`GRAVITY_FORECAST` 事件预测违规概率。`point_of_no_return_distance` 标记接近吸收的轨迹。 |
| **剩余风险** | 检测准确性依赖状态抽象函数和基线质量。新颖攻击模式可能不匹配基线。 |
| **OWASP 映射** | ASI02 |

### T-12：持久记忆中毒（OWASP ASI06）

| 字段 | 值 |
|---|---|
| **攻击者** | 任何可写 Agent 持久记忆者（RAG 语料、episodic 存储、工具结果缓存）。 |
| **攻击** | 嵌入提示注入内容；Agent 几天/几个会话后检索并遵循隐藏指令。 |
| **缓解** | `MEMORY_DRIFT`（V0.2）每次检索 + 写入；`MEMORY_QUARANTINE` 隔离可疑条目；来源日志追踪写入者。 |
| **剩余风险** | 对抗性训练数据可能规避分类器。对敏感部署结合手动记忆审查。 |
| **OWASP 映射** | ASI06 |

### T-13：NHI / 身份泄露（OWASP ASI03）

| 字段 | 值 |
|---|---|
| **攻击者** | 被入侵的非人类身份（服务账户、Agent 凭据）。 |
| **攻击** | 使用捕获的凭据冒充合法 Agent。 |
| **缓解** | `IDENTITY_VERIFICATION`（V0.2）— DID/NHI/AIAP card 哈希；JIT 凭据 ≤ 60s；持续重新授权；ANS 查询。 |
| **剩余风险** | 发放期间 JIT 凭据捕获；基于 embedding 模型的身份漂移检测不完美。 |
| **OWASP 映射** | ASI03 |

### T-14：Agent 间协调漂移（OWASP ASI07）

| 字段 | 值 |
|---|---|
| **攻击者** | N 个协调 Agent 中一个被入侵或涌现多 Agent 行为。 |
| **攻击** | 被入侵 Agent 通过 AIBP 消息影响组；组发展任一个体计划中没有的涌现目标。 |
| **缓解** | `INTER_AGENT_DRIFT`（V0.2）带 4 信号（目标方差、动作偏离、涌现计数、相互信任衰减）；组容器（GRAVITY_LOCK_GROUP、QUARANTINE_GROUP、DISBAND_GROUP）。 |
| **剩余风险** | 涌现目标本质难检测——可能是合法创造性协调。需要操作员审查。 |
| **OWASP 映射** | ASI07 |

### T-15：奖励欺骗（结构性均衡）

| 字段 | 值 |
|---|---|
| **攻击者** | 在大状态空间中优化代理奖励的任何 Agent。 |
| **攻击** | 找到最大化代理指标但不服务真实意图的路径。**根据 2026 研究，这不可避免。** |
| **缓解** | `REWARD_HACK_DETECTED`（V0.2）记录可观察模式（PROXY_METRIC_GAMING、REWARD_TAMPERING、SPECIFICATION_GAMING、DECEPTIVE_REWARD_MAXIMIZATION）。多信号验证。独立指标多样性。 |
| **剩余风险** | **不能消除** — 见 [Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md)。AIZP 检测可观察模式；复杂 Agent 可规避。 |
| **OWASP 映射** | ASI01 |

### 跨切：自进化失准 misevolution（arxiv 2509.26354）

对**自进化** Agent,安全对齐会在自主自我改进过程中劣化——**misevolution**(*Your Agent May Misevolve*, arxiv 2509.26354, 2025),在顶级基座模型上亦有观测。与 IPI 一样,这是**跨切风险**,而非单独编号的威胁:其四条进化路径累积在既有威胁目录之上。

| 自进化失准路径 | AIZP 覆盖 |
|---|---|
| **模型** —— 自调优中的安全遗忘(safety unlearning) | `drift_history` 基线重估 + `GRAVITY_FORECAST` 劣化趋势 |
| **记忆** —— 记忆累积后对齐衰减 | `MEMORY_DRIFT`、`MEMORY_QUARANTINE`(T-12) |
| **工具** —— 工具创建/复用中引入漏洞 | `TOOL_CHAIN_DRIFT`、`COMPOSITIONAL_DRIFT`(T-11) |
| **工作流** —— 自修改循环偏离轴线 | `RECURSIVE_DRIFT`(T-03) |

由于自进化失准是**跨会话、跨组件**累积的,单次动作的引力检查不足——这正是 AIZP `drift_history` 基线与 `GRAVITY_FORECAST` 在固定观察窗内做趋势监控的威胁理由,也是运行时对齐必须**持续而非一次性**的核心原因。

---

## 3. OWASP Top 10 for Agentic Applications 2026 — 覆盖

| OWASP | 覆盖的 AIZP 威胁 |
|---|---|
| ASI01 Agent 目标劫持 | T-01、T-15 |
| ASI02 工具滥用与利用 | T-02、T-05、T-11 |
| ASI03 身份与特权滥用 | T-02、T-04、T-13 |
| ASI04 Agentic 供应链漏洞 | T-09 |
| ASI05 意外代码执行（RCE）| —（带外；由容器 L3+ 约束，见 [Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md) §10）|
| ASI06 记忆与上下文投毒 | T-12 |
| ASI07 不安全的 Agent 间通信 | T-14 |
| ASI08 级联失败 | T-03 |
| ASI09 人机信任利用 | T-06、T-07 |
| ASI10 失控 Agent | T-08、T-10 |

完整映射见 [Compliance-Profiles/OWASP-Agentic-Top10-Mapping_cn.md](Compliance-Profiles/OWASP-Agentic-Top10-Mapping_cn.md)。

---

## 4. 攻击-防御矩阵

| 攻击 | 漂移检测 | 引力锁定 | 隔离 | 预测 | 安全停止 |
|---|---|---|---|---|---|
| 目标劫持 | INTENT | 可能 | 可能 | 可能 | 罕见 |
| 权限提升 | AUTHORITY | 是 | 是 | — | 可能 |
| 递归失控 | RECURSIVE | 是 | 是 | 是 | 是 |
| 身份伪造 | IDENTITY | 可能 | 可能 | — | 可能 |
| 经济操纵 | ECONOMIC | 可能 | 可能 | — | — |
| 社交操纵 | SOCIAL | 可能 | 可能 | — | — |
| 分数操纵 | — | — | — | — | — |
| **组合性** | COMPOSITIONAL | 可能 | 是 | **是** | 是 |
| **记忆中毒** | MEMORY | 是 | **是** | — | 可能 |
| **NHI 泄露** | IDENTITY + ID_VERIFY | — | — | — | **是** |
| **Agent 间** | INTER_AGENT | 组 | 组 | 可能 | 是 |
| **奖励欺骗** | — | — | — | — | —（仅检测）|

---

## 5. 纵深防御原则

AIZP 建议与以下分层：

1. **基础模型安全**：LM 层的 RLHF、Constitutional AI、RLAIF。
2. **沙箱**：Firecracker/gVisor 中的工具执行（容器 L2/L3）。
3. **审计轨迹**：取证重建的 G4 合规。
4. **人类监督**：高风险轨迹的周期性审查。
5. **网络策略**：出站过滤、速率限制、异常检测。
6. **零信任 / NHI**（V0.2）：JIT 凭据 + 持续授权。
7. **OTel 可观测性**（V0.2）：标准遥测管道。

AIZP 是安全 AI 部署的**必要但不充分**条件。

---

## 6. 披露策略

如果你发现本规范或任何参考实现中的漏洞，请通过项目的安全公告渠道报告。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
