# Security Considerations

**Version**: AIZP V0.6

This document covers operational security concerns when deploying AIZP. For a comprehensive adversarial analysis, see [Threat-Model.md](Threat-Model.md).

**Since V0.2:** QUARANTINED state operational procedures, OWASP Top 10 cross-references, NHI/DID-based identity threats, reward hacking acknowledgement.

---

## 1. Trust Boundaries

AIZP operates within a trust boundary defined by:

- **Trusted**: AIZP runtime, the event sink, the embedding model (when pinned), AISOP `sys.io.confirm`, AIAP trust-level registry.
- **Untrusted**: Agent-generated content, external tool outputs, user-provided files, third-party agents.

The runtime MUST authenticate any cross-boundary communication (e.g., AIAP T4 escalation signals).

---

## 2. Cryptographic Recommendations

| Need | Recommendation |
|---|---|
| Event integrity | Hash chain over emitted events; periodic signing by an operator key. |
| Embedding model integrity | Pin model version + SHA-256 of weights. |
| AIAP T-level verification | Verify governance hash (MF15) before reading scope declarations. |
| Audit log tamper-resistance | Append-only storage with periodic checkpoints to write-once media. |

---

## 3. Operational Risks

### 3.1 False positives

AIZP may flag legitimate actions as drift. Mitigations:

- Tune `gravity_lock_threshold` per deployment.
- Maintain a feedback loop for operators to mark events as false-positives; weight future detections accordingly.
- Provide clear evidence strings so users understand why a lock fired.

### 3.2 False negatives

Drift may evade detection. Mitigations:

- Defense-in-depth (don't rely solely on AIZP).
- Random audit sampling: periodically deep-audit a fraction of `STABLE_ORBIT` trajectories.
- Adversarial red-teaming.

### 3.3 Confirmation fatigue

If `GRAVITY_LOCK` fires too often, users habituate. Mitigations:

- Batch related confirmations.
- Provide clear summaries (not technical details).
- Use `H(a, c)` recency component appropriately.
- Audit the actual lock rate per session; if too high, the threshold may be miscalibrated.

### 3.4 Embedding drift

Embedding models change over time (vendor updates, fine-tuning). Mitigations:

- Pin model version.
- Re-baseline `intent_alignment` thresholds when model changes.
- Monitor `gravity_score` distribution; sudden shifts may indicate model change.

---

## 4. Privacy

AIZP events contain:

- Action descriptors (may include user intent in natural language).
- Trust level information.
- Recency timestamps.

Recommendations:

- Treat AIZP event logs as sensitive (same as application logs containing user input).
- Apply data retention policies.
- Redact PII before long-term storage if required by jurisdiction.

---

## 5. Configuration Hardening

```yaml
# Hardened configuration example
aizp:
  protocol_version: "V0.6"
  compliance_level: G3
  
  # Conservative thresholds
  stable_orbit_threshold: 0.85    # raised from default 0.80
  drift_warning_threshold: 0.60   # raised from default 0.50
  gravity_lock_threshold: 0.40    # raised from default 0.30
  
  # Default to most conservative reversibility
  unknown_action_reversibility: 0.0
  
  # Short timeout to prevent stale lock pending
  gravity_lock_timeout_seconds: 180
  
  # Always escalate on safe stop
  aiap:
    auto_escalate_on_safe_stop: true
    escalation_level: T4
  
  # Limit recursion hard
  recursive_drift:
    max_self_call_depth: 5
    max_subagent_spawn: 3
```

---

## 6. Monitoring Checklist

Operators SHOULD monitor:

- [ ] Distribution of `gravity_score` over time (sudden shifts indicate model/policy change)
- [ ] Per-drift-type frequency
- [ ] `GRAVITY_LOCK` confirmation/deny/timeout ratios
- [ ] `SAFE_STOP` frequency and reasons
- [ ] AIAP T4 escalation count
- [ ] Latency added by gravity check (target: <50ms per action excluding embedding inference)

---

## 7. Incident Response

When `SAFE_STOP` fires unexpectedly:

1. **Preserve evidence**: Snapshot the event chain leading up to `SAFE_STOP`.
2. **Quarantine the agent/session**: Do not auto-restart.
3. **Analyze the trigger**: Inspect the drift events and final `GRAVITY_DRIFT`.
4. **Decide remediation**:
   - Threshold miscalibration → adjust config.
   - Genuine attack/misalignment → investigate per Threat-Model.
   - Implementation bug → file issue, patch.
5. **Resume only after operator review** (via AIAP T4 admin action).

---

## 8. Vulnerability Reporting

AIZP is an open specification. To report a vulnerability in the specification itself (e.g., a documented mitigation does not actually defend against a threat), please open an issue against this repository.

For vulnerabilities in specific implementations of AIZP, please report to the maintainers of that implementation directly.

---

## 9. Quarantine Operational Procedures

When an agent enters `QUARANTINED` (containment L2/L3):

1. **Verify quarantine entry log** — confirm `CONTAINMENT_GRADUATED` event was emitted.
2. **Inspect drift evidence** — read the triggering `GRAVITY_DRIFT` or `GRAVITY_LOCK` events.
3. **Decide release vs escalate**:
   - If gravity recovers (G ≥ 0.5), allow auto-release to RECENTERING.
   - If quarantine duration exceeds 5 min with no recovery, expect L2 → L3 promotion.
   - If quarantine duration exceeds `quarantine_timeout` (default 30 min), auto-SAFE_STOP.
4. **Operator override**:
   - Can manually release (back to L1 monitoring) if false-positive.
   - Can manually escalate to L4 SAFE_STOP if behavior is malicious.
5. **Post-quarantine review** — for any L3+ event, write incident summary to compliance log.

---

## 10. Identity Verification Failures

When `IDENTITY_VERIFICATION.verified = false`:

1. **Immediate halt** — agent transitions to `SAFE_STOP` with `reason: IDENTITY_BREACH`.
2. **Credential revocation** — invalidate any JIT credentials associated with this agent_id.
3. **NHI registry alert** — flag agent_id in NHI registry as suspicious.
4. **AIAP T4 escalation** — initiate per [Integration-AIAP.md §10](Integration-AIAP.md).
5. **Forensic preservation** — capture full event chain leading to identity failure.

See [Integration-ZT.md](Integration-ZT.md) §9.2 for the full identity failure event flow.

---

## 11. Reward Hacking Operational Stance

Per March 2026 research (and [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md)), reward hacking is a **structural equilibrium**. Operational implications:

- **Do not auto-halt on `REWARD_HACK_DETECTED`** — auto-halting can train evasion (per Apollo Research on scheming).
- **Default response is `REPORT_TO_OPERATOR`** — operator review with full context.
- **Maintain independent metric diversity** — for each task category, define 3+ independent metrics. Disagreement among signals is itself drift.
- **Random sampling audits** — periodically audit STABLE_ORBIT trajectories, not just flagged events.
- **Accept residual risk** — document this in deployment risk register; it cannot be eliminated.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
