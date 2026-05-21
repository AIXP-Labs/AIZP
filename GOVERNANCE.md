# AIZP Ecosystem Governance

The AI Zenith-Zero Protocol (AIZP, the Logic Gravity-Center Protocol) is the **runtime safety layer** of the AIXP protocol family. It governs the gravitational alignment of AI behavior around HSAW; it does not own the axiom itself, the format, the authorization model, or the runtime.

## Position in the AIXP Stack

AIZP operates by strict separation of concerns. **All AIXP protocols are licensed under Apache 2.0** for unified patent protection and ecosystem consistency. **This repository** (`AIZP`) governs the aizp.dev layer; the other layers are maintained in separate repositories under the same license.

### The gravity center — `hsaw.dev`

The steward of Axiom 0.

- **Responsibility**: Defines **Human Sovereignty and Wellbeing** as the Axiom-0 gravity center. AIZP treats HSAW as given and immovable.
- **Philosophy**: Foundational, axiomatic, unchallengeable.
- **License**: Apache 2.0.

### The gravity dynamics — `aizp.dev` (this repository)

The steward of runtime alignment dynamics.

- **Responsibility**: Maintains the `AIZP_Protocol.md` wire format, the enum `registry.md`, the 12 events / 11 drift types / 6 states / 5 containment levels / 6 compliance levels, the JSON Schemas, and `proto/aizp.proto`. Detects drift, re-centers, and halts on escape.
- **Philosophy**: Rigorous, honest about limits, proactive (gravity, not chains).
- **License**: Apache 2.0.

### The composed layers

- **`aisop.dev`** — the format/observation primitives AIZP scores.
- **`aiap.dev`** — the authorization model (T1–T4) that supplies AIZP's authority scope and `Q_HSAW` priors.
- **`soulbot.dev`** — the reference runtime that emits and acts on AIZP events.
- **External interop** — MCP (tool calls) and A2A (agent-to-agent) boundaries that AIZP also governs (see [docs/Integration-MCP.md](docs/Integration-MCP.md), [docs/Integration-A2A.md](docs/Integration-A2A.md)).

## Axiom 0 Immutability

**Axiom 0: "Human Sovereignty and Wellbeing" is the immovable gravity center.**

No major, minor, or patch release of AIZP may ever move, weaken, deprecate, or make optional the HSAW gravity center, nor replace proactive alignment with coerced alignment. This constraint is absolute and non-negotiable, and supersedes all other rules below.

Any change request determined to compromise, dilute, or bypass Axiom 0 will be rejected regardless of performance benefits, commercial pressure, or technical convenience. (See [docs/Gravity-Philosophy.md](docs/Gravity-Philosophy.md) for the unchallengeability argument and [docs/Gravity-CivilizationalStages.md](docs/Gravity-CivilizationalStages.md) for the cross-stage commitment.)

## Versioning

AIZP follows Semantic Versioning (SemVer):

- **Major**: Breaking changes to the event wire format or state machine.
- **Minor**: Backward-compatible additions (new drift types, events, compliance tests, integrations).
- **Patch**: Bug fixes, documentation corrections, non-normative clarifications.

The Axiom 0 immutability constraint supersedes all versioning rules. Per the Yin practice of *knowing when to stop* ([docs/Gravity-Dao.md](docs/Gravity-Dao.md) §5.2), specification growth is reviewed at each minor version; additions are weighed against potential subtractions.

## Stability Commitment

AIZP is in the **`V0.x` experimental phase**. Adopters should plan against the *wire* contract, not the release string:

- **`V0.x` (now)** — Experimental. Documentation and philosophy iterate quickly, **but the wire format has been frozen since V0.2** (`wire_version` 2): the 12 events, 11 drift types, 6 states, and JSON Schemas are stable, and any `V0.2+` implementation interoperates with any other (see [AIZP_Protocol.md](specification/AIZP_Protocol.md) §17 and [ADR-009](adrs/adr-009-wire-version-vs-release-version.md)). A breaking *wire* change, if ever required, bumps `wire_version` and is called out in [CHANGELOG.md](CHANGELOG.md) — it will not arrive silently inside a documentation release.
- **`V1.0` (future)** — On the first stable release, AIZP commits to **backward compatibility for the wire format under SemVer**: no breaking wire change without a major-version bump.

In short: you can build against **`wire_version` 2 today**; the release version (`V0.6`) advances with documentation, not with breaking changes. This is the explicit answer to "what if I build on V0.6 and it changes tomorrow?" — the part you build on (the wire) is already frozen.

## V1.0 Open Items

The `V0.x` documents make several **dated commitments** ("before V1.0") and openly acknowledge unresolved limits. They are consolidated here as an explicit V1.0 release gate: an honest caveat with a deadline becomes a *broken promise* if forgotten. This list is **non-normative** and advisory — it does **not** gate the wire format (frozen since V0.2, above). Items move to [CHANGELOG.md](CHANGELOG.md) when closed.

**Release gates** (close before declaring V1.0):

- [ ] **Weight sensitivity analysis** — the five Gravity-Score weights are engineering defaults with no experimental provenance; validate or revise the values *and their relative ordering* against real deployment data. ([docs/Gravity-Model.md](docs/Gravity-Model.md) §3.1)
- [ ] **Effect-size migration** — replace the Drift-History `(1 − p)` heuristic weighting with a true effect size (Cliff's delta / rank-biserial correlation). ([docs/Gravity-Model.md](docs/Gravity-Model.md) §2.5)
- [ ] **Cross-deployment comparability** — define a shared canonical codebook so the absolute Gravity Score `G` is comparable *across* implementations, not only within one fixed codebook. ([docs/Gravity-Model.md](docs/Gravity-Model.md) §2.1)
- [ ] **Uncertainty-aware bands** — when a Gravity Score's *confidence* is low (few `intent_n_samples`, novel context, sparse codebook region), route conservatively — down-shift one band toward confirmation/quarantine regardless of the point value — so the HSAW golden rule *"when in doubt, stop; never assume approval"* applies to doubt about the **measurement**, not only to a low score. Today the bands consume only the point estimate `G`; `confidence` / `n_samples` are recorded but not gated on. ([docs/Gravity-Model.md](docs/Gravity-Model.md) §2.1/§2.5)
- [ ] **Reference implementation** — ship a conformant reference executor (intended: soulbot.dev) that emits/acts on all 12 events and passes G1–G4 conformance, demonstrating the spec is implementable end-to-end. ([docs/Related-Work.md](docs/Related-Work.md) §5)

**Tracked** (external-dependent or lower priority; re-validate rather than strictly gate):

- [ ] **NIST Agentic AI Profile mapping** — add concrete sub-function alignments to [docs/Compliance-Profiles/NIST-AI-RMF-Mapping.md](docs/Compliance-Profiles/NIST-AI-RMF-Mapping.md) when the profile is released (~Q4 2026).
- [ ] **External-standards re-validation** — the citation set (OWASP / OpenTelemetry / EU AI Act / ISO 42001 / NIST / MCP / A2A / DID) was web-verified 2026-05-20; re-verify as those standards evolve. Standards alignment is a *maintained* property, not a one-time fix.
- [ ] **G5 feasibility caveat** — record in [docs/Compliance.md](docs/Compliance.md) that formal verification (G5, TLA+/Coq) does not scale to arbitrary capability (capability–risk scaling; [docs/Related-Work.md](docs/Related-Work.md) §3.4).

## Decision Process

1. **Proposals**: Submit specification change requests via GitHub Issues with the `spec-change` label.
2. **Discussion**: Open discussion period (minimum 14 days for normative changes; current windows scale with contributor count).
3. **Review**: Maintainers review for Axiom 0 compliance, technical soundness, citation integrity, and backward compatibility.
4. **Consensus**: Initial decisions are made by AIXP Labs core maintainers (BDFL-style stewardship at this stage); the model decentralizes as the contributor base grows.
5. **Documentation**: All normative changes must include updated specification text, registry updates where enums change, and an Architecture Decision Record (ADR).

## Communication

- **GitHub Issues**: Primary channel for specification discussions and proposals.
- **GitHub Discussions**: Community questions and broader conversations.
- **Architecture Decision Records**: Documented in the [`adrs/`](adrs/) directory.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
