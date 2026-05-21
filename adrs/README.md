# Architecture Decision Records (ADRs)

This directory records the significant architectural decisions of AIZP — the *why* behind the protocol's structure. Each ADR captures the context, the decision, and its consequences. ADRs are append-only: superseded decisions are marked, not deleted.

Use the [adr-template.md](adr-template.md) for new records. Per [CONTRIBUTING.md](../CONTRIBUTING.md) and [GOVERNANCE.md](../GOVERNANCE.md), significant specification changes require an ADR.

## Index

| ADR | Title | Status |
|---|---|---|
| [001](adr-001-gravity-center-metaphor.md) | Gravity-Center Is the Primary Metaphor | Accepted (V0.5; reaffirmed V0.6) |
| [002](adr-002-hsaw-axiom-0-immovable.md) | HSAW Is the Axiom-0, Immovable Gravity Center | Accepted |
| [003](adr-003-jsd-over-cosine.md) | Jensen-Shannon Divergence for Intent & Drift Metrics | Accepted (V0.2; retained V0.6) |
| [004](adr-004-q-hsaw-approximation.md) | Q_HSAW Is Axiomatic in Status but Approximated in Computation | Accepted (V0.6) |
| [005](adr-005-out-of-band-honest-limit.md) | Out-of-Band Actions Are an Honest Limit, Not a Solvable Bug | Accepted (V0.6) |
| [006](adr-006-ipi-cross-cutting-vector.md) | Indirect Prompt Injection Is a Cross-Cutting Vector, Not a 12th Drift Type | Accepted (V0.6) |
| [007](adr-007-specification-vs-docs-separation.md) | Separate Normative `specification/` from Narrative `docs/` | Accepted (V0.6) |
| [008](adr-008-defer-to-hsaw-canonical-content.md) | Defer Value Hierarchy and Cross-Protocol Patterns to HSAW | Accepted (V0.6) |
| [009](adr-009-wire-version-vs-release-version.md) | Decouple the Wire-Format Version from the Release Version | Accepted (V0.6) |

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
