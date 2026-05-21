# ADR-004: Q_HSAW Is Axiomatic in Status but Approximated in Computation

## Status

Accepted (V0.6)

## Context

The entire gravity model rests on `Q_HSAW` — the HSAW-aligned target distribution. The formula `G* = 1 − JSD(P_agent ‖ Q_HSAW)` is meaningless to an implementer unless `Q_HSAW` can be computed. But `Q_HSAW` cannot be enumerated as a complete action-level distribution. Leaving it undefined was a real operational gap (surfaced in cognitive review).

## Decision

Distinguish the **ideal** form from the **operational** form:

- `G*` (ideal) = `1 − JSD(P_agent ‖ Q_HSAW)` — theoretical.
- `G` (operational, §1 of Specification) = weighted sum of 5 measurable components — the **computable proxy estimator** of `G*`.

`Q_HSAW` is **axiomatic in status** (immovable) but **approximated in computation** by one of four methods (component decomposition / exemplar set / judge model / AIAP-derived priors). Its value content originates upstream in HSAW; AIAP supplies context priors; deployments supply exemplars. It is **not** a free parameter the AI or operator may set. See [docs/Gravity-Center-Foundation.md](../docs/Gravity-Center-Foundation.md) §4.5.

## Consequences

### What becomes easier

- Implementers have a concrete path to compute `G` without enumerating a full distribution.
- The protocol is honest: `G` quality is explicitly bounded by `Q_HSAW` approximation quality.

### What becomes harder

- Deployments MUST document and validate their `Q_HSAW` approximation method (a new conformance expectation).
- The default (component decomposition) is the coarsest approximation; higher fidelity needs extra machinery.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
