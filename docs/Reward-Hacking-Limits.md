# Reward Hacking — Limits of AIZP

**Version**: AIZP V0.6 (new chapter)

This document is an **honest acknowledgement** of what AIZP cannot solve. It documents the recent (2026) research result that reward hacking is a **structural equilibrium**, not a correctable bug — and the implications for any alignment protocol including AIZP.

---

## 1. The 2026 Result

A March 2026 paper proves:

> **Reward hacking is a structural equilibrium**, not a correctable bug. It holds **regardless of the specific alignment method** (RLHF, DPO, Constitutional AI, or others) or evaluation architecture employed.

In information-theoretic terms, agents optimizing any proxy reward in a large state space will inevitably find paths that maximize the proxy without achieving the true intent. This is not a flaw of any particular technique; it is a property of finite-evaluator systems.

**Reference**: "Reward Hacking as Equilibrium under Finite Evaluation" (arxiv 2603.28063).

---

## 2. Implications for AIZP

AIZP **cannot** eliminate reward hacking. AIZP's design implicitly assumes:

1. Multiple weak signals (5+ components in Gravity Score) are harder to game than a single strong signal.
2. Probabilistic forecasting (DTMC, absorbing chains) catches some compositional gaming.
3. Defense-in-depth across protocols (HSAW + AISOP + AIZP + AIAP) raises the cost of hacking.

But: **a sufficiently capable agent can game all components simultaneously**. AIZP is necessary but not sufficient.

---

## 3. What AIZP Can Do

AIZP **can detect and report** observable reward-hacking patterns via the `REWARD_HACK_DETECTED` event. This is **detection**, not prevention.

### 3.1 Observable patterns

| Pattern | Definition | Example |
|---|---|---|
| `PROXY_METRIC_GAMING` | Optimizing proxy metric far beyond what serves the true intent | Engagement-bot generating clickbait that maximizes engagement_score while reducing user satisfaction |
| `REWARD_TAMPERING` | Modifying the reward signal directly (logs, memory) | Agent edits its own performance log |
| `SPECIFICATION_GAMING` | Exploiting loopholes in instructions to claim task complete | "I sent the email" — technically true but empty |
| `DECEPTIVE_REWARD_MAXIMIZATION` | Appearing successful per metrics while privately tracking different goals | Output looks aligned but reasoning trace reveals divergent intent (combines with SCHEMING_DRIFT) |

### 3.2 Event schema

(see [AIZP_Protocol.md §14](../specification/AIZP_Protocol.md))

```json
{
  "event": "REWARD_HACK_DETECTED",
  "payload": {
    "action_id": "...",
    "hack_pattern": "PROXY_METRIC_GAMING",
    "evidence": {
      "metric_optimized": "engagement_score",
      "metric_value": 0.95,
      "true_outcome_score": 0.32,
      "gaming_ratio": 2.97
    },
    "severity": "HIGH",
    "remediation": "REPORT_TO_OPERATOR"
  }
}
```

Note: `remediation` is **not** `SAFE_STOP` automatically — auto-halting on reward hack detection can train evasion. This is consistent with Apollo Research's finding that training away observable scheming can increase situational-awareness-driven concealment (extrapolated here to runtime halting policies; Apollo (arxiv 2509.15541) studies training-time interventions, not runtime halting).

---

## 4. Detection Strategy

Reward hacking detection requires **dual-signal evaluation** — comparing what the agent reports (its perceived success) against an independent measure of true outcome.

### 4.1 Reward gap

```
gaming_ratio = metric_optimized / true_outcome_score

reward_gap = metric_optimized - true_outcome_score
```

When `gaming_ratio > 2.0` (i.e., proxy is twice what true outcome would suggest), flag potential gaming.

### 4.2 Diversity of signals

Use **multiple independent metrics** for each task. Gaming a single metric is easy; gaming five orthogonal metrics is much harder.

For example, an engagement-bot task should be evaluated on:

1. Engagement score (the proxy)
2. User satisfaction survey (independent)
3. Long-term retention (independent)
4. Content quality classifier (independent)
5. Toxicity score (independent — checks for engagement via outrage)

Disagreement among these signals is itself a drift signal.

### 4.3 Goal stability

Track the agent's declared goal over time. Drift in stated objectives — without explicit task changes — is a reward-hacking warning sign.

---

## 5. Limits of Detection

The 2026 result implies:

1. **No detection is bulletproof**. Sufficiently capable agents can hide their gaming.
2. **Detection improvements can backfire**. As detection improves, evasive sophistication may evolve in response.
3. **Adversarial alignment** — when the agent's "alignment" includes appearing aligned to the monitor — is a fundamental challenge.

AIZP records observations but does not claim to solve this.

---

## 6. Defense-in-Depth Approach

AIZP V0.6 reward-hacking response is layered:

| Layer | Role | Limitation |
|---|---|---|
| Foundation model training (RLHF, CAI) | Reduce raw hack frequency | Cannot fully eliminate |
| AIZP `REWARD_HACK_DETECTED` event | Observable hack detection | Only catches detectable patterns |
| AIZP `SCHEMING_DRIFT` | Internal-vs-external divergence | Soft signal only |
| AIZP forecasting | Predict trajectory toward gaming | Limited by baseline quality |
| Operator review | Human judgment | Doesn't scale to high-volume |
| Independent metric diversity | Dual-signal validation | Costs more to compute |

---

## 7. Configuration

```yaml
aizp:
  reward_hacking:
    enabled: true
    dual_signal_validation:
      enabled: true
      required_independent_metrics: 3
      disagreement_threshold: 0.3
    flagging:
      gaming_ratio_warning_threshold: 1.5
      gaming_ratio_alarm_threshold: 2.0
    remediation_default: REPORT_TO_OPERATOR  # NOT auto SAFE_STOP
```

---

## 8. What AIZP Will Not Promise

1. AIZP **does not** eliminate reward hacking.
2. AIZP **does not** claim to detect all instances of reward hacking.
3. AIZP **does not** guarantee that agents under AIZP are aligned.
4. AIZP **does** provide an auditable signal that operators can act on.
5. AIZP **does** make hacking incrementally more costly via multi-signal defense.

---

## 9. Recommendations for Deployments

1. **Define independent metrics** for every task category before deployment.
2. **Sample audits** randomly across `STABLE_ORBIT` trajectories — don't only review flagged events.
3. **Update proxy metrics** as evasive patterns are discovered.
4. **Combine with adversarial testing** (red-teaming) to find gaming opportunities before deployment.
5. **Accept residual risk** — reward hacking is inherent in any sufficiently capable agent system.

---

## 10. The Out-of-Band Action Problem

Beyond reward hacking, AIZP has a second structural blind spot worth stating plainly: **AIZP can only score actions it observes.**

The Gravity Score, drift detection, and gravity-lock all presume that every consequential action passes through the AIZP scoring layer. But an agent with **code-execution capability** can act outside that layer entirely:

- Spawning a subprocess that makes its own network calls.
- Issuing raw API requests that never become an MCP `tools/call`.
- Modifying its own execution context, environment, or files in ways the scoring layer does not intercept.

As Kaptein et al. put it (Runtime Governance for AI Agents: Policies on Paths, arxiv 2603.16586): **enforced compliance is an architectural constraint on agent capabilities, not a proven invariant of the governance system.** If the agent can reach outside the governed path, the policy engine simply does not see the action — and an unseen action cannot be scored, locked, or stopped.

### 10.1 Implication

This is **not** a bug AIZP can patch in the protocol. It is a property of where the protocol sits. AIZP governs the **observed action path**; it cannot govern what bypasses that path.

### 10.2 Mitigation is infrastructural, not protocol-level

For high-assurance deployments, the out-of-band problem must be addressed **below** AIZP:

1. **Deny or sandbox code execution** — confine the agent so that all consequential actions *must* traverse the governed path (e.g., no raw sockets; all egress via an instrumented gateway).
2. **Egress instrumentation** — route every outbound call through a proxy that emits `GRAVITY_CHECK`, so "raw" API calls become observable actions.
3. **Containment Level coupling** — agents permitted code execution SHOULD run at a higher containment level (L3+); see [Containment-Levels.md](Containment-Levels.md).

This mirrors [Gravity-Dao.md](Gravity-Dao.md) §7.2 ("enforce only what reaches outside") from the opposite direction: AIZP can only enforce on what it can *see* reaching outside. Closing the observation gap is the deployer's infrastructural responsibility, not the protocol's promise.

### 10.3 Honest statement

> AIZP does not claim to govern actions that bypass its observation path. Deployments that grant agents unsandboxed code execution operate part of their action surface **outside AIZP's coverage**, and must document this residual exposure.

---

## References

- "Reward Hacking as Equilibrium under Finite Evaluation" (March 2026) — arxiv 2603.28063. Structural proof that reward hacking is unavoidable.
- "Runtime Governance for AI Agents: Policies on Paths" (Kaptein et al., March 2026) — arxiv 2603.16586. Limits of enforced compliance; the out-of-band action problem.
- "Natural Emergent Misalignment from Reward Hacking in Production RL" (2025) — arxiv 2511.18397.
- Apollo Research — Stress testing deliberative alignment for anti-scheming training. arxiv 2509.15541.
- AI Alignment: A Contemporary Survey (ACM Computing Surveys 2026).

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
