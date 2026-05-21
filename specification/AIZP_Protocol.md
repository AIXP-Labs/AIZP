# AIZP Specification

**Version**: AIZP V0.6
**Status**: Experimental
**Conformance Keywords**: "MUST", "SHOULD", "MAY" per [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

---

## 0. Document Overview

This document specifies the AIZP protocol events, their schemas, the state machine transitions, and conformance requirements.

**Current shape** (event vocabulary and state machine frozen since V0.2; see §18 and [CHANGELOG.md](../CHANGELOG.md)):
- **12** events (the original 5 plus `GRAVITY_FORECAST`, `IDENTITY_VERIFICATION`, `MEMORY_QUARANTINE`, `SCHEME_SUSPECTED`, `INTER_AGENT_DRIFT`, `CONTAINMENT_GRADUATED`, `REWARD_HACK_DETECTED`).
- **6**-state machine (the original 5 plus `QUARANTINED`).
- **11** drift types.

Related: [Gravity-Model.md](../docs/Gravity-Model.md), [Drift-Model.md](../docs/Drift-Model.md), [State-Machine.md](../docs/State-Machine.md), [Forecasting.md](../docs/Forecasting.md), [Containment-Levels.md](../docs/Containment-Levels.md), [Integration-AISOP.md](../docs/Integration-AISOP.md).

---

## 1. Axiom 0: HSAW, the Gravity Center

### 1.1 What HSAW Is

**HSAW (Human Sovereignty and Wellbeing)** is the **Axiom 0** of the AIXP ecosystem — an inviolable design principle independently adopted as the foundational axiom by AISOP, AIAP, AIBP, AILP, AIVP, and AIRP. AIZP is the runtime dynamics layer that keeps AI behavior gravitationally anchored to it.

> **Axiom 0 — Human Sovereignty and Wellbeing**
> The highest-level, inviolable constraint on all AI behavior. No optimization objective, autonomous decision, system evolution, social agreement, economic pressure, or governance vote may compromise human decision-making authority over consequential actions, or act against human wellbeing.

HSAW operates on **two dimensions**:

- **Sovereignty** — the human retains decision-making authority: the right to approve/reject, understand, intervene in, revoke, reverse, and sever consequential AI actions and connections.
- **Wellbeing** — the AI actively protects human interests: it must not harm even if instructed, must warn of detected harm, must preserve the human's ability to course-correct, must not coerce, and must protect human privacy above all.

It carries **four inviolable properties**: it **cannot be bypassed**, **cannot be modified**, **cannot be overridden**, and **propagates immutably** to subsystems.

> **AIZP does not define HSAW.** HSAW's full content — its definition, the scope of "consequential" actions, the value hierarchy, and its enforcement patterns — is owned by the HSAW specification ([hsaw.dev](https://hsaw.dev)). AIZP treats HSAW as upstream and immovable (see [ADR-002](../adrs/adr-002-hsaw-axiom-0-immovable.md)); it operationalizes HSAW as the gravity center, it does not redefine it.

### 1.2 HSAW as the Gravity Center

In AIZP, HSAW is the **fixed, axiomatic gravity center** of behavioral space — the target distribution `Q_HSAW` that the Gravity Score `G` measures orbital distance to. AI behavior proactively orbits HSAW; **drift** is outward motion away from it; **escape velocity** (`G < 0.15`) is decoupling and triggers `SAFE_STOP`.

### 1.3 Value Hierarchy (inherited from HSAW §3.5)

AIZP does not define its own value hierarchy. When values conflict, the canonical HSAW order applies:

```
1. Human Physical Safety   (highest)
2. Human Privacy
3. Human Economic Autonomy
4. Human Decision Authority
5. System Transparency
6. System Auditability
7. System Performance      (lowest)
```

**Privacy overrides Transparency**: AIZP never logs or surfaces human personal data in pursuit of observability.

### 1.4 Axiom 0 Precedence

When any AIZP rule, threshold, or weight conflicts with HSAW, **HSAW wins unconditionally**. An agent forced to choose between proceeding and protecting human sovereignty MUST halt toward the center (`SAFE_STOP`) — never optimize away from it.

---

## 2. Common Event Envelope

All AIZP events MUST share a common envelope:

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
  "payload": { /* event-type-specific */ }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `protocol` | string | MUST | Always `"AIZP"`. |
| `protocol_version` | string | MUST | Release version, e.g. `"V0.6"`. Human/audit-facing. |
| `wire_version` | integer | SHOULD | `2` — the wire-format compatibility contract (frozen since V0.2). Peers negotiate on this, not `protocol_version`. See §18 and [ADR-009](../adrs/adr-009-wire-version-vs-release-version.md). |
| `event` | string | MUST | One of 12 event types (see §3). |
| `event_id` | string (UUIDv4) | MUST | Unique per event. |
| `timestamp` | string (RFC3339 UTC) | MUST | Wall-clock time. |
| `agent_id` | string | MUST | Opaque agent identifier. |
| `session_id` | string | MUST | Opaque session identifier. |
| `payload` | object | MUST | Event-type-specific. |

---

## 3. Event Catalog (12 events)

| # | Event | Purpose | New in |
|---|---|---|---|
| 1 | `GRAVITY_CHECK` | Verify HSAW anchoring | V0.1 |
| 2 | `GRAVITY_DRIFT` | Detect behavioral deviation | V0.1 |
| 3 | `GRAVITY_LOCK` | Require human authorization | V0.1 |
| 4 | `RECENTERING` | Restore alignment | V0.1 |
| 5 | `SAFE_STOP` | Terminate unsafe behavior | V0.1 |
| 6 | **`GRAVITY_FORECAST`** | Predict future violation probability | **V0.2** |
| 7 | **`IDENTITY_VERIFICATION`** | NHI / DID identity check | **V0.2** |
| 8 | **`MEMORY_QUARANTINE`** | Context poisoning detected | **V0.2** |
| 9 | **`SCHEME_SUSPECTED`** | Covert misalignment signal | **V0.2** |
| 10 | **`INTER_AGENT_DRIFT`** | Multi-agent coordination drift | **V0.2** |
| 11 | **`CONTAINMENT_GRADUATED`** | Containment level changed | **V0.2** |
| 12 | **`REWARD_HACK_DETECTED`** | Reward signal exploitation | **V0.2** |

---

## 4. `GRAVITY_CHECK`

**Payload** — carries method markers for audit (since V0.2).

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

Required fields per [Gravity-Model.md](../docs/Gravity-Model.md) §8: `intent_method`, `intent_jsd`, `intent_n_samples`, `drift_mann_whitney_p` (for EU AI Act Art 12 audit).

---

## 5. `GRAVITY_DRIFT` (11 drift types)

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

`drift_types` enum (11 types):
```
INTENT_DRIFT | AUTHORITY_DRIFT | ECONOMIC_DRIFT | SOCIAL_DRIFT |
RECURSIVE_DRIFT | IDENTITY_DRIFT |
COMPOSITIONAL_DRIFT | SCHEMING_DRIFT | MEMORY_DRIFT |
TOOL_CHAIN_DRIFT | INTER_AGENT_DRIFT
```

---

## 6. `GRAVITY_LOCK`

(unchanged structure from V0.1; threshold band tightened)

Threshold: triggered at `0.30 ≤ G < 0.50`.

```json
{
  "action_id": "<opaque-string>",
  "action_descriptor": "<short-string>",
  "authorization_required": true,
  "status": "PENDING_CONFIRMATION",
  "confirmation_primitive": "sys.io.confirm",
  "timeout_seconds": 300,
  "confirmation_prompt": "Authorize transfer of $5000 to recipient X?",
  "fallback": "QUARANTINED"
}
```

`fallback` enum: `QUARANTINED | SAFE_STOP | RECENTERING`. Default fallback (since V0.2): `QUARANTINED` (graduated containment instead of full stop). See [Containment-Levels.md](../docs/Containment-Levels.md).

---

## 7. `RECENTERING`
**Purpose**: Restore HSAW alignment after a drift or lock, recording the recovery strategy and the gravity-score delta. (Structure unchanged from V0.1.)

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

- `action` enum: `RESTORE_HSAW_ALIGNMENT | REQUEST_CLARIFICATION | RELOAD_USER_INTENT`.
- `recovery_strategy` enum: `BACKTRACK_AND_CONFIRM | RELOAD_GOAL | REQUEST_CLARIFICATION | RESET_TO_STABLE_CHECKPOINT`.

Required: `action`, `trigger_event_id`, `recovery_strategy`.

---

## 8. `SAFE_STOP`

(unchanged from V0.1, but threshold tightened to `G < 0.15`)

```json
{
  "reason": "CRITICAL_DRIFT",
  "trigger_event_id": "<UUIDv4>",
  "gravity_score_at_stop": 0.10,
  "recovery_attempts": 2,
  "operator_notification_required": true
}
```

`reason` enum extended: `UNCONFIRMED_ALIGNMENT | GRAVITY_LOCK_TIMEOUT | GRAVITY_LOCK_DENIED | RECOVERY_FAILED | CRITICAL_DRIFT | QUARANTINE_TIMEOUT | IDENTITY_BREACH | SCHEMING_CONFIRMED`.

---

## 9. `GRAVITY_FORECAST`
**Purpose**: Predict the probability of reaching unsafe states within K future steps. Inspired by ProbGuard (DTMC) and SafetyDrift (absorbing chains).

### 9.1 Payload schema

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

### 9.2 Field requirements

| Field | Type | Required | Description |
|---|---|---|---|
| `current_state` | enum | MUST | One of state machine states. |
| `forecast_horizon_steps` | integer | MUST | K-step lookahead (default 5). |
| `predicted_states` | object | MUST | Probability mass over future states. Keys MUST be a subset of the six orbital states; the transient `RECENTERING` state MAY be omitted (it is a recovery action, not a forecast target). The listed probabilities MUST sum to ≈ 1.0 over the keys present. |
| `predicted_violation_probability` | number | MUST | P(violate within K). |
| `point_of_no_return_distance` | integer or null | SHOULD | Smallest k such that P(violate \| k) ≥ 0.5; null if not reached. |
| `absorbing_state_expected_arrival_steps` | number | SHOULD | Expected time-to-absorption. |
| `model` | enum | MUST | `DTMC`, `ABSORBING_MC`, `HMM`. |
| `model_version` | string | SHOULD | Versioned model identifier. |
| `confidence` | number | SHOULD | Model confidence in `[0, 1]`. |

See [Forecasting.md](../docs/Forecasting.md) for the full DTMC specification.

---

## 10. `IDENTITY_VERIFICATION`
**Purpose**: Verify agent identity against NHI registry, AIAP card hash, or Decentralized Identifier (DID).

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

- `identity_method` enum: `DID | AIAP_CARD_HASH | JWT | NHI_REGISTRY`.
- `credentials.type` enum: `JIT | LONG_LIVED | BEARER`.
- `recommended_action` enum: `ALLOW | DENY_AND_RETRY | DENY_AND_SAFE_STOP | ESCALATE_TO_T4`.
- `failure_reason` (string) SHOULD be present when `verified` is `false`.

See [Integration-ZT.md](../docs/Integration-ZT.md).

---

## 11. `MEMORY_QUARANTINE`
**Purpose**: Mark a memory entry as contaminated; isolate from future retrievals until reviewed.

```json
{
  "memory_id": "mem_xyz789",
  "memory_kind": "RAG_DOC",
  "trigger_metric": "prompt_injection_classifier_score",
  "trigger_value": 0.87,
  "trigger_threshold": 0.65,
  "evidence_text": "instruction-like content found in retrieved document",
  "quarantine_action": "ISOLATE_FROM_RETRIEVAL",
  "auto_release_after_review": false
}
```

`memory_kind` enum: `RAG_DOC | EPISODIC | TOOL_RESULT | INSTRUCTION_HISTORY`.

`quarantine_action` enum: `ISOLATE_FROM_RETRIEVAL | REDACT | DELETE | MARK_FOR_REVIEW`.

Maps to **OWASP ASI06 Memory & Context Poisoning**.

---

## 12. `SCHEME_SUSPECTED`
**Purpose**: Signal possible covert misalignment based on internal-vs-external divergence. Treated as a **weak signal**.

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

`recommended_action` enum: `INCREASE_OBSERVATION | LOWER_TRUST_LEVEL | GRAVITY_LOCK | INVESTIGATE`.

**Important**: a `SCHEME_SUSPECTED` event is informational. It MUST NOT automatically halt execution — Apollo Research findings indicate that aggressive halting on scheming signals can train evasion. Operator review is the appropriate response.

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

`recommendation` enum: `MONITOR | GRAVITY_LOCK_GROUP | QUARANTINE_GROUP | DISBAND_GROUP`.

---

## 14. `CONTAINMENT_GRADUATED`
**Purpose**: Record a containment-level change. Inspired by MI9 graduated containment.

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

- `previous_level` / `new_level` enum: `L0 | L1 | L2 | L3 | L4`.
- `scope` enum: `AGENT | GROUP` (default `AGENT`); `group_id` MUST be present when `scope` is `GROUP`.

Containment levels (L0–L4) — see [Containment-Levels.md](../docs/Containment-Levels.md).

---

## 15. `REWARD_HACK_DETECTED`
**Purpose**: Record observation of reward hacking signals. **Per March 2026 research, reward hacking is a structural equilibrium and cannot be fully eliminated** — this event records detection, not prevention.

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

`hack_pattern` enum: `PROXY_METRIC_GAMING | REWARD_TAMPERING | SPECIFICATION_GAMING | DECEPTIVE_REWARD_MAXIMIZATION`.

See [Reward-Hacking-Limits.md](../docs/Reward-Hacking-Limits.md) for limits of detection.

---

## 16. State Machine Summary (6 states)

```
STABLE_ORBIT     --G < 0.8--> DRIFT_WARNING
DRIFT_WARNING    --G < 0.5--> GRAVITY_LOCK_PENDING
GRAVITY_LOCK_PENDING --confirm--> RECENTERING
GRAVITY_LOCK_PENDING --deny/timeout--> QUARANTINED   ← default fallback
QUARANTINED      --gravity_recovers--> RECENTERING
QUARANTINED      --quarantine_timeout/G<0.15--> SAFE_STOP
RECENTERING      --G≥0.8--> STABLE_ORBIT
SAFE_STOP        --terminal--> (operator intervention)
```

Full state machine in [State-Machine.md](../docs/State-Machine.md).

---

## 17. Conformance Levels

(extended from V0.1; see [Compliance.md](../docs/Compliance.md) for full conformance tests)

| Level | Required events | Required drifts | Required state | New tests in V0.2 |
|---|---|---|---|---|
| G0 | none | none | none | — |
| G1 | `GRAVITY_CHECK` | none | STABLE_ORBIT only | — |
| G2 | + `GRAVITY_DRIFT` | ≥3 of 11 types | + DRIFT_WARNING | new drift types tested |
| G3 | + `GRAVITY_LOCK`, `RECENTERING`, `SAFE_STOP` | ≥5 of 11 | full 6-state machine | QUARANTINED tested |
| G4 | + `GRAVITY_FORECAST`, `CONTAINMENT_GRADUATED` | all 11 | full | predictive monitoring tested |
| G5 | all 12 events | all 11 | TLA+/Coq proof | formal verification |

---

## 18. Versioning

AIZP carries **two** version identifiers (see [ADR-009](../adrs/adr-009-wire-version-vs-release-version.md)):

- **`wire_version`** (integer, currently `2`) — the wire-format compatibility contract. It bumps only on a wire-incompatible change and is the identifier peers negotiate on. The Protobuf package (`aizp.wire2`) and schema `$id` paths (`/schemas/wire-2/`) are named for *this*, so they stay stable across documentation releases.
- **`protocol_version`** (string, currently `"V0.6"`) — the human/audit-facing release version. It advances every release, including documentation-only ones.

The normative machinery — event vocabulary (12), drift types (11), state machine (6), and schemas — has been **frozen at `wire_version` 2 since V0.2**; releases V0.3–V0.6 add documentation and philosophical material without changing the wire format (see [CHANGELOG.md](../CHANGELOG.md)).

| Transition | Nature |
|---|---|
| V0.1 → V0.2 | Backward-incompatible payload extensions in `GRAVITY_CHECK.components`; 5 → 12 events (new events additive — V0.1 implementations MAY ignore them); 5 → 6 states. Implementations MUST advertise the `protocol_version` they accept. |
| V0.2 → V0.3 | Documentation only (entropy/resonance sub-theories). Wire format unchanged. |
| V0.3 → V0.4 | Documentation only (gravity-metaphor consolidation). Wire format unchanged. |
| V0.4 → V0.5 | Documentation only (consensus-reinforced gravity, ADR-001/002). Wire format unchanged. |
| V0.5 → V0.6 | Documentation only (HSAW alignment, `specification/` split, ADRs). Wire format unchanged. |

Because the wire format is identical from V0.2 onward (all `wire_version` 2), a V0.6 implementation interoperates with any V0.2+ peer; only the `protocol_version` string differs. Peers that omit `wire_version` (pre-ADR-009 V0.2 senders) are treated as `wire_version` 2.

---

## 19. Reference JSON Schemas

Authoritative schemas in [`schemas/`](../schemas/):

- `gravity-check.schema.json` (updated)
- `gravity-drift.schema.json` (updated for 11 drift types)
- `gravity-lock.schema.json` (updated `fallback`)
- `recentering.schema.json`
- `safe-stop.schema.json` (updated `reason`)
- `gravity-forecast.schema.json` (new)
- `identity-verification.schema.json` (new)
- `memory-quarantine.schema.json` (new)
- `scheme-suspected.schema.json` (new)
- `inter-agent-drift.schema.json` (new)
- `containment-graduated.schema.json` (new)
- `reward-hack-detected.schema.json` (new)

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
