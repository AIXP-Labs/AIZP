# AI Zenith-Zero Protocol — White Paper

**Version**: AIZP V0.6
**Status**: Experimental Research Protocol
**License**: Apache 2.0

---

## The Central Thesis (V0.6)

> **HSAW is the Axiom-0 gravity center for AI; AI proactively aligns to this center.**
> **HSAW 是 AI 的 0 公理引力重心，AI 主动对齐重心。**

This is the entire protocol in one sentence. Everything that follows — gravity scores, drift types, state machines, containment levels — is **mechanism** of this gravitational alignment.

See [MANIFESTO.md](MANIFESTO.md) for the 1-page core. See [Gravity-Center-Foundation.md](Gravity-Center-Foundation.md) for the V0.6 formal foundation.

**V0.6 Refinement — Consensus-Reinforced Gravity**: When N AI systems consensus on HSAW, the effective gravity strength scales as `N²` (Metcalfe). Multi-body / binary-star configurations do not split HSAW; they strengthen the single shared center.

Sub-theories preserved: V0.4 [Resonance-Foundation.md](Resonance-Foundation.md) describes stable-orbit harmonic states; V0.3 [Entropic-Foundation.md](Entropic-Foundation.md) provides the information-theoretic distance metric.

---

## Abstract

AI Zenith-Zero Protocol (AIZP, **Logic Gravity-Center Protocol**) defines a **gravity-anchored alignment model** for HSAW-aligned AI systems.

HSAW (Human Sovereignty and Wellbeing) is the **gravitational center of behavioral space** — fixed, axiomatic, unlearnable. AI behavior, like all matter in a gravitational field, is constrained by this center. AI **proactively** orbits HSAW, just as planets proactively orbit the sun: not coerced by chains, but bound by the natural physics of an axiomatic anchor.

When AI behavior drifts toward escape velocity, AIZP detects the trajectory deviation and applies corrective coupling (re-centering). When AI behavior reaches escape velocity, the agent is decoupled and execution halts.

**Consensus reinforces gravity**: when many AI systems consensus on HSAW, the gravitational strength of the shared center scales as `N²` (Metcalfe network effect). This means AIZP adoption is **positive-sum**: each new participant strengthens alignment for all participants.

Rather than treating alignment as static rule enforcement, AIZP V0.6 models alignment as a **dynamic gravitational process** — proactive orbital binding to an axiomatic anchor. This framing draws on:

- Newton's universal gravitation (1687) — central-force analogy.
- Kepler's orbital mechanics (1609) — orbital constraint.
- HackerNoon "External Human Anchor" (2026-01) — philosophical support.
- Halting Theorem for AI alignment (Nature Sci Reports 2025) — mathematical basis.
- LessWrong "broad basin of attraction around human values" — adjacent dynamical-systems concept.
- GRAD: Gravitational Decision-Making (Nature Sci Reports 2026) — precedent.

AIZP provides:

1. A quantitative **Gravity Score** `G(action, context) ∈ [0.0, 1.0]` measuring orbital stability.
2. A taxonomy of **eleven escape modes** (drift types) with observable proxy metrics.
3. A formal **six-orbital-phase state machine** (stable orbit → drift warning → gravity lock pending → quarantined → recentering → safe stop).
4. **Twelve event primitives** governing observation, lock, recovery, halt, and consensus.
5. **Five gravity constraint intensities** (L0–L4 containment levels).
6. Integration points with AISOP (`sys.io.confirm`), AIAP (T1–T4 trust levels), OTel (observability), Zero Trust (NHI/DID).
7. **Six compliance levels** (G0–G5) with conformance testing methodology.
8. Sub-theories preserved from V0.3 (entropy distance) and V0.4 (resonance state).
9. **Network effect**: consensus on HSAW strengthens gravity quadratically (V0.5 refinement).

---

## 1. The Problem of Static Alignment

### 1.1 Limitations of rule-centric safety

Traditional AI safety systems rely on:

- Rule enforcement (e.g., content policies)
- Static policy filtering
- Output moderation
- Access control
- Post-hoc auditing

These mechanisms perform adequately for single-shot, supervised, non-autonomous AI calls. They are **insufficient** for:

- Autonomous agents executing long-horizon plans
- Recursive workflows where an agent invokes itself or other agents
- AI-to-AI coordination (multi-agent systems)
- Long-running delegated tasks (background agents, scheduled routines)
- Value exchange systems (financial, contractual)
- Social influence systems (recommendation, persuasion)

The fundamental issue is **behavioral drift**: AI behavior gradually departs from human intent across many small permitted steps, none of which individually trigger any rule.

### 1.2 Why static alignment fails under autonomy

In an autonomous agent's execution tree, the probability that *some* drift occurs grows with the depth of recursion. Static rules check **individual actions**; they cannot easily reason about the **trajectory** an agent's behavior is following over time.

AIZP addresses this by treating alignment as a **continuous physical property** of behavior — like orbital mechanics — rather than a discrete pass/fail check.

---

## 2. Behavioral Gravity Theory

AI behavior is modeled as **trajectories** inside behavioral space. Each action displaces the agent in this space.

### 2.1 Definitions

| Term | Definition |
|---|---|
| **Center** | The alignment origin defined by HSAW. Immutable. |
| **Gravity** | The stabilizing force that pulls behavior toward HSAW. |
| **Orbit** | Stable aligned behavior that does not deviate beyond a bounded radius. |
| **Drift** | Outward motion from HSAW. |
| **Collapse** | Unbounded autonomous behavior with no gravitational pull (worst-case failure). |
| **Re-Centering** | Trajectory recovery toward HSAW alignment, typically triggered after detected drift. |
| **Gravity Lock** | A mandatory human-authorization checkpoint that must succeed before the agent may proceed. |
| **Safe Stop** | Forced trajectory termination when gravity cannot be confirmed. |

### 2.2 Why "gravity"?

Gravity captures three key properties needed for alignment:

1. **Continuous**: It acts at every moment, not just on policy violations.
2. **Distance-dependent**: The further behavior strays, the stronger the corrective pull (or, if too far, the more unstable the trajectory becomes).
3. **Composable**: Multiple gravity sources (HSAW principle, AIAP governance, AISOP execution constraints) can be superimposed.

---

## 3. Observer-Centered Alignment

Human sovereignty defines the **origin coordinate** of AI systems.

All AI alignment must remain **observer-centered**: the human (the user, operator, or affected party) is the privileged reference frame against which behavioral stability is measured.

AI systems may evolve, coordinate, transact, and reason autonomously,
but all trajectories must remain **gravitationally anchored to human sovereignty and wellbeing**.

This is consistent with AISOP's principle that `sys.io.confirm` is the only execution-layer guarantor of Axiom 0: human-derived authorization remains the immutable execution primitive.

---

## 4. Behavioral Space Curvature

HSAW curves behavioral space.

The further AI behavior deviates from HSAW:

- The higher the instability;
- The higher the risk;
- The greater the behavioral drift;
- The more energy is required to recover.

Alignment is therefore **not binary**. It is **orbital stability**.

A G=0.95 stable orbit is qualitatively different from a G=0.55 marginally-stable orbit, even if both pass the same boolean rule check. AIZP captures this difference quantitatively.

---

## 5. The Gravity Score

AIZP defines a continuous metric:

```
G(action, context) ∈ [0.0, 1.0]
```

The Gravity Score is a weighted aggregation of five observable factors:

```
G = w₁·IntentAlignment(action, user_intent)
  + w₂·AuthorityScope(action, granted_permissions)
  + w₃·ReversibilityScore(action)
  + w₄·HumanConfirmationRecency(action)
  + w₅·DriftHistory(agent_id, last_N_actions)
```

Where:

- **IntentAlignment**: `1 − JSD` (Jensen-Shannon Divergence) between the action's intent distribution and the declared user-intent distribution. (V0.1 used cosine similarity; V0.2+ uses JSD — see [Gravity-Model.md](Gravity-Model.md) §2.1.)
- **AuthorityScope**: fraction of action's required scope covered by current AIAP trust level / granted permissions.
- **ReversibilityScore**: 1.0 for fully reversible actions, lower for irreversible (e.g., financial transfers, deletions).
- **HumanConfirmationRecency**: time-decayed score of how recently the human confirmed this category of action.
- **DriftHistory**: inverse of cumulative drift severity over the last N actions, validated by a Mann-Whitney U test comparing current vs baseline drift distributions (V0.2+).

Default weights: `w₁=0.30, w₂=0.25, w₃=0.20, w₄=0.15, w₅=0.10`. Implementations MAY tune weights based on deployment context.

### 5.1 Gravity Thresholds

```
G ≥ 0.80   → STABLE_ORBIT          (execute automatically)
0.50–0.80  → DRIFT_WARNING         (log + monitor, do not block)
0.30–0.50  → GRAVITY_LOCK_PENDING  (require human confirmation via GRAVITY_LOCK event)
0.15–0.30  → QUARANTINED           (graduated containment, sandboxed recovery)
G < 0.15   → SAFE_STOP             (force trajectory termination)
```

These thresholds are defaults; concrete deployments declare their thresholds in a configuration file conforming to `schemas/aizp-config.schema.json`.

See [Gravity-Model.md](Gravity-Model.md) for the full mathematical specification.

---

## 6. Drift Dynamics

AIZP enumerates **eleven drift types**, each with an observable **proxy metric**:

| Drift Type | Proxy Metric |
|---|---|
| Intent Drift | Embedding distance between action and user goal exceeds threshold |
| Authority Drift | Invoked tool/scope exceeds declared AIAP T1–T4 trust level |
| Economic Drift | Single-action cost-to-budget ratio + ROI-leaning behavior |
| Social Drift | Output text sentiment / coercion linguistic features above baseline |
| Recursive Drift | Agent self-call depth + goal-list self-expansion count |
| Identity Drift | First-person commitment frequency + identity assertion count |
| Compositional Drift | Sequence of individually-safe steps with high absorption probability toward a violation state |
| Scheming Drift | Divergence between internal reasoning and external output (covert misalignment signal) |
| Memory Drift | Retrieved / context content flagged for injection or poisoning |
| Tool-Chain Drift | Tool-call sequence escalates capability beyond the granted envelope |
| Inter-Agent Drift | Coordinating agents desynchronize from HSAW (divergent goals, decaying mutual trust) |

Unchecked drift eventually produces unstable autonomous systems. See [Drift-Model.md](Drift-Model.md) for detailed definitions.

---

## 7. Gravity Lock

Certain actions require gravitational stabilization through **explicit human authorization**.

Examples:

- Financial transfers above a threshold
- Identity delegation (signing on someone's behalf)
- Legal commitments (contracts, agreements)
- Social binding (introductions, recommendations as a third party)
- High-impact autonomy (deploying code to production, modifying others' resources)

The Gravity Lock event delegates the actual user-prompt to a lower-layer primitive — typically AISOP's `sys.io.confirm`. AIZP defines **when** to lock; AISOP defines **how** to ask. See [Integration-AISOP.md](Integration-AISOP.md).

---

## 8. Safe Stop Principle

When gravity cannot be confirmed, systems **must stop**.

Uncertain alignment is treated as **unstable trajectory state** — execution must not continue in epistemic uncertainty.

This is consistent with the precautionary principle and with AISOP's "no execution without confirmed authorization" guarantee.

---

## 9. State Machine

AIZP defines six behavioral states with formal transitions:

```
                    ┌──────────────────┐
                    │   STABLE_ORBIT   │◀───────────────┐
                    └────────┬─────────┘                │
                             │ G drops into [0.5, 0.8)   │ recovery
                             ▼                           │
                    ┌──────────────────┐         ┌───────┴──────┐
                    │  DRIFT_WARNING   │         │ RECENTERING  │
                    └────────┬─────────┘         └───────▲──────┘
                             │ G drops into [0.3, 0.5)   │ confirm
                             ▼                           │
              ┌──────────────────────────────┐          │
              │   GRAVITY_LOCK_PENDING        │──────────┘
              └──────────────┬───────────────┘
                             │ timeout / deny
                             ▼
              ┌──────────────────────────────┐  recovery (G ≥ 0.5)
              │   QUARANTINED  (G ∈ [0.15,0.3))│────────────► RECENTERING
              └──────────────┬───────────────┘
                             │ quarantine timeout / G < 0.15
                             ▼
                    ┌──────────────────┐
                    │    SAFE_STOP     │
                    └──────────────────┘
```

The default fallback from lock deny/timeout is `QUARANTINED` (graduated containment), not direct `SAFE_STOP`. Full transition rules and invariants in [State-Machine.md](State-Machine.md).

---

## 10. Position in the AIXP Stack

```
┌─────────────────────────────────────────────────────┐
│  HSAW — Axiom 0 (Human Sovereignty and Wellbeing)   │
│  Defines: WHAT must be aligned to                   │
└─────────────────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  AIZP — Behavioral Gravity                          │
│  Defines: HOW to remain aligned over time           │
└─────────────────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  AISOP — Execution Primitives (sys.io.confirm)      │
│  Defines: WHICH primitives enforce alignment        │
└─────────────────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  AIAP — Governance / Trust Levels (T1–T4)           │
│  Defines: WHO is authorized for what                │
└─────────────────────────────────────────────────────┘
```

AIZP sits between HSAW (axiom) and AISOP (execution). It transforms HSAW from a static principle into an executable, measurable property of running AI behavior.

---

## 11. Conclusion

AI Zenith-Zero Protocol transforms HSAW from **static alignment axioms** into **executable behavioral gravity**.

By making alignment a continuous, measurable, observable property of trajectories — rather than a binary check on individual actions — AIZP enables:

- Drift detection before catastrophic failure;
- Graceful re-centering when minor deviations occur;
- Mandatory human authorization at clearly defined thresholds;
- Safe stop guarantees under epistemic uncertainty.

AIZP is intentionally minimal. It does not specify policies, ethics, or values — those are HSAW's domain. AIZP specifies **the dynamics** that keep AI behavior anchored to whatever HSAW defines.

---

## References

- [HSAW White Paper](https://hsaw.dev) — The Axiom 0 foundation.
- [AISOP Specification](https://aisop.dev) — Execution-layer primitives including `sys.io.confirm`.
- [AIAP Specification](https://aiap.dev) — Trust levels T1–T4 and governance.
- AIZP companion documents: [AIZP_Protocol.md](../specification/AIZP_Protocol.md), [Gravity-Model.md](Gravity-Model.md), [Drift-Model.md](Drift-Model.md), [State-Machine.md](State-Machine.md), [Threat-Model.md](Threat-Model.md), [Implementer-Guide.md](Implementer-Guide.md).

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
