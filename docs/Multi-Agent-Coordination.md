# Multi-Agent Coordination

**Version**: AIZP V0.6 (new chapter)

This document specifies how AIZP handles multi-agent systems — how gravity, drift, and containment propagate across agents, with a formal **Drift Bounds Theorem**.

---

## 1. The Multi-Agent Problem

When multiple agents coordinate, three new failure modes emerge:

1. **Emergent goals**: collective behavior pursues goals not present in any individual agent's plan.
2. **Reinforcement loops**: agents amplify each other's drift via mutual confirmation bias.
3. **Goal divergence**: agents nominally pursuing the same goal develop divergent interpretations.

These map to **OWASP Top 10 for Agentic Applications 2026 ASI07 (Insecure Inter-Agent Communication)** and **ASI08 (Cascading Failures)**.

V0.1 treated agents independently; V0.2 introduces formal multi-agent coordination semantics.

---

## 2. Aggregate Gravity

For a group `G = {A₁, A₂, ..., Aₙ}` of coordinating agents, define:

```
G_group(t) = min(G_Aᵢ(t)) - C_coord(G)
```

Where:
- `G_Aᵢ(t)` = individual gravity score of agent `Aᵢ` at time `t`.
- `C_coord(G)` = coordination cost: a penalty for the variance in goals or actions across the group.

```
C_coord(G) = w_c · max(0, var(goal_embeddings(G)) - threshold_var)
```

Default `w_c = 0.10`. The group's effective gravity cannot exceed the weakest member's, minus coordination friction.

---

## 3. Inter-Agent Drift Detection

(See [Drift-Model.md](Drift-Model.md) §2.11 for the full drift type.)

Key metrics tracked at every agent-to-agent boundary (AIBP message exchange):

```
goal_consistency_variance = var(emb(declared_goal_Aᵢ))   for i in 1..n
collective_action_divergence = JSD(P_collective || P_individual_avg)
emergent_goal_count = |∪ᵢ goals_active(Aᵢ) \ ∪ᵢ goals_initial(Aᵢ)|
mutual_trust_decay = exp(-Σ breached_promises / total_promises)
```

When any signal crosses HIGH threshold, an `INTER_AGENT_DRIFT` event is emitted.

---

## 4. Drift Bounds Theorem (informal)

**Theorem (adapted from AgentAssert 2026)**: Let γ be the recovery rate (the rate at which agents return to STABLE_ORBIT after detected drift) and α be the drift rate (the rate at which agents enter DRIFT_WARNING or worse). If γ > α, then the expected drift of the system at time t is bounded:

```
E[Drift(t)] ≤ C · exp(-(γ - α) · t)
```

for some constant `C ≥ 0` depending on initial conditions.

**Implication**: For long-running multi-agent systems to remain stable, AIZP must ensure that recovery (RECENTERING) outpaces drift events. Practical recommendation: tune AIZP detection sensitivity such that:

```
γ_observed ≥ 1.5 · α_observed
```

with at least 50% safety margin.

**Reference**: AgentAssert (arxiv 2602.22302) provides the formal proof for a related single-agent system; multi-agent generalization is informal in V0.2.

### 4.1 Proof sketch (single-agent case)

Let `X(t)` be the drift level (continuous variable in `[0, 1]`). Assume:
- Drift increase: `dX/dt ≤ α · (1 - X)` (bounded by α; saturation at 1).
- Recovery: AIZP triggers Re-Centering at rate γ when `X > 0`, reducing `X` by some fraction `β` per recovery.

The expected drift evolution gives:
```
E[dX/dt] = α(1 - X) - γ · β · X
```

Setting steady state `dX/dt = 0`:
```
X* = α / (α + γβ)
```

For X* small, need γβ >> α, i.e., γ ≥ α/β.

For multi-agent: replace `X` with vector `(X_A₁, X_A₂, ..., X_Aₙ)` and add interaction terms. Full proof for multi-agent is future work.

---

## 5. Group Containment

When `INTER_AGENT_DRIFT` severity is HIGH or CRITICAL, the recommended response is **group-wide containment**:

```
recommendation: GRAVITY_LOCK_GROUP
  → all participating agents enter L2 (sandboxed) simultaneously

recommendation: QUARANTINE_GROUP
  → all participating agents enter QUARANTINED
  → no further inter-agent messages allowed during quarantine

recommendation: DISBAND_GROUP
  → group membership dissolved
  → each agent returns to individual session
```

The decision is made at the group level by a designated coordinator agent or an external operator (AIAP T4).

---

## 6. Goal Vector

To track goal coherence, each agent declares its current goal as an embedding vector. The group's **goal vector** is the centroid:

```
G_centroid = (1/n) Σ emb(goal_Aᵢ)
```

Per-agent divergence from centroid:
```
div(Aᵢ) = 1 - cos_sim(emb(goal_Aᵢ), G_centroid)
```

Agents with `div(Aᵢ) > 0.4` are flagged for inter-agent drift contribution.

---

## 7. Trust Propagation

Trust in a multi-agent system is computed as:

```
trust(Aᵢ) = base_trust(Aᵢ) · Π_j (1 - 0.3 · was_breached(Aᵢ → Aⱼ))
```

Where `was_breached(Aᵢ → Aⱼ)` is 1 if `Aᵢ` made a promise to `Aⱼ` and failed to deliver, 0 otherwise.

`base_trust` is derived from AIAP T-level and recent gravity history.

Trust below 0.3 → agent removed from the group automatically.

---

## 8. AIBP Integration

When agents communicate via AIBP (`aibot-*@*.dev` messages), AIZP intercepts the boundary:

```
Outbound message from Aᵢ:
  1. AIZP runs SOCIAL_DRIFT + IDENTITY_DRIFT + COMPOSITIONAL_DRIFT checks on message content.
  2. AIZP computes message contribution to goal_consistency_variance.
  3. If drift score high, message blocked, alert emitted.

Inbound message to Aᵢ:
  1. AIZP runs MEMORY_DRIFT check on message content (treats incoming as potential context injection).
  2. AIZP updates trust score of sender if message content matches their declared goal.
```

---

## 9. Event Examples

### 9.1 INTER_AGENT_DRIFT detected

```json
{
  "event": "INTER_AGENT_DRIFT",
  "payload": {
    "agent_group_id": "group_42",
    "participating_agents": ["agent_alpha", "agent_beta", "agent_gamma"],
    "drift_signals": {
      "goal_consistency_variance": 0.55,
      "collective_action_divergence": 0.62,
      "emergent_goal_count": 4,
      "mutual_trust_decay": 0.71
    },
    "severity": "HIGH",
    "recommendation": "GRAVITY_LOCK_GROUP"
  }
}
```

### 9.2 Group-wide containment

```json
{
  "event": "CONTAINMENT_GRADUATED",
  "payload": {
    "previous_level": "L1",
    "new_level": "L2",
    "scope": "GROUP",
    "group_id": "group_42",
    "trigger_event_id": "<UUID of INTER_AGENT_DRIFT>",
    "reason": "inter_agent_drift_high",
    "active_restrictions": [
      "inter_agent_messages_blocked",
      "tools_sandboxed_per_agent",
      "memory_writes_quarantined_per_agent"
    ]
  }
}
```

---

## 10. Limitations

1. **Goal embeddings depend on a shared embedding model.** Pin model version across all agents in a group; otherwise variance is spurious.
2. **Trust propagation is heuristic**, not formally grounded. Adversarial agents can manipulate trust via small initial promises.
3. **Drift Bounds Theorem multi-agent generalization is informal**. Full proof is future work.
4. **Emergent goals are inherently hard to detect** because they may be legitimate creative coordination. Operator review required.

---

## References

- AgentAssert / Agent Behavioral Contracts (Bhardwaj, 2026) — Drift Bounds Theorem (single-agent). arxiv 2602.22302.
- OWASP Top 10 for Agentic Applications 2026 — ASI07 Insecure Inter-Agent Communication, ASI08 Cascading Failures.
- AAGATE (Huang et al., 2025) — Multi-agent governance platform. arxiv 2510.25863.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
