# ADR-005: Out-of-Band Actions Are an Honest Limit, Not a Solvable Bug

## Status

Accepted (V0.6)

## Context

AIZP scores actions that pass through its observation path (`GRAVITY_CHECK` before dispatch). But an agent with code-execution capability can spawn subprocesses, issue raw API calls, or modify its own execution context — actions the scoring layer never sees. Kaptein et al. ("Runtime Governance for AI Agents: Policies on Paths", arxiv 2603.16586) state that enforced compliance is an architectural constraint on agent capabilities, not a proven invariant of the governance system.

A protocol could pretend to cover this; doing so would be dishonest and brittle.

## Decision

Document the **out-of-band action problem** as a first-class honest limit ([docs/Reward-Hacking-Limits.md](../docs/Reward-Hacking-Limits.md) §10): *AIZP governs the observed action path; it cannot govern what bypasses that path.* Mitigation is **infrastructural, not protocol-level** — sandbox/deny code execution (Containment L3+), instrument egress so raw calls become observable. Maps to OWASP **ASI05 Unexpected Code Execution (RCE)** with explicitly *partial* coverage.

## Consequences

### What becomes easier

- Honest positioning: deployers know exactly what AIZP does and does not cover, and document residual exposure.
- Clear division of responsibility (protocol vs. infrastructure).

### What becomes harder

- AIZP cannot claim end-to-end coverage; high-assurance deployments must add sandboxing they own.
- ASI05 is marked "partial", which a naive compliance reader might see as a weakness rather than honesty.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
