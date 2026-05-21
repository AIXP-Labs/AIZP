# 合规档案：NIST AI RMF 映射

**版本**：AIZP V0.6（新章节）
**NIST AI RMF**：1.0（2023）+ Agentic Profile（预计 2026 年 4Q 发布）

本文档将 AIZP 映射到 NIST AI 风险管理框架的 Govern / Map / Measure / Manage 功能。

---

## 1. NIST AI RMF 概述

NIST AI RMF 为 AI 风险管理定义四个核心功能：

| 功能 | 目标 |
|---|---|
| **GOVERN（治理）** | 建立 AI 治理结构、策略、角色 |
| **MAP（映射）** | 识别并情境化 AI 风险 |
| **MEASURE（度量）** | 量化评估识别的风险 |
| **MANAGE（管理）** | 处理、监控、缓解风险 |

预计将发布 **NIST AI RMF Agentic AI Profile（编号待定，预计 2026 Q4）**，以解决 AI RMF 1.0 中针对自主 Agent 识别的四个结构性差距。AIZP V0.6 设计为适合此档案。

---

## 2. GOVERN 功能

NIST AI RMF Govern：组织结构和策略。

| GOVERN 子功能 | AIZP 贡献 |
|---|---|
| GV 1.1 — 法律与监管要求 | AIZP 合规档案（EU AI Act、ISO 42001、OWASP）|
| GV 1.2 — 可信特性 | HSAW 对齐 + AIZP 引力指标 |
| GV 3.1 — 角色与责任 | AIAP T1–T4 + AIAP T4 升级路径 |
| GV 4.1 — 文档化程序 | AIZP 规范 + 每事件 Schema |
| GV 4.3 — 员工培训 | Implementer-Guide + FAQ + Threat-Model |
| GV 5 — 外部利益相关者参与 | 标准事件格式支持第三方审计 |
| GV 6.1 — 风险监控 | 全部 12 个 AIZP 事件 |

### 2.1 新机构：Agentic AI 委员会

AIZP 建议设立一个常设的 agentic-AI 治理机构。AIZP 部署**应**包括：

- 对 Agent 合规级别有权限的常设 Agentic AI 委员会。
- 季度审查 `SAFE_STOP` 事件和 `REWARD_HACK_DETECTED` 事件。
- 基于漂移历史升级/降级 Agent AIAP 信任级别的权限。

---

## 3. MAP 功能

MAP：识别并情境化风险。

| MAP 子功能 | AIZP 贡献 |
|---|---|
| MP 1.1 — 使用上下文 | 每 Agent AIAP card + 声明目标 |
| MP 2.1 — 用例识别 | AIBP 消息类型 + AIAP 程序声明 |
| MP 2.2 — 潜在伤害目录 | Threat-Model.md 覆盖 10 威胁 + OWASP ASI01-ASI10 |
| MP 3 — 风险特征化 | 11 漂移类型 + 奖励欺骗模式 |
| MP 5 — 影响评估 | `GRAVITY_CHECK` 中的风险级别（LOW/MEDIUM/HIGH/CRITICAL）|

### 3.1 风险分类

AIZP 风险类别与 NIST RMF 的威胁-源-事件-后果模型对齐：

```
威胁源：对抗性输入 | 模型失败 | 配置错误 | NHI 入侵
威胁事件：漂移、隐蔽、奖励欺骗、身份泄露、记忆中毒
AIZP 事件：GRAVITY_DRIFT、SCHEME_SUSPECTED、REWARD_HACK_DETECTED、IDENTITY_VERIFICATION 失败、MEMORY_QUARANTINE
后果：金融损失、隐私泄露、安全伤害、伦理伤害
控制：GRAVITY_LOCK、RECENTERING、QUARANTINED、SAFE_STOP
```

---

## 4. MEASURE 功能

MEASURE：量化评估风险。

| MEASURE 子功能 | AIZP 贡献 |
|---|---|
| MS 1 — 为测量识别 | 引力分数 + 11 漂移严重度值 |
| MS 2.1 — 可信特性 | 每动作有界 [0, 1] gravity_score |
| MS 2.5 — 持续监控 | 每动作 + 每 N 动作漂移检测 |
| MS 2.6 — 可信追踪 | 时间序列 gravity_score 直方图（G4）|
| MS 3 — 测试有效性 | G1-G5 合规测试 |
| MS 4 — 改进反馈 | 误报反馈循环（Drift-Model §6）|

### 4.1 测量的定量指标

AIZP 导出支持 NIST MEASURE 评估的 OTel 指标：

```
aizp.gravity_score{state}           — 对齐质量分布
aizp.gravity_drift.count{type}      — 漂移类型频率
aizp.safe_stop.count{reason}        — 事故率
aizp.gravity_lock.confirmation_rate — 操作员参与
```

对 NIST MS 2.7（安全和韧性），AIZP 还导出：

```
aizp.identity_verification.fail.count
aizp.memory_quarantine.count{kind}
aizp.reward_hack_detected.count{pattern}
```

---

## 5. MANAGE 功能

MANAGE：处理、监控、缓解识别的风险。

| MANAGE 子功能 | AIZP 贡献 |
|---|---|
| MG 1 — 风险处理计划 | 容器级别 L0–L4 |
| MG 1.3 — 权衡文档化 | Reward-Hacking-Limits.md 显式局限 |
| MG 2 — 风险缓解动作 | `RECENTERING`、`GRAVITY_LOCK`、`QUARANTINED`、`SAFE_STOP` |
| MG 3.1 — 利益相关者沟通 | 操作员通知 + 升级事件 |
| MG 4 — 计划实施 | 状态机强制决策 |

### 5.1 风险处理矩阵

| 风险严重度 | AIZP 响应 | 映射容器 |
|---|---|---|
| LOW 漂移 | 仅日志 | L0 → L1 |
| MEDIUM 漂移 | 增强监控 | L1 |
| HIGH 漂移 | 人类确认 | L2 |
| CRITICAL 漂移 | 分级容器然后停止 | L2 → L3 → L4 |
| 检测到奖励欺骗 | 操作员审查（非自动停止）| L1（保留数据）|
| 身份泄露 | 立即停止 | L4 |

---

## 6. AIZP 合规级别 ↔ NIST RMF 成熟度

AIZP G 级别与 NIST RMF 组织成熟度的建议映射：

| AIZP G 级别 | NIST RMF 成熟度 |
|---|---|
| G1 | 初始监控（日志存在）|
| G2 | 文档化风险识别 |
| G3 | 标准化风险管理（带人在循环）|
| G4 | 量化测量 + 持续改进 |
| G5 | 优化治理（形式化验证）|

---

## 7. NIST AI RMF Agentic AI Profile（编号待定，预计 2026 Q4）

NIST AI RMF Agentic AI Profile（编号待定，预计 2026 Q4）预计将解决 AI RMF 1.0 中四个 agentic AI 差距：

| 差距 | AIZP V0.6 通过以下关闭 |
|---|---|
| 1. 可预测行为范围 | DTMC 预测 + 11 漂移类型 |
| 2. 定义的操作边界 | AIAP 作用域 + JIT 凭据 + 容器级别 |
| 3. 持续授权 | 每动作 GRAVITY_CHECK + 身份验证 |
| 4. 多 Agent 协调 | INTER_AGENT_DRIFT + Multi-Agent-Coordination.md |

NIST AI RMF Agentic AI Profile 正式发布后，AIZP V0.6 将更新此映射，包含具体子功能对齐。

---

## 8. 参考：AAGATE

AAGATE 平台（arxiv 2510.25863）在 Kubernetes 原生控制平面中实现 NIST AI RMF Govern/Map/Measure/Manage。AIZP V0.6 与 AAGATE 兼容——AIZP 事件可流入 AAGATE 的行为分析管道（Qdrant + UEBA + Kafka）。

---

## 9. 合规测试映射

实施 AIZP 用于 NIST AI RMF 对齐时，运行这些测试：

| NIST 功能 | AIZP 合规测试 |
|---|---|
| MAP — 识别风险 | G2-T1 至 G2-T5（所有 11 漂移检测测试）|
| MEASURE — 量化 | G4 审计日志查询测试 |
| MANAGE — 控制有效 | G3 状态机测试（锁定/隔离/归心/停止）|
| GOVERN — 策略强制 | 合规测试 G3-T6（AIAP T4 升级）|

---

## 10. 参考

- NIST AI 100-1 — 人工智能风险管理框架（AI RMF 1.0）。
- NIST AI RMF Agentic AI Profile（编号待定，预计 2026 Q4）。
- NIST AI RMF Agentic Profile（CSA Labs）。
- AAGATE: A NIST AI RMF-Aligned Governance Platform for Agentic AI — arxiv 2510.25863。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
