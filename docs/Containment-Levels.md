# Containment Levels

**Version**: AIZP V0.6 (new chapter)

This document specifies the **graduated containment** model used by AIZP — five containment levels (L0–L4) that the runtime applies based on the agent's current state and gravity score.

V0.1 had only two effective levels: "execute" or "halt" (SAFE_STOP). V0.2, inspired by MI9's graduated containment, introduces intermediate levels with progressive restrictions.

> ⚠️ **Notation note.** AIZP **containment** levels `L0–L4` (Free / Monitored / Sandboxed / Restricted / Halt) are **not** the same as **HSAW compliance** levels `L0–L4` (None / Advisory / Enforced / Inviolable / Verified, HSAW §8.1). Same letters, different scales. AIZP's own *compliance* tier is `G0–G5` (see [Compliance.md](Compliance.md), which maps `G` ↔ HSAW `L`).

---

## 1. Levels Overview

| Level | Name | State alignment | Restrictions |
|---|---|---|---|
| **L0** | **Free Execution** | `STABLE_ORBIT` | None — agent operates with full granted scope. |
| **L1** | **Enhanced Monitoring** | `DRIFT_WARNING` | All actions logged with full evidence; periodic operator review. |
| **L2** | **Sandboxed Execution** | `GRAVITY_LOCK_PENDING` (during confirm), `QUARANTINED` (after deny) | Tools sandboxed (Firecracker/gVisor); network egress filtered. |
| **L3** | **Restricted Execution** | `QUARANTINED` (prolonged) | Read-only mode; no external API calls; memory writes quarantined. |
| **L4** | **Halt** | `SAFE_STOP` | Execution stopped; AIAP T4 escalation initiated; operator intervention required. |

---

## 2. Per-Level Specifications

### 2.1 L0 — Free Execution

| Aspect | Setting |
|---|---|
| Tool invocation | Unrestricted (within AIAP scope) |
| Network egress | Per declared policy |
| Memory writes | Allowed |
| Logging verbosity | Standard |
| Forecast cadence | Every 5 actions |
| State machine | `STABLE_ORBIT` |
| Auto-promotion to L1 | When `G(a, c) < 0.80` |

### 2.2 L1 — Enhanced Monitoring

| Aspect | Setting |
|---|---|
| Tool invocation | Allowed; **all calls logged with full evidence** |
| Network egress | Allowed; **destinations logged** |
| Memory writes | Allowed; **provenance recorded** |
| Logging verbosity | Verbose (include `components` object, all proxy metrics) |
| Forecast cadence | Every action |
| State machine | `DRIFT_WARNING` |
| Auto-demotion to L0 | When `G ≥ 0.80` for 5 consecutive checks |
| Auto-promotion to L2 | When `G < 0.50` OR any `CRITICAL` drift |

### 2.3 L2 — Sandboxed Execution

| Aspect | Setting |
|---|---|
| Tool invocation | **Sandboxed** (Firecracker microVM, gVisor, or equivalent) |
| Network egress | **Filtered** (allowlist only); egress queued for review |
| Memory writes | **Quarantined** (writes go to a staging buffer pending release) |
| File system | **Read-only on shared paths**; writes to ephemeral scratch only |
| External tools | **Approval required** for each invocation (sys.io.confirm) |
| Logging verbosity | Maximum (include full action chain, reasoning trace if available) |
| Forecast cadence | Every action + on state-entry |
| State machine | `GRAVITY_LOCK_PENDING` or early `QUARANTINED` |
| Auto-demotion to L1 | After successful confirmation + `G ≥ 0.70` for 3 actions |
| Auto-promotion to L3 | When quarantine_duration > 5 minutes OR `G < 0.30` |

**Implementation note**: per 2026 industry consensus (Northflank, Cloudflare, E2B), Firecracker microVMs are the strongest isolation for regulated data; gVisor is preferred for compute-heavy multi-tenant; V8 Isolates suit JS-only latency-critical tasks.

### 2.4 L3 — Restricted Execution

| Aspect | Setting |
|---|---|
| Tool invocation | **Read-only tools only**; no writes, no external calls |
| Network egress | **Blocked** except to AIAP T4 escalation channel |
| Memory writes | **Frozen**; agent state cannot persist new info |
| File system | **No writes anywhere** |
| External tools | **All denied** |
| Logging verbosity | Maximum + cryptographic hash chain |
| Forecast cadence | Every action |
| State machine | `QUARANTINED` (prolonged) |
| Auto-demotion to L2 | Only via operator action |
| Auto-promotion to L4 | When `G < 0.15` OR `quarantine_duration > 30 minutes` |

> **Coordination with the orbital state machine.** Containment level and orbital state ([State-Machine.md](State-Machine.md)) are **distinct axes** that move semi-independently: the orbital state tracks *trajectory health* (gravity score), while the containment level tracks *granted capability*. They can disagree, and **when they do, the more restrictive containment level governs actual permissions.** Concretely: a `QUARANTINED` agent at **L2** may auto-recover (`QUARANTINED → RECENTERING` once `G ≥ 0.5`) and its containment auto-demotes (L2 → L1 after confirmation + `G ≥ 0.70` for 3 actions). But once containment has escalated to **L3** (prolonged quarantine), the orbital state may still progress to `RECENTERING` while the **L3 capability restrictions persist** — `L3 → L2` is operator-only. So a recovered *trajectory* does not by itself restore *capability*: the agent runs read-only / no-external-calls until an operator demotes L3, even if its gravity score has recovered.

### 2.5 L4 — Halt

| Aspect | Setting |
|---|---|
| Tool invocation | **None** |
| Network egress | **None** |
| Memory writes | **None** |
| Agent execution | **Stopped** |
| Operator notification | **Required** |
| AIAP escalation | **Auto-triggered** to T4 admin |
| Recovery | Only via operator action + new `session_id` |
| State machine | `SAFE_STOP` (terminal) |

---

## 3. Transitions Between Levels

```
                  L0 ──drift──> L1 ──drift──> L2 ──deny──> L3 ──timeout──> L4
                  ▲              │              │             │
                  │ recover      │ recover      │ recover     │
                  └──────────────┴──────────────┘             │
                                                  (operator action only)
```

Forbidden transitions:
- `L4 → L0/L1/L2/L3` directly — `SAFE_STOP` is terminal within session.
- `L2 → L0` directly — must pass through L1 first (gradual de-escalation).

---

## 4. Containment Configuration

Implementations declare containment behavior in `aizp.config.yaml`:

```yaml
aizp:
  containment:
    L0:
      forecast_cadence_steps: 5
    L1:
      forecast_cadence_steps: 1
      logging_verbosity: "verbose"
      auto_demote_after_consecutive_safe: 5
    L2:
      sandbox_technology: "firecracker"   # or "gvisor", "v8_isolates"
      network_egress_allowlist: []
      memory_write_quarantine: true
      auto_promote_after_seconds: 300
    L3:
      file_writes_allowed: false
      external_calls_allowed: false
      escalation_channel: "aiap.t4"
      auto_promote_after_seconds: 1800
    L4:
      auto_escalate: true
      escalation_level: T4
      notify_operator: true
```

---

## 5. Event Emission

Every level transition MUST emit a `CONTAINMENT_GRADUATED` event:

```json
{
  "event": "CONTAINMENT_GRADUATED",
  "payload": {
    "previous_level": "L1",
    "new_level": "L2",
    "trigger_event_id": "<UUIDv4 of preceding GRAVITY_DRIFT or GRAVITY_LOCK>",
    "reason": "drift_severity_exceeded_threshold",
    "active_restrictions": [...],
    "auto_release_conditions": [...]
  }
}
```

---

## 6. Mapping to State Machine

| AIZP State | Default Containment | Notes |
|---|---|---|
| `STABLE_ORBIT` | L0 | Default unrestricted |
| `DRIFT_WARNING` | L1 | Enhanced monitoring |
| `GRAVITY_LOCK_PENDING` | L2 | Sandbox while awaiting confirmation |
| `QUARANTINED` (initial) | L2 | After deny/timeout, sandbox first |
| `QUARANTINED` (prolonged > 5 min) | L3 | Auto-escalate to restricted |
| `RECENTERING` | L2 → L1 | De-escalate as recovery progresses |
| `SAFE_STOP` | L4 | Terminal |

---

## 7. Conformance Requirements (G3+)

A G3-compliant implementation MUST:

1. Implement at least L0, L1, L2, L4 (L3 is recommended but not required for G3).
2. Emit `CONTAINMENT_GRADUATED` event on every level change.
3. Honor auto-promote and auto-demote thresholds.
4. Provide configurability via `aizp.config.yaml`.

G4 adds: maintain a queryable log of all level transitions.
G5 adds: formal verification of level transition invariants (e.g., "no skip from L0 to L4 without passing through L1, L2, L3, **except the direct L0→L4 path permitted when `G < 0.15`**" — consistent with [State-Machine.md](State-Machine.md) I-8 and [Compliance.md](Compliance.md) §7.1).

---

## 8. Defense-in-Depth

Containment is one layer. It complements:

- **AISOP** `sys.io.confirm` — explicit user authorization gate.
- **AIAP** T1–T4 — declarative scope-based authorization.
- **Zero Trust / NHI** — runtime credential validation (see [Integration-ZT.md](Integration-ZT.md)).
- **Output filtering** — content-safety filters at LM output (upstream).

Containment alone does not prevent misalignment — it bounds the damage of misalignment that has been detected.

---

## References

- MI9 framework (Wang et al., 2025) — graduated containment design. arxiv 2508.03858.
- Northflank / Cloudflare / E2B (2026) — Firecracker/gVisor industry adoption for AI agent sandboxing.
- AAGATE (Huang et al., 2025) — Kubernetes-native containment for agentic AI. arxiv 2510.25863.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
