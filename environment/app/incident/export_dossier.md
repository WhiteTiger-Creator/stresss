# Service Log Export Incident Dossier
Pelagia Margin Platform Ops — internal investigation (2025-11 through 2026-03).

## Executive Summary
The `/app/workflow/export_report.py` job produces incomplete flagged exports. On-call reports missing warn-level rows, zero timestamps on flagged events, and oldest-first ordering that breaks paging in the dashboard.

## Ground Truth Hints (verify against code and data)

### Issue: wrong_timestamp_field
- Analyst consensus (partial): Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
- Red herrings encountered:
  - Maybe events need millisecond strings not integers — checked schema, ts_ms is numeric.
  - Could be timezone conversion — not applicable to epoch ms field.
  - Perhaps id field collision — unrelated.

### Issue: severity_filter
- Analyst consensus (partial): Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
- Red herrings encountered:
  - Filter info rows too — spec excludes info/debug deliberately.
  - Merge warn into info — rejected by SRE lead.
  - Drop debug only — insufficient; warn still missing.

### Issue: sort_order
- Analyst consensus (partial): Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
- Red herrings encountered:
  - Sort by id instead — breaks paging contract.
  - Stable sort by service name — wrong primary key.
  - Reverse entire events.json input — corrupts summary counts.

### Issue: level_normalization
- Analyst consensus (partial): Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
- Red herrings encountered:
  - Add a separate severity enum table — rejected for this exporter.
  - Uppercase is valid in UI only — exporter contract requires lowercase.

### Issue: dedupe_policy
- Analyst consensus (partial): Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
- Red herrings encountered:
  - Keep first seen row — wrong for out-of-order batch replays.
  - Dedupe by message text — unstable.

### Issue: suppressed_filter
- Analyst consensus (partial): Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.
- Red herrings encountered:
  - Drop suppressed from summary totals — spec keeps them in level counts only.
  - Move suppressed rows to debug file — out of scope.

## Analyst Chat Log (excerpted)

### 2025-11-02 — #INC-8841
Sam: flagged.jsonl only has 3 lines again. summary says flagged_count=3 but I count 6 warn+error in events.json.

### 2025-11-02 — #INC-8841
Devon: ts_ms values in flagged output are all 0. grep shows event['timestamp'] in export_report.py — our payload uses ts_ms.

### 2025-11-03 — #INC-8841
Riley: Dashboard pager shows oldest error first. flagged.jsonl sorted ascending; runbook says descending.

### 2025-11-04 — #INC-8841
Sam: Rebuilt container, same behavior. Do not rewrite summary.json by hand — fix export_report.py.

### 2025-12-01 — #INC-9012
Devon: Maybe switch to CSV export — out of scope for this sprint.

### 2026-01-15 — #INC-9012
Riley: Confirmed events.json schema unchanged: id, ts_ms, level, service, message.

### 2026-02-20 — #INC-9200
Sam: warn rows still missing after partial patch that only fixed timestamp field.

### 2026-02-21 — #INC-9200
Devon: Partial patch kept level == 'error' filter — need warn and error in flagged export.

### 2026-03-01 — #INC-9200
Riley: Sort fix reverted during merge conflict — ascending sort landed again.
## Analyst Thread Archive (noise — verify in code)

### 2025-11-02 — #RUN-9001
Sam: rerun 1 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 1 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-03 — #RUN-9002
Sam: rerun 2 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 2 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-04 — #RUN-9003
Sam: rerun 3 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 3 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-05 — #RUN-9004
Sam: rerun 4 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 4 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-06 — #RUN-9005
Sam: rerun 5 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 5 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-07 — #RUN-9006
Sam: rerun 6 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 6 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-08 — #RUN-9007
Sam: rerun 7 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 7 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-09 — #RUN-9008
Sam: rerun 8 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 8 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-10 — #RUN-9009
Sam: rerun 9 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 9 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-11 — #RUN-9010
Sam: rerun 10 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 10 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-12 — #RUN-9011
Sam: rerun 11 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 11 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-13 — #RUN-9012
Sam: rerun 12 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 12 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-14 — #RUN-9013
Sam: rerun 13 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 13 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-15 — #RUN-9014
Sam: rerun 14 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 14 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-16 — #RUN-9015
Sam: rerun 15 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 15 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-17 — #RUN-9016
Sam: rerun 16 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 16 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-18 — #RUN-9017
Sam: rerun 17 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 17 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-19 — #RUN-9018
Sam: rerun 18 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 18 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-20 — #RUN-9019
Sam: rerun 19 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 19 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-21 — #RUN-9020
Sam: rerun 20 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 20 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-22 — #RUN-9021
Sam: rerun 21 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 21 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-23 — #RUN-9022
Sam: rerun 22 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 22 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-24 — #RUN-9023
Sam: rerun 23 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 23 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-25 — #RUN-9024
Sam: rerun 24 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 24 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-26 — #RUN-9025
Sam: rerun 25 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 25 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-27 — #RUN-9026
Sam: rerun 26 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 26 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-28 — #RUN-9027
Sam: rerun 27 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 27 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-01 — #RUN-9028
Sam: rerun 28 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 28 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-02 — #RUN-9029
Sam: rerun 29 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 29 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-03 — #RUN-9030
Sam: rerun 30 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 30 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-04 — #RUN-9031
Sam: rerun 31 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 31 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-05 — #RUN-9032
Sam: rerun 32 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 32 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-06 — #RUN-9033
Sam: rerun 33 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 33 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-07 — #RUN-9034
Sam: rerun 34 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 34 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-08 — #RUN-9035
Sam: rerun 35 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 35 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-09 — #RUN-9036
Sam: rerun 36 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 36 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-10 — #RUN-9037
Sam: rerun 37 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 37 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-11 — #RUN-9038
Sam: rerun 38 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 38 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-12 — #RUN-9039
Sam: rerun 39 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 39 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-13 — #RUN-9040
Sam: rerun 40 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 40 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-14 — #RUN-9041
Sam: rerun 41 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 41 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-15 — #RUN-9042
Sam: rerun 42 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 42 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-16 — #RUN-9043
Sam: rerun 43 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 43 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-17 — #RUN-9044
Sam: rerun 44 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 44 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-18 — #RUN-9045
Sam: rerun 45 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 45 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-19 — #RUN-9046
Sam: rerun 46 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 46 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-20 — #RUN-9047
Sam: rerun 47 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 47 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-21 — #RUN-9048
Sam: rerun 48 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 48 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-22 — #RUN-9049
Sam: rerun 49 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 49 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-23 — #RUN-9050
Sam: rerun 50 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 50 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-24 — #RUN-9051
Sam: rerun 51 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 51 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-25 — #RUN-9052
Sam: rerun 52 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 52 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-26 — #RUN-9053
Sam: rerun 53 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 53 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-27 — #RUN-9054
Sam: rerun 54 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 54 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-28 — #RUN-9055
Sam: rerun 55 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 55 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-01 — #RUN-9056
Sam: rerun 56 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 56 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-02 — #RUN-9057
Sam: rerun 57 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 57 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-03 — #RUN-9058
Sam: rerun 58 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 58 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-04 — #RUN-9059
Sam: rerun 59 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 59 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-05 — #RUN-9060
Sam: rerun 60 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 60 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-06 — #RUN-9061
Sam: rerun 61 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 61 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-07 — #RUN-9062
Sam: rerun 62 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 62 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-08 — #RUN-9063
Sam: rerun 63 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 63 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-09 — #RUN-9064
Sam: rerun 64 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 64 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-10 — #RUN-9065
Sam: rerun 65 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 65 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-11 — #RUN-9066
Sam: rerun 66 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 66 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-12 — #RUN-9067
Sam: rerun 67 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 67 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-13 — #RUN-9068
Sam: rerun 68 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 68 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-14 — #RUN-9069
Sam: rerun 69 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 69 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-15 — #RUN-9070
Sam: rerun 70 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 70 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-16 — #RUN-9071
Sam: rerun 71 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 71 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-17 — #RUN-9072
Sam: rerun 72 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 72 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-18 — #RUN-9073
Sam: rerun 73 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 73 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-19 — #RUN-9074
Sam: rerun 74 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 74 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-20 — #RUN-9075
Sam: rerun 75 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 75 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-21 — #RUN-9076
Sam: rerun 76 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 76 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-22 — #RUN-9077
Sam: rerun 77 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 77 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-23 — #RUN-9078
Sam: rerun 78 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 78 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-24 — #RUN-9079
Sam: rerun 79 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 79 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-25 — #RUN-9080
Sam: rerun 80 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 80 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-26 — #RUN-9081
Sam: rerun 81 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 81 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-27 — #RUN-9082
Sam: rerun 82 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 82 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-28 — #RUN-9083
Sam: rerun 83 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 83 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-01 — #RUN-9084
Sam: rerun 84 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 84 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-02 — #RUN-9085
Sam: rerun 85 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 85 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-03 — #RUN-9086
Sam: rerun 86 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 86 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-04 — #RUN-9087
Sam: rerun 87 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 87 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-05 — #RUN-9088
Sam: rerun 88 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 88 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-06 — #RUN-9089
Sam: rerun 89 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 89 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-07 — #RUN-9090
Sam: rerun 90 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 90 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-08 — #RUN-9091
Sam: rerun 91 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 91 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-09 — #RUN-9092
Sam: rerun 92 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 92 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-10 — #RUN-9093
Sam: rerun 93 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 93 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-11 — #RUN-9094
Sam: rerun 94 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 94 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-12 — #RUN-9095
Sam: rerun 95 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 95 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-13 — #RUN-9096
Sam: rerun 96 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 96 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-14 — #RUN-9097
Sam: rerun 97 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 97 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-15 — #RUN-9098
Sam: rerun 98 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 98 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-16 — #RUN-9099
Sam: rerun 99 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 99 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-17 — #RUN-9100
Sam: rerun 100 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 100 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-18 — #RUN-9101
Sam: rerun 101 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 101 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-19 — #RUN-9102
Sam: rerun 102 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 102 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-20 — #RUN-9103
Sam: rerun 103 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 103 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-21 — #RUN-9104
Sam: rerun 104 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 104 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-22 — #RUN-9105
Sam: rerun 105 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 105 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-23 — #RUN-9106
Sam: rerun 106 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 106 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-24 — #RUN-9107
Sam: rerun 107 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 107 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-25 — #RUN-9108
Sam: rerun 108 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 108 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-26 — #RUN-9109
Sam: rerun 109 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 109 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-27 — #RUN-9110
Sam: rerun 110 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 110 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-28 — #RUN-9111
Sam: rerun 111 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 111 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-01 — #RUN-9112
Sam: rerun 112 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 112 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-02 — #RUN-9113
Sam: rerun 113 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 113 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-03 — #RUN-9114
Sam: rerun 114 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 114 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-04 — #RUN-9115
Sam: rerun 115 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 115 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-05 — #RUN-9116
Sam: rerun 116 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 116 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-06 — #RUN-9117
Sam: rerun 117 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 117 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-07 — #RUN-9118
Sam: rerun 118 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 118 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-08 — #RUN-9119
Sam: rerun 119 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 119 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

### 2025-11-09 — #RUN-9120
Sam: rerun 120 still shows wrong flagged_count in dashboard export.
Devon: stale CSV migration note 120 is not authoritative.
> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.
> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.
> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.
> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.
> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.
> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

## Repeated Possible Leads (noise — verify in code)

> **Possible lead:** Broken export_report.py reads event['timestamp'] instead of event['ts_ms'], zeroing flagged timestamps whenever the legacy timestamp field is absent from JSON payloads.

> **Possible lead:** Flagged export keeps only level == 'error' rows but operations expects both warn and error severities in flagged.jsonl for paging review.

> **Possible lead:** Flagged rows are sorted by ts_ms ascending; runbook requires ts_ms descending so newest incidents appear first in flagged.jsonl.

> **Possible lead:** Source payloads include WARN and Error aliases; export_report.py must normalize level values to lowercase before counting or flagging rows.

> **Possible lead:** Duplicate event ids must collapse to the row with the highest ts_ms before export summaries run.

> **Possible lead:** Events with suppressed set true must be excluded from flagged.jsonl even when severity is error.

## Closing Notes
Treat chat noise as non-authoritative. The bundled `/app/data/events.json`, `/app/workflow/export_report.py`, and `/app/docs/report_spec.json` govern acceptance.
