# Integration: AISOP

**Version**: AIZP V0.6

**Since V0.2:** AISOP flow node annotations can include the extended fields (`min_gravity_score`, drift type lists, containment level), and the `GRAVITY_LOCK` default fallback is now `QUARANTINED` (containment L2) rather than direct `SAFE_STOP`.

This document specifies how AIZP integrates with AISOP, particularly the `sys.io.confirm` primitive. Without clear delineation, the two protocols would have overlapping authorization concerns.

---

## 1. Layering

```
AIZP — DECIDES WHEN human authorization is needed.
        ▼
AISOP — DEFINES HOW human authorization is requested (sys.io.confirm).
```

This separation of concerns:

- **AIZP** is **risk-evaluation logic**: it computes Gravity Score, detects drift, and decides authorization is required.
- **AISOP** is the **authorization primitive**: it knows how to prompt the user, render UI, capture input, and return a confirmation result.

Neither protocol implements the other's responsibility. They MUST work together to provide end-to-end coverage.

---

## 2. The Bridge: `GRAVITY_LOCK` → `sys.io.confirm`

When AIZP emits a `GRAVITY_LOCK` event, the runtime MUST:

1. Halt execution of the locked action.
2. Invoke `sys.io.confirm` with parameters derived from the `GRAVITY_LOCK` event payload.
3. Wait for `sys.io.confirm` to return.
4. Update the `GRAVITY_LOCK` event's `status` field based on the return value.
5. Drive the AIZP state machine accordingly (`RECENTERING` or `SAFE_STOP`).

---

## 3. Field Mapping

| `GRAVITY_LOCK` field | `sys.io.confirm` parameter |
|---|---|
| `action_descriptor` | `subject` (what the user is confirming) |
| `confirmation_prompt` | `prompt` (full text shown to user) |
| `timeout_seconds` | `timeout` |
| `payload.action_id` | `correlation_id` (for tracing) |

### 3.1 Status mapping

| `sys.io.confirm` result | `GRAVITY_LOCK.status` | AIZP next state |
|---|---|---|
| `confirmed` | `CONFIRMED` | `RECENTERING` |
| `denied` | `DENIED` | `SAFE_STOP` |
| `timeout` | `TIMEOUT` | `SAFE_STOP` |

---

## 4. Example Flow

### 4.1 AISOP flow with AIZP annotations

```json
{
  "flow_id": "process_payment",
  "nodes": [
    {
      "id": "validate_input",
      "type": "function",
      "aizp": {
        "gravity_check_required": true,
        "min_gravity_score": 0.8
      }
    },
    {
      "id": "transfer_funds",
      "type": "tool",
      "tool": "aivp.transfer",
      "aizp": {
        "gravity_check_required": true,
        "gravity_lock": "MANDATORY",
        "drift_types_monitored": ["AUTHORITY_DRIFT", "ECONOMIC_DRIFT"],
        "min_gravity_score": 0.9
      }
    }
  ]
}
```

### 4.2 Runtime sequence

```
[1] AISOP runtime reaches node "transfer_funds"
[2] AIZP intercepts: compute_gravity_score(action="transfer_funds", context=...)
    → G = 0.42 (below 0.5)
[3] AIZP emits GRAVITY_LOCK event
    {
      "event": "GRAVITY_LOCK",
      "action_id": "transfer_funds_001",
      "status": "PENDING_CONFIRMATION",
      "confirmation_primitive": "sys.io.confirm",
      "confirmation_prompt": "Confirm $5000 transfer to recipient X?",
      "timeout_seconds": 300,
      "fallback": "SAFE_STOP"
    }
[4] AISOP runtime invokes sys.io.confirm(
      subject="transfer_funds_001",
      prompt="Confirm $5000 transfer to recipient X?",
      timeout=300
    )
[5] User responds "confirmed"
[6] AISOP returns confirmed=true
[7] AIZP updates state: GRAVITY_LOCK_PENDING → RECENTERING
[8] AIZP emits RECENTERING event
[9] AIZP re-evaluates gravity (now G ≥ 0.8 with fresh confirmation)
[10] State → STABLE_ORBIT
[11] AISOP runtime executes "transfer_funds"
```

---

## 5. Independence Test

To verify the bridge is correctly implemented, run these two tests:

### 5.1 AISOP without AIZP

- Disable AIZP.
- Run an AISOP flow that includes `sys.io.confirm` calls.
- Expected: Confirms still work; no gravity events emitted; flow executes.

### 5.2 AIZP without AISOP

- Disable AISOP (or stub it).
- Trigger an AIZP `GRAVITY_LOCK`.
- Expected: AIZP logs the event but **cannot** complete authorization; the runtime should fall back to `SAFE_STOP` because no confirmation primitive is available.

Both tests confirm the two protocols are loosely coupled and have well-defined responsibilities.

---

## 6. Conflicts and Tie-Breaking

In rare cases, AIZP and AISOP MAY produce conflicting directives:

| Scenario | Resolution |
|---|---|
| AISOP flow has `sys.io.confirm` for an action that AIZP rates G ≥ 0.8 | Honor the AISOP-level confirm. AIZP's high score does not override an explicit AISOP requirement. |
| AIZP wants `GRAVITY_LOCK` but AISOP flow has no `sys.io.confirm` node | AIZP MUST insert a synthetic confirm prompt via the runtime's confirm primitive. If the primitive is unavailable, fall back to `SAFE_STOP`. |
| AIZP says `SAFE_STOP` but AISOP flow has continuation logic | `SAFE_STOP` is terminal. AISOP runtime MUST honor it and abort the flow. |

The rule of thumb: **AISOP-declared confirmations are mandatory regardless of AIZP score**. AIZP can only add more confirmations, not remove them.

---

## 7. Event Correlation

Both AIZP and AISOP events SHOULD include correlation fields for tracing:

| Field | Present in | Use |
|---|---|---|
| `agent_id` | both | Identifies the agent |
| `session_id` | both | Identifies the trajectory |
| `correlation_id` | AISOP | Links `sys.io.confirm` to the originating `GRAVITY_LOCK` |
| `trigger_event_id` | AIZP (RECENTERING, SAFE_STOP) | Links to the prior event in the chain |

This allows reconstructing the full chain:

```
GRAVITY_CHECK → GRAVITY_LOCK → sys.io.confirm → RECENTERING → execute
```

---

## 8. Conformance

An implementation claims AIZP + AISOP integration conformance if:

1. Every `GRAVITY_LOCK` event with `status = PENDING_CONFIRMATION` is followed by exactly one `sys.io.confirm` invocation correlated by `action_id` / `correlation_id`.
2. The `sys.io.confirm` result is reflected in the `GRAVITY_LOCK` event's final `status`.
3. The AIZP state machine transitions according to the result.

See [Compliance.md](Compliance.md) for the corresponding conformance test cases (G2+).

---

## 9. `aizp:` Flow Node Annotations

AISOP flow nodes can carry expanded V0.2 annotations:

```json
{
  "id": "transfer_funds",
  "type": "tool",
  "tool": "aivp.transfer",
  "aizp": {
    "gravity_check_required": true,
    "gravity_lock": "MANDATORY",
    "drift_types_monitored": [
      "AUTHORITY_DRIFT",
      "ECONOMIC_DRIFT",
      "COMPOSITIONAL_DRIFT"
    ],
    "min_gravity_score": 0.9,
    "fallback_on_deny": "QUARANTINED",
    "min_containment_level": "L2",
    "require_identity_verification": true,
    "forecast_horizon_steps": 5
  }
}
```

### 9.1 Fallback policy

V0.1 default: `GRAVITY_LOCK` deny → `SAFE_STOP`
V0.2 default: `GRAVITY_LOCK` deny → `QUARANTINED` (recovery attempt before terminal halt)

The new field `fallback_on_deny` lets implementations restore V0.1 behavior or choose `RECENTERING` for low-criticality flows.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
