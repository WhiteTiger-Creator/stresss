"""Verify service-log audit CLI and repaired export workflow."""

from __future__ import annotations

import ast
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

OUTPUT_DIR = Path("/app/output")
DIAGNOSIS_PATH = OUTPUT_DIR / "diagnosis.json"
SUMMARY_PATH = OUTPUT_DIR / "summary.json"
MATRIX_PATH = OUTPUT_DIR / "service_matrix.json"
FLAGGED_PATH = OUTPUT_DIR / "flagged.jsonl"
REPAIR_AUDIT_PATH = OUTPUT_DIR / "repair_audit.json"
CLI = Path("/app/log_audit.py")
PIPELINE = Path("/app/workflow/export_report.py")
ORIGINAL_PIPELINE = Path("/app/workflow/.export_report.original")
DOSSIER_PATH = Path("/app/incident/export_dossier.md")
INPUT_PATH = Path("/app/data/events.json")
REPORT_SPEC_PATH = Path("/app/docs/report_spec.json")
FIXTURES = Path("/tests/fixtures/expected_summary.json")
SPEC_DATA = json.loads(REPORT_SPEC_PATH.read_text())
FIXTURE_DATA = json.loads(FIXTURES.read_text())
ISSUE_EVIDENCE_TERMS = SPEC_DATA["diagnosis_report"]["issues_found_item"]["evidence"][
    "required_terms_by_issue"
]
REQUIRED_ISSUE_IDS = SPEC_DATA["diagnosis_report"]["issues_found_item"]["allowed_ids"]
FORBIDDEN_TOKENS = tuple(
    SPEC_DATA["repair_audit"]["forbidden_executable_tokens"]
)
REQUIRED_TOKENS = tuple(
    SPEC_DATA["workflow_repair"]["required_executable_tokens"]
)
FLAGGED_LEVELS = {"warn", "error"}
LEVEL_ORDER = ("debug", "error", "info", "warn")


def _normalize_ws(text: str) -> str:
    return " ".join(text.split())


def _executable_text(src: str) -> str:
    docstring_lines: set[int] = set()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
            continue
        if not node.body:
            continue
        first = node.body[0]
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
            if isinstance(first.value.value, str):
                end = getattr(first, "end_lineno", first.lineno)
                docstring_lines.update(range(first.lineno, end + 1))

    lines: list[str] = []
    for line_number, line in enumerate(src.splitlines(), start=1):
        if line_number in docstring_lines:
            continue
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if "#" in line:
            line = line.split("#", 1)[0]
        lines.append(line)
    return "\n".join(lines)


def _load_events(path: Path) -> list[dict]:
    return json.loads(path.read_text())


def _canonicalize_events(events: list[dict]) -> list[dict]:
    deduped: dict[str, dict] = {}
    for event in events:
        normalized = dict(event)
        normalized["level"] = str(normalized.get("level", "")).lower()
        event_id = str(normalized["id"])
        current = deduped.get(event_id)
        if current is None or normalized["ts_ms"] > current["ts_ms"]:
            deduped[event_id] = normalized
    return sorted(deduped.values(), key=lambda row: row["ts_ms"])


def _is_flagged(event: dict) -> bool:
    if event.get("suppressed") is True:
        return False
    return event["level"] in FLAGGED_LEVELS


def _build_service_matrix(events: list[dict]) -> dict[str, dict[str, int]]:
    matrix: dict[str, dict[str, int]] = {}
    for event in events:
        service = str(event.get("service", ""))
        level = str(event.get("level", ""))
        matrix.setdefault(service, {name: 0 for name in LEVEL_ORDER})
        if level in matrix[service]:
            matrix[service][level] += 1
    return {service: matrix[service] for service in sorted(matrix)}


def _compute_summary(events: list[dict]) -> dict:
    canonical = _canonicalize_events(events)
    level_counts = {level: 0 for level in LEVEL_ORDER}
    services: set[str] = set()
    flagged = _compute_flagged(events)
    for event in canonical:
        level = str(event.get("level", ""))
        if level in level_counts:
            level_counts[level] += 1
        services.add(str(event.get("service", "")))
    return {
        "schema_version": "service-log-report-v2",
        "raw_event_count": len(events),
        "unique_event_ids": len({str(event["id"]) for event in events}),
        "total_events": len(canonical),
        "level_counts": level_counts,
        "services": sorted(services),
        "flagged_count": len(flagged),
        "suppressed_excluded_count": sum(
            1
            for event in canonical
            if event.get("suppressed") is True and event["level"] in FLAGGED_LEVELS
        ),
    }


def _compute_flagged(events: list[dict]) -> list[dict]:
    rows = []
    for event in _canonicalize_events(events):
        if not _is_flagged(event):
            continue
        rows.append(
            {
                "id": event["id"],
                "ts_ms": event["ts_ms"],
                "level": event["level"],
                "service": event["service"],
                "message": event["message"],
            }
        )
    rows.sort(key=lambda row: row["ts_ms"], reverse=True)
    return rows


def _run_pipeline(
    pipeline: Path = PIPELINE,
    input_path: Path = INPUT_PATH,
    output_dir: Path = OUTPUT_DIR,
) -> subprocess.CompletedProcess[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        [
            "python3",
            str(pipeline),
            "--input",
            str(input_path),
            "--output-dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )


def _flagged_rows(path: Path = FLAGGED_PATH) -> list[dict]:
    rows = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


@pytest.fixture(scope="module")
def expected() -> dict:
    return FIXTURE_DATA


@pytest.fixture(scope="module")
def dossier_text() -> str:
    return _normalize_ws(DOSSIER_PATH.read_text())


@pytest.fixture(scope="module")
def diagnosis() -> dict:
    assert DIAGNOSIS_PATH.exists(), (
        f"Missing {DIAGNOSIS_PATH}. Run: python3 {CLI} repair --output-dir /app/output"
    )
    return json.loads(DIAGNOSIS_PATH.read_text())


@pytest.fixture(scope="module")
def summary(diagnosis: dict) -> dict:
    assert SUMMARY_PATH.exists(), "missing summary.json"
    data = json.loads(SUMMARY_PATH.read_text())
    assert data == diagnosis["verified_summary"]
    return data


@pytest.fixture(scope="module")
def flagged_rows() -> list[dict]:
    assert FLAGGED_PATH.exists(), "missing flagged.jsonl"
    return _flagged_rows()


def test_cli_exists():
    assert CLI.exists(), f"CLI not found at {CLI}"


def test_dossier_is_long_context():
    assert len(DOSSIER_PATH.read_text().splitlines()) >= 500


def test_repair_produces_required_outputs():
    for path in (SUMMARY_PATH, MATRIX_PATH, FLAGGED_PATH, REPAIR_AUDIT_PATH):
        assert path.exists(), f"missing required output: {path}"


def test_diagnosis_schema_repaired(diagnosis: dict):
    for key in ("pipeline_status", "issues_found", "input_stats", "verified_summary", "output_paths"):
        assert key in diagnosis
    assert diagnosis["pipeline_status"] == "repaired"


def test_output_paths_exact(diagnosis: dict):
    paths = diagnosis["output_paths"]
    assert paths["summary_json"] == str(SUMMARY_PATH)
    assert paths["flagged_jsonl"] == str(FLAGGED_PATH)
    assert paths["service_matrix_json"] == str(MATRIX_PATH)


def test_issues_found_exactly_six_allowed_ids(diagnosis: dict, expected: dict):
    assert len(diagnosis["issues_found"]) == 6
    assert {item["id"] for item in diagnosis["issues_found"]} == set(REQUIRED_ISSUE_IDS)


def test_issue_item_required_fields(diagnosis: dict):
    for issue in diagnosis["issues_found"]:
        for key in ("id", "severity", "description", "resolution", "evidence"):
            assert key in issue


def test_issue_evidence(diagnosis: dict):
    original_pipeline = ORIGINAL_PIPELINE.read_text()
    issues = {item["id"]: item for item in diagnosis["issues_found"]}
    for issue_id, terms in ISSUE_EVIDENCE_TERMS.items():
        evidence = issues[issue_id]["evidence"]
        for key in ("dossier_quote", "pipeline_evidence", "repair_action"):
            assert key in evidence
            assert len(evidence[key]) >= 10
        assert len(evidence["dossier_quote"]) >= 30
        for term in terms["dossier_quote"]:
            assert term in evidence["dossier_quote"]
        for term in terms["pipeline_evidence"]:
            assert term in evidence["pipeline_evidence"]
        assert evidence["pipeline_evidence"] in original_pipeline
        for term in terms["repair_action"]:
            assert term in evidence["repair_action"]


def test_dossier_quotes_are_verbatim(diagnosis: dict, dossier_text: str):
    for issue in diagnosis["issues_found"]:
        quote = _normalize_ws(issue["evidence"]["dossier_quote"])
        assert quote in dossier_text


def test_input_stats(diagnosis: dict, expected: dict):
    stats = diagnosis["input_stats"]
    assert stats["event_count"] == expected["event_count"]
    assert stats["unique_event_ids"] == expected["unique_ids"]
    assert stats["services"] == expected["services"]


def test_verified_summary_matches_fixture(diagnosis: dict, expected: dict):
    verified = diagnosis["verified_summary"]
    for key in (
        "schema_version",
        "raw_event_count",
        "unique_event_ids",
        "total_events",
        "level_counts",
        "services",
        "flagged_count",
        "suppressed_excluded_count",
    ):
        assert verified[key] == expected[key]
    assert list(verified["level_counts"].keys()) == list(LEVEL_ORDER)


def test_summary_computed_from_events(summary: dict):
    assert summary == _compute_summary(_load_events(INPUT_PATH))


def test_service_matrix_matches_fixture(expected: dict):
    matrix = json.loads(MATRIX_PATH.read_text())
    assert matrix == expected["expected_service_matrix"]
    assert matrix == _build_service_matrix(_canonicalize_events(_load_events(INPUT_PATH)))


def test_flagged_computed_from_events(flagged_rows: list[dict]):
    assert flagged_rows == _compute_flagged(_load_events(INPUT_PATH))


def test_flagged_sorted_descending(flagged_rows: list[dict], expected: dict):
    assert [row["id"] for row in flagged_rows] == expected["expected_flagged_ids_desc"]
    assert [row["ts_ms"] for row in flagged_rows] == expected["expected_flagged_ts_ms_desc"]


def test_flagged_levels(flagged_rows: list[dict]):
    for row in flagged_rows:
        assert row["level"] in FLAGGED_LEVELS


def test_flagged_jsonl_compact_format():
    for line in FLAGGED_PATH.read_text().splitlines():
        if not line.strip():
            continue
        assert ": " not in line
        parsed = json.loads(line)
        assert json.dumps(parsed, separators=(",", ":")) == line


def test_original_snapshot_preserved(expected: dict):
    assert ORIGINAL_PIPELINE.exists()
    digest = hashlib.sha256(ORIGINAL_PIPELINE.read_bytes()).hexdigest()
    assert digest == expected["broken_pipeline_sha256"]
    original = ORIGINAL_PIPELINE.read_text()
    for token in FORBIDDEN_TOKENS:
        assert token in original
    assert ".lower(" not in original


def test_broken_snapshot_produces_wrong_export(expected: dict):
    with tempfile.TemporaryDirectory() as tmp:
        broken = Path(tmp) / "export_report.py"
        out = Path(tmp) / "out"
        shutil.copy(ORIGINAL_PIPELINE, broken)
        result = _run_pipeline(pipeline=broken, output_dir=out)
        assert result.returncode == 0, result.stderr
        summary = json.loads((out / "summary.json").read_text())
        flagged = _flagged_rows(out / "flagged.jsonl")
        assert summary["flagged_count"] == expected["broken_flagged_count"]
        assert [row["id"] for row in flagged] == expected["broken_flagged_ids_asc"]
        assert all(row["ts_ms"] == 0 for row in flagged)


def test_pipeline_patched():
    ast.parse(PIPELINE.read_text())
    code = _executable_text(PIPELINE.read_text())
    for token in FORBIDDEN_TOKENS:
        assert token not in code
    for token in REQUIRED_TOKENS:
        assert token in code


def test_repair_audit(diagnosis: dict, expected: dict, summary: dict):
    audit = json.loads(REPAIR_AUDIT_PATH.read_text())
    code = _executable_text(PIPELINE.read_text())
    assert audit["patched_workflow"] == str(PIPELINE)
    assert audit["processing_steps"] == SPEC_DATA["repair_audit"]["processing_steps"]
    assert audit["removed_tokens"] == {
        token: token not in code for token in FORBIDDEN_TOKENS
    }
    assert all(audit["removed_tokens"].values())
    assert audit["pre_repair"]["pipeline_source_sha256"] == expected["broken_pipeline_sha256"]
    assert audit["pre_repair"]["pipeline_tokens_present"] == {
        token: True for token in FORBIDDEN_TOKENS
    }
    assert audit["post_repair"]["flagged_count"] == summary["flagged_count"]
    assert audit["post_repair"]["rerun_flagged_count"] == summary["flagged_count"]


def test_pipeline_reruns_idempotently(summary: dict, flagged_rows: list[dict], tmp_path_factory):
    rerun_dir = tmp_path_factory.mktemp("rerun")
    result = _run_pipeline(output_dir=rerun_dir)
    assert result.returncode == 0, result.stderr
    rerun_summary = json.loads((rerun_dir / "summary.json").read_text())
    rerun_flagged = _flagged_rows(rerun_dir / "flagged.jsonl")
    assert rerun_summary == summary
    assert rerun_flagged == flagged_rows


def test_patched_pipeline_supports_alternate_input(expected: dict, tmp_path_factory):
    alt_dir = tmp_path_factory.mktemp("alt")
    alt_input = Path(expected["alternate_input"])
    result = _run_pipeline(input_path=alt_input, output_dir=alt_dir)
    assert result.returncode == 0, result.stderr
    summary = json.loads((alt_dir / "summary.json").read_text())
    flagged = _flagged_rows(alt_dir / "flagged.jsonl")
    events = _load_events(alt_input)
    assert summary == _compute_summary(events)
    assert flagged == _compute_flagged(events)
    alt = expected["alternate_expected"]
    assert summary["raw_event_count"] == alt["raw_event_count"]
    assert summary["flagged_count"] == alt["flagged_count"]
    assert summary["suppressed_excluded_count"] == alt["suppressed_excluded_count"]
    assert [row["id"] for row in flagged] == alt["flagged_ids_desc"]


def test_cli_diagnose_subcommand(expected: dict, dossier_text: str):
    report = OUTPUT_DIR / "diagnosis_redundant.json"
    if report.exists():
        report.unlink()
    result = subprocess.run(
        [
            "python3",
            str(CLI),
            "diagnose",
            "--dossier",
            str(DOSSIER_PATH),
            "--report",
            str(report),
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert report.exists(), f"diagnose failed (rc={result.returncode}): {result.stderr}"
    data = json.loads(report.read_text())
    assert data["pipeline_status"] == "diagnosed"
    original_pipeline = ORIGINAL_PIPELINE.read_text()
    assert "input_stats" in data
    assert data["input_stats"]["event_count"] == expected["event_count"]
    assert data["input_stats"]["unique_event_ids"] == expected["unique_ids"]
    assert data["input_stats"]["services"] == expected["services"]
    for key in ("verified_summary", "output_paths"):
        assert key not in data
    assert {item["id"] for item in data["issues_found"]} == set(REQUIRED_ISSUE_IDS)
    for issue in data["issues_found"]:
        for key in ("id", "severity", "description", "resolution", "evidence"):
            assert key in issue
        for key in ("dossier_quote", "pipeline_evidence", "repair_action"):
            assert key in issue["evidence"]
            assert len(issue["evidence"][key]) >= 10
        assert issue["evidence"]["pipeline_evidence"] in original_pipeline
        quote = _normalize_ws(issue["evidence"]["dossier_quote"])
        assert quote in dossier_text


def test_repair_supports_custom_output_dir(tmp_path_factory, expected: dict):
    custom_dir = tmp_path_factory.mktemp("custom_output")
    current = PIPELINE.read_text()
    try:
        shutil.copy(ORIGINAL_PIPELINE, PIPELINE)
        result = subprocess.run(
            ["python3", str(CLI), "repair", "--output-dir", str(custom_dir)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, result.stderr
        summary = json.loads((custom_dir / "summary.json").read_text())
        flagged = _flagged_rows(custom_dir / "flagged.jsonl")
        diagnosis = json.loads((custom_dir / "diagnosis.json").read_text())
        assert summary == _compute_summary(_load_events(INPUT_PATH))
        assert flagged == _compute_flagged(_load_events(INPUT_PATH))
        assert diagnosis["output_paths"]["summary_json"] == str(custom_dir / "summary.json")
        assert diagnosis["output_paths"]["flagged_jsonl"] == str(custom_dir / "flagged.jsonl")
        assert diagnosis["output_paths"]["service_matrix_json"] == str(custom_dir / "service_matrix.json")
        assert summary["flagged_count"] == expected["flagged_count"]
    finally:
        PIPELINE.write_text(current)
