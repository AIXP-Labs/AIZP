# 合规档案：ISO/IEC 42001 映射

**版本**：AIZP V0.6（新章节）
**ISO/IEC 42001:2023**：信息技术——人工智能——管理系统

本文档将 AIZP 映射到 ISO/IEC 42001，世界首个 AI 管理系统（AIMS）标准，自 2023 年起可认证，在 AI 合规领域的采用正在增长。

---

## 1. 为什么 ISO 42001 重要

ISO 42001 **自愿但可认证**（不同于强制性的 EU AI Act）。认证提供：

- 对监管员（Colorado AI Act、Texas TRAIGA）的可证明风险管理。
- 客户保证——企业买家对 ISO 42001 或基于 ISO 42001 的 AIUC-1 的采用正在增长。
- 内部 AI 治理框架。

采用轨迹（2026 年中）：ISO 42001 在 AI 合规领域的采用正在增长。

---

## 2. 逐条款映射

ISO 42001 结构类似 ISO 27001（安全）。下面是主要条款的映射。

### 2.1 第 4 条 — 组织上下文

| ISO 42001 4.x | AIZP 贡献 |
|---|---|
| 4.1 内部/外部上下文 | AIAP card 声明 + 治理合约 |
| 4.2 利益相关者需求 | HSAW 公理 0 + 每利益相关者引力权重 |
| 4.3 AIMS 范围 | 每 Agent AIZP 合规级别声明 |
| 4.4 AIMS 本身 | AIZP 事件日志 + 状态机 |

### 2.2 第 5 条 — 领导

| ISO 42001 5.x | AIZP 贡献 |
|---|---|
| 5.1 领导承诺 | 文档化 AIZP 采用 + 合规级别目标 |
| 5.2 AI 策略 | AIZP 配置（`aizp.config.yaml`）是运行时策略 |
| 5.3 角色与权限 | AIAP T1–T4 + Agentic AI 委员会（AIZP 建议的治理机构，合规档案 NIST AI RMF §2）|

### 2.3 第 6 条 — 规划

| ISO 42001 6.x | AIZP 贡献 |
|---|---|
| 6.1 风险与机会 | Threat-Model.md + OWASP-Agentic-Top10-Mapping.md |
| 6.2 AI 目标 | HSAW + 每 AIAP 声明 Agent 目标 |
| 6.3 AI 系统影响评估 | GRAVITY_CHECK 中的 `risk_level` 字段 |

### 2.4 第 7 条 — 支持

| ISO 42001 7.x | AIZP 贡献 |
|---|---|
| 7.1 资源 | Implementer-Guide §11（参考实现结构）|
| 7.2 能力 | 操作员培训 + FAQ |
| 7.4 沟通 | OTel 集成 → dashboard |
| 7.5 文档化信息 | AIZP_Protocol.md + 所有 docs/ |

### 2.5 第 8 条 — 运营

| ISO 42001 8.x | AIZP 贡献 |
|---|---|
| 8.1 运营规划 | 状态机 + 容器级别 |
| 8.2 AI 系统影响评估 | 每动作 GRAVITY_CHECK risk_level |
| 8.3 AI 生命周期 | 合规级别 G0 → G5 成熟度模型 |

### 2.6 第 9 条 — 绩效评估

| ISO 42001 9.x | AIZP 贡献 |
|---|---|
| 9.1 监控与测量 | 12 个 AIZP 事件 + OTel 指标 |
| 9.2 内部审计 | G4 — 可审计引力时间序列 |
| 9.3 管理审查 | 季度审查 SAFE_STOP + REWARD_HACK |

### 2.7 第 10 条 — 改进

| ISO 42001 10.x | AIZP 贡献 |
|---|---|
| 10.1 不符合与纠正措施 | 误报反馈循环（Drift-Model §6）|
| 10.2 持续改进 | 基线刷新 + 合规级别升级路径 |

---

## 3. 附件 A 控制（ISO 42001:2023 附件 A）

附件 A 定义 AI 管理的参考控制。ISO/IEC 42001:2023 附件 A 包含约 38 项控制，跨 9 个域（A.2–A.10），并要求适用性声明（Statement of Applicability）。所选映射：

| 附件 A 控制 | AIZP 实施 |
|---|---|
| A.2 AI 策略 | aizp.config.yaml + 治理文档 |
| A.3 内部组织 | Agentic AI 委员会 + AIAP T4 升级 |
| A.4 AI 系统资源 | 合规级别声明 |
| A.5 影响分析 | GRAVITY_CHECK risk_level + Threat-Model.md |
| A.6.2 AI 系统生命周期 | 容器级别转换反映生命周期阶段 |
| A.7 数据管理 | AIAP 治理哈希 + memory_quarantine |
| A.8 用户信息 | AIBP 消息披露 + Identity-Verification 事件 |
| A.9 AI 系统使用 | RECENTERING + SAFE_STOP 强制安全使用 |
| A.10 第三方关系 | AIBP / AILP 集成（由其他 AIXP 协议覆盖）|

---

## 4. 认证路径

寻求 ISO 42001 认证的部署：

| 步骤 | AIZP 角色 |
|---|---|
| 1. 建立 AIMS | 采用 AIZP G3+ |
| 2. 文档化策略 | aizp.config.yaml + 每 Agent AIAP card |
| 3. 风险评估 | 使用 Threat-Model.md + OWASP 档案 |
| 4. 控制实施 | AIZP 事件 + 容器级别 |
| 5. 监控与测量 | OTel 管道 + dashboard |
| 6. 内部审计 | G4 审计日志查询 |
| 7. 管理审查 | Agentic AI 委员会会议 |
| 8. 外部认证审计 | 提供 AIZP 合规报告 + 事件样本 |

---

## 5. AIUC-1 集成

**AIUC-1** 是一个独立的 Agent 标准，参考现行法规与框架，为 AI Agent 采用提供单一可审计框架。

G4+ 的 AIZP 满足 AIUC-1 的运行时监控部分。其他 AIUC-1 组件（训练数据、模型卡、组织策略）超出 AIZP 范围。

---

## 6. ISO 42001 成熟度建议 AIZP 级别

| ISO 42001 成熟度 | 推荐 AIZP 级别 |
|---|---|
| 初始（基础 AIMS）| G1 |
| 标准化 | G2 |
| 定义（完整 AIMS）| G3 |
| 量化管理 | G4 |
| 优化 | G5 |

---

## 7. 参考

- ISO/IEC 42001:2023 — 信息技术——人工智能——管理系统。iso.org。
- ISO 42001 实施指南 — aigl.blog。
- Schellman、A-LIGN、BSI、Deloitte 2026 ISO 42001 指南。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
