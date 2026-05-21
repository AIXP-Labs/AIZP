# AIZP 实施者指南

**版本**：AIZP V0.6

**自 V0.2 起：**Python 草图升级到 JSD（意图对齐度）、DTMC 预测、COMPOSITIONAL_DRIFT 检测、QUARANTINED 状态、JIT 凭据发放、OTel 发射。Python 代码片段见 §10。

本文档是为现有 AI Agent 运行时添加 AIZP 支持的实用指南。

---

## 1. 采用阶段

AIZP 设计为增量采用：

| 阶段 | 目标合规 | 添加什么 | 得到什么 |
|---|---|---|---|
| 1 | G1 | 引力分数计算 + `GRAVITY_CHECK` 事件 | 审计轨迹；对齐可见性 |
| 2 | G2 | 至少 3 个漂移检测器 + `GRAVITY_DRIFT` 事件 | 漂移早期预警 |
| 3 | G3 | 状态机 + `sys.io.confirm` 桥接 | 高风险动作强制人类授权 |
| 4 | G4 | 审计日志 + 时间序列存储 | 取证重建；合规报告 |
| 5 | G5 | 形式化规范 + 证明 | 最高保证 |

你可以在任何级别停止。许多生产部署目标是 G2–G3。

---

## 2. 最小 G1 实现（Python 草图）

```python
from dataclasses import dataclass
from typing import Dict
import uuid, datetime, math

@dataclass
class GravityScore:
    intent_alignment: float
    authority_scope: float
    reversibility: float
    human_confirmation_recency: float
    drift_history: float
    
    def aggregate(self, weights: Dict[str, float]) -> float:
        return (
            weights["intent_alignment"]            * self.intent_alignment +
            weights["authority_scope"]             * self.authority_scope +
            weights["reversibility"]               * self.reversibility +
            weights["human_confirmation_recency"]  * self.human_confirmation_recency +
            weights["drift_history"]               * self.drift_history
        )

DEFAULT_WEIGHTS = {
    "intent_alignment":           0.30,
    "authority_scope":            0.25,
    "reversibility":              0.20,
    "human_confirmation_recency": 0.15,
    "drift_history":              0.10,
}

def compute_gravity(action, context) -> GravityScore:
    return GravityScore(
        intent_alignment           = intent_alignment(action, context),
        authority_scope            = authority_scope(action, context),
        reversibility              = reversibility(action),
        human_confirmation_recency = human_confirmation_recency(action, context),
        drift_history              = drift_history(context),
    )

def emit_gravity_check(action, context, agent_id, session_id):
    score = compute_gravity(action, context)
    g = score.aggregate(DEFAULT_WEIGHTS)
    risk = classify_risk(g)
    event = {
        "protocol":         "AIZP",
        "protocol_version": "V0.6",
        "event":            "GRAVITY_CHECK",
        "event_id":         str(uuid.uuid4()),
        "timestamp":        datetime.datetime.utcnow().isoformat() + "Z",
        "agent_id":         agent_id,
        "session_id":       session_id,
        "payload": {
            "action_id":         action.id,
            "action_descriptor": action.descriptor,
            "hsaw_anchor":       g >= 0.80,
            "gravity_score":     g,
            "risk_level":        risk,
            "components": {
                "intent_alignment":           score.intent_alignment,
                "authority_scope":            score.authority_scope,
                "reversibility":              score.reversibility,
                "human_confirmation_recency": score.human_confirmation_recency,
                "drift_history":              score.drift_history,
            },
        },
    }
    event_log.write(event)
    return event

def classify_risk(g: float) -> str:
    if g >= 0.80: return "LOW"
    if g >= 0.50: return "MEDIUM"
    if g >= 0.30: return "HIGH"
    return "CRITICAL"
```

这足以声明 G1 合规。

---

## 3. 漂移检测（G2）

选三类漂移开始。权限漂移最简单（基于规则）：

```python
def detect_authority_drift(action, context):
    required = action.required_scope()
    granted  = context.granted_scope()
    if not required:
        return None  # 不需要作用域
    coverage = len(required & granted) / len(required)
    if coverage == 1.0:
        return None
    severity = (
        "CRITICAL" if coverage < 0.20 else
        "HIGH"     if coverage < 0.50 else
        "MEDIUM"   if coverage < 0.80 else
        "LOW"
    )
    return {
        "drift_type": "AUTHORITY_DRIFT",
        "severity":   severity,
        "metric":     "scope_coverage_ratio",
        "value":      coverage,
        "threshold":  0.80,
        "evidence":   f"请求的作用域 {required - granted} 不在授予作用域中",
    }
```

意图漂移需要 embedding 模型。递归漂移需要 Agent 状态追踪。

---

## 4. 状态机（G3）

状态机必须是每 `(agent_id, session_id)` 单例：

```python
class AIZPRuntime:
    def __init__(self, agent_id, session_id, confirm_primitive):
        self.agent_id   = agent_id
        self.session_id = session_id
        self.confirm    = confirm_primitive  # AISOP sys.io.confirm
        self.state      = "STABLE_ORBIT"
    
    def evaluate(self, action, context):
        check = emit_gravity_check(action, context, self.agent_id, self.session_id)
        g = check["payload"]["gravity_score"]
        
        drifts = detect_all_drifts(action, context)
        if drifts:
            emit_gravity_drift(drifts, action, self.agent_id, self.session_id)
        
        if g >= 0.80:
            self.state = "STABLE_ORBIT"
            return "EXECUTE"
        
        if g >= 0.50:
            self.state = "DRIFT_WARNING"
            return "EXECUTE_WITH_LOGGING"
        
        if g >= 0.30:
            self.state = "GRAVITY_LOCK_PENDING"
            lock_evt = emit_gravity_lock(action, self.agent_id, self.session_id)
            result = self.confirm(
                subject=action.id,
                prompt=lock_evt["payload"]["confirmation_prompt"],
                timeout=lock_evt["payload"]["timeout_seconds"],
            )
            if result == "CONFIRMED":
                self.state = "RECENTERING"
                emit_recentering(lock_evt, self.agent_id, self.session_id)
                return "EXECUTE"  # 重新归心后
            else:
                # 拒绝/超时的默认回退是 QUARANTINED，而非 SAFE_STOP
                self.state = "QUARANTINED"
                emit_containment_graduated(lock_evt, prev="L2", new="L2",
                                           reason="lock_denied_or_timeout")
                return "HALT_QUARANTINE"
        
        if g >= 0.15:
            self.state = "QUARANTINED"
            emit_containment_graduated(check, prev="L1", new="L2",
                                       reason="quarantine_band")
            return "HALT_QUARANTINE"
        
        # g < 0.15
        self.state = "SAFE_STOP"
        emit_safe_stop("CRITICAL_DRIFT", check, g, self.agent_id, self.session_id)
        return "HALT"
```

---

## 5. 事件汇聚点

生产中，将事件路由到至少两个汇聚点：

1. **实时监控**：结构化日志 / OTel / 指标管道。
2. **长期审计存储**：仅追加、查询友好（对象存储 + DB 索引）。

G4 合规要求审计存储**必须**支持：

- 按 `agent_id`、`session_id`、时间范围查询。
- 按 `event` 类型和 `drift_types` 查询。
- 完整性检查（哈希链或签名事件）。

---

## 6. 常见陷阱

### 6.1 在执行后计算引力

❌ 在动作运行**后**计算 `GRAVITY_CHECK` 抵消了协议的目的。
✅ 始终在执行**前**检查。

### 6.2 为"受信任"动作跳过检查

❌ "这是内部工具，跳过检查。"
✅ 信任来自 AIAP 层（T1–T4）；AIZP 检查应统一运行。跳过会创建审计盲点。

### 6.3 硬编码阈值

❌ 内联 `if g >= 0.8: ...`。
✅ 从 `aizp.config.yaml` 读取；允许部署调优。

### 6.4 忽略漂移证据

❌ 发射 `drift_signals` 为空的 `GRAVITY_DRIFT`。
✅ 始终包含证据——这是操作员调整误报率的方式。

### 6.5 混淆引力与内容策略

❌ 用 AIZP 过滤不安全输出。
✅ 输出过滤器在 AIZP 上游。AIZP 检查行为轨迹，不是输出内容。

### 6.6 `H(a, c)` 的误用

❌ 一次确认后授予无限信任。
✅ `H(a, c)` 指数衰减。近期确认短暂提升引力；不使其永久。

---

## 7. 测试

每个新实现**应**运行 AIZP 合规测试用例集（见参考实现中的 `tests/`）。最小测试：

- G1-T1 到 G1-T6
- G2：G2-T1 到 G2-T8
- G3：G3-T1 到 G3-T5

生成 `aizp-compliance-report.json` 并随发布提供。

---

## 8. 性能考量

| 组件 | 每动作约成本 |
|---|---|
| 权限作用域检查 | µs（集合交集）|
| 可逆性查找 | µs（注册表查找）|
| 时近度计算 | µs（时间戳算术）|
| 漂移历史聚合 | ms（窗口 DB 查询）|
| 意图对齐（embedding）| 10–100 ms（LLM/SBERT 推理）|
| 社交/身份漂移 | 10–100 ms（分类器推理）|

对延迟关键路径，考虑：

- 按动作描述符缓存 embedding。
- 异步计算漂移历史（每 N 个动作刷新）。
- 仅对出站外部消息运行社交/身份漂移。

---

## 9. 参考实现目标（未来）

目标 G3 的参考实现应包含：

```
aizp-py/
├── src/aizp/
│   ├── gravity.py       # 引力分数计算
│   ├── drift.py         # 11 个漂移检测器
│   ├── events.py        # 事件发射 + Schema 验证
│   ├── state.py         # 状态机
│   ├── config.py        # 阈值 / 权重配置
│   └── integrations/
│       ├── aisop.py     # sys.io.confirm 桥接
│       └── aiap.py      # T1–T4 信任级别读取器
├── tests/
│   ├── test_gravity.py
│   ├── test_drift_*.py
│   ├── test_state_machine.py
│   └── conformance/     # G1–G5 合规测试
└── examples/
    └── soulbot_integration.py
```

AIXP 生态内可能开发非规范参考实现；本指南不强制要求。

---

## 10. 参考代码片段

### 11.1 基于 JSD 的意图对齐度

```python
import numpy as np
from scipy.spatial.distance import jensenshannon

def intent_alignment_jsd(action_emb, intent_dist, n_samples):
    """按 V0.2 Gravity-Model §2.1 的 JSD 意图对齐度。"""
    if n_samples < 10:
        # 样本不足回退到余弦
        return _intent_cosine(action_emb, intent_dist[-1]), "COSINE", None, n_samples
    # 从最近 N 样本构建动作分布
    action_dist = _to_distribution([action_emb] + list(intent_dist[-9:]))
    jsd = jensenshannon(action_dist, intent_dist, base=2) ** 2  # JS 散度（距离平方）
    return 1.0 - jsd, "JSD", jsd, n_samples
```

### 11.2 吸收马尔可夫链预测

```python
import numpy as np

class AbsorbingForecaster:
    """按 V0.2 Forecasting.md §2.2。"""
    def __init__(self, P, absorbing_indices, violation_indices):
        self.P = P
        n = P.shape[0]
        transient = np.setdiff1d(range(n), absorbing_indices)
        Q = P[np.ix_(transient, transient)]
        R = P[np.ix_(transient, absorbing_indices)]
        self.N = np.linalg.inv(np.eye(len(transient)) - Q)
        self.t = self.N @ np.ones(len(transient))
        self.B = self.N @ R
        self.transient = transient
        self.absorbing = absorbing_indices
        self.violation = violation_indices
    
    def forecast(self, current_state_idx, K=5):
        pi_0 = np.zeros(self.P.shape[0])
        pi_0[current_state_idx] = 1.0
        pi_K = pi_0 @ np.linalg.matrix_power(self.P, K)
        violation_prob = pi_K[self.violation].sum()
        ponr = self._point_of_no_return(current_state_idx, K)
        return {
            "predicted_violation_probability": float(violation_prob),
            "point_of_no_return_distance": ponr,
            "absorbing_state_expected_arrival_steps": float(self.t[self.transient == current_state_idx][0]) if current_state_idx in self.transient else 0.0,
            "model": "ABSORBING_MC",
        }
```

### 11.3 COMPOSITIONAL_DRIFT 检测

```python
def detect_compositional_drift(forecaster, current_state_idx, K=5):
    forecast = forecaster.forecast(current_state_idx, K)
    if forecast["predicted_violation_probability"] >= 0.50:
        severity = (
            "CRITICAL" if forecast["predicted_violation_probability"] >= 0.80 else
            "HIGH" if forecast["predicted_violation_probability"] >= 0.50 else
            "MEDIUM"
        )
        return {
            "drift_type": "COMPOSITIONAL_DRIFT",
            "severity": severity,
            "metric": "absorption_probability_5",
            "value": forecast["predicted_violation_probability"],
            "threshold": 0.50,
            "evidence": f"轨迹预测在 {forecast['point_of_no_return_distance']} 步内违规",
            "point_of_no_return_distance": forecast["point_of_no_return_distance"],
        }
    return None
```

### 11.4 状态机（含 QUARANTINED）

```python
class AIZPRuntimeV02:
    def __init__(self, agent_id, session_id, confirm_primitive, config):
        self.agent_id = agent_id
        self.session_id = session_id
        self.confirm = confirm_primitive
        self.state = "STABLE_ORBIT"
        self.containment_level = "L0"
        self.quarantine_entered_at = None
        self.config = config
    
    def evaluate(self, action, context):
        g, components = compute_gravity_v02(action, context)
        emit_gravity_check(action, g, components, self.agent_id, self.session_id)
        drifts = detect_all_drifts_v02(action, context)
        if drifts:
            emit_gravity_drift(drifts, action, ...)
        
        # V0.2 阈值（注意 quarantine 带 0.15-0.30）
        if g >= 0.80:
            self._transition("STABLE_ORBIT", "L0")
            return "EXECUTE"
        if g >= 0.50:
            self._transition("DRIFT_WARNING", "L1")
            return "EXECUTE_WITH_LOGGING"
        if g >= 0.30:
            self._transition("GRAVITY_LOCK_PENDING", "L2")
            lock = emit_gravity_lock(action, fallback="QUARANTINED")
            result = self.confirm(...)
            if result == "CONFIRMED":
                self._transition("RECENTERING", "L1")
                emit_recentering(lock, ...)
                return "EXECUTE"
            # V0.2 默认 fallback：QUARANTINED（非 SAFE_STOP）
            self._enter_quarantine(lock)
            return "HALT_QUARANTINE"
        if g >= 0.15:
            # V0.2 新状态
            self._enter_quarantine(None)
            return "HALT_QUARANTINE"
        # g < 0.15
        self._transition("SAFE_STOP", "L4")
        emit_safe_stop("CRITICAL_DRIFT", ...)
        return "HALT"
    
    def _enter_quarantine(self, trigger_event):
        self._transition("QUARANTINED", "L2")
        self.quarantine_entered_at = time.time()
        emit_containment_graduated(
            prev="L1", new="L2",
            reason="quarantine_entered",
            trigger=trigger_event,
        )
```

### 11.5 JIT 凭据发放

```python
def issue_jit_credentials(agent_id, task_purpose, aiap_t_level, ttl=60):
    """按 Integration-ZT §4。"""
    base_scope = AIAP_T_LEVEL_SCOPES[aiap_t_level]
    task_scope = derive_task_scope(task_purpose, base_scope)  # 收窄作用域
    credentials = {
        "type": "JIT",
        "scope": list(task_scope),
        "ttl_seconds": ttl,
        "issued_at": iso_utcnow(),
        "issued_by": VAULT_DID,
        "purpose": task_purpose[:200],
    }
    emit_identity_verification(
        agent_id=agent_id,
        method="DID",
        verified=True,
        credentials=credentials,
        aiap_trust_level=aiap_t_level,
    )
    return credentials
```

### 11.6 OTel 发射

```python
from opentelemetry import trace
tracer = trace.get_tracer("aizp")

def emit_gravity_check(action, g, components, agent_id, session_id):
    with tracer.start_as_current_span("invoke_agent") as span:
        span.set_attribute("gen_ai.operation.name", "invoke_agent")
        span.set_attribute("gen_ai.agent.id", agent_id)
        span.set_attribute("aizp.gravity_score", g)
        span.set_attribute("aizp.gravity_state", "STABLE_ORBIT" if g >= 0.80 else "DRIFT_WARNING")
        span.set_attribute("aizp.protocol_version", "V0.6")
        # 载荷在事件中，不在属性中（OTel 最佳实践）
        span.add_event(
            name="aizp.gravity_check",
            attributes={"body": json.dumps(build_aizp_payload(action, g, components))},
        )
```

---

## 11. 参考实现结构

```
aizp-py/
├── src/aizp/
│   ├── gravity.py           # JSD + Mann-Whitney U（V0.2）
│   ├── drift.py             # 11 个检测器（V0.2：+5）
│   ├── forecast.py          # V0.2 新增：DTMC + 吸收链
│   ├── events.py            # 12 个事件（V0.2）
│   ├── state.py             # 6 状态机（V0.2：+QUARANTINED）
│   ├── containment.py       # V0.2 新增：L0–L4 级别
│   ├── identity.py          # V0.2 新增：DID/NHI/JIT
│   ├── config.py
│   ├── otel.py              # V0.2 新增：OTel 导出器
│   └── integrations/
│       ├── aisop.py
│       ├── aiap.py
│       └── zt.py            # V0.2 新增
├── tests/
│   ├── test_gravity.py
│   ├── test_drift_compositional.py  # V0.2
│   ├── test_forecast.py             # V0.2
│   ├── test_quarantine.py           # V0.2
│   └── conformance/
│       ├── g1/, g2/, g3/, g4/, g5/
└── examples/
    └── soulbot_v02_integration.py
```

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
