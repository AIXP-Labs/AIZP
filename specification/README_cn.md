# AIZP 规范

**版本**：AIZP V0.6

本文件夹存放 AIZP 的**规范性规范**与**机器可读工件**。叙述性文档（哲学、模型、集成）位于 [`../docs/`](../docs/README.md)（英文）与 [`../docs_cn/`](../docs_cn/README_cn.md)（中文）。

| 工件 | 文件 | 用途 |
|---|---|---|
| **规范（英文）** | [AIZP_Protocol.md](AIZP_Protocol.md) | 规范性事件、schema、状态机、合规（RFC 2119）|
| **规范（中文）** | [AIZP_Protocol_cn.md](AIZP_Protocol_cn.md) | 中文翻译 |
| **注册表（英文）** | [registry.md](registry.md) | 规范性枚举分配——单一权威来源 |
| **注册表（中文）** | [registry_cn.md](registry_cn.md) | 枚举注册表 |
| **Protobuf IDL** | [proto/aizp.proto](proto/aizp.proto) | 语言中立 wire 定义（12 事件）|
| **标准（英文）** | [standards/README.md](standards/README.md) | AIZP 引用/对齐的外部标准 |
| **标准（中文）** | [standards/README_cn.md](standards/README_cn.md) | 标准对齐索引 |
| **JSON Schema** | [`../schemas/`](../schemas/) | 权威事件 schema（12）|
| **示例** | [`../examples/`](../examples/) | 合规事件载荷（13 文件，覆盖全部 12 事件类型）|

## 权威顺序

来源冲突时，优先级为：

1. [registry_cn.md](registry_cn.md) — 枚举值。
2. [`../schemas/`](../schemas/) — 事件结构（权威 wire 格式）。
3. [AIZP_Protocol_cn.md](AIZP_Protocol_cn.md) — 规范性语义与合规。
4. [proto/aizp.proto](proto/aizp.proto) — 非 JSON 生态的信息性参考；与 JSON Schema 不一致时以后者为准。

英文规范为规范性；[AIZP_Protocol_cn.md](AIZP_Protocol_cn.md) 是信息性翻译。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
