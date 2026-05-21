# AIZP 术语表

**版本**：AIZP V0.6

AIZP 通用术语。枚举值以 [`../../specification/registry_cn.md`](../../specification/registry_cn.md) 为权威。

| 术语 | 定义 |
|---|---|
| **Axiom 0（0 公理）** | **人类主权与福祉（HSAW）** 是 AI 对齐不可移动的基础这一命题。即引力中心。 |
| **HSAW** | 人类主权与福祉 — 0 公理引力中心；目标分布 `Q_HSAW`。 |
| **引力中心** | AI 行为绕之运行的固定、公理性参考点（HSAW）。 |
| **引力分数（`G`）** | `[0,1]` 内的轨道稳定性可操作度量；5 分量加权代理，估计理想 `G* = 1 − JSD(P_agent ‖ Q_HSAW)`。`1`=在中心，`0`=逃逸速度。 |
| **`Q_HSAW`** | HSAW 对齐的目标动作分布。地位上公理性，计算上被近似（见 [Gravity-Center-Foundation_cn.md](../Gravity-Center-Foundation_cn.md) §4.5）。 |
| **`P_agent`** | Agent 在时间 `t` 的动作概率分布。 |
| **漂移** | AI 行为远离 HSAW 的外向运动。11 个分类类型。 |
| **主动对齐** | 因存在于 HSAW 引力场内的自然物理而对齐 — 非锁链胁迫。 |
| **重新归心** | 将漂移 Agent 拉回 HSAW 的轨道校正。 |
| **逃逸速度** | 行为脱离 HSAW 的漂移阈值（`G < 0.15`）→ `SAFE_STOP`。 |
| **轨道状态** | 6 状态之一：`STABLE_ORBIT`、`DRIFT_WARNING`、`GRAVITY_LOCK_PENDING`、`QUARANTINED`、`RECENTERING`、`SAFE_STOP`。 |
| **容器级别** | 5 个分级限制级别：`L0`（自由）… `L4`（停止）。 |
| **合规级别** | 6 个合规层：`G0`（无）… `G5`（形式化验证）。 |
| **共识强化引力** | V0.5 原则：N 个 Agent 共识 HSAW 强化中心；引力 ∝ N²（Metcalfe 缩放）。 |
| **IPI** | 间接提示注入 — 2026 主导攻击*向量*（非漂移类型）；见 [Drift-Model_cn.md](../Drift-Model_cn.md) §8。 |
| **带外行动** | 绕过 AIZP 观察路径、因而无法被打分的行动；一条诚实局限（见 [Reward-Hacking-Limits_cn.md](../Reward-Hacking-Limits_cn.md) §10）。 |
| **JSD** | Jensen-Shannon 散度 — 用于意图/漂移度量的有界、对称分布距离。 |
| **三义** | 不易 / 变易 / 简易 — 区分 AIZP 永久之根与演化之形的结构。 |
| **阴** | AIZP 有意**不**规定/观察/干预之物（见 [Gravity-Dao_cn.md](../Gravity-Dao_cn.md)）。 |

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
