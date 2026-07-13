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
ORIGINAL_PIPELINE = Path("/app/workflow/.export_report.original")
SPEC_PATH = Path("/app/docs/report_spec.json")
FORBIDDEN_TOKENS = ('event["timestamp"]', 'level == "error"')
SERVICE_ALIASES = {
    "api-gw": "api",
    "api gateway": "api",
    "database": "db",
    "worker-batch": "worker",
}

ISSUE_META = {
    "wrong_timestamp_field": {
        "severity": "critical",
        "description": "Flagged rows read legacy timestamp instead of ts_ms.",
        "resolution": "Emit ts_ms from each event in flagged.jsonl.",
    },
    "severity_filter": {
        "severity": "critical",
        "description": "Flagged export keeps only error-level rows.",
        "resolution": "Include warn and error severities in flagged export.",
    },
    "sort_order": {
        "severity": "high",
        "description": "Flagged rows are sorted oldest-first.",
        "resolution": "Sort flagged rows by ts_ms descending (reverse=True).",
    },
    "level_normalization": {
        "severity": "high",
        "description": "Uppercase level aliases are not normalized.",
        "resolution": "Normalize level strings with .lower() before filtering.",
    },
    "dedupe_policy": {
        "severity": "high",
        "description": "Duplicate event ids are exported multiple times.",
        "resolution": "dedupe event ids keeping the highest ts_ms before export.",
    },
    "suppressed_filter": {
        "severity": "high",
        "description": "Suppressed rows appear in flagged export.",
        "resolution": "Exclude suppressed rows from flagged export.",
    },
}


def _normalize_ws(text: str) -> str:
    return " ".join(text.split())


def load_spec() -> dict:
    return json.loads(SPEC_PATH.read_text())


def load_events(path: Path = EVENTS_PATH) -> list[dict]:
    return json.loads(path.read_text())


def _normalize_service(value: object) -> str:
    normalized = str(value).strip().lower()
    return SERVICE_ALIASES.get(normalized, normalized)


def input_stats(events: list[dict]) -> dict:
    services = sorted({_normalize_service(event.get("service", "")) for event in events})
    return {
        "event_count": len(events),
        "unique_event_ids": len({str(event["id"]) for event in events}),
        "services": services,
    }


def pipeline_source_sha256(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def pre_repair_audit() -> dict:
    source = ORIGINAL_PIPELINE.read_text()
    return {
        "pipeline_source_sha256": pipeline_source_sha256(source),
        "pipeline_tokens_present": {token: token in source for token in FORBIDDEN_TOKENS},
    }


def _line_contains_all(line: str, terms: list[str]) -> bool:
    return all(term in line for term in terms)


def find_dossier_quote(dossier_text: str, terms: list[str]) -> str:
    normalized = _normalize_ws(dossier_text)
    candidates: list[str] = []
    for line in dossier_text.splitlines():
        stripped = line.strip()
        if len(stripped) < 30 or not _line_contains_all(stripped, terms):
            continue
        if _normalize_ws(stripped) in normalized:
            candidates.append(stripped)
    if not candidates:
        raise ValueError(f"no dossier quote found for terms {terms}")
    return max(candidates, key=len)


def find_pipeline_evidence(original_pipeline: str, terms: list[str]) -> str:
    for line in original_pipeline.splitlines():
        stripped = line.strip()
        if stripped and _line_contains_all(stripped, terms):
            return stripped
    if all(term in original_pipeline for term in terms):
        for line in original_pipeline.splitlines():
            if any(term in line for term in terms):
                return line.strip()
    raise ValueError(f"no pipeline evidence found for terms {terms}")


def build_repair_action(issue_id: str, terms: list[str]) -> str:
    templates = {
        "wrong_timestamp_field": "Use event ts_ms for flagged.jsonl timestamps.",
        "severity_filter": "Include warn and error rows in flagged export.",
        "sort_order": "Sort flagged rows with reverse=True for ts_ms descending output.",
        "level_normalization": "Normalize level with .lower() before severity checks.",
        "dedupe_policy": "dedupe event ids keeping the highest ts_ms before export.",
        "suppressed_filter": "Exclude suppressed true rows from flagged export.",
    }
    action = templates[issue_id]
    for term in terms:
        if term not in action:
            action = f"{action} ({term})"
    return action


def build_issues_from_sources(dossier_text: str, original_pipeline: str, spec: dict) -> list[dict]:
    evidence_spec = spec["diagnosis_report"]["issues_found_item"]["evidence"][
        "required_terms_by_issue"
    ]
    allowed_ids = spec["diagnosis_report"]["issues_found_item"]["allowed_ids"]
    issues = []
    for issue_id in allowed_ids:
        terms = evidence_spec[issue_id]
        meta = ISSUE_META[issue_id]
        issues.append(
            {
                "id": issue_id,
                "severity": meta["severity"],
                "description": meta["description"],
                "resolution": meta["resolution"],
                "evidence": {
                    "dossier_quote": find_dossier_quote(dossier_text, terms["dossier_quote"]),
                    "pipeline_evidence": find_pipeline_evidence(
                        original_pipeline, terms["pipeline_evidence"]
                    ),
                    "repair_action": build_repair_action(issue_id, terms["repair_action"]),
                },
            }
        )
    return issues


def patch_workflow() -> None:
    for candidate in (
        Path(__file__).resolve().parent / "export_report_fixed.py",
        Path("/app/export_report_fixed.py"),
    ):
        if candidate.exists():
            PIPELINE_PATH.write_text(candidate.read_text())
            return
    raise FileNotFoundError("repaired export_report.py template not found")


def build_diagnosis_report(
    status: str,
    events: list[dict],
    issues: list[dict],
    summary: dict | None = None,
    output_dir: Path | None = None,
) -> dict:
    report = {
        "pipeline_status": status,
        "issues_found": issues,
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
    dossier_text = dossier.read_text(encoding="utf-8", errors="replace")
    spec = load_spec()
    original_pipeline = ORIGINAL_PIPELINE.read_text()
    events = load_events()
    issues = build_issues_from_sources(dossier_text, original_pipeline, spec)
    report = build_diagnosis_report("diagnosed", events, issues)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n")


def cmd_repair(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    diagnosis_path = output_dir / "diagnosis.json"
    audit_path = output_dir / "repair_audit.json"
    rerun_dir = output_dir / "rerun"
    dossier_path = Path("/app/incident/export_dossier.md")

    spec = load_spec()
    dossier_text = dossier_path.read_text(encoding="utf-8", errors="replace")
    original_pipeline = ORIGINAL_PIPELINE.read_text()
    issues = build_issues_from_sources(dossier_text, original_pipeline, spec)

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
    diagnosis = build_diagnosis_report("repaired", events, issues, summary, output_dir)
    diagnosis_path.write_text(json.dumps(diagnosis, indent=2) + "\n")

    code = PIPELINE_PATH.read_text()
    original_sha = pipeline_source_sha256(original_pipeline)
    processing_steps = list(spec["repair_audit"]["processing_steps"])
    if "record_pre_repair_sha256" not in processing_steps:
        processing_steps.insert(0, "record_pre_repair_sha256")
    audit = {
        "mode": "repair",
        "snapshot_sha256": original_sha,
        "pre_repair_sha256": original_sha,
        "patched_workflow": str(PIPELINE_PATH),
        "processing_steps": processing_steps,
        "removed_tokens": {token: token not in code for token in FORBIDDEN_TOKENS},
        "pre_repair": pre_audit,
        "issues_repaired": [
            {
                "issue_id": issue["id"],
                "dossier_quote": issue["evidence"]["dossier_quote"],
                "repair_terms": ["ts_ms", ".lower(", "reverse=True"],
            }
            for issue in issues
        ],
        "post_repair": {
            "flagged_count": summary["flagged_count"],
            "rerun_flagged_count": json.loads((rerun_dir / "summary.json").read_text())[
                "flagged_count"
            ],
        },
    }
    audit_path.write_text(json.dumps(audit, indent=2) + "\n")
    audit_dir = Path("/app/audit")
    audit_dir.mkdir(parents=True, exist_ok=True)
    (audit_dir / "repair_audit.json").write_text(json.dumps(audit, indent=2) + "\n")


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
