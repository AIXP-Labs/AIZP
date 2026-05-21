"""AIZP V0.6 document-consistency guards.

These complement `test_aizp.py` (schema / enum / threshold integrity) by locking
in three *documentation* invariants that manual review rounds repeatedly caught
and that the existing version-narrative hygiene test does NOT cover:

  A. No stale version strings — a `protocol_version` literal inside any doc code
     fence must be the current release; no "V0.x reference implementation" prose.
  B. Prose count consistency — narrative counts ("N-protocol AIXP stack",
     "N drift detectors", ...) must equal the single canonical count.
  C. Section-number contiguity — top-level `## N.` headings in a numbered doc
     must be a gap-free, in-order run (catches a skipped or transposed section).

Run with pytest:      pytest tests/
Run standalone:       python tests/test_consistency.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC_DIRS = [ROOT / "docs", ROOT / "docs_cn", ROOT / "specification"]
TOP_LEVEL_FILES = [ROOT / "README.md", ROOT / "README_CN.md", ROOT / "CHANGELOG.md"]

CURRENT_VERSION = "V0.6"


def _iter_md(include_top: bool = True):
    seen: set[Path] = set()
    for d in DOC_DIRS:
        for path in sorted(d.rglob("*.md")):
            if path not in seen:
                seen.add(path)
                yield path
    if include_top:
        for path in TOP_LEVEL_FILES:
            if path.exists() and path not in seen:
                seen.add(path)
                yield path


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


# ---------------------------------------------------------------------------
# Guard A — version-string hygiene (code fences + version-claim prose)
# ---------------------------------------------------------------------------

_PV_IN_CODE = re.compile(r'protocol_version["\s:=]+["\']?(V0\.\d)')
# Present-tense capability claims pinned to an old version (e.g. the OTel
# "V0.2 reference implementations SHOULD ..." that slipped past hygiene).
_VERSION_CLAIM_PROSE = [
    re.compile(r"V0\.[1-5] reference implementation"),
    re.compile(r"V0\.[1-5] 参考实现"),
]


def test_no_stale_protocol_version_in_code_fences():
    # CHANGELOG/ADRs legitimately narrate version transitions, so this scans
    # only the doc/spec trees and only inside ``` fenced blocks.
    offenders = []
    for path in _iter_md(include_top=False):
        in_fence = False
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if not in_fence:
                continue
            m = _PV_IN_CODE.search(line)
            if m and m.group(1) != CURRENT_VERSION:
                offenders.append(f"{_rel(path)}:{lineno}: {line.strip()}")
    assert not offenders, (
        f"protocol_version in a code sample must be {CURRENT_VERSION}:\n"
        + "\n".join(offenders)
    )


def test_no_version_pinned_capability_prose():
    offenders = []
    for path in _iter_md(include_top=False):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for pat in _VERSION_CLAIM_PROSE:
                if pat.search(line):
                    offenders.append(f"{_rel(path)}:{lineno}: {line.strip()}")
    assert not offenders, (
        "Capability described as belonging to a past version (use the current "
        "cumulative voice, or 'Since V0.x' for provenance):\n" + "\n".join(offenders)
    )


# ---------------------------------------------------------------------------
# Guard B — prose count consistency
# ---------------------------------------------------------------------------

# (regex, expected_count, label). Patterns target the exact phrasing that
# regressed in review — the AIXP stack count (8 protocols; 10 projects).
#
# Drift-type/detector counts are deliberately NOT matched here: prose uses them
# as minimums ("≥3 of 11"), per-stage subsets ("2 drift types"), test fixtures
# ("inject 2 drift types"), and version-transition history ("6 → 11"), all of
# which are legitimate. The drift-type TOTAL (11) is already enforced
# structurally in test_aizp.py (registry ↔ schema ↔ proto), so a prose guard
# here would add only false positives.
_COUNT_PATTERNS = [
    (re.compile(r"(\d+)[- ]protocol AIXP stack"), 8, "AIXP protocol count"),
    (re.compile(r"(\d+)\s*协议\s*AIXP\s*栈"), 8, "AIXP protocol count (cn)"),
    (re.compile(r"(\d+) AIXP-stack projects"), 10, "AIXP project count"),
]


def test_prose_counts_match_canonical():
    offenders = []
    for path in _iter_md(include_top=True):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for pat, expected, label in _COUNT_PATTERNS:
                for m in pat.finditer(line):
                    if int(m.group(1)) != expected:
                        offenders.append(
                            f"{_rel(path)}:{lineno}: {label} = {m.group(1)} "
                            f"(canonical {expected}): {line.strip()}"
                        )
    assert not offenders, "Prose count diverges from canonical:\n" + "\n".join(offenders)


# ---------------------------------------------------------------------------
# Guard C — section-number contiguity in numbered docs
# ---------------------------------------------------------------------------

# Match a top-level numbered heading "## N. Title" but NOT a decimal subsection
# promoted to ## level (e.g. "## 8.5 ..."), which is an intentional insert.
_HEADING = re.compile(r"^##\s+(\d+)\.(?=\s|$)")
# Docs that intentionally do not use a single contiguous ## N. sequence.
_CONTIGUITY_SKIP: set[str] = set()


def test_section_numbers_are_contiguous():
    offenders = []
    for path in _iter_md(include_top=False):
        if _rel(path) in _CONTIGUITY_SKIP:
            continue
        nums = []
        in_fence = False
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            m = _HEADING.match(line)
            if m:
                nums.append(int(m.group(1)))
        if len(nums) < 3:
            continue  # not a numbered-section document
        expected = list(range(nums[0], nums[0] + len(nums)))
        if nums != expected:
            offenders.append(f"{_rel(path)}: ## headings {nums} (expected {expected})")
    assert not offenders, (
        "Top-level section numbers must be a gap-free, in-order run:\n"
        + "\n".join(offenders)
    )


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

def _main() -> int:
    failures = 0
    checks = [
        ("no_stale_protocol_version_in_code_fences", test_no_stale_protocol_version_in_code_fences),
        ("no_version_pinned_capability_prose", test_no_version_pinned_capability_prose),
        ("prose_counts_match_canonical", test_prose_counts_match_canonical),
        ("section_numbers_are_contiguous", test_section_numbers_are_contiguous),
    ]
    print("[consistency guards]")
    for name, fn in checks:
        try:
            fn()
            print(f"  PASS  {name}")
        except AssertionError as exc:
            failures += 1
            print(f"  FAIL  {name}:\n{exc}\n")
    print(f"\n{'ALL PASS' if failures == 0 else str(failures) + ' FAILURE(S)'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(_main())
