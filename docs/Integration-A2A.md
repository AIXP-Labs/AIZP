# Integration: Agent-to-Agent (A2A)

**Version**: AIZP V0.6 (new chapter — connects AIZP to the agent coordination ecosystem)

In 2026 the agent **coordination** layer — how agents discover each other and exchange tasks across boundaries — has consolidated around **A2A** (originally Google's Agent-to-Agent protocol; IBM's ACP merged into A2A under the Linux Foundation). A2A defines *how* agent A delegates to agent B; it does **not** verify A's authority or constrain B's scope, and it does not detect collective drift across a federation. That is where AIZP applies.

> A2A says: "here is how agent A hands a task to agent B."
> AIZP says: "this delegation, and the federation's collective trajectory, has Gravity Score G."

---

## 1. Why this integration matters

A2A `AgentCard`s carry **self-declared** identities with no attestation binding. When agent A delegates to agent B, A2A provides no mechanism to verify A's authority or to attenuate B's scope. The risks map directly to OWASP ASI (2026):

- **ASI01 Agent Goal Hijack** — a delegated task carries a hijacked goal.
- **Cross-agent propagation** — a compromised agent spreads misalignment through the federation (the "progressive breach" chain: compromised intent → operational power → cross-agent propagation → cascading failures).
- **ASI10 Rogue Agents** — a drifting agent keeps operating inside the system.

**Relationship to AIBP.** AIBP is the AIXP-native inter-agent protocol (`aibot-*@domain.dev`); A2A is the external cross-vendor interop standard. They are not competitors: AIZP applies the **same** `INTER_AGENT_DRIFT` machinery to both boundaries — AIBP for intra-stack agents, A2A for agents outside the AIXP stack. Where this document says "A2A delegation", the identical scoring applies to an AIBP message; only the transport differs. See [Integration-AIXP.md](Integration-AIXP.md) §7.3.

---

## 2. Layering

```
A2A    — TRANSPORTS the delegation (AgentCard discovery, task send/receive).
          ▼
AIZP   — SCORES the delegation and monitors the federation:
          INTER_AGENT_DRIFT, IDENTITY_VERIFICATION, Kuramoto coordination.
          ▼
AIP/ZT — VERIFIES identity & attenuates authority across the delegation chain.
```

---

## 3. The Bridge: A2A delegation → `INTER_AGENT_DRIFT` + `IDENTITY_VERIFICATION`

When agent A sends an A2A task to agent B, the runtime MUST:

1. Verify B's identity and A's authority to delegate (see [Integration-ZT.md](Integration-ZT.md) §on delegation chains).
2. Emit `IDENTITY_VERIFICATION` for the A→B hop.
3. Score the delegated task as an action under B's authority envelope (`A(a,c)` from B's granted scope, not A's).
4. Track the **collective** behavior of the federation via the multi-agent coordination term (see [Multi-Agent-Coordination.md](Multi-Agent-Coordination.md)).
5. If the federation's order parameter degrades (agents desynchronizing from HSAW), emit `INTER_AGENT_DRIFT`.

### 3.1 Field mapping

| A2A field | AIZP usage |
|---|---|
| `AgentCard.name` / `url` | identity claim → `IDENTITY_VERIFICATION` (requires attestation, not self-declaration) |
| delegated `Task` / `Message` | action `a` scored under recipient's authority scope |
| `Task` provenance chain | delegation chain → authority attenuation check |
| federation membership | nodes in the Kuramoto coordination model |

---

## 4. Scope attenuation across delegation

A core A2A gap is unconstrained delegation. AIZP's rule: **delegated authority is monotonically non-increasing.** Agent B's effective authority scope is the *intersection* of B's granted scope and the (attenuated) scope A is permitted to delegate:

```
granted_scope(B | via A) ⊆ delegatable_scope(A) ⊆ granted_scope(A)
```

Any action by B requiring scope beyond this intersection raises `AUTHORITY_DRIFT`. This is the conceptual companion to Invocation-Bound Capability Tokens (see [Integration-ZT.md](Integration-ZT.md)).

---

## 5. Collective drift (the federation as an orbital system)

A single aligned agent is not enough if the federation collectively drifts. AIZP models the multi-agent federation as coupled orbital bodies around HSAW (Kuramoto coupling — see [Multi-Agent-Coordination.md](Multi-Agent-Coordination.md)). Per the consensus-reinforced gravity principle (V0.5 refinement), more agents in HSAW consensus *strengthen* the center; conversely, a cluster desynchronizing is an early `INTER_AGENT_DRIFT` signal before any single agent crosses its own escape threshold.

---

## 6. What AIZP does NOT take over

- AIZP does not transport A2A messages or implement AgentCard discovery.
- AIZP does not issue identity tokens (AIP/IBCT + Zero Trust do — see [Integration-ZT.md](Integration-ZT.md)).
- AIZP scores delegations and monitors collective trajectory; it does not replace the coordination protocol.

---

## References

- A2A / Agent-to-Agent Protocol (Linux Foundation project since 2025-06; ACP merge announced 2025-09).
- OWASP Top 10 for Agentic Applications (2026) — ASI01 Goal Hijack, ASI10 Rogue Agents.
- AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A. arxiv 2603.24775.
- AIZP companion: [Integration-MCP.md](Integration-MCP.md), [Integration-ZT.md](Integration-ZT.md), [Multi-Agent-Coordination.md](Multi-Agent-Coordination.md).

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
