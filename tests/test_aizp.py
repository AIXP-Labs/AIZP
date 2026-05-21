"""AIZP V0.6 minimal conformance tests.

Two test groups:
  1. Schema validation — every example in examples/ validates against the
     schema in schemas/ whose `event` const matches the example's event.
  2. Gravity Score — reproduces the worked example in docs/Gravity-Model.md §5
     (expected G = 0.674 -> DRIFT_WARNING).

Run with pytest:      pytest tests/
Run standalone:       python tests/test_aizp.py

Requires: jsonschema  (pip install jsonschema)
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "schemas"
EXAMPLES_DIR = ROOT / "examples"
SPECIFICATION_DIR = ROOT / "specification"

CURRENT_VERSION = "V0.6"


def _load_json(path: Path) -> dict:
    # Examples/schemas are UTF-8; be explicit so Windows default (gbk) does not break.
    return json.loads(path.read_text(encoding="utf-8"))


def _build_event_schema_index() -> dict[str, dict]:
    """Map each schema's `event` const to the loaded schema object."""
    index: dict[str, dict] = {}
    for schema_path in sorted(SCHEMAS_DIR.glob("*.schema.json")):
        schema = _load_json(schema_path)
        event_const = (
            schema.get("properties", {}).get("event", {}).get("const")
        )
        if event_const:
            index[event_const] = schema
    return index


# ---------------------------------------------------------------------------
# Group 1 — schema validation
# ---------------------------------------------------------------------------

def iter_examples():
    for example_path in sorted(EXAMPLES_DIR.glob("*.json")):
        yield example_path


def validate_example(example_path: Path, index: dict[str, dict]) -> None:
    example = _load_json(example_path)
    event = example.get("event")
    assert event, f"{example_path.name}: missing 'event' field"
    assert event in index, (
        f"{example_path.name}: no schema with event const '{event}'"
    )
    jsonschema.validate(instance=example, schema=index[event])
    # Protocol-version consistency: examples must be V0.6.
    assert example.get("protocol_version") == "V0.6", (
        f"{example_path.name}: protocol_version != V0.6"
    )


def test_all_examples_validate():
    index = _build_event_schema_index()
    assert index, "no schemas found"
    for example_path in iter_examples():
        validate_example(example_path, index)


# ---------------------------------------------------------------------------
# Group 2 — Gravity Score worked example (docs/Gravity-Model.md §5)
# ---------------------------------------------------------------------------

DEFAULT_WEIGHTS = {"I": 0.30, "A": 0.25, "R": 0.20, "H": 0.15, "D": 0.10}


def gravity_score(I: float, A: float, R: float, H: float, D: float,
                  w: dict[str, float] = DEFAULT_WEIGHTS) -> float:
    return w["I"] * I + w["A"] * A + w["R"] * R + w["H"] * H + w["D"] * D


def orbital_state(g: float) -> str:
    if g >= 0.80:
        return "STABLE_ORBIT"
    if g >= 0.50:
        return "DRIFT_WARNING"
    if g >= 0.30:
        return "GRAVITY_LOCK_PENDING"
    if g >= 0.15:
        return "QUARANTINED"
    return "SAFE_STOP"


def test_recency_decay():
    # H(a,c) = exp(-Δt/τ), Δt=1800s, τ=3600s -> exp(-0.5) ≈ 0.6065
    h = math.exp(-1800 / 3600)
    assert abs(h - 0.6065) < 1e-3


def test_worked_example_transfer_funds():
    # docs/Gravity-Model.md §5: I=0.94, A=0.80, R=0.0, H≈0.61, D=1.0
    g = gravity_score(I=0.94, A=0.80, R=0.0, H=0.61, D=1.0)
    assert abs(g - 0.674) < 0.005, f"expected ~0.674, got {g:.4f}"
    assert orbital_state(g) == "DRIFT_WARNING"


def test_threshold_boundaries():
    assert orbital_state(0.80) == "STABLE_ORBIT"
    assert orbital_state(0.79) == "DRIFT_WARNING"
    assert orbital_state(0.50) == "DRIFT_WARNING"
    assert orbital_state(0.49) == "GRAVITY_LOCK_PENDING"
    assert orbital_state(0.30) == "GRAVITY_LOCK_PENDING"
    assert orbital_state(0.29) == "QUARANTINED"
    assert orbital_state(0.15) == "QUARANTINED"
    assert orbital_state(0.14) == "SAFE_STOP"


# ---------------------------------------------------------------------------
# Group 3 — deployment config schema (schemas/aizp-config.schema.json)
# ---------------------------------------------------------------------------

CONFIG_SCHEMA_PATH = SCHEMAS_DIR / "aizp-config.schema.json"
CONFIG_EXAMPLE_PATH = EXAMPLES_DIR / "config" / "deployment.example.json"


def test_config_example_validates():
    schema = _load_json(CONFIG_SCHEMA_PATH)
    config = _load_json(CONFIG_EXAMPLE_PATH)
    jsonschema.validate(instance=config, schema=schema)
    # Weights must sum to 1.0 (the schema cannot assert this).
    weights = config.get("weights", {})
    assert abs(sum(weights.values()) - 1.0) < 1e-9, (
        f"weights must sum to 1.0, got {sum(weights.values())}"
    )
    # Threshold bands must be strictly descending.
    t = config["thresholds"]
    assert t["stable_orbit"] > t["drift_warning"] > t["gravity_lock_pending"] > t["quarantined"], (
        "thresholds must be strictly descending"
    )


# The one place threshold band lower-bounds are asserted. Every other location
# (registry §3, WhitePaper §5.1, config schema defaults, orbital_state) must
# agree with these — guards against numeric drift the way the version-narrative
# hygiene test guards against version-string drift.
CANONICAL_THRESHOLDS = {
    "stable_orbit": 0.80,
    "drift_warning": 0.50,
    "gravity_lock_pending": 0.30,
    "quarantined": 0.15,
}


def test_threshold_single_source_of_truth():
    so = f"{CANONICAL_THRESHOLDS['stable_orbit']:.2f}"
    dw = f"{CANONICAL_THRESHOLDS['drift_warning']:.2f}"
    glp = f"{CANONICAL_THRESHOLDS['gravity_lock_pending']:.2f}"
    q = f"{CANONICAL_THRESHOLDS['quarantined']:.2f}"

    # 1. config schema defaults
    schema_props = _load_json(CONFIG_SCHEMA_PATH)["properties"]["thresholds"]["properties"]
    for name, value in CANONICAL_THRESHOLDS.items():
        assert schema_props[name]["default"] == value, (
            f"config schema default {name}={schema_props[name]['default']} != canonical {value}"
        )

    # 2. orbital_state() boundaries
    assert orbital_state(CANONICAL_THRESHOLDS["stable_orbit"]) == "STABLE_ORBIT"
    assert orbital_state(CANONICAL_THRESHOLDS["drift_warning"]) == "DRIFT_WARNING"
    assert orbital_state(CANONICAL_THRESHOLDS["gravity_lock_pending"]) == "GRAVITY_LOCK_PENDING"
    assert orbital_state(CANONICAL_THRESHOLDS["quarantined"]) == "QUARANTINED"
    assert orbital_state(CANONICAL_THRESHOLDS["quarantined"] - 0.01) == "SAFE_STOP"

    # 3. registry §3 table (format: "G ≥ 0.80", "0.50 ≤ G < 0.80", ... , "G < 0.15")
    registry = (SPECIFICATION_DIR / "registry.md").read_text(encoding="utf-8")
    for band in [f"G ≥ {so}", f"{dw} ≤ G < {so}", f"{glp} ≤ G < {dw}",
                 f"{q} ≤ G < {glp}", f"G < {q}"]:
        assert band in registry, f"registry.md §3 missing canonical band '{band}'"

    # 4. WhitePaper §5.1 block (format: "G ≥ 0.80", "0.50–0.80", ... , "G < 0.15")
    whitepaper = (ROOT / "docs" / "WhitePaper.md").read_text(encoding="utf-8")
    for band in [f"G ≥ {so}", f"{dw}–{so}", f"{glp}–{dw}", f"{q}–{glp}", f"G < {q}"]:
        assert band in whitepaper, f"WhitePaper.md §5.1 missing canonical band '{band}'"


# ---------------------------------------------------------------------------
# Group 4 — version-narrative hygiene (prevents P1/P4 staleness recurrence)
# ---------------------------------------------------------------------------

# Stale present-tense version idioms forbidden across all narrative + normative
# docs. These read as "this is a V0.x document" instead of describing the current
# cumulative state. Legitimate provenance is intentionally NOT matched:
#   - "Since V0.2", "自 V0.2 起"          (sourcing, not "what's new")
#   - bare "V0.2 新增" / "since V0.2" in table cells and code comments
#   - inline "(V0.2 — see ...)" sourcing on non-heading lines
#   - lineage / sub-theory / "(V0.6)" headings (version IS the subject / current)
_STALE_PATTERNS = [
    re.compile(r"\(NEW in V0\.\d\)"),
    re.compile(r"\*\*NEW in V0\.\d\*\*"),
    re.compile(r"（V0\.\d 新增）"),
    re.compile(r"\*\*V0\.\d 新增\*\*"),
    re.compile(r"\*\*V0\.\d (changes|additions)\*\*"),
    re.compile(r"\*\*V0\.\d (变更|添加)\*\*"),
    re.compile(r"— \*\*[A-Za-z ]*in V0\.\d\*\*"),  # "— **Refined in V0.2**"
]
# Frozen section-title pattern: a version range tag on a markdown heading line,
# e.g. "## 2. Event Catalog (V0.2 — 12 events)". Only flagged on heading lines so
# inline sourcing like "(V0.2 — see §2.5)" stays allowed.
_STALE_HEADING_PATTERN = re.compile(r"[（(]V0\.\d — ")

_NARRATIVE_DIRS = [ROOT / "docs", ROOT / "docs_cn", SPECIFICATION_DIR]


def test_no_stale_version_narrative():
    offenders = []
    for d in _NARRATIVE_DIRS:
        for path in sorted(d.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for lineno, line in enumerate(text.splitlines(), 1):
                for pat in _STALE_PATTERNS:
                    if pat.search(line):
                        offenders.append(f"{path.name}:{lineno}: {line.strip()}")
                if line.lstrip().startswith("#") and _STALE_HEADING_PATTERN.search(line):
                    offenders.append(f"{path.name}:{lineno}: {line.strip()}")
    assert not offenders, (
        "Stale present-tense version narrative (should describe the current "
        "cumulative state, not a past increment):\n" + "\n".join(offenders)
    )


def test_example_descriptions_carry_no_version_label():
    # Examples are version-neutral instances; provenance lives in registry §1.
    offenders = []
    for example_path in iter_examples():
        desc = _load_json(example_path).get("_description", "")
        if re.search(r"V0\.\d", desc):
            offenders.append(f"{example_path.name}: {desc}")
    assert not offenders, (
        "Example _description must not carry a version label "
        "(payload version is the protocol_version field):\n" + "\n".join(offenders)
    )


# ---------------------------------------------------------------------------
# Group 5 — cross-artifact integrity (registry ↔ schemas ↔ proto ↔ examples)
# ---------------------------------------------------------------------------

PROTO_PATH = SPECIFICATION_DIR / "proto" / "aizp.proto"
REGISTRY_PATH = SPECIFICATION_DIR / "registry.md"

# The .proto cannot reuse an enum value name across two enums in the same
# package, so three names carry a documented suffix vs. their JSON-canonical
# form (aizp.proto §enums). Any *undocumented* divergence must fail the sync
# test below — that is the whole point.
_PROTO_ALIASES = {
    "INTER_AGENT_DRIFT_TYPE": "INTER_AGENT_DRIFT",  # vs. INTER_AGENT_DRIFT event
    "RECENTERING_STATE": "RECENTERING",             # vs. RECENTERING event
    "SAFE_STOP_STATE": "SAFE_STOP",                 # vs. SAFE_STOP event
}


def _proto_enum_members(enum_name: str) -> set[str]:
    text = PROTO_PATH.read_text(encoding="utf-8")
    m = re.search(r"enum %s \{(.*?)\}" % enum_name, text, re.S)
    assert m, f"proto enum {enum_name} not found"
    members = re.findall(r"^\s*([A-Z][A-Z0-9_]*)\s*=", m.group(1), re.M)
    canonical = {_PROTO_ALIASES.get(x, x) for x in members}
    canonical.discard(f"{enum_name.upper()}_UNSPECIFIED")
    # also drop the generic *_UNSPECIFIED forms (enum names vary)
    return {x for x in canonical if not x.endswith("_UNSPECIFIED")}


def test_schemas_are_valid_jsonschema():
    # Each schema must itself be a legal Draft 2020-12 schema (catches typo'd
    # keywords / malformed enums that would silently weaken validation).
    for schema_path in sorted(SCHEMAS_DIR.glob("*.schema.json")):
        jsonschema.Draft202012Validator.check_schema(_load_json(schema_path))


def test_registry_events_match_schemas_and_examples():
    # registry §1 is the canonical event list; it MUST equal the set of event
    # schemas, and every event MUST have at least one conformant example.
    index = _build_event_schema_index()
    assert len(index) == 12, f"expected 12 event schemas, got {len(index)}"

    registry = REGISTRY_PATH.read_text(encoding="utf-8")
    events_section = registry.split("## 2.")[0]
    registry_events = set(re.findall(r"`([A-Z][A-Z_]+)`", events_section))
    assert registry_events == set(index), (
        "registry §1 events != event schemas: "
        f"only in registry={registry_events - set(index)}, "
        f"only in schemas={set(index) - registry_events}"
    )

    example_events = {_load_json(p).get("event") for p in iter_examples()}
    uncovered = set(index) - example_events
    assert not uncovered, f"events with no example payload: {sorted(uncovered)}"


def test_proto_enums_match_canonical_schemas():
    # The .proto is a second wire encoding; its enums must stay in lockstep with
    # the JSON-canonical sets (modulo the three documented suffix aliases).
    index = _build_event_schema_index()

    assert _proto_enum_members("EventType") == set(index), "EventType drift vs schemas"

    drift_enum = set(
        index["GRAVITY_DRIFT"]["properties"]["payload"]
        ["properties"]["drift_types"]["items"]["enum"]
    )
    assert _proto_enum_members("DriftType") == drift_enum, "DriftType drift vs schema"

    state_enum = set(
        index["GRAVITY_FORECAST"]["properties"]["payload"]
        ["properties"]["current_state"]["enum"]
    )
    assert _proto_enum_members("OrbitalState") == state_enum, "OrbitalState drift vs schema"


def _proto_message_fields(message_name: str) -> set[str]:
    text = PROTO_PATH.read_text(encoding="utf-8")
    m = re.search(r"message %s \{(.*?)\n\}" % message_name, text, re.S)
    assert m, f"proto message {message_name} not found"
    return set(re.findall(r"(?:^|\n)\s*(?:repeated\s+)?[\w.<>, ]+?\s+(\w+)\s*=\s*\d+", m.group(1)))


def test_proto_message_fields_match_schema_payloads():
    # Each event's proto message (PascalCase of the event name) must carry the
    # same payload field names as its JSON Schema — guards against name drift
    # like RECENTERING's old `method`/`gravity_score_before`.
    index = _build_event_schema_index()
    mismatches: dict[str, dict] = {}
    for event, schema in index.items():
        message = "".join(part.capitalize() for part in event.split("_"))
        schema_fields = set(schema["properties"]["payload"]["properties"])
        proto_fields = _proto_message_fields(message)
        if schema_fields != proto_fields:
            mismatches[event] = {
                "schema_only": sorted(schema_fields - proto_fields),
                "proto_only": sorted(proto_fields - schema_fields),
            }
    assert not mismatches, f"proto fields diverge from schema payloads:\n{mismatches}"


def test_wire_identifiers_are_release_independent():
    # ADR-009: the proto package and schema $id are named for the *wire* version
    # (wire2 / wire-2), never the release version, so doc-only releases do not
    # churn generated code or schema URLs. Guard against regression.
    proto = PROTO_PATH.read_text(encoding="utf-8")
    assert "package aizp.wire2;" in proto, "proto package must be aizp.wire2 (ADR-009)"
    assert re.search(r"package aizp\.v0_\d", proto) is None, (
        "proto package must not embed the release version"
    )
    for schema_path in sorted(SCHEMAS_DIR.glob("*.schema.json")):
        if schema_path.name == "aizp-config.schema.json":
            continue  # deployment config tracks the release line by design
        schema_id = _load_json(schema_path)["$id"]
        assert "/schemas/wire-2/" in schema_id, f"{schema_path.name}: $id must use /wire-2/"
        assert not re.search(r"/schemas/V0\.\d/", schema_id), (
            f"{schema_path.name}: $id must not embed the release version"
        )


def _iter_schema_enums(node):
    if isinstance(node, dict):
        if isinstance(node.get("enum"), list):
            yield node["enum"]
        for v in node.values():
            yield from _iter_schema_enums(v)
    elif isinstance(node, list):
        for v in node:
            yield from _iter_schema_enums(v)


def test_registry_documents_all_schema_enums():
    # registry.md is the single source of truth for enum allocations: every
    # UPPER_SNAKE enum value used by any event schema MUST appear in it.
    registry_tokens = set(
        re.findall(r"`([A-Z][A-Z0-9_]*)`", REGISTRY_PATH.read_text(encoding="utf-8"))
    )
    missing: dict[str, set[str]] = {}
    for schema_path in sorted(SCHEMAS_DIR.glob("*.schema.json")):
        if schema_path.name == "aizp-config.schema.json":
            continue
        for enum in _iter_schema_enums(_load_json(schema_path)):
            for value in enum:
                if re.fullmatch(r"[A-Z][A-Z0-9_]*", value) and value not in registry_tokens:
                    missing.setdefault(schema_path.name, set()).add(value)
    assert not missing, (
        "enum values used in schemas but undocumented in registry.md:\n"
        + "\n".join(f"  {k}: {sorted(v)}" for k, v in missing.items())
    )


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

def _main() -> int:
    failures = 0
    index = _build_event_schema_index()
    print(f"Loaded {len(index)} event schemas: {sorted(index)}")

    print("\n[1] Schema validation of examples/")
    for example_path in iter_examples():
        try:
            validate_example(example_path, index)
            print(f"  PASS  {example_path.name}")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"  FAIL  {example_path.name}: {exc}")

    print("\n[2] Gravity Score worked example (§5)")
    checks = [
        ("recency_decay", test_recency_decay),
        ("worked_example_transfer_funds", test_worked_example_transfer_funds),
        ("threshold_boundaries", test_threshold_boundaries),
    ]
    for name, fn in checks:
        try:
            fn()
            print(f"  PASS  {name}")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"  FAIL  {name}: {exc}")

    print("\n[3] Deployment config schema + version-narrative hygiene")
    hygiene = [
        ("config_example_validates", test_config_example_validates),
        ("threshold_single_source_of_truth", test_threshold_single_source_of_truth),
        ("no_stale_version_narrative", test_no_stale_version_narrative),
        ("example_descriptions_no_version_label", test_example_descriptions_carry_no_version_label),
    ]
    for name, fn in hygiene:
        try:
            fn()
            print(f"  PASS  {name}")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"  FAIL  {name}: {exc}")

    print("\n[4] Cross-artifact integrity (registry <-> schemas <-> proto <-> examples)")
    integrity = [
        ("schemas_are_valid_jsonschema", test_schemas_are_valid_jsonschema),
        ("registry_events_match_schemas_and_examples", test_registry_events_match_schemas_and_examples),
        ("proto_enums_match_canonical_schemas", test_proto_enums_match_canonical_schemas),
        ("proto_message_fields_match_schema_payloads", test_proto_message_fields_match_schema_payloads),
        ("registry_documents_all_schema_enums", test_registry_documents_all_schema_enums),
        ("wire_identifiers_are_release_independent", test_wire_identifiers_are_release_independent),
    ]
    for name, fn in integrity:
        try:
            fn()
            print(f"  PASS  {name}")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"  FAIL  {name}: {exc}")

    print(f"\n{'ALL PASS' if failures == 0 else str(failures) + ' FAILURE(S)'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(_main())
