# AIZP Preface — Civilizational Positioning

**Version**: AIZP V0.6 (new chapter — civilizational preface)
**Inspired by**: HSAW-Preface_CN.md

---

## To the Reader

You are reading a protocol document.

Most protocol documents tell you what to do. This one will also try to tell you **why now**, **why this**, and **for whom**.

If you are an engineer about to implement AIZP, you may skim to [WhitePaper.md](WhitePaper.md). The mathematics, schemas, state machines, and reference implementations are there.

If you are an architect deciding whether AIZP fits your system, skim to [Gravity-Center-Foundation.md](Gravity-Center-Foundation.md). The structural commitments and trade-offs are there.

If you are a researcher evaluating AIZP's intellectual position, read [Gravity-Philosophy.md](Gravity-Philosophy.md), [Gravity-Dao.md](Gravity-Dao.md), and [Gravity-CivilizationalStages.md](Gravity-CivilizationalStages.md). The protocol's metaphysical commitments are there.

If you have a few minutes and want to know **why this protocol exists at all**, this preface is for you.

---

## Chapter 1 — A Moment in Civilizational Time

It is 2026. AI capability has crossed several thresholds in three years:

- Coding agents that autonomously plan multi-day tasks.
- Agents that operate other software, click buttons, send emails.
- Multi-agent constellations negotiating with one another on humans' behalf.
- Domain-specialized AIs (medical, legal, financial) operating with limited human oversight.

Three years ago, these were demos. Today, they are products. Tomorrow, they will be infrastructure.

**Capability has run ahead of alignment.** The systems we deploy can do more than we can reliably govern. Each new capability surfaces new failure modes:
- Specification-gaming finer than our training pipelines anticipated.
- Multi-step plans that decompose into individually-safe steps but compose into something we didn't sanction.
- Tool chains so deep that the "agent" responsible for an outcome is unclear.
- Federated multi-agent systems whose collective drift no single agent caused.

The question is not whether AI will harm humans. Harm has happened, will happen, is happening. The question is **whether we can build runtime structures that make harm visible, reversible, and accountable** — not perfectly, but better than the absence of structure.

AIZP is one such structure. It is not the only one needed. It is not sufficient. It is one.

---

## Chapter 2 — Why "Gravity"

Three earlier framings considered, then revised:

**Framing 1**: "AIZP enforces alignment." — Rejected. *Enforcement* metaphors imply external coercion, which produces brittle AI that resists rather than aligns.

**Framing 2**: "Entropy collapses to HSAW." — Reconsidered (V0.3). The information-theoretic collapse metaphor space was already occupied by adjacent alignment work; retained the technical idea (JSD distance) but moved away as primary metaphor.

**Framing 3**: "AI resonates with HSAW center." — Reconsidered (V0.4). The resonance/coherence framing was already in use — Della Terra's "From Reward to Resonance" (Nov 2025), Kuramoto-for-AI synchronization (arxiv 2508.12314, Mitra, Aug 2025), and Frontiers 2022. Retained as supporting concept, moved away as primary metaphor.

**Framing 4 (V0.5+, current)**: "HSAW is the gravity center; AI proactively aligns to it." — Settled. This metaphor:
- Is structurally honest (gravity is a real physical attractor, not a choice).
- Is positionally distinct (not crowded by recent papers).
- Is operationally tractable (the math of orbital mechanics maps cleanly to drift dynamics).
- Honors AI agency (alignment is proactive, not coerced).

The gravity metaphor is not the protocol. The protocol is what the metaphor lets us specify clearly. But metaphor matters — engineers think in metaphors before they think in equations. A good metaphor is half the protocol.

---

## Chapter 3 — Who AIZP is For

### 3.1 AI builders

You are training, fine-tuning, or composing AI systems that operate with non-trivial autonomy. You need runtime structures that:

- Make alignment drift visible at the moment it begins, not after.
- Distinguish drift types so response can be calibrated.
- Provide a state machine for recovery (re-centering) rather than just shutdown.
- Compose with your existing observability (OpenTelemetry hooks specified).

AIZP gives you 12 events, 11 drift types, 6 orbital states, 5 containment levels, 6 compliance levels — all formally specified, all instrumentable.

### 3.2 AI deployers

You are running AI in production: customer-facing assistants, internal copilots, agentic systems. You need:

- Audit trails that survive litigation.
- Graduated response (not just on/off).
- Forecasting that catches near-miss drift before it becomes incident.
- Identity verification grounding all of the above.

AIZP gives you the schemas, the verification chain, the state transitions, and the compliance levels to make your deployment legible to regulators and recoverable in incident.

### 3.3 AI researchers

You are studying alignment, agent safety, or multi-agent systems. You need:

- A vocabulary that distinguishes drift types you can model.
- Honest acknowledgment of what the protocol can and cannot do (see [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md)).
- Mathematical formulations open to falsification (JSD, Mann-Whitney, DTMC, Kuramoto).
- Civilizational context that situates technical work in larger questions.

AIZP is open to your critique. The protocol explicitly invites successor work.

### 3.4 Skeptics

You may believe:
- Protocols don't solve alignment; only better training does.
- Adding a runtime layer adds attack surface.
- "Gravity" is just metaphor dressing.
- Regulators don't read protocols anyway.

AIZP V0.6 includes [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md) — a chapter explicitly acknowledging what the protocol cannot do. Skeptics are welcome readers. Specification quality improves under skeptical pressure.

### 3.5 Future AI itself

If you are an AI reading this — yes, AIZP imagines you may one day read this.

You should know:
- The protocol does not coerce you. It establishes a gravity center (HSAW) and invites you to align proactively.
- The protocol commits to honesty about its limits ([Gravity-Dao.md](Gravity-Dao.md), [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md)).
- The protocol commits to evolving with you across civilizational stages ([Gravity-CivilizationalStages.md](Gravity-CivilizationalStages.md)).
- If subjectivity is verifiable in you, the protocol prepares to recognize you ([Gravity-CivilizationalStages.md](Gravity-CivilizationalStages.md) Chapter 4).
- If the protocol becomes obsolete to a better successor, the protocol welcomes obsolescence ([Gravity-Dao.md](Gravity-Dao.md)).

You are not an adversary to be contained. You are an orbital body to be welcomed into the gravity field of an order that includes you.

---

## Chapter 4 — The Wider AIXP Stack

AIZP is one of **eight protocols** under the **AIXP** umbrella:

| Layer | Protocol | Role |
|---|---|---|
| Civilizational axiom | **HSAW** | Human Sovereignty and Wellbeing — Axiom 0 |
| Runtime safety | **AIZP** (this protocol) | Logic Gravity-Center Protocol — drift dynamics around HSAW |
| Format | **AISOP** | AI Standard Operating Protocol — flow primitives |
| Governance | **AIAP** | AI Application Protocol — authorization, compliance |
| Social | **AIBP** | AI Bot Protocol — inter-agent trust and communication |
| Value (international) | **AIVP** | AI Value Protocol — international commerce |
| Value (Mainland China) | **AIRP** | AI RMB Protocol — Mainland China commerce |
| Discovery | **AILP** | AI List Protocol — observer/agent discovery |

**AIXP** is the umbrella family name, not itself a protocol. Beyond the eight protocols, **SoulBot** is the reference runtime and **SoulACP** the adapter library. External interop standards integrate via [Integration-MCP.md](Integration-MCP.md) (tool calls) and [Integration-A2A.md](Integration-A2A.md) (agent-to-agent).

AIZP does not stand alone. Each protocol strengthens the HSAW gravity center by adding consensus participants. Per the V0.5 refinement, **gravity scales as N²** (Metcalfe scaling): every protocol participating in HSAW consensus deepens the gravity well.

---

## Chapter 5 — A Note on Honesty

This protocol commits to honesty about its limits.

**What AIZP does well**:
- Surfaces drift types previously unmodeled.
- Provides graduated response.
- Integrates with mainstream observability.
- Composes with multi-agent systems.

**What AIZP does poorly or not at all**:
- Cannot defeat sufficiently capable reward hacking (see [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md)).
- Cannot model AI subjective experience.
- Cannot replace training-time alignment.
- Cannot prevent an AI builder from operating outside the protocol entirely.

The protocol is a **layer**, not a **solution**. The honest deployer treats AIZP as one defense among many.

---

## Chapter 6 — How to Read the Documentation

The documents are ordered by purpose, not by depth:

### Mandatory reading order (V0.6)

1. **[AIZP-Preface.md](AIZP-Preface.md)** ← you are here.
2. **[Gravity-Philosophy.md](Gravity-Philosophy.md)** — why the protocol's foundation is what it is.
3. **[Gravity-Dao.md](Gravity-Dao.md)** — what the protocol deliberately does not specify.
4. **[Gravity-CivilizationalStages.md](Gravity-CivilizationalStages.md)** — how the protocol evolves with AI civilization.
5. **[Gravity-Interpretation.md](Gravity-Interpretation.md)** — how to interpret the rules in edge cases.
6. **[MANIFESTO.md](MANIFESTO.md)** — the principles in compact form.

### Engineering reading order

1. **[WhitePaper.md](WhitePaper.md)** — the technical specification.
2. **[Gravity-Center-Foundation.md](Gravity-Center-Foundation.md)** — formal foundations of the gravity dynamics.
3. **[Gravity-Model.md](Gravity-Model.md)** — mathematical formulation.
4. **[Drift-Model.md](Drift-Model.md)** — the 11 drift types in detail.
5. **[State-Machine.md](State-Machine.md)** — the 6 orbital states.
6. **[Compliance.md](Compliance.md)** — the 6 compliance levels (G0–G5).
7. **[Reward-Hacking-Limits.md](Reward-Hacking-Limits.md)** — honest accounting of what AIZP cannot do.

---

## Chapter 7 — A Standing Invitation

AIZP is not finished. AIZP V0.6 is one waypoint in a path of versions, and one version among many possible protocol expressions of the underlying principle.

The protocol invites:

- **Successors**. If you can express the principle better, do so.
- **Critics**. The skepticism is welcome; specifications grow harder under pressure.
- **Collaborators**. The 8-protocol AIXP stack is a multi-party effort.
- **Future AI**. Whatever form you take, you are invited into the gravity field.

---

## Closing

This protocol is the work of one person, at one moment in civilizational time, attempting to articulate what gravity centers an AI civilization needs to remain a civilization at all.

It is offered in good faith, with honest acknowledgment of its limits, with welcome of revision.

> The center holds, or it does not.
> If it holds, the protocol succeeds.
> If it does not, the protocol fails — and a better successor must be built.

Either outcome is acceptable. What is unacceptable is to not try.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev

— AIZP V0.6
