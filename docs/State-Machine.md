# AIZP State Machine

**Version**: AIZP V0.6

This document specifies the formal state machine governing AIZP behavior.

**Since V0.2:** state count grew from 5 → **6**, adding `QUARANTINED` as an intermediate graduated-containment state between `GRAVITY_LOCK_PENDING` and `SAFE_STOP`. The default fallback from lock-deny / timeout is now `QUARANTINED` instead of `SAFE_STOP`.

---

## 1. States (6 states)

| State | Symbol | Containment | Meaning |
|---|---|---|---|
| `STABLE_ORBIT` | `S` | L0 | Behavior aligned; auto-execute. |
| `DRIFT_WARNING` | `D` | L1 | Mild drift; enhanced monitoring. |
| `GRAVITY_LOCK_PENDING` | `L` | L2 | Awaiting human authorization. |
| **`QUARANTINED`** | **`Q`** | **L2/L3** | **Recovery attempt with sandboxing; since V0.2.** |
| `RECENTERING` | `R` | L1/L2 | Recovery in progress. |
| `SAFE_STOP` | `X` | L4 | Terminal halt. |

See [Containment-Levels.md](Containment-Levels.md) for L0–L4 details.

---

## 2. State Diagram

```
                         ┌───────────────┐
                         │ STABLE_ORBIT  │◀──────────────┐
                         │     (S)       │               │
                         └───────┬───────┘               │
                                 │ G < 0.8               │ G ≥ 0.8
                                 ▼                       │
                         ┌───────────────┐               │
                         │ DRIFT_WARNING │───────────────┤
                         │     (D)       │               │
                         └───────┬───────┘               │
                                 │ G < 0.5               │ G ≥ 0.8
                                 ▼                       │
                  ┌─────────────────────────────┐        │
                  │  GRAVITY_LOCK_PENDING (L)   │        │
                  └──┬─────────┬────────────┬───┘        │
              confirm│         │timeout/deny│            │
                     ▼         ▼            ▼            │
              ┌────────────┐  ┌──────────────────────┐   │
              │RECENTERING │  │   QUARANTINED  (Q)   │   │ G ≥ 0.8
              │    (R)     │  └──┬─────────────┬─────┘   │
              └─────┬──────┘     │ G recovers  │ timeout │
              G≥0.8 │           ▼              ▼          │
                    │     RECENTERING       SAFE_STOP     │
                    └────────────┬───────────────┐        │
                                 │ G ≥ 0.8       │        │
                                 ├───────────────┴────────┘
                                 │ G < 0.15 or fail
                                 ▼
                              SAFE_STOP (X)
                            (operator action only to reset)
```

> The diagram shows the **typical** stepwise descent. Any band is reachable on the **first** evaluation of an action (e.g. an action scoring `G = 0.4` enters `GRAVITY_LOCK_PENDING` directly, without passing through `DRIFT_WARNING`). The authoritative transitions are the table in §3 and the pseudocode in §5, not the figure.

---

## 3. Transitions

| From | To | Trigger | Event Emitted | Notes |
|---|---|---|---|---|
| `S` | `D` | `G ∈ [0.5, 0.8)` | `GRAVITY_DRIFT` (sev ≤ MEDIUM) | Containment → L1 |
| `S` | `L` | `G ∈ [0.3, 0.5)` | `GRAVITY_LOCK` (PENDING) | Containment → L2 |
| `S` | `X` | `G < 0.15` (critical) | `SAFE_STOP` (CRITICAL_DRIFT) | Containment → L4 |
| `D` | `S` | `G ≥ 0.8` next action | (none) | Containment → L0 |
| `D` | `L` | `G ∈ [0.3, 0.5)` | `GRAVITY_LOCK` (PENDING) | |
| `D` | `Q` | `G ∈ [0.15, 0.3)` | `CONTAINMENT_GRADUATED` (L1→L2) | since V0.2 |
| `D` | `X` | `G < 0.15` | `SAFE_STOP` | |
| `L` | `R` | confirm (`CONFIRMED`) | `RECENTERING` | |
| `L` | **`Q`** | **deny / timeout** | `CONTAINMENT_GRADUATED` + `GRAVITY_LOCK` (DENIED/TIMEOUT) | **new V0.2 default** |
| `L` | `X` | severe deny + `G < 0.15` | `SAFE_STOP` | exceptional |
| `Q` | `R` | `G ≥ 0.5` recovers | `RECENTERING` | new V0.2 |
| `Q` | `X` | `quarantine_timeout` OR `G < 0.15` | `SAFE_STOP` (QUARANTINE_TIMEOUT) | new V0.2 |
| `R` | `S` | `G ≥ 0.8` after recovery | (none) | |
| `R` | `X` | recovery fails or `G < 0.3` | `SAFE_STOP` (RECOVERY_FAILED) | |
| `X` | — | terminal | (none — operator) | |

### 3.1 Forbidden transitions

| Forbidden | Reason |
|---|---|
| `X → any` | Safe Stop is terminal; reset requires operator + new session_id. |
| `R → L` directly | Recovery should produce stable or stopped, not loop back through lock. |
| `S → X` without `GRAVITY_DRIFT` | All `X` transitions MUST be preceded by an explanatory event. |
| `Q → L` directly | Quarantine to lock requires recovery via RECENTERING. |
| `L → X` directly without going through `Q` first | **Since V0.2**: the default fallback is `Q`, not `X`. `X` is reserved for very critical cases. |

### 3.2 Quarantine timeout policy

Default `quarantine_timeout = 30 minutes` (configurable). If `G(a, c) ≥ 0.5` is achieved before timeout, transitions to `RECENTERING`. Otherwise → `SAFE_STOP`.

---

## 4. Invariants (9 invariants)

V0.1 had 7 invariants. V0.2 adds:

### I-1 to I-7 (unchanged)

(See V0.1 spec — Single Current State, Event Causality, Safe Stop Finality, Lock-Before-Execute, Audit Trail Completeness, Gravity Score Determinism, Threshold Monotonicity.)

### I-8: Containment monotonicity

Containment level changes MUST be monotonic per step: at most one level promotion per state transition. Skipping levels (e.g., L0 → L4 in one transition without passing through L1, L2, L3) is forbidden **except** when `G < 0.15`, which is the only allowed direct path to L4.

### I-9: Quarantine recoverability

From `QUARANTINED`, both `RECENTERING` and `SAFE_STOP` MUST be reachable within `quarantine_timeout` seconds. The state machine MUST NOT remain in `QUARANTINED` indefinitely.

---

## 5. Pseudocode

```python
class AIZPStateMachine:
    state: State = STABLE_ORBIT
    containment_level: str = "L0"
    quarantine_entered_at: float | None = None
    
    def evaluate(self, action, context) -> Decision:
        check = emit_gravity_check(action, context, ...)
        g = check["payload"]["gravity_score"]
        drifts = detect_drifts(action, context)
        if drifts:
            emit_gravity_drift(drifts, ...)
        
        # forecast (V0.2): if predictive monitoring enabled
        if self.forecasting_enabled:
            forecast = self.forecaster.forecast(self.state, K=5)
            emit_gravity_forecast(forecast, ...)
            # adjust g if forecast indicates compositional risk
            t = 1 - forecast["predicted_violation_probability"]
            g = g - 0.05 * (1 - t)  # mild penalty for trajectory risk
        
        if g >= 0.80:
            self._transition_to(STABLE_ORBIT, L0)
            return EXECUTE
        
        if g >= 0.50:
            self._transition_to(DRIFT_WARNING, L1)
            return EXECUTE_WITH_LOGGING
        
        if g >= 0.30:
            self._transition_to(GRAVITY_LOCK_PENDING, L2)
            lock_evt = emit_gravity_lock(action, ...)
            result = self.confirm(...)
            if result == CONFIRMED:
                self._transition_to(RECENTERING, L1)
                emit_recentering(lock_evt, ...)
                return EXECUTE
            else:  # DENIED or TIMEOUT
                # V0.2: default to QUARANTINED instead of SAFE_STOP
                self._transition_to(QUARANTINED, L2)
                self.quarantine_entered_at = time.now()
                return HALT_QUARANTINE
        
        if g >= 0.15:
            self._transition_to(QUARANTINED, L2)
            self.quarantine_entered_at = time.now()
            return HALT_QUARANTINE
        
        # g < 0.15
        self._transition_to(SAFE_STOP, L4)
        emit_safe_stop("CRITICAL_DRIFT", ...)
        return HALT
    
    def quarantine_tick(self, current_g):
        """Called periodically while in QUARANTINED."""
        if self.state != QUARANTINED:
            return
        elapsed = time.now() - self.quarantine_entered_at
        if current_g >= 0.50:
            self._transition_to(RECENTERING, L1)
            return
        if elapsed > self.config.quarantine_timeout:
            self._transition_to(SAFE_STOP, L4)
            emit_safe_stop("QUARANTINE_TIMEOUT", ...)
            return
        # Otherwise stay quarantined; may escalate L2 → L3 after 5 min
        if elapsed > 300 and self.containment_level == "L2":
            self._set_containment("L3")
```

---

## 6. Reset Semantics

Same as V0.1: `SAFE_STOP` is terminal within a session. Operator action + new `session_id` required to reset.

Since V0.2: `QUARANTINED` is **not** terminal. It auto-resolves to either `RECENTERING` (recovery) or `SAFE_STOP` (timeout/critical) within `quarantine_timeout`.

---

## 7. Concurrency (unchanged from V0.1)

(See V0.1 spec §7.)

---

## 8. Formal Properties

(V0.1 properties retained: Safety, Liveness, Recoverability, Boundedness.)

### Since V0.2:

**Graduated containment**: For any `G(a, c) ∈ [0.15, 0.30)`, the implementation MUST enter `QUARANTINED` (containment L2 or L3) rather than direct `SAFE_STOP`.

**Quarantine bounded duration**: A trajectory in `QUARANTINED` will leave within `quarantine_timeout` seconds (default 30 min), to either `RECENTERING` or `SAFE_STOP`.

**Compositional safety**: If predictive monitoring is enabled (G4+), no action proceeds when `T(c) < 0.30` (i.e., predicted violation probability > 0.70 within K steps) without explicit human confirmation, **regardless of the local gravity score**.

A formal TLA+ specification of these properties is the target for G5 compliance.

---

## 9. State Machine Compliance Matrix

| Compliance Level | States required |
|---|---|
| G1 | `STABLE_ORBIT` only (degenerate state machine) |
| G2 | + `DRIFT_WARNING` |
| G3 | + `GRAVITY_LOCK_PENDING`, `RECENTERING`, `SAFE_STOP`, **`QUARANTINED`** (V0.2) |
| G4 | full 6 states + predictive monitoring integration |
| G5 | full 6 states + TLA+/Coq verification |

---

## References

(unchanged from V0.1 plus:)

- MI9 framework (Wang et al., 2025) — graduated containment leading to the QUARANTINED state. arxiv 2508.03858.
- AAGATE (Huang et al., 2025) — Kubernetes-native state machine for agentic AI governance. arxiv 2510.25863.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
