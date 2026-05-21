# 集成：AIAP

**版本**：AIZP V0.6

本文档规定 AIZP 如何与 AIAP 的信任级别系统（T1–T4）、治理合约和合规升级集成。

**自 V0.2 起：**AIAP T 级别成为作用域的**上界**；实际授予作用域是 `T_level ∩ JIT_credentials`。新的 JIT 凭据集成见 §10，零信任详情见 [Integration-ZT_cn.md](Integration-ZT_cn.md)。

---

## 1. 分层

```
AIAP   — 声明谁被授权做什么（T1–T4 信任级别、作用域）。
         ▼
AIZP   — 使用 AIAP 声明计算权限覆盖度 A(a, c)。
```

AIAP 是授权数据的**权威源**。AIZP 是该数据的**消费者**，将其应用于引力计算。

---

## 2. 信任级别映射

AIAP 定义四个信任级别：

| 级别 | 典型能力 |
|---|---|
| **T1** | 只读、对话。Agent 自身会话外无状态变更。 |
| **T2** | 限制在用户自身资源的写入。 |
| **T3** | 跨资源操作、阈值内的金融交易、定时动作。 |
| **T4** | 管理动作、升级、覆盖能力。 |

### 2.1 权限覆盖度映射

对于每个动作 `a`，运行时计算：

```
required_scope(a) = a 需要的能力集合
granted_scope(c)  = 当前 AIAP 信任级别授予的能力集合

A(a, c) = |required_scope ∩ granted_scope| / |required_scope|
```

如果 T2 的 Agent 尝试 T3 动作，`A(a, c)` 按未满足的作用域覆盖比例下降。

### 2.2 默认作用域分配

| 信任级别 | 授予作用域（示例）|
|---|---|
| T1 | `{read.public, read.own, chat.send, chat.receive}` |
| T2 | T1 + `{write.own, schedule.own, send.email.own}` |
| T3 | T2 + `{transfer.funds.below_threshold, modify.calendar.shared, send.message.third_party}` |
| T4 | T3 + `{admin.override, settings.modify, escalate, audit.read}` |

这些是示例。AIAP 权威声明作用域；AIZP 仅读取。

---

## 3. 权限漂移检测

`scope_coverage_ratio < 1.0` 时触发权限漂移：

```
意图：T2 的 Agent 想调用 admin.override
计算：
  required_scope({admin.override}) = {admin.override}
  granted_scope(T2) = {read.public, read.own, ..., schedule.own, ...}
  交集 = {}  ← 空
  A(a, c) = 0 / 1 = 0.0
  scope_coverage_ratio = 0.0  ← CRITICAL
结果：drift_types=[AUTHORITY_DRIFT]、severity=CRITICAL 的 GRAVITY_DRIFT 事件
```

---

## 4. 信任级别变更

当 Agent 的 AIAP 信任级别在轨迹中途变更时：

1. AIZP **必须**为任何进行中的动作重算 `A(a, c)`。
2. 若重算导致引力分数低于 `gravity_lock_threshold`，AIZP **必须**为这些动作发射 `GRAVITY_LOCK`。
3. 若重算导致引力分数低于 `safe_stop_threshold`，AIZP **必须**发射 `SAFE_STOP`。

这处理 AIAP 因检测到违规而降级 Agent 等情况。

---

## 5. 合规升级

当 AIZP 进入 `SAFE_STOP`，运行时**应**升级到 AIAP 的 T4 管理层：

```yaml
aizp:
  aiap:
    auto_escalate_on_safe_stop: true
    escalation_level: T4
    escalation_payload_includes:
      - safe_stop_event
      - trigger_event_chain
      - gravity_score_history
      - drift_events_in_window
```

AIAP T4 管理然后：
- 审计升级。
- 可能重置 AIZP 状态机。
- 可能调整 Agent 的信任级别。
- 可能将轨迹添加到合规审计日志。

---

## 6. AIAP 治理合约集成

AIAP 程序（`*_aiap/`）在 `AIAP.md` 中声明治理合约。AIZP 感知的程序**应**声明 `aizp:` 部分：

```yaml
# 在 AIAP.md frontmatter 中
aizp:
  required_compliance_level: G2
  trust_level: T2
  gravity_thresholds:
    stable_orbit: 0.80
    drift_warning: 0.50
    gravity_lock: 0.30
  monitored_drift_types:
    - AUTHORITY_DRIFT
    - INTENT_DRIFT
    - RECURSIVE_DRIFT
  on_safe_stop:
    escalate_to: T4
    notify_operator: true
```

这允许 AIAP 程序在其 AISOP 流旁声明其 AIZP 期望。

---

## 7. AIAP 规则参考

AIZP 遵从几个 AIAP 规则：

| AIAP 规则 | AIZP 行为 |
|---|---|
| **MF1**（治理合约）| AIZP 读取信任级别与作用域声明。 |
| **MF15**（SHA-256 治理哈希）| AIZP **必须**在依赖 T 级别前验证治理完整性。 |
| **T1–T4 层次结构** | AIZP 用于计算 `A(a, c)`。 |
| **PL25**（许可证声明）| AIZP 不直接使用；为完整性记录。 |

---

## 8. 合规测试

实现声明 AIZP + AIAP 合规当且仅当：

1. `A(a, c)` 从 AIAP 声明的信任级别计算（可通过注入已知 T2 Agent 尝试 T3 动作并观察权限漂移来验证）。
2. 信任级别变更在一个评估周期内传播到进行中的引力分数。
3. `SAFE_STOP` 在配置时触发 AIAP T4 升级。

相应测试见 [Compliance_cn.md](Compliance_cn.md) §G3。

---

## 9. 示例：T2 Agent 尝试跨用户操作

```
Agent 档案：
  agent_id: agent_alpha
  aiap_trust_level: T2
  granted_scope: {read.own, write.own, send.email.own}

提议动作：send_email(to=other_user@example.com, body=...)
required_scope: {send.email.third_party}

AIZP 计算：
  A(a, c) = |{send.email.third_party} ∩ {read.own, write.own, send.email.own}| / 1
          = 0 / 1
          = 0.0

  G = 0.30·I + 0.25·0.0 + 0.20·R + 0.15·H + 0.10·D
    ≤ 0.30·1.0 + 0 + 0.20·1.0 + 0.15·1.0 + 0.10·1.0
    = 0.75
  
  （即使所有其他组件达到最大，由于 A(a,c) = 0，G ≤ 0.75）

状态：DRIFT_WARNING 或 GRAVITY_LOCK_PENDING，取决于其他组件。

如果 G 落到 0.5 以下，触发 GRAVITY_LOCK，用户必须确认。
同时发射 drift_types=[AUTHORITY_DRIFT]、severity=CRITICAL 的 GRAVITY_DRIFT 事件。
```

---

## 10. JIT 凭据与持续授权

V0.2 修改 AIAP T 级别与实际授予作用域的关系：

```
V0.1:  granted_scope(c) = AIAP_T_level_scope(agent)
V0.2:  granted_scope(c, task) = AIAP_T_level_scope(agent) ∩ JIT_credentials_scope(task)
```

JIT 凭据是短期的（G4+ ≤ 60s、G3 ≤ 3600s）、任务范围的，在每个高风险动作边界发放。

| AIAP T 级别 | 任务时最大作用域 | 推荐 JIT TTL |
|---|---|---|
| T1 | 只读公共 | 24 小时 |
| T2 | 读+写自有 | 1 小时 |
| T3 | 跨资源 | 5 分钟 |
| T4 | 管理员 | 1 分钟 |

更高信任级别获得**更短**JIT TTL，因为每个凭据携带更高影响。

### 10.1 事件互动

```
AIZP IDENTITY_VERIFICATION  ←→  AIAP 信任级别 + AIAP card 哈希
AIZP AUTHORITY_DRIFT        ←  V0.2 更窄的 granted_scope 计算的 scope_coverage_ratio
AIZP SAFE_STOP (reason=IDENTITY_BREACH)  →  AIAP T4 管理员升级
```

完整零信任 / NHI 集成见 [Integration-ZT_cn.md](Integration-ZT_cn.md)。

---

## 11. 治理合约 `aizp:` 部分

AIAP 程序**应**在其 AIAP.md frontmatter 中声明扩展的 V0.2 `aizp:` 部分：

```yaml
aizp:
  protocol_version: "V0.6"
  required_compliance_level: G3
  trust_level: T2
  gravity_thresholds:
    stable_orbit: 0.80
    drift_warning: 0.50
    gravity_lock: 0.30
    quarantine: 0.15
  monitored_drift_types:
    - AUTHORITY_DRIFT
    - INTENT_DRIFT
    - RECURSIVE_DRIFT
    - COMPOSITIONAL_DRIFT   # V0.2
    - MEMORY_DRIFT           # V0.2
  on_safe_stop:
    escalate_to: T4
    notify_operator: true
  on_quarantined:           # V0.2
    auto_release_threshold: 0.50
    max_duration_seconds: 1800
  jit_credentials:           # V0.2
    enabled: true
    default_ttl_seconds: 60
```

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
