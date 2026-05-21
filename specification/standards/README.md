# AIZP Standards Alignment

**Version**: AIZP V0.6

This index lists the external standards that AIZP **normatively references** or **aligns with**, each with its role in the protocol and a pointer to the relevant AIZP document. AIZP does not reinvent these standards; it composes with them.

> Normative language ("MUST", "SHOULD", "MAY") follows **RFC 2119**. The authoritative AIZP wire definition is [AIZP_Protocol.md](../AIZP_Protocol.md), with machine formats in [`../proto/aizp.proto`](../proto/aizp.proto) and [`../../schemas/`](../../schemas/). Canonical enums are in [registry.md](../registry.md).

---

## 1. Normative references

| Standard | Role in AIZP | AIZP document |
|---|---|---|
| **RFC 2119 / RFC 8174** | Conformance keywords (MUST/SHOULD/MAY) | [AIZP_Protocol.md](../AIZP_Protocol.md) |
| **RFC 3339** | Event `timestamp` format (UTC) | [AIZP_Protocol.md](../AIZP_Protocol.md) §1 |
| **RFC 4122 (UUIDv4)** | `event_id` format | [AIZP_Protocol.md](../AIZP_Protocol.md) §1 |
| **JSON Schema 2020-12** | Authoritative event schemas | [`../../schemas/`](../../schemas/) |
| **Protocol Buffers (proto3)** | Language-neutral wire IDL | [`../proto/aizp.proto`](../proto/aizp.proto) |

---

## 2. Identity & trust standards

| Standard | Role | AIZP document |
|---|---|---|
| **W3C DID v1.0 (Recommendation; v1.1 in Candidate Recommendation, 2026-03)** | `IDENTITY_VERIFICATION` proof method | [Integration-ZT.md](../../docs/Integration-ZT.md) |
| **OAuth 2.1 / JWT** | JIT credential carrier | [Integration-ZT.md](../../docs/Integration-ZT.md) |
| **AIP — Agent Identity Protocol (IBCT)** (arxiv 2603.24775) | Verifiable delegation, attenuated authority | [Integration-ZT.md](../../docs/Integration-ZT.md) §8.5 |

---

## 3. Observability standards

| Standard | Role | AIZP document |
|---|---|---|
| **OpenTelemetry GenAI Semantic Conventions** | `aizp.*` span/event mapping (custom namespace; OTel `gen_ai.*` used only for official attributes) | [Integration-OTel.md](../../docs/Integration-OTel.md) |

---

## 4. Agent ecosystem standards (external interop)

| Standard | Role | AIZP document |
|---|---|---|
| **MCP — Model Context Protocol** | Tool-call boundary scored by `GRAVITY_CHECK` | [Integration-MCP.md](../../docs/Integration-MCP.md) |
| **A2A — Agent-to-Agent** (Linux Foundation project since 2025-06; ACP merge announced 2025-09) | Delegation boundary scored by `INTER_AGENT_DRIFT` | [Integration-A2A.md](../../docs/Integration-A2A.md) |

---

## 5. Security & risk frameworks

| Framework | Role | AIZP document |
|---|---|---|
| **OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10)** | Threat taxonomy alignment | [OWASP-Agentic-Top10-Mapping.md](../../docs/Compliance-Profiles/OWASP-Agentic-Top10-Mapping.md) |
| **EU AI Act** (Annex III high-risk; effective 2026-08-02) | Art 12 logging / Art 14 oversight | [EU-AI-Act-Mapping.md](../../docs/Compliance-Profiles/EU-AI-Act-Mapping.md) |
| **NIST AI RMF** | Govern/Map/Measure/Manage | [NIST-AI-RMF-Mapping.md](../../docs/Compliance-Profiles/NIST-AI-RMF-Mapping.md) |
| **ISO/IEC 42001 (AIMS)** | Management-system clauses | [ISO-42001-Mapping.md](../../docs/Compliance-Profiles/ISO-42001-Mapping.md) |

---

## 6. Honest note

Standards text changes faster than this protocol. The mappings above are pointers; verify the current standard before relying on them. Regulatory regimes in flux (e.g., Colorado AI Act) are documented in the relevant compliance profile rather than asserted here.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
