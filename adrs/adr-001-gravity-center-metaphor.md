# ADR-001: Gravity-Center Is the Primary Metaphor

## Status

Accepted (V0.5; reaffirmed V0.6)

## Context

AIZP needs one organizing metaphor for "AI behavior staying aligned to HSAW". The metaphor shapes how engineers reason about the protocol before they read the equations. Earlier versions tried two framings, both of which collided with existing 2025–2026 literature:

- **V0.3 "Entropy collapses into HSAW"** — the information-theoretic collapse framing was already occupied by adjacent alignment work; retained only as the JSD distance idea.
- **V0.4 "AI resonates with HSAW's zero-entropy center"** — resonance/coherence framings were already in use (Della Terra's "From Reward to Resonance" Nov 2025; Kuramoto-for-AI synchronization, arxiv 2508.12314, Mitra Aug 2025; Frontiers 2022).

A primary metaphor was needed that is structurally honest, positionally distinct, operationally tractable, and respects AI agency.

## Decision

Adopt **gravity** as the primary metaphor: *HSAW is the Axiom-0 gravity center; AI proactively aligns to this center.* Drift = orbital deviation; re-centering = orbital correction; escape velocity = decoupling = halt.

Entropy collapse (V0.3) and resonance (V0.4) are **retained as sub-theories** describing specific phenomena within the gravity framework, not as the primary framing.

## Consequences

### What becomes easier

- Orbital-mechanics intuition maps cleanly to drift dynamics (attractive force, stable orbit, escape velocity).
- The metaphor is honest: gravity is a real attractor, not a coercive chain — supporting proactive (not coerced) alignment.
- Positionally distinct from the crowded entropy/resonance literature.

### What becomes harder

- Multi-body intuition needed a refinement (resolved in [ADR-002](adr-002-hsaw-axiom-0-immovable.md) / V0.5 consensus-reinforced gravity: many bodies share one barycenter, gravity ∝ N²).
- Sub-theories (entropy, resonance) must be maintained as compatible lenses, adding documentation surface.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
