# Contributing to AIZP

Thank you for your interest in contributing to the AI Zenith-Zero Protocol (Logic Gravity-Center Protocol)! This document provides guidelines for contributing.

> ⚠️ **Contribution Status (Current Stage)**
>
> We welcome **discussion through GitHub Issues** at this stage of development.
>
> **External Pull Requests are not currently accepted.** If you have a proposal — bug report, feature idea, specification clarification, or a new drift type / threat — please open an issue describing it. If we agree it adds value, maintainers will implement it and credit you.
>
> This policy may be revisited in the future.

> **Stage Status (V0.6)**
>
> AIZP is an experimental, conceptual protocol under continuous improvement. The processes below describe the *target* governance model. Initial decisions are made by AIXP Labs core maintainers; the community discussion period scales as the contributor base grows.

## How to Contribute

### Reporting Issues

- Use [GitHub Issues](https://github.com/AIXP-Labs/AIZP/issues) to report bugs, suggest features, or propose specification changes.
- For specification changes, use the `spec-change` issue label.
- Provide clear descriptions with examples where possible.

### Discussion-Driven Development

Instead of submitting PRs directly:

1. **Open an issue** describing your proposal, bug, or idea.
2. **Discuss** with maintainers — clarify scope, design, and approach.
3. **Wait for review** — significant proposals follow the [Specification Changes](#specification-changes) process below.
4. **If accepted**, maintainers will implement the change and credit you in commit/release notes.

### Specification Changes

Proposals affecting normative content (anything in `specification/`, `schemas/`, or the registry) follow this process:

1. An issue with the `spec-change` label describing the proposed change.
2. A minimum 14-day discussion period for non-trivial changes (target governance model; current windows scale with contributor count).
3. An Architecture Decision Record (ADR) in [`adrs/`](adrs/) for significant decisions.
4. **Axiom 0 compliance review** by maintainers (does it preserve HSAW as the immovable gravity center?).
5. Updated documentation and, where relevant, the [enum registry](specification/registry.md), JSON Schemas, and `proto/aizp.proto`.

### Citation Integrity

AIZP cites external research (arxiv papers, standards, frameworks). **Every citation MUST be verifiable.** Do not add author names, arxiv IDs, or "X proves Y" claims unless confirmed against the actual source. Unverifiable claims will be rejected or reworded as "inspired by / hypothesis".

### Documentation Changes

Suggestions for non-normative content (`docs/`, `docs_cn/`) are welcome via issues — typo fixes, clarifications, and additional examples are particularly valued. English (`docs/`) and Chinese (`docs_cn/`) versions should be kept in parity.

## Writing Guidelines

### RFC 2119 Keywords

When writing normative specification text, use the keywords from [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119):

- **MUST** / **MUST NOT** — Absolute requirements
- **SHOULD** / **SHOULD NOT** — Strong recommendations with documented exceptions
- **MAY** — Truly optional behavior

These keywords MUST be capitalized when used in their normative sense.

### Terminology

- Use "AIZP event" for the 12 governed event types; use the exact event names (`GRAVITY_CHECK`, etc.).
- Capitalize **"Axiom 0"** (it is a proper noun) and refer to HSAW as the **gravity center**.
- Write drift types in UPPER_SNAKE (`INTENT_DRIFT`); states likewise (`STABLE_ORBIT`).
- Write trust levels as "T1"–"T4"; containment as "L0"–"L4"; compliance as "G0"–"G5".
- Treat the [enum registry](specification/registry.md) as the single source of truth for these values.

### Document Structure

- Begin each document with a one-paragraph introduction and a `**Version**:` header.
- Use tables for field specifications; code blocks with language annotations for examples.
- Cross-reference between documents using relative links (mind the `docs/` ↔ `specification/` ↔ root depth).

### Closing Seal

All specification and documentation files end with:

```
Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
```

## Code of Conduct

All contributors must follow our [Code of Conduct](CODE_OF_CONDUCT.md). The Axiom 0 pledge applies to all contributions.

## License of Contributions

By submitting an issue or any other content (including specification proposals, code snippets, or design suggestions), you agree that your submitted content may be used by maintainers under the terms of the [Apache License 2.0](LICENSE), the same license as the project.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
