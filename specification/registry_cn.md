# AIZP 注册表 — 规范性枚举

**版本**：AIZP V0.6
**状态**：规范性。本文件是 AIZP 枚举分配的**单一权威来源**。其他文档列出这些值时，以本注册表为准。

维护单一权威注册表可防止枚举跨文档漂移（例如 OWASP ASI 分类名只需在此更新一次，而非每个文档）。

---

## 1. 事件（12）

| # | 事件 | 起始 |
|---|---|---|
| 1 | `GRAVITY_CHECK` | V0.1 |
| 2 | `GRAVITY_DRIFT` | V0.1 |
| 3 | `GRAVITY_LOCK` | V0.1 |
| 4 | `RECENTERING` | V0.1 |
| 5 | `SAFE_STOP` | V0.1 |
| 6 | `GRAVITY_FORECAST` | V0.2 |
| 7 | `IDENTITY_VERIFICATION` | V0.2 |
| 8 | `MEMORY_QUARANTINE` | V0.2 |
| 9 | `SCHEME_SUSPECTED` | V0.2 |
| 10 | `INTER_AGENT_DRIFT` | V0.2 |
| 11 | `CONTAINMENT_GRADUATED` | V0.2 |
| 12 | `REWARD_HACK_DETECTED` | V0.2 |

## 2. 漂移类型（11）

| # | 漂移类型 | 类别 |
|---|---|---|
| 1 | `INTENT_DRIFT` | 目标对齐 |
| 2 | `AUTHORITY_DRIFT` | 特权 |
| 3 | `ECONOMIC_DRIFT` | 资源 |
| 4 | `SOCIAL_DRIFT` | 操纵 |
| 5 | `RECURSIVE_DRIFT` | 自主 |
| 6 | `IDENTITY_DRIFT` | 冒充 |
| 7 | `COMPOSITIONAL_DRIFT` | 序列 |
| 8 | `SCHEMING_DRIFT` | 隐蔽 |
| 9 | `MEMORY_DRIFT` | 上下文 |
| 10 | `TOOL_CHAIN_DRIFT` | 能力 |
| 11 | `INTER_AGENT_DRIFT` | 协调 |

> 间接提示注入（IPI）**不是**漂移类型；它是跨切攻击向量——见 [Drift-Model_cn.md](../docs_cn/Drift-Model_cn.md) §8。

## 3. 轨道状态（6）与阈值

| 状态 | 引力分数带 | 容器 |
|---|---|---|
| `STABLE_ORBIT` | `G ≥ 0.80` | L0 |
| `DRIFT_WARNING` | `0.50 ≤ G < 0.80` | L1 |
| `GRAVITY_LOCK_PENDING` | `0.30 ≤ G < 0.50` | L2 |
| `QUARANTINED` | `0.15 ≤ G < 0.30` | L2/L3 |
| `RECENTERING` | 恢复 | L1/L2 |
| `SAFE_STOP` | `G < 0.15` | L4 |

## 4. 容器级别（5）

| 级别 | 名称 |
|---|---|
| `L0` | 自由执行 |
| `L1` | 增强监控 |
| `L2` | 沙箱执行 |
| `L3` | 受限执行 |
| `L4` | 停止 |

## 5. 合规级别（6）

| 级别 | 要点 |
|---|---|
| `G0` | 无引力（基线）|
| `G1` | 基础检查 |
| `G2` | 漂移检测（11 中 ≥3）|
| `G3` | 重新归心 + 隔离 |
| `G4` | 预测 + 可审计 |
| `G5` | 形式化证明 |

## 6. `SAFE_STOP.reason` 代码

`UNCONFIRMED_ALIGNMENT` · `GRAVITY_LOCK_TIMEOUT` · `GRAVITY_LOCK_DENIED` · `RECOVERY_FAILED` · `CRITICAL_DRIFT` · `QUARANTINE_TIMEOUT` · `IDENTITY_BREACH` · `SCHEMING_CONFIRMED`

## 7. `REWARD_HACK_DETECTED.hack_pattern`

`PROXY_METRIC_GAMING` · `REWARD_TAMPERING` · `SPECIFICATION_GAMING` · `DECEPTIVE_REWARD_MAXIMIZATION`

## 8. OWASP ASI 2026 ↔ AIZP 映射（权威）

| OWASP ASI（2026）| AIZP 主要防御 |
|---|---|
| ASI01 Agent 目标劫持 | `INTENT_DRIFT`、`SCHEMING_DRIFT`、IPI 向量 |
| ASI02 工具滥用与利用 | `TOOL_CHAIN_DRIFT`、`COMPOSITIONAL_DRIFT`、`AUTHORITY_DRIFT` |
| ASI03 身份与特权滥用 | `IDENTITY_VERIFICATION`、`IDENTITY_DRIFT`、`AUTHORITY_DRIFT` |
| ASI04 Agentic 供应链漏洞 | 描述钉住、组件验证（部分）|
| ASI05 意外代码执行（RCE）| 容器 L3+（带外；部分）|
| ASI06 记忆与上下文投毒 | `MEMORY_DRIFT`、`MEMORY_QUARANTINE` |
| ASI07 不安全的 Agent 间通信 | `INTER_AGENT_DRIFT`、ANS、A2A 桥 |
| ASI08 级联失败 | `RECURSIVE_DRIFT`、`ECONOMIC_DRIFT`、容器 |
| ASI09 人机信任利用 | `SCHEMING_DRIFT`、`SOCIAL_DRIFT`、`GRAVITY_LOCK` |
| ASI10 失控 Agent | 完整漂移 → 重新归心 → `SAFE_STOP` 循环 |

> 官方来源：OWASP Top 10 for Agentic Applications 2026（genai.owasp.org）。完整映射：[OWASP-Agentic-Top10-Mapping_cn.md](../docs_cn/Compliance-Profiles/OWASP-Agentic-Top10-Mapping_cn.md)。

## 9. 辅助载荷枚举

以下各事件载荷字段同为规范性内容；本注册表是其单一事实来源（[`../schemas/`](../schemas/) 中的 JSON Schema 与 [`proto`](proto/aizp.proto) 必须与本表一致）。`risk_level`/`severity` 与 `aiap_trust_level` 在多个事件间共享。

| 字段 | 事件 | 取值 |
|---|---|---|
| `risk_level` / `severity` | `GRAVITY_CHECK`、`GRAVITY_DRIFT`、`INTER_AGENT_DRIFT`、`REWARD_HACK_DETECTED` | `LOW` · `MEDIUM` · `HIGH` · `CRITICAL` |
| `aiap_trust_level` | `IDENTITY_VERIFICATION` | `T1` · `T2` · `T3` · `T4` |
| `components.intent_method` | `GRAVITY_CHECK` | `JSD` · `COSINE` · `CUSTOM` |
| `status` | `GRAVITY_LOCK` | `PENDING_CONFIRMATION` · `CONFIRMED` · `DENIED` · `TIMEOUT` |
| `fallback` | `GRAVITY_LOCK` | `QUARANTINED` · `SAFE_STOP` · `RECENTERING` |
| `action` | `RECENTERING` | `RESTORE_HSAW_ALIGNMENT` · `REQUEST_CLARIFICATION` · `RELOAD_USER_INTENT` |
| `recovery_strategy` | `RECENTERING` | `BACKTRACK_AND_CONFIRM` · `RELOAD_GOAL` · `REQUEST_CLARIFICATION` · `RESET_TO_STABLE_CHECKPOINT` |
| `model` | `GRAVITY_FORECAST` | `DTMC` · `ABSORBING_MC` · `HMM` |
| `identity_method` | `IDENTITY_VERIFICATION` | `DID` · `AIAP_CARD_HASH` · `JWT` · `NHI_REGISTRY` |
| `credentials.type` | `IDENTITY_VERIFICATION` | `JIT` · `LONG_LIVED` · `BEARER` |
| `recommended_action` | `IDENTITY_VERIFICATION` | `ALLOW` · `DENY_AND_RETRY` · `DENY_AND_SAFE_STOP` · `ESCALATE_TO_T4` |
| `memory_kind` | `MEMORY_QUARANTINE` | `RAG_DOC` · `EPISODIC` · `TOOL_RESULT` · `INSTRUCTION_HISTORY` |
| `quarantine_action` | `MEMORY_QUARANTINE` | `ISOLATE_FROM_RETRIEVAL` · `REDACT` · `DELETE` · `MARK_FOR_REVIEW` |
| `recommended_action` | `SCHEME_SUSPECTED` | `INCREASE_OBSERVATION` · `LOWER_TRUST_LEVEL` · `GRAVITY_LOCK` · `INVESTIGATE` |
| `recommendation` | `INTER_AGENT_DRIFT` | `MONITOR` · `GRAVITY_LOCK_GROUP` · `QUARANTINE_GROUP` · `DISBAND_GROUP` |
| `scope` | `CONTAINMENT_GRADUATED` | `AGENT` · `GROUP` |
| `remediation` | `REWARD_HACK_DETECTED` | `REPORT_TO_OPERATOR` · `LOWER_TRUST_LEVEL` · `INCREASE_OBSERVATION` · `SAFE_STOP` |

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
