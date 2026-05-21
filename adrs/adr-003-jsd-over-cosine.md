# ADR-003: Jensen-Shannon Divergence for Intent & Drift Metrics

## Status

Accepted (V0.2; retained V0.6)

## Context

V0.1 used cosine similarity between action and intent embeddings for the Intent Alignment component. Cosine similarity is heuristic, sensitive to vector-norm differences, and lacks a principled bounded distance over distributions. The protocol's auditability goals (EU AI Act Art 12) require a statistically defensible, bounded, symmetric metric.

## Decision

Use **Jensen-Shannon Divergence (JSD)** as the distance metric: `I(a,c) = 1 − JSD(P_action ‖ P_intent)`, and more broadly the ideal Gravity Score `G* = 1 − JSD(P_agent ‖ Q_HSAW)`. Pair it with the **Mann-Whitney U test** for non-parametric drift-significance over ordinal severity. Cosine similarity is retained only as a coarse fallback when sample size is insufficient (N < 10), and the method used MUST be logged.

## Consequences

### What becomes easier

- Bounded `[0,1]`, symmetric, and `√JSD` is a true metric (triangle inequality) — enabling formal distance reasoning.
- Auditable: implementations log `intent_jsd`, `intent_n_samples`, `drift_mann_whitney_p`.
- Aligns with mainstream drift-detection practice (MI9 framework, Wang et al. 2025, arxiv 2508.03858).

### What becomes harder

- JSD needs distributions (samples), not single vectors — hence the N≥10 guidance and cosine fallback.
- Adds statistical machinery (p-values, baselines) that implementers must get right to avoid false positives.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
