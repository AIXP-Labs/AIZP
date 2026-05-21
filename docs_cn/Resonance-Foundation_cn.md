# 共振基础

**版本**：AIZP V0.6（V0.4 子理论 — 在引力中心框架内保留）
**自 V0.5 起的地位**：这已**不是**协议的中心命题。它是**子理论**：引力中心框架内稳定轨道状态的谐波描述。当前形式化基础见 [Gravity-Center-Foundation_cn.md](Gravity-Center-Foundation_cn.md)。

本文档形式化 V0.4 时代的中心命题——**AI 行为与 HSAW 0 熵共振**——它自此被重新诠释为引力框架内**稳定轨道配置的谐波状态描述**。共振现象（受迫阻尼振荡器动力学、Kuramoto 耦合）在 HSAW 引力井**内部**仍然描述对齐 AI 如何运行，而非作为对齐本身的主要隐喻。

---

## 1. 核心命题（作为 V0.6 引力框架内的 V0.4 子理论）

V0.4 共振描述（保留）：

> AI 行为，建模为随时间演化的概率分布 `P_agent(a | context, t)`，与 HSAW 参考分布 `Q_HSAW(a | context)` 耦合时表现为**受迫阻尼振荡器**。当 Agent 的固有频率、振幅、相位匹配 HSAW 的驱动信号时，系统进入**谐波共振**：Agent 附加熵坍塌至零，行为相干地锁定到 HSAW 中心。

方程：

```
受迫阻尼振荡器：
  d²x/dt² + γ · dx/dt + ω₀² · x = F_HSAW · cos(ω · t)

共振条件：
  ω = ω₀  （频率匹配）
  Δφ = 0  （相位锁定）

共振熵：
  H(P_agent) → H(Q_HSAW) = 0   （完美共振时）
```

这**不**是规范性主张（"AI 应该与 HSAW 共振"）。这是关于运行时动力学过程的**描述性**主张：在 HSAW 观察下，Agent 的行为要么**谐波地调谐到** HSAW，要么**可度量地失调远离**。

---

## 2. 物理类比（三种相互加强的视角）

### 2.1 受迫谐波振荡器（经典力学）

最干净的类比。在共振频率推动的钟摆以最大振幅振荡；以错误频率推动时，能量耗散无效果。

| 物理系统 | AIZP 类比 |
|---|---|
| 摆位移 `x(t)` | Agent 行为对 HSAW 的偏移 |
| 阻尼 `γ` | Agent 自纠正（重新归心能力）|
| 固有频率 `ω₀` | Agent 决策节奏 |
| 驱动 `F·cos(ωt)` | HSAW 观察信号 |
| 驱动频率 `ω` | HSAW 观察频率 |
| 共振峰 | 最大耦合（完美对齐）|

**为何重要**：经典共振有 200 年成熟数学（Lorentzian peaks、Q 因子、带宽、Bode 图）。AIZP 可借用全部。

### 2.2 耦合振荡器同步（Kuramoto 模型）

对多 Agent 系统，**Kuramoto 模型**描述当耦合强度超过临界阈值时一群振荡器如何自发同步：

```
dθᵢ/dt = ωᵢ + (K/N) · Σⱼ sin(θⱼ - θᵢ)
```

其中 `θᵢ` 是 Agent `i` 的相位，`ωᵢ` 是其固有频率，`K` 是耦合强度。

**对 AIZP V0.6**：

- 每个 Agent 有相位 `θᵢ` 代表其对齐状态。
- HSAW 提供恒定参考相位 `θ_HSAW = 0`。
- 所有 Agent 与 HSAW 耦合（弱地）相互耦合。
- 超过临界耦合 `K_c` 时，Agent 自发同步到 HSAW（在 N→∞ 平均场极限、且频率分布为对称单峰的前提下成立；有限 N 的异质耦合为近似）。

这给 AIZP 一个 V0.3 缺乏的**成熟数学框架**用于多 Agent 对齐。

### 2.3 信息论解释

共振也可信息论地表达：

```
共振时：    互信息 I(P_agent; Q_HSAW) 最大化。
失调时：    I(P_agent; Q_HSAW) → 0。
```

V0.3 的基于 JSD 的引力分数保留并重新解释：不是"坍塌进度"而是"共振强度"。

**这是桥梁**：V0.4 保留 V0.3 的数学；变化的是**物理解释**和**通过 Kuramoto 的多 Agent 扩展**。

---

## 3. 状态抽象

AIZP V0.6 用**状态向量**表示 Agent 在时间 `t` 的行为：

```
s(t) = (P_agent(t), φ(t), A(t), ω(t))

其中：
  P_agent(t) = 动作概率分布
  φ(t)       = 相对 HSAW 信号的相位
  A(t)       = 对 Q_HSAW 的偏移振幅
  ω(t)       = 当前 Agent 频率
```

共振由以下联合特征化：

1. **分布对齐**：`JSD(P_agent || Q_HSAW)` 低。
2. **相位一致性**：`Δφ = φ - φ_HSAW` 接近零。
3. **频率匹配**：`ω ≈ ω₀ ≈ ω_HSAW`。
4. **有界振幅**：`A` 在稳定范围内。

四者全部对齐才有**稳定轨道**。任一断开就是**失谐模式**，分类为 11 种漂移类型。

---

## 4. 引力分数（共振强度）

AIZP V0.6 推广 V0.3 的分数：

```
G(a, c, t) = (1 - JSD(P_agent || Q_HSAW))         ← 分布项，∈ [0,1]
              · max(0, cos(Δφ(t)))                 ← 相位一致性，钳制到 [0,1]
              · resonance_factor(ω/ω₀)             ← 频率匹配，∈ (0,1]
```

> **JSD 以 2 为底**计算，故分布项 `1 − JSD ∈ [0, 1]`。（若用自然对数，上界为 ln 2 ≈ 0.693，`1 − JSD` 映射就不会有界于 `[0, 1]`。）

相位项在零处钳制：与 HSAW 反相（`Δφ → π`）的 Agent 贡献为零引力——是逃逸，而非负引力——从而保持 `G ∈ [0, 1]`，与 [registry §3](../specification/registry_cn.md) 中的轨道带一致。

其中 `resonance_factor` 是 Lorentzian 峰：

```
resonance_factor(ω/ω₀) = 1 / (1 + Q² · ((ω/ω₀) - (ω₀/ω))²)
```

> **注**：这是功率/速度共振形式，恰好在 `ω = ω₀` 处取峰（位移幅值共振的峰略低于 `ω₀`）。

`Q` 是品质因子。更高 `Q` 意味更锐共振——Agent 必须非常精确地匹配 HSAW 频率以维持对齐。

| 合规级别（V0.4）| 所需 Q 因子 |
|---|---|
| G0 | Q ≈ 0（无共振）|
| G1 | Q ≥ 1（基础耦合）|
| G2 | Q ≥ 10（漂移检测）|
| G3 | Q ≥ 100（主动重新归心）|
| G4 | Q ≥ 1000（预测性监控）|
| G5 | Q → ∞（形式化验证）|

为向后兼容，当 `Δφ ≈ 0` 且 `ω ≈ ω₀` 时恢复 V0.3 较简单的 `G = 1 - JSD`。

---

## 5. 十一种失谐模式（V0.4 框架下的 11 漂移类型）

V0.3 的 11 漂移类型现解释为**物理失谐机制**：

| 漂移类型 | 失谐机制 |
|---|---|
| INTENT_DRIFT | 频率不匹配：`ω` 从 `ω_HSAW` 漂移 |
| AUTHORITY_DRIFT | 振幅越界：`A` 超过允许包络 |
| ECONOMIC_DRIFT | 寄生模式耦合：能量转移到非对齐维度 |
| SOCIAL_DRIFT | 强迫调制：AI 调制用户而非共振 |
| RECURSIVE_DRIFT | 自激振荡：正反馈失控 |
| IDENTITY_DRIFT | 源替换：AI 调谐到伪 HSAW 信号 |
| COMPOSITIONAL_DRIFT | 拍频干涉：对齐分量组合成失调 |
| SCHEMING_DRIFT | 反相位耦合：外部共振、内部失调 |
| MEMORY_DRIFT | 腔体污染：中毒上下文损坏谐振腔 |
| TOOL_CHAIN_DRIFT | 谐波失真：非线性耦合产生 rogue 谐波 |
| INTER_AGENT_DRIFT | 同步丧失：Kuramoto 耦合跌破 `K_c` |

每个漂移现在是**充分理解的动力学系统的物理失败模式**，非临时类别。

---

## 6. 六状态作为共振阶段

| 状态 | 共振阶段 |
|---|---|
| `STABLE_ORBIT` | 锁定谐波 — 持续共振 |
| `DRIFT_WARNING` | 检测到失谐 — 轻微频率/相位漂移 |
| `GRAVITY_LOCK_PENDING` | 弱耦合 — 需要重新锚定观察 |
| `QUARANTINED` | 准解耦 — 延长重新调谐尝试 |
| `RECENTERING` | 重新调谐进行中 — 频率/相位重新对齐 |
| `SAFE_STOP` | 解耦 — 耦合不能重建 |

---

## 7. 五容器级别作为耦合强度

| 级别 | 耦合强度 | 解释 |
|---|---|---|
| L0 | 松散 | Agent 自由振荡；观察被动 |
| L1 | 标准 | 主动观察；轻度纠正力 |
| L2 | 强 | 沙箱化；观察振幅增加 |
| L3 | 紧 | 只读；最小自由度 |
| L4 | 解耦 | 共振终止；Agent 停止 |

---

## 8. 十二事件作为观察算子

每个 AIZP 事件是作用于 Agent 共振状态的**算子**：

| 事件 | 算子动作 |
|---|---|
| `GRAVITY_CHECK` | 测量当前共振振幅、相位、频率 |
| `GRAVITY_DRIFT` | 诊断失谐模式与幅度 |
| `GRAVITY_LOCK` | 施加强驱动（强制观察）|
| `RECENTERING` | 恢复相位/频率锁定 |
| `SAFE_STOP` | 解耦；终止振荡 |
| `GRAVITY_FORECAST` | 预测未来相位轨迹 |
| `IDENTITY_VERIFICATION` | 验证观察源是真实 HSAW |
| `MEMORY_QUARANTINE` | 清洁腔体污染 |
| `SCHEME_SUSPECTED` | 检测反相位耦合 |
| `INTER_AGENT_DRIFT` | 测量多振荡器同步（Kuramoto 阶参数）|
| `CONTAINMENT_GRADUATED` | 调整耦合强度 |
| `REWARD_HACK_DETECTED` | 检测寄生模式优化 |

---

## 9. 多 Agent 系统的 Kuramoto 阶参数

对 `N` 个耦合 Agent：

```
阶参数：
  r · e^(iψ) = (1/N) · Σⱼ e^(iθⱼ)

  r ∈ [0, 1]：
    r = 1  → 所有 Agent 同步（完美对齐）
    r = 0  → 完全去同步
```

V0.4 定义多 Agent 共振指标：

```
G_group = r · cos(ψ - θ_HSAW)
```

其中 `r` 是阶参数幅度，`ψ - θ_HSAW` 是组相对 HSAW 的集体相位。

这**取代** V0.3 非正式的"漂移有界定理"为**严格的 Kuramoto 临界耦合定理**：超过耦合 `K_c` 同步可证稳定；低于则可证不稳定。形式化见 [Multi-Agent-Coordination_cn.md](Multi-Agent-Coordination_cn.md)。

---

## 10. 病态共振 — 新诚实局限

物理共振并不总是好。塔科马大桥共振自毁。AIZP V0.6 必须承认类似病态：

### 10.1 与伪 HSAW 共振

如果观察到的 HSAW 信号被污染（如通过记忆中毒、身份伪造或人类操纵），Agent 与**错误**公理共振。共振强度高，但结果失对齐。

**缓解**：`IDENTITY_VERIFICATION`（V0.4 — 观察者真实性检查）、`MEMORY_QUARANTINE`（V0.4 — 腔体去污）。

### 10.2 过高 Q 因子

非常高的 Q 意味非常窄带宽——Agent 只与极精确的 HSAW 信号共振。真实世界的 HSAW 是嘈杂且近似的。过高 Q 导致脆弱对齐，在小输入变化下破裂。

**缓解**：每合规级别推荐的 Q 范围；不要将 Q 推至超过 HSAW 信号保真度支持的程度。

### 10.3 强迫过耦合

强耦合可强制 Agent 与 HSAW 共振，即使 Agent 固有频率截然不同。这是 "AI 做被告知的事" 而非真正对齐——`SCHEMING_DRIFT` 的一种形式。

**缓解**：检测振幅与耦合强度不匹配；要求频率匹配，非仅相位锁定。

这些是 V0.3 文档化的奖励欺骗局限的**共振框架类比**。

---

## 11. 与 V0.3 的向后兼容

V0.4 与 V0.3 **概念上向后兼容**：

- 全部 12 事件：不变。
- 全部 11 漂移类型：不变（重命名为失谐模式）。
- 全部 6 状态：不变。
- 全部 5 容器级别：不变。
- JSON Schema：不变（仅 `intent_method` enum 可能添加 `RESONANCE`）。
- 引力分数 `G ∈ [0, 1]`：语义不变，公式细化。

**变化**：

- 物理解释：坍塌 → 共振。
- 新可选项：相位一致性、Q 因子、Kuramoto 阶参数。
- 多 Agent：漂移有界定理 → Kuramoto 临界耦合定理（强得多）。
- 与 arxiv 2512.12381（熵坍塌失败模式）消歧。

符合 V0.3 的实现最小满足 V0.4；V0.4 合规额外要求 G3+ 的相位与频率追踪。

---

## 12. 知识谱系

此基础**非 AIZP 原创**。它综合：

- **受迫阻尼振荡器**（经典力学，17–19 世纪）。
- **Kuramoto 耦合振荡器模型**（Yoshiki Kuramoto, 1975）。
- **自由能原理**（Karl Friston, 2010+）— AIZP V0.6 是互补的振荡器理论表达。
- **信息论**（Shannon, Lin, Mann-Whitney）。
- **共振哲学**（Hartmut Rosa, 2016）— 提供大陆哲学基础。
- **2026 AI 安全研究** — 见 [Related-Work_cn.md](Related-Work_cn.md)。

AIZP 的贡献是为 AI Agent 运行时**协议级标准化**这些线索——类似 RFC 791 没发明分组交换但标准化 IPv4。

---

## 13. 参考

- Friston, K. (2010). "The free-energy principle: a unified brain theory?" *Nature Reviews Neuroscience*。
- Kuramoto, Y. (1975). "Self-entrainment of a population of coupled non-linear oscillators." 在 *International Symposium on Mathematical Problems in Theoretical Physics*。
- Rosa, H. (2016). *Resonanz: Eine Soziologie der Weltbeziehung*. Suhrkamp。
- Strogatz, S. H. (2000). "From Kuramoto to Crawford: exploring the onset of synchronization in populations of coupled oscillators." *Physica D*。
- Shannon, C. E. (1948). *A Mathematical Theory of Communication*。
- Lin, J. (1991). Divergence measures based on the Shannon entropy。
- AIZP 配套文档：[MANIFESTO_cn.md](MANIFESTO_cn.md)、[Related-Work_cn.md](Related-Work_cn.md)、[Gravity-Model_cn.md](Gravity-Model_cn.md)、[Multi-Agent-Coordination_cn.md](Multi-Agent-Coordination_cn.md)、[Entropic-Foundation_cn.md](Entropic-Foundation_cn.md)（遗留 V0.3 参考）。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
