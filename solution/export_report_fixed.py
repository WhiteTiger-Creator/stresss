#!/usr/bin/env python3
"""Export service-log summary and flagged events."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SCHEMA_VERSION = "service-log-report-v2"
FLAGGED_LEVELS = {"warn", "error"}
LEVEL_ORDER = ("debug", "error", "info", "warn")
SEVERITY_RANK = {"debug": 1, "info": 2, "warn": 3, "error": 4}
SERVICE_ALIASES = {
    "api-gw": "api",
    "api gateway": "api",
    "database": "db",
    "worker-batch": "worker",
}


def load_events(path: Path) -> list[dict]:
    return json.loads(path.read_text())


def normalize_level(value: object) -> str:
    return str(value).strip().lower()


def normalize_service(value: object) -> str:
    normalized = str(value).strip().lower()
    return SERVICE_ALIASES.get(normalized, normalized)


def normalize_ts_ms(value: object) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return 0


def normalize_message(value: object) -> str:
    return " ".join(str(value).split())


def normalize_suppressed(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes"}:
            return True
        if lowered in {"false", "0", "no", ""}:
            return False
    return bool(value)


def canonicalize_events(events: list[dict]) -> list[dict]:
    deduped: dict[str, dict] = {}
    for event in events:
        normalized = dict(event)
        normalized["level"] = normalize_level(normalized.get("level", ""))
        normalized["service"] = normalize_service(normalized.get("service", ""))
        normalized["ts_ms"] = normalize_ts_ms(normalized.get("ts_ms", 0))
        normalized["message"] = normalize_message(normalized.get("message", ""))
        normalized["suppressed"] = normalize_suppressed(normalized.get("suppressed", False))
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
                normalized_suppressed = normalize_suppressed(normalized.get("suppressed", False))
                current_suppressed = normalize_suppressed(current.get("suppressed", False))
                if current_suppressed and not normalized_suppressed:
                    should_replace = True
                elif current_suppressed == normalized_suppressed:
                    next_message = normalize_message(normalized.get("message", ""))
                    current_message = normalize_message(current.get("message", ""))
                    if next_message > current_message:
                        should_replace = True
                    elif next_message == current_message:
                        next_service = normalize_service(normalized.get("service", ""))
                        current_service = normalize_service(current.get("service", ""))
                        should_replace = next_service > current_service
        if should_replace:
            deduped[event_id] = normalized
    return sorted(deduped.values(), key=lambda row: row["ts_ms"])


def is_flagged(event: dict) -> bool:
    if normalize_suppressed(event.get("suppressed", False)):
        return False
    return event["level"] in FLAGGED_LEVELS


def build_service_matrix(events: list[dict]) -> dict[str, dict[str, int]]:
    matrix: dict[str, dict[str, int]] = {}
    for event in events:
        service = normalize_service(event.get("service", ""))
        level = normalize_level(event.get("level", ""))
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
    flagged.sort(
        key=lambda row: (
            row["ts_ms"],
            SEVERITY_RANK.get(row["level"], 0),
            row["id"],
        ),
        reverse=True,
    )
    flagged.sort(key=lambda row: row["id"])
    flagged.sort(key=lambda row: SEVERITY_RANK.get(row["level"], 0), reverse=True)
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
            if normalize_suppressed(event.get("suppressed", False))
            and event["level"] in FLAGGED_LEVELS
        ),
        "canonical_fingerprint": hashlib.sha1(
            "\n".join(
                f"{event['id']}|{event['ts_ms']}|{event['level']}|{event['service']}|"
                f"{event['message']}|{1 if normalize_suppressed(event.get('suppressed', False)) else 0}"
                for event in canonical
            ).encode("utf-8")
        ).hexdigest(),
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
