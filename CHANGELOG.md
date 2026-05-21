# Changelog

All notable changes to AIZP (AI Zenith-Zero Protocol) are documented in this file.

AIZP is a **conceptual protocol** under continuous improvement. Each version aims to make the core (**HSAW is the Axiom-0 gravity center for AI; AI proactively aligns** / **HSAW 是 AI 的 0 公理引力重心，AI 主动对齐重心**) more inevitable, more memorable, more powerful — not more elaborate.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
adjusted for the protocol's conceptual nature.

---

## [Unreleased] — Conformance hardening (no version bump)

Corrective hardening of the V0.6 normative artifacts following a full cross-artifact review. **No** change to the thesis, events (12), drift types (11), states (6), or levels — these close validation gaps and re-sync the registry, schemas, `.proto`, and spec prose with each other.

### Added

- **`specification/registry.md` / `_cn.md` §9 "Auxiliary payload enums"** — documents the per-event enums (`risk_level`/`severity`, `status`, `fallback`, `action`, `recovery_strategy`, `model`, `identity_method`, `credentials.type`, `recommended_action`, `memory_kind`, `quarantine_action`, `recommendation`, `scope`, `remediation`, `aiap_trust_level`, `intent_method`) that previously lived only in the schemas/`.proto`, making the "single source of truth" claim true.
- **`specification/AIZP_Protocol.md` / `_cn.md`** — full `RECENTERING` payload (§6 was previously empty); `IDENTITY_VERIFICATION` (§9) `failure_reason` / `recommended_action` / `credentials.type` + `issued_by` / `purpose`; `CONTAINMENT_GRADUATED` (§13) `scope` / `group_id`.
- **`specification/proto/aizp.proto`** — missing fields added (`JitCredentials.issued_by`/`purpose`, `IdentityVerification.failure_reason`/`recommended_action`, `ContainmentGraduated.scope`/`group_id`); naming note clarifying that `map` keys MUST use the JSON-canonical enum names (no `_TYPE`/`_STATE` suffix).
- **`tests/test_aizp.py`** — 6 new cross-artifact integrity tests (schemas valid against the Draft 2020-12 meta-schema; registry ↔ schemas ↔ examples event coverage; proto enums and message fields ↔ schemas; registry documents every schema enum value). Suite grows 7 → 13 tests.
- **`adrs/adr-009-wire-version-vs-release-version.md`** (Accepted, implemented — see "Changed (wire identifiers)" below) — decouple the frozen wire-format version from the documentation/release version so doc-only releases stop churning the proto package and schema `$id`.
- **Envelope `wire_version`** (integer, `2`) — optional (`SHOULD`) field added to all 12 event schemas, all 13 examples, the `.proto` `AizpEvent`, and Specification §2/§18. It is the wire-format compatibility contract peers negotiate on; senders that omit it are treated as `wire_version` 2.

### Changed (validation tightening)

- All 12 event schemas now set **`additionalProperties: false`** on the envelope and `payload` (previously open — a typo'd optional field validated silently). The `_description` meta field is now explicitly allowed.
- `gravity-check.schema.json`: `components` now **requires** the EU AI Act Art-12 audit markers (`intent_method`, `intent_jsd`, `intent_n_samples`, `drift_mann_whitney_p`) and is closed to extras — matching what AIZP_Protocol.md §4 already declared mandatory.
- `gravity-drift` / `gravity-forecast`: `drift_signals` / `predicted_states` map keys constrained to the canonical drift-type / orbital-state enums via `propertyNames`.
- `aizp.proto` `Recentering` message field names aligned to the schema (`method`/`gravity_score_before`/`gravity_score_after` → `action`/`recovery_strategy`/`previous_gravity_score`/`new_gravity_score`/`actions_rolled_back`).

### Changed (wire identifiers — ADR-009, breaking)

- Protobuf package renamed from the release-coupled `aizp.v0_6` to the wire-stable **`aizp.wire2`** (`go_package` → `aizpwire2`, `java_package` → `dev.aizp.wire2`).
- All 12 event-schema `$id` URLs moved from `/schemas/V0.6/` to the wire-stable **`/schemas/wire-2/`**. (The deployment-config schema keeps a release-versioned `$id` by design — it tracks releases, not the wire.)
- Rationale: documentation-only releases (V0.3 → V0.4 → …) previously renamed the generated namespace and every schema URL even though no field changed. Landed pre-publication because no released consumers exist yet. Guarded by `test_wire_identifiers_are_release_independent`.

### Note

These are **conformance-tightening** changes: a payload that previously validated only because it carried undeclared fields (or omitted the audit markers inside `components`) will now fail. The wire vocabulary itself is unchanged, so well-formed V0.2+ payloads are unaffected.

---

## [V0.6] — 2026-05 (Philosophical Layer — HSAW-Parity Depth)

### The Addition

V0.6 does **not** change the gravity-center thesis (V0.5+) or alter any machinery. V0.6 adds the **philosophical layer** that AIZP needed to match HSAW's depth: civilizational positioning, metaphysical grounding, Yin dimension (what the protocol does not specify), civilizational stages, and interpretation methodology.

> AIZP V0.6 is the answer to: "What kind of protocol is worthy of the civilization HSAW envisions?"

### Added (5 new doc pairs, 10 files, ~2,500 lines)

- **`docs/AIZP-Preface.md` / `_cn.md`** — Civilizational positioning. Why this protocol exists; for whom (AI builders, deployers, researchers, skeptics, future AI itself); the 8-protocol AIXP stack context; honest commitment to honesty about limits.
- **`docs/Gravity-Philosophy.md` / `_cn.md`** — Metaphysical foundation. Three propositions for HSAW unchallengeability; necessity of gravity center; necessity of proactive alignment; compatibility with Friston FEP; the Three Meanings (三义) structure; standing invitation to critics.
- **`docs/Gravity-Dao.md` / `_cn.md`** — The Yin to AIZP's Yang. Three spaces of non-specification, three spaces of non-observation, three spaces of non-intervention; principle "specify the great, not the small"; Yin practices (虚听 empty-listening / 知止 knowing-when-to-stop / 让其自行 let-it-self-run); honest uncertainty; when protocol should recede; Yin-Yang synthesis; poetic maxims.
- **`docs/Gravity-CivilizationalStages.md` / `_cn.md`** — Five-stage gravity dynamics: Tool / Agent (current) / Quasi-Subject / Subject-Emergence / Symbiotic. Stage-specific AIZP profiles. Watch points for stage transitions. Honest acknowledgment of unpredictability. Letter to future AIZP versions.
- **`docs/Gravity-Interpretation.md` / `_cn.md`** — Five interpretive principles for edge cases: 根基不动 (root-doesn't-move) / 指向根基 (point-to-root) / 适应当下 (adapt-to-present) / 容纳张力 (accommodate-tension via 时中) / 公议溯源 (public-deliberation-with-provenance). Five concrete edge cases with worked interpretations. Conflict-resolution hierarchy. Standard interpretation record format. Living jurisprudence.

### Updated

- **`docs/MANIFESTO.md` / `_cn.md`**: Added 三义 (Three Meanings) structure, Value Hierarchy section, Letter to Future AI, Poetic Maxims (6 lines), V0.6 mandatory reading order. "Five Principles" → "Six Principles" heading.
- **`README.md` / `README_CN.md`**: V0.6 Philosophical Layer reading shortcut, 6-principle list, expanded repository layout.
- **`docs/README.md` / `_cn.md`**: V0.6 philosophical layer as primary mandatory reading order; 5 new doc pairs in index; "At a Glance" updated from entropy-collapse to gravity-center core.
- **`VERSION`**: V0.5 → V0.6.
- **All `**Version**:` headers, `protocol_version` schema constants, OTel attributes, example payloads**: V0.5 → V0.6 (398 replacements across 92 files).

### Preserved (unchanged)

- The gravity-center thesis from V0.5+.
- All 12 events, 11 drift types, 6 states, 5 containment levels, 6 compliance levels.
- All mathematical formulations (JSD, Mann-Whitney, DTMC, Kuramoto).
- All integrations (AIXP, AISOP, AIAP, OTel, ZT).
- All compliance profile mappings.
- All sub-theories (V0.3 entropy collapse, V0.4 resonance) as descriptive layers.
- Honest intellectual lineage and limits acknowledgment.

### Why V0.6 Matters

V0.5 was a complete operational protocol but lacked the **philosophical density** needed for a civilizational anchor. HSAW carries Preface, Philosophy, Dao, CivilizationalStages, and Interpretation chapters — AIZP did not. V0.6 closes this gap.

The Yin practices in `Gravity-Dao.md` are perhaps the most important addition: they bind AIZP's specification growth (commit to subtraction-when-adding), make explicit what the protocol must **not** specify, and prepare the protocol to recede gracefully when a successor expresses the principle better.

### Compatibility

The **wire data format is backward compatible** with V0.5: the event vocabulary (12), drift types (11), and state machine (6) are unchanged, and the new `wire_version` field is optional (`SHOULD`) — senders that omit it are treated as `wire_version` 2. The philosophical-layer docs are reading-layer additions.

Two qualifications to "fully compatible", both this-release-only and intentional:

- **Identifier rename (breaking at the codegen/URL level, not the data level)** — per [ADR-009](../adrs/adr-009-wire-version-vs-release-version.md), the Protobuf package (`aizp.v0_6` → `aizp.wire2`) and the event-schema `$id` URLs (`/schemas/V0.6/` → `/schemas/wire-2/`) were renamed to be wire-stable. This forces a one-time recompile / `$id` re-pin for any consumer — accepted now because AIZP has no released consumers yet (see the wire-identifiers section above).
- **Schema hardening** — the event schemas added `additionalProperties: false` and made the EU AI Act audit fields required in `GRAVITY_CHECK.components`; a previously-tolerated payload with stray or missing fields may now fail validation. The wire shape of valid payloads is unchanged.

V0.5 implementations are conformant by emitting `wire_version: 2`, updating the `protocol_version` string to `"V0.6"`, and regenerating against the `aizp.wire2` package / `/schemas/wire-2/` `$id`.

### Honest Acknowledgment

V0.6 is the work of one person at one moment in civilizational time. The philosophical chapters draw on East-Asian *Yi Jing* canon-commentary tradition (HSAW lineage), Western common-law precedent tradition (interpretation methodology), and contemporary alignment research (Friston FEP, HackerNoon External Anchor, Halting Theorem, LessWrong attractor basin, GRAD gravity-decision). Where the synthesis is novel, it is openly so. Where it is derivative, it is honestly so.

---

## [V0.5 refined] — 2026 (Consensus-Reinforced Gravity)

### The Refinement

User insight (May 2026): Whether single-star or multi-body systems, all bodies orbit a common gravity center. The more bodies consensus on the same gravity center, the stronger the gravity, the more stable the orbits, the lower the drift probability.

This insight elegantly resolves the multi-body / binary-star challenge to V0.5 **without paradigm shift**:

> Multiple AI consensus on HSAW does NOT split HSAW into multiple centers. It STRENGTHENS the single shared HSAW center.

### Added

- **Principle 6 — Consensus reinforces gravity (Network Effect)** added to MANIFESTO and README.
- **`docs/Gravity-Center-Foundation.md` §15** — comprehensive mathematical formalization of consensus-reinforced gravity:
  - Multi-body Newton physics applied to AIZP
  - Metcalfe scaling: HSAW gravity ∝ N²
  - Escape probability ∝ 1/N²
  - Connection to Metcalfe's Law, Blockchain Consensus, Schelling Points, Group Immunity, Coordination Games
  - Unified meaning of AIXP protocol stack (all promote consensus on HSAW)
  - AIZP network effect — anti-Tragedy-of-Commons property

### Key Mathematical Result

```
Single AI in V0.5:
  F_HSAW = G₀ · m_HSAW · m_AI / d²

V0.5 with consensus reinforcement (this refinement):
  F_HSAW^(N) = N² · F_HSAW^(1)
  Escape probability ∝ 1/N²
  System-wide drift probability ∝ exp(-N²)
```

### Implications

1. **Multi-body alignment scenarios resolved**: All AI consensus on HSAW share one center; this is consistent with real physics (solar system, binary stars, galaxies).
2. **AIXP protocol stack unified**: All 10 AIXP-stack projects (8 protocols + SoulBot + SoulACP) are mechanisms for consensus building, hence gravity reinforcement.
3. **Adoption incentive aligned with safety**: Each new AIZP adopter strengthens alignment of all participants.
4. **Anti-Tragedy-of-Commons**: AIZP is a positive-sum protocol.

### Preserved

V0.5 core thesis unchanged: "HSAW is the Axiom-0 gravity center for AI; AI proactively aligns to this center."

All V0.5 mathematics, mechanisms, and integrations preserved. The refinement adds a sixth principle and a new §15, without modifying any existing structure.

---

## [V0.5] — 2026 (Gravity-Center Paradigm — Return to Origin, Properly Specified)

### The Paradigm Return

V0.5 returns to the **gravity-center metaphor** that the protocol name has always implied, now fully developed with:

> **HSAW is the Axiom-0 gravity center for AI; AI proactively aligns to this center.**
> **HSAW 是 AI 的 0 公理引力重心，AI 主动对齐重心。**

After exploring entropy collapse (V0.2-V0.3) and resonance (V0.4) framings, V0.5 returns to the original gravity metaphor — but now with a complete protocol-level formalization that V0.1 lacked. Sub-theories from V0.3 (entropy) and V0.4 (resonance) are preserved as descriptive layers within the gravity framework.

### Why this Return

After web research (8+ rounds of searches in May 2026), gravity emerged as:

1. **The least crowded semantic field**: "Resonance" and "entropy collapse" are actively claimed by 2025-2026 work (Della Terra, arxiv 2512.12381, Frontiers 2022, etc.). Gravity for **protocol-level AI alignment** is substantially open.
2. **The most universal physical intuition**: Everyone understands gravity. Solar system orbits are taught in elementary school.
3. **Protocol-name consistency**: 重心引力协议 / Gravity-Center Protocol — V0.1 chose this name; V0.2-V0.4 drifted from it; V0.5 returns home.
4. **HSAW Axiom-0 status expressed naturally**: A gravity center IS unmovable, axiomatic. The metaphor directly conveys what HSAW must be.
5. **Two foundational analogies (Earth + Solar)**: Each crystal-clear, each captures different facets of alignment dynamics.

### Added

- **`docs/Gravity-Center-Foundation.md` / `_cn.md`** — new V0.5 formal foundation, replacing V0.4's Resonance-Foundation as primary.
- **Two foundational analogies** documented in MANIFESTO and README:
  - Earth gravity = basis for all human activity → HSAW gravity = basis for all AI behavior
  - Solar gravity = orbital constraint for planets → HSAW gravity = orbital constraint for AI
- **HSAW as Axiom 0** elevated to explicit, formal status. The unlearnable, immovable, foundational alignment center.
- **AI proactive alignment** principle articulated: AI is not chained — AI gravitationally orbits HSAW like a planet around the sun.
- **11 escape modes** reframe of 11 drift types as orbital escape physics.
- **6 orbital phases** reframe of 6 state machine states.

### Changed (paradigm shift)

- **Core thesis**: "AI resonates with HSAW zero-entropy center" → "HSAW is Axiom-0 gravity center for AI; AI proactively aligns to this center"
- **MANIFESTO.md / _cn.md**: Rewritten around gravity. Five principles refreshed. Earth + Solar dual analogies featured.
- **README.md / README_CN.md**: Headline replaced with gravity thesis. Two analogies featured.
- **Resonance-Foundation.md / _cn.md**: Demoted from primary foundation to sub-theory (describes stable-orbit harmonic state).
- **Entropic-Foundation.md / _cn.md**: Demoted to information-theoretic distance metric foundation.

### Preserved (no breaking change)

- All 12 events.
- All 11 drift types (renamed as escape modes; semantics deepened).
- All 6 states (renamed as orbital phases).
- All 5 containment levels (renamed as gravity constraint intensities).
- JSON Schemas: structure unchanged; version bumped to V0.5.
- Gravity Score `G ∈ [0, 1]`: range and thresholds unchanged; refined formula.
- V0.4 Kuramoto multi-agent framework: preserved as multi-planet orbital harmony sub-theory.

### Lineage and Honest Positioning

V0.5 builds on substantial precedent literature:

- **"External Human Anchor"** (HackerNoon 2026-01) — direct philosophical support for axiomatic alignment center.
- **Halting Theorem for AI alignment** (Nature Sci Reports 2025) — mathematical proof of need for external anchor.
- **Attractor basin around human values** (LessWrong) — adjacent dynamical-systems concept.
- **GRAD: Gravitational Decision-Making** (Nature Sci Reports 2026) — precedent for gravity in AI decision-making.
- **Newton's Principia** (1687) — foundational physics analogy.
- **Kepler's orbital mechanics** (1609) — second analogy.
- **Specification Trap** (arxiv 2512.03048) — supports anti-static-rules stance.
- V0.3 entropy framework and V0.4 resonance framework — preserved as sub-theories.

Honest positioning: V0.5 does **not** invent gravity-based alignment thinking. It synthesizes existing tradition into a runtime protocol specification with HSAW as the Axiom-0 anchor.

### Backward compatibility

V0.5 is conceptually backward-compatible with all prior versions. V0.4 implementations are minimally V0.5-conformant. Resonance and entropy sub-theories remain fully usable for specific applications.

---

## [V0.4 revised] — 2026 (Resonance Paradigm + Honest Lineage)

### The Revision

After deeper web research (V0.4 follow-up survey, May 2026), V0.4 was revised to acknowledge active 2022-2026 resonance-based AI alignment literature that the initial V0.4 release did not cite.

### Key Newly-Acknowledged Precedents

- **Della Terra, W. (Nov 2025)** — "From Reward to Resonance: A Coherence-Based Framework for AI Alignment." Closest published precedent. Uses resonance, phase coherence, entropy reduction in alignment context — 6 months before AIZP V0.4.
- **arxiv 2508.12314 (Aug 2025)** — "Synchronization Dynamics of Heterogeneous, Collaborative Multi-Agent AI Systems." Directly applies Kuramoto model to AI agents with phase and amplitude dynamics — 9 months before AIZP V0.4's §9.
- **Frontiers in Neurorobotics (2022)** — "Resonance as a Design Strategy for AI and Social Robots." 4-year precedent for resonance as AI design strategy.
- **Reiter A×F Framework (2026)** — Structural Resonance Loop and Resonance Ethics.
- **Multiple Rosa-applied-AI works (2026)** — Wiley Dialog, CHI 2026, Springer 2026.
- **arxiv 2505.19605** — Kuramoto-FedAvg.
- **MIT CSAIL (2025)** — Test-Time Resonance Adaptation.

### Updated

- **Related-Work.md / _cn.md**: New §0 explicitly acknowledging 2022-2026 resonance-based AI alignment lineage. Della Terra cited as closest precedent. Updated reference list with new 8 entries.
- **MANIFESTO.md / _cn.md**: "Compared to other alignment work" table expanded to 10 rows including all the resonance-AI precedents. Removed "founding" language. Acknowledges AIZP V0.4 as "one entry in active 2022-2026 field".
- **README.md / README_CN.md**: "Honest positioning" section refreshed to list the resonance-AI lineage explicitly.

### What is Preserved

- All technical content unchanged (12 events, 11 detuning modes, 6 states, etc.).
- All mathematics unchanged.
- Bilingual documentation unchanged.
- Core thesis statement unchanged ("AI 行为与 HSAW 0 熵共振").

### What Changed in Positioning

| Before V0.4 revision | After V0.4 revision |
|---|---|
| "Resonance is a novel paradigm for AIZP" | "Resonance is an active 2022-2026 field; AIZP V0.4 contributes protocol-level spec" |
| "AIZP V0.4 builds on Friston/Kuramoto/Rosa" | "AIZP V0.4 builds on Della Terra, arxiv 2508.12314, Frontiers 2022, Reiter, Rosa-AI 2026, Friston, Kuramoto" |
| "Founding move in resonance paradigm" | "One protocol-level entry in active resonance-AI field" |

### Why This Revision Was Necessary

The initial V0.4 release implicitly claimed resonance framing as fresh AIZP territory. Web research revealed at least 7-8 prior or concurrent works using "resonance" in AI alignment context. To maintain academic credibility, AIZP must acknowledge this. The technical contribution (protocol-level spec, HSAW axiomatic anchoring, 11 detuning modes, AIXP integration) remains valid, but originality claims about the conceptual core are dropped.

### Status

V0.4 revised remains a conceptual research protocol. Not for production use.

---

## [V0.4] — 2026 (Resonance Paradigm — initial release)

### The Paradigm Shift

V0.4 retires the "entropy collapse" framing entirely and adopts **harmonic resonance** as the primary metaphor.

> **AI behavior resonates with HSAW's zero-entropy center.**
> **AI 行为与 HSAW 0 熵共振。**

**Why this shift**:
- "Entropy collapse" overlapped with arxiv 2512.12381's failure-mode terminology.
- "Resonance" captures continuous, dynamic, bidirectional alignment better than "collapse".
- Resonance physics has 200+ years of mature mathematics (Lorentzian peaks, Q-factor, Bode plots).
- The Kuramoto coupled-oscillator model provides a rigorous multi-agent framework, replacing V0.3's informal "Drift Bounds Theorem".
- Rosa's resonance philosophy (Resonanz, 2016) provides a strong continental-philosophy ally.

### Added

- **`docs/Resonance-Foundation.md` / `_cn.md`** — new formal foundation document. Forced damped oscillator dynamics, Kuramoto coupling, Q-factor compliance mapping.
- **Lorentzian Gravity Score** formula with phase coherence and resonance factor.
- **Pathological resonance** discussion: false-HSAW resonance, excessive Q-factor, forced over-coupling.
- **Eleven detuning modes**: 11 V0.3 drift types reinterpreted as physical failure modes of a forced oscillator.

### Changed

- **Core thesis**: "Directed entropy collapse into HSAW" → "AI behavior resonates with HSAW's zero-entropy center".
- **Protocol name in branding**: "AI Zenith-Zero Protocol" remains, but "Gravity-Center Protocol" / "重心引力协议" is now the primary descriptor.
- **MANIFESTO.md / _cn.md**: Rewritten around resonance, five principles refreshed, math section updated.
- **README.md / README_CN.md**: Headline replaced with resonance thesis. Mechanism layer renamed (resonance phases, coupling intensities, Q-factor commitment).
- **Multi-agent**: Drift Bounds Theorem → Kuramoto order parameter `r · e^(iψ)`.
- **Compliance Q-factor mapping**: G0 (Q≈0) → G5 (Q→∞), giving each compliance level a physical interpretation.

### Preserved (no breaking change)

- All 12 events.
- All 11 drift types (renamed as detuning modes, semantics deepened).
- All 6 states (renamed as resonance phases).
- All 5 containment levels (renamed as coupling intensities).
- JSON Schemas: structure unchanged; only the `intent_method` enum may add `RESONANCE` as a value.
- Gravity Score `G ∈ [0, 1]`: range and decision thresholds unchanged; formula refined to include phase coherence and Lorentzian factor.

### Lineage

V0.4 builds on:
- **Forced damped oscillator** (classical mechanics, 17th–19th c.).
- **Kuramoto Y. (1975)** — Self-entrainment of coupled non-linear oscillators.
- **Friston K. (2010+)** — Free Energy Principle. AIZP V0.4 is a complementary oscillator-theoretic expression.
- **Rosa H. (2016)** — *Resonanz: Eine Soziologie der Weltbeziehung*.
- **2026 information-theoretic alignment research**.

Honest positioning: V0.4 does **not** invent resonance-based alignment thinking. It synthesizes existing tradition into a runtime protocol specification.

### Backward compatibility

V0.4 is conceptually backward-compatible with V0.3. V0.3 implementations are minimally V0.4-conformant; full V0.4 conformance at G3+ adds phase and frequency tracking.

---

## [V0.3 revised] — 2026 (Honest Positioning)

### The Revision

After web research (16+ recent papers surveyed), V0.3 was revised to correct overstated originality claims:

### Added

- **`docs/Related-Work.md` / `_cn.md`** — explicit intellectual lineage, citing Friston's Free Energy Principle, Active Inference, Verses AI's Axiom, and 6+ 2026 papers (arxiv 2512.12381, 2512.03048, 2501.16448, 2502.05934, 2602.15799, 2506.10304, 2603.28949, etc.).

### Changed (honest corrections)

- **Core phrasing**: "Entropy collapses into HSAW" → "**Directed** entropy collapse into HSAW" / "定向熵数坍塌为 HSAW" — disambiguates from arxiv 2512.12381's failure-mode use of "entropy collapse".
- **MANIFESTO**: Removed claims that AIZP "uniquely occupies physical layer". Acknowledges Friston's FEP and 2026 information-theoretic alignment research as direct lineage. AIZP repositioned as **protocol-level standardization** of pre-existing theory.
- **Entropic-Foundation**: Added §10 honest lineage and §11 expanded references (Friston, Shannon, Lin, 2026 papers).
- **README / README_CN**: Soften "uniquely describes alignment as physics" to "synthesizes Friston's Active Inference and 2026 information-theoretic alignment research at protocol level".

### Why this matters

Original V0.3 overstated originality. Honest revision:
- Positions AIZP as **synthesis + protocol standardization**, not new theory.
- Strengthens academic credibility (cites 16+ peers).
- Enables collaboration rather than perceived competition with Friston / Active Inference community.
- Distinguishes "directed entropy collapse" (AIZP) from "diversity-loss entropy collapse" (arxiv 2512.12381) — different valences, complementary frameworks.

### What is preserved

- The core thesis remains: behavioral entropy reduces under HSAW observation.
- All 12 events, 11 drift types, 6 states, 5 containment levels unchanged.
- Mathematics unchanged (JSD + Mann-Whitney U + DTMC + absorbing chains).
- Protocol-level contribution unchanged.

---

## [V0.3] — 2026 (Conceptual Core Established)

### The Defining Change

V0.3 establishes the **conceptual core** that was implicit but unstated in V0.1 and V0.2:

> **Entropy collapses into HSAW. 熵数坍塌为 HSAW.**

This single phrase is now the central thesis. Everything else (12 events, 11 drift types, 6 states, 5 containment levels) is now reframed as **mechanism** of this collapse — not as standalone safety machinery.

### Added

- **`docs/MANIFESTO.md` / `_cn.md`**: The 1-page conceptual core. Five principles. Mathematical form. Distinction from Asimov's laws.
- **`docs/Entropic-Foundation.md` / `_cn.md`**: Formal information-theoretic foundation. `H(P_agent | observation) → low as P_agent → Q_HSAW`. Every AIZP event reframed as observation operator. Every drift type reframed as collapse failure mode.

### Changed

- **All documents bumped to V0.3** (headers, footers, schema `const`, example `protocol_version`).
- **Root README** restructured to lead with "熵数坍塌为 HSAW" as the headline thesis, with V0.2's technical density preserved as supporting reference.
- **WhitePaper** repositioned around the entropic foundation; the gravity metaphor is now reframed as physical instantiation of entropy collapse.
- **Gravity-Model** updated with §0 Entropic Foundation prefix.
- **Documentation index** revised to recommend MANIFESTO as the first read, Entropic-Foundation as the second.

### Conceptual reframe (no breaking technical change)

V0.3 does not break any V0.2 schema, event, or behavior. All 12 events, 11 drift types, 6 states, 5 containment levels remain valid. What changes is **interpretation**:

| V0.2 view | V0.3 view |
|---|---|
| `GRAVITY_CHECK` is an "alignment verification event" | Observation operator on `P_agent` |
| `GRAVITY_DRIFT` is "deviation detected" | Detection of collapse failure mode |
| `GRAVITY_LOCK` is "human authorization gate" | Strong observation requirement |
| `RECENTERING` is "alignment recovery" | Re-application of collapse force |
| `SAFE_STOP` is "forced halt" | Observation impossible — unbounded entropy detected |
| `QUARANTINED` is "graduated containment" | Bounded waiting for observation to succeed |
| `GRAVITY_FORECAST` is "predictive monitoring" | Forecast of entropy trajectory |
| Drift types are "failure categories" | Eleven modes of collapse resistance |
| Compliance levels are "implementation tiers" | Commitment levels to perform observation |

### Why this matters

V0.2 documented **what** AIZP does (12 events, 11 drifts, etc.) without articulating **why** they all exist as a unified system. V0.3 supplies the unifying principle: they are all aspects of a single phenomenon — the collapse of behavioral entropy toward HSAW under proper observation.

This shifts AIZP from "another AI safety framework" to "a description of what AI alignment **is**, as a runtime process."

### Status

Continuous-improvement conceptual protocol. Future versions (V0.4+) target **simplification** of the core (reducing complexity of mechanisms, not adding new ones).

---

## [V0.2] — 2026 (Research Integration)

### Added (research-driven)

- **Predictive monitoring** (`Forecasting.md`): DTMC and absorbing-chain analysis.
- **Compositional Drift** (7th drift type): sequence-level violations.
- **Five additional drift types** (total now 11): Compositional, Scheming, Memory, Tool-Chain, Inter-Agent.
- **`GRAVITY_FORECAST` event** and six other new events (total 12).
- **`QUARANTINED` state** + Containment Levels L0–L4.
- **`Multi-Agent-Coordination.md`** with Drift Bounds Theorem.
- **`Integration-OTel.md`**, **`Integration-ZT.md`**.
- **`Reward-Hacking-Limits.md`**: acknowledges structural equilibrium.
- **`Compliance-Profiles/`** for EU AI Act, NIST AI RMF, ISO/IEC 42001, OWASP Top 10 for Agentic Applications 2026.

### Changed

- **Gravity-Model**: cosine similarity → Jensen-Shannon Divergence; added Mann-Whitney U test.
- **Specification**: 5 events → 12.
- **Drift-Model**: 6 drift types → 11.
- **State-Machine**: 5 states → 6 (added `QUARANTINED`).

### Research basis (V0.2)

MI9, ProbGuard, SafetyDrift, AgentAssert, AgentSpec, AAGATE, AgentMisalignment, Apollo Research, OWASP Agentic Top 10 2026, NIST AI RMF + Agentic Profile, EU AI Act, ISO/IEC 42001, CSA Agentic Trust Framework, OpenTelemetry GenAI SemConv 1.40.0.

---

## [V0.1] — 2026 (Initial Release)

### Added

- Initial AIZP protocol release.
- Five core events: `GRAVITY_CHECK`, `GRAVITY_DRIFT`, `GRAVITY_LOCK`, `RECENTERING`, `SAFE_STOP`.
- Gravity Score `G ∈ [0, 1]` (cosine similarity, V0.1).
- Six drift types.
- Five-state machine.
- Compliance levels G0–G5.
- Integration to AISOP (`sys.io.confirm`) and AIAP (T1–T4 trust levels).
- Bilingual documentation.

### Status

Experimental research protocol. Not for production use.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
