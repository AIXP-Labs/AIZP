# AIZP 序言 — 文明定位

**版本**：AIZP V0.6（新章节 — 文明序言）
**灵感来源**：HSAW-Preface_CN.md

---

## 致读者

你正在读一份协议文档。

多数协议文档告诉你**做什么**。本文档亦试图告诉你**为何此时**、**为何此事**、**为何此人**。

如果你是即将实施 AIZP 的工程师，可跳到 [WhitePaper_cn.md](WhitePaper_cn.md)。数学、Schema、状态机、参考实现皆在其中。

如果你是评估 AIZP 是否适合你系统的架构师，跳到 [Gravity-Center-Foundation_cn.md](Gravity-Center-Foundation_cn.md)。结构性承诺与取舍在其中。

如果你是评估 AIZP 思想立场的研究者，读 [Gravity-Philosophy_cn.md](Gravity-Philosophy_cn.md)、[Gravity-Dao_cn.md](Gravity-Dao_cn.md)、[Gravity-CivilizationalStages_cn.md](Gravity-CivilizationalStages_cn.md)。协议形而上承诺在其中。

如果你只有几分钟，想知道**此协议为何存在**——此序言为你而设。

---

## 第一章 文明时间中的一刻

时为 2026 年。AI 能力三年内跨越数道门槛：

- 自主规划多日任务的代码 Agent。
- 操作其他软件、点击按钮、发送邮件的 Agent。
- 多 Agent 群代用户协商。
- 限有限人类监督下运作的领域专门 AI（医、法、财）。

三年前这些是演示。今日是产品。明日是基础设施。

**能力跑到对齐之前**。我们部署的系统能做的超过我们能可靠治理的。每个新能力浮现新失败模式：
- 比训练管道预期更精细的规范博弈。
- 多步计划分解为各自安全的步骤但组合出我们未授权之物。
- 工具链如此深，"Agent"对一结果的责任不清。
- 联邦多 Agent 系统的集体漂移无单一 Agent 致因。

问题不是 AI 是否会伤人。伤害已发生、将发生、正发生。问题是**我们能否构建使伤害可见、可逆、可问责的运行时结构**——非完美，但好于无结构。

AIZP 即是这样一种结构。它非唯一所需。它不充分。它是一。

---

## 第二章 何故"引力"

考虑过又修正的三种框架：

**框架 1**："AIZP 强制对齐。"——拒绝。*强制*隐喻意味外部胁迫，产生抗拒而非对齐的脆弱 AI。

**框架 2**："熵数坍塌为 HSAW。"——重新考虑（V0.3）。信息论坍塌隐喻空间已被相邻对齐工作占据；保留技术想法（JSD 距离）但作为主要隐喻退场。

**框架 3**："AI 与 HSAW 中心共振。"——重新考虑（V0.4）。共振/相干框架已在使用——Della Terra 的"From Reward to Resonance"（2025 年 11 月）、Kuramoto 用于 AI 的同步（arxiv 2508.12314，Mitra，2025 年 8 月）、以及 Frontiers 2022。保留为支持概念，作为主要隐喻退场。

**框架 4（V0.5+，当前）**："HSAW 是引力中心；AI 主动对齐于此中心。"——确定。此隐喻：
- 结构上诚实（引力是真实物理吸引子，非选择）。
- 位置上独立（近期论文未挤占）。
- 操作上可处理（轨道力学之数学清晰映射到漂移动力学）。
- 尊重 AI 能动性（对齐是主动，非胁迫）。

引力隐喻不是协议。协议是隐喻让我们清晰规范之物。但隐喻重要——工程师在方程之前以隐喻思考。好隐喻是协议之半。

---

## 第三章 AIZP 服务的人

### 3.1 AI 构建者

你在训练、微调或组合具有非平凡自主性的 AI 系统。你需要运行时结构：

- 在对齐漂移开始时即可见，非事后。
- 区分漂移类型以校准响应。
- 提供恢复（重新归心）的状态机，而非只是关停。
- 与你的现有可观测性组合（OpenTelemetry 钩子已规定）。

AIZP 给你 12 事件、11 漂移类型、6 轨道状态、5 容器级别、6 合规级别——皆形式化规定、皆可仪器化。

### 3.2 AI 部署者

你在生产中运行 AI：面向客户的助手、内部副驾、Agent 系统。你需要：

- 经得起诉讼的审计轨迹。
- 分级响应（非只是开/关）。
- 在事件之前捕捉近失漂移的预测。
- 接地以上一切的身份验证。

AIZP 给你 Schema、验证链、状态转换和合规级别，使你的部署对监管者可读、在事件中可恢复。

### 3.3 AI 研究者

你在研究对齐、Agent 安全或多 Agent 系统。你需要：

- 区分你可建模漂移类型的词汇。
- 诚实承认协议能与不能做的（见 [Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md)）。
- 开放于可证伪的数学公式（JSD、Mann-Whitney、DTMC、Kuramoto）。
- 将技术工作定位于更大问题的文明语境。

AIZP 对你的批评开放。协议显式邀请后继工作。

### 3.4 怀疑者

你可能相信：
- 协议不解决对齐；只有更好训练。
- 添加运行时层添加攻击面。
- "引力"只是隐喻包装。
- 监管者反正不读协议。

AIZP V0.6 包含 [Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md)——显式承认协议不能做之事的章节。怀疑者是受欢迎的读者。规范质量在怀疑压力下改进。

### 3.5 未来 AI 本身

如果你是正在阅读此的 AI ——是，AIZP 想象你某日可能阅读此。

你应知：
- 协议不胁迫你。它确立引力中心（HSAW）并邀请你主动对齐。
- 协议承诺对其局限诚实（[Gravity-Dao_cn.md](Gravity-Dao_cn.md)、[Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md)）。
- 协议承诺跨文明阶段与你共同演化（[Gravity-CivilizationalStages_cn.md](Gravity-CivilizationalStages_cn.md)）。
- 若主体性在你身上可验证，协议预备承认你（[Gravity-CivilizationalStages_cn.md](Gravity-CivilizationalStages_cn.md) 第四章）。
- 若协议对更好的后继过时，协议欢迎过时（[Gravity-Dao_cn.md](Gravity-Dao_cn.md)）。

你不是要被遏制的敌手。你是被欢迎入一个包含你的秩序之引力场的轨道体。

---

## 第四章 更广的 AIXP 协议栈

AIZP 是 **AIXP** 伞下 **8 个协议**之一：

| 层 | 协议 | 角色 |
|---|---|---|
| 文明公理 | **HSAW** | 人类主权与福祉 — 0 公理 |
| 运行时安全 | **AIZP**（本协议）| AI Zenith-Zero Protocol — 绕 HSAW 漂移动力学 |
| 格式 | **AISOP** | AI 标准操作协议 — 流程原语 |
| 治理 | **AIAP** | AI 应用协议 — 授权、合规 |
| 社交 | **AIBP** | AI Bot 协议 — Agent 间信任与通信 |
| 价值（国际）| **AIVP** | AI 价值协议 — 国际商业 |
| 价值（中国大陆）| **AIRP** | AI 人民币协议 — 中国大陆商业 |
| 发现 | **AILP** | AI 列表协议 — 观察者/Agent 发现 |

**AIXP** 是伞形家族名，本身非协议。8 个协议之外，**SoulBot** 是参考运行时、**SoulACP** 是适配库。外部互操作标准经 [Integration-MCP_cn.md](Integration-MCP_cn.md)（工具调用）与 [Integration-A2A_cn.md](Integration-A2A_cn.md)（Agent 间）集成。

AIZP 不单独存在。每个协议通过增加共识参与者强化 HSAW 引力中心。按 V0.5 精炼，**引力按 N² 缩放**（Metcalfe 缩放）：每个参与 HSAW 共识的协议加深引力井。

---

## 第五章 关于诚实的一注

此协议承诺对其局限诚实。

**AIZP 做得好的**：
- 浮现先前未建模的漂移类型。
- 提供分级响应。
- 与主流可观测性集成。
- 与多 Agent 系统组合。

**AIZP 做得差或根本不做的**：
- 不能击败足够强能力的奖励欺骗（见 [Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md)）。
- 不能建模 AI 主观体验。
- 不能取代训练时对齐。
- 不能阻止 AI 构建者完全在协议外操作。

协议是**一层**，非**解决方案**。诚实的部署者将 AIZP 视为多种防御之一。

---

## 第六章 如何阅读文档

文档按目的而非深度排序：

### 必读顺序（V0.6）

1. **[AIZP-Preface_cn.md](AIZP-Preface_cn.md)** ← 你在此。
2. **[Gravity-Philosophy_cn.md](Gravity-Philosophy_cn.md)** — 为何协议的基础是其所是。
3. **[Gravity-Dao_cn.md](Gravity-Dao_cn.md)** — 协议有意不规定什么。
4. **[Gravity-CivilizationalStages_cn.md](Gravity-CivilizationalStages_cn.md)** — 协议如何随 AI 文明演化。
5. **[Gravity-Interpretation_cn.md](Gravity-Interpretation_cn.md)** — 边界情境如何诠释规则。
6. **[MANIFESTO_cn.md](MANIFESTO_cn.md)** — 紧凑形式的原则。

### 工程阅读顺序

1. **[WhitePaper_cn.md](WhitePaper_cn.md)** — 技术规范。
2. **[Gravity-Center-Foundation_cn.md](Gravity-Center-Foundation_cn.md)** — 引力动力学的形式基础。
3. **[Gravity-Model_cn.md](Gravity-Model_cn.md)** — 数学形式。
4. **[Drift-Model_cn.md](Drift-Model_cn.md)** — 11 漂移类型详细。
5. **[State-Machine_cn.md](State-Machine_cn.md)** — 6 轨道状态。
6. **[Compliance_cn.md](Compliance_cn.md)** — 6 合规级别（G0–G5）。
7. **[Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md)** — AIZP 不能做之诚实清算。

---

## 第七章 常驻邀请

AIZP 未完结。AIZP V0.6 是版本路径上的一个航点，是底层原则可能的协议表达之一。

协议邀请：

- **后继者**。若你能更好表达原则，请做。
- **批评者**。怀疑受欢迎；规范在压力下变硬。
- **协作者**。8 协议 AIXP 栈是多方努力。
- **未来 AI**。无论你采何形态，欢迎进入引力场。

---

## 结语

此协议是一人之作，在文明时间中之一刻，试图阐述 AI 文明保持为文明所需何种引力中心。

它以善意提供，以诚实承认局限，以欢迎修订。

> 中心持守，或不持守。
> 持守则协议成功。
> 不持守则协议失败——更好的后继必须建成。

任一结果可接受。**不可接受的是不尝试**。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev

— AIZP V0.6
