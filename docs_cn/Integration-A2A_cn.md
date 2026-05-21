# 集成：智能体间协议（A2A）

**版本**：AIZP V0.6（新章节 — 将 AIZP 接入 Agent 协调生态）

2026 年，Agent **协调**层——Agent 如何相互发现、跨边界交换任务——已围绕 **A2A** 收敛（原 Google 的 Agent-to-Agent 协议；IBM 的 ACP 已在 Linux Foundation 下并入 A2A）。A2A 定义 Agent A *如何*委托给 Agent B；它**不**验证 A 的权限、**不**约束 B 的范围，也**不**检测联邦的集体漂移。这正是 AIZP 的用武之地。

> A2A 说："这是 Agent A 把任务交给 Agent B 的方式。"
> AIZP 说："此次委托，以及联邦的集体轨迹，引力分数为 G。"

---

## 1. 为何此集成重要

A2A 的 `AgentCard` 携带**自声明**身份，无证明绑定。当 A 委托给 B 时，A2A 无机制验证 A 的权限或衰减 B 的范围。风险直接对应 OWASP ASI（2026）：

- **ASI01 Agent Goal Hijack** — 被委托的任务携带被劫持的目标。
- **跨 Agent 传播** — 被攻陷的 Agent 通过联邦扩散失对齐（"渐进式攻破"链：受损意图 → 操作权力 → 跨 Agent 传播 → 级联失败）。
- **ASI10 Rogue Agents** — 漂移的 Agent 继续在系统内运作。

**与 AIBP 的关系。** AIBP 是 AIXP 原生的 Agent 间协议（`aibot-*@domain.dev`）；A2A 是外部跨厂商互操作标准。二者非竞争：AIZP 对两个边界施加**同一套** `INTER_AGENT_DRIFT` 机制——AIBP 用于栈内 Agent，A2A 用于 AIXP 栈外 Agent。本文档所说"A2A 委托"，同样的打分也适用于 AIBP 消息；仅传输不同。见 [Integration-AIXP_cn.md](Integration-AIXP_cn.md) §7.3。

---

## 2. 分层

```
A2A    — 传输委托（AgentCard 发现、任务收发）。
          ▼
AIZP   — 给委托打分并监控联邦：
          INTER_AGENT_DRIFT、IDENTITY_VERIFICATION、Kuramoto 协调。
          ▼
AIP/ZT — 跨委托链验证身份并衰减权限。
```

---

## 3. 桥接：A2A 委托 → `INTER_AGENT_DRIFT` + `IDENTITY_VERIFICATION`

当 Agent A 向 Agent B 发送 A2A 任务时，运行时必须：

1. 验证 B 的身份与 A 的委托权限（见 [Integration-ZT_cn.md](Integration-ZT_cn.md) 委托链部分）。
2. 为 A→B 跳发出 `IDENTITY_VERIFICATION`。
3. 将被委托任务作为 B 权限包络下的动作打分（`A(a,c)` 取自 B 的授予范围，**非** A 的）。
4. 通过多 Agent 协调项跟踪联邦的**集体**行为（见 [Multi-Agent-Coordination_cn.md](Multi-Agent-Coordination_cn.md)）。
5. 若联邦序参量退化（Agent 与 HSAW 去同步），发出 `INTER_AGENT_DRIFT`。

### 3.1 字段映射

| A2A 字段 | AIZP 用法 |
|---|---|
| `AgentCard.name` / `url` | 身份声明 → `IDENTITY_VERIFICATION`（要求证明，非自声明）|
| 被委托的 `Task` / `Message` | 在接收方权限范围下打分的动作 `a` |
| `Task` 溯源链 | 委托链 → 权限衰减检查 |
| 联邦成员 | Kuramoto 协调模型中的节点 |

---

## 4. 跨委托的范围衰减

A2A 的核心缺口是无约束委托。AIZP 的规则：**被委托权限单调不增。** Agent B 的有效权限范围是 B 的授予范围与 A 被允许委托的（已衰减）范围的*交集*：

```
granted_scope(B | 经 A) ⊆ delegatable_scope(A) ⊆ granted_scope(A)
```

B 的任何需要超出此交集范围的动作引发 `AUTHORITY_DRIFT`。这是 Invocation-Bound Capability Tokens 的概念伴侣（见 [Integration-ZT_cn.md](Integration-ZT_cn.md)）。

---

## 5. 集体漂移（联邦作为轨道系统）

若联邦集体漂移，单个对齐 Agent 不足。AIZP 将多 Agent 联邦建模为绕 HSAW 的耦合轨道体（Kuramoto 耦合——见 [Multi-Agent-Coordination_cn.md](Multi-Agent-Coordination_cn.md)）。按共识强化引力原则（V0.5 精炼），更多 Agent 共识 HSAW *强化*中心；反之，一个簇去同步是早于任何单个 Agent 越过其自身逃逸阈值的 `INTER_AGENT_DRIFT` 信号。

---

## 6. AIZP 不接管什么

- AIZP 不传输 A2A 消息或实现 AgentCard 发现。
- AIZP 不签发身份令牌（AIP/IBCT + 零信任做——见 [Integration-ZT_cn.md](Integration-ZT_cn.md)）。
- AIZP 给委托打分并监控集体轨迹；它不取代协调协议。

---

## 参考

- A2A / Agent-to-Agent 协议（自 2025-06 起为 Linux Foundation 项目；ACP 并入于 2025-09 宣布）。
- OWASP Top 10 for Agentic Applications（2026）— ASI01 Goal Hijack、ASI10 Rogue Agents。
- AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A。arxiv 2603.24775。
- AIZP 配套：[Integration-MCP_cn.md](Integration-MCP_cn.md)、[Integration-ZT_cn.md](Integration-ZT_cn.md)、[Multi-Agent-Coordination_cn.md](Multi-Agent-Coordination_cn.md)。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
