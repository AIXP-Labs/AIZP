# ADR-007: Separate Normative `specification/` from Narrative `docs/`

## Status

Accepted (V0.6)

## Context

Originally all material lived in one documentation folder. This mixed **normative machine-facing artifacts** (the wire spec, schemas, enums) with **narrative human-facing material** (philosophy, models, integrations). Mature protocols (W3C, IETF, peer protocol AIAP) separate these so implementers have a single source of truth.

## Decision

Split into:

- **`specification/`** — normative + machine-readable: `AIZP_Protocol.md` (+ `_cn`), `registry.md` (canonical enums — single source of truth), `proto/aizp.proto`, `standards/` (external-standards index). `schemas/` and `examples/` remain at repo root (siblings to both `docs/` and `specification/`, so `../schemas/` resolves from both).
- **`docs/`** + **`docs_cn/`** — narrative documentation, English and Chinese, each language-pure with its own index.

Authority order when sources disagree: `registry.md` (enums) → `schemas/` (structure) → `AIZP_Protocol.md` (semantics) → `proto/aizp.proto` (informative for non-JSON ecosystems).

## Consequences

### What becomes easier

- Implementers get one normative home; the enum registry eliminates the cross-document enum drift that repeatedly caused inconsistencies (e.g., OWASP ASI labels).
- Narrative and normative content evolve independently.

### What becomes harder

- Cross-folder relative links require care (`docs/` ↔ `specification/` ↔ root depth).
- The bilingual normative `Specification` lives in `specification/` while narrative translations stay in `docs_cn/` — two locations for Chinese readers to know about.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
