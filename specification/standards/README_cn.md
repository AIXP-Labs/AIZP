# AIZP 标准对齐

**版本**：AIZP V0.6

本索引列出 AIZP **规范性引用**或**对齐**的外部标准，各自在协议中的角色与相关 AIZP 文档指针。AIZP 不重造这些标准；它与之组合。

> 规范性语言（"MUST"、"SHOULD"、"MAY"）遵循 **RFC 2119**。AIZP 的权威 wire 定义是 [AIZP_Protocol_cn.md](../AIZP_Protocol_cn.md)，机器格式见 [`../proto/aizp.proto`](../proto/aizp.proto) 与 [`../../schemas/`](../../schemas/)。规范性枚举见 [registry_cn.md](../registry_cn.md)。

---

## 1. 规范性引用

| 标准 | 在 AIZP 中的角色 | AIZP 文档 |
|---|---|---|
| **RFC 2119 / RFC 8174** | 合规关键词（MUST/SHOULD/MAY）| [AIZP_Protocol_cn.md](../AIZP_Protocol_cn.md) |
| **RFC 3339** | 事件 `timestamp` 格式（UTC）| [AIZP_Protocol_cn.md](../AIZP_Protocol_cn.md) §1 |
| **RFC 4122（UUIDv4）** | `event_id` 格式 | [AIZP_Protocol_cn.md](../AIZP_Protocol_cn.md) §1 |
| **JSON Schema 2020-12** | 权威事件 schema | [`../../schemas/`](../../schemas/) |
| **Protocol Buffers（proto3）** | 语言中立 wire IDL | [`../proto/aizp.proto`](../proto/aizp.proto) |

---

## 2. 身份与信任标准

| 标准 | 角色 | AIZP 文档 |
|---|---|---|
| **W3C DID v1.0（推荐标准；v1.1 已于 2026-03 进入候选推荐 Candidate Recommendation）** | `IDENTITY_VERIFICATION` 证明方法 | [Integration-ZT_cn.md](../../docs_cn/Integration-ZT_cn.md) |
| **OAuth 2.1 / JWT** | JIT 凭据载体 | [Integration-ZT_cn.md](../../docs_cn/Integration-ZT_cn.md) |
| **AIP — Agent Identity Protocol（IBCT）**（arxiv 2603.24775）| 可验证委托、衰减授权 | [Integration-ZT_cn.md](../../docs_cn/Integration-ZT_cn.md) §8.5 |

---

## 3. 可观测性标准

| 标准 | 角色 | AIZP 文档 |
|---|---|---|
| **OpenTelemetry GenAI 语义约定** | `aizp.*` span/event 映射（自定义命名空间；OTel `gen_ai.*` 仅用于官方属性）| [Integration-OTel_cn.md](../../docs_cn/Integration-OTel_cn.md) |

---

## 4. Agent 生态标准（外部互操作）

| 标准 | 角色 | AIZP 文档 |
|---|---|---|
| **MCP — 模型上下文协议** | 工具调用边界由 `GRAVITY_CHECK` 打分 | [Integration-MCP_cn.md](../../docs_cn/Integration-MCP_cn.md) |
| **A2A — 智能体间协议**（自 2025-06 起为 Linux Foundation 项目；ACP 并入于 2025-09 宣布）| 委托边界由 `INTER_AGENT_DRIFT` 打分 | [Integration-A2A_cn.md](../../docs_cn/Integration-A2A_cn.md) |

---

## 5. 安全与风险框架

| 框架 | 角色 | AIZP 文档 |
|---|---|---|
| **OWASP Top 10 for Agentic Applications 2026（ASI01–ASI10）** | 威胁分类对齐 | [OWASP-Agentic-Top10-Mapping_cn.md](../../docs_cn/Compliance-Profiles/OWASP-Agentic-Top10-Mapping_cn.md) |
| **EU AI Act**（Annex III 高风险；2026-08-02 生效）| Art 12 日志 / Art 14 监督 | [EU-AI-Act-Mapping_cn.md](../../docs_cn/Compliance-Profiles/EU-AI-Act-Mapping_cn.md) |
| **NIST AI RMF** | Govern/Map/Measure/Manage | [NIST-AI-RMF-Mapping_cn.md](../../docs_cn/Compliance-Profiles/NIST-AI-RMF-Mapping_cn.md) |
| **ISO/IEC 42001（AIMS）** | 管理体系条款 | [ISO-42001-Mapping_cn.md](../../docs_cn/Compliance-Profiles/ISO-42001-Mapping_cn.md) |

---

## 6. 诚实说明

标准文本变化快于本协议。以上映射是指针；依赖前请核实当前标准。处于变动中的监管（如 Colorado AI Act）记录在相关合规档案中，而非在此断言。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
