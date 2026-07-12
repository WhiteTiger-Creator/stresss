# Service-log export recovery

Restore `/app/workflow/export_report.py` and build `/app/log_audit.py`. The normative contract is `/app/docs/report_spec.json`; inspect it before implementing.

## Fixed operational sources
- Events default to `/app/data/events.json`; workflow `--input PATH` replaces only this event source.
- Silence windows always come from `/app/data/silence_windows.json`.
- Dependency rules always come from `/app/data/service_dependencies.json`.
- Resolve those policy paths exactly as absolute defaults, never relative to the event input or output directory.
- Evidence comes from `/app/incident/export_dossier.md` and frozen `/app/workflow/.export_report.original`. Never alter the frozen file.

## CLI and diagnosis
- Implement `diagnose --dossier PATH --report PATH` and `repair --output-dir PATH`.
- Report exactly `wrong_timestamp_field`, `severity_filter`, `sort_order`, `level_normalization`, `dedupe_policy`, and `suppressed_filter`.
- Each issue contains `id`, `severity`, `description`, `resolution`, and nested `evidence` with `dossier_quote`, `pipeline_evidence`, and `repair_action`.
- Evidence minimum lengths are 30, 10, and 10. Dossier quotes are verbatim; pipeline excerpts are case-sensitive frozen-source substrings. Required evidence terms and ordering words such as `ascending`/`descending` must match the spec.
- Before finishing, check every evidence field against `quick_contract_index.evidence_term_checklist` in the spec. In particular, the level-normalization repair action must contain `lower`, and dedupe pipeline evidence must contain the exact frozen-source substring `for event in events`.
- Diagnose output has status `diagnosed` and only `pipeline_status`, `issues_found`, and `input_stats`. Repair output has status `repaired`, a complete key-for-key `verified_summary`, and `output_paths` keyed exactly by `summary_json`, `flagged_jsonl`, and `service_matrix_json`.
- `input_stats.services` contains sorted canonical service names after the same trim/lowercase and alias mapping used by the export; never report raw spellings there.

## Canonical export
- Normalize level by trim/lowercase; normalize service by trim/lowercase plus `api-gw→api`, `api gateway→api`, `database→db`, and `worker-batch→worker`.
- Integer-coerce `ts_ms` with invalid values becoming zero, collapse message whitespace, and normalize suppressed values (`true/1/yes` versus `false/0/no/empty`).
- Deduplicate by event id using: greatest `ts_ms`, severity `error>warn>info>debug`, non-suppressed first, lexicographically greater normalized message, then greater normalized service.
- Canonical deduplicated rows use ascending `ts_ms` order. Flagged candidates are unsuppressed, unsilenced `warn`/`error` rows.

## Silence and dependency state
- Normalize, validate, and compact silence windows per `(service, level_scope)`; the only valid scopes are `all`, `warn`, and `error`. Drop `debug`, `info`, and every other scope before compaction and checksum generation. Merge overlap and touching intervals, match half-open windows, and calculate `(all_overlap_ms//25)+(level_overlap_ms//15)` over `[ts_ms-90, ts_ms+1)`.
- Canonicalize dependency rules, reject invalid ranges/weights, and deduplicate identical service/range rules by maximum weight.
- Finalize candidates chronologically by `(ts_ms asc, id asc)`. A source contributes `weight*severity_rank + silence_pressure_score + source.dependency_pressure_score//2`; retain its best matching rule, then the strongest three sources by contribution desc, source time desc, and source id asc.
- Build lineage depth-first in retained-source order, keep five unique ids, cap chain depth at six, and calculate causal burst from finalized earlier sources.
- Compute blast radius over directed one- and two-hop service paths, bound cycles by that hop limit, and retain the strongest path capacity per destination.

## Ordering, digests, and files
- Final flagged order is `ts_ms` desc, severity desc, causal burst desc, blast radius desc, dependency pressure desc, chain depth desc, silence pressure desc, then id asc.
- Canonical fingerprint is SHA-1 over LF-joined ascending canonical rows `id|ts_ms|level|service|message|suppressed_int`. Silence and dependency checksums are SHA-256 over their ordered compacted/canonical rule rows.
- `lineage_digest` is the first 12 SHA-256 hex characters of `id|depth|burst|comma_joined_lineage`; `blast_radius_digest` is the first 10 SHA-1 characters of `service|comma_joined_services|score`.
- `event_digest` is the first 10 SHA-1 characters of the ordered row identity, silence/dependency fields, lineage fields and digest, then blast-radius fields and digest exactly as listed in the spec. Hash UTF-8 with literal `|`, comma, and LF delimiters and no trailing delimiter; use the published worked vectors.
- Emit compact `flagged.jsonl` plus `summary.json`, `service_matrix.json`, `diagnosis.json`, and `repair_audit.json` under the requested output directory.
- `service_matrix.json` is the service map itself: top-level canonical service names map directly to level-count objects. Do not wrap it in `schema_version` or `services`.
- In `repair_audit.json`, `patched_workflow` is the plain string `/app/workflow/export_report.py`. `pre_repair` uses exactly `pipeline_source_sha256` and `pipeline_tokens_present`; `post_repair` uses `flagged_count` and `rerun_flagged_count`. Copy `processing_steps` from the spec verbatim and in order. Token maps use the exact forbidden-source literals.
- Repair must reinstall the workflow even after reset, run it twice for idempotency, and record integer `flagged_count` and `rerun_flagged_count`. Leave `/app/output/diagnosis.json` in repaired mode.
- A repair targeting a custom directory writes all five artifacts only beneath that directory. It must not create, rewrite, or otherwise update `/app/output/diagnosis.json` or any other default-output artifact.
- Finish by running `python3 /app/log_audit.py repair --output-dir /app/output`; validation in a temporary directory does not satisfy the final handoff.
