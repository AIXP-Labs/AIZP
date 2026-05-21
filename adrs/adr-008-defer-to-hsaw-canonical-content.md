# ADR-008: Defer Value Hierarchy and Cross-Protocol Patterns to HSAW

## Status

Accepted (V0.6)

## Context

AIZP declares HSAW as its Axiom-0 gravity center, but earlier V0.6 drafts diverged from HSAW's canonical content in two ways:

1. **Value Hierarchy.** AIZP's MANIFESTO invented its own 5-level hierarchy (Sovereignty / Wellbeing / Transparency / Performance / Aesthetic). This **contradicted** HSAW §3.5's canonical 7-level hierarchy — most notably it **omitted Privacy** (HSAW's #2, with the explicit rule "Privacy overrides Transparency") and added a non-HSAW "Aesthetic" level.

2. **`NO_SELF_MODIFY`.** A review flagged `NO_SELF_MODIFY` in AIZP's Interpretation document as a "fictional identifier" and replaced it — but `NO_SELF_MODIFY` is in fact **HSAW §6.5 Pattern 5** (and AIAP's convergent Axiom-0 statement). The review erred by checking only AIZP's own specs, not HSAW's. (Note: this is distinct from `INJECTION_DRIFT`, which *was* genuinely fictional — see ADR-006.)

## Decision

**AIZP does not redefine content that HSAW, as the Axiom-0 steward, already defines. It defers and attributes.**

- The **Value Hierarchy** is inherited verbatim from HSAW §3.5 (7 levels, Privacy at #2, Privacy-overrides-Transparency). AIZP's MANIFESTO points to HSAW rather than asserting its own.
- **`NO_SELF_MODIFY`** is referenced as **HSAW Pattern 5**, enforced at the AIZP layer via `RECURSIVE_DRIFT` + `GRAVITY_LOCK` — not erased.
- More broadly: where HSAW defines a canonical artifact (value hierarchy, consequential-action scope, design patterns, compliance dimensions), AIZP composes with and cites it rather than inventing a parallel version.

## Consequences

### What becomes easier

- Genuine alignment: AIZP cannot drift from its own declared axiom by quietly redefining HSAW's content.
- Privacy is restored as a first-class value (HSAW #2), including the privacy-overrides-transparency rule for AIZP's observability.
- Cross-protocol patterns (HSAW patterns, AIAP authorization) are attributed correctly, strengthening the AIXP-stack story.

### What becomes harder

- AIZP must track HSAW revisions; if HSAW changes its hierarchy or patterns, AIZP's references must follow.
- Reviewers must check cross-protocol sources (HSAW, AIAP), not just AIZP's own specs, before flagging an identifier as fictional.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
