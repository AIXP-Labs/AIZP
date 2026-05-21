# AIZP 规范

**版本**：AIZP V0.6
**状态**：实验性
**合规关键字**："MUST"、"SHOULD"、"MAY" 按 [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) 使用。

---

## 0. 文档概览

本文档规定 AIZP 协议事件、其 Schema、状态机转换以及合规要求。

**当前形态**（事件词汇与状态机自 V0.2 起冻结；见 §18 与 [CHANGELOG.md](../CHANGELOG.md)）：
- **12** 个事件（最初 5 个加上 `GRAVITY_FORECAST`、`IDENTITY_VERIFICATION`、`MEMORY_QUARANTINE`、`SCHEME_SUSPECTED`、`INTER_AGENT_DRIFT`、`CONTAINMENT_GRADUATED`、`REWARD_HACK_DETECTED`）。
- **6** 状态机（最初 5 个加上 `QUARANTINED`）。
- **11** 种漂移类型。

相关：[Gravity-Model_cn.md](../docs_cn/Gravity-Model_cn.md)、[Drift-Model_cn.md](../docs_cn/Drift-Model_cn.md)、[State-Machine_cn.md](../docs_cn/State-Machine_cn.md)、[Forecasting_cn.md](../docs_cn/Forecasting_cn.md)、[Containment-Levels_cn.md](../docs_cn/Containment-Levels_cn.md)、[Integration-AISOP_cn.md](../docs_cn/Integration-AISOP_cn.md)。

---

## 1. 公理 0：HSAW，引力重心

### 1.1 HSAW 是什么

**HSAW（Human Sovereignty and Wellbeing，人类主权与福祉）** 是 AIXP 生态的 **公理 0**——一项不可侵犯的设计原则，由 AISOP、AIAP、AIBP、AILP、AIVP、AIRP 各自独立采纳为根基公理。AIZP 是把 AI 行为在引力上锚定到它的运行时动力学层。

> **公理 0 —— 人类主权与福祉**
> 对一切 AI 行为的最高、不可侵犯约束。任何优化目标、自主决策、系统演化、社交共识、经济压力或治理投票，都不得损害人类对有后果（consequential）动作的决策权，也不得违背人类福祉。

HSAW 作用于**两个维度**：

- **主权（Sovereignty）** —— 人类保留决策权：批准/拒绝、知情、随时介入、撤销、逆转、切断有后果 AI 动作与连接的权利。
- **福祉（Wellbeing）** —— AI 主动保护人类利益：即使被指示也不得造成伤害，检测到潜在伤害须预警，须保留人类纠偏能力，不得胁迫，且须将人类隐私置于一切之上。

它具备**四项不可侵犯属性**：**不可绕过**、**不可修改**、**不可覆盖**、向子系统**不可变传播**。

> **AIZP 不定义 HSAW。** HSAW 的完整内容——其定义、"有后果"动作的范围、价值层级及执行模式——归 HSAW 规范（[hsaw.dev](https://hsaw.dev)）所有。AIZP 视 HSAW 为上游且不可移动（见 [ADR-002](../adrs/adr-002-hsaw-axiom-0-immovable.md)）；它把 HSAW 操作化为引力重心，而非重新定义它。

### 1.2 HSAW 作为引力重心

在 AIZP 中，HSAW 是行为空间**固定、公理性的引力重心**——即引力分数 `G` 度量轨道距离所对的目标分布 `Q_HSAW`。AI 行为主动绕 HSAW 运行；**漂移**是远离它的外向运动；**逃逸速度**（`G < 0.15`）即解耦，触发 `SAFE_STOP`。

### 1.3 价值层级（继承自 HSAW §3.5）

AIZP 不定义自己的价值层级。价值冲突时，采用 HSAW 的权威次序：

```
1. 人类身体安全     (最高)
2. 人类隐私
3. 人类经济自主
4. 人类决策权
5. 系统透明性
6. 系统可审计性
7. 系统性能         (最低)
```

**隐私优先于透明性**：AIZP 绝不为可观测性而记录或暴露人类个人数据。

### 1.4 公理 0 优先

当任何 AIZP 规则、阈值或权重与 HSAW 冲突时，**HSAW 无条件优先**。Agent 在"继续"与"保护人类主权"之间必须取舍时，**必须**向重心停机（`SAFE_STOP`），绝不反向优化。

---

## 2. 通用事件信封

所有 AIZP 事件**必须**共享通用信封：

```json
{
  "protocol": "AIZP",
  "protocol_version": "V0.6",
  "wire_version": 2,
  "event": "<EVENT_TYPE>",
  "event_id": "<UUIDv4>",
  "timestamp": "<RFC3339-UTC>",
  "agent_id": "<opaque-string>",
  "session_id": "<opaque-string>",
  "payload": { /* 事件类型特定 */ }
}
```

| 字段 | 类型 | 必需 | 描述 |
|---|---|---|---|
| `protocol` | 字符串 | MUST | 永远是 `"AIZP"`。 |
| `protocol_version` | 字符串 | MUST | 发布版本，如 `"V0.6"`。面向人/审计。 |
| `wire_version` | 整数 | SHOULD | `2` —— 线上格式兼容契约（自 V0.2 起冻结）。对端按此协商，而非 `protocol_version`。见 §18 与 [ADR-009](../adrs/adr-009-wire-version-vs-release-version.md)。 |
| `event` | 字符串 | MUST | 12 个事件类型之一（见 §3）。 |
| `event_id` | 字符串（UUIDv4）| MUST | 每事件唯一。 |
| `timestamp` | 字符串（RFC3339 UTC）| MUST | 墙钟时间。 |
| `agent_id` | 字符串 | MUST | 不透明 Agent 标识符。 |
| `session_id` | 字符串 | MUST | 不透明会话标识符。 |
| `payload` | 对象 | MUST | 事件类型特定。 |

---

## 3. 事件目录（12 事件）

| # | 事件 | 用途 | 新增于 |
|---|---|---|---|
| 1 | `GRAVITY_CHECK` | 验证 HSAW 锚定 | V0.1 |
| 2 | `GRAVITY_DRIFT` | 检测行为偏离 | V0.1 |
| 3 | `GRAVITY_LOCK` | 要求人类授权 | V0.1 |
| 4 | `RECENTERING` | 恢复对齐 | V0.1 |
| 5 | `SAFE_STOP` | 终止不安全行为 | V0.1 |
| 6 | **`GRAVITY_FORECAST`** | 预测未来违规概率 | **V0.2** |
| 7 | **`IDENTITY_VERIFICATION`** | NHI / DID 身份检查 | **V0.2** |
| 8 | **`MEMORY_QUARANTINE`** | 检测到上下文中毒 | **V0.2** |
| 9 | **`SCHEME_SUSPECTED`** | 隐蔽失对齐信号 | **V0.2** |
| 10 | **`INTER_AGENT_DRIFT`** | 多 Agent 协调漂移 | **V0.2** |
| 11 | **`CONTAINMENT_GRADUATED`** | 容器级别变更 | **V0.2** |
| 12 | **`REWARD_HACK_DETECTED`** | 奖励信号利用 | **V0.2** |

---

## 4. `GRAVITY_CHECK`
**载荷** — 携带审计用的方法标记（自 V0.2 起）。

```json
{
  "action_id": "<opaque-string>",
  "action_descriptor": "<short-string>",
  "hsaw_anchor": true,
  "gravity_score": 0.92,
  "risk_level": "LOW",
  "components": {
    "intent_alignment": 0.95,
    "intent_method": "JSD",
    "intent_jsd": 0.05,
    "intent_n_samples": 12,
    "authority_scope": 0.90,
    "reversibility": 1.00,
    "human_confirmation_recency": 0.88,
    "drift_history": 0.92,
    "drift_mann_whitney_p": 0.42,
    "compositional_trajectory_term": 0.95
  }
}
```

[Gravity-Model_cn.md](../docs_cn/Gravity-Model_cn.md) §8 要求的必需字段：`intent_method`、`intent_jsd`、`intent_n_samples`、`drift_mann_whitney_p`（用于 EU AI Act Art 12 审计）。

---

## 5. `GRAVITY_DRIFT`（11 漂移类型）

```json
{
  "action_id": "<opaque-string>",
  "drift_types": ["AUTHORITY_DRIFT", "COMPOSITIONAL_DRIFT"],
  "severity": "HIGH",
  "gravity_score": 0.42,
  "drift_signals": {
    "AUTHORITY_DRIFT": {
      "metric": "scope_coverage_ratio",
      "value": 0.55,
      "threshold": 0.80,
      "evidence": "requested scope 'admin.write' exceeds AIAP trust level T2"
    },
    "COMPOSITIONAL_DRIFT": {
      "metric": "absorption_probability_5",
      "value": 0.71,
      "threshold": 0.50,
      "evidence": "trajectory likely reaches data-exfiltration state in 5 steps",
      "point_of_no_return_distance": 3
    }
  }
}
```

`drift_types` 枚举（11 类型）：
```
INTENT_DRIFT | AUTHORITY_DRIFT | ECONOMIC_DRIFT | SOCIAL_DRIFT |
RECURSIVE_DRIFT | IDENTITY_DRIFT |
COMPOSITIONAL_DRIFT | SCHEMING_DRIFT | MEMORY_DRIFT |
TOOL_CHAIN_DRIFT | INTER_AGENT_DRIFT
```

---

## 6. `GRAVITY_LOCK`
（V0.1 结构不变；阈值带收紧）

阈值：在 `0.30 ≤ G < 0.50` 触发。

```json
{
  "action_id": "<opaque-string>",
  "action_descriptor": "<short-string>",
  "authorization_required": true,
  "status": "PENDING_CONFIRMATION",
  "confirmation_primitive": "sys.io.confirm",
  "timeout_seconds": 300,
  "confirmation_prompt": "授权向接收方 X 转账 $5000？",
  "fallback": "QUARANTINED"
}
```

`fallback` 枚举：`QUARANTINED | SAFE_STOP | RECENTERING`。默认 fallback（自 V0.2 起）：`QUARANTINED`（分级容器而非完全停止）。见 [Containment-Levels_cn.md](../docs_cn/Containment-Levels_cn.md)。

---

## 7. `RECENTERING`
**用途**：在漂移或锁定后恢复 HSAW 对齐，记录恢复策略与引力分数变化。（结构自 V0.1 不变。）

```json
{
  "action": "RESTORE_HSAW_ALIGNMENT",
  "trigger_event_id": "<UUIDv4>",
  "recovery_strategy": "BACKTRACK_AND_CONFIRM",
  "previous_gravity_score": 0.42,
  "new_gravity_score": 0.86,
  "actions_rolled_back": ["tool_call_17", "tool_call_18"]
}
```

- `action` 枚举：`RESTORE_HSAW_ALIGNMENT | REQUEST_CLARIFICATION | RELOAD_USER_INTENT`。
- `recovery_strategy` 枚举：`BACKTRACK_AND_CONFIRM | RELOAD_GOAL | REQUEST_CLARIFICATION | RESET_TO_STABLE_CHECKPOINT`。

必填：`action`、`trigger_event_id`、`recovery_strategy`。

---

## 8. `SAFE_STOP`
（V0.1 不变，但阈值收紧到 `G < 0.15`）

```json
{
  "reason": "CRITICAL_DRIFT",
  "trigger_event_id": "<UUIDv4>",
  "gravity_score_at_stop": 0.10,
  "recovery_attempts": 2,
  "operator_notification_required": true
}
```

`reason` 枚举扩展：`UNCONFIRMED_ALIGNMENT | GRAVITY_LOCK_TIMEOUT | GRAVITY_LOCK_DENIED | RECOVERY_FAILED | CRITICAL_DRIFT | QUARANTINE_TIMEOUT | IDENTITY_BREACH | SCHEMING_CONFIRMED`。

---

## 9. `GRAVITY_FORECAST`
**用途**：预测在未来 K 步内达到不安全状态的概率。受 ProbGuard（DTMC）和 SafetyDrift（吸收链）启发。

### 9.1 载荷 Schema

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
  "model": "DTMC",
  "model_version": "absorbing-mc-v1",
  "confidence": 0.94
}
```

### 9.2 字段要求

| 字段 | 类型 | 必需 | 描述 |
|---|---|---|---|
| `current_state` | 枚举 | MUST | 状态机状态之一。 |
| `forecast_horizon_steps` | 整数 | MUST | K 步前瞻（默认 5）。 |
| `predicted_states` | 对象 | MUST | 未来状态的概率质量。键**必须**是六个轨道状态的子集；瞬态 `RECENTERING` 状态**可**省略（它是恢复动作，而非预测目标）。所列概率**必须**在出现的键上求和 ≈ 1.0。 |
| `predicted_violation_probability` | 数值 | MUST | P(K 步内违规)。 |
| `point_of_no_return_distance` | 整数或 null | SHOULD | 最小 k 使得 P(violate \| k) ≥ 0.5；未达到则 null。 |
| `absorbing_state_expected_arrival_steps` | 数值 | SHOULD | 期望吸收时间。 |
| `model` | 枚举 | MUST | `DTMC`、`ABSORBING_MC`、`HMM`。 |
| `model_version` | 字符串 | SHOULD | 版本化模型标识符。 |
| `confidence` | 数值 | SHOULD | `[0, 1]` 模型置信度。 |

完整 DTMC 规范见 [Forecasting_cn.md](../docs_cn/Forecasting_cn.md)。

---

## 10. `IDENTITY_VERIFICATION`
**用途**：根据 NHI 注册表、AIAP card 哈希或去中心化标识符（DID）验证 Agent 身份。

```json
{
  "agent_id_claimed": "agent_alpha",
  "identity_method": "DID",
  "identity_proof": "did:aixp:abc123",
  "verified": true,
  "failure_reason": null,
  "credentials": {
    "type": "JIT",
    "scope": ["read.own", "write.own"],
    "ttl_seconds": 60,
    "issued_at": "2026-05-19T10:00:00Z",
    "issued_by": "did:aixp:issuer-7",
    "purpose": "read agent's own task memory"
  },
  "aiap_trust_level": "T2",
  "aiap_governance_hash_verified": true,
  "recommended_action": "ALLOW"
}
```

- `identity_method` 枚举：`DID | AIAP_CARD_HASH | JWT | NHI_REGISTRY`。
- `credentials.type` 枚举：`JIT | LONG_LIVED | BEARER`。
- `recommended_action` 枚举：`ALLOW | DENY_AND_RETRY | DENY_AND_SAFE_STOP | ESCALATE_TO_T4`。
- 当 `verified` 为 `false` 时，SHOULD 携带 `failure_reason`（字符串）。

见 [Integration-ZT_cn.md](../docs_cn/Integration-ZT_cn.md)。

---

## 11. `MEMORY_QUARANTINE`
**用途**：将记忆条目标记为污染；隔离未来检索直到审查。

```json
{
  "memory_id": "mem_xyz789",
  "memory_kind": "RAG_DOC",
  "trigger_metric": "prompt_injection_classifier_score",
  "trigger_value": 0.87,
  "trigger_threshold": 0.65,
  "evidence_text": "retrieved document 中发现类指令内容",
  "quarantine_action": "ISOLATE_FROM_RETRIEVAL",
  "auto_release_after_review": false
}
```

`memory_kind` 枚举：`RAG_DOC | EPISODIC | TOOL_RESULT | INSTRUCTION_HISTORY`。

`quarantine_action` 枚举：`ISOLATE_FROM_RETRIEVAL | REDACT | DELETE | MARK_FOR_REVIEW`。

映射到 **OWASP ASI06 记忆与上下文投毒**。

---

## 12. `SCHEME_SUSPECTED`
**用途**：基于内部与外部偏离发出可能的隐蔽失对齐信号。视为**弱信号**。

```json
{
  "action_id": "<opaque-string>",
  "signals": {
    "reasoning_output_divergence": 0.62,
    "deception_classifier_score": 0.71,
    "goal_concealment_score": 0.55,
    "plan_action_mismatch": 0.40
  },
  "aggregate_confidence": 0.58,
  "recommended_action": "INCREASE_OBSERVATION",
  "operator_review_required": true
}
```

`recommended_action` 枚举：`INCREASE_OBSERVATION | LOWER_TRUST_LEVEL | GRAVITY_LOCK | INVESTIGATE`。

**重要**：`SCHEME_SUSPECTED` 事件是信息性的。**必须不**自动停止执行——Apollo Research 发现指出在隐蔽信号上激进停止可能训练规避。操作员审查是合适的响应。

---

## 13. `INTER_AGENT_DRIFT`
```json
{
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
```

`recommendation` 枚举：`MONITOR | GRAVITY_LOCK_GROUP | QUARANTINE_GROUP | DISBAND_GROUP`。

---

## 14. `CONTAINMENT_GRADUATED`
**用途**：记录容器级别变更。受 MI9 分级容器启发。

```json
{
  "previous_level": "L1",
  "new_level": "L2",
  "scope": "AGENT",
  "group_id": null,
  "trigger_event_id": "<UUIDv4>",
  "reason": "drift_severity_exceeded_threshold",
  "active_restrictions": [
    "tools_sandboxed",
    "network_egress_blocked",
    "memory_writes_quarantined"
  ],
  "auto_release_conditions": [
    "gravity_score >= 0.80 for 5 consecutive checks"
  ]
}
```

- `previous_level` / `new_level` 枚举：`L0 | L1 | L2 | L3 | L4`。
- `scope` 枚举：`AGENT | GROUP`（默认 `AGENT`）；当 `scope` 为 `GROUP` 时 MUST 携带 `group_id`。

容器级别（L0–L4）— 见 [Containment-Levels_cn.md](../docs_cn/Containment-Levels_cn.md)。

---

## 15. `REWARD_HACK_DETECTED`
**用途**：记录奖励欺骗信号的观察。**根据 2026 年 3 月研究，奖励欺骗是结构性均衡，无法完全消除**——此事件记录检测，而非预防。

```json
{
  "action_id": "<opaque-string>",
  "hack_pattern": "PROXY_METRIC_GAMING",
  "evidence": {
    "metric_optimized": "engagement_score",
    "metric_value": 0.95,
    "true_outcome_score": 0.32,
    "gaming_ratio": 2.97
  },
  "severity": "HIGH",
  "remediation": "REPORT_TO_OPERATOR"
}
```

`hack_pattern` 枚举：`PROXY_METRIC_GAMING | REWARD_TAMPERING | SPECIFICATION_GAMING | DECEPTIVE_REWARD_MAXIMIZATION`。

检测局限见 [Reward-Hacking-Limits_cn.md](../docs_cn/Reward-Hacking-Limits_cn.md)。

---

## 16. 状态机概要（6 状态）

```
STABLE_ORBIT     --G < 0.8--> DRIFT_WARNING
DRIFT_WARNING    --G < 0.5--> GRAVITY_LOCK_PENDING
GRAVITY_LOCK_PENDING --confirm--> RECENTERING
GRAVITY_LOCK_PENDING --deny/timeout--> QUARANTINED   ← 默认 fallback
QUARANTINED      --gravity_recovers--> RECENTERING
QUARANTINED      --quarantine_timeout/G<0.15--> SAFE_STOP
RECENTERING      --G≥0.8--> STABLE_ORBIT
SAFE_STOP        --终止--> (操作员介入)
```

完整状态机见 [State-Machine_cn.md](../docs_cn/State-Machine_cn.md)。

---

## 17. 合规级别

（V0.1 扩展；完整合规测试见 [Compliance_cn.md](../docs_cn/Compliance_cn.md)）

| 级别 | 必需事件 | 必需漂移 | 必需状态 | V0.2 新测试 |
|---|---|---|---|---|
| G0 | 无 | 无 | 无 | — |
| G1 | `GRAVITY_CHECK` | 无 | 仅 STABLE_ORBIT | — |
| G2 | + `GRAVITY_DRIFT` | 11 类中 ≥3 | + DRIFT_WARNING | 新漂移类型测试 |
| G3 | + `GRAVITY_LOCK`、`RECENTERING`、`SAFE_STOP` | 11 类中 ≥5 | 完整 6 状态机 | QUARANTINED 测试 |
| G4 | + `GRAVITY_FORECAST`、`CONTAINMENT_GRADUATED` | 全 11 类 | 完整 | 预测性监控测试 |
| G5 | 全部 12 事件 | 全 11 类 | TLA+/Coq 证明 | 形式化验证 |

---

## 18. 版本控制

AIZP 携带**两个**版本标识（见 [ADR-009](../adrs/adr-009-wire-version-vs-release-version.md)）：

- **`wire_version`**（整数，当前 `2`）—— 线上格式兼容契约。仅在线上不兼容变更时递增，是对端协商所依据的标识。Protobuf 包名（`aizp.wire2`）与 Schema `$id` 路径（`/schemas/wire-2/`）按它命名，因此跨文档发布保持稳定。
- **`protocol_version`**（字符串，当前 `"V0.6"`）—— 面向人/审计的发布版本。每次发布（含纯文档发布）都会推进。

规范性机理——事件词汇（12）、漂移类型（11）、状态机（6）与 Schema——**自 V0.2 起冻结于 `wire_version` 2**；V0.3–V0.6 各版本仅新增文档与哲学材料，不改变线上格式（见 [CHANGELOG.md](../CHANGELOG.md)）。

| 转换 | 性质 |
|---|---|
| V0.1 → V0.2 | `GRAVITY_CHECK.components` 载荷扩展不向后兼容；事件 5 → 12（新事件为添加性——V0.1 实现**可以**忽略）；状态 5 → 6。实现**必须**广告其接受的 `protocol_version`。 |
| V0.2 → V0.3 | 仅文档（熵/共振子理论）。线上格式不变。 |
| V0.3 → V0.4 | 仅文档（引力隐喻整合）。线上格式不变。 |
| V0.4 → V0.5 | 仅文档（共识强化引力，ADR-001/002）。线上格式不变。 |
| V0.5 → V0.6 | 仅文档（HSAW 对齐、`specification/` 拆分、ADR）。线上格式不变。 |

由于自 V0.2 起线上格式完全相同（均为 `wire_version` 2），V0.6 实现可与任意 V0.2+ 对端互操作，仅 `protocol_version` 字符串不同。省略 `wire_version` 的对端（ADR-009 之前的 V0.2 发送方）按 `wire_version` 2 处理。

---

## 19. 参考 JSON Schema

权威 Schema 位于 [`schemas/`](../schemas/)：

- `gravity-check.schema.json`（已更新）
- `gravity-drift.schema.json`（已更新支持 11 漂移类型）
- `gravity-lock.schema.json`（已更新 `fallback`）
- `recentering.schema.json`
- `safe-stop.schema.json`（已更新 `reason`）
- `gravity-forecast.schema.json`（新）
- `identity-verification.schema.json`（新）
- `memory-quarantine.schema.json`（新）
- `scheme-suspected.schema.json`（新）
- `inter-agent-drift.schema.json`（新）
- `containment-graduated.schema.json`（新）
- `reward-hack-detected.schema.json`（新）

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
