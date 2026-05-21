# ADR-009: Decouple the Wire-Format Version from the Release Version

## Status

Accepted (V0.6) — implemented pre-publication. Because AIZP has no released consumers yet, the breaking rename costs nothing now and avoids breaking real code later; this is the cheapest possible moment to land it.

## Context

The protocol carries a single version string, `protocol_version`, currently `"V0.6"`. This same string is burned into two machine-facing identifiers:

- the Protobuf package — `package aizp.v0_6;` (and `go_package`/`java_package` derived from it), in [`proto/aizp.proto`](../specification/proto/aizp.proto);
- the JSON Schema `$id` paths — `https://aizp.dev/schemas/V0.6/<event>.schema.json`, in [`../schemas/`](../schemas/).

But [`AIZP_Protocol.md`](../specification/AIZP_Protocol.md) §17 establishes that the **wire format has been frozen since V0.2**: releases V0.3–V0.6 add only documentation and philosophy, with an *identical* envelope, event vocabulary (12), drift types (11), state machine (6), and schemas. The spec explicitly states a V0.6 implementation interoperates with any V0.2+ peer.

This creates a contradiction. Each documentation-only release (V0.6 → V0.7 → …) will, under the current scheme, change:

- the generated Protobuf namespace (`aizp.v0_6` → `aizp.v0_7`), forcing a recompile and import churn for every gRPC/Go/Java/Rust consumer, even though no field changed;
- every schema `$id` URL, breaking any `$ref` or registry that pinned the V0.6 URL.

In other words, an artifact that is byte-for-byte identical across releases is given a new identity each release — the opposite of what a frozen wire format should guarantee.

## Decision

Separate the **wire-format version** (changes only on a wire-incompatible change) from the **release version** (`protocol_version`, the human-facing marketing/doc version). As implemented in V0.6:

1. **Protobuf package** — pinned to the wire generation, not the release: `package aizp.wire2;` (frozen since V0.2), with `go_package`/`java_package` following (`aizpwire2` / `dev.aizp.wire2`). Bumps only when the wire format actually changes.
2. **Schema `$id`** — wire-stable path: `https://aizp.dev/schemas/wire-2/<event>.schema.json`. The human-readable `title` still names the current release.
3. **Envelope** — `protocol_version` stays the release string (`"V0.6"`) for humans and audit; the normative compatibility contract is the new `wire_version` field (integer `2`). It is `SHOULD` (additive), so pre-ADR-009 V0.2 senders that omit it are treated as `wire_version` 2.

This was wire-affecting, so it was taken as a one-time breaking correction landed *before* publication (no released consumers exist). A guard test (`test_wire_identifiers_are_release_independent`) keeps the package/`$id` from re-acquiring a release-version label.

## Alternatives considered

- **Status quo (couple everything to `protocol_version`).** Simple, but guarantees recurring namespace/URL churn on every doc-only release and contradicts the §17 freeze claim.
- **Freeze the identifiers at `V0.2` forever.** Honest to the freeze, but `aizp.v0_2` / `/schemas/V0.2/` reads as stale to newcomers who see "V0.6" everywhere else.
- **Wire version + release version (recommended).** One extra concept, but it makes the freeze guarantee real and the identifiers honest.

## Consequences

### What becomes easier

- A frozen wire artifact keeps one stable identity; consumers pinned to `wire-2` never recompile for a doc release.
- The §17 "interoperates with any V0.2+ peer" claim becomes literally true at the identifier level, not just conceptually.

### What becomes harder

- One more version concept to explain (wire vs release) in the spec and onboarding docs.
- The transition itself is breaking (package + `$id` rename), so it must be scheduled deliberately and called out in [CHANGELOG.md](../CHANGELOG.md).

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
