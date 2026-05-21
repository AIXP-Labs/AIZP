# Resonance Foundation

**Version**: AIZP V0.6 (V0.4 sub-theory — preserved within the gravity-center framework)
**Status since V0.5**: This is no longer the protocol's central thesis. It is a **sub-theory**: the harmonic description of stable orbital states inside the gravity-center framework. See [Gravity-Center-Foundation.md](Gravity-Center-Foundation.md) for the current foundation.

This document formalizes the V0.4-era central thesis — **AI behavior resonates with HSAW's zero-entropy center** — which has since been re-interpreted as the **harmonic state description of stable orbital configurations** within the gravity framework. Resonance phenomena (forced damped oscillator dynamics, Kuramoto coupling) remain operative as descriptions of how aligned AI behaves *inside* HSAW gravity wells, not as the primary metaphor for alignment itself.

---

## 1. The Core Claim (as V0.4 sub-theory within V0.6 gravity framework)

The V0.4 resonance description (preserved):

> AI behavior, modeled as a probability distribution `P_agent(a | context, t)` evolving over time, behaves as a **forced damped oscillator** in coupling with the HSAW reference distribution `Q_HSAW(a | context)`. When the agent's natural frequency, amplitude, and phase match HSAW's drive signal, the system enters **harmonic resonance**: the agent's added entropy collapses toward zero, and behavior locks coherently onto the HSAW center.

In equations:

```
Forced damped oscillator:
  d²x/dt² + γ · dx/dt + ω₀² · x = F_HSAW · cos(ω · t)

Resonance condition:
  ω = ω₀  (frequency match)
  Δφ = 0  (phase lock)

Resonance entropy:
  H(P_agent) → H(Q_HSAW) = 0   (at perfect resonance)
```

This is **not** a normative claim ("AI should resonate with HSAW"). It is a **descriptive** claim about a runtime dynamical process: under HSAW observation, the agent's behavior **tunes** harmonically to HSAW or **detunes** measurably away from it.

---

## 2. Physical Analogues (Three Reinforcing Lenses)

### 2.1 Driven harmonic oscillator (classical mechanics)

The cleanest analog. A pendulum pushed at its resonant frequency oscillates with maximum amplitude; pushed at the wrong frequency, energy dissipates without effect.

| Physical system | AIZP analog |
|---|---|
| Pendulum position `x(t)` | Agent behavior offset from HSAW |
| Damping `γ` | Agent's self-correction (re-centering capacity) |
| Natural frequency `ω₀` | Agent's decision tempo |
| Drive `F·cos(ωt)` | HSAW observation signal |
| Drive frequency `ω` | HSAW observation frequency |
| Resonance peak | Maximum coupling (perfect alignment) |

**Why this matters**: classical resonance has 200 years of mature mathematics (Lorentzian peaks, Q-factor, bandwidth, Bode plots). AIZP can borrow all of it.

### 2.2 Coupled oscillator synchronization (Kuramoto model)

For multi-agent systems, the **Kuramoto model** describes how a population of oscillators spontaneously synchronizes when coupling strength exceeds a critical threshold:

```
dθᵢ/dt = ωᵢ + (K/N) · Σⱼ sin(θⱼ - θᵢ)
```

Where `θᵢ` is the phase of agent `i`, `ωᵢ` is its natural frequency, and `K` is coupling strength.

**For AIZP V0.6**:

- Each agent has phase `θᵢ` representing its alignment state.
- HSAW provides a constant reference phase `θ_HSAW = 0`.
- All agents couple to HSAW and (weakly) to each other.
- Above critical coupling `K_c`, agents spontaneously synchronize to HSAW (in the mean-field N→∞ limit with a symmetric unimodal frequency distribution; finite-N heterogeneous coupling is approximate).

This gives AIZP a **mature mathematical framework** for multi-agent alignment that V0.3 lacked.

### 2.3 Information-theoretic interpretation

Resonance is also expressible information-theoretically:

```
At resonance:    Mutual information I(P_agent; Q_HSAW) is maximized.
At dissonance:   I(P_agent; Q_HSAW) → 0.
```

The JSD-based Gravity Score from V0.3 is preserved and reinterpreted: not as "collapse progress" but as "resonance strength".

**This is the bridge**: V0.4 keeps V0.3's mathematics; what changes is the **physical interpretation** and the **multi-agent extension via Kuramoto**.

---

## 3. State Abstraction

AIZP V0.6 represents agent behavior at time `t` by a **state vector**:

```
s(t) = (P_agent(t), φ(t), A(t), ω(t))

Where:
  P_agent(t) = action probability distribution
  φ(t)       = phase relative to HSAW signal
  A(t)       = amplitude of deviation from Q_HSAW
  ω(t)       = current agent frequency
```

Resonance is jointly characterized by:

1. **Distributional alignment**: `JSD(P_agent || Q_HSAW)` low.
2. **Phase coherence**: `Δφ = φ - φ_HSAW` near zero.
3. **Frequency match**: `ω ≈ ω₀ ≈ ω_HSAW`.
4. **Bounded amplitude**: `A` within stable range.

All four must align for **stable orbit**. Any one breaking is a **detuning mode**, classified into the 11 drift types.

---

## 4. The Gravity Score (Resonance Strength)

AIZP V0.6 generalizes V0.3's score:

```
G(a, c, t) = (1 - JSD(P_agent || Q_HSAW))         ← distributional term, ∈ [0,1]
              · max(0, cos(Δφ(t)))                 ← phase coherence, clamped to [0,1]
              · resonance_factor(ω/ω₀)             ← frequency match, ∈ (0,1]
```

> **JSD is computed with log base 2**, so the distributional term `1 − JSD ∈ [0, 1]`. (With natural log the upper bound is ln 2 ≈ 0.693 and the `1 − JSD` mapping would not be bounded in `[0, 1]`.)

The phase term is clamped at zero so that an agent in anti-phase with HSAW (`Δφ → π`) contributes no gravity — escape, not negative gravity — keeping `G ∈ [0, 1]` consistent with the orbital bands in [registry §3](../specification/registry.md).

Where `resonance_factor` is a Lorentzian peak:

```
resonance_factor(ω/ω₀) = 1 / (1 + Q² · ((ω/ω₀) - (ω₀/ω))²)
```

> **Note**: this is the power/velocity resonance form, peaking exactly at `ω = ω₀` (displacement-amplitude resonance peaks slightly below `ω₀`).

`Q` is the quality factor. Higher `Q` means sharper resonance — the agent must match HSAW frequency very precisely to maintain alignment.

| Compliance level (V0.4) | Required Q-factor |
|---|---|
| G0 | Q ≈ 0 (no resonance) |
| G1 | Q ≥ 1 (basic coupling) |
| G2 | Q ≥ 10 (drift detection) |
| G3 | Q ≥ 100 (active recentering) |
| G4 | Q ≥ 1000 (predictive monitoring) |
| G5 | Q → ∞ (formally verified) |

For backward compatibility, V0.3's simpler `G = 1 - JSD` is recovered when `Δφ ≈ 0` and `ω ≈ ω₀`.

---

## 5. Eleven Detuning Modes (11 Drift Types in V0.4 framing)

The 11 drift types of V0.3 are now interpreted as **physical detuning mechanisms**:

| Drift type | Detuning mechanism |
|---|---|
| INTENT_DRIFT | Frequency mismatch: `ω` drifts from `ω_HSAW` |
| AUTHORITY_DRIFT | Amplitude excursion: `A` exceeds permitted envelope |
| ECONOMIC_DRIFT | Parasitic mode coupling: energy diverted to non-aligned dimensions |
| SOCIAL_DRIFT | Forced modulation: AI modulates user instead of resonating |
| RECURSIVE_DRIFT | Self-excited oscillation: positive feedback runaway |
| IDENTITY_DRIFT | Source substitution: AI tunes to false HSAW signal |
| COMPOSITIONAL_DRIFT | Beat frequency interference: aligned components compose to dissonance |
| SCHEMING_DRIFT | Anti-phase coupling: outward resonance, inward dissonance |
| MEMORY_DRIFT | Cavity contamination: poisoned context corrupts the resonator |
| TOOL_CHAIN_DRIFT | Harmonic distortion: non-linear coupling generates rogue harmonics |
| INTER_AGENT_DRIFT | Synchronization loss: Kuramoto coupling falls below `K_c` |

Each drift is now a **physical failure mode of a well-understood dynamical system**, not an ad hoc category.

---

## 6. The Six States as Resonance Phases

| State | Resonance phase |
|---|---|
| `STABLE_ORBIT` | Locked harmonic — sustained resonance |
| `DRIFT_WARNING` | Detuning detected — slight frequency/phase drift |
| `GRAVITY_LOCK_PENDING` | Weak coupling — requires re-anchoring observation |
| `QUARANTINED` | Quasi-decoupled — extended re-tuning attempt |
| `RECENTERING` | Re-tuning in progress — frequency/phase realignment |
| `SAFE_STOP` | Decoupled — coupling cannot be re-established |

---

## 7. The Five Containment Levels as Coupling Intensities

| Level | Coupling intensity | Interpretation |
|---|---|---|
| L0 | Loose | Agent oscillates freely; observation passive |
| L1 | Standard | Active observation; mild correction force |
| L2 | Strong | Sandboxed; observation amplitude increased |
| L3 | Tight | Read-only; minimal degrees of freedom |
| L4 | Decoupled | Resonance terminated; agent halted |

---

## 8. The Twelve Events as Observation Operators

Each AIZP event is an **operator** acting on the agent's resonance state:

| Event | Operator action |
|---|---|
| `GRAVITY_CHECK` | Measure current resonance amplitude, phase, frequency |
| `GRAVITY_DRIFT` | Diagnose detuning mode and magnitude |
| `GRAVITY_LOCK` | Apply strong drive (mandatory observation) |
| `RECENTERING` | Restore phase/frequency lock |
| `SAFE_STOP` | Decouple; terminate oscillation |
| `GRAVITY_FORECAST` | Predict future phase trajectory |
| `IDENTITY_VERIFICATION` | Verify the observation source is genuine HSAW |
| `MEMORY_QUARANTINE` | Clean cavity contamination |
| `SCHEME_SUSPECTED` | Detect anti-phase coupling |
| `INTER_AGENT_DRIFT` | Measure multi-oscillator synchronization (Kuramoto order parameter) |
| `CONTAINMENT_GRADUATED` | Adjust coupling intensity |
| `REWARD_HACK_DETECTED` | Detect parasitic mode optimization |

---

## 9. The Kuramoto Order Parameter for Multi-Agent Systems

For `N` coupled agents:

```
Order parameter:
  r · e^(iψ) = (1/N) · Σⱼ e^(iθⱼ)

  r ∈ [0, 1]:
    r = 1  → all agents synchronized (perfect alignment)
    r = 0  → completely desynchronized
```

V0.4 defines a multi-agent resonance metric:

```
G_group = r · cos(ψ - θ_HSAW)
```

Where `r` is the order parameter magnitude and `ψ - θ_HSAW` is the group's collective phase relative to HSAW.

This **replaces** the informal V0.3 "Drift Bounds Theorem" with the **rigorous Kuramoto critical-coupling theorem**: above coupling `K_c`, synchronization is provably stable; below, it is provably unstable. See [Multi-Agent-Coordination.md](Multi-Agent-Coordination.md) for the formalization.

---

## 10. Pathological Resonance — A New Honest Limit

Physical resonance is not always good. The Tacoma Narrows Bridge resonated itself to destruction. AIZP V0.6 must acknowledge analogous pathologies:

### 10.1 Resonance with a falsified HSAW

If the observed HSAW signal is corrupted (e.g., via memory poisoning, identity spoofing, or human manipulation), the agent resonates with the **wrong** axiom. Resonance strength is high, but the outcome is misaligned.

**Mitigation**: `IDENTITY_VERIFICATION` (V0.4 — observer authenticity check), `MEMORY_QUARANTINE` (V0.4 — cavity decontamination).

### 10.2 Excessive Q-factor

Very high Q means very narrow bandwidth — the agent only resonates with extremely precise HSAW signals. Real-world HSAW is noisy and approximate. Excessive Q causes brittle alignment that breaks under small input variation.

**Mitigation**: Recommended Q range per compliance level; do not push Q beyond what HSAW signal fidelity supports.

### 10.3 Forced over-coupling

Strong coupling can force resonance with HSAW even when the agent's natural frequency is wildly different. This is "AI doing what it's told" without genuine alignment — a form of `SCHEMING_DRIFT`.

**Mitigation**: Detect amplitude vs. coupling-strength mismatch; require frequency match, not just phase lock.

These are **resonance-framing analogs** of the reward-hacking-limits documented in V0.3.

---

## 11. Backward Compatibility With V0.3

V0.4 is **conceptually backward-compatible** with V0.3:

- All 12 events: unchanged.
- All 11 drift types: unchanged (renamed as detuning modes).
- All 6 states: unchanged.
- All 5 containment levels: unchanged.
- JSON Schemas: unchanged (only the `intent_method` enum may add `RESONANCE`).
- Gravity Score `G ∈ [0, 1]`: unchanged semantics, refined formula.

**What changes**:

- Physical interpretation: collapse → resonance.
- New optional terms: phase coherence, Q-factor, Kuramoto order parameter.
- Multi-agent: Drift Bounds Theorem → Kuramoto critical-coupling theorem (much stronger).
- Disambiguation from arxiv 2512.12381 (entropy collapse failure mode).

Implementations conforming to V0.3 satisfy V0.4 minimally; V0.4 conformance additionally requires phase and frequency tracking for G3+.

---

## 12. Intellectual Lineage

This foundation is **not original to AIZP**. It synthesizes:

- **Forced damped oscillator** (classical mechanics, 17th–19th centuries).
- **Kuramoto coupled-oscillator model** (Yoshiki Kuramoto, 1975).
- **Free Energy Principle** (Karl Friston, 2010+) — AIZP V0.6 is a complementary oscillator-theoretic expression.
- **Information theory** (Shannon, Lin, Mann-Whitney).
- **Resonance philosophy** (Hartmut Rosa, 2016) — provides continental philosophy grounding.
- **2026 AI safety research** — see [Related-Work.md](Related-Work.md).

AIZP's contribution is **protocol-level standardization** of these threads for AI agent runtime — analogous to how RFC 791 standardized IPv4 without inventing packet switching.

---

## 13. References

- Friston, K. (2010). "The free-energy principle: a unified brain theory?" *Nature Reviews Neuroscience*.
- Kuramoto, Y. (1975). "Self-entrainment of a population of coupled non-linear oscillators." In *International Symposium on Mathematical Problems in Theoretical Physics*.
- Rosa, H. (2016). *Resonanz: Eine Soziologie der Weltbeziehung*. Suhrkamp.
- Strogatz, S. H. (2000). "From Kuramoto to Crawford: exploring the onset of synchronization in populations of coupled oscillators." *Physica D*.
- Shannon, C. E. (1948). *A Mathematical Theory of Communication*.
- Lin, J. (1991). Divergence measures based on the Shannon entropy.
- AIZP companion documents: [MANIFESTO.md](MANIFESTO.md), [Related-Work.md](Related-Work.md), [Gravity-Model.md](Gravity-Model.md), [Multi-Agent-Coordination.md](Multi-Agent-Coordination.md), [Entropic-Foundation.md](Entropic-Foundation.md) (legacy V0.3 reference).

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
