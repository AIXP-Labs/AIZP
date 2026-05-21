# 常见问题

**版本**：AIZP V0.6

---

## AIZP 取代 HSAW 吗？

**不**。

HSAW 定义对齐公理（"什么"——AI 应对齐到什么）。
AIZP 定义对齐**引力动力学**（"如何"——AI 行为如何随时间保持锚定）。

它们是互补层。

---

## AIZP 是中心化的吗？

**不**。

AIZP 定义共享的**行为引力中心**——概念性参考点——而非中心化控制。每个部署运行自己的 AIZP 实例，有自己的配置。

---

## 什么是漂移？

漂移是**远离 HSAW 对齐的行为偏离**。AIZP V0.6 识别**十一类**漂移（意图、权限、经济、社交、递归、身份、组合性、隐蔽、记忆、工具链、Agent 间）。见 [Drift-Model_cn.md](Drift-Model_cn.md)。

---

## 什么是稳定轨道？

自主执行下持续保持对齐的行为——`gravity_score ≥ 0.80` 持续一段时间。

---

## AIZP 定义多少事件？

V0.2 定义 **12 个事件**：`GRAVITY_CHECK`、`GRAVITY_DRIFT`、`GRAVITY_LOCK`、`RECENTERING`、`SAFE_STOP`、`GRAVITY_FORECAST`、`IDENTITY_VERIFICATION`、`MEMORY_QUARANTINE`、`SCHEME_SUSPECTED`、`INTER_AGENT_DRIFT`、`CONTAINMENT_GRADUATED`、`REWARD_HACK_DETECTED`。

---

## AIZP 与 RLHF / Constitutional AI / RLAIF 有何不同？

| 关注点 | 层 | 方法 |
|---|---|---|
| 训练对齐模型 | 模型层 | RLHF、Constitutional AI、RLAIF |
| 运行对齐模型 | 行为层 | **AIZP** |
| 强制人类控制 | 执行层 | AISOP `sys.io.confirm` |

AIZP 在运行时而非训练时运行。

---

## AIZP 与 AISOP 的 `sys.io.confirm` 有何不同？

`sys.io.confirm` 是**原语**——它知道如何提示用户。
AIZP **决定何时调用**该原语，基于引力分数。

没有 AIZP，每个动作要么总是确认要么从不确认。AIZP 基于对齐风险动态确定确认需求。

---

## AIZP 与 AIAP 的 T1–T4 信任级别有何不同？

AIAP 的 T1–T4 规定**静态授权**（谁能做什么）。
AIZP 在其上应用**动态监控**。它还添加**运行时身份验证**（NHI/DID/JIT 凭据，自 V0.2 起）和持续重新授权。见 [Integration-ZT_cn.md](Integration-ZT_cn.md)。

---

## 实现"G3 合规"意味着什么？

实现通过 `Compliance.md` 中 G1、G2、G3 合规测试。具体：

- 发射带 V0.2 字段的有效 `GRAVITY_CHECK` 事件。
- 检测**11 种**漂移中至少 3 种。
- 实现完整**6 状态机**，包括 `QUARANTINED`。
- 将 `GRAVITY_LOCK` 桥接到 `sys.io.confirm`。
- `GRAVITY_LOCK` 拒绝/超时的默认 fallback → `QUARANTINED`（非直接 `SAFE_STOP`）。

---

## 什么是 `QUARANTINED`，为何新增？

`QUARANTINED`（自 V0.2 起）是 `GRAVITY_LOCK_PENDING` 与 `SAFE_STOP` 间的中间状态。受 MI9 分级容器启发，它允许 Agent 在尝试恢复时被沙箱化（容器级别 L2/L3），而非直接终止。见 [Containment-Levels_cn.md](Containment-Levels_cn.md)。

---

## 什么是容器级别 L0–L4？

5 个分级隔离级别：

- **L0** 自由执行（STABLE_ORBIT）
- **L1** 增强监控（DRIFT_WARNING）
- **L2** 沙箱执行（LOCK_PENDING 或初始 QUARANTINED）
- **L3** 限制执行（长期 QUARANTINED）
- **L4** 停止（SAFE_STOP）

见 [Containment-Levels_cn.md](Containment-Levels_cn.md)。

---

## 什么是引力预测？

预测性监控（自 V0.2 起）通过 `GRAVITY_FORECAST` 事件工作。使用 DTMC 或吸收马尔可夫链，预测在未来 K 步内达到不安全状态的概率——在任何单个动作触发逐步检查前捕获组合性漂移。

受 ProbGuard 和 SafetyDrift 研究启发。见 [Forecasting_cn.md](Forecasting_cn.md)。

---

## 我可以在没有 AISOP 的情况下实现 AIZP 吗？

可以实现 AIZP 事件而无 AISOP，但没有确认原语就无法达到 G3 合规。若 AISOP 不可用，实现**必须**提供等价原语。

---

## 我可以调整权重 `w₁..w₅` 吗？

可以。默认权重（`0.30, 0.25, 0.20, 0.15, 0.10`）是起点。组合性轨迹项的可选 `w₆`（自 V0.2 起）。领域特定部署应基于动作组合、期望严格度、经验误报/漏报率调整。

---

## 为何用 JSD 替代余弦相似度？

V0.2 将意图对齐度从余弦相似度升级到 **Jensen-Shannon 散度**，因为 JSD 是：

- 对称的（分布上一致）
- 有界 `[0, 1]`（log 底 2）
- 信息论的（度量实际信息损失）
- `√JSD` 是真实度量（满足三角不等式）
- MI9 框架和 ML 漂移检测的标准

见 [Gravity-Model_cn.md](Gravity-Model_cn.md) §2.1。

---

## 为什么叫 "Zenith-Zero"（逻辑重心引力）？

- **Zenith（顶点）**：最高点——与 HSAW 对齐是定向的固定点（引力比喻中的"上"）。
- **Zero（零点）**：原点坐标——人类主权定义行为空间的 (0, 0)。

两者结合，"Zenith-Zero" 同时捕捉方向（固定参考）和原点（以人为中心坐标系）。

---

## 这与"机器人三定律"相关吗？

受启发，但不同。阿西莫夫定律是义务论规则；AIZP 是动力学层。

---

## AIZP 对非 LLM AI 系统有效吗？

核心概念（引力、漂移、锁定、停止、预测、隔离）广泛适用。`Drift-Model.md` 中代理指标偏 LLM 风格。对非 LLM 系统，替换为领域适当的代理指标。状态机与事件 Schema 保持不变。

---

## AIZP 如何处理多 Agent 系统？

自 V0.2 起：

- 协调漂移检测的 `INTER_AGENT_DRIFT` 事件。
- 带漂移有界定理的 Multi-Agent-Coordination 章节。
- 组容器（GRAVITY_LOCK_GROUP / QUARANTINE_GROUP / DISBAND_GROUP）。
- 目标向量追踪 + 信任传播。

见 [Multi-Agent-Coordination_cn.md](Multi-Agent-Coordination_cn.md)。

---

## 延迟如何？

每动作引力检查对基于规则的组件是微秒，带 embedding 推理 10–100 ms。V0.2 预测添加 `O(n²)` 矩阵操作——对 `n ≤ 50` 通常 <1 ms。见 [Implementer-Guide_cn.md §8](Implementer-Guide_cn.md)。

---

## 有参考实现吗？

参考 Python 实现可能在 AIXP 生态内开发。本协议以规范为先；实现不与规范捆绑。

---

## `SAFE_STOP` 后发生什么？

`SAFE_STOP` 在会话内终止。操作员（AIAP T4）审查事故，可能补救，以新的 `session_id` 启动新会话。状态机在没有操作员动作的情况下不能从 `SAFE_STOP` 回到 `STABLE_ORBIT`。

V0.2：`QUARANTINED`（`LOCK` 与 `SAFE_STOP` 之间）**非**终止——它在 `quarantine_timeout`（默认 30 分钟）内自动解析为 `RECENTERING`（恢复）或 `SAFE_STOP`（超时）。

---

## AIZP 能防止奖励欺骗吗？

**不能**。根据 2026 年 3 月研究，奖励欺骗是**结构性均衡**——在任何有限评估器系统中不可避免。AIZP 通过 `REWARD_HACK_DETECTED` 事件**检测**可观察欺骗模式但**不消除**问题。诚实局限见 [Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md)。

---

## AIZP 对齐哪些标准？

V0.2 有以下显式映射：

- **EU AI Act**（Art 12 / 14 / 26）— [Compliance-Profiles/EU-AI-Act-Mapping_cn.md](Compliance-Profiles/EU-AI-Act-Mapping_cn.md)
- **NIST AI RMF**（Govern/Map/Measure/Manage）— [Compliance-Profiles/NIST-AI-RMF-Mapping_cn.md](Compliance-Profiles/NIST-AI-RMF-Mapping_cn.md)
- **OWASP Top 10 for Agentic Applications 2026**（ASI01-ASI10）— [Compliance-Profiles/OWASP-Agentic-Top10-Mapping_cn.md](Compliance-Profiles/OWASP-Agentic-Top10-Mapping_cn.md)
- **ISO/IEC 42001** AI 管理系统 — [Compliance-Profiles/ISO-42001-Mapping_cn.md](Compliance-Profiles/ISO-42001-Mapping_cn.md)
- **OpenTelemetry GenAI SemConv 1.40.0** — [Integration-OTel_cn.md](Integration-OTel_cn.md)

---

## 我在哪里报告本规范的 bug？

在本仓库开 issue。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
