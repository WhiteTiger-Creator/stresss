export is broken again — `/app/workflow/export_report.py` is not producing flagged output that matches what ops expects from `/app/data/events.json`.

months of incident notes are in `/app/incident/export_dossier.md`. most of it is noise and some early triage threads contradict later findings — treat the dossier as the source of truth for *behavior*, not every bridge-shift blurb. **All output schemas, audit fields, and acceptance constraints are defined in `/app/docs/report_spec.json`** — match that spec exactly.

build `/app/log_audit.py` with `diagnose` and `repair` subcommands per spec. `diagnose` writes a JSON report from `--dossier` / `--report` paths. `repair` patches `/app/workflow/export_report.py` in place and writes outputs under `--output-dir` (default `/app/output`).

keep `/app/workflow/.export_report.original` read-only and untouched. diagnosis evidence must cite that frozen snapshot (literal substrings) and verbatim dossier excerpts — not paraphrases and not text from already-patched code. `issues_found` must include **every** allowed issue id from the spec on both diagnose and repair runs.

after repair, write under the output dir: `summary.json`, `service_matrix.json`, `flagged.jsonl`, `diagnosis.json`, and `repair_audit.json`. `repair_audit.json` must record `pre_repair` **before** patching, use the exact `processing_steps` list from the spec, and map each forbidden executable token string to booleans in `removed_tokens` and `pre_repair.pipeline_tokens_present` as described in the spec. the patched pipeline must remove those forbidden tokens from executable code and include the required repair markers listed in the spec.

compute all summary, matrix, and flagged values from input JSON — do not hard-code verifier numbers. patched pipeline must accept `--input` and `--output-dir` and work with alternate input files the verifier supplies.
