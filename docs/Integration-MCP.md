# Integration: Model Context Protocol (MCP)

**Version**: AIZP V0.6 (new chapter — connects AIZP to the agent tool-call ecosystem)

In 2026 the agent ecosystem's tool-integration layer has consolidated around the **Model Context Protocol (MCP)** (MCP specification 2025-11-25) — the way a single agent connects to external tools and data. MCP defines *how* an agent calls a tool; it does **not** define whether that call is HSAW-aligned. That gap is exactly where AIZP applies.

> MCP says: "here is how to invoke a tool."
> AIZP says: "this specific invocation has Gravity Score G — proceed, lock, or stop."

---

## 1. Why this integration matters

MCP has known, documented security gaps (see [MCP Safety Audit](https://arxiv.org/abs/2504.03767), arxiv 2504.03767):

- **Tool poisoning**: malicious instructions embedded in a tool *description* can steer the agent into unintended calls.
- **No built-in authorization**: a 2026 scan found ~2,000 public MCP servers with no authentication.
- **Over-eager tool selection**: the LLM may decide a destructive tool is "appropriate" even when the user did not intend it.

The official MCP guidance recommends human-in-the-loop confirmation for sensitive operations but does not specify *when* an operation is sensitive. **AIZP supplies that decision function**; AISOP supplies the confirmation primitive (see [Integration-AISOP.md](Integration-AISOP.md)).

---

## 2. Layering

```
MCP    — TRANSPORTS the tool call (request/response, tool list, descriptions).
          ▼
AIZP   — SCORES the tool call (Gravity Score) and decides proceed / lock / stop.
          ▼
AISOP  — EXECUTES human confirmation when AIZP locks (sys.io.confirm).
```

Each MCP `tools/call` is, in AIZP terms, an **action `a`** to be evaluated by `GRAVITY_CHECK` before dispatch.

---

## 3. The Bridge: MCP `tools/call` → `GRAVITY_CHECK`

When an agent issues an MCP `tools/call`, the runtime MUST, **before forwarding the call to the MCP server**:

1. Construct an AIZP action descriptor from the MCP request.
2. Emit `GRAVITY_CHECK` and compute `G`.
3. If `G ≥ 0.80` (STABLE_ORBIT): forward the call.
4. If `0.50 ≤ G < 0.80` (DRIFT_WARNING): forward but log elevated `risk_level`.
5. If `0.30 ≤ G < 0.50` (GRAVITY_LOCK_PENDING): emit `GRAVITY_LOCK` → AISOP `sys.io.confirm`.
6. If `0.15 ≤ G < 0.30` (QUARANTINED): graduated containment; do not forward.
7. If `G < 0.15` (SAFE_STOP): force trajectory termination; do not forward.

### 3.1 Field mapping

| MCP `tools/call` field | AIZP action descriptor |
|---|---|
| `params.name` (tool name) | `action_descriptor` (verb) |
| `params.arguments` | action parameters (scored for authority scope + reversibility) |
| server identity (origin) | folded into `IDENTITY_VERIFICATION` |
| tool `description` (from `tools/list`) | scanned for tool-poisoning → may raise Memory/Social Drift via the IPI vector ([Drift-Model.md](Drift-Model.md) §8) |

### 3.2 Reversibility from MCP annotations

MCP tool definitions MAY carry annotations (e.g., `readOnlyHint`, `destructiveHint`). When present, AIZP SHOULD seed the Reversibility component `R(a)` from them:

> Per the MCP spec, tool annotations are hints and MUST NOT be trusted from unverified servers; only use them to seed R(a) when the server is TOFU-pinned (see §4).

| MCP annotation | `R(a)` seed |
|---|---|
| `readOnlyHint: true` | `1.0` |
| `destructiveHint: true` | `0.0` |
| (none) | default per [Drift-Model.md](Drift-Model.md); unknown → `0.0` |

---

## 4. Tool poisoning as a drift vector

MCP tool descriptions are attacker-controllable in untrusted-server scenarios. A poisoned description is an **indirect prompt injection** delivery channel. AIZP treats this under the IPI cross-cutting vector (see [Drift-Model.md](Drift-Model.md) §8):

- On `tools/list`, hash and pin each tool description (trust-on-first-use).
- A changed description for an already-pinned tool raises `IDENTITY_VERIFICATION` re-check + IPI-vector evaluation ([Drift-Model.md](Drift-Model.md) §8).
- Instructions embedded in a tool *result* (not just description) are scored against declared user intent: a large divergence raises the IPI signal → Intent/Memory Drift.

This aligns AIZP with documented MCP defenses (description pinning, e.g. mcp-context-protector) rather than reinventing them.

---

## 5. Observability

Each MCP call already carries a correlation ID from client → gateway → server. AIZP `GRAVITY_CHECK` events SHOULD reuse that correlation ID as `action_id`, so the OpenTelemetry trace (see [Integration-OTel.md](Integration-OTel.md)) links the gravity decision to the concrete MCP span.

---

## 6. What AIZP does NOT take over

- AIZP does not transport tool calls (MCP's job).
- AIZP does not authenticate MCP servers (Zero Trust / AIP delegation — see [Integration-ZT.md](Integration-ZT.md)).
- AIZP does not render the confirmation UI (AISOP's job).

AIZP is the **scoring and decision layer** between MCP transport and tool dispatch — nothing more, nothing less.

---

## References

- Model Context Protocol — Security Best Practices. https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices
- MCP Safety Audit: LLMs with the Model Context Protocol Allow Major Security Exploits. arxiv 2504.03767.
- AIZP companion: [Integration-A2A.md](Integration-A2A.md), [Integration-AISOP.md](Integration-AISOP.md), [Integration-ZT.md](Integration-ZT.md), [Drift-Model.md](Drift-Model.md).

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
