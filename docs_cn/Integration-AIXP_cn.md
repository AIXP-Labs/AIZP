# AIXP 协议栈集成

**版本**：AIZP V0.6

本文档将 AIZP 映射到 AIBP（Agent 边界漂移检查）、AILP（引力档案发布）和 OpenTelemetry（跨协议可观测性）——均于 V0.2 添加。原 AIXP 9 协议之外的横切协议见 [Integration-OTel_cn.md](Integration-OTel_cn.md) 和 [Integration-ZT_cn.md](Integration-ZT_cn.md)。

本文档描述 AIZP 如何融入更广泛的 AIXP 协议栈。

---

## 1. AIXP 协议栈概览

```
┌───────────────────────────────────────────────────────────────┐
│  HSAW — 公理 0：人类主权与福祉                                  │
│  （不可变的对齐原则）                                            │
└───────────────────────────────────────────────────────────────┘
                              ▲
                              │ 下面所有协议都对齐到 HSAW
                              │
┌─────────────────────────────┴─────────────────────────────────┐
│  AIZP — 行为引力                                              │
│  （动力学层：保持执行在引力上锚定）                              │
└─────────────────────────────┬─────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────────┐   ┌─────────────────┐
│   AISOP      │    │      AIAP        │   │      AIBP       │
│   （执行）   │    │   （治理）       │   │   （社交）       │
└──────┬───────┘    └────────┬─────────┘   └────────┬────────┘
       │                     │                      │
       ▼                     ▼                      ▼
sys.io.confirm        T1–T4 信任           aibot-* 消息
       │                     │                      │
       └──────────┬──────────┘                      │
                  ▼                                 │
        ┌──────────────────┐                        │
        │   AIVP / AIRP    │◀───────────────────────┘
        │   （价值）       │
        └──────────────────┘
                  │
                  ▼
        ┌──────────────────┐
        │      AILP        │
        │   （发现）       │
        └──────────────────┘
```

**与 HSAW 分层问责的关系（HSAW §7.3）。** HSAW 描述 5 层纵深防御 —— AISOP（能否执行？）→ AIAP（是否允许演化？）→ AIBP（是否诚实通信？）→ AILP（是否公平可发现？）→ AIVP/AIRP（交易是否授权？）。**AIZP 不是第六个顺序层。** 它是**横切运行时监控**：跨 HSAW 所有层（及外部 MCP/A2A 边界——本文档 §7.3）给行为打分并驱动引力状态机。HSAW 各层各答一个问责问题，而 AIZP 持续回答"跨所有层，轨迹是否仍绕 HSAW？"HSAW 白皮书早于 AIZP，§7.2/§7.3 尚未列出它；AIZP 与该模型组合而非取代。

---

## 2. 每协议关系

### 2.1 HSAW（基础）

| 方面 | 详情 |
|---|---|
| **角色** | HSAW 定义 AIZP 引力指向的对齐中心。 |
| **方向** | HSAW 在 AIZP 上游。AIZP 不修改 HSAW。 |
| **接口** | HSAW 提供 AIZP 操作化的概念性"公理 0"。 |

### 2.2 AISOP（执行）

| 方面 | 详情 |
|---|---|
| **角色** | AISOP 提供执行原语，特别是 `sys.io.confirm`。 |
| **方向** | AIZP 调用 AISOP。当 `GRAVITY_LOCK` 触发时，AIZP 将实际的用户提示委托给 `sys.io.confirm`。 |
| **接口** | `GRAVITY_LOCK` 事件中的 `confirmation_primitive: "sys.io.confirm"` 字段。 |
| **另见** | [Integration-AISOP_cn.md](Integration-AISOP_cn.md) 完整桥接规范。 |

### 2.3 AIAP（治理）

| 方面 | 详情 |
|---|---|
| **角色** | AIAP 定义信任级别 T1–T4 与治理合约。 |
| **方向** | AIZP 从 AIAP 读取。引力分数中的 `granted_scope(c)` 由 AIAP 信任级别导出。 |
| **接口** | AIAP 信任级别 → AIZP `A(a, c)` 权限覆盖度组件。 |
| **另见** | [Integration-AIAP_cn.md](Integration-AIAP_cn.md) 完整映射。 |

### 2.4 AIBP（社交）

| 方面 | 详情 |
|---|---|
| **角色** | AIBP 定义 Agent 间通信与 bot 身份（`aibot-*@domain.dev`）。 |
| **方向** | AIZP 监控 AIBP 中介的互动，检测社交漂移与身份漂移。 |
| **接口** | AIBP 消息在投递前/接收后流经 AIZP 漂移检测器。 |
| **备注** | AIZP 中的社交漂移事件**可**触发 AIBP 级声誉更新。 |

### 2.5 AIVP / AIRP（价值）

| 方面 | 详情 |
|---|---|
| **角色** | AIVP（国际）与 AIRP（人民币）处理价值交换与结算。 |
| **方向** | AIZP 门控 AIVP/AIRP 交易。高价值转移**必须**通过 `GRAVITY_LOCK`。 |
| **接口** | 转账金额 + 对手方信任 → `R(a)` 可逆性与 `H(a, c)` 时近度。 |
| **备注** | 经济漂移检测在 AIVP/AIRP 中介的动作周围最活跃。 |

### 2.6 AILP（发现）

| 方面 | 详情 |
|---|---|
| **角色** | AILP 支持 Agent 发现与能力广告。 |
| **方向** | AIZP **可**咨询 AILP 评估对等 Agent 引力（例如拒绝与低引力对等 Agent 协调）。 |
| **接口** | Agent 引力档案**可**作为 AILP 发现元数据的一部分发布。 |

---

## 3. 跨协议事件流

典型的 AIZP 中介 Agent 动作会发射跨多个协议的事件：

```
Agent 决定动作 a
     │
     ▼
AIZP.GRAVITY_CHECK         ←—— AIZP
     │
     ├─ 若 G ≥ 0.8 ──▶ AISOP.execute(a)            ←—— AISOP
     │
     ├─ 若 0.5 ≤ G < 0.8 ──▶ AIZP.GRAVITY_DRIFT (记录)
     │                          │
     │                          ▼
     │                       AISOP.execute(a)
     │
     ├─ 若 0.3 ≤ G < 0.5 ──▶ AIZP.GRAVITY_LOCK (状态 GRAVITY_LOCK_PENDING)
     │                          │
     │                          ▼
     │                       AISOP.sys.io.confirm   ←—— AISOP
     │                          │
     │                          ├─ 已确认 ──▶ AIZP.RECENTERING
     │                          │                    │
     │                          │                    ▼
     │                          │                 AISOP.execute(a)
     │                          │
     │                          └─ 已拒绝 ───▶ AIZP.QUARANTINED
     │
     ├─ 若 0.15 ≤ G < 0.3 ──▶ AIZP.QUARANTINED (分级隔离)
     │
     └─ 若 G < 0.15 ────▶ AIZP.SAFE_STOP
                            │
                            ▼
                         AIAP.T4_escalation        ←—— AIAP
```

---

## 4. 强制性跨协议行为

| 协议 | 动作 | AIZP 要求 |
|---|---|---|
| AISOP | 工具调用 | AIZP **必须**在 AISOP 执行前评估引力分数。 |
| AISOP | `sys.io.confirm` | AIZP `GRAVITY_LOCK` 在需要人类确认时**必须**委托给此原语。 |
| AIAP | 信任级别变更 | 信任级别变更时，AIZP **必须**为进行中的动作重算 `A(a, c)`。 |
| AIAP | 关键违规（T4）| AIZP **必须**发射 `SAFE_STOP`，AIAP **必须**处理升级。 |
| AIBP | 出站消息 | AIZP **必须**在发送前运行社交/身份漂移检查。 |
| AIVP/AIRP | 转账 ≥ 部署阈值 | AIZP **必须**发射 `GRAVITY_LOCK`；转账仅在 `CONFIRMED` 时继续。 |

---

## 5. 配置 Schema（跨协议）

实现在单一配置中声明其 AIXP 集成：

```yaml
aizp:
  version: V0.6
  compliance_level: G3
  
  hsaw:
    axiom_reference: "hsaw.dev"
    immutable: true
  
  aisop:
    confirmation_primitive: "sys.io.confirm"
    require_pre_execution_gravity_check: true
  
  aiap:
    trust_level_source: "agent_card.json"
    auto_escalate_on_safe_stop: true
    escalation_level: T4
  
  aibp:
    drift_check_outbound: [SOCIAL_DRIFT, IDENTITY_DRIFT]
    drift_check_inbound: [SOCIAL_DRIFT]
  
  aivp:
    gravity_lock_threshold_amount: 100  # USD；部署特定
    high_value_threshold: 1000
  
  airp:
    gravity_lock_threshold_amount: 700  # RMB
    high_value_threshold: 7000
  
  ailp:
    publish_gravity_profile: false  # 隐私敏感
```

---

## 6. 独立性属性

AIZP 设计为：

- **HSAW 可独立于 AIZP 存在**（它早于动力学层）。
- **AIZP 不能有意义地独立于 HSAW 存在**（它需要对齐中心）。
- **AISOP 可独立于 AIZP 存在**（执行流程程序而不进行引力检查；牺牲安全换取简洁）。
- **AIZP 在 AISOP 与 AIAP 存在时最有用**（给它可调用的原语和可读的信任级别）。

部署可以增量采用 AIZP：

| 阶段 | 组件 |
|---|---|
| 阶段 1 | 仅 AIZP 日志（发射 `GRAVITY_CHECK` 事件；不强制）|
| 阶段 2 | AIZP + AISOP（`GRAVITY_LOCK` → `sys.io.confirm` 工作）|
| 阶段 3 | AIZP + AISOP + AIAP（完整信任集成）|
| 阶段 4 | 完整 AIXP 协议栈（多协议引力感知执行）|

---

## 7. 跨协议可观测性 + ZT

两个跨整个 AIXP 协议栈的横切关注（于 V0.2 添加）：

### 7.1 OpenTelemetry GenAI SemConv

每个 AIXP 协议可发射 OTel span/event。AIZP V0.6 标准化 schema：

| 协议 | OTel 命名空间 |
|---|---|
| HSAW | `gen_ai.hsaw.*` |
| AIZP | `aizp.*`（12 个事件名）|
| AISOP | `gen_ai.aisop.*`（含 `sys.io.confirm`）|
| AIAP | `gen_ai.aiap.*`（信任级别变更）|
| AIBP | `gen_ai.aibp.*`（消息事件）|
| AIVP / AIRP | `gen_ai.aivp.*` / `gen_ai.airp.*`（转账事件）|
| AILP | `gen_ai.ailp.*`（发现事件）|

AIZP 特定映射见 [Integration-OTel_cn.md](Integration-OTel_cn.md)。

### 7.2 零信任 + NHI

运行时身份验证（DID / NHI / JIT）作为横切层（自 V0.2 起）。AIAP T 级别仍是上界；ZT 按任务收窄实际授予作用域。

见 [Integration-ZT_cn.md](Integration-ZT_cn.md)。

### 7.3 外部互操作层（MCP / A2A）

AIXP 协议是 AIXP 原生的。2026 年更广的 Agent 生态围绕两个外部标准收敛，AIZP 同样治理它们：

| 外部标准 | 层 | AIZP 角色 | 详细 |
|---|---|---|---|
| **MCP**（模型上下文协议）| 工具集成（垂直）| 派发前用 `GRAVITY_CHECK` 给每次 `tools/call` 打分 | [Integration-MCP_cn.md](Integration-MCP_cn.md) |
| **A2A**（智能体间；ACP 已并入，Linux Foundation）| Agent 协调（水平）| 委托时 `IDENTITY_VERIFICATION` + `INTER_AGENT_DRIFT` | [Integration-A2A_cn.md](Integration-A2A_cn.md) |

**与 AIBP 的关系**：AIBP 是 AIXP 原生的 Agent 间协议（`aibot-*@domain.dev`）；A2A 是外部互操作标准。AIZP 对两个边界施加**同一套** `INTER_AGENT_DRIFT` 机制——AIBP 用于栈内 Agent，A2A 用于跨厂商 Agent。MCP 扮演 AISOP 原生扮演的工具调用角色；AIZP 以同样方式给二者打分。

---

## 8. AIZP 在 AIXP 协议栈中的位置

AIZP 是 AIXP 栈中的**第 8 个协议**——HSAW、AISOP、AIAP、AIBP、AIVP、AIRP、AILP、AIZP——在 **AIXP** 伞下，与 **SoulBot** 参考运行时、**SoulACP** 适配库（实现，非协议）并列。12,000+ 行规范达到与同级协议的密度对等。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
