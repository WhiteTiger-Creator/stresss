#!/usr/bin/env python3
"""Export service-log summary and flagged events."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SCHEMA_VERSION = "service-log-report-v2"
FLAGGED_LEVELS = {"warn", "error"}
LEVEL_ORDER = ("debug", "error", "info", "warn")


def load_events(path: Path) -> list[dict]:
    return json.loads(path.read_text())


def canonicalize_events(events: list[dict]) -> list[dict]:
    deduped: dict[str, dict] = {}
    for event in events:
        normalized = dict(event)
        normalized["level"] = str(normalized.get("level", "")).lower()
        event_id = str(normalized["id"])
        current = deduped.get(event_id)
        if current is None or normalized["ts_ms"] > current["ts_ms"]:
            deduped[event_id] = normalized
    return sorted(deduped.values(), key=lambda row: row["ts_ms"])


def is_flagged(event: dict) -> bool:
    if event.get("suppressed") is True:
        return False
    return event["level"] in FLAGGED_LEVELS


def build_service_matrix(events: list[dict]) -> dict[str, dict[str, int]]:
    matrix: dict[str, dict[str, int]] = {}
    for event in events:
        service = str(event.get("service", ""))
        level = str(event.get("level", ""))
        matrix.setdefault(service, {name: 0 for name in LEVEL_ORDER})
        if level in matrix[service]:
            matrix[service][level] += 1
    return {service: matrix[service] for service in sorted(matrix)}


def export_report(events: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    canonical = canonicalize_events(events)

    level_counts = {level: 0 for level in LEVEL_ORDER}
    services: set[str] = set()
    for event in canonical:
        level = str(event.get("level", ""))
        if level in level_counts:
            level_counts[level] += 1
        services.add(str(event.get("service", "")))

    flagged = []
    for event in canonical:
        if not is_flagged(event):
            continue
        flagged.append(
            {
                "id": event["id"],
                "ts_ms": event["ts_ms"],
                "level": event["level"],
                "service": event["service"],
                "message": event["message"],
            }
        )
    flagged.sort(key=lambda row: row["ts_ms"], reverse=True)

    summary = {
        "schema_version": SCHEMA_VERSION,
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

    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (output_dir / "service_matrix.json").write_text(
        json.dumps(build_service_matrix(canonical), indent=2) + "\n"
    )
    with (output_dir / "flagged.jsonl").open("w", encoding="utf-8") as handle:
        for row in flagged:
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="/app/data/events.json")
    parser.add_argument("--output-dir", default="/app/output")
    args = parser.parse_args()

    events = load_events(Path(args.input))
    export_report(events, Path(args.output_dir))
    print(f"Wrote report to {args.output_dir}")


if __name__ == "__main__":
    main()
