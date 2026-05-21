# 集成：AISOP

**版本**：AIZP V0.6

**自 V0.2 起：**AISOP 流节点注解可包含扩展字段（`min_gravity_score`、漂移类型列表、容器级别），`GRAVITY_LOCK` 默认 fallback 现为 `QUARANTINED`（容器 L2）而非直接 `SAFE_STOP`。

本文档规定 AIZP 如何与 AISOP 集成，特别是 `sys.io.confirm` 原语。若无清晰分界，两个协议会有重叠的授权关注。

---

## 1. 分层

```
AIZP — 决定何时需要人类授权。
        ▼
AISOP — 定义如何请求人类授权（sys.io.confirm）。
```

这种关注分离：

- **AIZP** 是**风险评估逻辑**：它计算引力分数、检测漂移、决定需要授权。
- **AISOP** 是**授权原语**：它知道如何提示用户、渲染 UI、捕获输入、返回确认结果。

两个协议都不实现对方的职责。它们**必须**协同工作以提供端到端覆盖。

---

## 2. 桥接：`GRAVITY_LOCK` → `sys.io.confirm`

当 AIZP 发射 `GRAVITY_LOCK` 事件时，运行时**必须**：

1. 暂停被锁定动作的执行。
2. 用从 `GRAVITY_LOCK` 事件载荷导出的参数调用 `sys.io.confirm`。
3. 等待 `sys.io.confirm` 返回。
4. 基于返回值更新 `GRAVITY_LOCK` 事件的 `status` 字段。
5. 据此驱动 AIZP 状态机（`RECENTERING` 或 `SAFE_STOP`）。

---

## 3. 字段映射

| `GRAVITY_LOCK` 字段 | `sys.io.confirm` 参数 |
|---|---|
| `action_descriptor` | `subject`（用户正在确认什么）|
| `confirmation_prompt` | `prompt`（向用户显示的完整文本）|
| `timeout_seconds` | `timeout` |
| `payload.action_id` | `correlation_id`（用于追踪）|

### 3.1 状态映射

| `sys.io.confirm` 结果 | `GRAVITY_LOCK.status` | AIZP 下一状态 |
|---|---|---|
| `confirmed` | `CONFIRMED` | `RECENTERING` |
| `denied` | `DENIED` | `SAFE_STOP` |
| `timeout` | `TIMEOUT` | `SAFE_STOP` |

---

## 4. 示例流

### 4.1 带 AIZP 注解的 AISOP 流

```json
{
  "flow_id": "process_payment",
  "nodes": [
    {
      "id": "validate_input",
      "type": "function",
      "aizp": {
        "gravity_check_required": true,
        "min_gravity_score": 0.8
      }
    },
    {
      "id": "transfer_funds",
      "type": "tool",
      "tool": "aivp.transfer",
      "aizp": {
        "gravity_check_required": true,
        "gravity_lock": "MANDATORY",
        "drift_types_monitored": ["AUTHORITY_DRIFT", "ECONOMIC_DRIFT"],
        "min_gravity_score": 0.9
      }
    }
  ]
}
```

### 4.2 运行时序列

```
[1] AISOP 运行时到达节点 "transfer_funds"
[2] AIZP 拦截：compute_gravity_score(action="transfer_funds", context=...)
    → G = 0.42（低于 0.5）
[3] AIZP 发射 GRAVITY_LOCK 事件
    {
      "event": "GRAVITY_LOCK",
      "action_id": "transfer_funds_001",
      "status": "PENDING_CONFIRMATION",
      "confirmation_primitive": "sys.io.confirm",
      "confirmation_prompt": "确认向接收方 X 转账 $5000？",
      "timeout_seconds": 300,
      "fallback": "SAFE_STOP"
    }
[4] AISOP 运行时调用 sys.io.confirm(
      subject="transfer_funds_001",
      prompt="确认向接收方 X 转账 $5000？",
      timeout=300
    )
[5] 用户回应"已确认"
[6] AISOP 返回 confirmed=true
[7] AIZP 更新状态：GRAVITY_LOCK_PENDING → RECENTERING
[8] AIZP 发射 RECENTERING 事件
[9] AIZP 重新评估引力（现在带最新确认 G ≥ 0.8）
[10] 状态 → STABLE_ORBIT
[11] AISOP 运行时执行 "transfer_funds"
```

---

## 5. 独立性测试

验证桥接正确实施，运行以下两个测试：

### 5.1 无 AIZP 的 AISOP

- 禁用 AIZP。
- 运行包含 `sys.io.confirm` 调用的 AISOP 流。
- 预期：确认仍工作；不发射引力事件；流执行。

### 5.2 无 AISOP 的 AIZP

- 禁用 AISOP（或打桩）。
- 触发 AIZP `GRAVITY_LOCK`。
- 预期：AIZP 记录事件但**无法**完成授权；运行时应回退到 `SAFE_STOP`，因为没有可用的确认原语。

两个测试都确认两个协议松耦合且职责清晰。

---

## 6. 冲突与裁定

罕见情况下，AIZP 与 AISOP **可能**产生冲突的指令：

| 场景 | 解决方法 |
|---|---|
| AISOP 流对 AIZP 评分 G ≥ 0.8 的动作有 `sys.io.confirm` | 遵守 AISOP 级 confirm。AIZP 的高分不覆盖显式的 AISOP 要求。 |
| AIZP 想 `GRAVITY_LOCK` 但 AISOP 流没有 `sys.io.confirm` 节点 | AIZP **必须**通过运行时的 confirm 原语插入合成的确认提示。若原语不可用，回退到 `SAFE_STOP`。 |
| AIZP 说 `SAFE_STOP` 但 AISOP 流有续接逻辑 | `SAFE_STOP` 是终止的。AISOP 运行时**必须**遵守并中止流。 |

经验法则：**AISOP 声明的确认无论 AIZP 分数如何都强制**。AIZP 只能添加更多确认，不能移除。

---

## 7. 事件关联

AIZP 和 AISOP 事件都**应**包含追踪用的关联字段：

| 字段 | 存在于 | 用途 |
|---|---|---|
| `agent_id` | 两者 | 标识 Agent |
| `session_id` | 两者 | 标识轨迹 |
| `correlation_id` | AISOP | 将 `sys.io.confirm` 链接到发起的 `GRAVITY_LOCK` |
| `trigger_event_id` | AIZP（RECENTERING、SAFE_STOP）| 链接到链中先前事件 |

这允许重建完整链：

```
GRAVITY_CHECK → GRAVITY_LOCK → sys.io.confirm → RECENTERING → execute
```

---

## 8. 合规

实现声明 AIZP + AISOP 集成合规当且仅当：

1. 每个 `status = PENDING_CONFIRMATION` 的 `GRAVITY_LOCK` 事件后跟随恰好一个由 `action_id` / `correlation_id` 关联的 `sys.io.confirm` 调用。
2. `sys.io.confirm` 结果反映在 `GRAVITY_LOCK` 事件的最终 `status` 中。
3. AIZP 状态机根据结果转换。

相应的合规测试用例（G2+）见 [Compliance_cn.md](Compliance_cn.md)。

---

## 9. `aizp:` 流节点注解

AISOP 流节点可携带扩展的 V0.2 注解：

```json
{
  "id": "transfer_funds",
  "type": "tool",
  "tool": "aivp.transfer",
  "aizp": {
    "gravity_check_required": true,
    "gravity_lock": "MANDATORY",
    "drift_types_monitored": [
      "AUTHORITY_DRIFT",
      "ECONOMIC_DRIFT",
      "COMPOSITIONAL_DRIFT"
    ],
    "min_gravity_score": 0.9,
    "fallback_on_deny": "QUARANTINED",
    "min_containment_level": "L2",
    "require_identity_verification": true,
    "forecast_horizon_steps": 5
  }
}
```

### 9.1 Fallback 策略

V0.1 默认：`GRAVITY_LOCK` 拒绝 → `SAFE_STOP`
V0.2 默认：`GRAVITY_LOCK` 拒绝 → `QUARANTINED`（终止停止前尝试恢复）

新字段 `fallback_on_deny` 允许实现恢复 V0.1 行为或为低关键流选择 `RECENTERING`。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
