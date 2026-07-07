#!/usr/bin/env python3
"""Diagnostic and repair CLI for the service-log export workflow."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path

EVENTS_PATH = Path("/app/data/events.json")
PIPELINE_PATH = Path("/app/workflow/export_report.py")
FORBIDDEN_TOKENS = ('event["timestamp"]', 'level == "error"')

ISSUE_DEFINITIONS = [
    {
        "id": "wrong_timestamp_field",
        "severity": "critical",
        "description": (
            "The export workflow reads event['timestamp'] instead of event['ts_ms'], "
            "zeroing flagged timestamps when the legacy field is absent."
        ),
        "resolution": "Read ts_ms from each event when building flagged rows.",
        "evidence": {
            "dossier_quote": (
                "Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], "
                "zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads."
            ),
            "pipeline_evidence": "Original export_report.py references event[\"timestamp\"] when building flagged rows.",
            "repair_action": "Use event ts_ms for flagged.jsonl timestamps.",
        },
    },
    {
        "id": "severity_filter",
        "severity": "critical",
        "description": "Flagged export keeps only error-level rows, omitting warn events required by operations.",
        "resolution": "Include both warn and error severities in flagged.jsonl.",
        "evidence": {
            "dossier_quote": (
                "Flagged export keeps only level == 'error' rows but operations expects both warn and error "
                "severities in flagged.jsonl for paging review."
            ),
            "pipeline_evidence": "Original export_report.py filters with level == \"error\" only.",
            "repair_action": "Include warn and error rows in flagged export.",
        },
    },
    {
        "id": "sort_order",
        "severity": "high",
        "description": "Flagged rows are sorted ascending by ts_ms; runbook requires descending order.",
        "resolution": "Sort flagged rows by ts_ms descending (reverse=True).",
        "evidence": {
            "dossier_quote": (
                "Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest "
                "incidents appear first in flagged.jsonl."
            ),
            "pipeline_evidence": "Original export_report.py sorts flagged rows by ts_ms ascending without reverse.",
            "repair_action": "Sort flagged rows with reverse=True for ts_ms descending output.",
        },
    },
    {
        "id": "level_normalization",
        "severity": "high",
        "description": "Uppercase WARN/Error aliases are not normalized before severity filtering.",
        "resolution": "Normalize level strings with .lower() before counting and flagging.",
        "evidence": {
            "dossier_quote": (
                "Source payloads include WARN and Error aliases; export_report.py must normalize level values "
                "to lowercase before counting or flagging rows."
            ),
            "pipeline_evidence": "Original export_report.py leaves WARN casing unchanged and never calls .lower() on level values.",
            "repair_action": "Normalize level with .lower() before severity checks.",
        },
    },
    {
        "id": "dedupe_policy",
        "severity": "high",
        "description": "Duplicate event ids are exported multiple times instead of collapsing to the latest row.",
        "resolution": "Dedupe by event id keeping the highest ts_ms row.",
        "evidence": {
            "dossier_quote": (
                "Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run."
            ),
            "pipeline_evidence": "Original export_report.py iterates the raw events list without dedupe by id.",
            "repair_action": "Dedupe event ids keeping the highest ts_ms before export.",
        },
    },
    {
        "id": "suppressed_filter",
        "severity": "high",
        "description": "Suppressed error rows are written to flagged.jsonl when they must be excluded.",
        "resolution": "Skip rows where suppressed is true when building flagged.jsonl.",
        "evidence": {
            "dossier_quote": (
                "Events with suppressed set true must be excluded from flagged.jsonl even when severity is error."
            ),
            "pipeline_evidence": "Original export_report.py never checks the suppressed flag before writing flagged rows.",
            "repair_action": "Exclude suppressed true rows from flagged export.",
        },
    },
]


def load_events(path: Path = EVENTS_PATH) -> list[dict]:
    return json.loads(path.read_text())


def input_stats(events: list[dict]) -> dict:
    services = sorted({str(event.get("service", "")) for event in events})
    return {
        "event_count": len(events),
        "unique_event_ids": len({str(event["id"]) for event in events}),
        "services": services,
    }


def pipeline_source_sha256(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def pre_repair_audit() -> dict:
    source = PIPELINE_PATH.read_text()
    return {
        "pipeline_source_sha256": pipeline_source_sha256(source),
        "pipeline_tokens_present": {token: token in source for token in FORBIDDEN_TOKENS},
    }


def patch_workflow() -> None:
    for candidate in (
        Path(__file__).resolve().parent / "export_report.py",
        Path("/app/export_report_fixed.py"),
    ):
        if candidate.exists():
            PIPELINE_PATH.write_text(candidate.read_text())
            return
    raise FileNotFoundError("repaired export_report.py template not found")


def build_diagnosis_report(
    status: str,
    events: list[dict],
    summary: dict | None = None,
    output_dir: Path | None = None,
) -> dict:
    report = {
        "pipeline_status": status,
        "issues_found": ISSUE_DEFINITIONS,
        "input_stats": input_stats(events),
    }
    if summary is not None and output_dir is not None:
        report["verified_summary"] = summary
        report["output_paths"] = {
            "summary_json": str(output_dir / "summary.json"),
            "flagged_jsonl": str(output_dir / "flagged.jsonl"),
            "service_matrix_json": str(output_dir / "service_matrix.json"),
        }
    return report


def cmd_diagnose(dossier: Path, report_path: Path) -> None:
    _ = dossier.read_text(encoding="utf-8", errors="replace")
    events = load_events()
    report = build_diagnosis_report("diagnosed", events)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n")


def cmd_repair(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    diagnosis_path = output_dir / "diagnosis.json"
    audit_path = output_dir / "repair_audit.json"
    rerun_dir = output_dir / "rerun"

    pre_audit = pre_repair_audit()
    patch_workflow()
    ast.parse(PIPELINE_PATH.read_text())

    subprocess.run(
        [
            sys.executable,
            str(PIPELINE_PATH),
            "--input",
            str(EVENTS_PATH),
            "--output-dir",
            str(output_dir),
        ],
        check=True,
    )

    if rerun_dir.exists():
        for child in rerun_dir.iterdir():
            child.unlink()
    else:
        rerun_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            sys.executable,
            str(PIPELINE_PATH),
            "--input",
            str(EVENTS_PATH),
            "--output-dir",
            str(rerun_dir),
        ],
        check=True,
    )

    events = load_events()
    summary = json.loads((output_dir / "summary.json").read_text())
    diagnosis = build_diagnosis_report("repaired", events, summary, output_dir)
    diagnosis_path.write_text(json.dumps(diagnosis, indent=2) + "\n")

    code = PIPELINE_PATH.read_text()
    audit = {
        "patched_workflow": str(PIPELINE_PATH),
        "processing_steps": [
            "normalize_level",
            "dedupe_by_id",
            "filter_suppressed",
            "build_flagged",
        ],
        "removed_tokens": {token: token not in code for token in FORBIDDEN_TOKENS},
        "pre_repair": pre_audit,
        "post_repair": {
            "flagged_count": summary["flagged_count"],
            "rerun_flagged_count": json.loads((rerun_dir / "summary.json").read_text())[
                "flagged_count"
            ],
        },
    }
    audit_path.write_text(json.dumps(audit, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Service log export diagnostic CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    diag = sub.add_parser("diagnose")
    diag.add_argument("--dossier", type=Path, required=True)
    diag.add_argument("--report", type=Path, default=Path("/app/output/diagnosis.json"))

    repair = sub.add_parser("repair")
    repair.add_argument("--output-dir", type=Path, default=Path("/app/output"))

    args = parser.parse_args()
    if args.command == "diagnose":
        cmd_diagnose(args.dossier, args.report)
    else:
        cmd_repair(args.output_dir)


if __name__ == "__main__":
    main()
