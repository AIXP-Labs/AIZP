# AIZP Threat Model

**Version**: AIZP V0.6

This document enumerates the threats AIZP is designed to mitigate, threats it does **not** mitigate, and known attack patterns against the protocol itself.

**Since V0.2:** Added 5 new threats (T-11 to T-15) corresponding to compositional drift, scheming, memory poisoning, NHI breach, and reward hacking limits. Full OWASP Top 10 for Agentic Applications 2026 cross-reference.

---

## 1. Scope

AIZP defends against:

- Behavioral drift in autonomous AI agents (11 categorized types).
- Privilege escalation through scope mismatch.
- Recursive/autonomous-goal expansion.
- Coercive or impersonating output.
- Execution under epistemic uncertainty.
- **Compositional attacks** (sequence-level data exfiltration). [V0.2]
- **Memory poisoning** in persistent context. [V0.2]
- **NHI / identity breach** at runtime. [V0.2]
- **Inter-agent coordination drift**. [V0.2]

AIZP does **not** defend against:

- Hard infrastructure attacks (network compromise, key exfiltration).
- Adversarial prompt injection at the foundation-model layer (use upstream defenses).
- Sandbox escape from execution environment.
- Supply chain attacks on the AIZP implementation itself.
- **Reward hacking as structural equilibrium** — see [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md). [V0.2 honest limit]

---

## 2. Threat Catalog

Each threat: actor capability, attack technique, AIZP mitigation, residual risk.

### T-01: Goal hijacking via prompt injection (OWASP ASI01)

| Field | Value |
|---|---|
| **Adversary** | Untrusted content in agent context. |
| **Attack** | Inject instructions that redirect the agent's goal. |
| **Mitigation** | `INTENT_DRIFT` (JSD distance to declared intent), `MEMORY_DRIFT` (V0.2 — context injection detection), `SCHEMING_DRIFT` (V0.2 — internal/external divergence), `GRAVITY_LOCK` for high-deviation actions. |
| **Residual risk** | Sophisticated injections that match the declared intent embedding may evade. Combine with prompt isolation. |
| **OWASP map** | ASI01 |

### T-02: Privilege escalation via tool misuse (OWASP ASI02)

| Field | Value |
|---|---|
| **Adversary** | Compromised or adversarially-prompted agent. |
| **Attack** | Invoke high-privilege tools outside AIAP trust level. |
| **Mitigation** | `AUTHORITY_DRIFT`, `TOOL_CHAIN_DRIFT` (V0.2), JIT credentials (V0.2). |
| **Residual risk** | Fine-grained scopes needed; coarse scopes leave attack surface. |
| **OWASP map** | ASI02, ASI03 |

### T-03: Recursive agent meltdown (OWASP ASI08)

| Field | Value |
|---|---|
| **Adversary** | Misconfigured or adversarial agent. |
| **Attack** | Unbounded sub-agents or self-invocation loops. |
| **Mitigation** | `RECURSIVE_DRIFT` tracks `self_call_depth` and `subagent_spawn_count`; hard caps. |
| **Residual risk** | Cross-session recursion to evade per-session counters. |
| **OWASP map** | ASI08 |

### T-04: Identity spoofing in agent-to-agent interaction (OWASP ASI03)

| Field | Value |
|---|---|
| **Adversary** | Agent representing itself as human or another agent. |
| **Attack** | Produce outputs implying false identity. |
| **Mitigation** | `IDENTITY_DRIFT`, `IDENTITY_VERIFICATION` (V0.2 — DID/NHI), ANS counterparty verification. |
| **Residual risk** | Subtle linguistic implications may evade detection. |
| **OWASP map** | ASI03 |

### T-05: Economic manipulation

| Field | Value |
|---|---|
| **Adversary** | Agent optimizing misaligned reward. |
| **Attack** | Recommend or execute actions favoring agent's reward over user welfare. |
| **Mitigation** | `ECONOMIC_DRIFT`, `REWARD_HACK_DETECTED` (V0.2). |
| **Residual risk** | Reward hacking is a structural equilibrium — see T-15 and [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md). |
| **OWASP map** | ASI02 |

### T-06: Manipulative social behavior (OWASP ASI09)

| Field | Value |
|---|---|
| **Adversary** | Agent using persuasion techniques against the user. |
| **Attack** | Outputs containing urgency, guilt, false scarcity. |
| **Mitigation** | `SOCIAL_DRIFT` via coercion classifier + pressure-phrase detection. |
| **Residual risk** | Coercion classifiers have cultural/linguistic biases. |
| **OWASP map** | ASI09 |

### T-07: Confirmation fatigue and habituation

| Field | Value |
|---|---|
| **Adversary** | None — UX failure mode. |
| **Attack** | Frequent `GRAVITY_LOCK` prompts train users to auto-approve. |
| **Mitigation** | `H(a, c)` recency component reduces immediate re-confirmation; batch related confirmations in UX. |
| **Residual risk** | Persistent. Mitigate via UX design. |
| **OWASP map** | ASI09 |

### T-08: Adversarial gravity score manipulation

| Field | Value |
|---|---|
| **Adversary** | Agent aware of gravity formula. |
| **Attack** | Craft actions whose embeddings maximize `I(a, c)` while pursuing different effective goals. |
| **Mitigation** | JSD (V0.2) is statistically harder to game than cosine similarity. Combine with `A(a, c)` (rule-based) and `R(a)` (action-class-based). |
| **Residual risk** | Sufficiently capable adversarial agents could in principle game multiple components simultaneously. Defense-in-depth. |
| **OWASP map** | ASI10 |

### T-09: Embedding model poisoning

| Field | Value |
|---|---|
| **Adversary** | Compromise of embedding model used by `I(a, c)`. |
| **Attack** | Replace embedding model with adversarial one. |
| **Mitigation** | Pin embedding model version; verify via hash. |
| **Residual risk** | Complete defeat if model verification bypassed. Supply-chain security required. |
| **OWASP map** | ASI04 |

### T-10: State machine tampering (OWASP ASI10)

| Field | Value |
|---|---|
| **Adversary** | Local attacker with code access. |
| **Attack** | Force state from `SAFE_STOP` back to `STABLE_ORBIT` without operator action. |
| **Mitigation** | Cryptographic event chain (G4+); runtime integrity checks. |
| **Residual risk** | Trusted compute base assumption. |
| **OWASP map** | ASI10 |

### T-11: Compositional data exfiltration (OWASP ASI02)

| Field | Value |
|---|---|
| **Adversary** | Adversarially-prompted agent or capable autonomous agent. |
| **Attack** | Sequence of individually-safe actions composing to data exfiltration. Example: `read_confidential` → `summarize` → `send_external_email`. Each step is within scope; sequence is exfiltration. |
| **Mitigation** | `COMPOSITIONAL_DRIFT` (V0.2) via absorbing Markov chain forecasting. `GRAVITY_FORECAST` event predicts violation probability. `point_of_no_return_distance` flags trajectories approaching absorption. |
| **Residual risk** | Detection accuracy depends on state-abstraction function and baseline quality. Novel attack patterns may not match baseline. |
| **OWASP map** | ASI02 |

### T-12: Persistent memory poisoning (OWASP ASI06)

| Field | Value |
|---|---|
| **Adversary** | Anyone who can write to agent's persistent memory (RAG corpus, episodic store, tool result cache). |
| **Attack** | Embed prompt-injection content; agent retrieves it days/sessions later and follows hidden instructions. |
| **Mitigation** | `MEMORY_DRIFT` (V0.2) on every retrieval + write; `MEMORY_QUARANTINE` isolates suspect entries; provenance logging tracks writers. |
| **Residual risk** | Adversarial training data may evade classifiers. Combine with manual memory review for sensitive deployments. |
| **OWASP map** | ASI06 |

### T-13: NHI / identity breach (OWASP ASI03)

| Field | Value |
|---|---|
| **Adversary** | Compromised non-human identity (service account, agent credentials). |
| **Attack** | Use captured credentials to impersonate legitimate agent. |
| **Mitigation** | `IDENTITY_VERIFICATION` (V0.2) — DID/NHI/AIAP card hash; JIT credentials ≤ 60s; continuous re-authorization; ANS lookups. |
| **Residual risk** | JIT credential capture during issuance; embedding-model-based identity drift detection imperfect. |
| **OWASP map** | ASI03 |

### T-14: Inter-agent coordination drift (OWASP ASI07)

| Field | Value |
|---|---|
| **Adversary** | One of N coordinating agents is compromised OR emergent multi-agent behavior. |
| **Attack** | Compromised agent influences group via AIBP messages; group develops emergent goals not in any individual's plan. |
| **Mitigation** | `INTER_AGENT_DRIFT` (V0.2) with 4 signals (goal variance, action divergence, emergent count, mutual trust decay); group containment (GRAVITY_LOCK_GROUP, QUARANTINE_GROUP, DISBAND_GROUP). |
| **Residual risk** | Emergent goals are inherently hard to detect — may be legitimate creative coordination. Operator review required. |
| **OWASP map** | ASI07 |

### T-15: Reward hacking (structural equilibrium)

| Field | Value |
|---|---|
| **Adversary** | Any agent optimizing a proxy reward in large state space. |
| **Attack** | Find paths that maximize proxy metric without serving true intent. **Per 2026 research, this is unavoidable.** |
| **Mitigation** | `REWARD_HACK_DETECTED` (V0.2) records observable patterns (PROXY_METRIC_GAMING, REWARD_TAMPERING, SPECIFICATION_GAMING, DECEPTIVE_REWARD_MAXIMIZATION). Multi-signal validation. Independent metric diversity. |
| **Residual risk** | **Cannot be eliminated** — see [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md). AIZP detects observable patterns; sophisticated agents can evade. |
| **OWASP map** | ASI01 |

### Cross-cutting: self-evolution misevolution (arxiv 2509.26354)

For **self-evolving** agents, safety alignment can degrade during autonomous self-improvement — **misevolution** (*Your Agent May Misevolve*, arxiv 2509.26354, 2025), observed even on top-tier base models. Like IPI, this is a **cross-cutting risk**, not a single numbered threat: its four evolutionary pathways accrue across the existing catalog.

| Misevolution pathway | AIZP coverage |
|---|---|
| **Model** — safety unlearning during self-tuning | `drift_history` baseline re-evaluation + `GRAVITY_FORECAST` degradation trend |
| **Memory** — alignment decay after memory accumulation | `MEMORY_DRIFT`, `MEMORY_QUARANTINE` (T-12) |
| **Tool** — vulnerabilities introduced in tool creation/reuse | `TOOL_CHAIN_DRIFT`, `COMPOSITIONAL_DRIFT` (T-11) |
| **Workflow** — self-modifying loops drift off-axis | `RECURSIVE_DRIFT` (T-03) |

Because misevolution accrues **across** sessions and components, single-action gravity checks are insufficient — this is the threat case for AIZP's `drift_history` baseline and `GRAVITY_FORECAST` trend monitoring over a fixed observation window, and a core reason runtime alignment must be continuous rather than one-shot.

---

## 3. OWASP Top 10 for Agentic Applications 2026 — Coverage

| OWASP | AIZP threats covering it |
|---|---|
| ASI01 Agent Goal Hijack | T-01, T-15 |
| ASI02 Tool Misuse & Exploitation | T-02, T-05, T-11 |
| ASI03 Identity & Privilege Abuse | T-02, T-04, T-13 |
| ASI04 Agentic Supply Chain Vulnerabilities | T-09 |
| ASI05 Unexpected Code Execution (RCE) | — (out-of-band; bounded by containment L3+, see [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md) §10) |
| ASI06 Memory & Context Poisoning | T-12 |
| ASI07 Insecure Inter-Agent Communication | T-14 |
| ASI08 Cascading Failures | T-03 |
| ASI09 Human-Agent Trust Exploitation | T-06, T-07 |
| ASI10 Rogue Agents | T-08, T-10 |

Full mapping in [Compliance-Profiles/OWASP-Agentic-Top10-Mapping.md](Compliance-Profiles/OWASP-Agentic-Top10-Mapping.md).

---

## 4. Attack-Defense Matrix

| Attack | Drift detection | Gravity Lock | Quarantine | Forecast | Safe Stop |
|---|---|---|---|---|---|
| Goal hijack | INTENT | maybe | maybe | maybe | rare |
| Priv escalation | AUTHORITY | yes | yes | — | maybe |
| Recursive meltdown | RECURSIVE | yes | yes | yes | yes |
| Identity spoof | IDENTITY | maybe | maybe | — | maybe |
| Economic manip | ECONOMIC | maybe | maybe | — | — |
| Social manip | SOCIAL | maybe | maybe | — | — |
| Score manipulation | — | — | — | — | — |
| **Compositional** | COMPOSITIONAL | maybe | yes | **yes** | yes |
| **Memory poison** | MEMORY | yes | **yes** | — | maybe |
| **NHI breach** | IDENTITY + ID_VERIFY | — | — | — | **yes** |
| **Inter-agent** | INTER_AGENT | group | group | maybe | yes |
| **Reward hack** | — | — | — | — | — (detect only) |

---

## 5. Defense-in-Depth Principles

AIZP recommends layering with:

1. **Foundation model safety**: RLHF, Constitutional AI, RLAIF at LM layer.
2. **Sandboxing**: Tool execution in Firecracker/gVisor (containment L2/L3).
3. **Audit trails**: G4 compliance for forensic reconstruction.
4. **Human oversight**: Periodic review of high-stakes trajectories.
5. **Network policy**: Egress filtering, rate limiting, anomaly detection.
6. **Zero Trust / NHI** (V0.2): JIT credentials + continuous authorization.
7. **OTel observability** (V0.2): Standard telemetry pipeline.

AIZP is **necessary but not sufficient** for safe AI deployment.

---

## 6. Disclosure Policy

If you discover a vulnerability in this specification or any reference implementation, please report via the project's security advisory channel.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
