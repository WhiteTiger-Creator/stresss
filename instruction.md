Restore the failed service-log incident export at `/app/workflow/export_report.py`. Build `/app/log_audit.py` with `diagnose --dossier PATH --report PATH` and `repair --output-dir PATH`, using `/app/incident/export_dossier.md` and the frozen `/app/workflow/.export_report.original` to substantiate the six diagnosed defects.

Repair must be self-contained and safe after the active workflow is reset: capture evidence from the frozen original, reinstall the corrected workflow, execute it for the requested directory, and verify a second idempotent run. Leave the frozen original untouched. The final `/app/output/diagnosis.json` must be the repair-mode report, not a later diagnose-only overwrite.

Produce `summary.json`, `service_matrix.json`, compact `flagged.jsonl`, `diagnosis.json`, and `repair_audit.json`. Repair-mode `output_paths` uses exactly `summary_json`, `flagged_jsonl`, and `service_matrix_json`; `verified_summary` must equal the generated summary.

The repaired export must generalize to alternate inputs while handling canonicalization, silence policy, stateful dependency propagation, recursive lineage/burst state, and bounded cycle-safe downstream blast radius. `/app/docs/report_spec.json` is the operational acceptance contract for schemas, source paths, graph semantics, deterministic ordering, and digest formats.
