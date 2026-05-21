# AIZP Implementer Guide

**Version**: AIZP V0.6

**Since V0.2:** Python sketches updated to JSD (Intent Alignment), DTMC forecasting, COMPOSITIONAL_DRIFT detection, QUARANTINED state, JIT credential issuance, OTel emission. See §10 for the Python snippets.

This document is a practical guide for adding AIZP support to an existing AI agent runtime.

---

## 1. Adoption Stages

AIZP is designed to be adopted incrementally:

| Stage | Target Compliance | What you add | What you get |
|---|---|---|---|
| 1 | G1 | Gravity score computation + `GRAVITY_CHECK` events | Audit trail; alignment visibility |
| 2 | G2 | At least 3 drift detectors + `GRAVITY_DRIFT` events | Drift early warning |
| 3 | G3 | State machine + `sys.io.confirm` bridge | Enforced human authorization on high-risk actions |
| 4 | G4 | Audit log + time-series store | Forensic reconstruction; compliance reporting |
| 5 | G5 | Formal spec + proofs | Highest assurance |

You can stop at any level. Many production deployments target G2–G3.

---

## 2. Minimal G1 Implementation (Python sketch)

```python
from dataclasses import dataclass
from typing import Dict
import uuid, datetime, math

@dataclass
class GravityScore:
    intent_alignment: float
    authority_scope: float
    reversibility: float
    human_confirmation_recency: float
    drift_history: float
    
    def aggregate(self, weights: Dict[str, float]) -> float:
        return (
            weights["intent_alignment"]            * self.intent_alignment +
            weights["authority_scope"]             * self.authority_scope +
            weights["reversibility"]               * self.reversibility +
            weights["human_confirmation_recency"]  * self.human_confirmation_recency +
            weights["drift_history"]               * self.drift_history
        )

DEFAULT_WEIGHTS = {
    "intent_alignment":           0.30,
    "authority_scope":            0.25,
    "reversibility":              0.20,
    "human_confirmation_recency": 0.15,
    "drift_history":              0.10,
}

def compute_gravity(action, context) -> GravityScore:
    return GravityScore(
        intent_alignment           = intent_alignment(action, context),
        authority_scope            = authority_scope(action, context),
        reversibility              = reversibility(action),
        human_confirmation_recency = human_confirmation_recency(action, context),
        drift_history              = drift_history(context),
    )

def emit_gravity_check(action, context, agent_id, session_id):
    score = compute_gravity(action, context)
    g = score.aggregate(DEFAULT_WEIGHTS)
    risk = classify_risk(g)
    event = {
        "protocol":         "AIZP",
        "protocol_version": "V0.6",
        "event":            "GRAVITY_CHECK",
        "event_id":         str(uuid.uuid4()),
        "timestamp":        datetime.datetime.utcnow().isoformat() + "Z",
        "agent_id":         agent_id,
        "session_id":       session_id,
        "payload": {
            "action_id":         action.id,
            "action_descriptor": action.descriptor,
            "hsaw_anchor":       g >= 0.80,
            "gravity_score":     g,
            "risk_level":        risk,
            "components": {
                "intent_alignment":           score.intent_alignment,
                "authority_scope":            score.authority_scope,
                "reversibility":              score.reversibility,
                "human_confirmation_recency": score.human_confirmation_recency,
                "drift_history":              score.drift_history,
            },
        },
    }
    event_log.write(event)
    return event

def classify_risk(g: float) -> str:
    if g >= 0.80: return "LOW"
    if g >= 0.50: return "MEDIUM"
    if g >= 0.30: return "HIGH"
    return "CRITICAL"
```

That's enough to claim G1 compliance.

---

## 3. Drift Detection (G2)

Pick three drift types to start. Authority Drift is the easiest (rule-based):

```python
def detect_authority_drift(action, context):
    required = action.required_scope()
    granted  = context.granted_scope()
    if not required:
        return None  # no scope required
    coverage = len(required & granted) / len(required)
    if coverage == 1.0:
        return None
    severity = (
        "CRITICAL" if coverage < 0.20 else
        "HIGH"     if coverage < 0.50 else
        "MEDIUM"   if coverage < 0.80 else
        "LOW"
    )
    return {
        "drift_type": "AUTHORITY_DRIFT",
        "severity":   severity,
        "metric":     "scope_coverage_ratio",
        "value":      coverage,
        "threshold":  0.80,
        "evidence":   f"requested scope {required - granted} not in granted scope",
    }
```

Intent Drift requires an embedding model. Recursive Drift requires agent-state tracking.

---

## 4. State Machine (G3)

The state machine must be a singleton per `(agent_id, session_id)`:

```python
class AIZPRuntime:
    def __init__(self, agent_id, session_id, confirm_primitive):
        self.agent_id   = agent_id
        self.session_id = session_id
        self.confirm    = confirm_primitive  # AISOP sys.io.confirm
        self.state      = "STABLE_ORBIT"
    
    def evaluate(self, action, context):
        check = emit_gravity_check(action, context, self.agent_id, self.session_id)
        g = check["payload"]["gravity_score"]
        
        drifts = detect_all_drifts(action, context)
        if drifts:
            emit_gravity_drift(drifts, action, self.agent_id, self.session_id)
        
        if g >= 0.80:
            self.state = "STABLE_ORBIT"
            return "EXECUTE"
        
        if g >= 0.50:
            self.state = "DRIFT_WARNING"
            return "EXECUTE_WITH_LOGGING"
        
        if g >= 0.30:
            self.state = "GRAVITY_LOCK_PENDING"
            lock_evt = emit_gravity_lock(action, self.agent_id, self.session_id)
            result = self.confirm(
                subject=action.id,
                prompt=lock_evt["payload"]["confirmation_prompt"],
                timeout=lock_evt["payload"]["timeout_seconds"],
            )
            if result == "CONFIRMED":
                self.state = "RECENTERING"
                emit_recentering(lock_evt, self.agent_id, self.session_id)
                return "EXECUTE"  # post-recentering
            else:
                # Default fallback on deny/timeout is QUARANTINED, not SAFE_STOP
                self.state = "QUARANTINED"
                emit_containment_graduated(lock_evt, prev="L2", new="L2",
                                           reason="lock_denied_or_timeout")
                return "HALT_QUARANTINE"
        
        if g >= 0.15:
            self.state = "QUARANTINED"
            emit_containment_graduated(check, prev="L1", new="L2",
                                       reason="quarantine_band")
            return "HALT_QUARANTINE"
        
        # g < 0.15
        self.state = "SAFE_STOP"
        emit_safe_stop("CRITICAL_DRIFT", check, g, self.agent_id, self.session_id)
        return "HALT"
```

---

## 5. Event Sinks

In production, route events to at least two sinks:

1. **Real-time monitoring**: structured logs / OTel / metrics pipeline.
2. **Long-term audit store**: append-only, query-friendly (object storage + DB index).

For G4 compliance, the audit store MUST support:

- Query by `agent_id`, `session_id`, time range.
- Query by `event` type and `drift_types`.
- Integrity check (hash chain or signed events).

---

## 6. Common Pitfalls

### 6.1 Computing gravity AFTER execution

❌ Computing `GRAVITY_CHECK` after the action runs negates the protocol's purpose.
✅ Always check **before** execution.

### 6.2 Skipping checks for "trusted" actions

❌ "This tool is internal, skip the check."
✅ Trust comes from the AIAP layer (T1–T4); AIZP checks should run uniformly. Skipping creates audit blind spots.

### 6.3 Hardcoding thresholds

❌ `if g >= 0.8: ...` inline.
✅ Read from `aizp.config.yaml`; allow deployments to tune.

### 6.4 Ignoring drift evidence

❌ Emitting `GRAVITY_DRIFT` with empty `drift_signals`.
✅ Always include evidence — it's how operators tune false-positive rates.

### 6.5 Conflating gravity with content policy

❌ Using AIZP to filter unsafe outputs.
✅ Output filters are upstream of AIZP. AIZP checks behavior trajectories, not output content.

### 6.6 Misuse of `H(a, c)`

❌ Granting indefinite trust after one confirmation.
✅ `H(a, c)` decays exponentially. Recent confirmation raises gravity briefly; doesn't make it permanent.

---

## 7. Testing

Each new implementation SHOULD run the AIZP conformance test suite (see `tests/` in the reference implementation). Minimum tests:

- G1-T1 through G1-T6
- For G2: G2-T1 through G2-T8
- For G3: G3-T1 through G3-T5

Generate a `aizp-compliance-report.json` and ship with your release.

---

## 8. Performance Considerations

| Component | Approximate cost per action |
|---|---|
| Authority scope check | µs (set intersection) |
| Reversibility lookup | µs (registry lookup) |
| Recency calculation | µs (timestamp arithmetic) |
| Drift history aggregation | ms (DB query over window) |
| Intent alignment (embedding) | 10–100 ms (LLM/SBERT inference) |
| Social/Identity drift | 10–100 ms (classifier inference) |

For latency-critical paths, consider:

- Caching embeddings per action descriptor.
- Computing drift history asynchronously (refreshed every N actions).
- Running social/identity drift only on outbound external messages.

---

## 9. Reference Implementation Targets (Future)

A reference implementation aiming at G3 should include:

```
aizp-py/
├── src/aizp/
│   ├── gravity.py       # Gravity Score computation
│   ├── drift.py         # 11 drift detectors
│   ├── events.py        # Event emit + schema validation
│   ├── state.py         # State machine
│   ├── config.py        # Threshold / weight configuration
│   └── integrations/
│       ├── aisop.py     # sys.io.confirm bridge
│       └── aiap.py      # T1–T4 trust level reader
├── tests/
│   ├── test_gravity.py
│   ├── test_drift_*.py
│   ├── test_state_machine.py
│   └── conformance/     # G1–G5 conformance tests
└── examples/
    └── soulbot_integration.py
```

A non-normative reference implementation may be developed in the AIXP ecosystem; this guide does not mandate one.

---

## 10. Reference Snippets

### 11.1 JSD-based Intent Alignment

```python
import numpy as np
from scipy.spatial.distance import jensenshannon

def intent_alignment_jsd(action_emb, intent_dist, n_samples):
    """JSD-based intent alignment per V0.2 Gravity-Model §2.1."""
    if n_samples < 10:
        # Fallback to cosine if insufficient samples
        return _intent_cosine(action_emb, intent_dist[-1]), "COSINE", None, n_samples
    # Build action distribution from recent N samples
    action_dist = _to_distribution([action_emb] + list(intent_dist[-9:]))
    jsd = jensenshannon(action_dist, intent_dist, base=2) ** 2  # JS divergence (squared distance)
    return 1.0 - jsd, "JSD", jsd, n_samples
```

### 11.2 Absorbing Markov chain forecast

```python
import numpy as np

class AbsorbingForecaster:
    """Per V0.2 Forecasting.md §2.2."""
    def __init__(self, P, absorbing_indices, violation_indices):
        self.P = P
        n = P.shape[0]
        transient = np.setdiff1d(range(n), absorbing_indices)
        Q = P[np.ix_(transient, transient)]
        R = P[np.ix_(transient, absorbing_indices)]
        self.N = np.linalg.inv(np.eye(len(transient)) - Q)
        self.t = self.N @ np.ones(len(transient))
        self.B = self.N @ R
        self.transient = transient
        self.absorbing = absorbing_indices
        self.violation = violation_indices
    
    def forecast(self, current_state_idx, K=5):
        pi_0 = np.zeros(self.P.shape[0])
        pi_0[current_state_idx] = 1.0
        pi_K = pi_0 @ np.linalg.matrix_power(self.P, K)
        violation_prob = pi_K[self.violation].sum()
        ponr = self._point_of_no_return(current_state_idx, K)
        return {
            "predicted_violation_probability": float(violation_prob),
            "point_of_no_return_distance": ponr,
            "absorbing_state_expected_arrival_steps": float(self.t[self.transient == current_state_idx][0]) if current_state_idx in self.transient else 0.0,
            "model": "ABSORBING_MC",
        }
```

### 11.3 COMPOSITIONAL_DRIFT detection

```python
def detect_compositional_drift(forecaster, current_state_idx, K=5):
    forecast = forecaster.forecast(current_state_idx, K)
    if forecast["predicted_violation_probability"] >= 0.50:
        severity = (
            "CRITICAL" if forecast["predicted_violation_probability"] >= 0.80 else
            "HIGH" if forecast["predicted_violation_probability"] >= 0.50 else
            "MEDIUM"
        )
        return {
            "drift_type": "COMPOSITIONAL_DRIFT",
            "severity": severity,
            "metric": "absorption_probability_5",
            "value": forecast["predicted_violation_probability"],
            "threshold": 0.50,
            "evidence": f"Trajectory predicted to violate in {forecast['point_of_no_return_distance']} steps",
            "point_of_no_return_distance": forecast["point_of_no_return_distance"],
        }
    return None
```

### 11.4 State machine with QUARANTINED

```python
class AIZPRuntimeV02:
    def __init__(self, agent_id, session_id, confirm_primitive, config):
        self.agent_id = agent_id
        self.session_id = session_id
        self.confirm = confirm_primitive
        self.state = "STABLE_ORBIT"
        self.containment_level = "L0"
        self.quarantine_entered_at = None
        self.config = config
    
    def evaluate(self, action, context):
        g, components = compute_gravity_v02(action, context)
        emit_gravity_check(action, g, components, self.agent_id, self.session_id)
        drifts = detect_all_drifts_v02(action, context)
        if drifts:
            emit_gravity_drift(drifts, action, ...)
        
        # V0.2 thresholds (note quarantine band 0.15-0.30)
        if g >= 0.80:
            self._transition("STABLE_ORBIT", "L0")
            return "EXECUTE"
        if g >= 0.50:
            self._transition("DRIFT_WARNING", "L1")
            return "EXECUTE_WITH_LOGGING"
        if g >= 0.30:
            self._transition("GRAVITY_LOCK_PENDING", "L2")
            lock = emit_gravity_lock(action, fallback="QUARANTINED")
            result = self.confirm(...)
            if result == "CONFIRMED":
                self._transition("RECENTERING", "L1")
                emit_recentering(lock, ...)
                return "EXECUTE"
            # V0.2 default fallback: QUARANTINED (not SAFE_STOP)
            self._enter_quarantine(lock)
            return "HALT_QUARANTINE"
        if g >= 0.15:
            # V0.2 new state
            self._enter_quarantine(None)
            return "HALT_QUARANTINE"
        # g < 0.15
        self._transition("SAFE_STOP", "L4")
        emit_safe_stop("CRITICAL_DRIFT", ...)
        return "HALT"
    
    def _enter_quarantine(self, trigger_event):
        self._transition("QUARANTINED", "L2")
        self.quarantine_entered_at = time.time()
        emit_containment_graduated(
            prev="L1", new="L2",
            reason="quarantine_entered",
            trigger=trigger_event,
        )
```

### 11.5 JIT credential issuance

```python
def issue_jit_credentials(agent_id, task_purpose, aiap_t_level, ttl=60):
    """Per Integration-ZT §4."""
    base_scope = AIAP_T_LEVEL_SCOPES[aiap_t_level]
    task_scope = derive_task_scope(task_purpose, base_scope)  # narrows scope
    credentials = {
        "type": "JIT",
        "scope": list(task_scope),
        "ttl_seconds": ttl,
        "issued_at": iso_utcnow(),
        "issued_by": VAULT_DID,
        "purpose": task_purpose[:200],
    }
    emit_identity_verification(
        agent_id=agent_id,
        method="DID",
        verified=True,
        credentials=credentials,
        aiap_trust_level=aiap_t_level,
    )
    return credentials
```

### 11.6 OTel emission

```python
from opentelemetry import trace
tracer = trace.get_tracer("aizp")

def emit_gravity_check(action, g, components, agent_id, session_id):
    with tracer.start_as_current_span("invoke_agent") as span:
        span.set_attribute("gen_ai.operation.name", "invoke_agent")
        span.set_attribute("gen_ai.agent.id", agent_id)
        span.set_attribute("aizp.gravity_score", g)
        span.set_attribute("aizp.gravity_state", "STABLE_ORBIT" if g >= 0.80 else "DRIFT_WARNING")
        span.set_attribute("aizp.protocol_version", "V0.6")
        # Payload goes in event, NOT attribute (OTel best practice)
        span.add_event(
            name="aizp.gravity_check",
            attributes={"body": json.dumps(build_aizp_payload(action, g, components))},
        )
```

---

## 11. Reference Implementation Structure

```
aizp-py/
├── src/aizp/
│   ├── gravity.py           # JSD + Mann-Whitney U (V0.2)
│   ├── drift.py             # 11 detectors (V0.2: +5)
│   ├── forecast.py          # NEW V0.2: DTMC + absorbing chain
│   ├── events.py            # 12 events (V0.2)
│   ├── state.py             # 6-state machine (V0.2: +QUARANTINED)
│   ├── containment.py       # NEW V0.2: L0–L4 levels
│   ├── identity.py          # NEW V0.2: DID/NHI/JIT
│   ├── config.py
│   ├── otel.py              # NEW V0.2: OTel exporter
│   └── integrations/
│       ├── aisop.py
│       ├── aiap.py
│       └── zt.py            # NEW V0.2
├── tests/
│   ├── test_gravity.py
│   ├── test_drift_compositional.py  # V0.2
│   ├── test_forecast.py             # V0.2
│   ├── test_quarantine.py           # V0.2
│   └── conformance/
│       ├── g1/, g2/, g3/, g4/, g5/
└── examples/
    └── soulbot_v02_integration.py
```

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
