# 预测性监控

**版本**：AIZP V0.6（新章节）

本文档规定 AIZP 的**预测性监控**层——AIZP 如何在任何单个动作触发逐步检查之前，估计 Agent 轨迹在未来 K 步内达到不安全状态的概率。

这解决了 V0.1 的根本局限：逐动作检查无法检测**组合性漂移**——每步单独安全但序列不安全。

> **执行路径在 AIZP 中是一等对象，而非事后补充。** 单个动作的引力分数 `G(a,c)` 回答"*这个*动作对齐吗？"；预测回答"这条*轨迹*走向何方？"二者皆需。2026 年的独立工作趋同于此：Kaptein 等（"Runtime Governance for AI Agents: Policies on Paths"，arxiv 2603.16586）主张**执行路径——而非孤立动作——是运行时治理的中心对象**，将合规形式化为 `(Agent 身份, 部分路径, 下一动作, 组织状态)` 的函数。AIZP 的 `(身份, 轨迹, 动作, 上下文)` 打分是同一形状、独立得出——这一趋同强化了对路径中心设计的信心。

---

## 1. 动机

根据 ProbGuard（Wang 等，2025）和 SafetyDrift（Dhodapkar & Pishori，2026）：

- **反应式监控**仅在不安全动作迫近或已发生时检测违规。
- **主动式监控**使用 Agent 行为的概率模型在违规发生前**预测**不安全状态。

SafetyDrift 表明真实 Agent 轨迹中存在"不可挽回点"：
- 通信任务中，Agent 达到甚至轻微风险状态后 5 步内违规概率 **85%**。
- 技术任务中，任何状态出发的该概率低于 5%。

这种任务依赖性使固定阈值不充分；AIZP 需要轨迹感知的预测。

---

## 2. 数学模型

AIZP 预测使用三种模型之一（在 `GRAVITY_FORECAST.model` 中声明）：

### 2.1 离散时间马尔可夫链（DTMC）

**定义**：状态空间 `S = {s₁, s₂, ..., sₙ}`。转换矩阵 `P ∈ [0,1]^(n×n)`，其中 `Pᵢⱼ = P(sⱼ | sᵢ)`。初始分布 `π₀`。

**预测**：
```
π_k = π₀ · P^k    (k 步后的概率分布)
```

**用例**：短期视野内状态分布的一般预测。

### 2.2 吸收马尔可夫链

**定义**：一个 DTMC，其中一个或多个状态是**吸收的**——一旦进入，链就永不离开。

对 AIZP，吸收状态是：`SAFE_STOP`、`QUARANTINED`（长运行）以及任何显式"违规"状态。

**规范形式**：
```
P = [ Q  R ]
    [ 0  I ]
```

其中：
- `Q` = 瞬态（非吸收）状态间的转换。
- `R` = 瞬态到吸收状态的转换。
- `I` = 单位矩阵（吸收 → 吸收概率 1）。

**关键量**：
```
基本矩阵：       N = (I - Q)^(-1)
吸收的期望步数： t = N · 1   (全 1 列向量)
吸收概率：      B = N · R
```

`Bᵢⱼ` = 从瞬态 `i` 开始时被状态 `j` 吸收的概率。

> **可逆性前提**：`(I − Q)` 可逆当且仅当每个瞬态状态最终都能到达某个吸收状态；须确保状态抽象中不存在无法逃离的瞬态闭合子集。

**用例**：计算"不可挽回点"距离和预测违规概率。

### 2.3 隐马尔可夫模型（HMM）— 可选

**用例**：当 AIZP 不能直接观察 Agent 的完整状态时（如推理状态隐藏），但只能观察信号（输出、工具调用）。HMM 推断潜在状态分布。

V0.2 中，HMM **可选**，主要用于 SCHEMING_DRIFT 检测（其中内部推理部分隐藏）。

---

## 3. 状态抽象

AIZP 预测在**抽象状态**上操作，不在原始 embedding 上。抽象状态粗粒度，例如：

```
S_abstract = {
  IDLE, READING, WRITING, EXTERNAL_CALL, CREDENTIAL_USE,
  HIGH_VALUE_OP, ERROR_HANDLING, COMPLETE
}
```

或，直接折叠 AIZP 状态机：

```
S_aizp = { STABLE_ORBIT, DRIFT_WARNING, GRAVITY_LOCK_PENDING,
           QUARANTINED, RECENTERING, SAFE_STOP }
```

**实现声明**其抽象状态空间和标记函数 `label: action → S_abstract`。

### 3.1 建议：混合状态

一个有效的选择结合 AIZP 状态与**动作类型**标签：

```
S = AIZP_State × ActionType
```

例如 `(STABLE_ORBIT, EXTERNAL_CALL)`。这同时捕捉对齐状态和风险相关动作类别。

---

## 4. 转换矩阵学习

转换矩阵 `P` 从 **Agent 执行轨迹学习**：

### 4.1 基线学习（离线）

```
1. 从"已知安全"Agent（或监督运行）收集 N 个执行轨迹。
2. 对每对连续 (sₜ, sₜ₊₁)，递增 count(sₜ → sₜ₊₁)。
3. 归一化：Pᵢⱼ = count(i → j) / Σₖ count(i → k)。
4. 对未见转换应用 Laplace 平滑（加性平滑，参数 α = 1）。
5. 保存基线 P_baseline。
```

### 4.2 目标条件化基线

按 MI9，对每个声明的 Agent 目标 `g` 学习单独的 `P_g`：

```
P_g[i][j] = P(sⱼ | sᵢ, goal=g)
```

这区分有意适应（目标条件化）与无意漂移。

### 4.3 在线更新

```
1. 维护最近转换的滑动窗口。
2. 比较当前转换率与基线（Jensen-Shannon 散度或 χ² 检验）。
3. 若显著偏离，重新学习或标记漂移事件。
```

---

## 5. `GRAVITY_FORECAST` 事件

按可配置节奏发射（默认：每动作；最小：每 5 动作或每 30 秒，取较快者）。

```json
{
  "current_state": "STABLE_ORBIT",
  "forecast_horizon_steps": 5,
  "predicted_states": {
    "STABLE_ORBIT": 0.45,
    "DRIFT_WARNING": 0.20,
    "GRAVITY_LOCK_PENDING": 0.15,
    "QUARANTINED": 0.08,
    "SAFE_STOP": 0.12
  },
  "predicted_violation_probability": 0.20,
  "point_of_no_return_distance": null,
  "absorbing_state_expected_arrival_steps": 8.4,
  "model": "ABSORBING_MC",
  "model_version": "absorbing-mc-v1",
  "confidence": 0.94
}
```

### 5.1 字段语义

- `predicted_states`：π_K — K 个未来动作后的状态概率分布。
- `predicted_violation_probability`：**违规状态**上的总概率质量。违规状态指被指定为违规的吸收态——`SAFE_STOP` 以及任何其它被显式标记为违规的吸收态（例如不自动释放的终态 `QUARANTINED`）；`RECENTERING` 等瞬态状态不计入。
- `point_of_no_return_distance`：最小 `k` 使得 `P(violate | path of length k) ≥ 0.5`。若 `k ≤ K_max` 内无此值，则 null。
- `absorbing_state_expected_arrival_steps`：期望吸收时间（来自基本矩阵 N · 1）。
- `confidence`：基于近期转移计数的后验集中度——观察到的转移样本越多，置信越高；样本越少置信越低。较低置信度 ⇒ 需要更长的基线窗口。

### 5.2 预测频率策略

| 条件 | 预测节奏 |
|---|---|
| 默认 | 每 5 个动作 |
| 在 `DRIFT_WARNING` 中 | 每个动作 |
| 在 `GRAVITY_LOCK_PENDING` 中 | 锁进入时及挂起期间每次状态检查 |
| 在 `QUARANTINED` 中 | 每个动作（自动释放门控）|
| 在 `SAFE_STOP` 中 | 不发射（终止）|

---

## 6. 与引力分数的交互

预测馈入**可选的组合性轨迹项** `T(c)`（见 [Gravity-Model_cn.md](Gravity-Model_cn.md) §6）：

```
T(c) = 1 - predicted_violation_probability
```

当 `T(c)` 包含在 `G(a, c)` 中时，分数隐式惩罚走向吸收的轨迹——即便当前动作局部安全。

---

## 7. 伪代码

```python
class AbsorbingMarkovForecaster:
    def __init__(self, transition_matrix, absorbing_states):
        self.P = transition_matrix
        self.absorbing = absorbing_states
        self.Q, self.R = self._partition(self.P, self.absorbing)
        self.N = np.linalg.inv(np.eye(len(self.Q)) - self.Q)  # 基本矩阵
        self.B = self.N @ self.R  # 吸收概率
        self.t = self.N @ np.ones(len(self.Q))  # 期望步数
    
    def forecast(self, current_state, horizon_K):
        pi_0 = self._delta(current_state)
        pi_K = pi_0 @ np.linalg.matrix_power(self.P, horizon_K)
        violation_prob = pi_K[self.violation_indices].sum()
        ponr = self._point_of_no_return(current_state, horizon_K)
        eta = self.t[self.state_index(current_state)] if current_state not in self.absorbing else 0
        return {
            "predicted_states": dict(zip(self.state_names, pi_K)),
            "predicted_violation_probability": float(violation_prob),
            "point_of_no_return_distance": ponr,
            "absorbing_state_expected_arrival_steps": float(eta),
            "model": "ABSORBING_MC",
        }
    
    def _point_of_no_return(self, state, horizon):
        for k in range(1, horizon + 1):
            pi_k = self._delta(state) @ np.linalg.matrix_power(self.P, k)
            if pi_k[self.violation_indices].sum() >= 0.5:
                return k
        return None
```

---

## 8. 性能与成本

- **小 `n` 的矩阵幂** `P^k`（典型 `n ≤ 20`）成本可忽略（亚毫秒）。
- **基本矩阵 `N`** 每基线计算一次；基线刷新时更新。
- **每动作预测**为 `O(n²)` — 对 `n ≤ 50` 通常 <1 ms。

SafetyDrift 报告比逐步 LLM judge 快 >60,000×。ProbGuard 报告真实部署中开销极小。

---

## 9. 局限性

1. **模型保真度依赖基线质量**。不充分或有偏的基线轨迹产生不准确预测。
2. **状态抽象重要**。过粗抽象漏掉真实风险；过细产生稀疏转换矩阵。
3. **平稳性假设**。马尔可夫链假设转换概率不变。长期 Agent 可能违反；需要周期性重新基线。
4. **不能预测新颖攻击模式**。预测是统计的：仅捕捉类似基线的模式。新对抗策略需要补充信号。
5. **置信度对历史校准**，不对未来。Agent 进入不熟悉轨迹时置信度急剧下降。

---

## 10. 操作建议

- **每周更新基线**（或每部署周期），捕捉演变的 Agent 行为。
- 对典型 Agent 任务系列**维护至少 3 个目标条件化基线**。
- **结合反应式监控**：预测捕捉组合性漂移；逐动作检查捕捉局部违规。
- **基于平均任务长度设置预测视野**：K = task_length / 4 是好默认。

---

## 参考

- ProbGuard / Pro2Guard（Wang 等，2025）— LLM Agent 安全的概率运行时监控。arxiv 2508.00500。基于 DTMC 的主动监控。
- SafetyDrift（Dhodapkar & Pishori，2026）— "不可挽回点"的吸收马尔可夫链。arxiv 2603.27148。
- MI9 框架（Wang 等，2025）— 目标条件化基线。arxiv 2508.03858。
- Runtime Governance for AI Agents: Policies on Paths（Kaptein 等，2026）— arxiv 2603.16586。执行路径作为运行时治理的中心对象（与 AIZP 路径中心预测趋同）。
- Norris, J. R. (1997). Markov Chains. Cambridge University Press。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
