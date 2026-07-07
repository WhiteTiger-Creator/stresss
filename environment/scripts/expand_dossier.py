#!/usr/bin/env python3
"""Expand export_dossier.md with long-context noise for benchmark authoring."""

from __future__ import annotations

from pathlib import Path

DOSSIER = Path("/app/incident/export_dossier.md")
if not DOSSIER.exists():
    DOSSIER = Path(__file__).resolve().parents[1] / "app" / "incident" / "export_dossier.md"

LEADS = [
    (
        "Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], "
        "zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads."
    ),
    (
        "Flagged export keeps only level == 'error' rows but operations expects both warn and error "
        "severities in flagged.jsonl for paging review."
    ),
    (
        "Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest "
        "incidents appear first in flagged.jsonl."
    ),
    (
        "Source payloads include WARN and Error aliases; export_report.py must normalize level values "
        "to lowercase before counting or flagging rows."
    ),
    "Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.",
    (
        "Events with suppressed set true must be excluded from flagged.jsonl even when severity is error."
    ),
]


def main() -> None:
    head = DOSSIER.read_text(encoding="utf-8")
    prefix = head.split("## Analyst Thread Archive", 1)[0]
    if "## Analyst Thread Archive" not in head:
        prefix = head.split("## Repeated Possible Leads", 1)[0]

    noise_lines = ["## Analyst Thread Archive (noise — verify in code)", ""]
    for i in range(1, 121):
        noise_lines.append(f"### 2025-11-{(i % 28) + 1:02d} — #RUN-{9000 + i}")
        noise_lines.append(f"Sam: rerun {i} still shows wrong flagged_count in dashboard export.")
        noise_lines.append(f"Devon: stale CSV migration note {i} is not authoritative.")
        for lead in LEADS:
            noise_lines.append(f"> **Possible lead:** {lead}")
        noise_lines.append("")

    tail_lines = ["## Repeated Possible Leads (noise — verify in code)", ""]
    for lead in LEADS:
        tail_lines.append(f"> **Possible lead:** {lead}")
        tail_lines.append("")

    tail_lines.extend(
        [
            "## Closing Notes",
            "Treat chat noise as non-authoritative. The bundled `/app/data/events.json`, "
            "`/app/workflow/export_report.py`, and `/app/docs/report_spec.json` govern acceptance.",
            "",
        ]
    )

    DOSSIER.write_text("\n".join([prefix.rstrip(), *noise_lines, *tail_lines]), encoding="utf-8")
    print(f"Expanded dossier to {len(DOSSIER.read_text().splitlines())} lines")


if __name__ == "__main__":
    main()
