The service-log export in `/app/workflow/export_report.py` is broken again — missing warn rows, duplicate ids, uppercase severities treated as non-matching, suppressed noise in flagged output, zero timestamps, and the wrong sort order. Input events are in `/app/data/events.json`; months of analyst notes live in `/app/incident/export_dossier.md` (mostly noise — verify against code and data). Acceptance rules are in `/app/docs/report_spec.json`.

Environment contract: keep the frozen broken snapshot at `/app/workflow/.export_report.original` intact and use it as the authoritative pre-repair baseline for diagnosis/audit behavior. Long-context dossier contract: `/app/incident/export_dossier.md` is expected to remain a large incident archive (at least 500 lines) with the final directive section preserved.

Build `/app/log_audit.py` as a CLI with `diagnose` and `repair` subcommands:

- `diagnose` — run as `python3 /app/log_audit.py diagnose --dossier PATH --report PATH`. Read the dossier, inspect the pipeline and data, and write JSON with `pipeline_status` `"diagnosed"`. **Always include every allowed root-cause issue id** in `issues_found`, even when run after repair. Allowed ids: `wrong_timestamp_field`, `severity_filter`, `sort_order`, `level_normalization`, `dedupe_policy`, `suppressed_filter`. Base evidence on the dossier and the **original** broken workflow — not only a live grep of an already-patched file. Include `input_stats` (`event_count`, `unique_event_ids`, sorted `services`). Do **not** include repaired-only keys (`verified_summary`, `output_paths`).
- `repair` — run as `python3 /app/log_audit.py repair --output-dir PATH`. Capture `pre_repair` **before** patching. Patch `/app/workflow/export_report.py` in place, run the corrected pipeline, and write all outputs under the provided `--output-dir` (default `/app/output`):
  - `summary.json`, `service_matrix.json`, and `flagged.jsonl` from the corrected pipeline
  - `diagnosis.json` with `pipeline_status` `"repaired"`, all issue ids retained, plus `verified_summary` and `output_paths`
  - `repair_audit.json` with `pre_repair.pipeline_source_sha256`, `removed_tokens`, `processing_steps`, and `post_repair` counts

Fix all six root-cause bugs:

1. **wrong_timestamp_field** — use `ts_ms`, not `timestamp`
2. **severity_filter** — include both `warn` and `error` in flagged output
3. **sort_order** — sort flagged rows by `ts_ms` **descending** (`reverse=True`)
4. **level_normalization** — normalize `level` with `.lower()` before counting or flagging (handles `WARN` / `Error` aliases)
5. **dedupe_policy** — collapse duplicate `id` values keeping the row with the **highest** `ts_ms` before summaries run
6. **suppressed_filter** — exclude rows where `suppressed` is `true` from `flagged.jsonl` (they may still count in summary level totals)

Every `issues_found` item must include `id`, `severity`, `description`, `resolution`, and `evidence` with `dossier_quote`, `pipeline_evidence`, and `repair_action`. `dossier_quote` must be a **verbatim excerpt** from `/app/incident/export_dossier.md` (matching after whitespace normalization). Evidence must include these terms literally:

- `wrong_timestamp_field`: dossier `timestamp` + `ts_ms`; pipeline `event["timestamp"]`; repair `ts_ms`
- `severity_filter`: dossier `warn` + `error`; pipeline `level == "error"`; repair `warn`
- `sort_order`: dossier `ascending` + `descending`; pipeline `sort` + `ts_ms`; repair `reverse=True`
- `level_normalization`: dossier `WARN` + `lowercase`; pipeline `WARN`; repair `.lower(`
- `dedupe_policy`: dossier `duplicate` + `ts_ms`; pipeline `for event in events`; repair `dedupe`
- `suppressed_filter`: dossier `suppressed` + `excluded`; pipeline `suppressed`; repair `suppressed`

After repair, `output_paths` must point to the actual files under the effective output directory (`--output-dir`, default `/app/output`): `<output-dir>/summary.json`, `<output-dir>/flagged.jsonl`, and `<output-dir>/service_matrix.json`. `summary.json` must include `schema_version`, `raw_event_count`, `unique_event_ids`, `total_events`, alphabetical `level_counts`, `services`, `flagged_count`, and `suppressed_excluded_count`. `service_matrix.json` must map each service to alphabetical per-level counts. `flagged.jsonl` must use compact JSON (no spaces after `:`). `repair_audit.json` must include `post_repair.rerun_flagged_count`.

Remove forbidden bug tokens from executable pipeline code after repair (`event["timestamp"]`, `level == "error"`). Comments may mention removed bugs. Compute every summary, matrix, and flagged value from input JSON — do not hard-code verifier numbers.

The patched `/app/workflow/export_report.py` must honor `--input` and `--output-dir` (defaults: `/app/data/events.json`, `/app/output`) and work with alternate input files supplied by tests.

Report shape, audit schema, and output formats are defined in `/app/docs/report_spec.json`. Match that spec exactly.
