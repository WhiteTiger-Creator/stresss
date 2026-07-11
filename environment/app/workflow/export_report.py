#!/usr/bin/env python3
"""Export service-log summary and flagged events."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

SCHEMA_VERSION = "service-log-report-v2"


def load_events(path: Path) -> list[dict]:
    return json.loads(path.read_text())


def export_report(events: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    level_counts = {level: 0 for level in ("debug", "error", "info", "warn")}
    services: set[str] = set()
    for event in events:
        level = str(event.get("level", ""))
        if level in level_counts:
            level_counts[level] += 1
        services.add(str(event.get("service", "")))

    flagged = []
    for event in events:
        level = event.get("level")
        if level == "error":
            flagged.append(
                {
                    "id": event["id"],
                    "ts_ms": event["timestamp"] if "timestamp" in event else 0,
                    "level": event["level"],
                    "service": event["service"],
                    "message": event["message"],
                }
            )

    flagged.sort(key=lambda row: row["ts_ms"])

    summary = {
        "schema_version": SCHEMA_VERSION,
        "raw_event_count": len(events),
        "unique_event_ids": len({str(event["id"]) for event in events}),
        "total_events": len(events),
        "level_counts": level_counts,
        "services": sorted(services),
        "flagged_count": len(flagged),
        "suppressed_excluded_count": 0,
    }

    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (output_dir / "service_matrix.json").write_text(json.dumps({}, indent=2) + "\n")
    with (output_dir / "flagged.jsonl").open("w", encoding="utf-8") as handle:
        for row in flagged:
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=os.environ.get("EVENTS_PATH", "/app/data/events.json"))
    parser.add_argument("--output-dir", default=os.environ.get("OUTPUT_DIR", "/app/output"))
    args = parser.parse_args()

    events = load_events(Path(args.input))
    export_report(events, Path(args.output_dir))
    print(f"Wrote report to {args.output_dir}")


if __name__ == "__main__":
    main()
