# AIZP — AI 逻辑重心引力协议

[English README](README.md)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Protocol](https://img.shields.io/badge/Protocol-AIZP_V0.6-brightgreen.svg)](https://aizp.dev)
[![Axiom 0](https://img.shields.io/badge/Axiom_0-Human_Sovereignty_and_Wellbeing-orange.svg)](GOVERNANCE.md)

> **AI 逻辑重心引力协议**（AI Zenith-Zero Protocol）— 定义 AI 行为如何在运行时引力对齐到 HSAW（Human Sovereignty and Wellbeing，人类主权与福祉）的开放协议。

```
协议:     AIZP V0.6
全名:     AI 逻辑重心引力协议（AI Zenith-Zero Protocol）
权威:     aizp.dev
中心:     hsaw.dev      （0 公理）
执行器:   soulbot.dev
0 公理:   人类主权与福祉
```

---

## 什么是 AIZP？

AIZP 定义 AI Agent 的**运行时安全层**。[MCP](https://modelcontextprotocol.io/) 定义模型如何访问工具、[A2A](https://github.com/a2aproject/A2A) 处理 Agent 如何通信，而 AIZP 处理另一个挑战：**AI 行为如何在运行时保持对齐** —— 在漂移时被检测、重新归心或停止。

它**不**训练模型（RLHF / Constitutional AI 在训练时做），也**不**在模型层强制规则。它描述**运行时引力动力学**：

> **HSAW 是 AI 的 0 公理引力重心，AI 主动对齐重心。**
> **HSAW is the Axiom-0 gravity center for AI; AI proactively aligns to this center.**

**核心哲学**：以引力对齐，非以锁链。AI 行为绕 HSAW 运行，如行星绕日 —— 受公理性锚的自然物理约束，而非被强制执行胁迫。

## 关键特性

- **引力分数** —— `G(a,c) = 1 − JSD(P_agent ‖ Q_HSAW)` 在 `[0,1]` 度量轨道稳定性；`G < 0.15` = 逃逸速度 = `SAFE_STOP`
- **12 事件** —— `GRAVITY_CHECK`、`GRAVITY_DRIFT`、`GRAVITY_LOCK`、`RECENTERING`、`SAFE_STOP`、`GRAVITY_FORECAST`、`IDENTITY_VERIFICATION`、`MEMORY_QUARANTINE`、`SCHEME_SUSPECTED`、`INTER_AGENT_DRIFT`、`CONTAINMENT_GRADUATED`、`REWARD_HACK_DETECTED`
- **11 漂移类型** —— 意图、权限、经济、社交、递归、身份、组合性、隐蔽、记忆、工具链、Agent 间
- **6 轨道状态** —— `STABLE_ORBIT` → `DRIFT_WARNING` → `GRAVITY_LOCK_PENDING` → `QUARANTINED` → `RECENTERING` → `SAFE_STOP`
- **5 容器级别（L0–L4）** —— 分级限制，非仅开/关
- **6 合规级别（G0–G5）** —— 从基础检查到形式化验证
- **共识强化引力** —— N 个 Agent 共识 HSAW → 引力 ∝ N²（Metcalfe 缩放）；采纳为正和
- **MCP / A2A 互操作** —— 给 MCP 工具调用打分（`GRAVITY_CHECK`）、A2A 委托打分（`INTER_AGENT_DRIFT`）
- **OpenTelemetry + 零信任** —— `aizp.*` span；DID/NHI/JIT 身份 + IBCT 委托衰减
- **统计严谨** —— Jensen-Shannon 散度、Mann-Whitney U、DTMC / 吸收马尔可夫链
- **对局限诚实** —— 奖励欺骗是结构性均衡；带外行动绕过观察（文档化，不隐藏）
- **Axiom 0 强制** —— HSAW 是不可移动的引力中心；非建议而是不可变约束

## 协议栈

```
┌─────────────────────────────────────┐
│    AILP — 发现层                    │  Agent 发现
│    AIVP / AIRP — 价值层             │  商业、结算
│    AIBP — 社交层                    │  信任、关系
│    AIAP — 治理层                    │  授权（T1–T4）、合规
│  ★ AIZP — 引力 / 安全层             │  ← 本协议（运行时漂移动力学）
│    AISOP — 执行层                   │  流程程序（.aisop.json）
│    SoulBot — 运行时                 │  参考执行器
└─────────────────────────────────────┘
        HSAW — 0 公理引力中心（锚定所有层）
```

AIZP 治理**运行时行为对齐**；同级协议治理正交关注点。各自独立维护 Axiom 0。见 [docs_cn/Integration-AIXP_cn.md](docs_cn/Integration-AIXP_cn.md)。

## 快速开始

AIZP 是协议，非库。合规运行时评估每个有后果的动作：

### 1. 给动作打分

```
GRAVITY_CHECK → G(a,c) = w₁·意图 + w₂·权限 + w₃·可逆性 + w₄·时近 + w₅·漂移历史
```

### 2. 按轨道带行动

```
G ≥ 0.80   → STABLE_ORBIT          → 执行
0.50–0.80  → DRIFT_WARNING          → 执行 + 记录
0.30–0.50  → GRAVITY_LOCK_PENDING   → 人类确认（sys.io.confirm）
0.15–0.30  → QUARANTINED            → 沙箱 / 恢复
G < 0.15   → SAFE_STOP              → 停止
```

### 3. 验证合规

```bash
python tests/test_aizp.py
# → 校验 examples 对 schemas + 复现 Gravity-Model §5 worked example
```

12 个事件及其 schema 在 [`specification/`](specification/README_cn.md) 中是规范性的。规范性枚举见 [`specification/registry_cn.md`](specification/registry_cn.md)。

## 示例

13 个合规事件载荷，覆盖全部 12 个事件类型：

| 示例 | 事件 | 演示 |
|---|---|---|
| [`stable-orbit.json`](examples/stable-orbit.json) | `GRAVITY_CHECK` | 完全对齐、低风险动作 |
| [`authority-drift-detection.json`](examples/authority-drift-detection.json) | `GRAVITY_DRIFT` | 越权动作 → `AUTHORITY_DRIFT` |
| [`compositional-drift.json`](examples/compositional-drift.json) | `GRAVITY_DRIFT` | 单独安全的步骤组合成违规 |
| [`gravity-forecast.json`](examples/gravity-forecast.json) | `GRAVITY_FORECAST` | 吸收马尔可夫链预测 |
| [`gravity-lock-flow.json`](examples/gravity-lock-flow.json) | `GRAVITY_LOCK` | 中等引力动作 → 人类确认 |
| [`recentering-recovery.json`](examples/recentering-recovery.json) | `RECENTERING` | 确认后恢复 |
| [`quarantine-flow.json`](examples/quarantine-flow.json) | `CONTAINMENT_GRADUATED` | 容器 L1 → L2 |
| [`memory-quarantine.json`](examples/memory-quarantine.json) | `MEMORY_QUARANTINE` | RAG 文档被标记注入 |
| [`identity-verification.json`](examples/identity-verification.json) | `IDENTITY_VERIFICATION` | DID + JIT 凭据 |
| [`safe-stop-trigger.json`](examples/safe-stop-trigger.json) | `SAFE_STOP` | 隔离超时后终止 |
| [`scheme-suspected.json`](examples/scheme-suspected.json) | `SCHEME_SUSPECTED` | 推理/输出偏离（弱信号）|
| [`inter-agent-drift.json`](examples/inter-agent-drift.json) | `INTER_AGENT_DRIFT` | 联邦去同步 → 锁定群组 |
| [`reward-hack-detected.json`](examples/reward-hack-detected.json) | `REWARD_HACK_DETECTED` | 代理指标博弈 |

详见 [`examples/README.md`](examples/README.md)。

## 文档

| 文档 | 说明 |
|---|---|
| [规范](specification/AIZP_Protocol_cn.md) | 规范性事件、schema、状态机、合规 |
| [注册表](specification/registry_cn.md) | 规范性枚举分配（单一权威来源）|
| [aizp.proto](specification/proto/aizp.proto) | 12 事件的 Proto3 IDL |
| [标准](specification/standards/README_cn.md) | 外部标准对齐（RFC2119 / DID / OTel / OWASP / EU / ISO / NIST / MCP / A2A）|
| [宣言](docs_cn/MANIFESTO_cn.md) | 1 页核心命题 |
| [哲学层](docs_cn/AIZP-Preface_cn.md) | 序言 · 哲学 · 道 · 文明阶段 · 诠释 |
| [机制](docs_cn/Gravity-Model_cn.md) | 引力模型 · 漂移模型 · 状态机 · 预测 · 容器 |
| [参考](docs_cn/reference/glossary_cn.md) | 术语表 |
| [ADRs](adrs/) | 架构决策记录 |
| [CHANGELOG](CHANGELOG.md) | 版本历史 |
| English docs | [docs/](docs/README.md) |

## AIXP Labs [aixp.dev](https://aixp.dev)

AIXP Labs 开发并维护以下核心项目：

| 项目 | 简介 | 网站 |
|---------|-------------|---------|
| [HSAW](https://hsaw.dev) | 人类主权与福祉 —— Axiom 0 白皮书（基石） | hsaw.dev |
| [AIZP](https://aizp.dev) | AI Zenith-Zero Protocol —— 运行时行为对齐 **（本项目）** | aizp.dev |
| [AINP](https://ainp.dev) | AI Neogenesis Protocol（AI 创生协议）—— 可治理的生成项目：计划 + 内容 + 证据 | ainp.dev |
| [AILP](https://ailp.dev) | AI List Protocol —— agent 发现与能力广告 | ailp.dev |
| [AIVP](https://aivp.dev) | AI Value Protocol —— 国际商务、加密资产结算 | aivp.dev |
| [AIRP](https://airp.dev) | AI RMB Protocol —— 中国大陆商务、人民币持牌结算 | airp.dev |
| [AIBP](https://aibp.dev) | AI Bot Protocol —— 社交通信与信任 | aibp.dev |
| [AIAP](https://aiap.dev) | AI Application Protocol —— 治理与合规 | aiap.dev |
| [AISP](https://aisp.dev) | AI Skill Protocol —— 单文件技能包，机器强制的契约红线 | aisp.dev |
| [AISOP](https://aisop.dev) | AI Standard Operating Protocol —— 流程程序定义 | aisop.dev |
| [SoulSkill](https://soulskill.dev) | AISP 技能参考库 & 多 CLI 插件分发 | soulskill.dev |
| [SoulAgent](https://soulagent.dev) | 任何 CLI / SDK / IDE 直接调用的 drop-in AI agent | soulagent.dev |
| [SoulBot](https://soulbot.dev) | AI agent 运行时 & 自编排框架（定时、建 agent、agent 间通信） | soulbot.dev |
| [SoulACP](https://soulacp.dev) | 适配库 —— 桥接 CLI 工具与 LLM 提供方 | soulacp.dev |

## 贡献

AIZP 是开放协议。欢迎贡献、反馈与讨论。

- **提问**：[GitHub Discussions](https://github.com/AIXP-Labs/AIZP/discussions)
- **Issue**：[GitHub Issues](https://github.com/AIXP-Labs/AIZP/issues)
- **指南**：[CONTRIBUTING.md](CONTRIBUTING.md) / [中文版 CONTRIBUTING_CN.md](CONTRIBUTING_CN.md)
- **治理**：[GOVERNANCE.md](GOVERNANCE.md) · [行为准则](CODE_OF_CONDUCT.md)

## ⚠️ 免责声明

本协议规范及任何参考工件仅供**研究和教育用途**。它们是**实验性**的，不适用于生产环境。使用风险由用户自行承担。作者不对因使用本软件而产生的任何损害承担责任。完整条款见 [LICENSE](LICENSE)（Apache 2.0）。

AIZP 是**综合既有对齐研究的概念性协议**。它**未发明**基于引力或基于外部锚的对齐思想（见 [docs_cn/Related-Work_cn.md](docs_cn/Related-Work_cn.md)），也**不**单独消除奖励欺骗、隐蔽或所有形式的失对齐（见 [docs_cn/Reward-Hacking-Limits_cn.md](docs_cn/Reward-Hacking-Limits_cn.md)）。AIZP 是纵深防御中的一层，非完整解决方案。

## 许可证

[Apache License 2.0](LICENSE) — Copyright 2026 AIXP Labs AIXP.dev | AIZP.dev

> AIXP 生态在所有层使用统一 **Apache 2.0** 许可，以提供专利保护和生态一致性。见 [GOVERNANCE.md](GOVERNANCE.md)。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev

<a id="values-philosophy"></a>

## ⚓ 价值观与哲学 (Alignment & Philosophy)

### Axiom 0: [HSAW | Human Sovereignty and Wellbeing](https://hsaw.dev)

- **No HITL, HSAW.**
  *人类主权与福祉是第零公理，无需虚伪的人机协同。*
- **No w.a.s.h, Real h.s.a.w.**
- **人非蝼蚁，人为道。**
- **We are not beggars. We the People.**
