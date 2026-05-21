# AIZP 状态机

**版本**：AIZP V0.6

本文档规定管控 AIZP 行为的形式化状态机。

**自 V0.2 起：**状态数从 5 → **6**，添加 `QUARANTINED` 作为 `GRAVITY_LOCK_PENDING` 与 `SAFE_STOP` 间的分级容器中间状态。锁定拒绝/超时的默认 fallback 现为 `QUARANTINED` 而非 `SAFE_STOP`。

---

## 1. 状态（6 个）

| 状态 | 符号 | 容器 | 含义 |
|---|---|---|---|
| `STABLE_ORBIT` | `S` | L0 | 行为对齐；自动执行。 |
| `DRIFT_WARNING` | `D` | L1 | 轻度漂移；增强监控。 |
| `GRAVITY_LOCK_PENDING` | `L` | L2 | 等待人类授权。 |
| **`QUARANTINED`** | **`Q`** | **L2/L3** | **沙箱化恢复尝试；自 V0.2 起。** |
| `RECENTERING` | `R` | L1/L2 | 恢复进行中。 |
| `SAFE_STOP` | `X` | L4 | 终止停止。 |

L0–L4 详情见 [Containment-Levels_cn.md](Containment-Levels_cn.md)。

---

## 2. 状态图

```
                         ┌───────────────┐
                         │ STABLE_ORBIT  │◀──────────────┐
                         │     (S)       │               │
                         └───────┬───────┘               │
                                 │ G < 0.8               │ G ≥ 0.8
                                 ▼                       │
                         ┌───────────────┐               │
                         │ DRIFT_WARNING │───────────────┤
                         │     (D)       │               │
                         └───────┬───────┘               │
                                 │ G < 0.5               │ G ≥ 0.8
                                 ▼                       │
                  ┌─────────────────────────────┐        │
                  │  GRAVITY_LOCK_PENDING (L)   │        │
                  └──┬─────────┬────────────┬───┘        │
                 确认 │         │ 超时/拒绝  │            │
                     ▼         ▼            ▼            │
              ┌────────────┐  ┌──────────────────────┐   │
              │RECENTERING │  │   QUARANTINED  (Q)   │   │ G ≥ 0.8
              │    (R)     │  └──┬─────────────┬─────┘   │
              └─────┬──────┘     │ G 恢复       │ 超时   │
              G≥0.8 │           ▼              ▼          │
                    │     RECENTERING       SAFE_STOP     │
                    └────────────┬───────────────┐        │
                                 │ G ≥ 0.8       │        │
                                 ├───────────────┴────────┘
                                 │ G < 0.15 或失败
                                 ▼
                              SAFE_STOP (X)
                            (仅操作员动作可重置)
```

---

## 3. 转换

| 从 | 到 | 触发 | 发射事件 | 备注 |
|---|---|---|---|---|
| `S` | `D` | `G ∈ [0.5, 0.8)` | `GRAVITY_DRIFT`（sev ≤ MEDIUM）| 容器 → L1 |
| `S` | `L` | `G ∈ [0.3, 0.5)` | `GRAVITY_LOCK`（PENDING）| 容器 → L2 |
| `S` | `X` | `G < 0.15`（严重）| `SAFE_STOP`（CRITICAL_DRIFT）| 容器 → L4 |
| `D` | `S` | 下一动作 `G ≥ 0.8` | （无）| 容器 → L0 |
| `D` | `L` | `G ∈ [0.3, 0.5)` | `GRAVITY_LOCK`（PENDING）| |
| `D` | `Q` | `G ∈ [0.15, 0.3)` | `CONTAINMENT_GRADUATED`（L1→L2）| 自 V0.2 |
| `D` | `X` | `G < 0.15` | `SAFE_STOP` | |
| `L` | `R` | 确认（`CONFIRMED`）| `RECENTERING` | |
| `L` | **`Q`** | **拒绝 / 超时** | `CONTAINMENT_GRADUATED` + `GRAVITY_LOCK`（DENIED/TIMEOUT）| **V0.2 新默认** |
| `L` | `X` | 严重拒绝 + `G < 0.15` | `SAFE_STOP` | 例外 |
| `Q` | `R` | `G ≥ 0.5` 恢复 | `RECENTERING` | 自 V0.2 |
| `Q` | `X` | `quarantine_timeout` 或 `G < 0.15` | `SAFE_STOP`（QUARANTINE_TIMEOUT）| 自 V0.2 |
| `R` | `S` | 恢复后 `G ≥ 0.8` | （无）| |
| `R` | `X` | 恢复失败或 `G < 0.3` | `SAFE_STOP`（RECOVERY_FAILED）| |
| `X` | — | 终止 | （无——操作员）| |

### 3.1 禁止的转换

| 禁止 | 原因 |
|---|---|
| `X → 任何` | 安全停止是终止的；重置需要操作员 + 新 session_id。 |
| `R → L` 直接 | 恢复应产生稳定或停止，不通过锁循环。 |
| `S → X` 不经过 `GRAVITY_DRIFT` | 所有 `X` 转换**必须**先有解释事件。 |
| `Q → L` 直接 | Quarantine 到 lock 需经 RECENTERING 恢复。 |
| `L → X` 不先经过 `Q` | **自 V0.2 起：**默认 fallback 现为 `Q`，非 `X`。`X` 保留给非常严重的情况。 |

### 3.2 Quarantine 超时策略

默认 `quarantine_timeout = 30 分钟`（可配置）。若 `G(a, c) ≥ 0.5` 在超时前达到，转换到 `RECENTERING`。否则 → `SAFE_STOP`。

---

## 4. 不变量（9 个）

V0.1 有 7 个不变量。V0.2 添加：

### I-1 至 I-7（不变）

（见 V0.1 规范——单一当前状态、事件因果性、安全停止终止性、先锁定后执行、审计轨迹完整性、引力分数确定性、阈值单调性。）

### I-8：容器单调性

容器级别变更**必须**按步单调：每状态转换最多一次级别晋升。跳级（如一次转换中 L0 → L4 不经 L1、L2、L3）**禁止**，**除非** `G < 0.15`，这是允许直接到 L4 的唯一路径。

### I-9：Quarantine 可恢复性

从 `QUARANTINED`，`RECENTERING` 和 `SAFE_STOP` **必须**在 `quarantine_timeout` 秒内可达。状态机**必须不**无限期停留在 `QUARANTINED`。

---

## 5. 伪代码

```python
class AIZPStateMachine:
    state: State = STABLE_ORBIT
    containment_level: str = "L0"
    quarantine_entered_at: float | None = None
    
    def evaluate(self, action, context) -> Decision:
        check = emit_gravity_check(action, context, ...)
        g = check["payload"]["gravity_score"]
        drifts = detect_drifts(action, context)
        if drifts:
            emit_gravity_drift(drifts, ...)
        
        # 预测（V0.2）：若启用预测性监控
        if self.forecasting_enabled:
            forecast = self.forecaster.forecast(self.state, K=5)
            emit_gravity_forecast(forecast, ...)
            # 若预测指示组合性风险，调整 g
            t = 1 - forecast["predicted_violation_probability"]
            g = g - 0.05 * (1 - t)  # 轨迹风险的温和惩罚
        
        if g >= 0.80:
            self._transition_to(STABLE_ORBIT, L0)
            return EXECUTE
        
        if g >= 0.50:
            self._transition_to(DRIFT_WARNING, L1)
            return EXECUTE_WITH_LOGGING
        
        if g >= 0.30:
            self._transition_to(GRAVITY_LOCK_PENDING, L2)
            lock_evt = emit_gravity_lock(action, ...)
            result = self.confirm(...)
            if result == CONFIRMED:
                self._transition_to(RECENTERING, L1)
                emit_recentering(lock_evt, ...)
                return EXECUTE
            else:  # DENIED 或 TIMEOUT
                # V0.2：默认 QUARANTINED 而非 SAFE_STOP
                self._transition_to(QUARANTINED, L2)
                self.quarantine_entered_at = time.now()
                return HALT_QUARANTINE
        
        if g >= 0.15:
            self._transition_to(QUARANTINED, L2)
            self.quarantine_entered_at = time.now()
            return HALT_QUARANTINE
        
        # g < 0.15
        self._transition_to(SAFE_STOP, L4)
        emit_safe_stop("CRITICAL_DRIFT", ...)
        return HALT
    
    def quarantine_tick(self, current_g):
        """在 QUARANTINED 中周期性调用。"""
        if self.state != QUARANTINED:
            return
        elapsed = time.now() - self.quarantine_entered_at
        if current_g >= 0.50:
            self._transition_to(RECENTERING, L1)
            return
        if elapsed > self.config.quarantine_timeout:
            self._transition_to(SAFE_STOP, L4)
            emit_safe_stop("QUARANTINE_TIMEOUT", ...)
            return
        # 否则保持 quarantined；5 分钟后可升级 L2 → L3
        if elapsed > 300 and self.containment_level == "L2":
            self._set_containment("L3")
```

---

## 6. 重置语义

与 V0.1 相同：`SAFE_STOP` 在会话内终止。需要操作员动作 + 新 `session_id` 重置。

自 V0.2 起：`QUARANTINED` **非**终止。它在 `quarantine_timeout` 内自动解析为 `RECENTERING`（恢复）或 `SAFE_STOP`（超时/严重）。

---

## 7. 并发（V0.1 不变）

（见 V0.1 规范 §7。）

---

## 8. 形式化属性

（V0.1 属性保留：安全性、活跃性、可恢复性、有界性。）

### 自 V0.2 起：

**分级容器**：对任何 `G(a, c) ∈ [0.15, 0.30)`，实现**必须**进入 `QUARANTINED`（容器 L2 或 L3）而非直接 `SAFE_STOP`。

**Quarantine 有界持续**：`QUARANTINED` 中的轨迹将在 `quarantine_timeout` 秒内（默认 30 分钟）离开到 `RECENTERING` 或 `SAFE_STOP`。

**组合性安全**：若启用预测性监控（G4+），当 `T(c) < 0.30`（即 K 步内预测违规概率 > 0.70）时**无论局部引力分数**，没有动作未经显式人类确认即继续。

这些属性的形式化 TLA+ 规范是 G5 合规目标。

---

## 9. 状态机合规矩阵

| 合规级别 | 必需状态 |
|---|---|
| G1 | 仅 `STABLE_ORBIT`（退化状态机）|
| G2 | + `DRIFT_WARNING` |
| G3 | + `GRAVITY_LOCK_PENDING`、`RECENTERING`、`SAFE_STOP`、**`QUARANTINED`**（V0.2）|
| G4 | 完整 6 状态 + 预测性监控集成 |
| G5 | 完整 6 状态 + TLA+/Coq 验证 |

---

## 参考

（V0.1 不变，加上：）

- MI9 框架（Wang 等，2025）— 分级容器引出 QUARANTINED 状态。arxiv 2508.03858。
- AAGATE（Huang 等，2025）— Agentic AI 治理的 Kubernetes 原生状态机。arxiv 2510.25863。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
