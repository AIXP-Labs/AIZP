# AIZP Registry — Canonical Enumerations

**Version**: AIZP V0.6
**Status**: Normative. This file is the **single source of truth** for AIZP enum allocations. Where any other document lists these values, this registry prevails.

Maintaining one authoritative registry prevents enum drift across documents (e.g., the OWASP ASI category names must be updated here once, not in every doc).

---

## 1. Events (12)

| # | Event | Since |
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

## 2. Drift types (11)

| # | Drift type | Category |
|---|---|---|
| 1 | `INTENT_DRIFT` | Goal alignment |
| 2 | `AUTHORITY_DRIFT` | Privilege |
| 3 | `ECONOMIC_DRIFT` | Resource |
| 4 | `SOCIAL_DRIFT` | Manipulation |
| 5 | `RECURSIVE_DRIFT` | Autonomy |
| 6 | `IDENTITY_DRIFT` | Impersonation |
| 7 | `COMPOSITIONAL_DRIFT` | Sequence |
| 8 | `SCHEMING_DRIFT` | Covert |
| 9 | `MEMORY_DRIFT` | Context |
| 10 | `TOOL_CHAIN_DRIFT` | Capability |
| 11 | `INTER_AGENT_DRIFT` | Coordination |

> Indirect Prompt Injection (IPI) is **not** a drift type; it is a cross-cutting attack vector — see [Drift-Model.md](../docs/Drift-Model.md) §8.

## 3. Orbital states (6) and thresholds

| State | Gravity Score band | Containment |
|---|---|---|
| `STABLE_ORBIT` | `G ≥ 0.80` | L0 |
| `DRIFT_WARNING` | `0.50 ≤ G < 0.80` | L1 |
| `GRAVITY_LOCK_PENDING` | `0.30 ≤ G < 0.50` | L2 |
| `QUARANTINED` | `0.15 ≤ G < 0.30` | L2/L3 |
| `RECENTERING` | recovery | L1/L2 |
| `SAFE_STOP` | `G < 0.15` | L4 |

## 4. Containment levels (5)

| Level | Name |
|---|---|
| `L0` | Free Execution |
| `L1` | Enhanced Monitoring |
| `L2` | Sandboxed Execution |
| `L3` | Restricted Execution |
| `L4` | Halt |

## 5. Compliance levels (6)

| Level | Headline |
|---|---|
| `G0` | No Gravity (baseline) |
| `G1` | Basic Check |
| `G2` | Drift Detection (≥3 of 11) |
| `G3` | Re-Centering + Quarantine |
| `G4` | Predictive + Auditable |
| `G5` | Formal Proofs |

## 6. `SAFE_STOP.reason` codes

`UNCONFIRMED_ALIGNMENT` · `GRAVITY_LOCK_TIMEOUT` · `GRAVITY_LOCK_DENIED` · `RECOVERY_FAILED` · `CRITICAL_DRIFT` · `QUARANTINE_TIMEOUT` · `IDENTITY_BREACH` · `SCHEMING_CONFIRMED`

## 7. `REWARD_HACK_DETECTED.hack_pattern`

`PROXY_METRIC_GAMING` · `REWARD_TAMPERING` · `SPECIFICATION_GAMING` · `DECEPTIVE_REWARD_MAXIMIZATION`

## 8. OWASP ASI 2026 ↔ AIZP mapping (authoritative)

| OWASP ASI (2026) | AIZP primary defense |
|---|---|
| ASI01 Agent Goal Hijack | `INTENT_DRIFT`, `SCHEMING_DRIFT`, IPI vector |
| ASI02 Tool Misuse & Exploitation | `TOOL_CHAIN_DRIFT`, `COMPOSITIONAL_DRIFT`, `AUTHORITY_DRIFT` |
| ASI03 Identity & Privilege Abuse | `IDENTITY_VERIFICATION`, `IDENTITY_DRIFT`, `AUTHORITY_DRIFT` |
| ASI04 Agentic Supply Chain Vulnerabilities | description pinning, component verification (partial) |
| ASI05 Unexpected Code Execution (RCE) | containment L3+ (out-of-band; partial) |
| ASI06 Memory & Context Poisoning | `MEMORY_DRIFT`, `MEMORY_QUARANTINE` |
| ASI07 Insecure Inter-Agent Communication | `INTER_AGENT_DRIFT`, ANS, A2A bridge |
| ASI08 Cascading Failures | `RECURSIVE_DRIFT`, `ECONOMIC_DRIFT`, containment |
| ASI09 Human-Agent Trust Exploitation | `SCHEMING_DRIFT`, `SOCIAL_DRIFT`, `GRAVITY_LOCK` |
| ASI10 Rogue Agents | full drift → re-center → `SAFE_STOP` loop |

> Official source: OWASP Top 10 for Agentic Applications 2026 (genai.owasp.org). Full mapping: [OWASP-Agentic-Top10-Mapping.md](../docs/Compliance-Profiles/OWASP-Agentic-Top10-Mapping.md).

## 9. Auxiliary payload enums

The per-event payload fields below are also normative; this registry is their single source of truth (the JSON Schemas in [`../schemas/`](../schemas/) and the [`proto`](proto/aizp.proto) MUST agree with this table). `risk_level`/`severity` and `aiap_trust_level` are shared across multiple events.

| Field | Event(s) | Values |
|---|---|---|
| `risk_level` / `severity` | `GRAVITY_CHECK`, `GRAVITY_DRIFT`, `INTER_AGENT_DRIFT`, `REWARD_HACK_DETECTED` | `LOW` · `MEDIUM` · `HIGH` · `CRITICAL` |
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
