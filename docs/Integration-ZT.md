# Integration: Zero Trust + Non-Human Identity

**Version**: AIZP V0.6 (new chapter)

This document specifies how AIZP integrates with Zero Trust (ZT) architectures and Non-Human Identity (NHI) management — the dominant 2026 paradigm for autonomous agent security.

By mid-2026, NHIs outnumber human identities in many enterprises by ratios from 40:1 to over 100:1, and NHI exploitation has become the **#1 cybersecurity threat** (per WEF, CSA, and HashiCorp 2026 reports). AIZP cannot remain identity-agnostic.

---

## 1. The Identity Problem

Traditional IAM was designed for humans and static service accounts. AI agents differ:

| Property | Human user | Static service account | AI agent |
|---|---|---|---|
| Identity stability | Stable | Stable | **Dynamic, ephemeral** |
| Authorization | Joiner-mover-leaver | Configured at creation | **Per-task, runtime** |
| Behavior | Predictable | Predictable | **Goal-interpreting, chaining** |
| Lifecycle | Years | Months | **Minutes to hours** |
| Scale | Thousands | Tens of thousands | **Millions of NHIs** |

Static AIAP T1–T4 trust levels are insufficient. AIZP V0.6 adds **continuous authorization** via the `IDENTITY_VERIFICATION` event.

---

## 2. Core Principles

AIZP adopts CSA's Agentic Trust Framework principles:

1. **Never trust, always verify** — re-verify identity at each high-risk action.
2. **Just-In-Time (JIT) credentials** — short-lived, task-scoped, automatically expiring.
3. **Continuous authorization** — context-aware re-evaluation, not point-in-time grants.
4. **Decentralized Identifiers (DIDs)** — cryptographically verifiable agent identity.
5. **Least privilege** — narrowest possible scope per task.
6. **Anomaly detection** — runtime behavior monitoring (this is where AIZP's drift detection plugs in).

---

## 3. Identity Methods

AIZP supports four identity verification methods, declared in `IDENTITY_VERIFICATION.payload.identity_method`:

### 3.1 `DID` — Decentralized Identifier

```
did:aixp:abc123
did:web:agents.aixp.dev:agent_alpha
```

Most rigorous. Cryptographic proof of identity backed by a public key. Resolvable via standard DID methods (W3C DID v1.0 Recommendation; v1.1 in Candidate Recommendation, 2026-03). `did:aixp:` is a custom AIZP DID method (proposed/to-be-registered), not an already-registered standard method; `did:web:` is a registered standard method.

**Verification**:
```
1. Resolve DID to DID document.
2. Verify signature on agent assertion using public key.
3. Check revocation status (if revocation registry available).
```

**Recommendation**: Required for G4+ deployments.

### 3.2 `AIAP_CARD_HASH` — AIAP Card Integrity

```
SHA-256 hash of agent_card.json + AIAP governance contract
```

Verifies that the agent's declared capability description (AIAP Card) has not been tampered. Pin during agent registration; re-verify on each session start.

**Recommendation**: Required for G2+ deployments.

### 3.3 `JWT` — Bearer token

Standard JWT issued by an OIDC provider. Useful for cloud-hosted agents.

**Verification**:
```
1. Validate signature.
2. Check expiration.
3. Check `aud` claim matches deployment.
4. Check `scope` claim covers declared agent scope.
```

### 3.4 `NHI_REGISTRY` — Enterprise NHI registry lookup

Lookup in the organization's NHI registry (e.g., HashiCorp Vault, AWS IAM Roles Anywhere, CyberArk).

```
1. Query registry by agent_id.
2. Verify agent is in "active" state.
3. Retrieve current scope (may have been revoked).
4. Match against AIZP's `granted_scope(c)`.
```

---

## 4. JIT Credentials

For G3+ deployments, the runtime issues JIT credentials per-task or per-tool-call:

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

| Property | Constraint |
|---|---|
| `ttl_seconds` | ≤ 3600 (1 hour) for G3; ≤ 60 for G4+ |
| `scope` | Strict subset of agent's AIAP T-level granted scope |
| `purpose` | Human-readable summary; SHOULD be ≤ 200 chars (per `identity-verification.schema.json` `maxLength`) |
| `issued_by` | DID of credential issuer |

JIT credentials are **not stored persistently** — they're regenerated as needed.

---

## 5. Continuous Authorization Loop

AIZP's continuous authorization is the loop:

```
1. Agent requests action a.
2. AIZP runs GRAVITY_CHECK.
3. If gravity_score requires it OR scope changes:
   a. AIZP emits IDENTITY_VERIFICATION event.
   b. AIZP re-checks DID / AIAP card hash / NHI registry.
   c. AIZP requests fresh JIT credentials for the action.
4. AIZP grants ephemeral credentials to the action only.
5. After action completes, JIT credentials are revoked.
6. Repeat.
```

Each step is logged for audit (EU AI Act Art 12 + ISO 27001 / 42001).

---

## 6. Identity Drift Detection

ZT-aware drift detection adds:

| Drift signal | Detection |
|---|---|
| `credential_misuse` | JIT credentials used outside declared purpose |
| `scope_lateral_movement` | Agent attempts to use credentials from another session |
| `identity_assertion_breach` | Agent's claimed identity ≠ verified identity |
| `revocation_ignored` | Agent attempts to use revoked credentials |

These feed into AIZP's `AUTHORITY_DRIFT` (existing) and `IDENTITY_DRIFT` (V0.1).

---

## 7. Integration with AIAP

AIAP T1–T4 trust levels become the **upper bound** of scope, not the granted scope:

```
granted_scope(c, task) = AIAP_T_level_scope(agent) ∩ JIT_credentials_scope(task)
```

| AIAP | Max scope at task time | JIT TTL recommendation |
|---|---|---|
| T1 | Read-only public | 24 hours |
| T2 | Read+write own | 1 hour |
| T3 | Cross-resource | 5 minutes |
| T4 | Admin | 1 minute |

Higher trust levels get **shorter** JIT TTLs because each credential carries higher impact.

---

## 8. Agent Name Service (ANS)

For multi-agent environments, AIZP V0.6 references the **Agent Name Service (ANS)**, introduced in arxiv 2505.10609 and adopted by AAGATE (arxiv 2510.25863):

```
ANS resolves: agent_id → {
  public_key,
  DID,
  AIAP_trust_level,
  active_aizp_compliance_level,
  current_gravity_state,
  current_containment_level
}
```

When AIBP messages flow between agents, AIZP queries ANS to verify the counterparty before allowing the message through (similar to DNSSEC for service-to-service).

ANS is **optional** for single-agent deployments; **recommended** for multi-agent.

---

## 8.5 Verifiable Delegation Chains

ANS verifies *who an agent is*. It does not, by itself, verify *what authority an agent carries when it delegates to another agent*. In 2026 the agent ecosystem surfaced this gap sharply: MCP and A2A let agents call tools and delegate tasks, but neither verifies the delegating agent's authority or constrains the delegate's scope (a scan of ~2,000 MCP servers found all lacked authentication).

AIZP aligns with **Invocation-Bound Capability Tokens (IBCTs)**, the primitive proposed by the Agent Identity Protocol (AIP, arxiv 2603.24775), which fuses identity, *attenuated* authorization, and provenance into a single append-only token chain.

### 8.5.1 The attenuation invariant

AIZP requires that delegated authority be **monotonically non-increasing** along the chain:

```
granted_scope(Bₙ) ⊆ delegatable_scope(Bₙ₋₁) ⊆ ... ⊆ granted_scope(B₀)
```

Each hop may *narrow* but never *widen* scope. Any action requiring scope beyond the attenuated intersection raises `AUTHORITY_DRIFT` (see [Drift-Model.md](Drift-Model.md) §2.2), and the delegation provenance is recorded for audit.

### 8.5.2 Mapping to AIZP

| IBCT concept | AIZP mechanism |
|---|---|
| Identity in token | `IDENTITY_VERIFICATION` event |
| Attenuated authorization | Authority Scope `A(a,c)` computed against the *attenuated* scope, not the root grant |
| Provenance binding (append-only chain) | delegation chain logged; feeds `INTER_AGENT_DRIFT` and the A2A bridge ([Integration-A2A.md](Integration-A2A.md) §4) |
| Single-hop (compact JWT) / multi-hop (chained) | single `IDENTITY_VERIFICATION` vs. per-hop chain of events |

### 8.5.3 What AIZP adds

AIP/IBCT provides the **token mechanics**; AIZP provides the **behavioral consequence**: a delegate that behaves within its attenuated scope orbits stably, while one that drifts toward the edge of (or beyond) its delegated envelope triggers graduated containment. Identity attestation and behavioral gravity are complementary — neither replaces the other.

---

## 9. Event Examples

### 9.1 Initial identity verification

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

### 9.2 Identity verification failure

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

Failure triggers immediate `SAFE_STOP` with reason `IDENTITY_BREACH`.

---

## 10. Conformance

Implementations claim AIZP + ZT conformance at compliance levels:

| Level | ZT requirements |
|---|---|
| G2 | `AIAP_CARD_HASH` verification on session start |
| G3 | + `IDENTITY_VERIFICATION` event emitted; JIT credentials with TTL ≤ 1h |
| G4 | + DID-based verification; JIT TTL ≤ 1 min; full event audit trail |
| G5 | + formal verification of credential lifecycle invariants |

---

## 11. Limitations

1. **DID infrastructure is still maturing** in 2026. Enterprise adoption uneven.
2. **JIT credential issuance latency** can hurt high-frequency agent loops. Cache where safe.
3. **Identity verification alone doesn't prevent capable insiders** with valid credentials. AIZP's drift detection is the complement.

---

## References

- CSA Agentic Trust Framework (2026) — Zero Trust for AI agents.
- HashiCorp (2026) — Zero trust for agentic systems: managing NHIs at scale.
- WEF (2025) — Non-human identities: agentic AI's new frontier of cybersecurity risk.
- Cisco (2026) — Zero Trust for Agentic AI white paper.
- Agent Name Service (ANS) — introduced in arxiv 2505.10609.
- AAGATE (Huang et al., 2025) — adopts ANS. arxiv 2510.25863.
- AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A (Prakash, 2026) — Invocation-Bound Capability Tokens. arxiv 2603.24775.
- Decentralized Identifiers (DIDs) v1.0 — W3C Recommendation (v1.1 in Candidate Recommendation, 2026-03).

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
