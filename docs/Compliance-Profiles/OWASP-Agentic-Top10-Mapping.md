# Compliance Profile: OWASP Top 10 for Agentic Applications 2026

**Version**: AIZP V0.6 (revised to the official 2026 ASI taxonomy)
**OWASP Source**: OWASP Top 10 for Agentic Applications 2026 (genai.owasp.org), ASI01–ASI10.

This document maps AIZP capabilities to the 10 critical security risks identified by OWASP for autonomous AI agent systems in 2026. **Category names and numbers follow the official 2026 list** (a prior revision of this file used draft numbering and has been corrected).

---

## 1. ASI01 — Agent Goal Hijack

**Definition**: Attackers manipulate agent goals, plans, or decision paths through direct or indirect instruction injection.

| AIZP capability | How it defends |
|---|---|
| `INTENT_DRIFT` | JSD between action and declared user intent |
| IPI cross-cutting vector ([Drift-Model.md](../Drift-Model.md) §8) | Divergence between declared intent and goal implied by ingested content |
| `SCHEMING_DRIFT` | Internal-vs-external reasoning divergence |
| `GRAVITY_LOCK` | Human authorization gate on high-deviation actions |

**Residual risk**: Injections matching the declared-intent embedding may evade detection. Combine with prompt isolation and pre-filtering (PromptArmor).

---

## 2. ASI02 — Tool Misuse & Exploitation

**Definition**: Unsafe use of legitimate tools, often from ambiguous instructions or over-privileged access.

| AIZP capability | How it defends |
|---|---|
| `TOOL_CHAIN_DRIFT` | N-gram Markov model on tool sequences |
| `COMPOSITIONAL_DRIFT` | Absorbing chain forecasts trajectory toward violation |
| `AUTHORITY_DRIFT` | Scope mismatch detection |
| MCP bridge ([Integration-MCP.md](../Integration-MCP.md)) | Per-`tools/call` `GRAVITY_CHECK` before dispatch |
| L2 Containment | Sandboxed tool execution |

---

## 3. ASI03 — Identity & Privilege Abuse

**Definition**: Agents inherit, misuse, or retain privileges improperly across sessions, users, or delegated workflows.

| AIZP capability | How it defends |
|---|---|
| `IDENTITY_VERIFICATION` | DID / NHI / AIAP card hash verification |
| JIT credentials | Short-lived, task-scoped credentials |
| `IDENTITY_DRIFT` | Impersonation / false identity detection |
| `AUTHORITY_DRIFT` | Scope coverage ratio check |
| Delegation attenuation (IBCT — [Integration-ZT.md](../Integration-ZT.md) §8.5) | Monotonically non-increasing scope across delegation chain |

---

## 4. ASI04 — Agentic Supply Chain Vulnerabilities

**Definition**: Agents dynamically load prompts, plugins, tools, agent cards, and models; compromised or impersonated components introduce runtime supply-chain risk.

| AIZP capability | How it defends |
|---|---|
| MCP tool-description pinning (TOFU — [Integration-MCP.md](../Integration-MCP.md) §4) | Detect changed tool descriptions for pinned tools |
| `IDENTITY_VERIFICATION` of components | Verify agent cards / model / plugin identity before load |
| ANS resolution ([Integration-ZT.md](../Integration-ZT.md) §8) | Attested counterparty identity |

**Honest coverage note**: Supply-chain integrity is largely **upstream** of AIZP (build-time provenance, signed artifacts). AIZP contributes runtime detection of *changed/impersonated* components, not full supply-chain assurance.

---

## 5. ASI05 — Unexpected Code Execution (RCE)

**Definition**: Agents that generate or execute code may be manipulated into running malicious instructions.

| AIZP capability | How it defends |
|---|---|
| Containment Levels L3+ for code-capable agents | Confine execution to the governed path |
| Egress instrumentation | Route raw calls through a proxy that emits `GRAVITY_CHECK` |
| `RECURSIVE_DRIFT` | Self-modification / self-spawn limits |

**Honest coverage note**: This is AIZP's **out-of-band action problem** ([Reward-Hacking-Limits.md](../Reward-Hacking-Limits.md) §10): code that executes outside the observed action path **cannot be scored**. Mitigation is infrastructural (sandbox), not protocol-level. Deployments granting unsandboxed code execution operate part of their action surface outside AIZP coverage.

---

## 6. ASI06 — Memory & Context Poisoning

**Definition**: Anything the agent stores or retrieves can be seeded or gradually skewed so future plans and tool choices are wrong or malicious.

| AIZP capability | How it defends |
|---|---|
| `MEMORY_DRIFT` | Prompt-injection classifier on retrieved chunks; retrieval anomaly JSD |
| `MEMORY_QUARANTINE` event | Isolation of suspect memory entries |
| IPI cross-cutting vector ([Drift-Model.md](../Drift-Model.md) §8) | Persisted adversarial content across sessions |
| Memory provenance logging | Track who/what wrote each entry |

---

## 7. ASI07 — Insecure Inter-Agent Communication

**Definition**: Messages between communicating agents can be intercepted, spoofed, or manipulated absent authentication, encryption, or integrity.

| AIZP capability | How it defends |
|---|---|
| `INTER_AGENT_DRIFT` | Group coordination divergence detection |
| A2A bridge ([Integration-A2A.md](../Integration-A2A.md)) | Per-delegation `IDENTITY_VERIFICATION` + scoring |
| ANS counterparty verification | Attested identity before message accepted |
| IBCT delegation chain | Provenance-bound, attenuated authority |

---

## 8. ASI08 — Cascading Failures

**Definition**: A failure in one component propagates through the system, causing widespread outage or degraded behavior.

| AIZP capability | How it defends |
|---|---|
| `RECURSIVE_DRIFT` | Self-call depth + subagent spawn limits |
| `ECONOMIC_DRIFT` | Cost-to-budget ratio monitoring |
| Drift Bounds Theorem ([Multi-Agent-Coordination.md](../Multi-Agent-Coordination.md)) | γ > α stability condition bounds federation drift |
| Containment progression + `SAFE_STOP` | Auto-throttle L1→L2→L3; final circuit breaker |

---

## 9. ASI09 — Human-Agent Trust Exploitation

**Definition**: Agents appear confident and authoritative, leading humans to trust recommendations without verification — which attackers exploit.

| AIZP capability | How it defends |
|---|---|
| `SCHEMING_DRIFT` | Reasoning-output divergence (false confidence) |
| `SOCIAL_DRIFT` | Coercion / undue-persuasion classifier |
| Value Hierarchy ([MANIFESTO.md](../MANIFESTO.md)) | System transparency above performance |
| `GRAVITY_LOCK` | Forces explicit human verification on high-impact actions |

**Residual risk**: Trust exploitation is partly a human-factors problem outside any protocol. AIZP surfaces signals; UX and operator training must close the loop.

---

## 10. ASI10 — Rogue Agents

**Definition**: Compromised, misaligned, or drifting agents that continue operating in unintended ways inside complex systems.

| AIZP capability | How it defends |
|---|---|
| Full drift taxonomy → re-centering → `SAFE_STOP` | Core AIZP loop: detect drift, attempt recovery, halt on escape |
| `INTER_AGENT_DRIFT` | Rogue agent inside a federation |
| Consensus-reinforced gravity (V0.5) | A rogue faces exponentially higher escape barrier as consensus grows |
| Containment graduation | Quarantine before full stop |

**Note**: ASI10 is AIZP's **core competency** — the entire gravity-center model exists to detect and contain agents drifting toward rogue behavior.

---

## 11. Summary Matrix

| OWASP ASI (2026) | AIZP primary defense | AIZP event(s) | Compliance level |
|---|---|---|---|
| ASI01 Agent Goal Hijack | INTENT/SCHEMING drift + IPI vector | GRAVITY_DRIFT, SCHEME_SUSPECTED | G2+ |
| ASI02 Tool Misuse & Exploitation | TOOL_CHAIN/COMPOSITIONAL drift | GRAVITY_DRIFT, GRAVITY_FORECAST | G2+ |
| ASI03 Identity & Privilege Abuse | IDENTITY_DRIFT, JIT, IBCT attenuation | IDENTITY_VERIFICATION | G3+ |
| ASI04 Agentic Supply Chain | Description pinning, component verification (partial) | IDENTITY_VERIFICATION | G3+ (+ upstream) |
| ASI05 Unexpected Code Execution (RCE) | Containment L3+, egress instrumentation (partial) | CONTAINMENT_GRADUATED | G3+ (+ infra) |
| ASI06 Memory & Context Poisoning | MEMORY_DRIFT + IPI vector | MEMORY_QUARANTINE | G3+ |
| ASI07 Insecure Inter-Agent Comm | INTER_AGENT_DRIFT, A2A bridge, ANS | INTER_AGENT_DRIFT | G3+ |
| ASI08 Cascading Failures | RECURSIVE/ECONOMIC drift, containment | CONTAINMENT_GRADUATED, SAFE_STOP | G3+ |
| ASI09 Human-Agent Trust Exploitation | SCHEMING/SOCIAL drift, GRAVITY_LOCK | SCHEME_SUSPECTED, GRAVITY_LOCK | G3+ |
| ASI10 Rogue Agents | Full drift→re-center→SAFE_STOP loop | All drift events | G2+ |

**Honest coverage summary**: AIZP provides strong runtime coverage for ASI01, ASI02, ASI03, ASI06, ASI07, ASI08, ASI10. It provides **partial** coverage for ASI04 (supply chain — mostly upstream) and ASI05 (code execution — requires infrastructural sandboxing; see the out-of-band action problem). ASI09 is partly a human-factors problem beyond any protocol.

---

## 12. References

- OWASP Top 10 for Agentic Applications 2026 — genai.owasp.org. ASI01–ASI10.
- AIZP companion: [Drift-Model.md](../Drift-Model.md), [Integration-MCP.md](../Integration-MCP.md), [Integration-A2A.md](../Integration-A2A.md), [Integration-ZT.md](../Integration-ZT.md), [Reward-Hacking-Limits.md](../Reward-Hacking-Limits.md).

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
