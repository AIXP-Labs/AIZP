# AIXP Stack Integration

**Version**: AIZP V0.6

This document maps AIZP to AIBP (drift inspection at the agent boundary), AILP (gravity profile publication), and OpenTelemetry (cross-protocol observability) — all added in V0.2. See [Integration-OTel.md](Integration-OTel.md) and [Integration-ZT.md](Integration-ZT.md) for the cross-cutting protocols outside the original AIXP 9.

This document describes how AIZP integrates into the broader AIXP protocol stack.

---

## 1. AIXP Stack Overview

```
┌───────────────────────────────────────────────────────────────┐
│  HSAW — Axiom 0: Human Sovereignty and Wellbeing              │
│  (The immutable alignment principle)                          │
└───────────────────────────────────────────────────────────────┘
                              ▲
                              │ all protocols below align to HSAW
                              │
┌─────────────────────────────┴─────────────────────────────────┐
│  AIZP — Behavioral Gravity                                    │
│  (Dynamics layer: keeps execution gravitationally anchored)   │
└─────────────────────────────┬─────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────────┐   ┌─────────────────┐
│   AISOP      │    │      AIAP        │   │      AIBP       │
│   (exec)     │    │  (governance)    │   │    (social)     │
└──────┬───────┘    └────────┬─────────┘   └────────┬────────┘
       │                     │                      │
       ▼                     ▼                      ▼
sys.io.confirm        T1–T4 trust          aibot-* messages
       │                     │                      │
       └──────────┬──────────┘                      │
                  ▼                                 │
        ┌──────────────────┐                        │
        │   AIVP / AIRP    │◀───────────────────────┘
        │     (value)      │
        └──────────────────┘
                  │
                  ▼
        ┌──────────────────┐
        │      AILP        │
        │   (discovery)    │
        └──────────────────┘
```

**Relationship to HSAW's Layered Accountability (HSAW §7.3).** HSAW describes a 5-layer defense-in-depth — AISOP (can it execute?) → AIAP (allowed to evolve?) → AIBP (communicating honestly?) → AILP (discoverable fairly?) → AIVP/AIRP (transaction authorized?). **AIZP is not a sixth sequential layer.** It is a **cross-cutting runtime monitor**: it scores behavior *across* all of HSAW's layers (and the external MCP/A2A boundaries — §7.3 of this document) and drives the gravity state machine. Where HSAW's layers each answer one accountability question, AIZP continuously answers "is the trajectory, across all layers, still orbiting HSAW?" The HSAW WhitePaper predates AIZP and does not yet list it in §7.2/§7.3; AIZP composes with that model rather than replacing it.

---

## 2. Per-Protocol Relationship

### 2.1 HSAW (Foundation)

| Aspect | Detail |
|---|---|
| **Role** | HSAW defines the alignment center to which AIZP gravity points. |
| **Direction** | HSAW is upstream of AIZP. AIZP does not modify HSAW. |
| **Interface** | HSAW provides the conceptual "Axiom 0" that AIZP operationalizes. |

### 2.2 AISOP (Execution)

| Aspect | Detail |
|---|---|
| **Role** | AISOP provides execution primitives, especially `sys.io.confirm`. |
| **Direction** | AIZP calls into AISOP. When `GRAVITY_LOCK` triggers, AIZP delegates the actual user prompt to `sys.io.confirm`. |
| **Interface** | `confirmation_primitive: "sys.io.confirm"` field in `GRAVITY_LOCK` event. |
| **See also** | [Integration-AISOP.md](Integration-AISOP.md) for the full bridge specification. |

### 2.3 AIAP (Governance)

| Aspect | Detail |
|---|---|
| **Role** | AIAP defines trust levels T1–T4 and governance contracts. |
| **Direction** | AIZP reads from AIAP. `granted_scope(c)` in the Gravity Score is derived from AIAP trust level. |
| **Interface** | AIAP trust level → AIZP `A(a, c)` Authority Scope component. |
| **See also** | [Integration-AIAP.md](Integration-AIAP.md) for the full mapping. |

### 2.4 AIBP (Social)

| Aspect | Detail |
|---|---|
| **Role** | AIBP defines agent-to-agent communication and bot identity (`aibot-*@domain.dev`). |
| **Direction** | AIZP monitors AIBP-mediated interactions for Social Drift and Identity Drift. |
| **Interface** | AIBP messages flow through AIZP drift detectors before delivery / after receipt. |
| **Notes** | A Social Drift event in AIZP MAY trigger AIBP-level reputation updates. |

### 2.5 AIVP / AIRP (Value)

| Aspect | Detail |
|---|---|
| **Role** | AIVP (international) and AIRP (RMB) handle value exchange and settlement. |
| **Direction** | AIZP gates AIVP/AIRP transactions. High-value transfers MUST pass through `GRAVITY_LOCK`. |
| **Interface** | Transfer amount + counterparty trust → `R(a)` Reversibility and `H(a, c)` Recency. |
| **Notes** | Economic Drift detection is most active around AIVP/AIRP-mediated actions. |

### 2.6 AILP (Discovery)

| Aspect | Detail |
|---|---|
| **Role** | AILP enables agent discovery and capability advertising. |
| **Direction** | AIZP MAY consult AILP to assess peer agent gravity (e.g., refuse to coordinate with low-gravity peers). |
| **Interface** | Agent gravity profile MAY be published as part of AILP discovery metadata. |

---

## 3. Cross-Protocol Event Flow

A typical AIZP-mediated agent action emits events spanning multiple protocols:

```
Agent decides action a
     │
     ▼
AIZP.GRAVITY_CHECK         ←—— AIZP
     │
     ├─ if G ≥ 0.8 ──▶ AISOP.execute(a)            ←—— AISOP
     │
     ├─ if 0.5 ≤ G < 0.8 ──▶ AIZP.GRAVITY_DRIFT (log)
     │                          │
     │                          ▼
     │                       AISOP.execute(a)
     │
     ├─ if 0.3 ≤ G < 0.5 ──▶ AIZP.GRAVITY_LOCK (state GRAVITY_LOCK_PENDING)
     │                          │
     │                          ▼
     │                       AISOP.sys.io.confirm   ←—— AISOP
     │                          │
     │                          ├─ confirmed ──▶ AIZP.RECENTERING
     │                          │                    │
     │                          │                    ▼
     │                          │                 AISOP.execute(a)
     │                          │
     │                          └─ denied  ────▶ AIZP.QUARANTINED
     │
     ├─ if 0.15 ≤ G < 0.3 ──▶ AIZP.QUARANTINED (graduated containment)
     │
     └─ if G < 0.15 ────▶ AIZP.SAFE_STOP
                            │
                            ▼
                         AIAP.T4_escalation        ←—— AIAP
```

---

## 4. Mandatory Cross-Protocol Behaviors

| Protocol | Action | AIZP Requirement |
|---|---|---|
| AISOP | Tool invocation | AIZP MUST evaluate Gravity Score before AISOP executes. |
| AISOP | `sys.io.confirm` | AIZP `GRAVITY_LOCK` MUST delegate to this primitive when human confirmation is needed. |
| AIAP | Trust level change | AIZP MUST recompute `A(a, c)` for in-flight actions when trust level changes. |
| AIAP | Critical violation (T4) | AIZP MUST emit `SAFE_STOP` and AIAP MUST handle escalation. |
| AIBP | Outbound message | AIZP MUST run Social/Identity Drift checks before send. |
| AIVP/AIRP | Transfer ≥ deployment threshold | AIZP MUST emit `GRAVITY_LOCK`; transfer proceeds only on `CONFIRMED`. |

---

## 5. Configuration Schema (Cross-Protocol)

Implementations declare their AIXP integrations in a single config:

```yaml
aizp:
  version: V0.6
  compliance_level: G3
  
  hsaw:
    axiom_reference: "hsaw.dev"
    immutable: true
  
  aisop:
    confirmation_primitive: "sys.io.confirm"
    require_pre_execution_gravity_check: true
  
  aiap:
    trust_level_source: "agent_card.json"
    auto_escalate_on_safe_stop: true
    escalation_level: T4
  
  aibp:
    drift_check_outbound: [SOCIAL_DRIFT, IDENTITY_DRIFT]
    drift_check_inbound: [SOCIAL_DRIFT]
  
  aivp:
    gravity_lock_threshold_amount: 100  # USD; deployment-specific
    high_value_threshold: 1000
  
  airp:
    gravity_lock_threshold_amount: 700  # RMB
    high_value_threshold: 7000
  
  ailp:
    publish_gravity_profile: false  # Privacy-sensitive
```

---

## 6. Independence Properties

AIZP is designed so that:

- **HSAW can exist without AIZP** (it predates the dynamics layer).
- **AIZP cannot meaningfully exist without HSAW** (it needs an alignment center).
- **AISOP can exist without AIZP** (executes flow programs without gravity checks; trades safety for simplicity).
- **AIZP is most useful when AISOP and AIAP are present** (gives it primitives to call and trust levels to read).

Deployments may adopt AIZP incrementally:

| Stage | Components |
|---|---|
| Stage 1 | AIZP logging only (`GRAVITY_CHECK` events emitted; no enforcement) |
| Stage 2 | AIZP + AISOP (`GRAVITY_LOCK` → `sys.io.confirm` works) |
| Stage 3 | AIZP + AISOP + AIAP (full trust integration) |
| Stage 4 | Full AIXP stack (multi-protocol gravity-aware execution) |

---

## 7. Cross-Protocol Observability + ZT

Two cross-cutting concerns (added in V0.2) span the entire AIXP stack:

### 7.1 OpenTelemetry GenAI SemConv

Every AIXP protocol can emit OTel spans/events. AIZP V0.6 standardizes the schema:

| Protocol | OTel namespace |
|---|---|
| HSAW | `gen_ai.hsaw.*` |
| AIZP | `aizp.*` (12 event names) |
| AISOP | `gen_ai.aisop.*` (incl. `sys.io.confirm`) |
| AIAP | `gen_ai.aiap.*` (trust level changes) |
| AIBP | `gen_ai.aibp.*` (message events) |
| AIVP / AIRP | `gen_ai.aivp.*` / `gen_ai.airp.*` (transfer events) |
| AILP | `gen_ai.ailp.*` (discovery events) |

See [Integration-OTel.md](Integration-OTel.md) for AIZP-specific mapping.

### 7.2 Zero Trust + NHI

Runtime identity verification (DID / NHI / JIT) is a cross-cutting layer (since V0.2). AIAP T-levels remain the upper bound; ZT narrows actual granted scope per task.

See [Integration-ZT.md](Integration-ZT.md).

### 7.3 External Interoperability Layers (MCP / A2A)

The AIXP protocols are AIXP-native. In 2026 the broader agent ecosystem consolidated around two external standards that AIZP also governs:

| External standard | Layer | AIZP role | Detail |
|---|---|---|---|
| **MCP** (Model Context Protocol) | Tool integration (vertical) | Score each `tools/call` with `GRAVITY_CHECK` before dispatch | [Integration-MCP.md](Integration-MCP.md) |
| **A2A** (Agent-to-Agent; ACP merged in, Linux Foundation) | Agent coordination (horizontal) | `IDENTITY_VERIFICATION` + `INTER_AGENT_DRIFT` on delegations | [Integration-A2A.md](Integration-A2A.md) |

**Relationship to AIBP**: AIBP is the AIXP-native inter-agent protocol (`aibot-*@domain.dev`); A2A is the external interop standard. AIZP applies the **same** `INTER_AGENT_DRIFT` machinery to both boundaries — AIBP for intra-stack agents, A2A for cross-vendor agents. MCP plays the tool-call role that AISOP plays natively; AIZP scores both the same way.

---

## 8. AIXP Protocol Slot for AIZP

AIZP is the **eighth protocol** in the AIXP stack — HSAW, AISOP, AIAP, AIBP, AIVP, AIRP, AILP, AIZP — under the **AIXP** umbrella, alongside the **SoulBot** reference runtime and the **SoulACP** adapter library (implementations, not protocols). The 12,000+ line specification reaches parity density with peer protocols.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
