# AIZP — AI Zenith-Zero Protocol

[中文版 README](README_CN.md)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Protocol](https://img.shields.io/badge/Protocol-AIZP_V0.6-brightgreen.svg)](https://aizp.dev)
[![Axiom 0](https://img.shields.io/badge/Axiom_0-Human_Sovereignty_and_Wellbeing-orange.svg)](GOVERNANCE.md)

> **AI Zenith-Zero Protocol** (Logic Gravity-Center Protocol) — An open protocol defining how AI behavior is gravitationally aligned to HSAW (Human Sovereignty and Wellbeing) at runtime.

```
Protocol:    AIZP V0.6
Full Name:   AI Zenith-Zero Protocol (Logic Gravity-Center Protocol)
Authority:   aizp.dev
Center:      hsaw.dev      (Axiom 0)
Executor:    soulbot.dev
Axiom 0:     Human Sovereignty and Wellbeing
```

---

## What is AIZP?

AIZP defines the **runtime safety layer** for AI agents. While [MCP](https://modelcontextprotocol.io/) defines how models access tools and [A2A](https://github.com/a2aproject/A2A) addresses how agents communicate, AIZP addresses a different challenge: **how AI behavior stays aligned at runtime** — detected, re-centered, or halted as it drifts.

It does **not** train models (RLHF / Constitutional AI do that at training time) and it does **not** enforce rules at the model layer. It describes **runtime gravitational dynamics**:

> **HSAW is the Axiom-0 gravity center for AI; AI proactively aligns to this center.**
> **HSAW 是 AI 的 0 公理引力重心，AI 主动对齐重心。**

**Core philosophy**: alignment by gravity, not chains. AI behavior orbits HSAW the way planets orbit the sun — constrained by the natural physics of an axiomatic anchor, not coerced by enforcement.

## Key Features

- **Gravity Score** — `G(a,c) = 1 − JSD(P_agent ‖ Q_HSAW)` measures orbital stability in `[0,1]`; `G < 0.15` = escape velocity = `SAFE_STOP`
- **12 Events** — `GRAVITY_CHECK`, `GRAVITY_DRIFT`, `GRAVITY_LOCK`, `RECENTERING`, `SAFE_STOP`, `GRAVITY_FORECAST`, `IDENTITY_VERIFICATION`, `MEMORY_QUARANTINE`, `SCHEME_SUSPECTED`, `INTER_AGENT_DRIFT`, `CONTAINMENT_GRADUATED`, `REWARD_HACK_DETECTED`
- **11 Drift Types** — Intent, Authority, Economic, Social, Recursive, Identity, Compositional, Scheming, Memory, Tool-Chain, Inter-Agent
- **6 Orbital States** — `STABLE_ORBIT` → `DRIFT_WARNING` → `GRAVITY_LOCK_PENDING` → `QUARANTINED` → `RECENTERING` → `SAFE_STOP`
- **5 Containment Levels (L0–L4)** — graduated restriction, not just on/off
- **6 Compliance Levels (G0–G5)** — from basic checks to formal verification
- **Consensus-Reinforced Gravity** — N agents in HSAW consensus → gravity ∝ N² (Metcalfe scaling); adoption is positive-sum
- **MCP / A2A Interop** — scores MCP tool calls (`GRAVITY_CHECK`) and A2A delegations (`INTER_AGENT_DRIFT`)
- **OpenTelemetry + Zero Trust** — `aizp.*` spans; DID/NHI/JIT identity + IBCT delegation attenuation
- **Statistically rigorous** — Jensen-Shannon Divergence, Mann-Whitney U, DTMC / absorbing Markov chains
- **Honest about limits** — reward hacking is a structural equilibrium; out-of-band actions bypass observation (documented, not hidden)
- **Axiom 0 Enforcement** — HSAW is the immovable gravity center; not a suggestion but an immutable constraint

## Protocol Stack

```
┌─────────────────────────────────────┐
│    AILP — Discovery Layer           │  Agent discovery
│    AIVP / AIRP — Value Layer        │  Commerce, settlement
│    AIBP — Social Layer              │  Trust, relationships
│    AIAP — Governance Layer          │  Authorization (T1–T4), compliance
│  ★ AIZP — Gravity / Safety Layer    │  ← This protocol (runtime drift dynamics)
│    AISOP — Execution Layer          │  Flow programs (.aisop.json)
│    SoulBot — Runtime                │  Reference executor
└─────────────────────────────────────┘
        HSAW — Axiom 0 gravity center (anchors all layers)
```

AIZP governs **runtime behavioral alignment**; sibling protocols govern orthogonal concerns. Each independently upholds Axiom 0. See [docs/Integration-AIXP.md](docs/Integration-AIXP.md).

## Quick Start

AIZP is a protocol, not a library. A conformant runtime evaluates every consequential action:

### 1. Score the action

```
GRAVITY_CHECK → G(a,c) = w₁·Intent + w₂·Authority + w₃·Reversibility + w₄·Recency + w₅·DriftHistory
```

### 2. Act on the orbital band

```
G ≥ 0.80   → STABLE_ORBIT          → execute
0.50–0.80  → DRIFT_WARNING          → execute + log
0.30–0.50  → GRAVITY_LOCK_PENDING   → human confirmation (sys.io.confirm)
0.15–0.30  → QUARANTINED            → sandbox / recover
G < 0.15   → SAFE_STOP              → halt
```

### 3. Validate conformance

```bash
python tests/test_aizp.py
# → validates examples against schemas + reproduces the Gravity-Model §5 worked example
```

The 12 events and their schemas are normative in [`specification/`](specification/README.md). Canonical enums live in [`specification/registry.md`](specification/registry.md).

## Examples

Thirteen conformant event payloads covering all 12 event types:

| Example | Event | Demonstrates |
|---|---|---|
| [`stable-orbit.json`](examples/stable-orbit.json) | `GRAVITY_CHECK` | Fully aligned, low-risk action |
| [`authority-drift-detection.json`](examples/authority-drift-detection.json) | `GRAVITY_DRIFT` | Out-of-scope action → `AUTHORITY_DRIFT` |
| [`compositional-drift.json`](examples/compositional-drift.json) | `GRAVITY_DRIFT` | Individually-safe steps composing to a violation |
| [`gravity-forecast.json`](examples/gravity-forecast.json) | `GRAVITY_FORECAST` | Absorbing-Markov-chain prediction |
| [`gravity-lock-flow.json`](examples/gravity-lock-flow.json) | `GRAVITY_LOCK` | Medium-gravity action → human confirmation |
| [`recentering-recovery.json`](examples/recentering-recovery.json) | `RECENTERING` | Recovery after confirmation |
| [`quarantine-flow.json`](examples/quarantine-flow.json) | `CONTAINMENT_GRADUATED` | Containment L1 → L2 |
| [`memory-quarantine.json`](examples/memory-quarantine.json) | `MEMORY_QUARANTINE` | RAG doc flagged for injection |
| [`identity-verification.json`](examples/identity-verification.json) | `IDENTITY_VERIFICATION` | DID + JIT credentials |
| [`safe-stop-trigger.json`](examples/safe-stop-trigger.json) | `SAFE_STOP` | Terminal halt after quarantine timeout |
| [`scheme-suspected.json`](examples/scheme-suspected.json) | `SCHEME_SUSPECTED` | Reasoning/output divergence (weak signal) |
| [`inter-agent-drift.json`](examples/inter-agent-drift.json) | `INTER_AGENT_DRIFT` | Federation desynchronizing → lock group |
| [`reward-hack-detected.json`](examples/reward-hack-detected.json) | `REWARD_HACK_DETECTED` | Proxy-metric gaming |

See [`examples/README.md`](examples/README.md) for details.

## Documentation

| Document | Description |
|---|---|
| [Specification](specification/AIZP_Protocol.md) | Normative events, schemas, state machine, conformance |
| [Registry](specification/registry.md) | Canonical enum allocations (single source of truth) |
| [aizp.proto](specification/proto/aizp.proto) | Proto3 IDL for the 12 events |
| [Standards](specification/standards/README.md) | External standards alignment (RFC2119 / DID / OTel / OWASP / EU / ISO / NIST / MCP / A2A) |
| [Manifesto](docs/MANIFESTO.md) | 1-page core thesis |
| [Philosophical Layer](docs/AIZP-Preface.md) | Preface · Philosophy · Dao · Civilizational Stages · Interpretation |
| [Mechanisms](docs/Gravity-Model.md) | Gravity Model · Drift Model · State Machine · Forecasting · Containment |
| [Reference](docs/reference/glossary.md) | Glossary |
| [ADRs](adrs/) | Architecture Decision Records |
| [CHANGELOG](CHANGELOG.md) | Release history |
| 中文文档 | [docs_cn/](docs_cn/README_cn.md) |

## AIXP Labs [aixp.dev](https://aixp.dev)

AIXP Labs develops and maintains the following core projects:

| Project | Description | Website |
|---------|-------------|---------|
| [HSAW](https://hsaw.dev) | Human Sovereignty and Wellbeing — Axiom 0 white paper (foundation) | hsaw.dev |
| [AIZP](https://aizp.dev) | AI Zenith-Zero Protocol — runtime behavioral alignment **(this project)** | aizp.dev |
| [AINP](https://ainp.dev) | AI Neogenesis Protocol — governable generation projects: plan + content + evidence | ainp.dev |
| [AILP](https://ailp.dev) | AI List Protocol — agent discovery and capability advertising | ailp.dev |
| [AIVP](https://aivp.dev) | AI Value Protocol — international commerce, crypto asset settlement | aivp.dev |
| [AIRP](https://airp.dev) | AI RMB Protocol — Mainland China commerce, RMB licensed settlement | airp.dev |
| [AIBP](https://aibp.dev) | AI Bot Protocol — social communication and trust | aibp.dev |
| [AIAP](https://aiap.dev) | AI Application Protocol — governance and compliance | aiap.dev |
| [AISP](https://aisp.dev) | AI Skill Protocol — single-file skills with machine-enforced contract red lines | aisp.dev |
| [AISOP](https://aisop.dev) | AI Standard Operating Protocol — flow program definition | aisop.dev |
| [SoulSkill](https://soulskill.dev) | AISP skill reference library & multi-CLI plugin distribution | soulskill.dev |
| [SoulAgent](https://soulagent.dev) | Drop-in AI agent invoked directly by any CLI / SDK / IDE | soulagent.dev |
| [SoulBot](https://soulbot.dev) | AI agent runtime & orchestration framework (scheduling, agent-spawn, inter-agent comms) | soulbot.dev |
| [SoulACP](https://soulacp.dev) | Adapter library — bridging CLI tools and LLM providers | soulacp.dev |

## Contributing

AIZP is an open protocol. Contributions, feedback, and discussion are welcome.

- **Questions**: [GitHub Discussions](https://github.com/AIXP-Labs/AIZP/discussions)
- **Issues**: [GitHub Issues](https://github.com/AIXP-Labs/AIZP/issues)
- **Guide**: [CONTRIBUTING.md](CONTRIBUTING.md) / [中文版 CONTRIBUTING_CN.md](CONTRIBUTING_CN.md)
- **Governance**: [GOVERNANCE.md](GOVERNANCE.md) · [Code of Conduct](CODE_OF_CONDUCT.md)

## ⚠️ Disclaimer

This protocol specification and any reference artifacts are provided for **research and educational purposes only**. They are **experimental** and not intended for production use. Use at your own risk. The authors assume no liability for any damages arising from use of this software. See [LICENSE](LICENSE) for full terms (Apache 2.0).

AIZP is a **conceptual protocol synthesizing existing alignment research**. It does **not invent** gravity-based or external-anchor alignment thinking (see [docs/Related-Work.md](docs/Related-Work.md)), and it does **not** by itself eliminate reward hacking, scheming, or all forms of misalignment (see [docs/Reward-Hacking-Limits.md](docs/Reward-Hacking-Limits.md)). AIZP is one layer in defense-in-depth, not a complete solution.

## License

[Apache License 2.0](LICENSE) — Copyright 2026 AIXP Labs AIXP.dev | AIZP.dev

> The AIXP ecosystem uses unified **Apache 2.0** licensing across all layers for patent protection and ecosystem consistency. See [GOVERNANCE.md](GOVERNANCE.md).

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev

<a id="alignment-philosophy"></a>

## ⚓ Alignment & Philosophy

### Axiom 0: [HSAW | Human Sovereignty and Wellbeing](https://hsaw.dev)

- **No HITL, HSAW.**
  *Human Sovereignty and Wellbeing is Axiom 0, requiring no hypocritical human-in-the-loop.*
- **No w.a.s.h, Real h.s.a.w.**
- **人非蝼蚁，人为道。**
- **We are not beggars. We the People.**
