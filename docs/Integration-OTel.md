# Integration: OpenTelemetry

**Version**: AIZP V0.6 (new chapter)

This document specifies how AIZP events map to **OpenTelemetry GenAI Semantic Conventions** (SemConv 1.40.0, as of April 2026), enabling AIZP instrumentation to flow through standard observability pipelines (OTel Collector, Datadog, Grafana, etc.) without bespoke adapters.

---

## 1. Why OTel?

OpenTelemetry GenAI semantic conventions are still in Development status (as of 2026-04, not yet stable); the mappings below are forward-looking alignment. Aligning AIZP with OTel:

- Makes AIZP events queryable in existing dashboards.
- Avoids reinventing trace propagation, correlation, sampling.
- Enables auto-instrumentation for AIZP-aware runtimes.
- Satisfies EU AI Act Art 12 logging via OTel's audit pipelines.

---

## 2. Span Mapping

OTel GenAI defines several agent operations, identified by the `gen_ai.operation.name` attribute (`create_agent`, `invoke_agent`, `invoke_workflow`, `execute_tool`); the span name takes the form `"invoke_agent {gen_ai.agent.name}"`. AIZP layers its own attributes on top:

| OTel operation (`gen_ai.operation.name`) | AIZP attributes (added) |
|---|---|
| `invoke_agent` | `aizp.gravity_score`, `aizp.gravity_state`, `aizp.containment_level` |
| `execute_tool` | `aizp.drift_types`, `aizp.lock_status` |
| `create_agent` | `aizp.compliance_level`, `aizp.aiap_trust_level` |

### 2.1 Span attributes

AIZP custom attributes use the independent reverse-domain `aizp.*` namespace (OTel naming rules forbid using an existing OTel semantic-convention namespace such as `gen_ai.*` as a prefix for custom attributes):

| Attribute key | AIZP value source | Cardinality |
|---|---|---|
| `aizp.gravity_score` | `GRAVITY_CHECK.payload.gravity_score` | Continuous [0,1] |
| `aizp.gravity_state` | state machine state name | 6-cardinality enum |
| `aizp.containment_level` | L0–L4 | 5-cardinality enum |
| `aizp.drift_types` | `GRAVITY_DRIFT.payload.drift_types` (array) | Up to 11 values |
| `aizp.drift_severity` | `GRAVITY_DRIFT.payload.severity` | 4-cardinality enum |
| `aizp.lock_status` | `GRAVITY_LOCK.payload.status` | 4-cardinality enum |
| `aizp.aiap_trust_level` | `IDENTITY_VERIFICATION.payload.aiap_trust_level` | 4-cardinality enum |
| `aizp.compliance_level` | implementation declaration | 6-cardinality enum |
| `aizp.protocol_version` | `"V0.6"` | constant |

---

## 3. Event Mapping (Span Events, NOT Attributes)

OTel GenAI strongly recommends storing payloads in **span events**, not attributes (attributes are indexed and limited in size; events allow filtering at the Collector level).

AIZP events become OTel span events with the prefix `aizp.*`:

| AIZP event | OTel span event name |
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

Each span event body MUST be the AIZP payload JSON, serialized as event attribute body.

---

## 4. Metrics

AIZP defines OTel metrics for monitoring:

### 4.1 Counters

```
aizp.gravity_check.count{state, containment_level}
aizp.gravity_drift.count{drift_type, severity}
aizp.gravity_lock.count{status}
aizp.safe_stop.count{reason}
aizp.containment_graduated.count{previous, new}
```

### 4.2 Histograms

```
aizp.gravity_score{state}                 (distribution of scores)
aizp.gravity_check.duration_ms            (per-check latency)
aizp.gravity_lock.confirmation_duration_s (user response time)
aizp.quarantine.duration_s                (time spent in QUARANTINED)
```

### 4.3 Required metrics (G4+)

Implementations claiming G4+ MUST export:

- `aizp.gravity_score` histogram (auditable distribution).
- `aizp.safe_stop.count` (incident telemetry).
- `aizp.drift.count` per drift type (drift profile).

---

## 5. Privacy Considerations

OTel explicitly warns:

> "Storing full prompt text in span attributes is an anti-pattern: attributes are always indexed, have size limits, and expose PII in your backend."

AIZP implementations MUST:

1. **NOT** put full action descriptors or user prompts in span attributes.
2. **DO** put them in span events (body), which can be filtered at the Collector.
3. **DO** redact / hash long-tail content (e.g., action descriptors > 256 chars).
4. **DO** support OTel Collector `attributes` processor to drop sensitive fields per deployment policy.

### 5.1 Sensitive field policy

| Field | OTel placement | Reason |
|---|---|---|
| `action_descriptor` | span event body | may contain user goal |
| `confirmation_prompt` | span event body | may contain transaction details |
| `evidence_text` (MEMORY_QUARANTINE) | span event body | the suspicious content itself |
| `agent_id`, `session_id` | span attribute | typically opaque |
| `gravity_score`, drift types | span attribute | safe to index |

---

## 6. Trace Context Propagation

AIZP events MUST propagate OTel trace context:

```
W3C TraceContext:
  - traceparent: <version>-<trace-id>-<parent-id>-<flags>
  - tracestate: aizp=session=<session_id>;agent=<agent_id>

AIZP-specific:
  - aizp.event_id is the OTel span_id of the event-emitting span
  - aizp.trigger_event_id links to parent span_id when applicable
```

This enables:
- Distributed tracing across multi-agent systems.
- Correlation of agent-to-agent (AIBP) messages with their AIZP-driven approval flows.
- Linking `sys.io.confirm` (AISOP) span to its triggering `GRAVITY_LOCK` AIZP event.

---

## 7. Sampling

AIZP events SHOULD respect OTel sampling rules but with **mandatory always-on** for these events (regardless of sampling):

- `GRAVITY_DRIFT` with severity `HIGH` or `CRITICAL`
- `GRAVITY_LOCK` (any status)
- `SAFE_STOP` (always)
- `CONTAINMENT_GRADUATED` (always)
- `IDENTITY_VERIFICATION` with `verified=false`
- `SCHEME_SUSPECTED` with `aggregate_confidence > 0.5`

Routine `GRAVITY_CHECK` events MAY be sampled at deployment-defined rates (e.g., 1/100 in high-volume environments).

---

## 8. Example OTel Span (concrete)

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
        body: "<JSON of AIZP GRAVITY_CHECK payload>"
    - name: "aizp.gravity_drift"
      timestamp: 2026-05-19T10:00:00.150Z
      attributes:
        body: "<JSON of AIZP GRAVITY_DRIFT payload>"
    - name: "aizp.gravity_lock"
      timestamp: 2026-05-19T10:00:00.200Z
      attributes:
        body: "<JSON of AIZP GRAVITY_LOCK payload>"
```

---

## 9. Vendor Compatibility (as of May 2026)

| Backend | OTel GenAI SemConv support | AIZP attribute query |
|---|---|---|
| Datadog (v1.37+) | Native | Filter by `aizp.gravity_state` |
| Grafana Loki | Logs ingest | Search logs with AIZP attributes |
| Uptrace | Native | Full-text + structured |
| Jaeger | Span attributes | Manual config |
| Honeycomb | Native | Auto-derive fields |

> Note: vendor support not independently verified.

Reference implementations SHOULD ship an OTel Exporter that produces the spans above. See [Implementer-Guide.md](Implementer-Guide.md) §10.

---

## 10. Compliance: EU AI Act Art 12

EU AI Act Art 12 requires automatic event logging with 6-month retention. OTel-based AIZP instrumentation natively satisfies:

- **Automatic logging**: AIZP events flow through OTel pipeline without app code.
- **Traceability**: W3C TraceContext links all events of a session.
- **Retention**: Collector → Object storage with retention policy.
- **Tamper-resistance**: hash-chain at Collector (G4+).

See [Compliance-Profiles/EU-AI-Act-Mapping.md](Compliance-Profiles/EU-AI-Act-Mapping.md).

---

## References

- OpenTelemetry GenAI Semantic Conventions 1.40.0 (April 2026 release).
- OpenTelemetry GenAI Agent SemConv Cheat Sheet 2026 (techbytes.app).
- OpenTelemetry blog — AI Agent Observability: Evolving Standards and Best Practices.
- Datadog v1.37 native GenAI support.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
