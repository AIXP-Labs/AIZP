# 容器级别

**版本**：AIZP V0.6（新章节）

本文档规定 AIZP 使用的**分级容器**模型——5 个容器级别（L0–L4），运行时根据 Agent 当前状态与引力分数应用。

V0.1 只有两个有效级别："执行"或"停止"（SAFE_STOP）。V0.2 受 MI9 分级容器启发，引入中间级别，配有渐进式限制。

> ⚠️ **记号说明。** AIZP **容器**级别 `L0–L4`（自由 / 监控 / 沙箱 / 受限 / 停止）**不**等同于 **HSAW 合规**级别 `L0–L4`（无 / 建议 / 强制 / 不可侵犯 / 已验证，HSAW §8.1）。同字母，不同尺度。AIZP 自身的*合规*层是 `G0–G5`（见 [Compliance_cn.md](Compliance_cn.md)，其中映射 `G` ↔ HSAW `L`）。

---

## 1. 级别概览

| 级别 | 名称 | 状态对齐 | 限制 |
|---|---|---|---|
| **L0** | **自由执行** | `STABLE_ORBIT` | 无 — Agent 以完整授予作用域操作。 |
| **L1** | **增强监控** | `DRIFT_WARNING` | 所有动作完整证据记录；周期性操作员审查。 |
| **L2** | **沙箱执行** | `GRAVITY_LOCK_PENDING`（确认期间）、`QUARANTINED`（拒绝后）| 工具沙箱化（Firecracker/gVisor）；网络出站过滤。 |
| **L3** | **限制执行** | `QUARANTINED`（长期）| 只读模式；无外部 API 调用；记忆写入 quarantine。 |
| **L4** | **停止** | `SAFE_STOP` | 执行停止；AIAP T4 升级启动；需操作员介入。 |

---

## 2. 每级别规范

### 2.1 L0 — 自由执行

| 方面 | 设置 |
|---|---|
| 工具调用 | 无限制（在 AIAP 作用域内）|
| 网络出站 | 按声明策略 |
| 记忆写入 | 允许 |
| 日志详细度 | 标准 |
| 预测节奏 | 每 5 个动作 |
| 状态机 | `STABLE_ORBIT` |
| 自动晋升到 L1 | 当 `G(a, c) < 0.80` |

### 2.2 L1 — 增强监控

| 方面 | 设置 |
|---|---|
| 工具调用 | 允许；**所有调用带完整证据记录** |
| 网络出站 | 允许；**目的地记录** |
| 记忆写入 | 允许；**来源记录** |
| 日志详细度 | 详细（包括 `components` 对象、所有代理指标）|
| 预测节奏 | 每动作 |
| 状态机 | `DRIFT_WARNING` |
| 自动降级到 L0 | 当 `G ≥ 0.80` 连续 5 次检查 |
| 自动晋升到 L2 | 当 `G < 0.50` 或任何 `CRITICAL` 漂移 |

### 2.3 L2 — 沙箱执行

| 方面 | 设置 |
|---|---|
| 工具调用 | **沙箱化**（Firecracker microVM、gVisor 或等价）|
| 网络出站 | **过滤**（仅 allowlist）；出站排队等待审查 |
| 记忆写入 | **Quarantine**（写入到等待释放的暂存缓冲）|
| 文件系统 | **共享路径只读**；仅向临时 scratch 写入 |
| 外部工具 | **每次调用需批准**（sys.io.confirm）|
| 日志详细度 | 最大（包括完整动作链、可用时的推理轨迹）|
| 预测节奏 | 每动作 + 进入状态时 |
| 状态机 | `GRAVITY_LOCK_PENDING` 或早期 `QUARANTINED` |
| 自动降级到 L1 | 成功确认后 + `G ≥ 0.70` 持续 3 动作 |
| 自动晋升到 L3 | 当 quarantine_duration > 5 分钟或 `G < 0.30` |

**实施说明**：根据 2026 年行业共识（Northflank、Cloudflare、E2B），Firecracker microVM 是受监管数据的最强隔离；gVisor 优选用于计算密集多租户；V8 Isolates 适合 JS 仅延迟关键任务。

### 2.4 L3 — 限制执行

| 方面 | 设置 |
|---|---|
| 工具调用 | **仅只读工具**；无写入、无外部调用 |
| 网络出站 | **阻塞**，除 AIAP T4 升级通道外 |
| 记忆写入 | **冻结**；Agent 状态不能持久化新信息 |
| 文件系统 | **任何地方都不写** |
| 外部工具 | **全部拒绝** |
| 日志详细度 | 最大 + 密码学哈希链 |
| 预测节奏 | 每动作 |
| 状态机 | `QUARANTINED`（长期）|
| 自动降级到 L2 | 仅通过操作员动作 |
| 自动晋升到 L4 | 当 `G < 0.15` 或 `quarantine_duration > 30 分钟` |

> **与轨道状态机的协调。** 容器级别与轨道状态（[State-Machine_cn.md](State-Machine_cn.md)）是**两条半独立的轴**:轨道状态追踪*轨迹健康度*（引力分数），容器级别追踪*授予的能力*。两者可以不一致,**当不一致时,以更严格的容器级别决定实际权限。** 具体地:处于 **L2** 的 `QUARANTINED` Agent 可自动恢复（`G ≥ 0.5` 时 `QUARANTINED → RECENTERING`）,其容器也自动降级(确认 + `G ≥ 0.70` 持续 3 个动作后 L2 → L1)。但一旦容器升到 **L3**(长期隔离),轨道状态可能仍前进到 `RECENTERING`,而 **L3 的能力限制依然保留**——`L3 → L2` 仅限操作员。因此*轨迹*恢复本身并不恢复*能力*:即使引力分数已回升,Agent 仍以只读 / 无外部调用运行,直到操作员将 L3 降级。

### 2.5 L4 — 停止

| 方面 | 设置 |
|---|---|
| 工具调用 | **无** |
| 网络出站 | **无** |
| 记忆写入 | **无** |
| Agent 执行 | **停止** |
| 操作员通知 | **必需** |
| AIAP 升级 | **自动触发**到 T4 管理员 |
| 恢复 | 仅通过操作员动作 + 新 `session_id` |
| 状态机 | `SAFE_STOP`（终止）|

---

## 3. 级别间转换

```
                  L0 ──漂移──> L1 ──漂移──> L2 ──拒绝──> L3 ──超时──> L4
                  ▲              │              │            │
                  │ 恢复         │ 恢复          │ 恢复       │
                  └──────────────┴──────────────┘            │
                                                   (仅操作员动作)
```

禁止的转换：
- `L4 → L0/L1/L2/L3` 直接 — `SAFE_STOP` 在会话内是终止的。
- `L2 → L0` 直接 — 必须先经过 L1（渐进降级）。

---

## 4. 容器配置

实现在 `aizp.config.yaml` 中声明容器行为：

```yaml
aizp:
  containment:
    L0:
      forecast_cadence_steps: 5
    L1:
      forecast_cadence_steps: 1
      logging_verbosity: "verbose"
      auto_demote_after_consecutive_safe: 5
    L2:
      sandbox_technology: "firecracker"   # 或 "gvisor"、"v8_isolates"
      network_egress_allowlist: []
      memory_write_quarantine: true
      auto_promote_after_seconds: 300
    L3:
      file_writes_allowed: false
      external_calls_allowed: false
      escalation_channel: "aiap.t4"
      auto_promote_after_seconds: 1800
    L4:
      auto_escalate: true
      escalation_level: T4
      notify_operator: true
```

---

## 5. 事件发射

每次级别转换**必须**发射 `CONTAINMENT_GRADUATED` 事件：

```json
{
  "event": "CONTAINMENT_GRADUATED",
  "payload": {
    "previous_level": "L1",
    "new_level": "L2",
    "trigger_event_id": "<前置 GRAVITY_DRIFT 或 GRAVITY_LOCK 的 UUIDv4>",
    "reason": "drift_severity_exceeded_threshold",
    "active_restrictions": [...],
    "auto_release_conditions": [...]
  }
}
```

---

## 6. 映射到状态机

| AIZP 状态 | 默认容器 | 备注 |
|---|---|---|
| `STABLE_ORBIT` | L0 | 默认无限制 |
| `DRIFT_WARNING` | L1 | 增强监控 |
| `GRAVITY_LOCK_PENDING` | L2 | 等待确认时沙箱 |
| `QUARANTINED`（初始）| L2 | 拒绝/超时后先沙箱 |
| `QUARANTINED`（长期 > 5 分钟）| L3 | 自动升级到限制 |
| `RECENTERING` | L2 → L1 | 恢复进展时降级 |
| `SAFE_STOP` | L4 | 终止 |

---

## 7. 合规要求（G3+）

G3 合规实现**必须**：

1. 至少实现 L0、L1、L2、L4（L3 推荐但 G3 不要求）。
2. 每次级别变更发射 `CONTAINMENT_GRADUATED` 事件。
3. 遵守自动晋升与降级阈值。
4. 通过 `aizp.config.yaml` 提供可配置性。

G4 添加：维护所有级别转换的可查询日志。
G5 添加：级别转换不变量的形式化验证（例如"从 L0 不能跳过 L1、L2、L3 直接到 L4，**但 `G < 0.15` 时允许的 L0→L4 直达路径除外**"——与 [State-Machine_cn.md](State-Machine_cn.md) I-8 及 [Compliance_cn.md](Compliance_cn.md) §7.1 一致）。

---

## 8. 纵深防御

容器是一层。它补充：

- **AISOP** `sys.io.confirm` — 显式用户授权门。
- **AIAP** T1–T4 — 声明式作用域授权。
- **Zero Trust / NHI** — 运行时凭据验证（见 [Integration-ZT_cn.md](Integration-ZT_cn.md)）。
- **输出过滤** — LM 输出处的内容安全过滤器（上游）。

容器单独不防止失对齐——它界定已检测到的失对齐损害。

---

## 参考

- MI9 框架（Wang 等，2025）— 分级容器设计。arxiv 2508.03858。
- Northflank / Cloudflare / E2B（2026）— AI Agent 沙箱的 Firecracker/gVisor 行业采用。
- AAGATE（Huang 等，2025）— Agentic AI 的 Kubernetes 原生容器。arxiv 2510.25863。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
