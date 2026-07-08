export is broken again — `/app/workflow/export_report.py` is not producing flagged output that matches what ops expects from `/app/data/events.json`.

months of incident notes are in `/app/incident/export_dossier.md`. most of it is noise and some early triage threads contradict later findings — treat the dossier as the source of truth for *behavior*, not every bridge-shift blurb. output shape and audit schemas are in `/app/docs/report_spec.json`.

build `/app/log_audit.py` with `diagnose` and `repair` subcommands per spec. `diagnose` writes a JSON report from `--dossier` / `--report` paths. `repair` patches `/app/workflow/export_report.py` in place and writes outputs under `--output-dir` (default `/app/output`).

keep `/app/workflow/.export_report.original` read-only and untouched. diagnosis evidence must cite that frozen snapshot (literal substrings) and verbatim dossier excerpts — not paraphrases and not text from already-patched code.

after repair: `summary.json`, `service_matrix.json`, `flagged.jsonl`, `diagnosis.json`, and `repair_audit.json` under the output dir. compute all counts from input JSON; do not hard-code verifier numbers. patched pipeline must accept `--input` and `--output-dir` and work with alternate input files the verifier supplies.
