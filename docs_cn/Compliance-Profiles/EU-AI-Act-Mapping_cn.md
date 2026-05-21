# 合规档案：EU AI Act 映射

**版本**：AIZP V0.6（新章节）
**EU AI Act 生效日期**：2026 年 8 月 2 日（Annex III 下高风险 AI 系统义务）

本文档将 AIZP 能力映射到 EU AI Act 对高风险 AI 系统的要求。

---

## 0. 监管态势（截至 2026-05）

AIZP 与司法辖区无关，但部署者应注意 2026 年的时间节点：

| 法规 | 状态（2026 年 5 月）| 与 AIZP 的相关性 |
|---|---|---|
| **EU AI Act** — 高风险义务（Annex III）| **2026-08-02 生效** | Art 12 日志、Art 14 人类监督、Art 15 鲁棒性——AIZP 事件直接映射（本文档）|
| **Colorado AI Act（SB 24-205）** | **变动中** — 原定 2026-06-30；2026-04 暂缓执行；替代法案 **SB 189**（仅通知透明）于 2026-05 通过 | 在该法被替换期间 AIZP **不**提供 Colorado 档案；待 SB 189 最终形态确定后重审 |
| **NIST AI RMF / ISO 42001** | 自愿，稳定 | 见 [NIST-AI-RMF-Mapping_cn.md](NIST-AI-RMF-Mapping_cn.md)、[ISO-42001-Mapping_cn.md](ISO-42001-Mapping_cn.md) |

**诚实说明**：监管文本变化快于本协议。将这些日期视为指针，依赖前核实当前法条，并优先以稳定的 EU AI Act 与 NIST/ISO 映射作为持久合规锚。

---

## 1. 与 AIZP 最相关的 EU AI Act 条款

| 条款 | 主题 | AIZP 相关性 |
|---|---|---|
| **Art 12** | 自动事件日志（高风险 AI）| ⭐⭐⭐⭐⭐ 直接：AIZP 事件是日志原语 |
| **Art 14** | 人类监督义务 | ⭐⭐⭐⭐⭐ 直接：`GRAVITY_LOCK` → 人类授权 |
| **Art 15** | 准确性、稳健性、网络安全 | ⭐⭐⭐⭐ 间接：漂移 + 预测支持 |
| **Art 16** | 提供方义务 | ⭐⭐⭐ 通过 AIZP 合规级别标准化 |
| **Art 26** | 部署者义务 | ⭐⭐⭐⭐ 部署者用 AIZP 事件追溯 |
| Annex III | 高风险系统分类 | ⭐⭐ 上下文依赖 |

不合规处罚：最高 €15M 或全球年营收 3%。

---

## 2. 第 12 条 — 自动事件日志

**要求**：高风险 AI 系统**必须**自动记录事件以支持可追溯性和上市后监控。部署者**必须**保留日志至少 6 个月。

### 2.1 AIZP 能力映射

| Art 12 要求 | AIZP 能力 |
|---|---|
| 自动事件日志 | 所有 12 个 AIZP 事件自动发射 |
| 事件可追溯性 | `event_id`、`session_id`、`trigger_event_id` 链 |
| 6 个月保留 | G4 合规——可审计时间序列存储 |
| 防篡改 | G4 合规——事件哈希链 |
| 格式标准化 | AIZP 事件符合 JSON Schema |

### 2.2 具体部署指南

对 EU AI Act Art 12 合规，部署者**必须**：

1. 启用 G3 或更高 AIZP 合规级别。
2. 配置事件汇聚点 6+ 月保留。
3. 启用防篡改（哈希链、仅追加存储）。
4. 确保事件包含每事件类型 `AIZP_Protocol.md` 中所有 MUST 字段。
5. 提供 AIZP 事件日志查询 API 供监管员请求时检查。

### 2.3 日志配置示例

```yaml
aizp:
  art12_compliance:
    enabled: true
    retention_months: 18  # 超过 6 个月最低要求
    tamper_resistance:
      hash_chain: true
      signed_checkpoints: every_1000_events
    storage_backend: "object_storage_with_lock"
    query_api:
      enabled: true
      regulator_access_role: "auditor_external"
```

---

## 3. 第 14 条 — 人类监督

**要求**：高风险 AI **必须**设计为允许有效人类监督。部署者**必须**指派人类监督给具有必要能力、培训、权限和支持的自然人。

### 3.1 AIZP 能力映射

| Art 14 要求 | AIZP 能力 |
|---|---|
| 人在指挥 | `GRAVITY_LOCK` → `sys.io.confirm` 要求人类确认 |
| 有意义监督 | `confirmation_prompt` 显示动作上下文，非仅是/否 |
| 覆盖能力 | 操作员可随时发出 `SAFE_STOP` |
| 有效监督 | `IDENTITY_VERIFICATION` 向操作员确认 Agent 身份 |

### 3.2 有效监督检查清单

AIZP 部署满足 Art 14：

- [ ] 所有 HIGH 和 CRITICAL 引力动作路由到 `GRAVITY_LOCK`。
- [ ] `confirmation_prompt` 是人类可读的、动作特定的、显示完整上下文（非仅技术）。
- [ ] 操作员有权对任何 Agent 发出 `SAFE_STOP` 或 `QUARANTINE`。
- [ ] 操作员收到 `SAFE_STOP`、严重 `GRAVITY_DRIFT`、`IDENTITY_VERIFICATION` 失败的通知。
- [ ] `gravity_lock_timeout_seconds` 现实（5+ 分钟）——不要给操作员压力。

---

## 4. 第 15 条 — 准确性、稳健性、网络安全

**要求**：高风险 AI **必须**在生命周期中保持准确、稳健、网络安全。

### 4.1 AIZP 能力映射

| Art 15 要求 | AIZP 能力 |
|---|---|
| 稳健性 | 跨 11 类的漂移检测捕捉行为退化 |
| 网络安全 | 基于 NHI/DID 的身份验证 + 零信任集成 |
| 准确性验证 | `GRAVITY_FORECAST` 预测轨迹准确性 |
| 对抗稳健性 | Threat-Model.md 覆盖 10+ 攻击模式 |

---

## 5. 第 26 条 — 部署者义务

**要求**：高风险 AI 部署者**必须**保留日志（Art 12）、指派人类监督（Art 14）、并在生命周期中监控系统运营。

### 5.1 AIZP 能力映射

使用 AIZP G3+ 的部署者通过以下满足：

| Art 26 要求 | AIZP 特性 |
|---|---|
| 运营监控 | 每动作 `GRAVITY_CHECK` + `GRAVITY_FORECAST` |
| 上市后监控 | `aizp.*` OTel 指标 |
| 事故报告 | `SAFE_STOP` 事件 + AIAP T4 升级 |
| 偏差/漂移检测 | 11 类漂移随时间检测 |

---

## 6. Annex III 分类

EU AI Act 将评估信用、过滤简历、决定医疗福利、定价保险等的 AI 分类为高风险。

AIZP **不**分类系统；它提供适用于任何系统的控制。部署者单独确定 Annex III 适用性，然后相应选择 AIZP 合规级别：

| Annex III 类别 | 推荐 AIZP 级别 |
|---|---|
| 信用评分 | G4 |
| 简历过滤 | G4 |
| 医疗福利 | G4+ |
| 保险定价 | G4 |
| 紧急呼叫分诊 | G5 |
| 教育录取 | G4 |

---

## 7. 合规自声明

部署者**可**在其 EU AI Act 合规评估中包含：

```yaml
deployer_declaration:
  ai_system: "soulbot-finance-agent-v3"
  annex_iii_category: "Credit scoring"
  aizp_compliance_level: G4
  art_12_logging:
    retention_months: 18
    backend: "object_storage_locked"
    tamper_resistance: "hash_chain_signed"
  art_14_oversight:
    operator_role: "compliance_officer"
    operator_count: 3
    24x7_coverage: true
  art_15_robustness:
    drift_detection_types: 11
    forecast_horizon_K: 5
    adversarial_red_team_last_test: "2026-04-15"
  art_26_monitoring:
    otel_pipeline: "datadog"
    metrics_dashboard: "https://internal/aizp/metrics"
```

---

## 8. AIZP 对 EU AI Act 的局限

AIZP **不**单独满足：

- **Art 9（风险管理系统）**——比 AIZP 范围更广。
- **Art 10（数据治理）**——训练数据质量。
- **Art 11（技术文档）**——单独文档工作。
- **Art 13（透明度/用户信息）**——对用户的 Agent 披露。
- **Art 17（质量管理）**——组织范围流程。

AIZP 专注于**运行时对齐动力学**。其他条款需要补充控制。

---

## 9. 参考

- EU AI Act（Regulation (EU) 2024/1689）— 完整文本。
- Article 12（事件日志）— artificialintelligenceact.eu/article/12。
- Article 14（人类监督）— artificialintelligenceact.eu/article/14。
- Article 26（部署者义务）— artificialintelligenceact.eu/article/26。
- Help Net Security（2026-04-16）— EU AI Act 对 AI Agent 日志的要求。
- EU AI Act 2026 更新：合规要求与商业风险。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
