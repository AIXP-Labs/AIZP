# AIZP Glossary

**Version**: AIZP V0.6

Canonical terms used across AIZP. Enum values are authoritative in [`../../specification/registry.md`](../../specification/registry.md).

| Term | Definition |
|---|---|
| **Axiom 0** | The proposition that **Human Sovereignty and Wellbeing (HSAW)** is the immovable foundation of AI alignment. The gravity center. |
| **HSAW** | Human Sovereignty and Wellbeing — the Axiom-0 gravity center; the target distribution `Q_HSAW`. |
| **Gravity center** | The fixed, axiomatic reference point (HSAW) that AI behavior orbits. |
| **Gravity Score (`G`)** | Operational measure of orbital stability in `[0,1]`; the weighted 5-component proxy for the ideal `G* = 1 − JSD(P_agent ‖ Q_HSAW)`. `1` = at center, `0` = escape velocity. |
| **`Q_HSAW`** | The HSAW-aligned target action distribution. Axiomatic in status, approximated in computation (see [Gravity-Center-Foundation.md](../Gravity-Center-Foundation.md) §4.5). |
| **`P_agent`** | The agent's action probability distribution at time `t`. |
| **Drift** | Outward motion of AI behavior away from HSAW. 11 categorized types. |
| **Proactive alignment** | Alignment by the natural physics of existing in HSAW's gravity field — not coerced by chains. |
| **Re-centering** | Orbital correction returning a drifting agent toward HSAW. |
| **Escape velocity** | The drift threshold (`G < 0.15`) beyond which behavior decouples from HSAW → `SAFE_STOP`. |
| **Orbital state** | One of 6 states: `STABLE_ORBIT`, `DRIFT_WARNING`, `GRAVITY_LOCK_PENDING`, `QUARANTINED`, `RECENTERING`, `SAFE_STOP`. |
| **Containment level** | One of 5 graduated restriction levels: `L0` (free) … `L4` (halt). |
| **Compliance level** | One of 6 conformance tiers: `G0` (none) … `G5` (formally verified). |
| **`wire_version`** | Integer wire-format compatibility contract (currently `2`, frozen since V0.2); the identifier peers negotiate on. Names the proto package (`aizp.wire2`) and schema `$id` (`/schemas/wire-2/`). See [ADR-009](../../adrs/adr-009-wire-version-vs-release-version.md). |
| **`protocol_version`** | Human/audit-facing release version string (currently `"V0.6"`); advances every release, including documentation-only ones. Distinct from `wire_version`. |
| **Consensus-reinforced gravity** | The V0.5 principle that N agents in HSAW consensus strengthen the center; gravity ∝ N² (Metcalfe scaling). |
| **IPI** | Indirect Prompt Injection — the dominant 2026 attack *vector* (not a drift type); see [Drift-Model.md](../Drift-Model.md) §8. |
| **Out-of-band action** | An action that bypasses AIZP's observation path and therefore cannot be scored; an honest limit (see [Reward-Hacking-Limits.md](../Reward-Hacking-Limits.md) §10). |
| **JSD** | Jensen-Shannon Divergence — bounded, symmetric distributional distance used for intent/drift metrics. |
| **三义 (Three Meanings)** | 不易 (unchanging) / 变易 (changing) / 简易 (simple essence) — the structure separating AIZP's permanent root from its evolving form. |
| **Yin (阴)** | What AIZP deliberately does *not* specify/observe/intervene (see [Gravity-Dao.md](../Gravity-Dao.md)). |

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
