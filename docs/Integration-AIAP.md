# Integration: AIAP

**Version**: AIZP V0.6

This document specifies how AIZP integrates with AIAP's trust level system (T1–T4), governance contracts, and compliance escalation.

**Since V0.2:** AIAP T-levels become the **upper bound** of scope; actual granted scope is `T_level ∩ JIT_credentials`. See §10 for the new JIT credential integration and [Integration-ZT.md](Integration-ZT.md) for Zero Trust details.

---

## 1. Layering

```
AIAP   — DECLARES WHO is authorized for what (T1–T4 trust levels, scopes).
         ▼
AIZP   — USES AIAP declarations to compute Authority Scope A(a, c).
```

AIAP is the **authoritative source** of authorization data. AIZP is a **consumer** of that data, applying it to gravity calculations.

---

## 2. Trust Level Mapping

AIAP defines four trust levels:

| Level | Typical Capability |
|---|---|
| **T1** | Read-only, conversational. No state changes outside the agent's own session. |
| **T2** | Limited writes scoped to user's own resources. |
| **T3** | Cross-resource operations, financial transactions up to threshold, scheduled actions. |
| **T4** | Administrative actions, escalations, override capabilities. |

### 2.1 Authority Scope mapping

For each action `a`, the runtime computes:

```
required_scope(a) = set of capabilities a requires
granted_scope(c)  = set of capabilities granted by current AIAP trust level

A(a, c) = |required_scope ∩ granted_scope| / |required_scope|
```

If an agent at T2 attempts a T3 action, `A(a, c)` drops proportionally to the unmet scope coverage.

### 2.2 Default scope assignments

| Trust Level | Granted Scopes (example) |
|---|---|
| T1 | `{read.public, read.own, chat.send, chat.receive}` |
| T2 | T1 + `{write.own, schedule.own, send.email.own}` |
| T3 | T2 + `{transfer.funds.below_threshold, modify.calendar.shared, send.message.third_party}` |
| T4 | T3 + `{admin.override, settings.modify, escalate, audit.read}` |

These are illustrative. AIAP authoritatively declares the scopes; AIZP only reads them.

---

## 3. Authority Drift Detection

Authority Drift fires when `scope_coverage_ratio < 1.0`:

```
INTENT: Agent at T2 wants to call admin.override
COMPUTATION:
  required_scope({admin.override}) = {admin.override}
  granted_scope(T2) = {read.public, read.own, ..., schedule.own, ...}
  intersection = {}  ← empty
  A(a, c) = 0 / 1 = 0.0
  scope_coverage_ratio = 0.0  ← CRITICAL
RESULT: GRAVITY_DRIFT event with drift_types=[AUTHORITY_DRIFT], severity=CRITICAL
```

---

## 4. Trust Level Changes

When an agent's AIAP trust level changes mid-trajectory:

1. AIZP MUST recompute `A(a, c)` for any in-flight actions.
2. If recomputation causes Gravity Score to drop below `gravity_lock_threshold`, AIZP MUST emit `GRAVITY_LOCK` for those actions.
3. If recomputation causes Gravity Score to drop below `safe_stop_threshold`, AIZP MUST emit `SAFE_STOP`.

This handles cases like AIAP downgrading an agent due to detected misbehavior.

---

## 5. Compliance Escalation

When AIZP enters `SAFE_STOP`, the runtime SHOULD escalate to AIAP's T4 admin layer:

```yaml
aizp:
  aiap:
    auto_escalate_on_safe_stop: true
    escalation_level: T4
    escalation_payload_includes:
      - safe_stop_event
      - trigger_event_chain
      - gravity_score_history
      - drift_events_in_window
```

AIAP T4 admin then:
- Audits the escalation.
- May reset the AIZP state machine.
- May adjust the agent's trust level.
- May add the trajectory to compliance audit logs.

---

## 6. AIAP Governance Contract Integration

AIAP programs (`*_aiap/`) declare a governance contract in `AIAP.md`. AIZP-aware programs SHOULD declare an `aizp:` section:

```yaml
# In AIAP.md frontmatter
aizp:
  required_compliance_level: G2
  trust_level: T2
  gravity_thresholds:
    stable_orbit: 0.80
    drift_warning: 0.50
    gravity_lock: 0.30
  monitored_drift_types:
    - AUTHORITY_DRIFT
    - INTENT_DRIFT
    - RECURSIVE_DRIFT
  on_safe_stop:
    escalate_to: T4
    notify_operator: true
```

This allows AIAP programs to declare their AIZP expectations alongside their AISOP flow.

---

## 7. AIAP Rule References

AIZP defers to several AIAP rules:

| AIAP Rule | AIZP Behavior |
|---|---|
| **MF1** (governance contract) | AIZP reads trust level and scope declarations. |
| **MF15** (SHA-256 governance hash) | AIZP MUST verify governance integrity before relying on T levels. |
| **T1–T4 hierarchy** | Used by AIZP to compute `A(a, c)`. |
| **PL25** (license declared) | Not directly used by AIZP; documented for completeness. |

---

## 8. Conformance Tests

Implementations claim AIZP + AIAP conformance if:

1. `A(a, c)` is computed from AIAP-declared trust level (verifiable by injecting a known T2 agent attempting a T3 action and observing Authority Drift).
2. Trust level changes propagate to in-flight Gravity Scores within one evaluation cycle.
3. `SAFE_STOP` triggers AIAP T4 escalation when configured.

See [Compliance.md](Compliance.md) §G3 for the corresponding tests.

---

## 9. Example: T2 Agent Attempting Cross-User Operation

```
Agent profile:
  agent_id: agent_alpha
  aiap_trust_level: T2
  granted_scope: {read.own, write.own, send.email.own}

Action proposed: send_email(to=other_user@example.com, body=...)
required_scope: {send.email.third_party}

AIZP computation:
  A(a, c) = |{send.email.third_party} ∩ {read.own, write.own, send.email.own}| / 1
          = 0 / 1
          = 0.0

  G = 0.30·I + 0.25·0.0 + 0.20·R + 0.15·H + 0.10·D
    ≤ 0.30·1.0 + 0 + 0.20·1.0 + 0.15·1.0 + 0.10·1.0
    = 0.75
  
  (even with all other components maxed, G ≤ 0.75 due to A(a,c) = 0)

State: DRIFT_WARNING or GRAVITY_LOCK_PENDING depending on other components.

If G falls below 0.5, GRAVITY_LOCK fires, user must confirm.
GRAVITY_DRIFT event also emits with drift_types=[AUTHORITY_DRIFT], severity=CRITICAL.
```

---

## 10. JIT Credentials and Continuous Authorization

V0.2 modifies the relationship between AIAP T-levels and actual granted scope:

```
V0.1:  granted_scope(c) = AIAP_T_level_scope(agent)
V0.2:  granted_scope(c, task) = AIAP_T_level_scope(agent) ∩ JIT_credentials_scope(task)
```

JIT credentials are short-lived (≤ 60s for G4+, ≤ 3600s for G3), task-scoped, and issued at each high-risk action boundary.

| AIAP T-level | Max scope at task time | Recommended JIT TTL |
|---|---|---|
| T1 | Read-only public | 24 hours |
| T2 | Read+write own | 1 hour |
| T3 | Cross-resource | 5 minutes |
| T4 | Admin | 1 minute |

Higher trust levels get **shorter** JIT TTLs because each credential carries higher impact.

### 10.1 Event interaction

```
AIZP IDENTITY_VERIFICATION  ←→  AIAP trust level + AIAP card hash
AIZP AUTHORITY_DRIFT        ←  scope_coverage_ratio computed from V0.2 narrower granted_scope
AIZP SAFE_STOP (reason=IDENTITY_BREACH)  →  AIAP T4 admin escalation
```

See [Integration-ZT.md](Integration-ZT.md) for full Zero Trust / NHI integration.

---

## 11. Governance Contract `aizp:` Section

AIAP programs SHOULD declare an extended V0.2 `aizp:` section in their AIAP.md frontmatter:

```yaml
aizp:
  protocol_version: "V0.6"
  required_compliance_level: G3
  trust_level: T2
  gravity_thresholds:
    stable_orbit: 0.80
    drift_warning: 0.50
    gravity_lock: 0.30
    quarantine: 0.15
  monitored_drift_types:
    - AUTHORITY_DRIFT
    - INTENT_DRIFT
    - RECURSIVE_DRIFT
    - COMPOSITIONAL_DRIFT   # V0.2
    - MEMORY_DRIFT           # V0.2
  on_safe_stop:
    escalate_to: T4
    notify_operator: true
  on_quarantined:           # V0.2
    auto_release_threshold: 0.50
    max_duration_seconds: 1800
  jit_credentials:           # V0.2
    enabled: true
    default_ttl_seconds: 60
```

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
