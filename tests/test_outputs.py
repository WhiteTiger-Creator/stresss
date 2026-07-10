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
SEVERITY_RANK = {"debug": 1, "info": 2, "warn": 3, "error": 4}
SERVICE_ALIASES = {
    "api-gw": "api",
    "api gateway": "api",
    "database": "db",
    "worker-batch": "worker",
}


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


def _normalize_level(value: object) -> str:
    return str(value).strip().lower()


def _normalize_service(value: object) -> str:
    normalized = str(value).strip().lower()
    return SERVICE_ALIASES.get(normalized, normalized)


def _normalize_ts_ms(value: object) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return 0


def _normalize_message(value: object) -> str:
    return " ".join(str(value).split())


def _normalize_suppressed(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes"}:
            return True
        if lowered in {"false", "0", "no", ""}:
            return False
    return bool(value)


def _canonicalize_events(events: list[dict]) -> list[dict]:
    deduped: dict[str, dict] = {}
    for event in events:
        normalized = dict(event)
        normalized["level"] = _normalize_level(normalized.get("level", ""))
        normalized["service"] = _normalize_service(normalized.get("service", ""))
        normalized["ts_ms"] = _normalize_ts_ms(normalized.get("ts_ms", 0))
        normalized["message"] = _normalize_message(normalized.get("message", ""))
        normalized["suppressed"] = _normalize_suppressed(normalized.get("suppressed", False))
        event_id = str(normalized["id"])
        current = deduped.get(event_id)
        should_replace = current is None or normalized["ts_ms"] > current["ts_ms"]
        if (
            not should_replace
            and current is not None
            and normalized["ts_ms"] == current["ts_ms"]
        ):
            current_rank = SEVERITY_RANK.get(str(current.get("level", "")), 0)
            next_rank = SEVERITY_RANK.get(str(normalized.get("level", "")), 0)
            if next_rank > current_rank:
                should_replace = True
            elif next_rank == current_rank:
                normalized_suppressed = _normalize_suppressed(normalized.get("suppressed", False))
                current_suppressed = _normalize_suppressed(current.get("suppressed", False))
                if current_suppressed and not normalized_suppressed:
                    should_replace = True
                elif current_suppressed == normalized_suppressed:
                    next_message = _normalize_message(normalized.get("message", ""))
                    current_message = _normalize_message(current.get("message", ""))
                    if next_message > current_message:
                        should_replace = True
                    elif next_message == current_message:
                        next_service = _normalize_service(normalized.get("service", ""))
                        current_service = _normalize_service(current.get("service", ""))
                        should_replace = next_service > current_service
        if should_replace:
            deduped[event_id] = normalized
    return sorted(deduped.values(), key=lambda row: row["ts_ms"])


def _is_flagged(event: dict) -> bool:
    if _normalize_suppressed(event.get("suppressed", False)):
        return False
    return event["level"] in FLAGGED_LEVELS


def _build_service_matrix(events: list[dict]) -> dict[str, dict[str, int]]:
    matrix: dict[str, dict[str, int]] = {}
    for event in events:
        service = _normalize_service(event.get("service", ""))
        level = _normalize_level(event.get("level", ""))
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
            if _normalize_suppressed(event.get("suppressed", False))
            and event["level"] in FLAGGED_LEVELS
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
    rows.sort(key=lambda row: row["id"])
    rows.sort(key=lambda row: SEVERITY_RANK.get(row["level"], 0), reverse=True)
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
            assert term.lower() in evidence["dossier_quote"].lower()
        for term in terms["pipeline_evidence"]:
            assert term in evidence["pipeline_evidence"]
        assert evidence["pipeline_evidence"] in original_pipeline
        for term in terms["repair_action"]:
            assert term.lower() in evidence["repair_action"].lower()


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


def test_service_and_suppressed_normalization_edge_cases(tmp_path_factory):
    events = [
        {
            "id": "s1",
            "ts_ms": 10,
            "level": " WARN ",
            "service": " API ",
            "message": "warn one",
        },
        {
            "id": "s2",
            "ts_ms": 20,
            "level": " error ",
            "service": "api",
            "message": "suppressed string true",
            "suppressed": "YeS",
        },
        {
            "id": "s3",
            "ts_ms": 30,
            "level": "warn",
            "service": " Api  ",
            "message": "kept",
            "suppressed": "no",
        },
    ]
    input_path = tmp_path_factory.mktemp("norm") / "events.json"
    input_path.write_text(json.dumps(events))
    out_dir = tmp_path_factory.mktemp("norm_out")
    result = _run_pipeline(input_path=input_path, output_dir=out_dir)
    assert result.returncode == 0, result.stderr

    summary = json.loads((out_dir / "summary.json").read_text())
    flagged = _flagged_rows(out_dir / "flagged.jsonl")
    matrix = json.loads((out_dir / "service_matrix.json").read_text())

    assert summary["services"] == ["api"]
    assert summary["flagged_count"] == 2
    assert summary["suppressed_excluded_count"] == 1
    assert [row["id"] for row in flagged] == ["s3", "s1"]
    assert matrix == {"api": {"debug": 0, "error": 1, "info": 0, "warn": 2}}


def test_dedupe_tie_break_on_level_then_message(tmp_path_factory):
    events = [
        {
            "id": "d1",
            "ts_ms": 100,
            "level": "warn",
            "service": "worker",
            "message": "aaa",
        },
        {
            "id": "d1",
            "ts_ms": 100,
            "level": "error",
            "service": "worker",
            "message": "bbb",
        },
        {
            "id": "d2",
            "ts_ms": 200,
            "level": "warn",
            "service": "worker",
            "message": "alpha",
        },
        {
            "id": "d2",
            "ts_ms": 200,
            "level": "warn",
            "service": "worker",
            "message": "zeta",
        },
    ]
    input_path = tmp_path_factory.mktemp("tie") / "events.json"
    input_path.write_text(json.dumps(events))
    out_dir = tmp_path_factory.mktemp("tie_out")
    result = _run_pipeline(input_path=input_path, output_dir=out_dir)
    assert result.returncode == 0, result.stderr

    flagged = _flagged_rows(out_dir / "flagged.jsonl")
    kept = {row["id"]: row for row in flagged}

    assert len(flagged) == 2
    assert kept["d1"]["level"] == "error"
    assert kept["d1"]["message"] == "bbb"
    assert kept["d2"]["message"] == "zeta"


def test_ts_ms_normalization_and_invalid_fallback(tmp_path_factory):
    events = [
        {
            "id": "t1",
            "ts_ms": " 410 ",
            "level": "warn",
            "service": "api",
            "message": " keep   spaces   compact ",
        },
        {
            "id": "t2",
            "ts_ms": "invalid",
            "level": "error",
            "service": "api",
            "message": "bad ts",
        },
    ]
    input_path = tmp_path_factory.mktemp("ts_norm") / "events.json"
    input_path.write_text(json.dumps(events))
    out_dir = tmp_path_factory.mktemp("ts_norm_out")
    result = _run_pipeline(input_path=input_path, output_dir=out_dir)
    assert result.returncode == 0, result.stderr

    flagged = _flagged_rows(out_dir / "flagged.jsonl")
    assert [row["id"] for row in flagged] == ["t1", "t2"]
    assert flagged[0]["ts_ms"] == 410
    assert flagged[0]["message"] == "keep spaces compact"
    assert flagged[1]["ts_ms"] == 0


def test_service_alias_and_dedupe_tie_break_prefers_non_suppressed_then_service(tmp_path_factory):
    events = [
        {
            "id": "a1",
            "ts_ms": 100,
            "level": "warn",
            "service": "api-gw",
            "message": "same msg",
            "suppressed": "yes",
        },
        {
            "id": "a1",
            "ts_ms": 100,
            "level": "warn",
            "service": "api gateway",
            "message": "same msg",
            "suppressed": "no",
        },
        {
            "id": "a2",
            "ts_ms": 200,
            "level": "warn",
            "service": "database",
            "message": "db alias",
        },
        {
            "id": "a3",
            "ts_ms": 300,
            "level": "warn",
            "service": "worker-batch",
            "message": "worker alias",
        },
    ]
    input_path = tmp_path_factory.mktemp("svc_alias") / "events.json"
    input_path.write_text(json.dumps(events))
    out_dir = tmp_path_factory.mktemp("svc_alias_out")
    result = _run_pipeline(input_path=input_path, output_dir=out_dir)
    assert result.returncode == 0, result.stderr

    summary = json.loads((out_dir / "summary.json").read_text())
    matrix = json.loads((out_dir / "service_matrix.json").read_text())
    flagged = _flagged_rows(out_dir / "flagged.jsonl")

    assert summary["services"] == ["api", "db", "worker"]
    assert matrix["api"]["warn"] == 1
    assert matrix["db"]["warn"] == 1
    assert matrix["worker"]["warn"] == 1
    assert [row["service"] for row in flagged] == ["worker", "db", "api"]


def test_flagged_sort_tie_break_on_severity_then_id(tmp_path_factory):
    events = [
        {"id": "z2", "ts_ms": 500, "level": "warn", "service": "api", "message": "warn row"},
        {"id": "z1", "ts_ms": 500, "level": "error", "service": "api", "message": "error row"},
        {"id": "a9", "ts_ms": 500, "level": "error", "service": "api", "message": "error same ts"},
    ]
    input_path = tmp_path_factory.mktemp("sort_tie") / "events.json"
    input_path.write_text(json.dumps(events))
    out_dir = tmp_path_factory.mktemp("sort_tie_out")
    result = _run_pipeline(input_path=input_path, output_dir=out_dir)
    assert result.returncode == 0, result.stderr

    flagged = _flagged_rows(out_dir / "flagged.jsonl")
    assert [row["id"] for row in flagged] == ["a9", "z1", "z2"]
    assert [row["level"] for row in flagged] == ["error", "error", "warn"]
