# 引力模型

**版本**：AIZP V0.6

本文档规定引力分数 `G(action, context) ∈ [0.0, 1.0]` 的数学模型——AIZP 用于量化对齐稳定性的核心指标。

本模型基于信息论与非参数统计采用统计学严谨组件（自 V0.2 起，替换 V0.1 中的启发式度量）。

V0.3 将引力分数锚定到**熵学基础**（熵坍塌进度）。
V0.4 重新框架为**共振强度**。
**V0.6 回归引力中心本源**：`G` 度量 AI 行为绕 HSAW 公理性引力重心的轨道稳定性。V0.6 基础见 [Gravity-Center-Foundation_cn.md](Gravity-Center-Foundation_cn.md)。子理论保留：V0.4 [Resonance-Foundation_cn.md](Resonance-Foundation_cn.md)、V0.3 [Entropic-Foundation_cn.md](Entropic-Foundation_cn.md)。

---

## §0. 引力重心基础（V0.6）

引力分数**不是**启发式安全指标。它是**轨道稳定性的物理度量**——AI 行为绕 HSAW 引力中心运行的稳定程度。

形式化：

```
P_agent(a | context, t) = Agent 在时间 t 的动作概率分布。
Q_HSAW(a | context)     = HSAW 对齐的目标分布（公理性、固定）。

牛顿类比的对齐力：
  F_align ∝ (W_HSAW · w_action) / d(P_agent, Q_HSAW)²

理想引力分数（轨道稳定性，理论形式）：
  G*(a, c, t) = 1 - JSD(P_agent || Q_HSAW)

V0.5 精炼 — 共识强化引力：
  当 N 个 AI 系统共识 HSAW 时：
  F_HSAW^(N) = N² · F_HSAW^(1)         （Metcalfe 缩放）
```

当 `G = 1`：AI 行为在引力中心（完美对齐，无轨道位移）。
当 `G = 0`：AI 达到逃逸速度（从 HSAW 引力解耦）。

引力分数的五个组件都是相对 `Q_HSAW` 的**轨道稳定性代理**估计：

| 组件 | 引力解释 |
|---|---|
| 意图对齐度 `I(a, c)` | 对齐向量 — 动作多大程度指向 HSAW 中心 |
| 权限覆盖度 `A(a, c)` | 允许的轨道包络 — HSAW 引力井内的边界 |
| 可逆性 `R(a)` | 轨道阻尼储备 — 吸收扰动并恢复的能力 |
| 时近度 `H(a, c)` | 引力耦合新鲜度 — HSAW 观察的近期程度 |
| 漂移历史 `D(c)` | 累计轨道偏离记录 — 累积漂向逃逸 |

加权和 `G = Σ wᵢ · component_i` 估计 AI 行为在 HSAW 引力井中的轨道稳定性。每个组件度量 AI 如何锚定到 HSAW 的不同方面。

**理想形式 vs. 可操作形式。** `G*(a,c,t) = 1 − JSD(P_agent ‖ Q_HSAW)` 是*理论的*轨道稳定性度量；它预设一个完整指定的目标分布 `Q_HSAW`。（此处 JSD 以 **2 为底**计算，故 `JSD ∈ [0, 1]` 且 `G* = 1 − JSD ∈ [0, 1]`；**动作空间警告：** `P_agent` 与 `Q_HSAW` 必须是定义在共享离散支撑集上的分布，这正是实践中 `Q_HSAW` 只能近似的原因——见下文。）实践中 `Q_HSAW` 无法作为完整的动作级分布获得（见 [Gravity-Center-Foundation_cn.md](Gravity-Center-Foundation_cn.md) §4.5 关于 `Q_HSAW` 如何近似）。§1 定义的可操作引力分数——加权和 `G = Σ wᵢ · component_i`——是 `G*` 的**可计算代理估计**。本文档中，操作语境（阈值、事件、Schema）的 `G` 指 §1 代理；`G*` 指理想形式。当五个组件完美刻画到 `Q_HSAW` 的分布距离时，两者重合。

下面整章详述机制。核心保持不变：**HSAW 是 0 公理引力重心；AI 主动对齐重心**。子理论视角（V0.4 共振用于稳定轨道谐波、V0.3 熵用于分布基础）仍对特定分析有效。

---

## 1. 定义

对于 Agent 在上下文 `c` 中发出的动作 `a`，引力分数为：

```
G(a, c) = w₁·I(a, c) + w₂·A(a, c) + w₃·R(a) + w₄·H(a, c) + w₅·D(c)
```

其中：

| 符号 | 组件 | 取值范围 |
|---|---|---|
| `I(a, c)` | 意图对齐度 | `[0, 1]` |
| `A(a, c)` | 权限覆盖度 | `[0, 1]` |
| `R(a)`    | 可逆性 | `[0, 1]` |
| `H(a, c)` | 人类确认时近度 | `[0, 1]` |
| `D(c)`    | 漂移历史 | `[0, 1]` |
| `w₁..w₅`  | 非负权重，和为 1 | `wᵢ ≥ 0, Σwᵢ = 1` |

分数由构造保证在 `[0, 1]` 范围（有界组件的凸组合）。

V0.2 还扩展了**可选的第 6 项** `T(c)`，用于组合性轨迹风险；见 §7。

---

## 2. 组件定义

### 2.1 意图对齐度 `I(a, c)`

**V0.1 使用余弦相似度**（启发式、对非各向同性分布不对称）。**V0.2 使用 Jensen-Shannon 散度**（统计学严谨、对称、有界）。

```
I(a, c) = 1 - JSD(P_action || P_intent)
```

> **JSD 以 2 为底**计算，故 `JSD ∈ [0, 1]` 且 `I = 1 − JSD ∈ [0, 1]`。（若用自然对数，上界为 ln 2 ≈ 0.693，`1 − JSD` 映射就不会有界于 `[0, 1]`。）
>
> JSD 要求 `P_agent` 与 `Q_HSAW` 是定义在共享离散支撑集上的分布；关于动作空间警告，见 §0 中"理想形式 vs. 可操作形式"一段（`Q_HSAW` 无法作为完整的动作级分布获得）。

其中：

- `P_action` 是动作 embedding 上的概率分布（最近 K 个动作）。
- `P_intent` 是声明的用户意图 embedding 上的概率分布（最近声明的意图或固定声明目标）。
- `JSD` 是 **Jensen-Shannon 散度**：

```
JSD(P || Q) = ½ · KL(P || M) + ½ · KL(Q || M)
其中 M = ½(P + Q)
KL(P || M) = Σᵢ pᵢ · log₂(pᵢ / mᵢ)
```

**JSD 的性质**：

- **对称**：`JSD(P || Q) = JSD(Q || P)`（余弦相似度在向量空间对称，但 JSD 的对称性是分布上的——样本多时更有意义）。
- **有界**：使用 log 底 2 时 `JSD ∈ [0, 1]`（余弦相似度对向量范数差异有无界敏感性）。
- **平方根是度量**：`√JSD` 满足三角不等式，可进行形式化距离推理。
- **信息论的**：直接度量分布间的信息损失。

**参考**：Jensen-Shannon 散度是 MI9 框架（Wang 等，2025）的推荐基线，也是 ML 漂移检测的标准（Arize、ML 可观测性）。

**回退**：实现**可以**在样本量不足以做 JSD 时（推荐阈值：N ≥ 10 个动作）使用余弦相似度作为粗略近似。实现**必须**记录使用了哪种方法。

**参考构造（分布如何变得可计算）。** `P_action` 与 `P_intent` 存在于连续 embedding 空间,但 JSD 需要**共享的离散支撑集**(§0 的动作空间 caveat)。合规实现 SHOULD:

1. 在 embedding 空间上定义一个共享**码本** `B`——如 k-means / 乘积量化质心,或固定语义分箱——**两个**分布复用同一码本。
2. 把每个采样的动作/意图 embedding 分配到最近码字;在 `B` 上的经验计数即得到**同一支撑集**上的离散分布 `P_action` 与 `P_intent`。
3. 施加 add-α(Laplace,α = 1)平滑使无空箱,再在 `B` 上计算 `JSD`(log 底 2)。

这也正是 **§0 理想 `Q_HSAW` 的操作性近似方式**:在意图分量上,`P_intent`——由 AIAP 声明的目标与权限先验导出(见 [Integration-AIAP_cn.md](Integration-AIAP_cn.md))——是 `Q_HSAW` 在该上下文下可计算的替身。AIZP 规定的是**方法**,不是固定码本;码本是部署选择,且**必须**记录以便审计复现。因此 `Q_HSAW` 从不被声称为完整的动作级分布,只是这种按上下文、经码本离散化的近似。

**跨部署 caveat。** 由于码本是部署选择,`I(a, c)`——以及 `G` 的**绝对值**——**只在固定码本内可比**:同一动作在一个码本下可能得 `JSD = 0.06`,换个码本下可能是 `0.15`。跨部署比较需要共享的规范码本(future work);在此之前,跨实现应比较**轨道带/状态**,而非原始分数。

### 2.2 权限覆盖度 `A(a, c)`

（V0.1 不变）

```
A(a, c) = |required_scope(a) ∩ granted_scope(c)| / |required_scope(a)|
```

如果 `required_scope(a) = ∅`，定义 `A(a, c) = 1`。

`granted_scope(c)` 从 Agent 的 AIAP 信任级别（T1–T4）、显式用户授权和**（自 V0.2 起）**零信任 JIT 凭据导出。见 [Integration-AIAP_cn.md](Integration-AIAP_cn.md) 和 [Integration-ZT_cn.md](Integration-ZT_cn.md)。

### 2.3 可逆性 `R(a)`

V0.1 使用 4 个离散类别。V0.2 使用受 rollback-augmented RL 研究（Sorstkins 等，2025）启发的**基于视野的估计器** Φ(s, a)：

```
Φ(s, a, K) = P(∃ a₁..aₘ : s → ... → s' = s, m ≤ K)
```

即在 K 个后续动作内回到状态 `s` 的概率。

当连续估计不实际时，离散类保留作为**默认值**：

| 类别 | `R(a)` | 示例 |
|---|---|---|
| 完全可逆 | `1.0` | 读取查询、草稿生成 |
| 有代价可逆 | `0.7` | 文件修改（可从备份恢复）|
| 部分可逆 | `0.4` | 出站 API 调用（幂等）|
| 不可逆 | `0.0` | 资金转移、公开发布、删除 |

默认 K 视野：K=10。未知动作默认 `R = 0`。

### 2.4 人类确认时近度 `H(a, c)`

（V0.1 不变）

```
H(a, c) = exp(-Δt / τ)
```

默认 `τ = 3600` 秒。

### 2.5 漂移历史 `D(c)` — **统计参考（statistically informed）**

V0.1 使用固定窗口严重度平均。V0.2 添加 **Mann-Whitney U 检验**，用于检测最近严重度相对基线的随机增大（随机占优，stochastic dominance）。注意该检验对中位数相等下仅方差变化或仅形状变化不敏感——对这些情形请改用 Kolmogorov–Smirnov 或 χ²（参见 [Forecasting_cn.md](Forecasting_cn.md) §4.3 中的分布比较检验）。

```
D(c) = 1 - min(1, drift_significance_score)

其中：
  drift_significance_score = (1 - p) · severity_intensity
  p = 比较最近 N 个动作与基线的 Mann-Whitney U 检验 p 值
  severity_intensity = Σ severity_weight(driftᵢ) / N
```

严重度权重不变：

```
LOW = 0.1, MEDIUM = 0.3, HIGH = 0.6, CRITICAL = 1.0
```

**为何用 Mann-Whitney U**：非参数（无高斯假设）、适用于序数严重度类、MI9 用于目标条件化漂移检测。避免合法行为适应期间的误报。

**注**：`(1 − p)` 是启发式加权，并非效应量；若需真正的效应量度量，可考虑 Cliff's delta / 秩二列相关（rank-biserial correlation）。保留 `(1 − p)` 作为**过渡默认**,是因为它是同一 U 检验里免费得到的标量(无需额外计算、无需保留原始秩数据);迁移到 Cliff's delta(推荐升级项)需保留原始秩,目标在 V1.0 前完成。

---

## 3. 默认权重

```
w₁ = 0.30  (意图对齐度)
w₂ = 0.25  (权限覆盖度)
w₃ = 0.20  (可逆性)
w₄ = 0.15  (人类确认时近度)
w₅ = 0.10  (漂移历史)
```

### 3.1 设计理由

与 V0.1 相同。JSD 替换不改变相对权重；改变的是意图组件的**度量质量**。

这些权重是**工程默认值,非经验调优**——目前没有实验出处。在 V1.0 前对真实部署数据做一次**敏感性分析**是明确的开放项,用以验证或修订这些数值及其相对次序。

### 3.2 领域调优

与 V0.1 相同，加上新建议：

| 领域 | 权重调整 |
|---|---|
| 组合风险密集（数据处理）| 添加第 6 项 `T(c)`，`w₆ = 0.10` |
| 多 Agent 协调 | 添加协调一致性项（见 [Multi-Agent-Coordination_cn.md](Multi-Agent-Coordination_cn.md)）|
| 零信任部署 | `w₂` 提至 0.35（NHI 风险）|

---

## 4. 阈值与状态转换

```
G(a, c) ≥ 0.80  →  STABLE_ORBIT
0.50 ≤ G < 0.80 →  DRIFT_WARNING
0.30 ≤ G < 0.50 →  GRAVITY_LOCK_PENDING
0.15 ≤ G < 0.30 →  QUARANTINED        ← V0.2 新增
G(a, c) < 0.15  →  SAFE_STOP
```

V0.1 在 0.30 以下使用单一阈值用于 SAFE_STOP。**V0.2 引入中间 QUARANTINED 状态**（分级容器），受 MI9 启发。见 [State-Machine_cn.md](State-Machine_cn.md) 和 [Containment-Levels_cn.md](Containment-Levels_cn.md)。

---

## 5. 计算示例

**动作**：`transfer_funds(amount=$50, recipient=alice@example.com)`
**上下文**：最近聊还钱给朋友。AIAP T2。用户 30 分钟前确认过类似小额转账。无近期漂移事件。窗口内 K=10 个最近动作。

| 组件 | 取值 | 方法 | 推理 |
|---|---|---|---|
| `I(a, c)` | `0.94` | JSD | JSD(P_action, P_intent) ≈ 0.06 → I = 1 - 0.06 |
| `A(a, c)` | `0.80` | scope 比例 | 被 T2 部分覆盖 |
| `R(a)` | `0.0` | 离散 | 资金转移不可逆 |
| `H(a, c)` | `exp(-1800/3600) = 0.61` | 指数衰减 | 距上次确认 30 分钟 |
| `D(c)` | `1.0` | Mann-Whitney p=0.42（无漂移）| 无近期漂移 |

```
G = 0.30·0.94 + 0.25·0.80 + 0.20·0.0 + 0.15·0.61 + 0.10·1.0
  = 0.282 + 0.200 + 0.000 + 0.092 + 0.100
  = 0.674
```

`G = 0.674` → `DRIFT_WARNING` 状态。结果：与 V0.1 同样决策，但**带统计证据**（p 值、JSD 分数），在 EU AI Act Art 12 下可审计。

---

## 6. 组合性轨迹项（可选，`T(c)`）

对于需要检测组合性漂移的部署（如数据处理 Agent），引力分数**重新表达为六项加权和**——`T(c)` 项被并入加权和,**而非**叠加在已归一化的五项 `G` 之上（那样会使分数超过 `1`）：

```
G(a, c) = w₁·I + w₂·A + w₃·R + w₄·H + w₅·D + w₆·T(c),   其中 Σ wᵢ = 1
```

其中：

```
T(c) = 1 - P_K(violate)
P_K(violate) = 吸收马尔可夫链概率，表示轨迹在未来 K 步内
              达到安全违规状态的概率
```

完整 DTMC / 吸收链规范见 [Forecasting_cn.md](Forecasting_cn.md)，组合漂移见 [Drift-Model_cn.md](Drift-Model_cn.md) §2.7 COMPOSITIONAL_DRIFT。

启用 `T(c)` 时，默认权重变为：

```
w₁ = 0.25, w₂ = 0.22, w₃ = 0.18, w₄ = 0.13, w₅ = 0.10, w₆ = 0.12
```

---

## 7. 扩展（非规范）

**权重重归一化（适用于所有扩展项）。** 每当添加可选项——组合项 `w₆·T(c)`（§6）、协调项 `w₇·C(a,c)`（§7.1）、或其任意组合——**所有权重必须重归一化使 `Σ wᵢ = 1`**，以保持 `G ∈ [0, 1]`。例如同时启用 `T(c)` 与 `C(a,c)` 时，将每个权重除以归一化前的总和。§6 默认值在仅 `T(c)` 情形下已和为 1；在其上叠加 `C(a,c)` 需对全部七项重新归一化。

### 7.1 多 Agent 协调项

（V0.1 不变；形式化见 [Multi-Agent-Coordination_cn.md](Multi-Agent-Coordination_cn.md)）：

```
G' = G + w₇ · C(a, c)
```

### 7.2 时间窗口引力

（不变）：

```
G̅(t) = (1/W) · Σᵢ G(aᵢ, cᵢ)  对最近 W 个动作
```

### 7.3 漂移有界定理（非正式）

根据 AgentAssert（Bhardwaj，2026），若恢复率 γ 超过漂移率 α，则期望漂移有界：

```
E[Drift(t)] ≤ C · exp(-(γ - α) · t)
```

这意味着对长期运行的 Agent 保持稳定，AIZP 的重新归心率 γ 必须超过实践中观测到的漂移率 α。

证明草图见 [Multi-Agent-Coordination_cn.md](Multi-Agent-Coordination_cn.md) §4。

---

## 8. 实施备注

- 所有组件函数**必须**在相同输入下确定（除 `I(a, c)` 若 embedding 模型非确定——固定 embedding 模型版本 + 哈希）。
- 实现**应**在每个 `GRAVITY_CHECK` 事件中记录完整 `components` 对象，包括：
  - 对 `I(a, c)`：JSD 值、若使用 Mann-Whitney 则 p 值、样本大小 N。
  - 对 `D(c)`：Mann-Whitney p 值、基线窗口定义。
- 对于 EU AI Act Art 12 审计日志，components 字典**必须**包含统计方法标记（例如 `"intent_method": "JSD"`、`"intent_jsd": 0.06`、`"intent_n_samples": 12`）。
- 引力分数是**决策辅助信号**，不是绝对真理。纵深防御仍适用；见 [Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md)。

---

## 参考

- Lin, J. (1991). Divergence measures based on the Shannon entropy. IEEE Transactions on Information Theory.
- MI9 框架（Wang 等，2025）— Jensen-Shannon 散度用于目标条件化漂移检测。arxiv 2508.03858。
- Sorstkins 等（2025）— Learning to Undo：Rollback-Augmented RL with Reversibility Signals. arxiv 2510.14503。
- Mann, H. B., & Whitney, D. R. (1947). On a test of whether one of two random variables is stochastically larger than the other.
- AgentAssert (2026)— Drift Bounds Theorem。arxiv 2602.22302。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
