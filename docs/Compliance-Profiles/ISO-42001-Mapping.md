# Compliance Profile: ISO/IEC 42001 Mapping

**Version**: AIZP V0.6 (new chapter)
**ISO/IEC 42001:2023**: Information technology — Artificial intelligence — Management system

This document maps AIZP to ISO/IEC 42001, the world's first AI management system (AIMS) standard, certifiable since 2023 and seeing growing adoption for AI compliance.

---

## 1. Why ISO 42001 Matters

ISO 42001 is **voluntary but certifiable** (unlike EU AI Act which is mandatory). Certification provides:

- Demonstrable risk management for regulators (Colorado AI Act, Texas TRAIGA).
- Customer assurance — enterprise buyer adoption of ISO 42001 or AIUC-1 (which builds on ISO 42001) is growing.
- Internal AI governance framework.

Adoption trajectory (mid-2026): adoption of ISO 42001 for AI compliance is growing.

---

## 2. Clause-by-Clause Mapping

ISO 42001 is structured similarly to ISO 27001 (security). Below is mapping for major clauses.

### 2.1 Clause 4 — Context of the Organization

| ISO 42001 4.x | AIZP Contribution |
|---|---|
| 4.1 Internal/external context | AIAP card declarations + governance contract |
| 4.2 Stakeholder needs | HSAW Axiom 0 + per-stakeholder gravity weights |
| 4.3 AIMS scope | Per-agent AIZP compliance level declaration |
| 4.4 AIMS itself | AIZP event log + state machine |

### 2.2 Clause 5 — Leadership

| ISO 42001 5.x | AIZP Contribution |
|---|---|
| 5.1 Leadership commitment | Documented AIZP adoption + compliance level target |
| 5.2 AI policy | AIZP configuration (`aizp.config.yaml`) is the runtime policy |
| 5.3 Roles & authorities | AIAP T1–T4 + Agentic AI Committee (AIZP-recommended governance body, Compliance Profile NIST AI RMF §2) |

### 2.3 Clause 6 — Planning

| ISO 42001 6.x | AIZP Contribution |
|---|---|
| 6.1 Risks & opportunities | Threat-Model.md + OWASP-Agentic-Top10-Mapping.md |
| 6.2 AI objectives | HSAW + declared agent goals per AIAP |
| 6.3 AI system impact assessment | `risk_level` field in GRAVITY_CHECK |

### 2.4 Clause 7 — Support

| ISO 42001 7.x | AIZP Contribution |
|---|---|
| 7.1 Resources | Implementer-Guide §11 (reference impl structure) |
| 7.2 Competence | Operator training + FAQ |
| 7.4 Communication | OTel integration → dashboards |
| 7.5 Documented info | AIZP_Protocol.md + all docs/ |

### 2.5 Clause 8 — Operation

| ISO 42001 8.x | AIZP Contribution |
|---|---|
| 8.1 Operational planning | State machine + containment levels |
| 8.2 AI system impact assessment | GRAVITY_CHECK risk_level per action |
| 8.3 AI lifecycle | Compliance levels G0 → G5 maturity model |

### 2.6 Clause 9 — Performance Evaluation

| ISO 42001 9.x | AIZP Contribution |
|---|---|
| 9.1 Monitoring & measurement | 12 AIZP events + OTel metrics |
| 9.2 Internal audit | G4 — auditable gravity time-series |
| 9.3 Management review | Quarterly review of SAFE_STOP + REWARD_HACK |

### 2.7 Clause 10 — Improvement

| ISO 42001 10.x | AIZP Contribution |
|---|---|
| 10.1 Nonconformity & corrective action | False-positive feedback loop (Drift-Model §6) |
| 10.2 Continual improvement | Baseline refresh + compliance level upgrade path |

---

## 3. Annex A Controls (ISO 42001:2023 Annex A)

Annex A defines reference controls for AI management. ISO/IEC 42001:2023 Annex A contains ~38 controls across 9 domains (A.2–A.10) and requires a Statement of Applicability. Selected mappings:

| Annex A Control | AIZP Implementation |
|---|---|
| A.2 AI policies | aizp.config.yaml + governance documentation |
| A.3 Internal organization | Agentic AI Committee + AIAP T4 escalation |
| A.4 Resources for AI systems | Compliance level declarations |
| A.5 Impact analysis | GRAVITY_CHECK risk_level + Threat-Model.md |
| A.6.2 AI system life cycle | Containment Level transitions reflect lifecycle phases |
| A.7 Data management | AIAP governance hash + memory_quarantine |
| A.8 Information for users | AIBP message disclosure + Identity-Verification events |
| A.9 Use of AI systems | RECENTERING + SAFE_STOP enforce safe use |
| A.10 Third-party relationships | AIBP / AILP integration (covered by other AIXP protocols) |

---

## 4. Certification Path

For deployments seeking ISO 42001 certification:

| Step | AIZP Role |
|---|---|
| 1. Establish AIMS | Adopt AIZP at G3+ |
| 2. Document policies | aizp.config.yaml + per-agent AIAP card |
| 3. Risk assessment | Use Threat-Model.md + OWASP profile |
| 4. Controls implementation | AIZP events + containment levels |
| 5. Monitoring & measurement | OTel pipeline + dashboards |
| 6. Internal audit | G4 audit log query |
| 7. Management review | Agentic AI Committee meetings |
| 8. External certification audit | Provide AIZP compliance report + event samples |

---

## 5. AIUC-1 Integration

**AIUC-1** is an independent agent standard that references current regulations and frameworks, providing a single auditable framework for AI agent adoption.

AIZP at G4+ satisfies the runtime monitoring portion of AIUC-1. Other AIUC-1 components (training data, model cards, organizational policy) are out of AIZP scope.

---

## 6. Recommended AIZP Levels per ISO 42001 Maturity

| ISO 42001 maturity | Recommended AIZP level |
|---|---|
| Initial (foundational AIMS) | G1 |
| Standardized | G2 |
| Defined (full AIMS) | G3 |
| Quantitatively managed | G4 |
| Optimizing | G5 |

---

## 7. References

- ISO/IEC 42001:2023 — Information technology — Artificial intelligence — Management system. iso.org.
- ISO 42001 Implementation Guide — aigl.blog.
- Schellman, A-LIGN, BSI, Deloitte 2026 ISO 42001 guides.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
