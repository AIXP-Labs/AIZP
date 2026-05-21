# Compliance Profile: NIST AI RMF Mapping

**Version**: AIZP V0.6 (new chapter)
**NIST AI RMF**: 1.0 (2023) + Agentic Profile (4Q2026 release expected)

This document maps AIZP to NIST AI Risk Management Framework's Govern / Map / Measure / Manage functions.

---

## 1. NIST AI RMF Overview

NIST AI RMF defines four core functions for AI risk management:

| Function | Goal |
|---|---|
| **GOVERN** | Establish AI governance structures, policies, roles |
| **MAP** | Identify and contextualize AI risks |
| **MEASURE** | Quantitatively assess identified risks |
| **MANAGE** | Treat, monitor, and mitigate risks |

An **NIST AI RMF Agentic AI Profile (designation TBD, expected ~Q4 2026)** is anticipated to address the four structural gaps identified in AI RMF 1.0 for autonomous agents. AIZP V0.6 is designed to fit this profile.

---

## 2. GOVERN Function

NIST AI RMF Govern: organizational structures and policies.

| GOVERN sub-function | AIZP contribution |
|---|---|
| GV 1.1 — Legal & regulatory requirements | AIZP compliance profiles (EU AI Act, ISO 42001, OWASP) |
| GV 1.2 — Trustworthiness characteristics | HSAW alignment + AIZP gravity metric |
| GV 3.1 — Roles & responsibilities | AIAP T1–T4 + AIAP T4 escalation paths |
| GV 4.1 — Documented procedures | AIZP specification + per-event Schema |
| GV 4.3 — Workforce training | Implementer-Guide + FAQ + Threat-Model |
| GV 5 — External stakeholder engagement | Standard event format enables third-party audit |
| GV 6.1 — Risk monitoring | All 12 AIZP events |

### 2.1 New body: Agentic AI Committee

AIZP recommends establishing a standing agentic-AI governance body. AIZP deployments SHOULD include:

- A standing Agentic AI Committee with authority over agent compliance levels.
- Quarterly review of `SAFE_STOP` events and `REWARD_HACK_DETECTED` events.
- Authority to upgrade/downgrade agent AIAP trust levels based on drift history.

---

## 3. MAP Function

MAP: identify and contextualize risks.

| MAP sub-function | AIZP contribution |
|---|---|
| MP 1.1 — Context of use | Per-agent AIAP card + declared goals |
| MP 2.1 — Use cases identified | AIBP message types + AIAP program declarations |
| MP 2.2 — Potential harms catalogued | Threat-Model.md covers 10 threats + OWASP ASI01-ASI10 |
| MP 3 — Risks characterized | 11 drift types + reward hacking patterns |
| MP 5 — Impact assessment | Risk levels in `GRAVITY_CHECK` (LOW/MEDIUM/HIGH/CRITICAL) |

### 3.1 Risk taxonomy

AIZP risk categories align with NIST RMF's threat-source-event-consequence model:

```
Threat source: adversarial input | model failure | misconfiguration | NHI compromise
Threat event: drift, scheming, reward hacking, identity breach, memory poisoning
AIZP event: GRAVITY_DRIFT, SCHEME_SUSPECTED, REWARD_HACK_DETECTED, IDENTITY_VERIFICATION failed, MEMORY_QUARANTINE
Consequence: financial loss, privacy breach, safety harm, ethical harm
Control: GRAVITY_LOCK, RECENTERING, QUARANTINED, SAFE_STOP
```

---

## 4. MEASURE Function

MEASURE: quantitatively assess risks.

| MEASURE sub-function | AIZP contribution |
|---|---|
| MS 1 — Identified for measurement | Gravity Score + 11 drift severity values |
| MS 2.1 — Trustworthiness characteristics | Bounded [0, 1] gravity_score per action |
| MS 2.5 — Continuous monitoring | Per-action + per-N-action drift detection |
| MS 2.6 — Trustworthiness tracking | Time-series gravity_score histogram (G4) |
| MS 3 — Test effectiveness | Compliance tests G1-G5 conformance |
| MS 4 — Feedback for improvement | False-positive feedback loop (Drift-Model §6) |

### 4.1 Quantitative metrics for measurement

AIZP exports OTel metrics enabling NIST MEASURE evaluation:

```
aizp.gravity_score{state}           — distribution of alignment quality
aizp.gravity_drift.count{type}      — drift type frequency
aizp.safe_stop.count{reason}        — incident rate
aizp.gravity_lock.confirmation_rate — operator engagement
```

For NIST MS 2.7 (security & resilience), AIZP also exports:

```
aizp.identity_verification.fail.count
aizp.memory_quarantine.count{kind}
aizp.reward_hack_detected.count{pattern}
```

---

## 5. MANAGE Function

MANAGE: treat, monitor, mitigate identified risks.

| MANAGE sub-function | AIZP contribution |
|---|---|
| MG 1 — Risk treatment plans | Containment levels L0–L4 |
| MG 1.3 — Trade-off documented | Reward-Hacking-Limits.md explicit limits |
| MG 2 — Risk mitigation actions | `RECENTERING`, `GRAVITY_LOCK`, `QUARANTINED`, `SAFE_STOP` |
| MG 3.1 — Stakeholder communication | Operator notifications + escalation events |
| MG 4 — Implementation of plans | State machine enforces decisions |

### 5.1 Risk treatment matrix

| Risk severity | AIZP response | Mapped containment |
|---|---|---|
| LOW drift | Log only | L0 → L1 |
| MEDIUM drift | Enhanced monitoring | L1 |
| HIGH drift | Human confirmation | L2 |
| CRITICAL drift | Graduated containment then halt | L2 → L3 → L4 |
| Reward hacking detected | Operator review (not auto-halt) | L1 (preserves data) |
| Identity breach | Immediate halt | L4 |

---

## 6. AIZP Compliance Level ↔ NIST RMF Maturity

Suggested mapping between AIZP G-levels and NIST RMF organizational maturity:

| AIZP G-level | NIST RMF maturity |
|---|---|
| G1 | Initial monitoring (logs exist) |
| G2 | Documented risk identification |
| G3 | Standardized risk management (with human-in-loop) |
| G4 | Quantitative measurement + continuous improvement |
| G5 | Optimized governance (formal verification) |

---

## 7. NIST AI RMF Agentic AI Profile (designation TBD, expected ~Q4 2026)

The NIST AI RMF Agentic AI Profile (designation TBD, expected ~Q4 2026) is anticipated to address four agentic AI gaps in AI RMF 1.0:

| Gap | AIZP V0.6 closes via |
|---|---|
| 1. Predictable behavior envelope | DTMC forecasting + 11 drift types |
| 2. Defined operational boundaries | AIAP scopes + JIT credentials + containment levels |
| 3. Continuous authorization | Per-action GRAVITY_CHECK + identity verification |
| 4. Multi-agent coordination | INTER_AGENT_DRIFT + Multi-Agent-Coordination.md |

When the NIST AI RMF Agentic AI Profile is officially released, AIZP V0.6 will update this mapping with concrete sub-function alignments.

---

## 8. Reference: AAGATE

The AAGATE platform (arxiv 2510.25863) implements NIST AI RMF Govern/Map/Measure/Manage in a Kubernetes-native control plane. AIZP V0.6 is compatible with AAGATE — AIZP events can flow into AAGATE's behavioral analytics pipeline (Qdrant + UEBA + Kafka).

---

## 9. Conformance Test Mapping

When implementing AIZP for NIST AI RMF alignment, run these tests:

| NIST Function | AIZP Compliance Test |
|---|---|
| MAP — risks identified | G2-T1 through G2-T5 (all 11 drift detection tests) |
| MEASURE — quantitative | G4 audit log query tests |
| MANAGE — control effective | G3 state machine tests (lock/quarantine/recenter/stop) |
| GOVERN — policies enforced | Compliance Test G3-T6 (AIAP T4 escalation) |

---

## 10. References

- NIST AI 100-1 — Artificial Intelligence Risk Management Framework (AI RMF 1.0).
- NIST AI RMF Agentic AI Profile (designation TBD, expected ~Q4 2026).
- NIST AI RMF Agentic Profile (CSA Labs).
- AAGATE: A NIST AI RMF-Aligned Governance Platform for Agentic AI — arxiv 2510.25863.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
