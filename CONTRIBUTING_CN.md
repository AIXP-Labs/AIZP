# 如何贡献 AIZP

感谢您有兴趣为 AI 逻辑重心引力协议（AI Zenith-Zero Protocol）做出贡献！本文档提供贡献指南。

> ⚠️ **当前阶段的贡献政策**
>
> 我们欢迎通过 **GitHub Issues 进行讨论**。
>
> **当前不接受外部 Pull Request。** 如果您有任何建议 — bug 报告、功能想法、规范澄清，或新的漂移类型/威胁 — 请通过 Issue 描述。如果我们认为有价值，由维护者实现并在 commit/release notes 中署名感谢您。
>
> 此政策未来会重新审视。

> **阶段状态（V0.6）**
>
> AIZP 是持续改进中的实验性概念协议。下方流程描述的是**目标**治理模型。初期决策由 AIXP Labs 核心维护者做出；社区讨论窗口将随贡献者基数增长而扩大。

## 如何贡献

### 报告 Issue

- 使用 [GitHub Issues](https://github.com/AIXP-Labs/AIZP/issues) 报告 bug、提议功能或建议规范变更。
- 规范变更请使用 `spec-change` 标签。
- 提供清晰描述，尽可能附带示例。

### 讨论驱动开发

请勿直接提交 PR，而是：

1. **打开 Issue**，描述您的提议、Bug 或想法。
2. **与维护者讨论** — 明确范围、设计和方法。
3. **等待审查** — 重大提议遵循下方[规范变更](#规范变更)流程。
4. **若被接受**，由维护者实现并在 commit/release notes 中署名感谢。

### 规范变更

影响规范性内容（`specification/`、`schemas/` 或注册表）的提议遵循：

1. 带 `spec-change` 标签、描述变更的 Issue。
2. 非平凡变更至少 14 天讨论期（目标治理模型；当前窗口随贡献者数缩放）。
3. 重大决策在 [`adrs/`](adrs/) 写架构决策记录（ADR）。
4. 维护者做 **Axiom 0 合规审查**（是否保持 HSAW 为不可移动的引力中心？）。
5. 更新文档，及相关的[枚举注册表](specification/registry_cn.md)、JSON Schema、`proto/aizp.proto`。

### 引用真实性

AIZP 引用外部研究（arxiv 论文、标准、框架）。**每个引用必须可核实。** 不得添加未经核实的作者姓名、arxiv 编号或"X 证明 Y"式陈述。无法核实的将被拒绝或改写为"受启发 / 假设"。

### 文档变更

非规范性内容（`docs/`、`docs_cn/`）的建议欢迎通过 Issue 提出 — 尤其欢迎错别字修正、澄清和补充示例。英文（`docs/`）与中文（`docs_cn/`）版本应保持对位。

## 写作指南

### RFC 2119 关键词

撰写规范性文本时使用 [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) 关键词：

- **MUST** / **MUST NOT** — 绝对要求
- **SHOULD** / **SHOULD NOT** — 有文档化例外的强烈建议
- **MAY** — 真正可选的行为

在规范意义上使用时这些关键词必须大写。

### 术语

- 12 个受治理事件用确切名称（`GRAVITY_CHECK` 等）。
- **"Axiom 0"** 大写（专有名词）；HSAW 称为**引力中心**。
- 漂移类型用大写蛇形（`INTENT_DRIFT`）；状态同理（`STABLE_ORBIT`）。
- 信任级别写 "T1"–"T4"；容器 "L0"–"L4"；合规 "G0"–"G5"。
- 以[枚举注册表](specification/registry_cn.md)为这些值的单一权威来源。

### 文档结构

- 每个文档以一段引言和 `**版本**：` 头部开始。
- 字段规范用表格；示例用带语言标注的代码块。
- 文档间用相对链接交叉引用（注意 `docs/` ↔ `specification/` ↔ 根 的深度）。

### 结尾印

所有规范与文档文件以此结尾：

```
Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
```

## 行为准则

所有贡献者须遵守[行为准则](CODE_OF_CONDUCT.md)。Axiom 0 誓约适用于所有贡献。

## 贡献许可

提交 Issue 或任何内容（包括规范提议、代码片段或设计建议）即表示您同意您提交的内容可由维护者在 [Apache License 2.0](LICENSE)（与本项目相同许可）条款下使用。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
