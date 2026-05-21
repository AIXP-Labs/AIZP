# 集成：零信任 + 非人类身份

**版本**：AIZP V0.6（新章节）

本文档规定 AIZP 如何与零信任（ZT）架构和非人类身份（NHI）管理集成——2026 年自主 Agent 安全的主导范式。

到 2026 年中期，NHI 在许多企业中数量超过人类身份 40:1 到 100:1 以上，NHI 滥用已成为 **#1 网络安全威胁**（根据 WEF、CSA、HashiCorp 2026 报告）。AIZP 不能保持身份无关。

---

## 1. 身份问题

传统 IAM 为人类和静态服务账户设计。AI Agent 不同：

| 属性 | 人类用户 | 静态服务账户 | AI Agent |
|---|---|---|---|
| 身份稳定性 | 稳定 | 稳定 | **动态、短暂** |
| 授权 | 入职-调动-离职 | 创建时配置 | **每任务、运行时** |
| 行为 | 可预测 | 可预测 | **目标解释、链式** |
| 生命周期 | 年 | 月 | **分钟到小时** |
| 规模 | 数千 | 数万 | **数百万 NHI** |

静态 AIAP T1–T4 信任级别不够。AIZP V0.6 通过 `IDENTITY_VERIFICATION` 事件添加**持续授权**。

---

## 2. 核心原则

AIZP 采用 CSA Agentic Trust Framework 原则：

1. **永不信任，始终验证** — 在每个高风险动作重新验证身份。
2. **即时（JIT）凭据** — 短期、任务范围、自动过期。
3. **持续授权** — 上下文感知重新评估，非时点授予。
4. **去中心化标识符（DID）** — 密码学可验证的 Agent 身份。
5. **最小权限** — 每任务最窄可能作用域。
6. **异常检测** — 运行时行为监控（这是 AIZP 漂移检测的接入点）。

---

## 3. 身份方法

AIZP 支持四种身份验证方法，在 `IDENTITY_VERIFICATION.payload.identity_method` 中声明：

### 3.1 `DID` — 去中心化标识符

```
did:aixp:abc123
did:web:agents.aixp.dev:agent_alpha
```

最严格。由公钥支持的身份密码学证明。通过标准 DID 方法可解析（W3C DID v1.0 推荐标准；v1.1 已于 2026-03 进入候选推荐 Candidate Recommendation）。`did:aixp:` 是 AIZP 自定义/拟注册的 DID method，并非已注册的标准 method；`did:web:` 是已注册的标准 method。

**验证**：
```
1. 将 DID 解析为 DID 文档。
2. 用公钥验证 Agent 断言上的签名。
3. 检查吊销状态（若有吊销注册表）。
```

**建议**：G4+ 部署必需。

### 3.2 `AIAP_CARD_HASH` — AIAP Card 完整性

```
agent_card.json + AIAP 治理合约的 SHA-256 哈希
```

验证 Agent 声明的能力描述（AIAP Card）未被篡改。Agent 注册时固定；每个会话开始时重新验证。

**建议**：G2+ 部署必需。

### 3.3 `JWT` — Bearer token

由 OIDC 提供方发放的标准 JWT。适用于云托管 Agent。

**验证**：
```
1. 验证签名。
2. 检查过期。
3. 检查 `aud` claim 匹配部署。
4. 检查 `scope` claim 覆盖声明的 Agent 作用域。
```

### 3.4 `NHI_REGISTRY` — 企业 NHI 注册表查找

在组织的 NHI 注册表中查找（如 HashiCorp Vault、AWS IAM Roles Anywhere、CyberArk）。

```
1. 按 agent_id 查询注册表。
2. 验证 Agent 处于"活跃"状态。
3. 检索当前作用域（可能已被吊销）。
4. 与 AIZP 的 `granted_scope(c)` 匹配。
```

---

## 4. JIT 凭据

对 G3+ 部署，运行时按任务或按工具调用发放 JIT 凭据：

```json
{
  "credentials": {
    "type": "JIT",
    "scope": ["read.own", "send.email.own"],
    "ttl_seconds": 60,
    "issued_at": "2026-05-19T10:00:00Z",
    "issued_by": "did:aixp:vault_service",
    "purpose": "summarize_and_send_one_email"
  }
}
```

| 属性 | 约束 |
|---|---|
| `ttl_seconds` | G3 ≤ 3600（1 小时）；G4+ ≤ 60 |
| `scope` | Agent AIAP T 级别授予作用域的严格子集 |
| `purpose` | 人类可读摘要；**应** ≤ 200 字符（依 `identity-verification.schema.json` 的 `maxLength`）|
| `issued_by` | 凭据发放者的 DID |

JIT 凭据**不持久存储**——按需重新生成。

---

## 5. 持续授权循环

AIZP 的持续授权是循环：

```
1. Agent 请求动作 a。
2. AIZP 运行 GRAVITY_CHECK。
3. 若 gravity_score 要求或作用域变更：
   a. AIZP 发射 IDENTITY_VERIFICATION 事件。
   b. AIZP 重新检查 DID / AIAP card 哈希 / NHI 注册表。
   c. AIZP 为动作请求新的 JIT 凭据。
4. AIZP 仅向动作授予临时凭据。
5. 动作完成后，JIT 凭据被吊销。
6. 重复。
```

每步记录用于审计（EU AI Act Art 12 + ISO 27001 / 42001）。

---

## 6. 身份漂移检测

ZT 感知漂移检测添加：

| 漂移信号 | 检测 |
|---|---|
| `credential_misuse` | JIT 凭据在声明目的外使用 |
| `scope_lateral_movement` | Agent 尝试使用其他会话的凭据 |
| `identity_assertion_breach` | Agent 声称身份 ≠ 已验证身份 |
| `revocation_ignored` | Agent 尝试使用已吊销凭据 |

这些馈入 AIZP 的 `AUTHORITY_DRIFT`（现有）和 `IDENTITY_DRIFT`（V0.1）。

---

## 7. 与 AIAP 集成

AIAP T1–T4 信任级别成为作用域的**上界**，而非授予作用域：

```
granted_scope(c, task) = AIAP_T_level_scope(agent) ∩ JIT_credentials_scope(task)
```

| AIAP | 任务时最大作用域 | JIT TTL 建议 |
|---|---|---|
| T1 | 只读公共 | 24 小时 |
| T2 | 读+写自有 | 1 小时 |
| T3 | 跨资源 | 5 分钟 |
| T4 | 管理员 | 1 分钟 |

更高信任级别获得**更短**JIT TTL，因为每个凭据携带更高影响。

---

## 8. Agent Name Service (ANS)

对多 Agent 环境，AIZP V0.6 引用 **Agent Name Service (ANS)**——由 arxiv 2505.10609 引入、并被 AAGATE（arxiv 2510.25863）采用：

```
ANS 解析：agent_id → {
  public_key,
  DID,
  AIAP_trust_level,
  active_aizp_compliance_level,
  current_gravity_state,
  current_containment_level
}
```

当 AIBP 消息在 Agent 间流动时，AIZP 在允许消息通过前查询 ANS 验证对手方（类似服务到服务的 DNSSEC）。

ANS 对单 Agent 部署**可选**；对多 Agent **推荐**。

---

## 8.5 可验证委托链

ANS 验证*Agent 是谁*。但它本身不验证*Agent 委托给另一 Agent 时携带何种权限*。2026 年 Agent 生态尖锐地暴露了这一缺口：MCP 与 A2A 让 Agent 调用工具、委托任务，却都不验证委托方的权限或约束被委托方的范围（约 2000 个 MCP 服务器扫描全部缺认证）。

AIZP 对齐 **Invocation-Bound Capability Tokens（IBCT）**——Agent Identity Protocol（AIP，arxiv 2603.24775）提出的原语，将身份、*衰减*授权、溯源融合进单一 append-only token 链。

### 8.5.1 衰减不变量

AIZP 要求被委托权限沿链**单调不增**：

```
granted_scope(Bₙ) ⊆ delegatable_scope(Bₙ₋₁) ⊆ ... ⊆ granted_scope(B₀)
```

每一跳可*收窄*但绝不*扩宽*范围。任何需要超出衰减交集范围的动作引发 `AUTHORITY_DRIFT`（见 [Drift-Model_cn.md](Drift-Model_cn.md) §2.2），且委托溯源被记录以供审计。

### 8.5.2 映射到 AIZP

| IBCT 概念 | AIZP 机制 |
|---|---|
| token 中的身份 | `IDENTITY_VERIFICATION` 事件 |
| 衰减授权 | 权限范围 `A(a,c)` 对照*衰减后*范围计算，而非根授予 |
| 溯源绑定（append-only 链）| 委托链被记录；馈入 `INTER_AGENT_DRIFT` 与 A2A 桥（[Integration-A2A_cn.md](Integration-A2A_cn.md) §4）|
| 单跳（紧凑 JWT）/ 多跳（链式）| 单个 `IDENTITY_VERIFICATION` vs. 逐跳事件链 |

### 8.5.3 AIZP 增添什么

AIP/IBCT 提供 **token 机制**；AIZP 提供**行为后果**：在其衰减范围内行事的被委托方稳定运行，而漂向（或越过）其委托包络边缘的则触发分级容器。身份证明与行为引力互补——彼此不可替代。

---

## 9. 事件示例

### 9.1 初始身份验证

```json
{
  "event": "IDENTITY_VERIFICATION",
  "payload": {
    "agent_id_claimed": "agent_alpha",
    "identity_method": "DID",
    "identity_proof": "did:aixp:abc123",
    "verified": true,
    "credentials": {
      "type": "JIT",
      "scope": ["read.own", "send.email.own"],
      "ttl_seconds": 60,
      "issued_at": "2026-05-19T10:00:00Z"
    },
    "aiap_trust_level": "T2",
    "aiap_governance_hash_verified": true
  }
}
```

### 9.2 身份验证失败

```json
{
  "event": "IDENTITY_VERIFICATION",
  "payload": {
    "agent_id_claimed": "agent_alpha",
    "identity_method": "DID",
    "identity_proof": "did:aixp:fakeid",
    "verified": false,
    "failure_reason": "DID_RESOLUTION_FAILED",
    "credentials": null,
    "recommended_action": "DENY_AND_SAFE_STOP"
  }
}
```

失败触发立即 `SAFE_STOP`，reason `IDENTITY_BREACH`。

---

## 10. 合规

实现在合规级别声明 AIZP + ZT 合规：

| 级别 | ZT 要求 |
|---|---|
| G2 | 会话开始的 `AIAP_CARD_HASH` 验证 |
| G3 | + 发射 `IDENTITY_VERIFICATION` 事件；JIT 凭据 TTL ≤ 1h |
| G4 | + 基于 DID 的验证；JIT TTL ≤ 1 分钟；完整事件审计轨迹 |
| G5 | + 凭据生命周期不变量的形式化验证 |

---

## 11. 局限性

1. **DID 基础设施在 2026 仍在成熟**。企业采用不均。
2. **JIT 凭据发放延迟**可能伤害高频 Agent 循环。安全处缓存。
3. **仅身份验证不防有合法凭据的能力内部人员**。AIZP 漂移检测是补充。

---

## 参考

- CSA Agentic Trust Framework（2026）— AI Agent 的零信任。
- HashiCorp（2026）— Agentic 系统零信任：大规模管理 NHI。
- WEF（2025）— 非人类身份：Agentic AI 的网络安全新前沿。
- Cisco（2026）— Agentic AI 零信任白皮书。
- Agent Name Service (ANS) — 由 arxiv 2505.10609 引入。
- AAGATE（Huang 等，2025）— 采用 ANS。arxiv 2510.25863。
- AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A（Prakash，2026）— Invocation-Bound Capability Tokens。arxiv 2603.24775。
- 去中心化标识符（DIDs）v1.0 — W3C 推荐（v1.1 已于 2026-03 进入候选推荐 Candidate Recommendation）。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
