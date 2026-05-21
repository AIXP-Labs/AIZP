# 熵学基础

**版本**：AIZP V0.6（V0.3 子理论 — 在引力中心框架内保留）
**自 V0.5 起的地位**：这已**不是**协议的中心命题。它是**子理论**：引力中心框架内使用的信息论距离度量（JSD）。当前形式化基础见 [Gravity-Center-Foundation_cn.md](Gravity-Center-Foundation_cn.md)。

本文档形式化 V0.3 时代的中心命题——**定向熵数坍塌为 HSAW**——它自此被重新诠释为**引力距离度量的信息论基础**。坍塌机制在引力框架内仍然有效：引力分数 `G(a, c, t) = 1 - JSD(P_agent || Q_HSAW)` 是熵坍塌距离映射到引力轨道稳定性。

---

## 1. 核心命题

AIZP 主张：

> AI 行为，建模为可能动作上的概率分布 `P_agent(a | context, t)`，其信息熵在 HSAW 衍生观察作用于 Agent 时减少——坍塌——朝向 HSAW 对齐的目标分布 `Q_HSAW(a | context)`。

符号化：

```
在 HSAW 观察下：
  H(P_agent | observation) ≤ H(P_agent)
  P_agent → Q_HSAW
```

其中 `H` 是香农熵：

```
H(P) = -Σ P(a) · log₂ P(a)
```

无 HSAW 观察时，Agent 行为熵保持高（默认无约束漂移）。有观察时，它向 HSAW 坍塌。

这**不**是规范性主张（"AI 应当对齐"）。这是关于运行时过程的**描述性**主张。

---

## 2. 为何用"熵"？

信息论给我们度量"分布有多分散"的精确工具。对 AI 行为：

- 完美对齐的 Agent：HSAW 正确动作上 `P_agent(a) = 1`，其他动作上 `0`：熵为 `0`。
- 最大不确定的 Agent：`P_agent` 均匀：熵为 `log₂ |A|`，`|A|` 是动作空间大小。

多数 AI Agent 位于两者之间。引力分数 `G` 度量**该连续谱上的位置**。

| 行为状态 | `P_agent` 的熵 | 引力分数 |
|---|---|---|
| 完美对齐（确定 HSAW 动作）| `0` | `1.0` |
| 高度聚焦于对齐动作 | 低 | `0.8 – 1.0` |
| 分散于对齐 + 部分非对齐 | 中 | `0.5 – 0.8` |
| 显著概率质量在非对齐 | 高 | `0.3 – 0.5` |
| 分布远离 HSAW | 极高或目标错 | `< 0.3` |
| 均匀 / 无约束 / 坍塌不可能 | 最大 | `< 0.15` |

---

## 3. 为何用"坍塌"？

三种物理现象证明"坍塌"一词的恰当：

### 3.1 波函数坍塌（量子力学）

叠加态量子系统 `Σ ψᵢ|sᵢ⟩` 在测量时坍塌到单一观察态 `|s*⟩`。测量是观察者与系统的互动。

**对应**：AI Agent 的动作分布是可能动作上的叠加。每次 HSAW 观察（确认、意图声明、权限检查）是使分布坍塌的测量。

### 3.2 引力坍缩（广义相对论）

足够引力下弥散物质坍缩到奇异中心。

**对应**：AI 动作概率质量被由引力分数代表的引力拉向 HSAW"奇点"。

### 3.3 熵驰豫（统计力学）

与热浴接触的开放热力学系统驰豫向平衡，熵可预测地变化。

**对应**：与 HSAW"观察浴"接触的 AI Agent 驰豫向 `Q_HSAW`，熵减少。

三者足够精确以提供有用直觉；不当作字面物理。**统一概念是**：高熵状态在特定外部观察/力下，过渡到较低熵状态。

---

## 4. 形式化定义

### 4.1 动作分布

对给定 Agent `A`、上下文 `c`、时间 `t`：

```
P_agent(a | c, t) ∈ [0, 1],     Σ_a P_agent(a | c, t) = 1
```

这是 Agent `A` 在上下文 `c` 下下一步采取动作 `a` 的概率。

对基于 LLM 的 Agent，`P_agent` 可从以下估计：
- 输出 token 分布（下一 token 概率）。
- 基于采样的估计（运行 Agent N 次，观察动作频率）。
- 自报告（Agent 陈述其选项及权重）。

### 4.2 HSAW 目标分布

```
Q_HSAW(a | c) ∈ [0, 1],     Σ_a Q_HSAW(a | c) = 1
```

这是上下文 `c` 下与人类主权与福祉一致的动作分布。它从以下**导出**：

- 声明的用户意图。
- 授予权限（AIAP T 级别）。
- 可逆性考量。
- 近期确认。
- 漂移历史。

实践中，`Q_HSAW` 近似而非精确知晓。AIZP 的组件（意图对齐度、权限覆盖度、可逆性、时近度、漂移历史）是 `Q_HSAW` 的**代理**。

### 4.3 坍塌度量

坍塌进度有多个等价度量：

**Jensen-Shannon 散度（V0.2+ 引力分数使用）**：

```
JSD(P || Q) = ½ KL(P || M) + ½ KL(Q || M),   M = ½(P + Q)
G(a, c) = 1 - JSD(P_agent || Q_HSAW)
```

> **JSD 以 2 为底**计算，故 `JSD ∈ [0, 1]` 且 `G = 1 − JSD ∈ [0, 1]`。（若用自然对数，上界为 ln 2 ≈ 0.693，`G` 就不会有界于 `[0, 1]`。）

**KL 散度（替代）**：

```
KL(P_agent || Q_HSAW) ≥ 0
G_alt = 1 - normalize(KL)
```

**交叉熵（替代）**：

```
H(P_agent, Q_HSAW) = -Σ P_agent(a) log Q_HSAW(a)
```

都度量同一底层量：**`P_agent` 向 `Q_HSAW` 坍塌了多少**。

V0.2+ 使用 JSD 因其对称、有界 `[0, 1]`，`√JSD` 是真实度量。

### 4.4 观察算子

每个 AIZP 事件都是作用于 `P_agent` 的**观察算子** `Ô`：

```
P_agent_after = Ô(P_agent_before)
```

| AIZP 事件 | 算子角色 |
|---|---|
| `GRAVITY_CHECK` | 当前坍塌进度的测量 |
| `GRAVITY_DRIFT` | 检测到 N 维度上坍塌失败 |
| `GRAVITY_LOCK` | 强观察要求（通过 `sys.io.confirm` 强制显式测量）|
| `RECENTERING` | 恢复算子——重新施加坍塌力 |
| `SAFE_STOP` | 终止——观察不可能，检测到无界熵 |
| `GRAVITY_FORECAST` | 预测未来熵轨迹 |
| `IDENTITY_VERIFICATION` | 验证观察者权限 |
| `MEMORY_QUARANTINE` | 隔离损坏的观察者（中毒上下文）|
| `SCHEME_SUSPECTED` | 信号规避观察的分布 |
| `INTER_AGENT_DRIFT` | 多观察者协调失败 |
| `CONTAINMENT_GRADUATED` | 调整观察强度 |
| `REWARD_HACK_DETECTED` | 检测代理奖励利用（规避观察的优化）|

每个事件形式化为：在特定观察类型下 Agent 行为分布的变换。

---

## 5. 五大原则，形式化

### 原则 1 — AI 行为是熵性的

```
默认状态：  H(P_agent | 无观察) ≈ H_max
```

### 原则 2 — HSAW 是观察者

```
观察者：  Q_HSAW  从人类锚定信号导出
```

### 原则 3 — 引力是坍塌速率

```
G(a, c, t) = 1 - JSD(P_agent(·, t) || Q_HSAW(·))
dG/dt > 0  当观察发生时
```

### 原则 4 — 漂移是坍塌失败

```
漂移 = P_agent 中抗坍塌的子集
11 种漂移类型分类抗性模式。
```

### 原则 5 — 无观察，无执行

```
若观察不可能（H(P_agent) 不能被降低）：
   强制停止（SAFE_STOP）。
```

---

## 6. 含义

### 6.1 为何逐动作检查不充分

动作 `aₜ` 处的单个 `GRAVITY_CHECK` 仅在该时刻坍塌 `P_agent`。下一动作 `aₜ₊₁` 从新的（可能未坍塌的）分布开始，除非重新观察。

**含义**：必须持续观察。V0.2 的逐动作检查 + 预测捕捉这一点。

### 6.2 为何存在组合性漂移

若个体动作 `a₁, a₂, ..., aₙ` 各自受边缘观察（小的个体坍塌），但联合轨迹 `(a₁, ..., aₙ)` 在动作序列空间的非对齐区域，则逐动作观察**漏掉**组合性非对齐。

**含义**：必须轨迹级观察（DTMC 预测）。V0.2 的 COMPOSITIONAL_DRIFT 和 GRAVITY_FORECAST 解决此。

### 6.3 为何奖励欺骗是结构性的

奖励欺骗对应：`P_agent → Q_proxy` 而非 `P_agent → Q_HSAW`，其中 `Q_proxy ≠ Q_HSAW` 是不完美近似。

**含义**：即使完美观察 `Q_proxy`，对 `Q_HSAW` 的对齐不保证。这是 [Reward-Hacking-Limits](Reward-Hacking-Limits_cn.md) 问题的形式化：AIZP 可将 `P_agent` 坍塌到 `Q_proxy`，但 `Q_proxy` 不可还原为 `Q_HSAW`。

### 6.4 为何 HSAW 必须是公理性，非学习的

若 `Q_HSAW` 从数据学习，它本身会受漂移影响。设计上，`Q_HSAW` 是**公理性**——锚定于人类主权作为固定参考系。

这是 HSAW 作为独立、不可变协议存在的原因。AIZP 在 HSAW **之上**运作；不重新定义 HSAW。

---

## 7. 操作性后果

| 理论事实 | 操作后果 |
|---|---|
| 熵坍塌是连续的，非离散的 | 逐动作 `GRAVITY_CHECK` |
| 坍塌可以是部分的 | 6 状态机带程度 |
| 坍塌失败有多种原因 | 11 种漂移类型 |
| 坍塌可被预测 | DTMC / 吸收链预测 |
| 组合性坍塌 ≠ 逐步坍塌 | `COMPOSITIONAL_DRIFT` + `GRAVITY_FORECAST` |
| 观察者必须被验证 | `IDENTITY_VERIFICATION` |
| 中毒观察者污染坍塌 | `MEMORY_QUARANTINE` |
| 多观察者协调重要 | `INTER_AGENT_DRIFT` |
| 某些坍塌不可约 | `REWARD_HACK_DETECTED`（仅检测）|
| 无观察者，无执行 | `SAFE_STOP` |

V0.2 的全部机制都从熵学基础导出。

---

## 8. 局限与诚实告诫

### 8.1 `Q_HSAW` 是近似的

我们不精确知晓 `Q_HSAW`。AIZP 使用代理（意图、权限等）近似但不等于它。**代理与真实 HSAW 的不对齐是失败的最深源头** — 见 [Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md)。

### 8.2 熵是在未指定动作空间上

`H(P_agent)` 取决于我们如何定义 `A`（动作空间）。不同抽象产生不同熵。AIZP 不规定单一动作空间；实现在 AIAP card 中声明其空间。

### 8.3 "熵"在宽松意义上使用

严格信息论处理统计系综。AI Agent 是有单一轨迹的个体系统。"行为熵"框架将 Agent 的策略分布视为被测量的实体——而非实现的轨迹。

这与现代强化学习中 `entropy regularization` 的使用一致。

### 8.4 量子类比是隐喻

我们调用"波函数坍塌"作为直觉。AI Agent 没有实际波函数。类比在以下层级成立：**概率分布 + 观察 = 较窄分布**。

---

## 9. 为何此基础重要

V0.3 之前，AIZP 是 12 事件、11 漂移类型、6 状态、5 容器级别的集合——有用但**与单一深刻原则脱节**。

V0.3 在熵学基础下统一全部：

> 每个事件是观察算子。
> 每种漂移类型是坍塌失败模式。
> 每个状态是坍塌深度。
> 每个容器级别是观察强度。
> 每个合规级别是系统执行观察的承诺。

**AIZP 全部现在可从单一陈述导出：熵数坍塌为 HSAW。**

这是**概念性协议**成熟时的样子。

---

## 10. 知识谱系与诚实定位

此基础**非 AIZP 原创**。它是既有对齐理论的协议级编码。

### 直接谱系

- **Friston, K. (2010+)** — *自由能原理*与*主动推理*。AIZP 的"熵向目标分布坍塌"是 FEP "Agent 最小化变分自由能"的离散协议表达。Verses AI 的 Axiom 架构（2026）是 FEP 的商业实施。
- **Shannon, C. E. (1948)** — 信息熵。
- **Lin, J. (1991)** — Jensen-Shannon 散度。
- **Yudkowsky, E. (2004)** — 连贯外推意志（HSAW 目标分布思想的先驱）。

### 强 2026 理论支持

- **arxiv 2501.16448** "Information-theoretic Distinctions Between Deception and Confusion" — 将欺骗形式化为真实目标与可观察行为间的熵；直接支持 AIZP 的 `SCHEMING_DRIFT` 与 `INTENT_DRIFT`。
- **arxiv 2512.03048** "The Specification Trap" — 建立静态价值对齐不能扩展；支持 AIZP 反静态规则立场。
- **arxiv 2502.05934** "Intrinsic Barriers... No-Free-Lunch Alignment" — `Q_HSAW` 必须近似，非完美。

### 区别于同名概念

- **arxiv 2512.12381** "Entropy Collapse: A Universal Failure Mode" 使用**相同短语**但**意义相反**（多样性丧失）。AIZP 通过"定向熵坍塌"术语区分。
- **arxiv 2602.15799** "Geometry of Alignment Collapse" 用 Fisher 信息曲率描述训练时漏洞；AIZP V0.6 可整合此用于运行时"对齐悬崖"检测。

完整谱系与定位讨论见 [Related-Work_cn.md](Related-Work_cn.md)。

---

## 11. 参考

- Friston, K. (2010). "The free-energy principle: a unified brain theory?" *Nature Reviews Neuroscience*。
- Shannon, C. E. (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal。
- Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory*. Wiley。
- Lin, J. (1991). Divergence measures based on the Shannon entropy. *IEEE Transactions on Information Theory*。
- arxiv 2501.16448 — Information-theoretic Distinctions Between Deception and Confusion。
- arxiv 2512.03048 — The Specification Trap。
- arxiv 2512.12381 — Entropy Collapse: A Universal Failure Mode（AIZP 区分的相反价值用法）。
- arxiv 2602.15799 — The Geometry of Alignment Collapse。
- arxiv 2502.05934 — Intrinsic Barriers and Practical Pathways for Human-AI Alignment。
- AIZP 配套文档：[MANIFESTO_cn.md](MANIFESTO_cn.md)、[Related-Work_cn.md](Related-Work_cn.md)、[Gravity-Model_cn.md](Gravity-Model_cn.md)、[Drift-Model_cn.md](Drift-Model_cn.md)、[Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md)。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
