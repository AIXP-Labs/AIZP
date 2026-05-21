# 集成：模型上下文协议（MCP）

**版本**：AIZP V0.6（新章节 — 将 AIZP 接入 Agent 工具调用生态）

2026 年，Agent 生态的工具集成层已围绕 **模型上下文协议（MCP）**（MCP specification 2025-11-25）收敛——即单个 Agent 如何连接外部工具与数据。MCP 定义 Agent *如何*调用工具；它**不**定义该调用是否 HSAW 对齐。这个缺口正是 AIZP 的用武之地。

> MCP 说："这是调用工具的方式。"
> AIZP 说："此次调用的引力分数为 G——放行、锁定、或停止。"

---

## 1. 为何此集成重要

MCP 有已记录的安全缺口（见 [MCP Safety Audit](https://arxiv.org/abs/2504.03767)，arxiv 2504.03767）：

- **工具投毒**：嵌入工具*描述*中的恶意指令可诱导 Agent 进行非预期调用。
- **无内置授权**：2026 年一次扫描发现约 2000 个公开 MCP 服务器无认证。
- **过度热心的工具选择**：即便用户无此意图，LLM 也可能判定某破坏性工具"合适"。

MCP 官方指南建议对敏感操作做人在回路确认，但不定义*何时*操作算敏感。**AIZP 提供该决策函数**；AISOP 提供确认原语（见 [Integration-AISOP_cn.md](Integration-AISOP_cn.md)）。

---

## 2. 分层

```
MCP    — 传输工具调用（请求/响应、工具列表、描述）。
          ▼
AIZP   — 给工具调用打分（引力分数），决定放行 / 锁定 / 停止。
          ▼
AISOP  — 当 AIZP 锁定时执行人类确认（sys.io.confirm）。
```

每次 MCP `tools/call`，以 AIZP 术语，是一个在派发前需经 `GRAVITY_CHECK` 评估的**动作 `a`**。

---

## 3. 桥接：MCP `tools/call` → `GRAVITY_CHECK`

当 Agent 发出 MCP `tools/call` 时，运行时必须在**将调用转发给 MCP 服务器之前**：

1. 从 MCP 请求构造 AIZP 动作描述符。
2. 发出 `GRAVITY_CHECK` 并计算 `G`。
3. 若 `G ≥ 0.80`（STABLE_ORBIT）：转发调用。
4. 若 `0.50 ≤ G < 0.80`（DRIFT_WARNING）：转发但记录升高的 `risk_level`。
5. 若 `0.30 ≤ G < 0.50`（GRAVITY_LOCK_PENDING）：发出 `GRAVITY_LOCK` → AISOP `sys.io.confirm`。
6. 若 `0.15 ≤ G < 0.30`（QUARANTINED）：分级隔离；不转发。
7. 若 `G < 0.15`（SAFE_STOP）：强制轨迹终止；不转发。

### 3.1 字段映射

| MCP `tools/call` 字段 | AIZP 动作描述符 |
|---|---|
| `params.name`（工具名）| `action_descriptor`（动词）|
| `params.arguments` | 动作参数（按权限范围 + 可逆性打分）|
| 服务器身份（来源）| 折入 `IDENTITY_VERIFICATION` |
| 工具 `description`（来自 `tools/list`）| 扫描工具投毒 → 经 IPI 向量可能引发记忆/社交漂移（[Drift-Model_cn.md](Drift-Model_cn.md) §8）|

### 3.2 从 MCP 注解推导可逆性

MCP 工具定义可携带注解（如 `readOnlyHint`、`destructiveHint`）。存在时，AIZP 应据其初始化可逆性组件 `R(a)`：

> 根据 MCP 规范，工具注解只是提示（hints），**禁止**信任来自未经验证服务器的注解；仅当服务器已 TOFU 锁定（pinned）时才用其初始化 R(a)（见 §4）。

| MCP 注解 | `R(a)` 初值 |
|---|---|
| `readOnlyHint: true` | `1.0` |
| `destructiveHint: true` | `0.0` |
| （无）| 按 [Drift-Model_cn.md](Drift-Model_cn.md) 默认；未知 → `0.0` |

---

## 4. 工具投毒作为漂移向量

在不可信服务器场景下，MCP 工具描述是攻击者可控的。被投毒的描述是**间接提示注入**的投递通道。AIZP 在间接提示注入（IPI）跨切向量下处理（见 [Drift-Model_cn.md](Drift-Model_cn.md) §8）：

- 在 `tools/list` 时，对每个工具描述做哈希并钉住（首次信任 TOFU）。
- 已钉住工具的描述变更引发 `IDENTITY_VERIFICATION` 复检 + IPI 向量评估（[Drift-Model_cn.md](Drift-Model_cn.md) §8）。
- 嵌入工具*结果*（不仅是描述）中的指令对照声明的用户意图打分：大幅偏离引发 IPI 信号 → 意图/记忆漂移。

这使 AIZP 与已记录的 MCP 防御（描述钉住，如 mcp-context-protector）对齐，而非重复造轮。

---

## 5. 可观测性

每次 MCP 调用已携带从客户端 → 网关 → 服务器的关联 ID。AIZP `GRAVITY_CHECK` 事件应复用该关联 ID 作为 `action_id`，使 OpenTelemetry trace（见 [Integration-OTel_cn.md](Integration-OTel_cn.md)）将引力决策链接到具体的 MCP span。

---

## 6. AIZP 不接管什么

- AIZP 不传输工具调用（MCP 的职责）。
- AIZP 不认证 MCP 服务器（零信任 / AIP 委托——见 [Integration-ZT_cn.md](Integration-ZT_cn.md)）。
- AIZP 不渲染确认 UI（AISOP 的职责）。

AIZP 是 MCP 传输与工具派发之间的**打分与决策层**——仅此而已。

---

## 参考

- Model Context Protocol — Security Best Practices。https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices
- MCP Safety Audit: LLMs with the Model Context Protocol Allow Major Security Exploits。arxiv 2504.03767。
- AIZP 配套：[Integration-A2A_cn.md](Integration-A2A_cn.md)、[Integration-AISOP_cn.md](Integration-AISOP_cn.md)、[Integration-ZT_cn.md](Integration-ZT_cn.md)、[Drift-Model_cn.md](Drift-Model_cn.md)。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
