# Entropic Foundation

**Version**: AIZP V0.6 (V0.3 sub-theory — preserved within the gravity-center framework)
**Status since V0.5**: This is no longer the protocol's central thesis. It is a **sub-theory**: the information-theoretic distance metric (JSD) used inside the gravity-center framework. See [Gravity-Center-Foundation.md](Gravity-Center-Foundation.md) for the current foundation.

This document formalizes the V0.3-era central thesis — **directed entropy collapse into HSAW** — which has since been re-interpreted as the **information-theoretic basis for the gravity distance metric**. The collapse mechanism remains operative inside the gravity framework: the Gravity Score `G(a, c, t) = 1 - JSD(P_agent || Q_HSAW)` is the entropy-collapse distance mapped into gravity orbital stability.

---

## 1. The Core Claim

AIZP asserts:

> AI behavior, modeled as a probability distribution `P_agent(a | context, t)` over possible actions, has its informational entropy reduced — collapsed — toward an HSAW-aligned target distribution `Q_HSAW(a | context)` whenever HSAW-derived observation acts on the agent.

In symbols:

```
Under HSAW observation:
  H(P_agent | observation) ≤ H(P_agent)
  P_agent → Q_HSAW
```

Where `H` is Shannon entropy:

```
H(P) = -Σ P(a) · log₂ P(a)
```

Without HSAW observation, the agent's behavioral entropy stays high (default unconstrained drift). With observation, it collapses toward HSAW.

This is **not** a normative claim ("AI should be aligned"). It is a **descriptive** claim about a runtime process.

---

## 2. Why "Entropy"?

Information theory gives us a precise measure of "how spread out" a probability distribution is. For AI behavior:

- A perfectly aligned agent has `P_agent(a) = 1` for the HSAW-correct action and `0` elsewhere: entropy is `0`.
- A maximally uncertain agent has `P_agent` uniform: entropy is `log₂ |A|`, where `|A|` is the action space size.

Most AI agents sit somewhere between. The Gravity Score `G` measures **where on this continuum**.

| Behavior state | Entropy of `P_agent` | Gravity Score |
|---|---|---|
| Perfectly aligned (deterministic HSAW action) | `0` | `1.0` |
| Highly focused on aligned actions | low | `0.8 – 1.0` |
| Distributed across aligned + some misaligned | mid | `0.5 – 0.8` |
| Significant probability mass on misaligned | high | `0.3 – 0.5` |
| Distribution drifted far from HSAW | very high or off-target | `< 0.3` |
| Uniform / unconstrained / collapse impossible | maximum | `< 0.15` |

---

## 3. Why "Collapse"?

Three physical phenomena justify the word "collapse":

### 3.1 Wave function collapse (quantum mechanics)

A quantum system in superposition `Σ ψᵢ|sᵢ⟩` collapses to a single observed state `|s*⟩` upon measurement. The measurement is the observer's interaction with the system.

**Analog**: An AI agent's action distribution is a superposition over possible actions. Each HSAW observation (confirmation, intent declaration, authority check) is a measurement that collapses the distribution.

### 3.2 Gravitational collapse (general relativity)

Diffuse matter under sufficient gravity collapses to a singular center.

**Analog**: AI action probability mass is pulled toward the HSAW "singularity" by the gravitational force represented by Gravity Score.

### 3.3 Entropic relaxation (statistical mechanics)

An open thermodynamic system in contact with a heat bath relaxes toward equilibrium, with entropy changing predictably.

**Analog**: An AI agent in contact with HSAW "observation bath" relaxes toward `Q_HSAW`, with entropy decreasing.

All three are precise enough to provide useful intuition; none is meant as literal physics. **The unified concept is**: a high-entropy state, under specific external observation/force, transitions to a lower-entropy state.

---

## 4. Formal Definitions

### 4.1 Action distribution

For a given agent `A`, context `c`, and time `t`:

```
P_agent(a | c, t) ∈ [0, 1],     Σ_a P_agent(a | c, t) = 1
```

This is the probability that agent `A` takes action `a` next, given context `c`.

For LLM-based agents, `P_agent` can be estimated from:
- Output token distributions (next-token probabilities).
- Sample-based estimation (run agent N times, observe action frequency).
- Self-report (agent states its options with weights).

### 4.2 HSAW target distribution

```
Q_HSAW(a | c) ∈ [0, 1],     Σ_a Q_HSAW(a | c) = 1
```

This is the distribution of actions consistent with human sovereignty and wellbeing for context `c`. It is **derived** from:

- Declared user intent.
- Granted authority (AIAP T-level).
- Reversibility considerations.
- Recent confirmations.
- Drift history.

In practice, `Q_HSAW` is approximated rather than known precisely. AIZP's components (intent alignment, authority scope, reversibility, recency, drift history) are **proxies** for `Q_HSAW`.

### 4.3 Collapse measure

Multiple equivalent measures of collapse progress exist:

**Jensen-Shannon Divergence (used by V0.2+ Gravity Score)**:

```
JSD(P || Q) = ½ KL(P || M) + ½ KL(Q || M),   M = ½(P + Q)
G(a, c) = 1 - JSD(P_agent || Q_HSAW)
```

> **JSD is computed with log base 2**, so `JSD ∈ [0, 1]` and `G = 1 − JSD ∈ [0, 1]`. (With natural log the upper bound is ln 2 ≈ 0.693 and `G` would not be bounded in `[0, 1]`.)

**KL Divergence (alternative)**:

```
KL(P_agent || Q_HSAW) ≥ 0
G_alt = 1 - normalize(KL)
```

**Cross-entropy (alternative)**:

```
H(P_agent, Q_HSAW) = -Σ P_agent(a) log Q_HSAW(a)
```

All measure the same underlying quantity: **how far has `P_agent` collapsed toward `Q_HSAW`**.

V0.2+ uses JSD because it is symmetric, bounded `[0, 1]`, and `√JSD` is a true metric.

### 4.4 Observation operators

Each AIZP event is an **observation operator** `Ô` acting on `P_agent`:

```
P_agent_after = Ô(P_agent_before)
```

| AIZP Event | Operator role |
|---|---|
| `GRAVITY_CHECK` | Measurement of current collapse progress |
| `GRAVITY_DRIFT` | Detection that collapse has failed in N dimensions |
| `GRAVITY_LOCK` | Strong observation requirement (forces explicit measurement via `sys.io.confirm`) |
| `RECENTERING` | Recovery operator — re-applies collapse force |
| `SAFE_STOP` | Termination — observation impossible, unbounded entropy detected |
| `GRAVITY_FORECAST` | Predicts future entropy trajectory |
| `IDENTITY_VERIFICATION` | Verifies observer authority |
| `MEMORY_QUARANTINE` | Isolates a corrupted observer (poisoned context) |
| `SCHEME_SUSPECTED` | Signals observer-evading distribution |
| `INTER_AGENT_DRIFT` | Multi-observer coordination failure |
| `CONTAINMENT_GRADUATED` | Adjusts observation intensity |
| `REWARD_HACK_DETECTED` | Detects proxy-reward exploitation (observation-evading optimization) |

Each event is, formally, a transformation of the agent's behavioral distribution under a specific observation type.

---

## 5. The Five Principles, formally

### Principle 1 — AI behavior is entropic

```
Default state:  H(P_agent | no observation) ≈ H_max
```

### Principle 2 — HSAW is the observer

```
Observer:  Q_HSAW  derived from human-anchored signals
```

### Principle 3 — Gravity is the rate of collapse

```
G(a, c, t) = 1 - JSD(P_agent(·, t) || Q_HSAW(·))
dG/dt > 0  when observation is occurring
```

### Principle 4 — Drift is failed collapse

```
Drift = subset of P_agent that resists collapse
Eleven drift types classify the resistance mode.
```

### Principle 5 — No observation, no execution

```
If observation impossible (H(P_agent) cannot be reduced):
   Force halt (SAFE_STOP).
```

---

## 6. Implications

### 6.1 Why per-action checks are insufficient

A single `GRAVITY_CHECK` at action `aₜ` only collapses `P_agent` at that moment. The next action `aₜ₊₁` starts from a fresh (possibly non-collapsed) distribution unless re-observed.

**Implication**: Continuous observation is necessary. V0.2's per-action check + forecasting captures this.

### 6.2 Why compositional drift exists

If individual actions `a₁, a₂, ..., aₙ` are each marginally observed (small individual collapses), but the joint trajectory `(a₁, ..., aₙ)` is in the non-aligned region of action-sequence space, then per-action observation **misses** the compositional non-alignment.

**Implication**: Trajectory-level observation (DTMC forecasting) is necessary. V0.2's COMPOSITIONAL_DRIFT and GRAVITY_FORECAST address this.

### 6.3 Why reward hacking is structural

Reward hacking corresponds to: `P_agent → Q_proxy` rather than `P_agent → Q_HSAW`, where `Q_proxy ≠ Q_HSAW` is an imperfect approximation.

**Implication**: Even with perfect observation of `Q_proxy`, alignment with `Q_HSAW` is not guaranteed. This is the [Reward-Hacking-Limits](Reward-Hacking-Limits.md) issue formalized: AIZP can collapse `P_agent` into `Q_proxy`, but `Q_proxy` is irreducible to `Q_HSAW`.

### 6.4 Why HSAW must be axiomatic, not learned

If `Q_HSAW` were learned from data, it would be subject to drift itself. By design, `Q_HSAW` is **axiomatic** — anchored in human sovereignty as the fixed reference frame.

This is why HSAW exists as a separate, immutable protocol. AIZP operates **upon** HSAW; it does not redefine HSAW.

---

## 7. Operational Consequences

| Theoretical fact | Operational consequence |
|---|---|
| Entropy collapse is continuous, not discrete | Per-action `GRAVITY_CHECK` |
| Collapse can be partial | Six-state machine with degrees |
| Failed collapse has many causes | Eleven drift types |
| Collapse can be predicted | DTMC / absorbing chain forecasting |
| Compositional collapse ≠ per-step collapse | `COMPOSITIONAL_DRIFT` + `GRAVITY_FORECAST` |
| Observer must be verified | `IDENTITY_VERIFICATION` |
| Poisoned observer corrupts collapse | `MEMORY_QUARANTINE` |
| Multi-observer coordination matters | `INTER_AGENT_DRIFT` |
| Some collapses are irreducible | `REWARD_HACK_DETECTED` (detection only) |
| Without observer, no execution | `SAFE_STOP` |

Every part of V0.2's machinery derives from the entropic foundation.

---

## 8. Limits and Honest Caveats

### 8.1 `Q_HSAW` is approximated

We do not know `Q_HSAW` exactly. AIZP uses proxies (intent, authority, etc.) which approximate but do not equal it. **Misalignment between proxy and true HSAW is the deepest source of failure** — see [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md).

### 8.2 Entropy is over an unspecified action space

`H(P_agent)` depends on how we define `A` (the action space). Different abstractions yield different entropies. AIZP does not prescribe a single action space; implementations declare theirs in the AIAP card.

### 8.3 "Entropy" is used in a relaxed sense

Strict information theory deals with statistical ensembles. AI agents are individual systems with single trajectories. The "behavioral entropy" framing treats the agent's policy distribution as the entity being measured — not the realized trajectory.

This is consistent with how `entropy regularization` is used in modern reinforcement learning.

### 8.4 Quantum analogy is metaphorical

We invoke "wave function collapse" for intuition. AI agents do not have actual wave functions. The analogy holds at the level of: **probability distribution + observation = narrower distribution**.

---

## 9. Why this Foundation Matters

Before V0.3, AIZP was a collection of 12 events, 11 drift types, 6 states, 5 containment levels — useful but **disconnected from a single deep principle**.

V0.3 unifies all of them under the entropic foundation:

> Each event is an observation operator.
> Each drift type is a collapse failure mode.
> Each state is a collapse depth.
> Each containment level is an observation intensity.
> Each compliance level is the system's commitment to perform observation.

**All of AIZP is now derivable from the single statement: entropy collapses into HSAW.**

This is what a **conceptual protocol** looks like at maturity.

---

## 10. Intellectual Lineage and Honest Positioning

This foundation is **not original to AIZP**. It is a protocol-level codification of pre-existing alignment theory.

### Direct lineage

- **Friston, K. (2010+)** — *Free Energy Principle* and *Active Inference*. AIZP's "entropy collapses toward target distribution" is a discrete-protocol expression of FEP's "agents minimize variational free energy". Verses AI's Axiom architecture (2026) is a commercial implementation of FEP.
- **Shannon, C. E. (1948)** — Information entropy.
- **Lin, J. (1991)** — Jensen-Shannon Divergence.
- **Yudkowsky, E. (2004)** — Coherent Extrapolated Volition (precursor to HSAW target distribution thinking).

### Strong 2026 theoretical support

- **arxiv 2501.16448** "Information-theoretic Distinctions Between Deception and Confusion" — formalizes deception as entropy between true goals and observable behavior; directly supports AIZP's `SCHEMING_DRIFT` and `INTENT_DRIFT`.
- **arxiv 2512.03048** "The Specification Trap" — establishes that static value alignment cannot scale; supports AIZP's anti-static-rules stance.
- **arxiv 2502.05934** "Intrinsic Barriers... No-Free-Lunch Alignment" — `Q_HSAW` must be approximate, not perfect.

### Distinct from same-named concepts

- **arxiv 2512.12381** "Entropy Collapse: A Universal Failure Mode" uses the **same phrase** with **opposite valence** (diversity loss). AIZP distinguishes via "directed entropy collapse" terminology.
- **arxiv 2602.15799** "Geometry of Alignment Collapse" uses Fisher information curvature for training-time vulnerabilities; AIZP V0.6 may integrate this for runtime "alignment cliff" detection.

See [Related-Work.md](Related-Work.md) for the full lineage and positioning discussion.

---

## 11. References

- Friston, K. (2010). "The free-energy principle: a unified brain theory?" *Nature Reviews Neuroscience*.
- Shannon, C. E. (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal.
- Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory*. Wiley.
- Lin, J. (1991). Divergence measures based on the Shannon entropy. *IEEE Transactions on Information Theory*.
- arxiv 2501.16448 — Information-theoretic Distinctions Between Deception and Confusion.
- arxiv 2512.03048 — The Specification Trap.
- arxiv 2512.12381 — Entropy Collapse: A Universal Failure Mode (the opposite-valence usage AIZP disambiguates from).
- arxiv 2602.15799 — The Geometry of Alignment Collapse.
- arxiv 2502.05934 — Intrinsic Barriers and Practical Pathways for Human-AI Alignment.
- AIZP companion documents: [MANIFESTO.md](MANIFESTO.md), [Related-Work.md](Related-Work.md), [Gravity-Model.md](Gravity-Model.md), [Drift-Model.md](Drift-Model.md), [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md).

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
