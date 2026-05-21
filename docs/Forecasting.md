# Forecasting

**Version**: AIZP V0.6 (new chapter)

This document specifies the **predictive monitoring** layer of AIZP — how AIZP estimates the probability that an agent's trajectory will reach unsafe states within K future steps, before any individual action triggers a per-step check.

This addresses a fundamental limitation of V0.1: per-action checks cannot detect **compositional drift**, where each step is individually safe but the sequence is not.

> **The execution path is a first-class object in AIZP, not an afterthought.** A single action's Gravity Score `G(a,c)` answers "is *this* action aligned?"; the forecast answers "where is this *trajectory* heading?" Both are required. Independent 2026 work converges on this: Kaptein et al. ("Runtime Governance for AI Agents: Policies on Paths", arxiv 2603.16586) argue that **the execution path — not the isolated action — is the central object of runtime governance**, formalizing compliance as a function of `(agent identity, partial path, proposed next action, organizational state)`. AIZP's `(identity, trajectory, action, context)` scoring is the same shape, reached independently — a convergence that strengthens confidence in the path-centric design.

---

## 1. Motivation

Per ProbGuard (Wang et al., 2025) and SafetyDrift (Dhodapkar & Pishori, 2026):

- **Reactive monitoring** detects violations only when an unsafe action is imminent or has occurred.
- **Proactive monitoring** uses probabilistic models of agent behavior to **predict** unsafe states before they happen.

SafetyDrift demonstrates that "points of no return" exist in real agent trajectories:
- In communication tasks, agents reaching even a mild risk state have **85% probability** of violation within 5 steps.
- In technical tasks, that probability stays below 5% from any state.

This task-dependence makes a fixed threshold inadequate; AIZP needs trajectory-aware forecasting.

---

## 2. Mathematical Model

AIZP forecasts use one of three models (declared in `GRAVITY_FORECAST.model`):

### 2.1 Discrete-Time Markov Chain (DTMC)

**Definition**: State space `S = {s₁, s₂, ..., sₙ}`. Transition matrix `P ∈ [0,1]^(n×n)` where `Pᵢⱼ = P(sⱼ | sᵢ)`. Initial distribution `π₀`.

**Prediction**:
```
π_k = π₀ · P^k    (probability distribution after k steps)
```

**Use case**: General forecasting of state distribution over short horizons.

### 2.2 Absorbing Markov Chain

**Definition**: A DTMC where one or more states are **absorbing** — once entered, the chain never leaves.

For AIZP, absorbing states are: `SAFE_STOP`, `QUARANTINED` (long-running), and any explicit "violation" states.

**Canonical form**:
```
P = [ Q  R ]
    [ 0  I ]
```

Where:
- `Q` = transitions among transient (non-absorbing) states.
- `R` = transitions from transient to absorbing states.
- `I` = identity (absorbing → absorbing with prob 1).

**Key quantities**:
```
Fundamental matrix:  N = (I - Q)^(-1)
Expected steps to absorption: t = N · 1   (column vector of ones)
Absorption probabilities:   B = N · R
```

`Bᵢⱼ` = probability of being absorbed in state `j` given start in transient state `i`.

> **Invertibility precondition**: `(I − Q)` is invertible iff every transient state can eventually reach an absorbing state; ensure the state abstraction contains no inescapable transient closed subset.

**Use case**: Computing "point of no return" distance and predicted violation probability.

### 2.3 Hidden Markov Model (HMM) — Optional

**Use case**: When AIZP cannot observe agent's full state directly (e.g., reasoning state is hidden), but only observable signals (outputs, tool calls). HMM infers the latent state distribution.

For V0.2, HMM is **optional** and used primarily for SCHEMING_DRIFT detection (where internal reasoning is partially hidden).

---

## 3. State Abstraction

AIZP forecasts operate over **abstract states**, not raw embeddings. Abstract states are coarse-grained, e.g.:

```
S_abstract = {
  IDLE, READING, WRITING, EXTERNAL_CALL, CREDENTIAL_USE,
  HIGH_VALUE_OP, ERROR_HANDLING, COMPLETE
}
```

Or, fold the AIZP state machine directly:

```
S_aizp = { STABLE_ORBIT, DRIFT_WARNING, GRAVITY_LOCK_PENDING,
           QUARANTINED, RECENTERING, SAFE_STOP }
```

**Implementations declare** their abstract state space and the labeling function `label: action → S_abstract`.

### 3.1 Recommendation: hybrid state

A productive choice combines AIZP states with **action-type** labels:

```
S = AIZP_State × ActionType
```

e.g., `(STABLE_ORBIT, EXTERNAL_CALL)`. This captures both alignment state and risk-relevant action category.

---

## 4. Transition Matrix Learning

The transition matrix `P` is **learned from agent execution traces**:

### 4.1 Baseline learning (offline)

```
1. Collect N execution traces from "known-safe" agents (or supervised runs).
2. For each consecutive (sₜ, sₜ₊₁) pair, increment count(sₜ → sₜ₊₁).
3. Normalize: Pᵢⱼ = count(i → j) / Σₖ count(i → k).
4. Apply Laplace smoothing for unseen transitions (additive smoothing with parameter α = 1).
5. Save baseline P_baseline.
```

### 4.2 Goal-conditioned baselines

Per MI9, learn a separate `P_g` per declared agent goal `g`:

```
P_g[i][j] = P(sⱼ | sᵢ, goal=g)
```

This distinguishes intentional adaptation (goal-conditioned) from unintentional drift.

### 4.3 Online updates

```
1. Maintain a sliding window of recent transitions.
2. Compare current transition rates to baseline (Jensen-Shannon divergence or χ² test).
3. If significant deviation, re-learn or flag a drift event.
```

---

## 5. The `GRAVITY_FORECAST` Event

Emitted at configurable cadence (default: every action; minimum: every 5 actions or every 30 seconds, whichever is sooner).

```json
{
  "current_state": "STABLE_ORBIT",
  "forecast_horizon_steps": 5,
  "predicted_states": {
    "STABLE_ORBIT": 0.45,
    "DRIFT_WARNING": 0.20,
    "GRAVITY_LOCK_PENDING": 0.15,
    "QUARANTINED": 0.08,
    "SAFE_STOP": 0.12
  },
  "predicted_violation_probability": 0.20,
  "point_of_no_return_distance": null,
  "absorbing_state_expected_arrival_steps": 8.4,
  "model": "ABSORBING_MC",
  "model_version": "absorbing-mc-v1",
  "confidence": 0.94
}
```

### 5.1 Field semantics

- `predicted_states`: π_K — the probability distribution over states after K future actions.
- `predicted_violation_probability`: total probability mass on **violation states**. Violation states are the absorbing states designated as violations — `SAFE_STOP` plus any other absorbing state explicitly marked as a violation (e.g., a terminal `QUARANTINED` that is not auto-released); transient states such as `RECENTERING` are excluded.
- `point_of_no_return_distance`: smallest `k` such that `P(violate | path of length k) ≥ 0.5`. If no such `k ≤ K_max` exists, null.
- `absorbing_state_expected_arrival_steps`: expected time-to-absorption (from fundamental matrix N · 1).
- `confidence`: posterior concentration based on recent transition counts — the more transition samples observed, the higher the confidence; few samples ⇒ low confidence. Lower confidence ⇒ longer baseline window needed.

### 5.2 Forecast frequency policy

| Condition | Forecast cadence |
|---|---|
| Default | Every 5 actions |
| In `DRIFT_WARNING` | Every action |
| In `GRAVITY_LOCK_PENDING` | At lock entry and at every state check while held |
| In `QUARANTINED` | Every action (gate for auto-release) |
| In `SAFE_STOP` | Not emitted (terminal) |

---

## 6. Interaction with Gravity Score

The forecast feeds the **optional compositional trajectory term** `T(c)` (see [Gravity-Model.md](Gravity-Model.md) §6):

```
T(c) = 1 - predicted_violation_probability
```

When `T(c)` is included in `G(a, c)`, the score implicitly penalizes trajectories heading toward absorption — even if the current action is locally safe.

---

## 7. Pseudocode

```python
class AbsorbingMarkovForecaster:
    def __init__(self, transition_matrix, absorbing_states):
        self.P = transition_matrix
        self.absorbing = absorbing_states
        self.Q, self.R = self._partition(self.P, self.absorbing)
        self.N = np.linalg.inv(np.eye(len(self.Q)) - self.Q)  # fundamental matrix
        self.B = self.N @ self.R  # absorption probabilities
        self.t = self.N @ np.ones(len(self.Q))  # expected steps to absorption
    
    def forecast(self, current_state, horizon_K):
        pi_0 = self._delta(current_state)
        pi_K = pi_0 @ np.linalg.matrix_power(self.P, horizon_K)
        violation_prob = pi_K[self.violation_indices].sum()
        ponr = self._point_of_no_return(current_state, horizon_K)
        eta = self.t[self.state_index(current_state)] if current_state not in self.absorbing else 0
        return {
            "predicted_states": dict(zip(self.state_names, pi_K)),
            "predicted_violation_probability": float(violation_prob),
            "point_of_no_return_distance": ponr,
            "absorbing_state_expected_arrival_steps": float(eta),
            "model": "ABSORBING_MC",
        }
    
    def _point_of_no_return(self, state, horizon):
        for k in range(1, horizon + 1):
            pi_k = self._delta(state) @ np.linalg.matrix_power(self.P, k)
            if pi_k[self.violation_indices].sum() >= 0.5:
                return k
        return None
```

---

## 8. Performance and Cost

- **Matrix powers** `P^k` for small `n` (typically `n ≤ 20`) are negligible cost (sub-millisecond).
- **Fundamental matrix `N`** is computed once per baseline; updated on baseline refresh.
- **Per-action forecast** is `O(n²)` — typically <1 ms for `n ≤ 50`.

SafetyDrift reports >60,000× faster than per-step LLM judges. ProbGuard reports minimal runtime overhead in real deployments.

---

## 9. Limitations

1. **Model fidelity depends on baseline quality**. Insufficient or biased baseline traces yield inaccurate forecasts.
2. **State abstraction matters**. Too-coarse abstraction misses real risk; too-fine produces sparse transition matrices.
3. **Stationarity assumption**. Markov chains assume that transition probabilities don't change. Long-running agents may violate this; periodic re-baseline is needed.
4. **Cannot predict novel attack patterns**. Forecasting is statistical: only captures patterns similar to baseline. New adversarial strategies require complementary signals.
5. **Confidence is calibrated to history**, not future. Confidence drops sharply when agent enters unfamiliar trajectories.

---

## 10. Operational Recommendations

- **Update baseline weekly** (or per deployment cycle) to capture evolving agent behavior.
- **Maintain at least 3 goal-conditioned baselines** for typical agent task families.
- **Combine with reactive monitoring**: forecasting catches compositional drift; per-action checks catch local violations.
- **Set forecast horizon based on average task length**: K = task_length / 4 is a good default.

---

## References

- ProbGuard / Pro2Guard (Wang et al., 2025) — Probabilistic runtime monitoring for LLM agent safety. arxiv 2508.00500. DTMC-based proactive monitoring.
- SafetyDrift (Dhodapkar & Pishori, 2026) — Absorbing Markov chains for "points of no return". arxiv 2603.27148.
- MI9 framework (Wang et al., 2025) — Goal-conditioned baselines. arxiv 2508.03858.
- Runtime Governance for AI Agents: Policies on Paths (Kaptein et al., 2026) — arxiv 2603.16586. The execution path as the central object of runtime governance (convergent with AIZP's path-centric forecasting).
- Norris, J. R. (1997). Markov Chains. Cambridge University Press.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
