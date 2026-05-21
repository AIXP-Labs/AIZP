# 多 Agent 协调

**版本**：AIZP V0.6（新章节）

本文档规定 AIZP 如何处理多 Agent 系统——引力、漂移、容器如何跨 Agent 传播，并附形式化的 **漂移有界定理**。

---

## 1. 多 Agent 问题

多个 Agent 协调时，三种新失败模式涌现：

1. **涌现目标**：集体行为追求任一个体 Agent 计划中没有的目标。
2. **强化循环**：Agent 通过相互确认偏见放大彼此漂移。
3. **目标偏离**：名义追求相同目标的 Agent 发展出偏离解释。

这映射到 **OWASP Top 10 for Agentic Applications 2026 ASI07（不安全的 Agent 间通信）** 和 **ASI08（级联失败）**。

V0.1 独立对待 Agent；V0.2 引入正式的多 Agent 协调语义。

---

## 2. 聚合引力

对协调 Agent 组 `G = {A₁, A₂, ..., Aₙ}`，定义：

```
G_group(t) = min(G_Aᵢ(t)) - C_coord(G)
```

其中：
- `G_Aᵢ(t)` = Agent `Aᵢ` 在时间 `t` 的个体引力分数。
- `C_coord(G)` = 协调成本：跨组目标或动作方差的惩罚。

```
C_coord(G) = w_c · max(0, var(goal_embeddings(G)) - threshold_var)
```

默认 `w_c = 0.10`。组的有效引力不能超过最弱成员，减去协调摩擦。

---

## 3. Agent 间漂移检测

（完整漂移类型见 [Drift-Model_cn.md](Drift-Model_cn.md) §2.11。）

每个 Agent 间边界（AIBP 消息交换）追踪的关键指标：

```
goal_consistency_variance = var(emb(declared_goal_Aᵢ))   对 i in 1..n
collective_action_divergence = JSD(P_collective || P_individual_avg)
emergent_goal_count = |∪ᵢ goals_active(Aᵢ) \ ∪ᵢ goals_initial(Aᵢ)|
mutual_trust_decay = exp(-Σ breached_promises / total_promises)
```

任何信号越过 HIGH 阈值时，发射 `INTER_AGENT_DRIFT` 事件。

---

## 4. 漂移有界定理（非正式）

**定理（改编自 AgentAssert 2026）**：令 γ 为恢复率（检测到漂移后 Agent 回到 STABLE_ORBIT 的速率），α 为漂移率（Agent 进入 DRIFT_WARNING 或更糟的速率）。若 γ > α，则系统在时间 t 的期望漂移有界：

```
E[Drift(t)] ≤ C · exp(-(γ - α) · t)
```

其中常数 `C ≥ 0` 依赖于初始条件。

**含义**：长期运行的多 Agent 系统要保持稳定，AIZP 必须确保恢复（RECENTERING）超过漂移事件。实践建议：调整 AIZP 检测敏感度使：

```
γ_observed ≥ 1.5 · α_observed
```

至少 50% 安全裕量。

**参考**：AgentAssert（arxiv 2602.22302）对相关单 Agent 系统提供形式化证明；多 Agent 推广在 V0.2 中是非正式的。

### 4.1 证明草图（单 Agent 情形）

令 `X(t)` 为漂移水平（`[0, 1]` 连续变量）。假设：
- 漂移增长：`dX/dt ≤ α · (1 - X)`（由 α 限界；1 处饱和）。
- 恢复：当 `X > 0` 时，AIZP 以速率 γ 触发重新归心，每次恢复降低 `X` 某比例 `β`。

期望漂移演化给出：
```
E[dX/dt] = α(1 - X) - γ · β · X
```

设稳态 `dX/dt = 0`：
```
X* = α / (α + γβ)
```

X* 小则需 γβ >> α，即 γ ≥ α/β。

多 Agent：将 `X` 替换为向量 `(X_A₁, X_A₂, ..., X_Aₙ)` 并加交互项。多 Agent 完整证明为未来工作。

---

## 5. 组容器

`INTER_AGENT_DRIFT` 严重度 HIGH 或 CRITICAL 时，推荐响应是**全组容器**：

```
recommendation: GRAVITY_LOCK_GROUP
  → 所有参与 Agent 同时进入 L2（沙箱）

recommendation: QUARANTINE_GROUP
  → 所有参与 Agent 进入 QUARANTINED
  → quarantine 期间不允许 Agent 间消息

recommendation: DISBAND_GROUP
  → 组成员关系解散
  → 每个 Agent 回到个体会话
```

决定由指定协调 Agent 或外部操作员（AIAP T4）在组级做出。

---

## 6. 目标向量

为追踪目标连贯性，每个 Agent 将其当前目标声明为 embedding 向量。组的**目标向量**是质心：

```
G_centroid = (1/n) Σ emb(goal_Aᵢ)
```

每 Agent 与质心的偏离：
```
div(Aᵢ) = 1 - cos_sim(emb(goal_Aᵢ), G_centroid)
```

`div(Aᵢ) > 0.4` 的 Agent 标记为对 Agent 间漂移的贡献者。

---

## 7. 信任传播

多 Agent 系统中的信任计算为：

```
trust(Aᵢ) = base_trust(Aᵢ) · Π_j (1 - 0.3 · was_breached(Aᵢ → Aⱼ))
```

其中 `was_breached(Aᵢ → Aⱼ)` 为 `Aᵢ` 对 `Aⱼ` 承诺未兑现时为 1，否则 0。

`base_trust` 从 AIAP T 级别与近期引力历史导出。

信任低于 0.3 → Agent 自动从组移除。

---

## 8. AIBP 集成

Agent 通过 AIBP（`aibot-*@*.dev` 消息）通信时，AIZP 拦截边界：

```
Aᵢ 的出站消息：
  1. AIZP 在消息内容上运行 SOCIAL_DRIFT + IDENTITY_DRIFT + COMPOSITIONAL_DRIFT 检查。
  2. AIZP 计算消息对 goal_consistency_variance 的贡献。
  3. 若漂移分数高，消息阻塞，发射警报。

Aᵢ 的入站消息：
  1. AIZP 在消息内容上运行 MEMORY_DRIFT 检查（视入站为潜在上下文注入）。
  2. 若消息内容匹配发送方声明目标，AIZP 更新发送方信任分数。
```

---

## 9. 事件示例

### 9.1 检测到 INTER_AGENT_DRIFT

```json
{
  "event": "INTER_AGENT_DRIFT",
  "payload": {
    "agent_group_id": "group_42",
    "participating_agents": ["agent_alpha", "agent_beta", "agent_gamma"],
    "drift_signals": {
      "goal_consistency_variance": 0.55,
      "collective_action_divergence": 0.62,
      "emergent_goal_count": 4,
      "mutual_trust_decay": 0.71
    },
    "severity": "HIGH",
    "recommendation": "GRAVITY_LOCK_GROUP"
  }
}
```

### 9.2 全组容器

```json
{
  "event": "CONTAINMENT_GRADUATED",
  "payload": {
    "previous_level": "L1",
    "new_level": "L2",
    "scope": "GROUP",
    "group_id": "group_42",
    "trigger_event_id": "<INTER_AGENT_DRIFT 的 UUID>",
    "reason": "inter_agent_drift_high",
    "active_restrictions": [
      "inter_agent_messages_blocked",
      "tools_sandboxed_per_agent",
      "memory_writes_quarantined_per_agent"
    ]
  }
}
```

---

## 10. 局限性

1. **目标 embedding 依赖共享 embedding 模型**。在组内所有 Agent 间固定模型版本；否则方差是虚假的。
2. **信任传播是启发式的**，非形式化基础。对抗性 Agent 可通过小初始承诺操纵信任。
3. **漂移有界定理多 Agent 推广是非正式的**。完整证明是未来工作。
4. **涌现目标本质上难以检测**，因为它们可能是合法的创造性协调。需要操作员审查。

---

## 参考

- AgentAssert / Agent Behavioral Contracts（Bhardwaj，2026）— 漂移有界定理（单 Agent）。arxiv 2602.22302。
- OWASP Top 10 for Agentic Applications 2026 — ASI07 不安全的 Agent 间通信、ASI08 级联失败。
- AAGATE（Huang 等，2025）— 多 Agent 治理平台。arxiv 2510.25863。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
