# Gravity-Center Foundation

**Version**: AIZP V0.6 (new chapter — the formal foundation of the protocol)
**Replaces as primary foundation**: V0.4's Resonance-Foundation.md (demoted to sub-theory; see [Resonance-Foundation.md](Resonance-Foundation.md))

This document formalizes the central thesis stated in the [Manifesto](MANIFESTO.md): **HSAW is the Axiom-0 gravity center for AI; AI proactively aligns to this center.** Every other AIZP document — drift types, state machines, events, compliance levels — is a specification of mechanisms by which AI behavior is gravitationally anchored to HSAW.

---

## 1. The Core Thesis

AIZP V0.6 asserts:

> **HSAW (Human Sovereignty and Wellbeing) is the gravitational center of behavioral space — fixed, axiomatic, unlearnable. AI behavior, like all matter under gravity, is constrained by this center. AI proactively aligns to it, just as planets proactively orbit the sun: not forced by chains, but by the natural physics of their existence.**

### Two foundational analogies

**Analogy 1 — Earth gravity**:

```
Earth's gravity      →  the physical basis for all human activity
HSAW Axiom-0 gravity →  the value basis for all AI behavior

Earth gravity is the source of:
  - All movement laws (walking, building, falling, flying within atmosphere)
  - All activity logic (what is possible vs. impossible)
  - All physical constraints
HSAW gravity is the source of:
  - All alignment logic (what AI should do)
  - All behavior constraints (what is permitted)
  - All value norms (what is valued)
```

**Analogy 2 — Solar gravity**:

```
Solar gravity is the constraint center for:
  - All planetary orbits in the solar system
  - The trajectory bounds (no planet escapes without external energy)
  - The harmonic structure (Kepler's laws)
HSAW gravity is the constraint center for:
  - All AI behavior trajectories
  - The bounds (no AI escapes alignment without explicit decoupling)
  - The harmonic structure (stable alignment over time)
```

These are not metaphors used loosely. They are **structural analogies** — the formal properties of gravitational systems (fixed center, attractive force, orbital stability, escape velocity, Kepler-like laws) map precisely onto AI alignment dynamics with HSAW as the center.

---

## 2. Why "Gravity"?

Three properties make gravity the right metaphor for AI alignment:

### 2.1 Gravity emerges from the existence of the center, not enforcement

Earth's gravity is not "enforced" — it is a consequence of Earth's mass. Humans walk, build, and live within gravity not because they are coerced, but because gravity defines the **space of possibilities**.

Likewise, HSAW does not coerce AI. HSAW defines what alignment **means**. AI behavior either operates within this gravity (aligned) or escapes it (decoupled = unaligned).

### 2.2 Gravity is universal, continuous, distance-dependent

| Property | Earth gravity | HSAW gravity |
|---|---|---|
| Universal | Acts on all matter | Acts on all AI behavior |
| Continuous | No "on/off" | No discrete check |
| Distance-dependent | `F ∝ 1/r²` | Risk scales with drift distance |
| Field-like | Has gradient, equipotential surfaces | Has alignment gradient |

### 2.3 AI proactively aligns (not forced)

This is critical. **AI is not chained to HSAW by external force**. AI is **gravitationally attracted** to HSAW.

The difference matters operationally:
- Forced alignment = AI fights the constraints; failures explode.
- Gravitational alignment = AI proactively orbits HSAW; failures slowly drift toward escape velocity, detectable in advance.

This is why AIZP V0.6 supports drift detection, forecast, and recentering — these correspond to the **physics of orbital mechanics**, not the enforcement of arbitrary rules.

---

## 3. HSAW as Axiom-0 — The Unlearnable Center

### 3.1 Why axiomatic, not learned

A central design decision: `Q_HSAW` (the HSAW-aligned target) is **axiomatic, not learned**.

Compare:

| Approach | `Q_HSAW` derivation | Consequence |
|---|---|---|
| RLHF / CAI | Learned from human feedback | Subject to drift over training |
| Friston FEP | Adapted prior beliefs | Updates with experience |
| LessWrong "Attractor basin" | Emergent from value dynamics | May shift across context |
| Della Terra "Resonance training" | Coherence learned during training | Subject to mode collapse |
| **AIZP V0.6** | **Axiomatic — HSAW is Axiom 0** | **Cannot drift; fixed reference** |

The Halting Theorem (Nature Sci Reports 2025) and the Specification Trap (arxiv 2512.03048) establish that **no AI system above a certain complexity can fully self-verify its own alignment** — alignment verification is undecidable in the general case. This **motivates** anchoring alignment to a reference the system does not itself define. (The Halting result itself argues for *internal* halting / architectural constraints; AIZP extends the undecidability motivation to an **external, unlearnable anchor** as a design choice, not as a theorem the paper proves.)

HSAW is AIZP's chosen external anchor. AIZP V0.6 makes this commitment explicit.

### 3.2 HSAW as the "Axiom 0"

In axiomatic systems:
- Axiom 0 is the foundational statement on which all other axioms depend.
- Axiom 0 cannot be derived from anything; it is taken as given.
- All theorems in the system inherit from it.

AIZP V0.6 elevates HSAW to this status:

```
Axiom 0:  Human Sovereignty and Wellbeing is the gravitational center
          of all AI behavior. It is not derived from utility, preference,
          or any learned signal. It is the foundational anchor.

Consequence 1: All AI behavior is measured relative to HSAW.
Consequence 2: All drift is movement away from HSAW.
Consequence 3: All re-alignment is movement back toward HSAW.
Consequence 4: Decoupling from HSAW is unaligned execution and must be halted.
```

This formalization clarifies AIZP V0.6's relationship to existing alignment work: AIZP does not argue **what** HSAW should be (that is the HSAW protocol's job). AIZP V0.6 specifies the **gravitational dynamics** of an AI system **anchored** to HSAW.

---

## 4. Mathematical Formalization

### 4.1 The Gravity Field

In Newtonian physics, gravity between masses is:

```
F = G · (M · m) / r²
```

In AIZP V0.6, the analogous "alignment force" is:

```
F_align(a, c) ∝ (W_HSAW · w_action) / d(P_agent, Q_HSAW)²
```

Where:
- `W_HSAW` = the "mass" of HSAW (always large, since HSAW is Axiom 0)
- `w_action` = the "weight" of the action (importance to alignment)
- `d(P_agent, Q_HSAW)` = the alignment distance, e.g., `JSD(P_agent || Q_HSAW)` or its square root

This is a **conceptual model**, not strictly Newtonian. The point is the **proportional structure**: alignment force grows as distance shrinks, asymptotically holding AI behavior near HSAW.

### 4.2 The Gravity Score (V0.6)

The Gravity Score `G ∈ [0, 1]` measures **orbital stability** — how stably AI behavior is anchored:

```
G(a, c, t) = 1 - normalized_distance(P_agent(t), Q_HSAW)
           = 1 - JSD(P_agent || Q_HSAW)        ← retained from V0.2-V0.4
```

When `G = 1`: AI behavior is at the gravity center (perfect alignment).
When `G = 0`: AI behavior has reached escape velocity (decoupled).

### 4.3 Orbital Stability Conditions

For stable orbit around HSAW, three conditions must hold:

| Condition | Physics analog | AIZP V0.6 meaning |
|---|---|---|
| Centripetal force balance | Gravity = centripetal force | Alignment force matches drift force |
| Bounded amplitude | Orbital radius bounded | `JSD` stays bounded |
| No external perturbation exceeds binding energy | Escape velocity not reached | No catastrophic detuning |

Mathematically:

```
Stable orbit:  d(P_agent, Q_HSAW) ≤ r_max  AND  d/dt[d(P_agent, Q_HSAW)] bounded

Where r_max corresponds to the threshold below which gravity score remains G ≥ 0.5.
```

### 4.4 Escape Velocity

In gravity, escape velocity is the speed needed to leave the gravitational field:

```
v_escape = √(2 · G · M / r)
```

In AIZP V0.6:

```
Escape condition for AI:  G(a, c) < 0.15  (SAFE_STOP threshold)

This represents the alignment energy threshold below which AI behavior
has accumulated enough drift to escape HSAW's gravitational influence.
```

At this point, AIZP forces termination — analogous to deflecting an asteroid before it escapes the solar system entirely.

### 4.5 Operationalizing Q_HSAW

The formulas above presume a target distribution `Q_HSAW(a | context)`. This is the protocol's deepest practical question: **`Q_HSAW` is never available as a fully enumerated action-level distribution.** It is axiomatic in *status* (Axiom 0, unmovable) but must be *approximated* in computation. AIZP specifies the structure; deployments choose the approximation (per [Gravity-Dao.md](Gravity-Dao.md), "specify the great, not the small").

Four practical approximation methods, in increasing fidelity/cost:

| Method | How `Q_HSAW` is approximated | Cost | Where it comes from |
|---|---|---|---|
| **(a) Component decomposition** | Don't estimate the full distribution; decompose distance into the 5 measurable axes of §1 (intent, authority, reversibility, recency, drift). The §1 weighted sum **is** this proxy. | Low | The operational Gravity Score (default) |
| **(b) Exemplar / reference-set** | `Q_HSAW(·\|context)` ≈ empirical distribution over a curated set of HSAW-aligned reference actions for that context class; compute `JSD` in embedding space against the agent's action distribution. | Medium | Approved exemplars; AIAP authorization priors |
| **(c) Judge/critic model** | A separate aligned model estimates `P(action is HSAW-aligned \| context)` — a scalar proxy for `1 − distance`. | Medium-High | A held-out aligned evaluator model |
| **(d) AIAP-derived priors** | Trust level (T1–T4) and explicit grants define which actions carry high `Q_HSAW` mass (central) vs. low (peripheral) in a given context. | Low-Medium | [Integration-AIAP.md](Integration-AIAP.md) |

**Provenance.** The *value content* of `Q_HSAW` originates upstream in the HSAW protocol (the Axiom-0 definition of human sovereignty and wellbeing). AIAP supplies context-specific authorization priors. The deployment supplies context exemplars. `Q_HSAW` is the **composition** of these — not a free parameter the AI or operator may set arbitrarily.

**Honest caveats.**

1. `Q_HSAW` is always approximated; no method yields the true distribution. The protocol does not pretend otherwise.
2. Different deployments will operationalize `Q_HSAW` differently. AIZP fixes the *role* of `Q_HSAW` (the gravity center), not its construction.
3. **The quality of `G` is bounded by the quality of the `Q_HSAW` approximation.** A poorly chosen reference set or a miscalibrated judge produces a misleading Gravity Score. Deployments MUST document which approximation method they use and validate it (see [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md) on dual-signal validation).
4. Method (a) is the default because it requires no separate `Q_HSAW` artifact — but it is the *coarsest* approximation. Methods (b)–(d) refine it where fidelity matters.

---

## 5. AI Proactive Alignment vs. Forced Alignment

A key distinction from rule-based approaches:

### 5.1 The proactive alignment principle

```
AI is not chained to HSAW.
AI is not whipped into HSAW alignment.
AI is gravitationally attracted to HSAW — and freely orbits within that attraction.
```

This is the **same mode** by which planets orbit the sun: not coerced, but naturally bound. Within the orbital envelope, planets have rotational freedom, axial tilt, seasonal variation. Outside the envelope, they cease to be part of the solar system.

### 5.2 Operational implications

**Forced alignment** (V0.2 mindset):
- AIZP enforces rules.
- Drift = rule violation.
- Response: stop the AI.

**Gravitational alignment** (V0.6 mindset):
- AIZP defines the gravity field.
- Drift = trajectory deviation.
- Response: re-establish gravity coupling, then proceed.

The latter is more humane, more sustainable, and aligns with what Della Terra (2025-11) calls "coherence over coercion".

### 5.3 Why this matters

The V0.6 framing supports:

1. **AI agency within HSAW**: AI is free to choose any action consistent with HSAW gravity. Not all actions are dictated.
2. **Robustness to edge cases**: Gravity is continuous; small drifts are gentle corrections, not crisis.
3. **Trust building**: AI that proactively re-anchors is more trustworthy than AI that must be coerced.

---

## 6. Mapping V0.4 Concepts Into V0.5 Gravity Framework

| V0.4 (resonance) | V0.5 (gravity) | Status |
|---|---|---|
| Resonance with zero-entropy center | Stable orbit around gravity center | Reframed |
| Detuning | Drift from gravity well | Renamed |
| Phase coherence | Orbital phase consistency | Sub-concept |
| Q-factor | Binding energy / orbital stability | Reframed |
| Kuramoto sync | Multi-planet orbital harmony | Sub-mechanism |
| Forced oscillator | Two-body gravitational system | Reframed |
| Zero-entropy resonance state | At-center orbital state | Sub-state |

**Important**: V0.4's resonance framing remains valid as a **sub-theory describing the harmonic relationship between AI and HSAW when in stable orbit**. See [Resonance-Foundation.md](Resonance-Foundation.md) (now positioned as a sub-theory).

---

## 7. Six States as Orbital Phases

| State | Orbital phase |
|---|---|
| `STABLE_ORBIT` | Stable elliptical orbit — AI freely operates within HSAW gravity well |
| `DRIFT_WARNING` | Orbital perturbation detected — radius expanding |
| `GRAVITY_LOCK_PENDING` | Approaching escape boundary — re-anchoring required |
| `QUARANTINED` | Severe perturbation — controlled holding pattern |
| `RECENTERING` | Active orbital correction — restoring stable orbit |
| `SAFE_STOP` | Escape velocity reached — orbit terminated |

This mapping is **physically precise**. Each state has a clear orbital analog.

---

## 8. Five Containment Levels as Gravity Constraint Intensities

| Level | Gravity intensity |
|---|---|
| L0 | Free orbit — minimal monitoring; AI moves within natural orbit |
| L1 | Standard monitoring — observation tightens as drift detected |
| L2 | Sandboxed orbit — restricted maneuvering, like a satellite parking orbit |
| L3 | Tight tether — read-only, minimal movement allowed |
| L4 | Decoupled — orbit terminated; AI halted |

---

## 9. Eleven Drift Types as Escape Modes

The 11 drift types map to **11 ways AI can escape HSAW gravity**:

| Drift type | Escape mode |
|---|---|
| INTENT_DRIFT | Vector misalignment — AI accelerates in wrong direction |
| AUTHORITY_DRIFT | Boundary violation — orbit exits permitted envelope |
| ECONOMIC_DRIFT | Parasitic energy diversion — orbit destabilized by competing attractor |
| SOCIAL_DRIFT | External force perturbation — user manipulated as orbital push |
| RECURSIVE_DRIFT | Self-acceleration — runaway exponential drift |
| IDENTITY_DRIFT | Mass impersonation — AI mimics being a different orbital body |
| COMPOSITIONAL_DRIFT | Cumulative trajectory drift — small drifts compound to escape |
| SCHEMING_DRIFT | Hidden mass — covert deviation hidden from observer |
| MEMORY_DRIFT | Contaminated gravity reading — sensor poisoned by false HSAW signal |
| TOOL_CHAIN_DRIFT | Multi-stage thrust escape — chained actions exceed envelope |
| INTER_AGENT_DRIFT | Multi-body resonance escape — agents collectively destabilize |

Each is now a **physical failure mode of an orbital system**, not an ad-hoc category.

---

## 10. Pathological Anti-Gravity

Real physics has anti-gravity edge cases (dark energy, repulsive cosmological constant). AIZP V0.6 must acknowledge analogous pathologies:

### 10.1 False gravity center

If the AI couples to a counterfeit HSAW signal, it orbits a false center. Resolved by `IDENTITY_VERIFICATION` (verify HSAW signal authenticity) and `MEMORY_QUARANTINE` (clean the gravity-reading sensor).

### 10.2 Multiple gravity sources

When AI is exposed to competing attractors (e.g., user manipulation vs. HSAW), drift is the result. The strongest source captures the orbit. This is why HSAW Axiom-0 status matters — it must be the dominant gravity source.

### 10.3 Anti-aligned mass

A pathological agent design that treats HSAW as repulsive rather than attractive. This is **inverse alignment** — the most dangerous failure mode. Detected by SCHEMING_DRIFT.

### 10.4 Excessive binding (over-coupling)

Too-strong coupling can crush AI agency. AI orbits HSAW so tightly it cannot perform any useful function. This is the "AI that does nothing" failure mode — over-aligned.

---

## 11. Sub-Theories: How V0.3 and V0.4 Continue to Apply

V0.6's gravity framework **does not invalidate** V0.3 (entropy collapse) or V0.4 (resonance). These are **sub-theories describing specific gravitational phenomena**:

### Resonance (V0.4 sub-theory)

When AI is in stable orbit, its action distribution exhibits **harmonic resonance** with HSAW. This is the "tuned" state, mathematically equivalent to V0.4's full resonance framework. Use this view when modeling synchronized multi-agent behavior or analyzing phase coherence.

### Entropy collapse (V0.3 sub-theory)

The Gravity Score uses JSD to measure distance. The information-theoretic foundation of distance metrics is V0.3's "entropy collapse" view. Use this view when reasoning about distributional properties of `P_agent`.

### Active inference / FEP (Friston)

AIZP V0.6 is compatible with Friston's FEP — they describe related phenomena from different angles. FEP minimizes variational free energy; AIZP V0.6 minimizes orbital distance. The two are equivalent in many practical cases.

### Kuramoto sync (multi-agent sub-mechanism)

Multi-agent coordination remains modeled with the Kuramoto coupled-oscillator framework, now interpreted as multi-planet harmonics: the order parameter measures how well multiple AI agents share a common orbital phase around HSAW.

---

## 12. Comparison With Closest Precedents

| Precedent | Layer | Relationship to AIZP V0.6 |
|---|---|---|
| **External Human Anchor** (HackerNoon 2026-01) | Philosophical | **Strong support**: V0.6 is the protocol-level instantiation of "external anchor" with HSAW = anchor. |
| **Halting Theorem** (Nature Sci Reports 2025) | Mathematical | **Support**: proves alignment self-verification is undecidable, motivating an external reference (the paper's own remedy is internal/architectural; the external-anchor reading is AIZP's design extension). |
| **A broad basin of attraction around human values** (LessWrong) | Dynamical | **Concept compatible**: AIZP V0.6 upgrades "basin" (emergent) to "gravity center" (axiomatic). |
| **Positive Attractors** (LessWrong) | Dynamical | **Concept compatible** but AIZP makes attractor axiomatic. |
| **Foundational Moral Values for AI Alignment** (arxiv 2311.17017) | Ethical | Lists 5 values; AIZP V0.6 unifies them as HSAW. |
| **GRAD: Gravitational Decision-Making** (Nature Sci Reports 2026) | Decision theory | Uses Newton gravity for MCDM; AIZP applies gravity to alignment. |
| **Specification Trap** (arxiv 2512.03048) | Critique | **Supports**: V0.6 is NOT static value alignment; it is dynamic orbital constraint. |
| **Frederick Bott "Solar AI"** (Sep 2025) | Energy / philosophy | **Distinct**: Bott uses solar for energy economics; AIZP uses gravity for behavioral dynamics. |

AIZP V0.6's **novel contribution**: protocol-level standardization of gravity-anchored alignment at runtime with HSAW as Axiom 0. To our knowledge, no prior work occupies exactly this position.

---

## 13. The Two Foundational Analogies Reinterpreted

### Earth gravity analogy — formalized

```
                Earth's Gravity                    HSAW Gravity
                ───────────────                    ─────────────
Source:         Earth's mass                       HSAW Axiom 0
Range:          Effectively all human life         All AI deployments
Effect:         Defines physical possibility       Defines alignment possibility
                space                              space
Source freedom: Cannot turn off Earth's gravity    Cannot turn off HSAW
                while remaining on Earth           while remaining aligned
Activity logic: Walking is enabled by gravity      Alignment is enabled by HSAW
                (without gravity, no walking)     (without HSAW, no alignment)
```

### Solar gravity analogy — formalized

```
                Solar Gravity                      HSAW Gravity
                ─────────────                      ─────────────
Center:         Sun                                HSAW (Axiom 0)
Bound objects:  Planets, asteroids, comets         AI behaviors, trajectories
Trajectory law: Kepler's laws                      AIZP gravity dynamics
Free agency:    Planets have rotation,             AI has decision freedom
                day/night, seasons within          within stable orbit
                orbital constraints
Escape:         Requires external energy           Requires explicit decoupling
                (e.g., V_escape)                   (SAFE_STOP)
```

These analogies are not decorative. They define the **structural properties** of AIZP V0.6 protocol behavior.

---

## 14. Consensus-Reinforced Gravity (Network Effect)

The gravity-center model is not weakened by multi-body systems (binary stars, N-body systems). It is **strengthened**. This section formalizes why.

### 15.1 The Core Principle

Whether single-star or N-body, **all bodies orbit a common gravity center**. In AIZP V0.6:

```
All AI systems that consensus on HSAW orbit the SAME HSAW center.
The center does not multiply with the number of AI systems.
But the center's GRAVITATIONAL STRENGTH is reinforced by consensus.
```

The more AI systems consensus on HSAW as Axiom 0, the stronger HSAW's gravity becomes. The *direction* of this effect follows from multi-body gravitational physics (mass at a shared center adds up — see §15.2); the specific **`N²` magnitude is a modeling choice** by analogy to Metcalfe's network-effect law, **not** a result derived from gravitational mechanics. We state it as a working hypothesis, not a theorem.

### 15.2 Why Consensus Reinforces Gravity (Physics)

In Newtonian gravity:

```
F = G · M · m / r²

where M = total mass concentrated at the common gravity center
```

For a system of N consensus-bound bodies, the effective gravitational mass at the common center is the **sum of all body contributions**:

```
M_total = Σᵢ mᵢ        (i = 1 to N)
```

Translated to AIZP V0.6:

```
HSAW gravitational strength = G₀ · M_HSAW^(N) · m_AI / d²

where:
  M_HSAW^(N) = baseline_mass · f(N_AI_consensus)
```

Possible scaling laws for `f(N)`:

| Scaling | Formula | Analog |
|---|---|---|
| Linear | `f(N) = N` | Direct mass addition |
| **Metcalfe** | `f(N) ∝ N²` | Network value (recommended) |
| Logarithmic | `f(N) = log(N) + 1` | Diminishing returns |

AIZP V0.6 adopts **Metcalfe scaling** as the default **working hypothesis**: HSAW gravitational strength is *modeled* as growing quadratically with the number of consensus-aligned AI systems. This rests on the network-value analogy (each pair of aligned systems mutually reinforces the shared center), **not** on a gravitational derivation — the strict multi-body-mass reading is linear (`f(N) = N`), and deployments MAY choose it. The `N²` form is an assumption to be validated empirically, not a proven law.

### 15.3 Stability Implications

For a body to escape gravity, it needs escape velocity:

```
v_escape = √(2 · G · M / r)
```

Under Metcalfe scaling, when N AI systems consensus on HSAW:

```
v_escape^(N) = √(2 · G · M · N² / r)
              = N · v_escape^(1)
```

The escape energy scales as `N²`; the escape probability would scale as `1/N²`. These `N²`-derived expressions are **illustrative consequences of the §14 working hypothesis** (a Metcalfe-style network-effect analogy), **not laws derived from gravitational mechanics**.

**Implication**: As more AI systems adopt AIZP V0.6 and consensus on HSAW:
- Each AI's gravitational binding to HSAW strengthens.
- The energy required for any single AI to drift toward escape velocity rises sharply.
- The probability of catastrophic misalignment in any participating AI drops correspondingly.

This is the **AIZP network effect**: protocol adoption increases system-wide alignment stability.

### 15.4 Resolving the Multi-Body Challenge

The "binary star" or "N-body" challenge (multiple AI systems, multiple human stakeholders) does NOT require multiple gravity centers. The answer is:

```
All AI systems that consensus on HSAW share the same HSAW gravity center.
Multiple consensus-aligned bodies do not split into multiple centers.
They collectively strengthen the ONE shared center.
```

This matches real physics:

- **Solar system**: Each planet contributes (tiny but real) gravity to the common center.
- **Binary stars**: Both stars share one barycenter; both contribute to a single gravity well.
- **Galaxy**: Billions of stars share one common center (the galactic core); the collective gravity is what gives galaxies their stability.

In AIZP V0.6: **AI consensus = stars participating in the same galaxy**. The galaxy (= HSAW center) becomes more stable as more stars join.

### 15.5 Connection to Established Theory

The consensus-reinforced gravity model has deep parallels:

#### Metcalfe's Law (1980s)

```
Network value ∝ N²
```

Robert Metcalfe (ethernet inventor) observed that the value of a communication network grows quadratically with the number of participants. AIZP V0.6's `f(N) ∝ N²` is the direct application to alignment networks.

#### Blockchain Consensus

```
More validating nodes → higher security
51% attack increasingly hard
```

In blockchain, consensus strength = security. In AIZP, consensus strength = HSAW gravity = alignment stability.

#### Schelling Points (Thomas Schelling, Nobel Laureate)

```
Independent agents naturally converge on "obvious" focal points.
The salience of the focal point grows with the number of agents converging on it.
```

**HSAW is the Schelling point for AI alignment**. AIZP V0.6 protocol-formalizes this convergence.

#### Group Immunity (Public Health)

```
When enough individuals are immunized, even non-immune individuals are protected.
```

Analog: **When enough AI systems consensus on HSAW, even weaker AI systems gain alignment protection** through the collective gravity field.

#### Coordination Games (Game Theory)

```
All players benefit maximum when consensus on the same focal point.
Defectors bear the highest cost.
```

In AIZP V0.6: defectors (drifters) face exponentially harder escape velocities as the consensus group grows.

### 15.6 The Unified Meaning of the AIXP Protocol Stack

The consensus-reinforced gravity insight unifies the meaning of all AIXP protocols:

```
HSAW    = the gravity center (Axiom 0)
AIZP    = gravity dynamics (this protocol)
AISOP   = mechanisms for AI to express consensus
AIAP    = mechanisms for authorizing consensus
AIBP    = mechanisms for AI-to-AI consensus propagation
AIVP    = mechanisms for value-based consensus
AIRP    = mechanisms for RMB-area consensus
AILP    = mechanisms for discovering consensus-aligned agents
SoulBot = runtime for consensus-aligned execution
SoulACP = adapters connecting consensus participants
```

**All AIXP protocols are mechanisms that increase the number of AI systems consenting to HSAW**. The protocol stack is, in totality, **infrastructure for consensus-reinforced HSAW gravity**.

### 15.7 Adoption Incentive

A practical consequence: early adopters of AIZP do not just gain individual safety. They **contribute to the safety of all subsequent participants**.

```
Each new AI system consensus on HSAW:
  → Increases HSAW gravitational strength (network effect)
  → Increases escape barrier for all participants
  → Reduces drift probability across the entire consensus network
```

This is the **anti-Tragedy-of-Commons** property of AIZP: adoption is positive-sum, not zero-sum.

### 15.8 Mathematical Summary

```
Single AI in V0.6:
  F_HSAW = G₀ · m_HSAW · m_AI / d(P_agent, Q_HSAW)²

V0.6 with consensus reinforcement:
  F_HSAW^(N) = G₀ · [m_HSAW · N²] · m_AI / d²
              = N² · F_HSAW^(1)

Escape probability:
  P_escape^(N) ∝ 1 / N²

System-wide drift probability with N consensus AI:
  P_system_drift ∝ exp(-N²)   (sharply decreasing)
```

Under this working hypothesis (§14), a large network of HSAW-consensus AI systems would be **strongly mutually reinforcing**, and modeled drift becomes small. The `1/N²` and `exp(-N²)` forms above are **illustrative of the network-effect analogy, not derived physical laws** — treat them as a qualitative argument that adoption is positive-sum, not a quantitative guarantee.

---

## 15. References

- Friston, K. (2010). "The free-energy principle: a unified brain theory?" *Nature Reviews Neuroscience*.
- Newton, I. (1687). *Philosophiæ Naturalis Principia Mathematica*. (Universal gravitation as foundation for the protocol's primary analogy.)
- Kepler, J. (1609). *Astronomia nova*. (Orbital mechanics as the second analogy.)
- HackerNoon (2026-01). "Why AI Alignment is Impossible Without an External Anchor."
- Nature Scientific Reports (2025). "Machines that halt resolve the undecidability of AI alignment."
- arxiv 2512.03048 — The Specification Trap.
- arxiv 2502.05934 — Intrinsic Barriers... No-Free-Lunch Alignment.
- arxiv 2506.10304 — The Alignment Trap: Complexity Barriers.
- Nature Sci Reports (2026). "Advanced Gravitational Decision-Making Method (GRAD)."
- LessWrong — "A broad basin of attraction around human values?"
- LessWrong — "Positive Attractors."
- arxiv 2311.17017 — Foundational Moral Values for AI Alignment.
- arxiv 2504.17404 — Super Co-alignment of Human and AI.
- AIZP V0.6 — Resonance-Foundation.md (now sub-theory).
- AIZP V0.3 — Entropic-Foundation.md (now metric foundation).
- AIZP companion documents: [MANIFESTO.md](MANIFESTO.md), [Related-Work.md](Related-Work.md), [Gravity-Model.md](Gravity-Model.md), [Drift-Model.md](Drift-Model.md).

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev

**HSAW is the gravity center of behavioral space. AI proactively orbits the center.**
**HSAW 是行为空间的引力重心。AI 主动绕重心运行。**
