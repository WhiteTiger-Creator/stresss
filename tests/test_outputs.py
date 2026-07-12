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
SILENCE_PATH = Path("/app/data/silence_windows.json")
DEPENDENCY_PATH = Path("/app/data/service_dependencies.json")
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


def _normalize_level_scope(value: object) -> str:
    normalized = str(value).strip().lower()
    return normalized if normalized in {"all", "warn", "error"} else ""


def _compact_silence_windows(rows: list[dict]) -> dict[tuple[str, str], list[tuple[int, int]]]:
    by_key: dict[tuple[str, str], list[tuple[int, int]]] = {}
    for row in rows:
        service = _normalize_service(row.get("service", ""))
        scope = _normalize_level_scope(row.get("level_scope", ""))
        if not scope:
            continue
        start = _normalize_ts_ms(row.get("start_ms", 0))
        end = _normalize_ts_ms(row.get("end_ms", 0))
        if end <= start:
            continue
        by_key.setdefault((service, scope), []).append((start, end))

    compacted: dict[tuple[str, str], list[tuple[int, int]]] = {}
    for key, intervals in by_key.items():
        merged: list[list[int]] = []
        for start, end in sorted(intervals):
            if not merged or start > merged[-1][1]:
                merged.append([start, end])
            else:
                merged[-1][1] = max(merged[-1][1], end)
        compacted[key] = [(start, end) for start, end in merged]
    return compacted


def _is_silenced(event: dict, compacted: dict[tuple[str, str], list[tuple[int, int]]]) -> bool:
    service = _normalize_service(event.get("service", ""))
    level = _normalize_level(event.get("level", ""))
    ts_ms = _normalize_ts_ms(event.get("ts_ms", 0))
    for scope in ("all", level):
        for start, end in compacted.get((service, scope), []):
            if start <= ts_ms < end:
                return True
    return False


def _silence_compaction_checksum(compacted: dict[tuple[str, str], list[tuple[int, int]]]) -> str:
    return hashlib.sha256(
        "\n".join(
            f"{service}|{scope}|{start}|{end}"
            for service, scope in sorted(compacted)
            for start, end in compacted[(service, scope)]
        ).encode("utf-8")
    ).hexdigest()


def _canonicalize_dependency_rules(rows: list[dict]) -> list[dict]:
    deduped: dict[tuple[str, str, int, int], int] = {}
    for row in rows:
        upstream = _normalize_service(row.get("upstream_service", ""))
        downstream = _normalize_service(row.get("downstream_service", ""))
        lag_min = _normalize_ts_ms(row.get("lag_min_ms", 0))
        lag_max = _normalize_ts_ms(row.get("lag_max_ms", 0))
        weight = _normalize_ts_ms(row.get("weight", 0))
        if not upstream or not downstream or lag_min < 0 or lag_max <= lag_min or weight <= 0:
            continue
        key = (upstream, downstream, lag_min, lag_max)
        deduped[key] = max(deduped.get(key, 0), weight)
    return [
        {
            "upstream_service": upstream,
            "downstream_service": downstream,
            "lag_min_ms": lag_min,
            "lag_max_ms": lag_max,
            "weight": deduped[(upstream, downstream, lag_min, lag_max)],
        }
        for upstream, downstream, lag_min, lag_max in sorted(deduped)
    ]


def _dependency_compaction_checksum(rules: list[dict]) -> str:
    return hashlib.sha256(
        "\n".join(
            f"{row['upstream_service']}|{row['downstream_service']}|"
            f"{row['lag_min_ms']}|{row['lag_max_ms']}|{row['weight']}"
            for row in rules
        ).encode("utf-8")
    ).hexdigest()


def _dependency_blast_radius(
    service: str, rules: list[dict]
) -> tuple[list[str], int]:
    edge_weights: dict[tuple[str, str], int] = {}
    for rule in rules:
        edge = (rule["upstream_service"], rule["downstream_service"])
        edge_weights[edge] = max(edge_weights.get(edge, 0), rule["weight"])
    adjacency: dict[str, list[tuple[str, int]]] = {}
    for (upstream, downstream), weight in edge_weights.items():
        adjacency.setdefault(upstream, []).append((downstream, weight))
    for upstream in adjacency:
        adjacency[upstream].sort()

    strongest_capacity: dict[str, int] = {}
    for downstream, weight in adjacency.get(service, []):
        if downstream != service:
            strongest_capacity[downstream] = max(
                strongest_capacity.get(downstream, 0), weight
            )
        for second_hop, second_weight in adjacency.get(downstream, []):
            if second_hop == service:
                continue
            capacity = min(weight, second_weight)
            strongest_capacity[second_hop] = max(
                strongest_capacity.get(second_hop, 0), capacity
            )
    services = sorted(strongest_capacity)
    return services, sum(strongest_capacity.values())


def _probe_overlap_ms(anchor_ms: int, spans: list[tuple[int, int]], lookback_ms: int = 90) -> int:
    probe_start = anchor_ms - lookback_ms
    probe_end = anchor_ms + 1
    total = 0
    for start_ms, end_ms in spans:
        overlap_start = max(probe_start, start_ms)
        overlap_end = min(probe_end, end_ms)
        if overlap_end > overlap_start:
            total += overlap_end - overlap_start
    return total


def _silence_pressure_score(
    event: dict, compacted_silence: dict[tuple[str, str], list[tuple[int, int]]]
) -> int:
    service = _normalize_service(event.get("service", ""))
    level = _normalize_level(event.get("level", ""))
    ts_ms = _normalize_ts_ms(event.get("ts_ms", 0))
    all_overlap_ms = _probe_overlap_ms(ts_ms, compacted_silence.get((service, "all"), []))
    level_overlap_ms = _probe_overlap_ms(ts_ms, compacted_silence.get((service, level), []))
    return (all_overlap_ms // 25) + (level_overlap_ms // 15)


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


def _compute_summary(
    events: list[dict],
    silence_rows: list[dict] | None = None,
    dependency_rows: list[dict] | None = None,
) -> dict:
    canonical = _canonicalize_events(events)
    level_counts = {level: 0 for level in LEVEL_ORDER}
    services: set[str] = set()
    silence_rows = (
        json.loads(SILENCE_PATH.read_text()) if silence_rows is None else silence_rows
    )
    compacted_silence = _compact_silence_windows(silence_rows)
    dependency_rows = (
        json.loads(DEPENDENCY_PATH.read_text()) if dependency_rows is None else dependency_rows
    )
    dependency_rules = _canonicalize_dependency_rules(dependency_rows)
    flagged = _compute_flagged(
        events, silence_rows=silence_rows, dependency_rows=dependency_rows
    )
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
        "silence_excluded_count": sum(
            1
            for event in canonical
            if event["level"] in FLAGGED_LEVELS
            and not _normalize_suppressed(event.get("suppressed", False))
            and _is_silenced(event, compacted_silence)
        ),
        "canonical_fingerprint": hashlib.sha1(
            "\n".join(
                f"{event['id']}|{event['ts_ms']}|{event['level']}|{event['service']}|"
                f"{event['message']}|{1 if _normalize_suppressed(event.get('suppressed', False)) else 0}"
                for event in canonical
            ).encode("utf-8")
        ).hexdigest(),
        "silence_compaction_checksum": _silence_compaction_checksum(compacted_silence),
        "dependency_compaction_checksum": _dependency_compaction_checksum(dependency_rules),
        "max_silence_pressure_score": max(
            (row["silence_pressure_score"] for row in flagged),
            default=0,
        ),
        "max_dependency_pressure_score": max(
            (row["dependency_pressure_score"] for row in flagged),
            default=0,
        ),
        "max_causal_burst_score": max(
            (row["causal_burst_score"] for row in flagged),
            default=0,
        ),
        "max_dependency_chain_depth": max(
            (row["dependency_chain_depth"] for row in flagged),
            default=0,
        ),
        "max_blast_radius_score": max(
            (row["blast_radius_score"] for row in flagged),
            default=0,
        ),
        "blast_radius_digest_checksum": hashlib.sha256(
            "|".join(row["blast_radius_digest"] for row in flagged).encode("utf-8")
        ).hexdigest(),
        "lineage_digest_checksum": hashlib.sha256(
            "|".join(row["lineage_digest"] for row in flagged).encode("utf-8")
        ).hexdigest(),
        "flagged_digest_checksum": hashlib.sha256(
            "|".join(row["event_digest"] for row in flagged).encode("utf-8")
        ).hexdigest(),
    }


def _compute_flagged(
    events: list[dict],
    silence_rows: list[dict] | None = None,
    dependency_rows: list[dict] | None = None,
) -> list[dict]:
    silence_rows = (
        json.loads(SILENCE_PATH.read_text()) if silence_rows is None else silence_rows
    )
    compacted_silence = _compact_silence_windows(silence_rows)
    dependency_rows = (
        json.loads(DEPENDENCY_PATH.read_text()) if dependency_rows is None else dependency_rows
    )
    dependency_rules = _canonicalize_dependency_rules(dependency_rows)
    rows = []
    for event in _canonicalize_events(events):
        if not _is_flagged(event):
            continue
        if _is_silenced(event, compacted_silence):
            continue
        pressure_score = _silence_pressure_score(event, compacted_silence)
        rows.append(
            {
                "id": event["id"],
                "ts_ms": event["ts_ms"],
                "level": event["level"],
                "service": event["service"],
                "message": event["message"],
                "silence_pressure_score": pressure_score,
            }
        )
    chronological = sorted(rows, key=lambda row: (row["ts_ms"], str(row["id"])))
    finalized_by_id: dict[str, dict] = {}
    for target_index, target in enumerate(chronological):
        candidates: list[tuple[int, int, str]] = []
        for source in chronological[:target_index]:
            if source["ts_ms"] >= target["ts_ms"]:
                continue
            lag = target["ts_ms"] - source["ts_ms"]
            contributions = [
                rule["weight"] * SEVERITY_RANK.get(source["level"], 0)
                + source["silence_pressure_score"]
                + (source["dependency_pressure_score"] // 2)
                for rule in dependency_rules
                if rule["upstream_service"] == source["service"]
                and rule["downstream_service"] == target["service"]
                and rule["lag_min_ms"] <= lag < rule["lag_max_ms"]
            ]
            if contributions:
                candidates.append((max(contributions), source["ts_ms"], str(source["id"])))
        strongest = sorted(candidates, key=lambda item: (-item[0], -item[1], item[2]))[:3]
        target["dependency_pressure_score"] = sum(item[0] for item in strongest)
        target["dependency_source_ids"] = [item[2] for item in strongest]
        lineage_ids: list[str] = []
        source_burst_rollup = 0
        source_depths: list[int] = []
        for rank, (_, _, source_id) in enumerate(strongest):
            source = finalized_by_id[source_id]
            source_burst_rollup += source["causal_burst_score"] // (rank + 2)
            source_depths.append(source["dependency_chain_depth"])
            for lineage_id in [source_id, *source["dependency_lineage_ids"]]:
                if lineage_id not in lineage_ids:
                    lineage_ids.append(lineage_id)
                if len(lineage_ids) == 5:
                    break
            if len(lineage_ids) == 5:
                break
        target["dependency_chain_depth"] = (
            min(1 + max(source_depths), 6) if source_depths else 0
        )
        target["dependency_lineage_ids"] = lineage_ids
        target["causal_burst_score"] = min(
            target["dependency_pressure_score"]
            + source_burst_rollup
            + (target["dependency_chain_depth"] * 3),
            9999,
        )
        (
            target["blast_radius_services"],
            target["blast_radius_score"],
        ) = _dependency_blast_radius(target["service"], dependency_rules)
        target["blast_radius_digest"] = hashlib.sha1(
            (
                f"{target['service']}|{','.join(target['blast_radius_services'])}|"
                f"{target['blast_radius_score']}"
            ).encode("utf-8")
        ).hexdigest()[:10]
        target["lineage_digest"] = hashlib.sha256(
            (
                f"{target['id']}|{target['dependency_chain_depth']}|"
                f"{target['causal_burst_score']}|{','.join(lineage_ids)}"
            ).encode("utf-8")
        ).hexdigest()[:12]
        target["event_digest"] = hashlib.sha1(
            (
                f"{target['id']}|{target['ts_ms']}|{target['level']}|{target['service']}|"
                f"{target['message']}|{target['silence_pressure_score']}|"
                f"{target['dependency_pressure_score']}|{','.join(target['dependency_source_ids'])}|"
                f"{target['dependency_chain_depth']}|{target['causal_burst_score']}|"
                f"{','.join(target['dependency_lineage_ids'])}|{target['lineage_digest']}|"
                f"{target['blast_radius_score']}|{','.join(target['blast_radius_services'])}|"
                f"{target['blast_radius_digest']}"
            ).encode("utf-8")
        ).hexdigest()[:10]
        finalized_by_id[str(target["id"])] = target
    rows.sort(key=lambda row: row["id"])
    rows.sort(key=lambda row: row["silence_pressure_score"], reverse=True)
    rows.sort(key=lambda row: row["dependency_chain_depth"], reverse=True)
    rows.sort(key=lambda row: row["dependency_pressure_score"], reverse=True)
    rows.sort(key=lambda row: row["blast_radius_score"], reverse=True)
    rows.sort(key=lambda row: row["causal_burst_score"], reverse=True)
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
        "silence_excluded_count",
        "canonical_fingerprint",
        "silence_compaction_checksum",
        "dependency_compaction_checksum",
        "max_silence_pressure_score",
        "max_dependency_pressure_score",
        "max_causal_burst_score",
        "max_dependency_chain_depth",
        "max_blast_radius_score",
        "blast_radius_digest_checksum",
        "lineage_digest_checksum",
        "flagged_digest_checksum",
    ):
        assert verified[key] == expected[key]
    assert list(verified["level_counts"].keys()) == list(LEVEL_ORDER)
    assert len(verified["canonical_fingerprint"]) == 40
    assert len(verified["blast_radius_digest_checksum"]) == 64
    assert len(verified["lineage_digest_checksum"]) == 64
    assert len(verified["flagged_digest_checksum"]) == 64


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
        assert isinstance(row["silence_pressure_score"], int)
        assert isinstance(row["dependency_pressure_score"], int)
        assert isinstance(row["dependency_source_ids"], list)
        assert isinstance(row["dependency_chain_depth"], int)
        assert isinstance(row["dependency_lineage_ids"], list)
        assert isinstance(row["causal_burst_score"], int)
        assert isinstance(row["blast_radius_services"], list)
        assert isinstance(row["blast_radius_score"], int)
        assert len(row["blast_radius_digest"]) == 10
        assert len(row["lineage_digest"]) == 12
        assert len(row["event_digest"]) == 10


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
    assert summary["silence_excluded_count"] == alt["silence_excluded_count"]
    assert summary["canonical_fingerprint"] == alt["canonical_fingerprint"]
    assert summary["silence_compaction_checksum"] == alt["silence_compaction_checksum"]
    assert summary["dependency_compaction_checksum"] == alt["dependency_compaction_checksum"]
    assert summary["max_silence_pressure_score"] == alt["max_silence_pressure_score"]
    assert summary["max_dependency_pressure_score"] == alt["max_dependency_pressure_score"]
    assert summary["max_causal_burst_score"] == alt["max_causal_burst_score"]
    assert summary["max_dependency_chain_depth"] == alt["max_dependency_chain_depth"]
    assert summary["max_blast_radius_score"] == alt["max_blast_radius_score"]
    assert summary["blast_radius_digest_checksum"] == alt[
        "blast_radius_digest_checksum"
    ]
    assert summary["lineage_digest_checksum"] == alt["lineage_digest_checksum"]
    assert summary["flagged_digest_checksum"] == alt["flagged_digest_checksum"]
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


def test_repair_repatches_reset_workflow_with_custom_output_dir(
    tmp_path_factory, expected: dict
):
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
        assert 'event["timestamp"]' not in PIPELINE.read_text()
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


def test_flagged_sort_tie_break_on_silence_pressure_score(tmp_path_factory):
    original_silence = SILENCE_PATH.read_text()
    try:
        silence_rows = [
            {"service": "api", "level_scope": "all", "start_ms": 450, "end_ms": 500},
            {"service": "api", "level_scope": "error", "start_ms": 430, "end_ms": 500},
        ]
        SILENCE_PATH.write_text(json.dumps(silence_rows, indent=2) + "\n")
        events = [
            {"id": "p2", "ts_ms": 500, "level": "error", "service": "db", "message": "low pressure"},
            {"id": "p1", "ts_ms": 500, "level": "error", "service": "api", "message": "high pressure"},
            {"id": "p3", "ts_ms": 500, "level": "warn", "service": "api", "message": "warn pressure"},
        ]
        input_path = tmp_path_factory.mktemp("pressure_sort") / "events.json"
        input_path.write_text(json.dumps(events))
        out_dir = tmp_path_factory.mktemp("pressure_sort_out")
        result = _run_pipeline(input_path=input_path, output_dir=out_dir)
        assert result.returncode == 0, result.stderr

        flagged = _flagged_rows(out_dir / "flagged.jsonl")
        assert [row["id"] for row in flagged] == ["p1", "p2", "p3"]
        assert flagged[0]["silence_pressure_score"] > flagged[1]["silence_pressure_score"]
        assert flagged[1]["silence_pressure_score"] >= 0
    finally:
        SILENCE_PATH.write_text(original_silence)


def test_canonical_fingerprint_uses_ts_ms_ascending_canonical_order(tmp_path_factory):
    events = [
        {"id": "f1", "ts_ms": 500, "level": "warn", "service": "api", "message": "late"},
        {"id": "f2", "ts_ms": 100, "level": "info", "service": "api", "message": "early"},
        {"id": "f3", "ts_ms": " 300 ", "level": "error", "service": "database", "message": "mid"},
    ]
    input_path = tmp_path_factory.mktemp("fingerprint_order") / "events.json"
    input_path.write_text(json.dumps(events))
    out_dir = tmp_path_factory.mktemp("fingerprint_order_out")
    result = _run_pipeline(input_path=input_path, output_dir=out_dir)
    assert result.returncode == 0, result.stderr

    summary = json.loads((out_dir / "summary.json").read_text())
    canonical = _canonicalize_events(events)
    assert [row["ts_ms"] for row in canonical] == [100, 300, 500]
    expected_fingerprint = hashlib.sha1(
        "\n".join(
            f"{row['id']}|{row['ts_ms']}|{row['level']}|{row['service']}|{row['message']}|"
            f"{1 if _normalize_suppressed(row.get('suppressed', False)) else 0}"
            for row in canonical
        ).encode("utf-8")
    ).hexdigest()
    assert summary["canonical_fingerprint"] == expected_fingerprint


def test_pipeline_does_not_reference_test_or_solution_artifacts():
    pipeline_code = _executable_text(PIPELINE.read_text())
    cli_code = _executable_text(CLI.read_text())
    forbidden = ["/tests", "expected_summary.json", "fixtures/alt_events.json", "/solution/"]
    for token in forbidden:
        assert token not in pipeline_code
        assert token not in cli_code


def test_silence_source_path_affects_output(tmp_path_factory):
    original_silence = SILENCE_PATH.read_text()
    try:
        baseline_dir = tmp_path_factory.mktemp("silence_base")
        baseline = _run_pipeline(output_dir=baseline_dir)
        assert baseline.returncode == 0, baseline.stderr
        baseline_summary = json.loads((baseline_dir / "summary.json").read_text())
        baseline_flagged = _flagged_rows(baseline_dir / "flagged.jsonl")

        SILENCE_PATH.write_text("[]\n")
        no_silence_dir = tmp_path_factory.mktemp("silence_none")
        no_silence = _run_pipeline(output_dir=no_silence_dir)
        assert no_silence.returncode == 0, no_silence.stderr
        no_silence_summary = json.loads((no_silence_dir / "summary.json").read_text())
        no_silence_flagged = _flagged_rows(no_silence_dir / "flagged.jsonl")

        assert baseline_summary["silence_excluded_count"] > 0
        assert no_silence_summary["silence_excluded_count"] == 0
        assert baseline_summary["silence_compaction_checksum"] != no_silence_summary[
            "silence_compaction_checksum"
        ]
        assert len(no_silence_flagged) > len(baseline_flagged)
    finally:
        SILENCE_PATH.write_text(original_silence)


def test_silence_compaction_and_level_scope_exercised(tmp_path_factory):
    original_silence = SILENCE_PATH.read_text()
    try:
        silence_rows = [
            {"service": "api-gw", "level_scope": "warn", "start_ms": 100, "end_ms": 130},
            {"service": "api gateway", "level_scope": "warn", "start_ms": 130, "end_ms": 180},
            {"service": "api", "level_scope": "all", "start_ms": 200, "end_ms": 240},
            {"service": "api", "level_scope": "debug", "start_ms": 0, "end_ms": 999},
        ]
        SILENCE_PATH.write_text(json.dumps(silence_rows, indent=2) + "\n")
        events = [
            {"id": "q1", "ts_ms": 120, "level": "warn", "service": "api-gw", "message": "warn silenced"},
            {"id": "q2", "ts_ms": 120, "level": "error", "service": "api gateway", "message": "error kept"},
            {"id": "q3", "ts_ms": 210, "level": "error", "service": "api", "message": "all silenced"},
            {"id": "q4", "ts_ms": 260, "level": "warn", "service": "api", "message": "warn kept"},
        ]
        input_path = tmp_path_factory.mktemp("silence_scope") / "events.json"
        input_path.write_text(json.dumps(events))
        out_dir = tmp_path_factory.mktemp("silence_scope_out")
        result = _run_pipeline(input_path=input_path, output_dir=out_dir)
        assert result.returncode == 0, result.stderr

        summary = json.loads((out_dir / "summary.json").read_text())
        flagged = _flagged_rows(out_dir / "flagged.jsonl")
        assert summary["silence_excluded_count"] == 2
        assert [row["id"] for row in flagged] == ["q4", "q2"]
    finally:
        SILENCE_PATH.write_text(original_silence)


def test_silence_checksum_worked_example_matches_source_data():
    example = SPEC_DATA["canonicalization"][
        "silence_compaction_checksum_worked_example"
    ]
    compacted = _compact_silence_windows(json.loads(SILENCE_PATH.read_text()))
    payload = "\n".join(
        f"{service}|{scope}|{start}|{end}"
        for service, scope in sorted(compacted)
        for start, end in compacted[(service, scope)]
    )
    assert payload == example["exact_sha256_payload"]
    assert hashlib.sha256(payload.encode("utf-8")).hexdigest() == example[
        "expected_sha256"
    ]


def test_dependency_source_path_affects_output(tmp_path_factory):
    original_dependencies = DEPENDENCY_PATH.read_text()
    try:
        baseline_dir = tmp_path_factory.mktemp("dependency_base")
        baseline = _run_pipeline(output_dir=baseline_dir)
        assert baseline.returncode == 0, baseline.stderr
        baseline_summary = json.loads((baseline_dir / "summary.json").read_text())
        baseline_flagged = _flagged_rows(baseline_dir / "flagged.jsonl")

        DEPENDENCY_PATH.write_text("[]\n")
        empty_dir = tmp_path_factory.mktemp("dependency_empty")
        empty = _run_pipeline(output_dir=empty_dir)
        assert empty.returncode == 0, empty.stderr
        empty_summary = json.loads((empty_dir / "summary.json").read_text())
        empty_flagged = _flagged_rows(empty_dir / "flagged.jsonl")

        assert baseline_summary["max_dependency_pressure_score"] > 0
        assert empty_summary["max_dependency_pressure_score"] == 0
        assert baseline_summary["max_blast_radius_score"] > 0
        assert empty_summary["max_blast_radius_score"] == 0
        assert baseline_summary["dependency_compaction_checksum"] != empty_summary[
            "dependency_compaction_checksum"
        ]
        assert [row["id"] for row in baseline_flagged] == [row["id"] for row in empty_flagged]
        assert baseline_summary["flagged_digest_checksum"] != empty_summary[
            "flagged_digest_checksum"
        ]
        assert baseline_summary["lineage_digest_checksum"] != empty_summary[
            "lineage_digest_checksum"
        ]
        assert baseline_summary["blast_radius_digest_checksum"] != empty_summary[
            "blast_radius_digest_checksum"
        ]
    finally:
        DEPENDENCY_PATH.write_text(original_dependencies)


def test_dependency_dedupe_lag_boundaries_and_top_three_sources(tmp_path_factory):
    original_dependencies = DEPENDENCY_PATH.read_text()
    try:
        rules = [
            {
                "upstream_service": "api-gw",
                "downstream_service": "worker",
                "lag_min_ms": 50,
                "lag_max_ms": 200,
                "weight": 2,
            },
            {
                "upstream_service": "api gateway",
                "downstream_service": "worker-batch",
                "lag_min_ms": "50",
                "lag_max_ms": "200",
                "weight": 4,
            },
            {
                "upstream_service": "database",
                "downstream_service": "worker",
                "lag_min_ms": 50,
                "lag_max_ms": 100,
                "weight": 3,
            },
            {
                "upstream_service": "api",
                "downstream_service": "worker",
                "lag_min_ms": -1,
                "lag_max_ms": 500,
                "weight": 99,
            },
        ]
        DEPENDENCY_PATH.write_text(json.dumps(rules, indent=2) + "\n")
        events = [
            {"id": "s1", "ts_ms": 100, "level": "error", "service": "api", "message": "first"},
            {"id": "s2", "ts_ms": 110, "level": "warn", "service": "api-gw", "message": "second"},
            {"id": "s3", "ts_ms": 120, "level": "error", "service": "db", "message": "third"},
            {"id": "s4", "ts_ms": 200, "level": "error", "service": "worker", "message": "target"},
        ]
        input_path = tmp_path_factory.mktemp("dependency_rules") / "events.json"
        input_path.write_text(json.dumps(events))
        out_dir = tmp_path_factory.mktemp("dependency_rules_out")
        result = _run_pipeline(input_path=input_path, output_dir=out_dir)
        assert result.returncode == 0, result.stderr

        flagged = _flagged_rows(out_dir / "flagged.jsonl")
        target = next(row for row in flagged if row["id"] == "s4")
        assert target["dependency_source_ids"] == ["s1", "s3", "s2"]
        assert target["dependency_pressure_score"] == 40
        assert target["dependency_chain_depth"] == 1
        assert target["dependency_lineage_ids"] == ["s1", "s3", "s2"]
        assert target["causal_burst_score"] == 43
        assert json.loads((out_dir / "summary.json").read_text()) == _compute_summary(
            events, dependency_rows=rules
        )
    finally:
        DEPENDENCY_PATH.write_text(original_dependencies)


def test_recursive_dependency_lineage_and_burst_propagation(tmp_path_factory):
    original_dependencies = DEPENDENCY_PATH.read_text()
    try:
        rules = [
            {
                "upstream_service": "api",
                "downstream_service": "worker",
                "lag_min_ms": 1,
                "lag_max_ms": 200,
                "weight": 4,
            },
            {
                "upstream_service": "worker",
                "downstream_service": "db",
                "lag_min_ms": 1,
                "lag_max_ms": 200,
                "weight": 2,
            },
        ]
        DEPENDENCY_PATH.write_text(json.dumps(rules) + "\n")
        events = [
            {"id": "a", "ts_ms": 100, "level": "error", "service": "api", "message": "a"},
            {"id": "b", "ts_ms": 200, "level": "error", "service": "worker", "message": "b"},
            {"id": "c", "ts_ms": 300, "level": "error", "service": "db", "message": "c"},
        ]
        input_path = tmp_path_factory.mktemp("lineage") / "events.json"
        input_path.write_text(json.dumps(events))
        out_dir = tmp_path_factory.mktemp("lineage_out")
        result = _run_pipeline(input_path=input_path, output_dir=out_dir)
        assert result.returncode == 0, result.stderr
        by_id = {row["id"]: row for row in _flagged_rows(out_dir / "flagged.jsonl")}
        assert by_id["a"]["dependency_chain_depth"] == 0
        assert by_id["a"]["dependency_lineage_ids"] == []
        assert by_id["a"]["causal_burst_score"] == 0
        assert by_id["b"]["dependency_chain_depth"] == 1
        assert by_id["b"]["dependency_lineage_ids"] == ["a"]
        assert by_id["b"]["causal_burst_score"] == 19
        assert by_id["c"]["dependency_chain_depth"] == 2
        assert by_id["c"]["dependency_lineage_ids"] == ["b", "a"]
        assert by_id["c"]["causal_burst_score"] == 31
    finally:
        DEPENDENCY_PATH.write_text(original_dependencies)


def test_dependency_blast_radius_is_cycle_safe_and_uses_strongest_path(
    tmp_path_factory,
):
    original_dependencies = DEPENDENCY_PATH.read_text()
    try:
        rules = [
            {
                "upstream_service": "api",
                "downstream_service": "worker",
                "lag_min_ms": 1,
                "lag_max_ms": 200,
                "weight": 4,
            },
            {
                "upstream_service": "worker",
                "downstream_service": "db",
                "lag_min_ms": 1,
                "lag_max_ms": 200,
                "weight": 3,
            },
            {
                "upstream_service": "api",
                "downstream_service": "db",
                "lag_min_ms": 1,
                "lag_max_ms": 200,
                "weight": 2,
            },
            {
                "upstream_service": "db",
                "downstream_service": "api",
                "lag_min_ms": 1,
                "lag_max_ms": 200,
                "weight": 9,
            },
        ]
        DEPENDENCY_PATH.write_text(json.dumps(rules) + "\n")
        events = [
            {
                "id": "origin",
                "ts_ms": 100,
                "level": "error",
                "service": "api",
                "message": "origin",
            }
        ]
        input_path = tmp_path_factory.mktemp("blast") / "events.json"
        input_path.write_text(json.dumps(events))
        out_dir = tmp_path_factory.mktemp("blast_out")
        result = _run_pipeline(input_path=input_path, output_dir=out_dir)
        assert result.returncode == 0, result.stderr
        row = _flagged_rows(out_dir / "flagged.jsonl")[0]
        assert row["blast_radius_services"] == ["db", "worker"]
        assert row["blast_radius_score"] == 7
        assert len(row["blast_radius_digest"]) == 10
    finally:
        DEPENDENCY_PATH.write_text(original_dependencies)


def test_flagged_sort_tie_break_on_dependency_pressure(tmp_path_factory):
    original_dependencies = DEPENDENCY_PATH.read_text()
    try:
        rules = [
            {
                "upstream_service": "api",
                "downstream_service": "worker",
                "lag_min_ms": 1,
                "lag_max_ms": 200,
                "weight": 4,
            },
            {
                "upstream_service": "api",
                "downstream_service": "db",
                "lag_min_ms": 1,
                "lag_max_ms": 200,
                "weight": 1,
            },
        ]
        DEPENDENCY_PATH.write_text(json.dumps(rules) + "\n")
        events = [
            {"id": "source", "ts_ms": 100, "level": "error", "service": "api", "message": "source"},
            {"id": "lower", "ts_ms": 200, "level": "error", "service": "db", "message": "lower"},
            {"id": "higher", "ts_ms": 200, "level": "error", "service": "worker", "message": "higher"},
        ]
        input_path = tmp_path_factory.mktemp("dependency_sort") / "events.json"
        input_path.write_text(json.dumps(events))
        out_dir = tmp_path_factory.mktemp("dependency_sort_out")
        result = _run_pipeline(input_path=input_path, output_dir=out_dir)
        assert result.returncode == 0, result.stderr
        flagged = _flagged_rows(out_dir / "flagged.jsonl")
        assert [row["id"] for row in flagged[:2]] == ["higher", "lower"]
        assert flagged[0]["dependency_pressure_score"] > flagged[1][
            "dependency_pressure_score"
        ]
    finally:
        DEPENDENCY_PATH.write_text(original_dependencies)
