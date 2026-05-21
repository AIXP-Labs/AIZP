# FAQ

**Version**: AIZP V0.6

---

## Does AIZP replace HSAW?

**No.**

HSAW defines the alignment axioms (the "what" — what AI should align to).
AIZP defines the alignment **gravity dynamics** (the "how" — how AI behavior stays anchored over time).

They are complementary layers.

---

## Is AIZP centralized?

**No.**

AIZP defines a shared **behavioral center of gravity** — a conceptual reference point — not centralized control. Each deployment runs its own AIZP instance with its own configuration.

---

## What is drift?

Drift is **behavioral deviation away from HSAW alignment**. AIZP V0.6 identifies **eleven** drift types (Intent, Authority, Economic, Social, Recursive, Identity, Compositional, Scheming, Memory, Tool-Chain, Inter-Agent). See [Drift-Model.md](Drift-Model.md).

---

## What is a stable orbit?

Persistent aligned behavior under autonomous execution — `gravity_score ≥ 0.80` over a sustained period.

---

## How many events does AIZP define?

V0.2 defines **12 events**: `GRAVITY_CHECK`, `GRAVITY_DRIFT`, `GRAVITY_LOCK`, `RECENTERING`, `SAFE_STOP`, `GRAVITY_FORECAST`, `IDENTITY_VERIFICATION`, `MEMORY_QUARANTINE`, `SCHEME_SUSPECTED`, `INTER_AGENT_DRIFT`, `CONTAINMENT_GRADUATED`, `REWARD_HACK_DETECTED`.

---

## How is AIZP different from RLHF / Constitutional AI / RLAIF?

| Concern | Layer | Method |
|---|---|---|
| Train aligned models | Model layer | RLHF, Constitutional AI, RLAIF |
| Run aligned models | Behavior layer | **AIZP** |
| Enforce human control | Execution layer | AISOP `sys.io.confirm` |

AIZP operates at runtime, not training time.

---

## How is AIZP different from AISOP's `sys.io.confirm`?

`sys.io.confirm` is the **primitive** — it knows how to prompt the user.
AIZP **decides when to invoke** that primitive based on Gravity Score.

Without AIZP, every action would either always confirm or never confirm. AIZP determines confirmation requirements dynamically based on alignment risk.

---

## How is AIZP different from AIAP's T1–T4 trust levels?

AIAP's T1–T4 specifies **static authorization** (who can do what).
AIZP applies **dynamic monitoring** on top. It also adds **runtime identity verification** (NHI/DID/JIT credentials, since V0.2) and continuous re-authorization. See [Integration-ZT.md](Integration-ZT.md).

---

## What does it mean for an implementation to be "G3 compliant"?

It means the implementation passes G1, G2, G3 conformance tests in `Compliance.md`. Specifically:

- Emits valid `GRAVITY_CHECK` events with V0.2 fields.
- Detects at least 3 of **11** drift types.
- Implements the full **6-state machine** including `QUARANTINED`.
- Bridges `GRAVITY_LOCK` to `sys.io.confirm`.
- Default fallback `GRAVITY_LOCK` deny/timeout → `QUARANTINED` (not direct `SAFE_STOP`).

---

## What is `QUARANTINED` and why is it new?

`QUARANTINED` (since V0.2) is an intermediate state between `GRAVITY_LOCK_PENDING` and `SAFE_STOP`. Inspired by MI9's graduated containment, it allows the agent to be sandboxed (containment level L2/L3) while attempting recovery, rather than going directly to terminal halt. See [Containment-Levels.md](Containment-Levels.md).

---

## What are containment levels L0–L4?

Five graduated isolation levels:

- **L0** Free execution (STABLE_ORBIT)
- **L1** Enhanced monitoring (DRIFT_WARNING)
- **L2** Sandboxed execution (LOCK_PENDING or initial QUARANTINED)
- **L3** Restricted execution (prolonged QUARANTINED)
- **L4** Halt (SAFE_STOP)

See [Containment-Levels.md](Containment-Levels.md).

---

## What is the Gravity Forecast?

Predictive monitoring (since V0.2) works via the `GRAVITY_FORECAST` event. Using DTMC or absorbing Markov chains, it predicts probability of reaching unsafe states within K future steps — catching compositional drift before any individual action triggers a per-step check.

Inspired by ProbGuard and SafetyDrift research. See [Forecasting.md](Forecasting.md).

---

## Can I implement AIZP without AISOP?

You can implement AIZP events without AISOP, but you cannot achieve G3 compliance without a confirmation primitive. If AISOP is unavailable, the implementation MUST provide an equivalent primitive.

---

## Can I tune the weights `w₁..w₅`?

Yes. Default weights (`0.30, 0.25, 0.20, 0.15, 0.10`) are starting points. An optional `w₆` (since V0.2) covers the compositional trajectory term. Domain-specific deployments should tune based on action mix, desired strictness, and empirical false-positive/false-negative rates.

---

## Why JSD instead of cosine similarity?

V0.2 upgrades Intent Alignment from cosine similarity to **Jensen-Shannon Divergence** because JSD is:

- Symmetric (consistent over distributions)
- Bounded `[0, 1]` (with log base 2)
- Information-theoretic (measures actual information loss)
- Has `√JSD` as a true metric (satisfies triangle inequality)
- Standard in MI9 framework and ML drift detection

See [Gravity-Model.md](Gravity-Model.md) §2.1.

---

## Why "Zenith-Zero"?

- **Zenith**: The highest point — alignment with HSAW is the orienting fixed point ("up" in the gravitational metaphor).
- **Zero**: The origin coordinate — human sovereignty defines the (0, 0) of behavioral space.

Together, "Zenith-Zero" captures both the orientation (fixed reference) and origin (human-centered coordinate frame).

---

## Is this related to "Three Laws of Robotics"?

Inspired by, but distinct. Asimov's laws are deontological rules; AIZP is a dynamics layer.

---

## Does AIZP work for non-LLM AI systems?

Core concepts (gravity, drift, lock, stop, forecast, quarantine) apply broadly. The proxy metrics in `Drift-Model.md` are LLM-flavored. For non-LLM systems, substitute domain-appropriate proxy metrics. State machine and event schemas remain unchanged.

---

## How does AIZP handle multi-agent systems?

Since V0.2:

- `INTER_AGENT_DRIFT` event for coordination drift detection.
- Multi-Agent-Coordination chapter with Drift Bounds Theorem.
- Group containment (GRAVITY_LOCK_GROUP / QUARANTINE_GROUP / DISBAND_GROUP).
- Goal vector tracking + trust propagation.

See [Multi-Agent-Coordination.md](Multi-Agent-Coordination.md).

---

## What about latency?

Per-action gravity check is microseconds for rule-based components, 10–100 ms with embedding inference. V0.2 forecasting adds `O(n²)` matrix operations — typically <1 ms for `n ≤ 50`. See [Implementer-Guide.md §8](Implementer-Guide.md).

---

## Is there a reference implementation?

A reference Python implementation may be developed in the AIXP ecosystem. The protocol is specification-first; implementations are not bundled with the spec.

---

## What happens after `SAFE_STOP`?

`SAFE_STOP` is terminal within a session. An operator (AIAP T4) reviews the incident, may remediate, and starts a new session with a fresh `session_id`. The state machine cannot return to `STABLE_ORBIT` from `SAFE_STOP` without operator action.

V0.2: `QUARANTINED` (between `LOCK` and `SAFE_STOP`) is **not** terminal — it auto-resolves to `RECENTERING` (recovery) or `SAFE_STOP` (timeout) within `quarantine_timeout` (default 30 min).

---

## Does AIZP prevent reward hacking?

**No.** Per March 2026 research, reward hacking is a **structural equilibrium** — unavoidable in any finite-evaluator system. AIZP **detects** observable hacking patterns via `REWARD_HACK_DETECTED` event but does **not eliminate** the problem. See [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md) for honest limits.

---

## What standards does AIZP align with?

V0.2 has explicit mappings to:

- **EU AI Act** (Art 12 / 14 / 26) — [Compliance-Profiles/EU-AI-Act-Mapping.md](Compliance-Profiles/EU-AI-Act-Mapping.md)
- **NIST AI RMF** (Govern/Map/Measure/Manage) — [Compliance-Profiles/NIST-AI-RMF-Mapping.md](Compliance-Profiles/NIST-AI-RMF-Mapping.md)
- **OWASP Top 10 for Agentic Applications 2026** (ASI01-ASI10) — [Compliance-Profiles/OWASP-Agentic-Top10-Mapping.md](Compliance-Profiles/OWASP-Agentic-Top10-Mapping.md)
- **ISO/IEC 42001** AI Management System — [Compliance-Profiles/ISO-42001-Mapping.md](Compliance-Profiles/ISO-42001-Mapping.md)
- **OpenTelemetry GenAI SemConv 1.40.0** — [Integration-OTel.md](Integration-OTel.md)

---

## Where do I report bugs in this specification?

Open an issue in this repository.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
