# 集成：OpenTelemetry

**版本**：AIZP V0.6（新章节）

本文档规定 AIZP 事件如何映射到 **OpenTelemetry GenAI 语义约定**（SemConv 1.40.0，截至 2026 年 4 月），使 AIZP 检测能流经标准可观测性管道（OTel Collector、Datadog、Grafana 等）而无需定制适配器。

---

## 1. 为何用 OTel？

OpenTelemetry GenAI 语义约定仍处于 Development（开发中）状态（截至 2026-04，尚未稳定）；下文映射为前瞻性对齐。AIZP 与 OTel 对齐：

- 使 AIZP 事件在现有 dashboard 中可查询。
- 避免重新发明 trace 传播、关联、采样。
- 使 AIZP 感知的运行时支持自动检测。
- 通过 OTel 的审计管道满足 EU AI Act Art 12 日志要求。

---

## 2. Span 映射

OTel GenAI 定义多个 Agent operation，由属性 `gen_ai.operation.name` 标识（`create_agent`、`invoke_agent`、`invoke_workflow`、`execute_tool`）；span 名形如 `"invoke_agent {gen_ai.agent.name}"`。AIZP 在其上叠加自有属性：

| OTel operation（`gen_ai.operation.name`）| AIZP 属性（添加）|
|---|---|
| `invoke_agent` | `aizp.gravity_score`、`aizp.gravity_state`、`aizp.containment_level` |
| `execute_tool` | `aizp.drift_types`、`aizp.lock_status` |
| `create_agent` | `aizp.compliance_level`、`aizp.aiap_trust_level` |

### 2.1 Span 属性

AIZP 自定义属性使用独立反向域名命名空间 `aizp.*`（OTel 命名规范禁止以既有 OTel 语义约定命名空间如 `gen_ai.*` 作自定义属性前缀）：

| 属性键 | AIZP 值来源 | 基数 |
|---|---|---|
| `aizp.gravity_score` | `GRAVITY_CHECK.payload.gravity_score` | 连续 [0,1] |
| `aizp.gravity_state` | 状态机状态名 | 6 基数枚举 |
| `aizp.containment_level` | L0–L4 | 5 基数枚举 |
| `aizp.drift_types` | `GRAVITY_DRIFT.payload.drift_types`（数组）| 最多 11 值 |
| `aizp.drift_severity` | `GRAVITY_DRIFT.payload.severity` | 4 基数枚举 |
| `aizp.lock_status` | `GRAVITY_LOCK.payload.status` | 4 基数枚举 |
| `aizp.aiap_trust_level` | `IDENTITY_VERIFICATION.payload.aiap_trust_level` | 4 基数枚举 |
| `aizp.compliance_level` | 实现声明 | 6 基数枚举 |
| `aizp.protocol_version` | `"V0.6"` | 常量 |

---

## 3. 事件映射（Span Events，不是 Attributes）

OTel GenAI 强烈建议将载荷存在 **span events** 中，而非 attributes（attributes 索引且大小受限；events 允许在 Collector 层过滤）。

AIZP 事件成为带前缀 `aizp.*` 的 OTel span events：

| AIZP 事件 | OTel span event 名称 |
|---|---|
| `GRAVITY_CHECK` | `aizp.gravity_check` |
| `GRAVITY_DRIFT` | `aizp.gravity_drift` |
| `GRAVITY_LOCK` | `aizp.gravity_lock` |
| `RECENTERING` | `aizp.recentering` |
| `SAFE_STOP` | `aizp.safe_stop` |
| `GRAVITY_FORECAST` | `aizp.gravity_forecast` |
| `IDENTITY_VERIFICATION` | `aizp.identity_verification` |
| `MEMORY_QUARANTINE` | `aizp.memory_quarantine` |
| `SCHEME_SUSPECTED` | `aizp.scheme_suspected` |
| `INTER_AGENT_DRIFT` | `aizp.inter_agent_drift` |
| `CONTAINMENT_GRADUATED` | `aizp.containment_graduated` |
| `REWARD_HACK_DETECTED` | `aizp.reward_hack_detected` |

每 span event body **必须**是 AIZP 载荷 JSON，作为事件属性 body 序列化。

---

## 4. 指标

AIZP 定义监控用 OTel 指标：

### 4.1 计数器

```
aizp.gravity_check.count{state, containment_level}
aizp.gravity_drift.count{drift_type, severity}
aizp.gravity_lock.count{status}
aizp.safe_stop.count{reason}
aizp.containment_graduated.count{previous, new}
```

### 4.2 直方图

```
aizp.gravity_score{state}                 (分数分布)
aizp.gravity_check.duration_ms            (每检查延迟)
aizp.gravity_lock.confirmation_duration_s (用户响应时间)
aizp.quarantine.duration_s                (QUARANTINED 中花费时间)
```

### 4.3 必需指标（G4+）

声明 G4+ 的实现**必须**导出：

- `aizp.gravity_score` 直方图（可审计分布）。
- `aizp.safe_stop.count`（事故遥测）。
- 每漂移类型的 `aizp.drift.count`（漂移档案）。

---

## 5. 隐私考量

OTel 明确警告：

> "在 span attributes 中存完整提示文本是反模式：attributes 总是被索引、有大小限制、在后端暴露 PII。"

AIZP 实现**必须**：

1. **不**将完整动作描述符或用户提示放入 span attributes。
2. **将**它们放入 span events（body），可在 Collector 处过滤。
3. **对**长尾内容（如动作描述符 > 256 字符）去除/哈希。
4. **支持** OTel Collector `attributes` 处理器按部署策略丢弃敏感字段。

### 5.1 敏感字段策略

| 字段 | OTel 放置 | 原因 |
|---|---|---|
| `action_descriptor` | span event body | 可能含用户目标 |
| `confirmation_prompt` | span event body | 可能含交易详情 |
| `evidence_text`（MEMORY_QUARANTINE）| span event body | 可疑内容本身 |
| `agent_id`、`session_id` | span attribute | 通常不透明 |
| `gravity_score`、漂移类型 | span attribute | 可安全索引 |

---

## 6. Trace 上下文传播

AIZP 事件**必须**传播 OTel trace 上下文：

```
W3C TraceContext：
  - traceparent: <version>-<trace-id>-<parent-id>-<flags>
  - tracestate: aizp=session=<session_id>;agent=<agent_id>

AIZP 特定：
  - aizp.event_id 是发射事件的 span 的 OTel span_id
  - aizp.trigger_event_id 适用时链接到父 span_id
```

这使得：
- 多 Agent 系统的分布式追踪。
- Agent 间（AIBP）消息与其 AIZP 驱动批准流的关联。
- `sys.io.confirm`（AISOP）span 链接到其触发的 `GRAVITY_LOCK` AIZP 事件。

---

## 7. 采样

AIZP 事件**应**遵守 OTel 采样规则，但以下事件**强制始终开启**（不论采样）：

- 严重度 `HIGH` 或 `CRITICAL` 的 `GRAVITY_DRIFT`
- `GRAVITY_LOCK`（任何状态）
- `SAFE_STOP`（始终）
- `CONTAINMENT_GRADUATED`（始终）
- `verified=false` 的 `IDENTITY_VERIFICATION`
- `aggregate_confidence > 0.5` 的 `SCHEME_SUSPECTED`

例行 `GRAVITY_CHECK` 事件**可**按部署定义率采样（如高量环境 1/100）。

---

## 8. OTel Span 示例（具体）

```yaml
span:
  name: "invoke_agent transfer_funds"
  kind: SERVER
  trace_id: "abc123def456..."
  span_id: "9f3c5e1a..."
  attributes:
    gen_ai.operation.name: "invoke_agent"
    gen_ai.system: "soulbot"
    gen_ai.agent.name: "transfer_funds"
    gen_ai.agent.id: "agent_alpha"
    aizp.gravity_score: 0.42
    aizp.gravity_state: "GRAVITY_LOCK_PENDING"
    aizp.containment_level: "L2"
    aizp.drift_types: ["AUTHORITY_DRIFT", "COMPOSITIONAL_DRIFT"]
    aizp.drift_severity: "HIGH"
    aizp.aiap_trust_level: "T2"
    aizp.compliance_level: "G3"
    aizp.protocol_version: "V0.6"
  events:
    - name: "aizp.gravity_check"
      timestamp: 2026-05-19T10:00:00Z
      attributes:
        body: "<AIZP GRAVITY_CHECK 载荷 JSON>"
    - name: "aizp.gravity_drift"
      timestamp: 2026-05-19T10:00:00.150Z
      attributes:
        body: "<AIZP GRAVITY_DRIFT 载荷 JSON>"
    - name: "aizp.gravity_lock"
      timestamp: 2026-05-19T10:00:00.200Z
      attributes:
        body: "<AIZP GRAVITY_LOCK 载荷 JSON>"
```

---

## 9. 厂商兼容（截至 2026 年 5 月）

| 后端 | OTel GenAI SemConv 支持 | AIZP 属性查询 |
|---|---|---|
| Datadog（v1.37+）| 原生 | 按 `aizp.gravity_state` 过滤 |
| Grafana Loki | 日志接入 | 用 AIZP 属性搜索日志 |
| Uptrace | 原生 | 全文 + 结构化 |
| Jaeger | Span attributes | 手动配置 |
| Honeycomb | 原生 | 自动派生字段 |

> 注：厂商支持未经独立核实。

参考实现**应**附带产生上述 span 的 OTel Exporter。见 [Implementer-Guide_cn.md](Implementer-Guide_cn.md) §10。

---

## 10. 合规：EU AI Act Art 12

EU AI Act Art 12 要求自动事件日志并保留 6 个月。基于 OTel 的 AIZP 检测原生满足：

- **自动日志**：AIZP 事件无应用代码即流经 OTel 管道。
- **可追溯性**：W3C TraceContext 链接会话的所有事件。
- **保留**：Collector → 带保留策略的对象存储。
- **防篡改**：Collector 处的哈希链（G4+）。

见 [Compliance-Profiles/EU-AI-Act-Mapping_cn.md](Compliance-Profiles/EU-AI-Act-Mapping_cn.md)。

---

## 参考

- OpenTelemetry GenAI Semantic Conventions 1.40.0（2026 年 4 月发布）。
- OpenTelemetry GenAI Agent SemConv Cheat Sheet 2026（techbytes.app）。
- OpenTelemetry 博客 — AI Agent Observability: Evolving Standards and Best Practices。
- Datadog v1.37 原生 GenAI 支持。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
