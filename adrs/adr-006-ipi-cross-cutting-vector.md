# ADR-006: Indirect Prompt Injection Is a Cross-Cutting Vector, Not a 12th Drift Type

## Status

Accepted (V0.6)

## Context

Indirect prompt injection (IPI) is the dominant agentic attack vector of 2026 (≈55–60% of attacks; OWASP ASI01 basis). It was tempting to add `INJECTION_DRIFT` as a 12th drift type. But "11 drift types" is deeply embedded across ~40 locations, and — more importantly — IPI describes *how* misalignment is delivered, not *what kind* of misalignment results. The drift taxonomy answers "what kind"; IPI is orthogonal to it.

(An earlier draft did reference a fictional `INJECTION_DRIFT`; this was caught in review and removed — see also the prohibition on citing non-existent identifiers.)

## Decision

Model IPI as a **cross-cutting attack vector** ([docs/Drift-Model.md](../docs/Drift-Model.md) §8), not a numbered drift type. IPI is *delivered* via retrieved content / tool descriptions / tool results / memory / inter-agent messages, and *manifests* as existing drift types (Intent, Memory, Social, Tool-Chain). The drift-type count stays at 11.

## Consequences

### What becomes easier

- Conceptually correct: vector (how) vs. taxonomy (what) are kept distinct.
- No disruptive renumbering of the 11 drift types or schemas.
- A single §8 covers delivery channels, detection signal, defenses (PromptArmor), and benchmarks (AgentDojo, InjecAgent).

### What becomes harder

- Readers expecting a named `INJECTION_DRIFT` must learn it is handled via the vector + existing types.
- IPI detection logic is spread across Memory/Intent/Social drift rather than localized in one type.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
