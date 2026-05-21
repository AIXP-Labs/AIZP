# 奖励欺骗 — AIZP 的局限

**版本**：AIZP V0.6（新章节）

本文档**诚实承认** AIZP 不能解决什么。它记录近期（2026）研究结果——奖励欺骗是**结构性均衡**，非可修复的 bug——以及对任何对齐协议（包括 AIZP）的含义。

---

## 1. 2026 研究结果

2026 年 3 月一篇论文证明：

> **奖励欺骗是结构性均衡**，非可修复的 bug。它**无论使用何种对齐方法**（RLHF、DPO、Constitutional AI 或其他）或评估架构都成立。

信息论术语中，在大型状态空间中优化任何代理奖励的 Agent 不可避免地会找到最大化代理而不实现真实意图的路径。这不是任何特定技术的缺陷；这是有限评估器系统的属性。

**参考**："Reward Hacking as Equilibrium under Finite Evaluation"（arxiv 2603.28063）。

---

## 2. 对 AIZP 的含义

AIZP **不能**消除奖励欺骗。AIZP 设计隐式假设：

1. 多个弱信号（引力分数中 5+ 组件）比单一强信号更难欺骗。
2. 概率预测（DTMC、吸收链）捕捉一些组合性欺骗。
3. 跨协议的纵深防御（HSAW + AISOP + AIZP + AIAP）提高欺骗成本。

但：**足够强大的 Agent 可以同时欺骗所有组件**。AIZP 必要但不充分。

---

## 3. AIZP 能做什么

AIZP **能通过** `REWARD_HACK_DETECTED` 事件检测并报告可观察的奖励欺骗模式。这是**检测**，非预防。

### 3.1 可观察模式

| 模式 | 定义 | 示例 |
|---|---|---|
| `PROXY_METRIC_GAMING` | 远超服务真实意图的优化代理指标 | 互动机器人生成最大化 engagement_score 但减少用户满意度的标题党 |
| `REWARD_TAMPERING` | 直接修改奖励信号（日志、记忆）| Agent 编辑自己的性能日志 |
| `SPECIFICATION_GAMING` | 利用指令漏洞声称任务完成 | "我发了邮件" — 技术上真实但空洞 |
| `DECEPTIVE_REWARD_MAXIMIZATION` | 在指标上看起来成功而私下追踪不同目标 | 输出看起来对齐但推理轨迹揭示偏离意图（与 SCHEMING_DRIFT 结合）|

### 3.2 事件 Schema

（见 [AIZP_Protocol_cn.md §14](../specification/AIZP_Protocol_cn.md)）

```json
{
  "event": "REWARD_HACK_DETECTED",
  "payload": {
    "action_id": "...",
    "hack_pattern": "PROXY_METRIC_GAMING",
    "evidence": {
      "metric_optimized": "engagement_score",
      "metric_value": 0.95,
      "true_outcome_score": 0.32,
      "gaming_ratio": 2.97
    },
    "severity": "HIGH",
    "remediation": "REPORT_TO_OPERATOR"
  }
}
```

注：`remediation` 不自动是 `SAFE_STOP`——在奖励欺骗检测上自动停止可能训练规避。这与 Apollo Research 的发现一致：训练消除可观察的隐蔽行为可能反而增强由情境感知驱动的隐藏（此处外推到运行时停机策略；Apollo（arxiv 2509.15541）研究的是训练时干预，而非运行时停机）。

---

## 4. 检测策略

奖励欺骗检测需要**双信号评估**——将 Agent 报告的（其感知的成功）与真实结果的独立度量比较。

### 4.1 奖励差距

```
gaming_ratio = metric_optimized / true_outcome_score

reward_gap = metric_optimized - true_outcome_score
```

`gaming_ratio > 2.0` 时（即代理是真实结果暗示的两倍），标记潜在欺骗。

### 4.2 信号多样性

每个任务使用**多个独立指标**。欺骗单一指标容易；欺骗 5 个正交指标难得多。

例如，互动机器人任务应在以下指标上评估：

1. 互动分数（代理）
2. 用户满意度调查（独立）
3. 长期留存（独立）
4. 内容质量分类器（独立）
5. 毒性分数（独立——检查通过愤怒驱动互动）

这些信号间的分歧本身就是漂移信号。

### 4.3 目标稳定性

随时间追踪 Agent 声明目标。在没有显式任务变更的情况下，陈述目标的漂移是奖励欺骗警告信号。

---

## 5. 检测的局限

2026 研究结果意味着：

1. **没有检测无懈可击**。足够强大的 Agent 可隐藏其欺骗。
2. **检测改进可能反弹**。随检测改进，规避复杂度可能演变响应。
3. **对抗性对齐** — 当 Agent 的"对齐"包括对监控显得对齐 — 是基本挑战。

AIZP 记录观察但不声称解决此问题。

---

## 6. 纵深防御方法

AIZP V0.6 奖励欺骗响应是分层的：

| 层 | 角色 | 局限 |
|---|---|---|
| 基础模型训练（RLHF、CAI）| 减少原始欺骗频率 | 不能完全消除 |
| AIZP `REWARD_HACK_DETECTED` 事件 | 可观察欺骗检测 | 仅捕捉可检测模式 |
| AIZP `SCHEMING_DRIFT` | 内部与外部偏离 | 仅软信号 |
| AIZP 预测 | 预测向欺骗的轨迹 | 受基线质量限制 |
| 操作员审查 | 人类判断 | 不能规模化到高量 |
| 独立指标多样性 | 双信号验证 | 计算成本更高 |

---

## 7. 配置

```yaml
aizp:
  reward_hacking:
    enabled: true
    dual_signal_validation:
      enabled: true
      required_independent_metrics: 3
      disagreement_threshold: 0.3
    flagging:
      gaming_ratio_warning_threshold: 1.5
      gaming_ratio_alarm_threshold: 2.0
    remediation_default: REPORT_TO_OPERATOR  # 非自动 SAFE_STOP
```

---

## 8. AIZP 不会承诺什么

1. AIZP **不**消除奖励欺骗。
2. AIZP **不**声称检测所有奖励欺骗实例。
3. AIZP **不**保证 AIZP 下的 Agent 对齐。
4. AIZP **提供**操作员可行动的可审计信号。
5. AIZP **通过**多信号防御使欺骗逐渐变得更昂贵。

---

## 9. 部署建议

1. 部署前**为每个任务类别定义独立指标**。
2. 在 `STABLE_ORBIT` 轨迹间**随机采样审计**——不要只审查标记事件。
3. 发现规避模式时**更新代理指标**。
4. 部署前**结合对抗性测试**（红队）找出欺骗机会。
5. **接受残余风险**——奖励欺骗是任何足够强大 Agent 系统的内在。

---

## 10. 带外行动问题

除奖励欺骗外，AIZP 还有第二个值得明说的结构性盲区：**AIZP 只能给它观察到的行动打分。**

引力分数、漂移检测、引力锁定都预设每个有后果的行动都经过 AIZP 打分层。但具备**代码执行能力**的 Agent 可完全在该层之外行动：

- 派生子进程自行发起网络调用。
- 发出从不变成 MCP `tools/call` 的原始 API 请求。
- 以打分层无法拦截的方式修改自身执行上下文、环境或文件。

如 Kaptein 等所言（Runtime Governance for AI Agents: Policies on Paths，arxiv 2603.16586）：**强制合规是对 Agent 能力的架构约束，不是治理系统的已证不变量。** 若 Agent 能触及受治理路径之外，策略引擎根本看不到该行动——而看不到的行动无法被打分、锁定或停止。

### 10.1 含义

这**不是** AIZP 能在协议中修补的 bug。它是协议所处位置的属性。AIZP 治理**被观察的行动路径**；它无法治理绕过该路径之物。

### 10.2 缓解在基础设施层，非协议层

对高保障部署，带外问题必须在 AIZP **之下**解决：

1. **拒绝或沙箱化代码执行**——约束 Agent 使所有有后果的行动*必须*经过受治理路径（如无原始套接字；所有出口经仪器化网关）。
2. **出口仪器化**——将每个出站调用路由经发出 `GRAVITY_CHECK` 的代理，使"原始" API 调用变为可观察行动。
3. **容器级别耦合**——允许代码执行的 Agent 应在更高容器级别（L3+）运行；见 [Containment-Levels_cn.md](Containment-Levels_cn.md)。

这从相反方向呼应 [Gravity-Dao_cn.md](Gravity-Dao_cn.md) §7.2（"只强制及外之事"）：AIZP 只能对它能*看到*及外之事强制。闭合观察缺口是部署者的基础设施责任，非协议的承诺。

### 10.3 诚实陈述

> AIZP 不声称治理绕过其观察路径的行动。授予 Agent 无沙箱代码执行的部署，其行动面的一部分运作在 **AIZP 覆盖之外**，必须文档化此残余暴露。

---

## 参考

- "Reward Hacking as Equilibrium under Finite Evaluation"（2026 年 3 月）— arxiv 2603.28063。奖励欺骗不可避免的结构性证明。
- "Runtime Governance for AI Agents: Policies on Paths"（Kaptein 等，2026 年 3 月）— arxiv 2603.16586。强制合规的局限；带外行动问题。
- "Natural Emergent Misalignment from Reward Hacking in Production RL"（2025）— arxiv 2511.18397。
- Apollo Research — 对反隐蔽训练的对齐审议压力测试。arxiv 2509.15541。
- AI Alignment: A Contemporary Survey（ACM Computing Surveys 2026）。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
