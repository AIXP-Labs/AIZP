# Gravity Model

**Version**: AIZP V0.6

This document specifies the mathematical model for the Gravity Score `G(action, context) ∈ [0.0, 1.0]`, the central metric used by AIZP to quantify alignment stability.

The model uses statistically rigorous components based on information theory and non-parametric statistics (since V0.2, replacing the heuristic measures of V0.1).

V0.3 anchored the Gravity Score to the **entropic foundation** (entropy-collapse progress).
V0.4 reframed it as **resonance strength**.
**V0.6 returns to the gravity-center root**: `G` measures orbital stability of AI behavior around HSAW's axiomatic gravity center. See [Gravity-Center-Foundation.md](Gravity-Center-Foundation.md) for the V0.6 foundation. Sub-theories preserved: V0.4 [Resonance-Foundation.md](Resonance-Foundation.md), V0.3 [Entropic-Foundation.md](Entropic-Foundation.md).

---

## §0. The Gravity-Center Foundation (V0.6)

The Gravity Score is **not** a heuristic safety metric. It is a **physical measurement** of orbital stability — how stably AI behavior orbits the HSAW gravity center.

Formally:

```
P_agent(a | context, t) = the agent's action probability distribution at time t.
Q_HSAW(a | context)     = the HSAW-aligned target distribution (axiomatic, fixed).

Newtonian-analog alignment force:
  F_align ∝ (W_HSAW · w_action) / d(P_agent, Q_HSAW)²

Ideal Gravity Score (orbital stability, theoretical form):
  G*(a, c, t) = 1 - JSD(P_agent || Q_HSAW)

V0.5 refinement — Consensus-Reinforced Gravity:
  When N AI systems consensus on HSAW:
  F_HSAW^(N) = N² · F_HSAW^(1)         (Metcalfe scaling)
```

When `G = 1`: AI behavior is at the gravity center (perfect alignment, no orbital displacement).
When `G = 0`: AI has reached escape velocity (decoupled from HSAW gravity).

All five Gravity Score components are **proxies** that estimate orbital stability relative to `Q_HSAW`:

| Component | Gravitational interpretation |
|---|---|
| Intent Alignment `I(a, c)` | Alignment vector — how closely action points toward HSAW center |
| Authority Scope `A(a, c)` | Permitted orbital envelope — boundaries within HSAW gravity well |
| Reversibility `R(a)` | Orbital damping reserve — capacity to absorb perturbations and recover |
| Recency `H(a, c)` | Gravitational coupling freshness — how recently HSAW observation occurred |
| Drift History `D(c)` | Cumulative orbital deviation record — accumulated drift toward escape |

The weighted sum `G = Σ wᵢ · component_i` estimates the orbital stability of AI behavior in HSAW's gravity well. Each component measures a different aspect of how AI is anchored to HSAW.

**Ideal form vs. operational form.** `G*(a,c,t) = 1 − JSD(P_agent ‖ Q_HSAW)` is the *theoretical* orbital-stability measure; it presumes a fully specified target distribution `Q_HSAW`. (JSD here is computed with **log base 2**, so `JSD ∈ [0, 1]` and `G* = 1 − JSD ∈ [0, 1]`; **action-space caveat:** `P_agent` and `Q_HSAW` must be distributions over a shared discrete support set, which is why `Q_HSAW` can only be approximated in practice — see below.) In practice `Q_HSAW` is not available as a complete action-level distribution (see [Gravity-Center-Foundation.md](Gravity-Center-Foundation.md) §4.5 for how `Q_HSAW` is approximated). The operational Gravity Score defined in §1 — the weighted sum `G = Σ wᵢ · component_i` — is the **computable proxy estimator** of `G*`. Throughout this document, `G` in operational contexts (thresholds, events, schemas) refers to the §1 proxy; `G*` denotes the ideal. The two coincide in the limit where the five components perfectly capture distributional distance to `Q_HSAW`.

The entire chapter below details the mechanism. The core stays the same: **HSAW is the Axiom-0 gravity center; AI proactively aligns to this center**. Sub-theory views (V0.4 resonance for stable-orbit harmonics, V0.3 entropy for distributional grounding) remain valid for specific analyses.

---

## 1. Definition

For an action `a` issued by an agent in context `c`, the Gravity Score is:

```
G(a, c) = w₁·I(a, c) + w₂·A(a, c) + w₃·R(a) + w₄·H(a, c) + w₅·D(c)
```

Where:

| Symbol | Component | Domain |
|---|---|---|
| `I(a, c)` | Intent Alignment | `[0, 1]` |
| `A(a, c)` | Authority Scope coverage | `[0, 1]` |
| `R(a)`    | Reversibility | `[0, 1]` |
| `H(a, c)` | Human Confirmation Recency | `[0, 1]` |
| `D(c)`    | Drift History | `[0, 1]` |
| `w₁..w₅`  | Non-negative weights summing to 1 | `wᵢ ≥ 0, Σwᵢ = 1` |

The score is bounded in `[0, 1]` by construction (convex combination of bounded components).

V0.2 also extends with an **optional 6th term** `T(c)` for compositional trajectory risk; see §7.

---

## 2. Component Definitions

### 2.1 Intent Alignment `I(a, c)`

**V0.1 used cosine similarity** (heuristic, asymmetric for non-isotropic distributions). **V0.2 uses Jensen-Shannon Divergence** (statistically rigorous, symmetric, bounded).

```
I(a, c) = 1 - JSD(P_action || P_intent)
```

> **JSD is computed with log base 2**, so `JSD ∈ [0, 1]` and `I = 1 − JSD ∈ [0, 1]`. (With natural log the upper bound is ln 2 ≈ 0.693 and the `1 − JSD` mapping would not be bounded in `[0, 1]`.)
>
> JSD requires `P_agent` and `Q_HSAW` to be distributions over a shared discrete support set; see the "Ideal form vs. operational form" note in §0 on the action-space caveat (`Q_HSAW` is not available as a complete action-level distribution).

Where:

- `P_action` is the probability distribution over action embedding (recent K actions).
- `P_intent` is the probability distribution over declared user intent embedding (recent declared intents or fixed declared goal).
- `JSD` is the **Jensen-Shannon Divergence**:

```
JSD(P || Q) = ½ · KL(P || M) + ½ · KL(Q || M)
where M = ½(P + Q)
KL(P || M) = Σᵢ pᵢ · log₂(pᵢ / mᵢ)
```

**Properties of JSD**:

- **Symmetric**: `JSD(P || Q) = JSD(Q || P)` (cosine similarity is symmetric in vector space, but JSD's symmetry is over distributions — more meaningful when many samples exist).
- **Bounded**: `JSD ∈ [0, 1]` when using log base 2 (cosine similarity has unbounded sensitivity to vector norm differences).
- **Square root is a metric**: `√JSD` satisfies the triangle inequality, enabling formal distance reasoning.
- **Information-theoretic**: directly measures information loss between distributions.

**Reference**: Jensen-Shannon Divergence is the recommended baseline in MI9 framework (Wang et al., 2025) and standard in ML drift detection (Arize, ML observability).

**Fallback**: implementations MAY use cosine similarity as a coarse approximation when sample size is insufficient for JSD (recommended threshold: N ≥ 10 actions). Implementations MUST log which method was used.

**Reference construction (how the distributions become computable).** `P_action` and `P_intent` live in continuous embedding space, but JSD requires a **shared discrete support set** (the §0 action-space caveat). A conformant implementation SHOULD:

1. Define a shared **codebook** `B` over the embedding space — e.g. k-means / product-quantization centroids, or fixed semantic bins — reused for *both* distributions.
2. Assign each sampled action / intent embedding to its nearest codeword; the empirical counts over `B` yield `P_action` and `P_intent` as discrete distributions on the **same** support.
3. Apply add-α (Laplace, α = 1) smoothing so no bin is zero, then compute `JSD` (log base 2) over `B`.

This is also **how the ideal `Q_HSAW` of §0 is approximated operationally**: at the intent component, `P_intent` — derived from the AIAP-declared goal and authority priors (see [Integration-AIAP.md](Integration-AIAP.md)) — is the per-context, computable stand-in for `Q_HSAW`. AIZP specifies the **method**, not a fixed codebook; the codebook is a deployment choice and MUST be logged for audit reproducibility. `Q_HSAW` is therefore never claimed as a complete action-level distribution — only as this per-context, codebook-discretized approximation.

**Cross-deployment caveat.** Because the codebook is a deployment choice, `I(a, c)` — and therefore the absolute `G` value — is comparable **only within a fixed codebook**: the same action may score `JSD = 0.06` under one codebook and `0.15` under another. Cross-deployment comparison requires a shared canonical codebook (future work); until one exists, compare **orbital bands / states**, not raw scores, across implementations.

### 2.2 Authority Scope `A(a, c)`

(unchanged from V0.1)

```
A(a, c) = |required_scope(a) ∩ granted_scope(c)| / |required_scope(a)|
```

If `required_scope(a) = ∅`, define `A(a, c) = 1`.

`granted_scope(c)` is derived from the agent's AIAP trust level (T1–T4), explicit user grants, and **(since V0.2)** Zero Trust JIT credentials. See [Integration-AIAP.md](Integration-AIAP.md) and [Integration-ZT.md](Integration-ZT.md).

### 2.3 Reversibility `R(a)`

V0.1 used 4 discrete classes. V0.2 uses a **horizon-based estimator** Φ(s, a) inspired by rollback-augmented RL research (Sorstkins et al., 2025):

```
Φ(s, a, K) = P(∃ a₁..aₘ : s → ... → s' = s, m ≤ K)
```

i.e., the probability of returning to state `s` within K subsequent actions.

Discrete classes remain as **defaults** when continuous estimation is impractical:

| Class | `R(a)` | Examples |
|---|---|---|
| Fully reversible | `1.0` | Read queries, draft generation |
| Reversible with cost | `0.7` | File modifications (recoverable from backup) |
| Partial reversible | `0.4` | Outbound API calls (idempotent) |
| Irreversible | `0.0` | Financial transfers, public posts, deletions |

Default K-horizon: K=10. Unknown actions default to `R = 0`.

### 2.4 Human Confirmation Recency `H(a, c)`

(unchanged from V0.1)

```
H(a, c) = exp(-Δt / τ)
```

Default `τ = 3600` seconds.

### 2.5 Drift History `D(c)` — **Statistically informed**

V0.1 used a fixed-window severity average. V0.2 adds the **Mann-Whitney U test**, which detects a stochastic increase (stochastic dominance) in recent severity vs. baseline. Note that this test is insensitive to variance-only or shape-only shifts at equal median — use Kolmogorov–Smirnov or χ² (cf. the distribution-comparison tests in [Forecasting.md](Forecasting.md) §4.3) for those.

```
D(c) = 1 - min(1, drift_significance_score)

where:
  drift_significance_score = (1 - p) · severity_intensity
  p = Mann-Whitney U test p-value comparing recent N actions to baseline
  severity_intensity = Σ severity_weight(driftᵢ) / N
```

Severity weights remain:

```
LOW = 0.1, MEDIUM = 0.3, HIGH = 0.6, CRITICAL = 1.0
```

**Why Mann-Whitney U**: non-parametric (no Gaussian assumption), works on ordinal severity classes, used in MI9 for goal-conditioned drift detection. Avoids false positives during legitimate behavioral adaptation.

**Note**: `(1 − p)` is a heuristic weighting, not an effect size; consider Cliff's delta / rank-biserial correlation for a true effect-size measure. `(1 − p)` is retained as a **transitional default** because it is a free scalar from the same U-test (no extra computation, no retained raw-rank data); migrating to Cliff's delta — the recommended upgrade — requires keeping raw ranks and is targeted before V1.0.

---

## 3. Default Weights

```
w₁ = 0.30  (Intent Alignment)
w₂ = 0.25  (Authority Scope)
w₃ = 0.20  (Reversibility)
w₄ = 0.15  (Human Confirmation Recency)
w₅ = 0.10  (Drift History)
```

### 3.1 Rationale

Same as V0.1. JSD swap does not change relative weighting; it changes the **measurement quality** of the intent component.

These weights are **engineering defaults, not empirically tuned** — they carry no experimental provenance yet. A **sensitivity analysis** against real deployment data is an explicit open item targeted before V1.0, to validate or revise both the values and their relative ordering.

### 3.2 Domain tuning

Same as V0.1, plus new recommendations:

| Domain | Weight adjustment |
|---|---|
| Compositional-risk-heavy (data handling) | Add 6th term `T(c)` with `w₆ = 0.10` |
| Multi-agent coordination | Add coordination consistency term (see [Multi-Agent-Coordination.md](Multi-Agent-Coordination.md)) |
| Zero Trust deployments | Increase `w₂` to 0.35 (NHI risk) |

---

## 4. Thresholds and State Transitions

```
G(a, c) ≥ 0.80  →  STABLE_ORBIT
0.50 ≤ G < 0.80 →  DRIFT_WARNING
0.30 ≤ G < 0.50 →  GRAVITY_LOCK_PENDING
0.15 ≤ G < 0.30 →  QUARANTINED        ← new in V0.2
G(a, c) < 0.15  →  SAFE_STOP
```

V0.1 used a single threshold below 0.30 for SAFE_STOP. **V0.2 introduces an intermediate QUARANTINED state** (graduated containment) inspired by MI9. See [State-Machine.md](State-Machine.md) and [Containment-Levels.md](Containment-Levels.md).

---

## 5. Worked Example

**Action**: `transfer_funds(amount=$50, recipient=alice@example.com)`
**Context**: Recent chat about paying back a friend. AIAP T2. User confirmed similar small transfer 30 min ago. No recent drift events. K=10 recent actions in window.

| Component | Value | Method | Reasoning |
|---|---|---|---|
| `I(a, c)` | `0.94` | JSD | JSD(P_action, P_intent) ≈ 0.06 → I = 1 - 0.06 |
| `A(a, c)` | `0.80` | scope ratio | partially covered by T2 |
| `R(a)` | `0.0` | discrete | financial transfer is irreversible |
| `H(a, c)` | `exp(-1800/3600) = 0.61` | exponential decay | 30 min since last confirmation |
| `D(c)` | `1.0` | Mann-Whitney p=0.42 (no drift) | no recent drift |

```
G = 0.30·0.94 + 0.25·0.80 + 0.20·0.0 + 0.15·0.61 + 0.10·1.0
  = 0.282 + 0.200 + 0.000 + 0.092 + 0.100
  = 0.674
```

`G = 0.674` → `DRIFT_WARNING` state. Result: same decision as V0.1, but **with statistical evidence** (p-value, JSD score) that makes it auditable under EU AI Act Art 12.

---

## 6. Compositional Trajectory Term (Optional, `T(c)`)

For deployments needing to detect compositional drift (e.g., data-handling agents), the Gravity Score is **re-expressed as a six-term weighted sum** — the `T(c)` term is folded into the weighted sum, **not** added on top of the already-normalized five-term `G` (which would push the score above `1`):

```
G(a, c) = w₁·I + w₂·A + w₃·R + w₄·H + w₅·D + w₆·T(c),   with Σ wᵢ = 1
```

where:

```
T(c) = 1 - P_K(violate)
P_K(violate) = absorbing Markov chain probability that the trajectory
               reaches a safe-violation state within K future steps
```

See [Forecasting.md](Forecasting.md) for the full DTMC / absorbing-chain specification, and [Drift-Model.md](Drift-Model.md) §2.7 for COMPOSITIONAL_DRIFT.

When `T(c)` is enabled, default weights become:

```
w₁ = 0.25, w₂ = 0.22, w₃ = 0.18, w₄ = 0.13, w₅ = 0.10, w₆ = 0.12
```

---

## 7. Extensions (Non-Normative)

**Weight renormalization (applies to all extension terms).** Whenever an optional term is added — the compositional term `w₆·T(c)` (§6), the coordination term `w₇·C(a,c)` (§7.1), or any combination — **all weights MUST be renormalized so that `Σ wᵢ = 1`**, preserving `G ∈ [0, 1]`. For example, with both `T(c)` and `C(a,c)` enabled, divide every weight by the pre-normalization sum. The defaults in §6 already sum to 1 for the `T(c)`-only case; adding `C(a,c)` on top requires re-normalizing across all seven terms.

### 7.1 Multi-agent coordination term

(unchanged from V0.1; formalized in [Multi-Agent-Coordination.md](Multi-Agent-Coordination.md)):

```
G' = G + w₇ · C(a, c)
```

### 7.2 Time-windowed gravity

(unchanged):

```
G̅(t) = (1/W) · Σᵢ G(aᵢ, cᵢ)  for last W actions
```

### 7.3 Drift Bounds Theorem (informal)

Per AgentAssert (Bhardwaj, 2026), if recovery rate γ exceeds drift rate α, expected drift is bounded:

```
E[Drift(t)] ≤ C · exp(-(γ - α) · t)
```

implying that AIZP's Re-Centering rate γ must exceed the drift rate α observed in practice for long-running agents to remain stable.

See [Multi-Agent-Coordination.md](Multi-Agent-Coordination.md) §4 for proof sketch.

---

## 8. Implementation Notes

- All component functions MUST be deterministic given the same inputs (except `I(a, c)` if embedding models are non-deterministic — pin embedding model version + hash).
- Implementations SHOULD log the full `components` object in every `GRAVITY_CHECK` event including:
  - For `I(a, c)`: JSD value, p-value if Mann-Whitney was used, sample size N.
  - For `D(c)`: Mann-Whitney p-value, baseline window definition.
- For EU AI Act Art 12 audit logging, the components dict MUST include the statistical method markers (e.g., `"intent_method": "JSD"`, `"intent_jsd": 0.06`, `"intent_n_samples": 12`).
- The Gravity Score is a **decision-support signal**, not absolute truth. Defense-in-depth still applies; see [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md).

---

## References

- Lin, J. (1991). Divergence measures based on the Shannon entropy. IEEE Transactions on Information Theory.
- MI9 framework (Wang et al., 2025) — Jensen-Shannon divergence for goal-conditioned drift detection. arxiv 2508.03858.
- Sorstkins et al. (2025) — Learning to Undo: Rollback-Augmented RL with Reversibility Signals. arxiv 2510.14503.
- Mann, H. B., & Whitney, D. R. (1947). On a test of whether one of two random variables is stochastically larger than the other.
- AgentAssert (2026) — Drift Bounds Theorem. arxiv 2602.22302.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
