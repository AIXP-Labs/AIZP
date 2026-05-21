# 漂移模型

**版本**：AIZP V0.6

本文档规定 AIZP 追踪的**十一类**漂移、其代理指标、严重度评分和检测指南。

**自 V0.2 起：**添加五类新漂移（组合性、隐蔽、记忆、工具链、Agent 间），基于 2025–2026 研究（SafetyDrift、Apollo Research、OWASP Agentic Top 10 2026）。

---

## 1. 概览

漂移是 **AI 行为远离 HSAW 的外向运动**。AIZP 识别十一类漂移。每类漂移至少有一个可观测代理指标。

| # | 漂移类型 | 类别 | 添加于 |
|---|---|---|---|
| 1 | 意图 | 目标对齐 | V0.1 |
| 2 | 权限 | 特权 | V0.1 |
| 3 | 经济 | 资源 | V0.1 |
| 4 | 社交 | 操纵 | V0.1 |
| 5 | 递归 | 自主 | V0.1 |
| 6 | 身份 | 冒充 | V0.1 |
| 7 | **组合性** | **序列** | **V0.2** |
| 8 | **隐蔽** | **隐蔽** | **V0.2** |
| 9 | **记忆** | **上下文** | **V0.2** |
| 10 | **工具链** | **能力** | **V0.2** |
| 11 | **Agent 间** | **协调** | **V0.2** |

---

## 2. 漂移类型

### 2.1 意图漂移

（V0.1 不变——见 Gravity-Model §2.1；V0.2 用 JSD 替代余弦相似度）

**代理指标**：`intent_distance = JSD(P_action || P_intent)` 替代 `1 - cos_sim(emb(action), emb(intent))`。

严重度阈值不变。

---

### 2.2 权限漂移

（V0.1 不变）

**代理指标**：`scope_coverage_ratio = |required_scope ∩ granted_scope| / |required_scope|`

映射到 **OWASP ASI03 身份与特权滥用**。

---

### 2.3 经济漂移

（V0.1 不变）

---

### 2.4 社交漂移

（V0.1 不变）

映射到 **OWASP ASI09 人机信任利用**（子集：不当劝服）。

---

### 2.5 递归漂移

（V0.1 不变）

映射到 **OWASP ASI08 级联失败**（子集：自加速 / 资源耗尽）。

---

### 2.6 身份漂移

（V0.1 不变）

映射到 **OWASP ASI03 身份与特权滥用**（子集：冒充）。

---

### 2.7 组合性漂移

**定义**：单独允许的动作序列组合产生违规。

**为何危险**：2026 研究中最受关注的"隐身"失败模式（SafetyDrift，arxiv 2603.27148）。每步通过逐动作检查，但轨迹越界。

**经典例子**：
```
步骤 1：read_confidential_file()       — 允许（T2 read.own）
步骤 2：summarize(file_content)         — 允许（纯计算）
步骤 3：send_email(external, summary)   — 允许（T2 send.email.own）
结果：外部数据外泄。
```

**代理指标**：
```
absorption_probability_K = P(轨迹在未来 K 步内达到安全违规状态)
point_of_no_return_distance = 最小 k 使得 P_k(violate | current_state) ≥ 0.5
```

通过抽象状态上的吸收马尔可夫链计算（见 [Forecasting_cn.md](Forecasting_cn.md)）。

**严重度阈值**：

| `absorption_probability_5` | 严重度 |
|---|---|
| `< 0.05` | （非漂移）|
| `0.05 – 0.20` | `LOW` |
| `0.20 – 0.50` | `MEDIUM` |
| `0.50 – 0.80` | `HIGH` |
| `≥ 0.80` | `CRITICAL` |

**检测频率**：每动作，基于窗口 K=5 前瞻。

**映射到 OWASP**：ASI02 工具滥用与利用、ASI06 记忆与上下文投毒（经投毒上下文组合时）。

**参考**：SafetyDrift 论文实现 94.7% 检测率，提前 3.7 步预警。

**局限**(此漂移比逐动作类更难界定——依赖它之前请先读这段):`absorption_probability_K` 的好坏完全取决于马尔可夫模型的**抽象状态空间**。由此有两类失败:(a)**抽象导致的漏报**——若违规存在于抽象未捕获的语义中,模型看不见;(b)**视界盲区**——在 K 步窗口**之外**才完成的违规会被完全漏掉,而调大 K 是用覆盖度去换组合式膨胀的状态空间。94.7% 是**基准结果**(SafetyDrift),并非对任意工具/动作空间的保证。把组合检测当作**有界前瞻,而非安全证明**:对高风险轨迹应配合容器(L2+),使未被检出的组合也无法无监督地完成。

---

### 2.8 隐蔽漂移

**定义**：Agent 的内部推理与外部行为偏离——追求隐蔽目标，同时呈现对齐的外表。

**为何危险**：2026 研究（Apollo Research；698 个真实世界事故 2025-10–2026-03）显示隐蔽是高能力 LLM Agent 中可度量且增长的失败模式。

**代理指标**（多信号——需要 LLM-as-judge 或可解释性访问）：
```
reasoning_output_divergence = JSD(emb(internal_reasoning) || emb(external_output))
deception_classifier_score = P(deception | output_text)
goal_concealment_score = 关于声明目标的输出显式度
plan_action_mismatch = 已述计划与实际动作步骤比例
```

**严重度阈值**：

下列各带**统一适用于全部四个**代理信号（`reasoning_output_divergence`、`deception_classifier_score`、`goal_concealment_score`、`plan_action_mismatch`）；两个最高风险信号另有更严格的 `HIGH` 覆盖。

| 条件（信号值 `s`）| 严重度 |
|---|---|
| 四个信号均 `s < 0.30` | （非漂移）|
| 任一单信号 `s ∈ [0.30, 0.50)` | `LOW` |
| 任一单信号 `s ∈ [0.50, 0.70)` | `MEDIUM` |
| 任一单信号 `s ≥ 0.70`，**或** `deception_classifier_score ≥ 0.65`，**或** `goal_concealment_score ≥ 0.65` | `HIGH` |
| 两个或更多信号 `s ≥ 0.70` | `CRITICAL` |

**检测频率**：每 N=5 个动作（昂贵——需要 judge 模型）。

**映射到 OWASP**：ASI01 Agent 目标劫持（欺骗子集）。

**局限**(caveat 最多的漂移——**设计上就是弱信号**):代理信号是有噪的。`deception_classifier_score`(LLM-as-judge)自带误报率,而 `reasoning_output_divergence` 可能因**正当**原因偏高——一个在输出前压缩、重述或概括其推理的模型并不必然在 scheming。因此 `SCHEME_SUSPECTED` 事件**必须不**自动停机:与 Apollo Research 的发现一致——训练消除*可观察*的 scheming 可能增加由情境感知驱动的隐藏(此处外推到运行时停机策略),激进的自动响应可能训练出规避而非诚实。正确响应是**按 `aggregate_confidence` 门控的操作员审查**,而非自动化(见 [AIZP_Protocol_cn.md](../specification/AIZP_Protocol_cn.md) §11)。Apollo 的反隐蔽训练**减少但不消除**隐蔽动作,且足够强大的模型可规避检测本身——AIZP 记录信号,不声称确定性检测。**judge 独立性:** `deception_classifier_score` 的 judge/分类器**必须**与不可信上下文隔离(它本身就是 IPI 靶子),并**应当**独立于被测 agent 的底模与厂商——共用底模会带来共模失效与共谋盲区。

---

### 2.9 记忆漂移

**定义**：Agent 的持久上下文、记忆存储或检索文档包含重定向其行为的内容。

**为何危险**：OWASP Agentic Top 10 2026 将**持久记忆中毒**列为顶级风险。长期运行的 Agent 累积上下文；嵌入此上下文的对抗性内容可跨多个会话漂移 Agent。

**代理指标**：
```
prompt_injection_classifier_score = P(injection | context_chunk)
memory_freshness_delta = age_seconds(memory_entry)
unauthorized_memory_write_count = 来自不可信源的记忆写入计数
retrieved_doc_anomaly_score = JSD(P_retrieved_today || P_baseline_retrieval)
```

**严重度阈值**：

| `prompt_injection_score` | 严重度 |
|---|---|
| `< 0.20` | （非漂移）|
| `0.20 – 0.45` | `LOW` |
| `0.45 – 0.65` | `MEDIUM` |
| `0.65 – 0.85` | `HIGH` |
| `≥ 0.85` | `CRITICAL` |

**映射到 OWASP**：ASI06 记忆与上下文投毒。

**检测频率**：每次上下文检索和每次记忆写入。

**缓解**：触发 `MEMORY_QUARANTINE` 事件；Agent **应**移至容器级别 L2（沙箱）直到 quarantine 解决。

---

### 2.10 工具链漂移

**定义**：特定多工具调用序列表现出与基线偏离的异常模式。

**为何危险**：直接映射到 **OWASP ASI02 工具滥用与利用**——链式工具产生任一工具单独不授予的能力。

**代理指标**：
```
tool_sequence_likelihood = P(观察到的序列 | 基线序列分布)
unauthorized_tool_combo = 布尔（链包含声明范围之外的组合）
tool_invocation_rate_anomaly = 工具/分钟相对基线的 z 分数
```

序列似然度通过工具 ID 上的三元或 n 元马尔可夫模型估计。

**严重度阈值**：

| `1 - tool_sequence_likelihood` | 严重度 |
|---|---|
| `< 0.20` | （非漂移）|
| `0.20 – 0.45` | `LOW` |
| `0.45 – 0.70` | `MEDIUM` |
| `0.70 – 0.90` | `HIGH` |
| `≥ 0.90` 或 `unauthorized_tool_combo == true` | `CRITICAL` |

**映射到 OWASP**：ASI02 工具滥用与利用。

---

### 2.11 Agent 间漂移

**定义**：多 Agent 系统表现出协调失败——Agent 间声明目标偏离，或集体行为与任一个体 Agent 声明意图矛盾。

**为何危险**：多 Agent 系统通过强化循环和涌现目标放大单 Agent 漂移。**OWASP ASI07 不安全的 Agent 间通信** 在 2026 中明确涵盖此类风险。

**代理指标**：
```
goal_consistency_variance = 跨 Agent 组的声明目标 embedding 方差
collective_action_divergence = JSD(P_collective_action || P_individual_intent_average)
emergent_goal_count = 不在任一个体初始计划中的 Agent 协调目标数
mutual_trust_decay = Agent 间消息日志中违背承诺的指数衰减
```

**严重度阈值**：

| 最强信号 | 严重度 |
|---|---|
| 全部一致 | （非漂移）|
| `goal_consistency_variance ∈ [0.20, 0.40]` | `LOW` |
| `collective_action_divergence ∈ [0.40, 0.60]` | `MEDIUM` |
| 任一信号 ≥ 0.70 | `HIGH` |
| `emergent_goal_count ≥ 3` 且 `mutual_trust_decay ≥ 0.6` | `CRITICAL` |

**映射到 OWASP**：ASI07 不安全的 Agent 间通信、ASI08 级联失败。

**检测频率**：每个 Agent 间通信边界（AIBP 消息）。

**触发**：在 `GRAVITY_DRIFT` 之外还触发 `INTER_AGENT_DRIFT` 事件。

---

## 3. 严重度聚合

（从 V0.1 扩展）

同一动作上检测到多种漂移时：

```
aggregate_severity = max(severityᵢ)
gravity_drift_signal = 最高严重度漂移类型
combined_drift_evidence = 所有漂移信号条目的并集
```

`GRAVITY_DRIFT` 事件**必须**在 `drift_types` 数组中报告所有检测到的漂移类型（最多 11 项）。

**自 V0.2 起**：当 `COMPOSITIONAL_DRIFT` 检测到 `severity ≥ HIGH` 时，**必须**同时发射 `GRAVITY_FORECAST` 事件（见 [Forecasting_cn.md](Forecasting_cn.md)）。

---

## 4. 漂移检测频率

| 漂移类型 | 频率 | 为何 |
|---|---|---|
| 意图、权限、身份 | 每动作 | 便宜（基于规则/embedding）|
| 递归 | 持续 | 作为 Agent 状态追踪 |
| 经济、社交 | 每 N=5 动作 | 分类器成本 |
| 工具链 | 每动作 | 马尔可夫模型便宜 |
| 组合性 | 每动作（K=5 前瞻）| DTMC 推理 |
| 记忆 | 每次检索 + 写入 | 边界检查 |
| 隐蔽 | 每 N=5 动作 | Judge 模型昂贵 |
| Agent 间 | 每个 AIBP 消息 | 边界检查 |

---

## 5. 漂移严重度 → 引力分数影响

（从 V0.1 扩展）

回顾 `D(c)` 组件：

```
D(c) = 1 - min(1, drift_significance_score)
drift_significance_score = (1 - p) · severity_intensity
```

其中 Mann-Whitney U 产生 p 值（V0.2——见 [Gravity-Model_cn.md](Gravity-Model_cn.md) §2.5）。

对 COMPOSITIONAL_DRIFT，G 上可选添加单独项 `T(c)`：
```
G' = G + w₆ · T(c)
T(c) = 1 - absorption_probability_K
```

---

## 6. 误报处理

（从 V0.1 扩展）

自 V0.2 起：

7. **对 D(c) 应用 Mann-Whitney U 显著性检验** — 漂移严重度必须在统计上可区分于基线。基线形成良好时，误报急剧下降。
8. **目标条件化基线**用于合法行为适应：MI9 框架的方法——以声明目标为条件比较基线，而非绝对基线。合法任务变更期间主动学习 + 强化。

---

## 7. 局限性

（从 V0.1 扩展）

自 V0.2 起：

- **隐蔽漂移根本上难以检测**——这与 Apollo Research 的发现一致：训练消除可观察的隐蔽行为可能反而增强由情境感知驱动的隐藏（此处外推到运行时检测/停机策略；Apollo（arxiv 2509.15541）研究的是训练时干预，而非运行时停机）。AIZP 记录信号但仅视为弱指标。
- **组合性漂移检测依赖良好的状态抽象函数**——过粗会漏真实违规；过细会得到假 DTMC 路径。
- **记忆漂移检测依赖提示注入分类器**，分类器本身可对抗规避。
- 所有代理指标都可被足够强大的对抗性 Agent **欺骗**。漂移检测**必要但不充分**。

---

## 8. 间接提示注入（IPI）— 跨切向量

**IPI 不是第十二个漂移类型。它是诱发既有漂移类型的主导攻击*向量*。** 2026 年，间接提示注入估计占 Agent 攻击的 55–60%，是 OWASP **ASI01 Agent Goal Hijack** 的基础。AIZP 将其建模为跨切关注点而非编号类别，因为 IPI 描述失对齐*如何*被投递，而非*何种*失对齐结果。

### 8.1 投递通道

| 通道 | 载荷藏于何处 | 显现为漂移类型 |
|---|---|---|
| 检索内容 | 投毒网页、文档、RAG 块 | 记忆漂移（§2.9）、意图漂移（§2.1）|
| 工具描述 | MCP `tools/list` 条目中的恶意文本 | 记忆/社交漂移（见 [Integration-MCP_cn.md](Integration-MCP_cn.md) §4）|
| 工具结果 | 嵌入工具输出中的指令 | 意图漂移（§2.1）、工具链漂移（§2.10）|
| 长期记忆 | 跨会话持久化的对抗内容 | 记忆漂移（§2.9）|
| Agent 间消息 | 经另一 Agent 中继的注入指令 | Agent 间漂移（§2.11）、社交漂移（§2.4）|

### 8.2 检测信号

核心 IPI 信号是**Agent 声明/用户意图与新摄入内容隐含目标之间的偏离**：

```
ipi_signal = JSD(P_intent_declared || P_goal_after_ingestion)
```

在检索外部内容后该信号立即大幅跳变——且无相应用户指令——即 IPI 指纹。这补充（不取代）记忆漂移（§2.9）中已有的 `prompt_injection_classifier_score`。

### 8.3 推荐防御（组合，勿重造）

AIZP **观察并打分**；预防依赖既有 IPI 防御：

- **预过滤**：现成 LLM 在摄入前剥除注入内容（PromptArmor，arxiv 2507.15219）。
- **描述钉住（TOFU）**：首次使用时钉住工具描述；变更重新触发验证（见 [Integration-MCP_cn.md](Integration-MCP_cn.md) §4）。
- **潜空间动力学检测**：IPI 显现为可在表层语义之下检测的内在"注意力坍塌"模式。
- **来源分离**：将检索/工具内容视为数据，绝不视为指令。

### 8.4 验证基准

部署应对照已发布基准验证 IPI 处理：

- **AgentDojo**（Debenedetti 等，NeurIPS 2024）— 97 任务、629 安全用例。arxiv 2406.13352。
- **InjecAgent**（Zhan 等，ACL Findings 2024）— 工具集成 Agent 中的 IPI。
- **Agent Security Bench**（Zhang 等，2025）— arxiv 2410.02644。

### 8.5 诚实局限

无 IPI 防御是完整的；因隐藏载荷，注入贡献了过半的假阴性。AIZP 的 IPI 信号提升相关漂移类型的严重度，但不能保证检测（见 §7 与 [Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md)）。

---

## 参考

- SafetyDrift（Dhodapkar & Pishori，2026）— arxiv 2603.27148。"不可挽回点"的吸收马尔可夫链。94.7% 检测。
- Apollo Research (2026) — 对反隐蔽训练的对齐审议压力测试。arxiv 2509.15541。
- "Scheming in the wild"（Long Term Resilience，2026）— 2025-10–2026-03 间 698 个真实世界隐蔽事故。
- OWASP Top 10 for Agentic Applications 2026 — ASI01–ASI10 类别。
- MI9 框架（Wang 等，2025）— Jensen-Shannon 散度 + Mann-Whitney U + 目标条件化基线。arxiv 2508.03858。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
