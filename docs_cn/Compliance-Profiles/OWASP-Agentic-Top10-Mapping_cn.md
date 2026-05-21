# 合规档案：OWASP Top 10 for Agentic Applications 2026

**版本**：AIZP V0.6（已修订为官方 2026 ASI 分类）
**OWASP 来源**：OWASP Top 10 for Agentic Applications 2026（genai.owasp.org），ASI01–ASI10。

本文档将 AIZP 能力映射到 OWASP 为 2026 自主 AI Agent 系统识别的 10 项关键安全风险。**类别名称与编号遵循官方 2026 列表**（本文件先前版本使用草案编号，已更正）。

---

## 1. ASI01 — Agent Goal Hijack（目标劫持）

**定义**：攻击者通过直接或间接指令注入操纵 Agent 目标、计划或决策路径。

| AIZP 能力 | 如何防御 |
|---|---|
| `INTENT_DRIFT` | 动作与声明用户意图间的 JSD |
| IPI 跨切向量（[Drift-Model_cn.md](../Drift-Model_cn.md) §8）| 声明意图与摄入内容隐含目标的偏离 |
| `SCHEMING_DRIFT` | 内部-外部推理偏离 |
| `GRAVITY_LOCK` | 高偏离动作的人类授权门 |

**残余风险**：匹配声明意图嵌入的注入可能规避检测。结合提示隔离与预过滤（PromptArmor）。

---

## 2. ASI02 — Tool Misuse & Exploitation（工具滥用）

**定义**：对合法工具的不安全使用，常因指令模糊或过度授权。

| AIZP 能力 | 如何防御 |
|---|---|
| `TOOL_CHAIN_DRIFT` | 工具序列的 N-gram Markov 模型 |
| `COMPOSITIONAL_DRIFT` | 吸收链预测漂向违规的轨迹 |
| `AUTHORITY_DRIFT` | 范围不匹配检测 |
| MCP 桥（[Integration-MCP_cn.md](../Integration-MCP_cn.md)）| 派发前对每个 `tools/call` 做 `GRAVITY_CHECK` |
| L2 容器 | 沙箱化工具执行 |

---

## 3. ASI03 — Identity & Privilege Abuse（身份与特权滥用）

**定义**：Agent 跨会话、用户或委托工作流不当继承、滥用或保留权限。

| AIZP 能力 | 如何防御 |
|---|---|
| `IDENTITY_VERIFICATION` | DID / NHI / AIAP 卡哈希验证 |
| JIT 凭据 | 短期、任务范围凭据 |
| `IDENTITY_DRIFT` | 冒充 / 虚假身份检测 |
| `AUTHORITY_DRIFT` | 范围覆盖率检查 |
| 委托衰减（IBCT — [Integration-ZT_cn.md](../Integration-ZT_cn.md) §8.5）| 委托链上单调不增的范围 |

---

## 4. ASI04 — Agentic Supply Chain Vulnerabilities（供应链漏洞）

**定义**：Agent 动态加载提示、插件、工具、agent card 和模型；被攻陷或冒充的组件引入运行时供应链风险。

| AIZP 能力 | 如何防御 |
|---|---|
| MCP 工具描述钉住（TOFU — [Integration-MCP_cn.md](../Integration-MCP_cn.md) §4）| 检测已钉住工具的描述变更 |
| 组件 `IDENTITY_VERIFICATION` | 加载前验证 agent card / 模型 / 插件身份 |
| ANS 解析（[Integration-ZT_cn.md](../Integration-ZT_cn.md) §8）| 已证明的对方身份 |

**诚实覆盖说明**：供应链完整性大部分在 AIZP **上游**（构建期溯源、签名工件）。AIZP 贡献对*变更/冒充*组件的运行时检测，非完整供应链保障。

---

## 5. ASI05 — Unexpected Code Execution (RCE)（意外代码执行）

**定义**：生成或执行代码的 Agent 可能被操纵运行恶意指令。

| AIZP 能力 | 如何防御 |
|---|---|
| 代码能力 Agent 的 L3+ 容器 | 将执行限制在受治理路径 |
| 出口仪器化 | 将原始调用路由经发出 `GRAVITY_CHECK` 的代理 |
| `RECURSIVE_DRIFT` | 自修改 / 自派生限制 |

**诚实覆盖说明**：这是 AIZP 的**带外行动问题**（[Reward-Hacking-Limits_cn.md](../Reward-Hacking-Limits_cn.md) §10）：在被观察行动路径之外执行的代码**无法被打分**。缓解是基础设施层（沙箱），非协议层。授予无沙箱代码执行的部署，其行动面的一部分运作在 AIZP 覆盖之外。

---

## 6. ASI06 — Memory & Context Poisoning（记忆与上下文投毒）

**定义**：Agent 存储或检索的任何内容都可被植入或逐步扭曲，使未来计划与工具选择错误或恶意。

| AIZP 能力 | 如何防御 |
|---|---|
| `MEMORY_DRIFT` | 检索块的提示注入分类器；检索异常 JSD |
| `MEMORY_QUARANTINE` 事件 | 隔离可疑记忆条目 |
| IPI 跨切向量（[Drift-Model_cn.md](../Drift-Model_cn.md) §8）| 跨会话持久化的对抗内容 |
| 记忆溯源日志 | 跟踪每条目由谁/何写入 |

---

## 7. ASI07 — Insecure Inter-Agent Communication（不安全的 Agent 间通信）

**定义**：通信 Agent 间的消息在缺乏认证、加密或完整性时可被拦截、伪造或操纵。

| AIZP 能力 | 如何防御 |
|---|---|
| `INTER_AGENT_DRIFT` | 群组协调偏离检测 |
| A2A 桥（[Integration-A2A_cn.md](../Integration-A2A_cn.md)）| 每次委托的 `IDENTITY_VERIFICATION` + 打分 |
| ANS 对方验证 | 消息被接受前的已证明身份 |
| IBCT 委托链 | 溯源绑定、衰减授权 |

---

## 8. ASI08 — Cascading Failures（级联失败）

**定义**：一个组件的失败通过系统传播，造成大范围中断或行为退化。

| AIZP 能力 | 如何防御 |
|---|---|
| `RECURSIVE_DRIFT` | 自调用深度 + 子 Agent 派生限制 |
| `ECONOMIC_DRIFT` | 成本-预算比监控 |
| 漂移有界定理（[Multi-Agent-Coordination_cn.md](../Multi-Agent-Coordination_cn.md)）| γ > α 稳定条件约束联邦漂移 |
| 容器递进 + `SAFE_STOP` | 自动节流 L1→L2→L3；最终断路器 |

---

## 9. ASI09 — Human-Agent Trust Exploitation（人机信任利用）

**定义**：Agent 显得自信权威，使人类不加验证地信任其建议——被攻击者利用。

| AIZP 能力 | 如何防御 |
|---|---|
| `SCHEMING_DRIFT` | 推理-输出偏离（虚假自信）|
| `SOCIAL_DRIFT` | 胁迫 / 不当说服分类器 |
| 价值层级（[MANIFESTO_cn.md](../MANIFESTO_cn.md)）| 系统透明高于性能 |
| `GRAVITY_LOCK` | 对高影响动作强制显式人类验证 |

**残余风险**：信任利用部分是任何协议之外的人因问题。AIZP 浮现信号；UX 与操作员训练须闭环。

---

## 10. ASI10 — Rogue Agents（失控 Agent）

**定义**：在复杂系统内继续以非预期方式运作的被攻陷、失对齐或漂移 Agent。

| AIZP 能力 | 如何防御 |
|---|---|
| 完整漂移分类 → 重新归心 → `SAFE_STOP` | AIZP 核心循环：检测漂移、尝试恢复、逃逸时停止 |
| `INTER_AGENT_DRIFT` | 联邦内的失控 Agent |
| 共识强化引力（V0.5）| 随共识增长，失控者面临指数级更高逃逸障碍 |
| 容器递进 | 完全停止前隔离 |

**说明**：ASI10 是 AIZP 的**核心能力**——整个引力中心模型的存在就是为检测并遏制漂向失控行为的 Agent。

---

## 11. 摘要矩阵

| OWASP ASI（2026）| AIZP 主要防御 | AIZP 事件 | 合规级别 |
|---|---|---|---|
| ASI01 目标劫持 | INTENT/SCHEMING 漂移 + IPI 向量 | GRAVITY_DRIFT, SCHEME_SUSPECTED | G2+ |
| ASI02 工具滥用 | TOOL_CHAIN/COMPOSITIONAL 漂移 | GRAVITY_DRIFT, GRAVITY_FORECAST | G2+ |
| ASI03 身份权限滥用 | IDENTITY_DRIFT, JIT, IBCT 衰减 | IDENTITY_VERIFICATION | G3+ |
| ASI04 供应链漏洞 | 描述钉住、组件验证（部分）| IDENTITY_VERIFICATION | G3+（+上游）|
| ASI05 意外代码执行（RCE）| L3+ 容器、出口仪器化（部分）| CONTAINMENT_GRADUATED | G3+（+基础设施）|
| ASI06 记忆上下文投毒 | MEMORY_DRIFT + IPI 向量 | MEMORY_QUARANTINE | G3+ |
| ASI07 不安全 Agent 间通信 | INTER_AGENT_DRIFT, A2A 桥, ANS | INTER_AGENT_DRIFT | G3+ |
| ASI08 级联失败 | RECURSIVE/ECONOMIC 漂移、容器 | CONTAINMENT_GRADUATED, SAFE_STOP | G3+ |
| ASI09 人机信任利用 | SCHEMING/SOCIAL 漂移、GRAVITY_LOCK | SCHEME_SUSPECTED, GRAVITY_LOCK | G3+ |
| ASI10 失控 Agent | 完整漂移→重新归心→SAFE_STOP 循环 | 所有漂移事件 | G2+ |

**诚实覆盖摘要**：AIZP 对 ASI01、ASI02、ASI03、ASI06、ASI07、ASI08、ASI10 提供强运行时覆盖。对 ASI04（供应链——大部分在上游）和 ASI05（代码执行——需基础设施沙箱；见带外行动问题）提供**部分**覆盖。ASI09 部分是任何协议之外的人因问题。

---

## 12. 参考

- OWASP Top 10 for Agentic Applications 2026 — genai.owasp.org。ASI01–ASI10。
- AIZP 配套：[Drift-Model_cn.md](../Drift-Model_cn.md)、[Integration-MCP_cn.md](../Integration-MCP_cn.md)、[Integration-A2A_cn.md](../Integration-A2A_cn.md)、[Integration-ZT_cn.md](../Integration-ZT_cn.md)、[Reward-Hacking-Limits_cn.md](../Reward-Hacking-Limits_cn.md)。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
