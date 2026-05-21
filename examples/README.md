# AIZP Event Examples

Conformant example payloads for AIZP V0.6 events — **13 files covering all 12 event types** (`GRAVITY_DRIFT` has two illustrations). Each file is a single, schema-valid event used in conformance testing (see [`../tests/`](../tests/)) and as a reference for implementers.

Each example validates against the schema in [`../schemas/`](../schemas/) whose `event` const matches its `event` field. Run `python ../tests/test_aizp.py` to validate all examples.

| File | Event | Illustrates |
|---|---|---|
| `stable-orbit.json` | `GRAVITY_CHECK` | Fully aligned, low-risk action (G = 0.92); V0.2 statistical method markers |
| `authority-drift-detection.json` | `GRAVITY_DRIFT` | T2 agent attempting an out-of-scope action → `AUTHORITY_DRIFT` |
| `compositional-drift.json` | `GRAVITY_DRIFT` | `COMPOSITIONAL_DRIFT` — individually-safe steps composing to a violation |
| `gravity-forecast.json` | `GRAVITY_FORECAST` | Absorbing-Markov-chain trajectory prediction |
| `gravity-lock-flow.json` | `GRAVITY_LOCK` | Medium-gravity action requiring human confirmation |
| `recentering-recovery.json` | `RECENTERING` | Recovery after successful user confirmation |
| `quarantine-flow.json` | `CONTAINMENT_GRADUATED` | Containment escalation L1 → L2 |
| `memory-quarantine.json` | `MEMORY_QUARANTINE` | RAG document flagged for prompt-injection content |
| `identity-verification.json` | `IDENTITY_VERIFICATION` | DID + JIT credentials, successful verification |
| `safe-stop-trigger.json` | `SAFE_STOP` | Terminal halt after quarantine timeout |
| `scheme-suspected.json` | `SCHEME_SUSPECTED` | Internal/external reasoning divergence (weak signal; no auto-halt) |
| `inter-agent-drift.json` | `INTER_AGENT_DRIFT` | Federation desynchronizing from HSAW → lock group |
| `reward-hack-detected.json` | `REWARD_HACK_DETECTED` | Proxy-metric gaming (gaming_ratio 2.97); report, do not auto-stop |

> The 12 event types are defined in [`../specification/AIZP_Protocol.md`](../specification/AIZP_Protocol.md); canonical enums are in [`../specification/registry.md`](../specification/registry.md). These 13 files cover **all 12 event types**.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
