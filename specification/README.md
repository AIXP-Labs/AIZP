# AIZP Specification

**Version**: AIZP V0.6

This folder holds the **normative specification** and **machine-readable artifacts** of AIZP. The narrative documentation (philosophy, models, integrations) lives in [`../docs/`](../docs/README.md) (English) and [`../docs_cn/`](../docs_cn/README_cn.md) (中文).

| Artifact | File | Purpose |
|---|---|---|
| **Specification (EN)** | [AIZP_Protocol.md](AIZP_Protocol.md) | Normative events, schemas, state machine, conformance (RFC 2119) |
| **Specification (中文)** | [AIZP_Protocol_cn.md](AIZP_Protocol_cn.md) | Chinese translation |
| **Registry (EN)** | [registry.md](registry.md) | Canonical enum allocations — single source of truth |
| **Registry (中文)** | [registry_cn.md](registry_cn.md) | 枚举注册表 |
| **Protobuf IDL** | [proto/aizp.proto](proto/aizp.proto) | Language-neutral wire definition (12 events) |
| **Standards (EN)** | [standards/README.md](standards/README.md) | External standards AIZP references / aligns with |
| **Standards (中文)** | [standards/README_cn.md](standards/README_cn.md) | 标准对齐索引 |
| **JSON Schemas** | [`../schemas/`](../schemas/) | Authoritative event schemas (12) |
| **Examples** | [`../examples/`](../examples/) | Conformant event payloads (13 files, all 12 event types) |

## Authority order

When sources disagree, precedence is:

1. [registry.md](registry.md) — for enum values.
2. [`../schemas/`](../schemas/) — for event structure (authoritative wire format).
3. [AIZP_Protocol.md](AIZP_Protocol.md) — for normative semantics and conformance.
4. [proto/aizp.proto](proto/aizp.proto) — informative for non-JSON ecosystems; defers to the JSON Schemas where they differ.

The English Specification is normative; [AIZP_Protocol_cn.md](AIZP_Protocol_cn.md) is an informative translation.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
