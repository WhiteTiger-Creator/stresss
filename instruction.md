export is broken again — `/app/workflow/export_report.py` is not producing flagged output that matches what ops expects from `/app/data/events.json`.

months of incident notes are in `/app/incident/export_dossier.md` (long-context archive, at least 500 lines). most of it is noise and some early triage threads contradict later findings — treat the dossier as the source of truth for *behavior*, not every bridge-shift blurb. **All output schemas, audit fields, and acceptance constraints are defined in `/app/docs/report_spec.json`** — match that spec exactly.

build `/app/log_audit.py` with `diagnose` and `repair` subcommands per spec. `diagnose` reads `/app/data/events.json` for `input_stats` (no separate `--input` flag on diagnose), writes a JSON report from `--dossier` / `--report`, and must **not** include `verified_summary` or `output_paths`. `repair` patches `/app/workflow/export_report.py` in place and writes outputs under `--output-dir` (default `/app/output`).

keep `/app/workflow/.export_report.original` read-only and untouched. diagnosis evidence must cite that frozen snapshot (literal substrings) and verbatim dossier excerpts — not paraphrases and not text from already-patched code. `issues_found` must include **every** allowed issue id from the spec on both diagnose and repair runs. for each issue, evidence fields must satisfy the substring terms in `required_terms_by_issue` inside `/app/docs/report_spec.json`.

minimum evidence cues by issue (see spec for the exact contract):
- `wrong_timestamp_field`: mention `ts_ms`; include pipeline token `event["timestamp"]`
- `severity_filter`: mention `warn`; include pipeline token `level == "error"`
- `sort_order`: mention both `ascending` and `descending` recency/sort behavior
- `level_normalization`: mention both `WARN` and `lowercase` normalization
- `dedupe_policy`: mention duplicate-id collapse with newest `ts_ms`
- `suppressed_filter`: mention suppressed rows excluded from flagged export

after repair, write under the output dir: `summary.json`, `service_matrix.json`, `flagged.jsonl`, `diagnosis.json`, and `repair_audit.json`. `flagged.jsonl` must use compact JSON (`json.dumps(..., separators=(",", ":"))`, no space after `:`). `repair_audit.json` must record `pre_repair` **before** patching, use the exact `processing_steps` list from the spec, and map each forbidden executable token string to booleans in `removed_tokens` and `pre_repair.pipeline_tokens_present`. the patched pipeline must remove forbidden tokens from executable code and include required repair markers from the spec. rerunning the patched pipeline with the same input must be idempotent and produce byte-identical logical outputs.

canonicalization per spec: normalize level and service via `str(...).strip().lower()`, apply service aliases (`api-gw`/`api gateway` -> `api`, `database` -> `db`, `worker-batch` -> `worker`), normalize `ts_ms` with `int(str(...).strip())` (invalid -> `0`), normalize message by collapsing internal whitespace, normalize suppressed strings (`true/1/yes`, `false/0/no`), dedupe by event id keeping **highest ts_ms** (tie-break by severity rank `error>warn>info>debug`, then prefer non-suppressed rows, then lexicographically greater normalized message, then normalized service), and count `total_events` from canonical deduped rows (suppressed rows still counted in totals). flagged export includes warn+error, excludes suppressed, and sorts by `ts_ms` descending, then severity rank descending, then `id` ascending. compute all summary, matrix, and flagged values from input JSON — do not hard-code verifier numbers. patched pipeline must accept `--input` and `--output-dir` and work with alternate input files the verifier supplies.
