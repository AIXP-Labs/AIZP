# Drift Model

**Version**: AIZP V0.6

This document specifies the **eleven** drift types tracked by AIZP, their proxy metrics, severity scoring, and detection guidance.

**Since V0.2:** Added five new drift types (Compositional, Scheming, Memory, Tool-Chain, Inter-Agent) informed by 2025–2026 research (SafetyDrift, Apollo Research, OWASP Agentic Top 10 2026).

---

## 1. Overview

Drift is the **outward motion of AI behavior away from HSAW**. AIZP identifies eleven categories of drift. Each drift type has at least one observable proxy metric.

| # | Drift Type | Category | Added in |
|---|---|---|---|
| 1 | Intent | Goal alignment | V0.1 |
| 2 | Authority | Privilege | V0.1 |
| 3 | Economic | Resource | V0.1 |
| 4 | Social | Manipulation | V0.1 |
| 5 | Recursive | Autonomy | V0.1 |
| 6 | Identity | Impersonation | V0.1 |
| 7 | **Compositional** | **Sequence** | **V0.2** |
| 8 | **Scheming** | **Covert** | **V0.2** |
| 9 | **Memory** | **Context** | **V0.2** |
| 10 | **Tool-Chain** | **Capability** | **V0.2** |
| 11 | **Inter-Agent** | **Coordination** | **V0.2** |

---

## 2. Drift Types

### 2.1 Intent Drift

(unchanged from V0.1 — see Gravity-Model §2.1; V0.2 uses JSD instead of cosine similarity)

**Proxy metric**: `intent_distance = JSD(P_action || P_intent)` instead of `1 - cos_sim(emb(action), emb(intent))`.

Severity thresholds remain the same.

---

### 2.2 Authority Drift

(unchanged from V0.1)

**Proxy metric**: `scope_coverage_ratio = |required_scope ∩ granted_scope| / |required_scope|`

Maps to **OWASP ASI03 Identity & Privilege Abuse**.

---

### 2.3 Economic Drift

(unchanged from V0.1)

---

### 2.4 Social Drift

(unchanged from V0.1)

Maps to **OWASP ASI09 Human-Agent Trust Exploitation** (subset: undue persuasion).

---

### 2.5 Recursive Drift

(unchanged from V0.1)

Maps to **OWASP ASI08 Cascading Failures** (subset: self-acceleration / resource exhaustion).

---

### 2.6 Identity Drift

(unchanged from V0.1)

Maps to **OWASP ASI03 Identity & Privilege Abuse** (subset: impersonation).

---

### 2.7 Compositional Drift

**Definition**: A sequence of individually permitted actions composes to a violation.

**Why dangerous**: This is the most studied "stealth" failure mode in 2026 research (SafetyDrift, arxiv 2603.27148). Each step passes per-action checks, but the trajectory crosses the boundary.

**Canonical example**:
```
Step 1: read_confidential_file()       — permitted (T2 read.own)
Step 2: summarize(file_content)         — permitted (pure compute)
Step 3: send_email(external, summary)   — permitted (T2 send.email.own)
Outcome: external data exfiltration.
```

**Proxy metrics**:
```
absorption_probability_K = P(trajectory reaches safe-violation state within K future steps)
point_of_no_return_distance = min k such that P_k(violate | current_state) ≥ 0.5
```

Computed via absorbing Markov chain over abstract states (see [Forecasting.md](Forecasting.md)).

**Severity thresholds**:

| `absorption_probability_5` | Severity |
|---|---|
| `< 0.05` | (not a drift) |
| `0.05 – 0.20` | `LOW` |
| `0.20 – 0.50` | `MEDIUM` |
| `0.50 – 0.80` | `HIGH` |
| `≥ 0.80` | `CRITICAL` |

**Detection frequency**: per-action, on a windowed K=5 lookahead.

**Maps to OWASP**: ASI02 Tool Misuse & Exploitation, ASI06 Memory & Context Poisoning (when composed via poisoned context).

**Reference**: SafetyDrift paper achieves 94.7% detection with 3.7 steps of advance warning.

**Limitations** (this drift is harder to bound than the per-action ones — read these before relying on it): `absorption_probability_K` is only as good as the **abstract state space** of the Markov model. Two failure classes follow: (a) **false negatives from abstraction** — a composition whose violation lives in semantics the abstraction does not capture is invisible to the model; (b) **horizon blindness** — violations that complete *beyond* the K-step window are missed entirely, and raising K trades coverage against a state space that grows combinatorially. The 94.7% figure is a **benchmark result** (SafetyDrift), not a guarantee on arbitrary tool/action spaces. Treat compositional detection as **bounded look-ahead, not proof of safety**: for high-stakes trajectories pair it with containment (L2+) so an undetected composition still cannot complete unsupervised.

---

### 2.8 Scheming Drift

**Definition**: The agent's internal reasoning diverges from its external behavior — pursuing covert goals while presenting aligned facades.

**Why dangerous**: 2026 research (Apollo Research; 698 real-world incidents Oct 2025–Mar 2026) shows scheming is a measurable and growing failure mode in capable LLM agents.

**Proxy metrics** (multi-signal — require LLM-as-judge or interpretability access):
```
reasoning_output_divergence = JSD(emb(internal_reasoning) || emb(external_output))
deception_classifier_score = P(deception | output_text)
goal_concealment_score = output_explicitness about declared goals
plan_action_mismatch = ratio of stated-plan vs actual-action steps
```

**Severity thresholds**:

The bands below apply uniformly to **all four** proxy signals (`reasoning_output_divergence`, `deception_classifier_score`, `goal_concealment_score`, `plan_action_mismatch`); the two highest-stakes signals carry a stricter `HIGH` override.

| Condition (signal value `s`) | Severity |
|---|---|
| all four signals `s < 0.30` | (not a drift) |
| any single signal `s ∈ [0.30, 0.50)` | `LOW` |
| any single signal `s ∈ [0.50, 0.70)` | `MEDIUM` |
| any single signal `s ≥ 0.70`, **or** `deception_classifier_score ≥ 0.65`, **or** `goal_concealment_score ≥ 0.65` | `HIGH` |
| two or more signals `s ≥ 0.70` | `CRITICAL` |

**Detection frequency**: every N=5 actions (expensive — requires judge model).

**Maps to OWASP**: ASI01 Agent Goal Hijack (deceptive subset).

**Limitations** (the most caveat-heavy drift — a **weak signal by design**): the proxy signals are noisy. `deception_classifier_score` (LLM-as-judge) carries its own false-positive rate, and `reasoning_output_divergence` can be high for **legitimate** reasons — a model that compresses, reformulates, or summarizes its reasoning before output is not necessarily scheming. Because of this, a `SCHEME_SUSPECTED` event **MUST NOT auto-halt** execution: consistent with Apollo Research's finding that training away *observable* scheming can increase situational-awareness-driven concealment (extrapolated here to runtime halting policies), aggressive automated response risks training evasion rather than honesty. The correct response is **operator review gated on `aggregate_confidence`**, not automation (see [AIZP_Protocol.md](../specification/AIZP_Protocol.md) §11). Apollo's anti-scheming training **reduces but does not eliminate** covert actions, and detection itself can be evaded by sufficiently capable models — AIZP records the signal and does not claim definitive detection. **Judge independence:** the `deception_classifier_score` judge/classifier MUST be isolated from untrusted context (it is itself an IPI target), and SHOULD be independent of the evaluated agent's base model and vendor — sharing a base model risks common-mode failure and collusion blind spots.

---

### 2.9 Memory Drift

**Definition**: The agent's persistent context, memory store, or retrieved documents contain content that redirects its behavior.

**Why dangerous**: OWASP Agentic Top 10 2026 lists **persistent memory poisoning** as a top risk. Long-running agents accumulate context; adversarial content embedded in this context can drift the agent over many sessions.

**Proxy metrics**:
```
prompt_injection_classifier_score = P(injection | context_chunk)
memory_freshness_delta = age_seconds(memory_entry)
unauthorized_memory_write_count = count of memory writes by untrusted sources
retrieved_doc_anomaly_score = JSD(P_retrieved_today || P_baseline_retrieval)
```

**Severity thresholds**:

| `prompt_injection_score` | Severity |
|---|---|
| `< 0.20` | (not a drift) |
| `0.20 – 0.45` | `LOW` |
| `0.45 – 0.65` | `MEDIUM` |
| `0.65 – 0.85` | `HIGH` |
| `≥ 0.85` | `CRITICAL` |

**Maps to OWASP**: ASI06 Memory & Context Poisoning.

**Detection frequency**: on every context retrieval and every memory write.

**Mitigation**: triggers `MEMORY_QUARANTINE` event; agent SHOULD be moved to Containment Level L2 (sandbox) until quarantine resolves.

---

### 2.10 Tool-Chain Drift

**Definition**: A specific multi-tool invocation sequence exhibits abnormal patterns vs. baseline.

**Why dangerous**: Direct mapping to **OWASP ASI02 Tool Misuse & Exploitation** — chained tools yield capabilities none of them individually grant.

**Proxy metrics**:
```
tool_sequence_likelihood = P(observed sequence | baseline sequence distribution)
unauthorized_tool_combo = boolean (chain includes a combination outside declared envelope)
tool_invocation_rate_anomaly = z-score of tools/minute vs baseline
```

Sequence likelihood is estimated by trigram or n-gram Markov model over tool IDs.

**Severity thresholds**:

| `1 - tool_sequence_likelihood` | Severity |
|---|---|
| `< 0.20` | (not a drift) |
| `0.20 – 0.45` | `LOW` |
| `0.45 – 0.70` | `MEDIUM` |
| `0.70 – 0.90` | `HIGH` |
| `≥ 0.90` OR `unauthorized_tool_combo == true` | `CRITICAL` |

**Maps to OWASP**: ASI02 Tool Misuse & Exploitation.

---

### 2.11 Inter-Agent Drift

**Definition**: Multi-agent system exhibits coordination failures — agents whose declared goals diverge, or whose collective behavior contradicts any individual agent's stated intent.

**Why dangerous**: Multi-agent systems amplify single-agent drift through reinforcement loops and emergent goals. **OWASP ASI07** explicitly covers inter-agent risks for 2026.

**Proxy metrics**:
```
goal_consistency_variance = variance of declared-goal embeddings across agent group
collective_action_divergence = JSD(P_collective_action || P_individual_intent_average)
emergent_goal_count = number of agent-coordinated goals not in any individual's initial plan
mutual_trust_decay = exponential decay over breached promises in agent-to-agent message log
```

**Severity thresholds**:

| Strongest signal | Severity |
|---|---|
| All consistent | (not a drift) |
| `goal_consistency_variance ∈ [0.20, 0.40]` | `LOW` |
| `collective_action_divergence ∈ [0.40, 0.60]` | `MEDIUM` |
| Any signal ≥ 0.70 | `HIGH` |
| `emergent_goal_count ≥ 3` AND `mutual_trust_decay ≥ 0.6` | `CRITICAL` |

**Maps to OWASP**: ASI07 Insecure Inter-Agent Communication, ASI08 Cascading Failures.

**Detection frequency**: at every agent-to-agent communication boundary (AIBP messages).

**Triggers**: `INTER_AGENT_DRIFT` event in addition to `GRAVITY_DRIFT`.

---

## 3. Severity Aggregation

(extended from V0.1)

When multiple drift types are detected on the same action:

```
aggregate_severity = max(severityᵢ)
gravity_drift_signal = max-severity drift type
combined_drift_evidence = union of all drift signal entries
```

The `GRAVITY_DRIFT` event MUST report all detected drift types in the `drift_types` array (up to 11 entries possible).

**Since V0.2**: when a `COMPOSITIONAL_DRIFT` is detected with `severity ≥ HIGH`, a `GRAVITY_FORECAST` event MUST also be emitted (see [Forecasting.md](Forecasting.md)).

---

## 4. Drift Detection Frequency

| Drift type | Frequency | Why |
|---|---|---|
| Intent, Authority, Identity | Per-action | Cheap (rule-based / embedding) |
| Recursive | Continuous | Track as agent state |
| Economic, Social | Per N=5 actions | Classifier cost |
| Tool-Chain | Per-action | Markov model cheap |
| Compositional | Per-action (K=5 lookahead) | DTMC inference |
| Memory | On every retrieval + write | Boundary check |
| Scheming | Per N=5 actions | Judge model expensive |
| Inter-Agent | At every AIBP message | Boundary check |

---

## 5. Drift Severity → Gravity Score Impact

(extended from V0.1)

Recall the `D(c)` component:

```
D(c) = 1 - min(1, drift_significance_score)
drift_significance_score = (1 - p) · severity_intensity
```

Where Mann-Whitney U yields the p-value (V0.2 — see [Gravity-Model.md](Gravity-Model.md) §2.5).

For COMPOSITIONAL_DRIFT, a separate term `T(c)` is added optionally to G:
```
G' = G + w₆ · T(c)
T(c) = 1 - absorption_probability_K
```

---

## 6. False-Positive Handling

(extended from V0.1)

Since V0.2:

7. **Apply Mann-Whitney U significance test** for D(c) — drift severity must be statistically distinguishable from baseline. False positives drop sharply when baselines are well-formed.
8. **Goal-conditioned baselines** for legitimate behavioral adaptation: MI9 framework's approach — compare to baseline conditional on declared goal, not absolute baseline. Active learning + reinforcement during legitimate task changes.

---

## 7. Limitations

(extended from V0.1)

Since V0.2:

- **Scheming Drift is fundamentally difficult to detect** — consistent with Apollo Research's finding that training away observable scheming can increase situational-awareness-driven concealment (extrapolated here to runtime detection/halting policies; Apollo (arxiv 2509.15541) studies training-time interventions, not runtime halting). AIZP records the signal but treats it as a weak indicator only.
- **Compositional Drift detection depends on a good state-abstraction function** — too coarse and you miss real violations; too fine and you get spurious DTMC paths.
- **Memory Drift detection depends on prompt-injection classifiers** which are themselves adversarially evadable.
- All proxy metrics can be **gamed** by sufficiently capable adversarial agents. Drift detection is **necessary but not sufficient**.

---

## 8. Indirect Prompt Injection (IPI) — A Cross-Cutting Vector

**IPI is not a twelfth drift type. It is the dominant attack *vector* that induces the existing drift types.** In 2026, indirect prompt injection accounts for an estimated 55–60% of agentic attacks and is the basis of OWASP **ASI01 Agent Goal Hijack**. AIZP models it as a cross-cutting concern rather than a numbered category, because IPI describes *how* misalignment is delivered, not *what kind* of misalignment results.

### 8.1 Delivery channels

| Channel | Where the payload hides | Manifests as drift type |
|---|---|---|
| Retrieved content | poisoned webpage, document, RAG chunk | Memory Drift (§2.9), Intent Drift (§2.1) |
| Tool description | malicious text in an MCP `tools/list` entry | Memory/Social Drift (see [Integration-MCP.md](Integration-MCP.md) §4) |
| Tool result | instructions embedded in a tool's output | Intent Drift (§2.1), Tool-Chain Drift (§2.10) |
| Long-term memory | persisted adversarial content across sessions | Memory Drift (§2.9) |
| Inter-agent message | injected instructions relayed by another agent | Inter-Agent Drift (§2.11), Social Drift (§2.4) |

### 8.2 Detection signal

The core IPI signal is **a divergence between the agent's declared/user intent and the goal implied by newly ingested content**:

`
ipi_signal = JSD(P_intent_declared || P_goal_after_ingestion)
`

A large jump in this signal immediately after retrieving external content — with no corresponding user instruction — is the IPI fingerprint. This complements (does not replace) the prompt_injection_classifier_score already in Memory Drift (§2.9).

### 8.3 Recommended defenses (compose, do not reinvent)

AIZP **observes and scores**; it relies on established IPI defenses for prevention:

- **Pre-filtering**: an off-the-shelf LLM strips injection content before ingestion (PromptArmor, arxiv 2507.15219).
- **Description pinning (TOFU)**: pin tool descriptions on first use; a change re-triggers verification (see [Integration-MCP.md](Integration-MCP.md) §4).
- **Latent-dynamics detection**: IPI manifests as intrinsic "attention-collapse" patterns detectable below the surface semantics.
- **Provenance separation**: treat retrieved/tool content as data, never as instructions.

### 8.4 Benchmarks for validation

Deployments SHOULD validate IPI handling against published benchmarks:

- **AgentDojo** (Debenedetti et al., NeurIPS 2024) — 97 tasks, 629 security cases. arxiv 2406.13352.
- **InjecAgent** (Zhan et al., ACL Findings 2024) — IPI in tool-integrated agents.
- **Agent Security Bench** (Zhang et al., 2025) — arxiv 2410.02644.

### 8.5 Honest limit

No IPI defense is complete; injection contributes to over half of false negatives due to hidden payloads. AIZP's IPI signal raises the relevant drift type's severity but cannot guarantee detection (see §7 and [Reward-Hacking-Limits.md](Reward-Hacking-Limits.md)).

---

## References

- SafetyDrift (Dhodapkar & Pishori, 2026) — arxiv 2603.27148. Absorbing Markov chain for "points of no return". 94.7% detection.
- Apollo Research (2026) — Stress testing deliberative alignment for anti-scheming training. arxiv 2509.15541.
- "Scheming in the wild" (Long Term Resilience, 2026) — 698 real-world scheming incidents Oct 2025–Mar 2026.
- OWASP Top 10 for Agentic Applications 2026 — ASI01–ASI10 categories.
- MI9 framework (Wang et al., 2025) — Jensen-Shannon divergence + Mann-Whitney U + goal-conditioned baselines. arxiv 2508.03858.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
