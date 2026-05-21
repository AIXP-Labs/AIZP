# AIZP Conformance Tests

Minimal test layer that turns AIZP from a "conceptual protocol" into a
**verifiable** one. Five groups:

1. **Schema validation** — every file in `examples/` is validated against the
   schema in `schemas/` whose `event` const matches the example's `event`
   field. Also checks `protocol_version == "V0.6"`.
2. **Gravity Score** — reproduces the worked example in
   [`docs/Gravity-Model.md`](../docs/Gravity-Model.md) §5
   (expected `G = 0.674` → `DRIFT_WARNING`) and verifies the threshold bands
   and the recency-decay formula `H = exp(-Δt/τ)`.
3. **Deployment config schema** — validates `examples/config/deployment.example.json`
   against `schemas/aizp-config.schema.json`, plus the cross-field invariants the
   schema cannot express (weights sum to 1.0; threshold bands strictly descending).
4. **Version-narrative hygiene** — guards against stale present-tense version
   narrative in normative/doc files and version labels in example `_description`s.
5. **Cross-artifact integrity** — registry ↔ schemas ↔ proto ↔ examples enum
   alignment and release-independent wire identifiers.

## Requirements

```bash
pip install jsonschema    # ≥ 4.0
# pytest is optional (the runner also works standalone)
```

## Run

```bash
# standalone (no pytest needed)
python tests/test_aizp.py

# or with pytest
pytest tests/
```

## What is NOT covered (honest scope)

These tests verify **structural** conformance (schema shape, arithmetic of the
documented example), not **semantic** correctness of alignment. Per
[`docs/Reward-Hacking-Limits.md`](../docs/Reward-Hacking-Limits.md), no test
suite can certify that an agent is aligned — only that its event payloads are
well-formed and the scoring arithmetic matches the specification.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
