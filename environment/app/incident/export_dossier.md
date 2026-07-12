# Service Log Export Incident Dossier
Pelagia Margin Platform Ops — internal investigation (2025-11 through 2026-03).

## Executive Summary
Pelagia Margin service-log export has been unstable since late 2025. Early triage blamed dashboard cache lag and suggested CSV fallback — those notes are archived below and may contradict later findings. For acceptance behavior, cross-check analyst notes embedded in bridge-shift records against bundled events.json — early triage sections above are not authoritative.

## Investigation Navigation
The authoritative evidence is in quoted `Incident note` records. Search this archive for `ts_ms`, `ascending`, `WARN`, `duplicate event ids`, `suppressed rows`, and `level ==` rather than treating repeated bridge-shift telemetry or vendor-email archives as requirements.

## Initial Triage Notes (2025-10 — superseded)
Lead analyst recommended switching to CSV export and disabling flagged.jsonl paging until cache refresh SLO recovered. Replay against bundled `events.json` showed the pipeline miscounts even on cold cache. Do not implement CSV fallback for this incident.

## Preliminary Hypotheses (2025-10 — mostly wrong)
- Dashboard read replica lag causing stale flagged counts (disproved: direct pipeline export shows same wrong counts)
- Missing timestamp metadata in upstream feed (disproved on replay against bundled events.json)
- Warn-level rows intentionally excluded by design (disproved on replay against bundled events.json)

## Bridge Timeline Archive (2024-Q4 through 2026-Q1)


### Bridge shift 0001 — db lane
Shift lead noted routine telemetry drift on db during window 1. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0002 — worker lane
Shift lead noted routine telemetry drift on worker during window 2. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0003 — cache lane
Shift lead noted routine telemetry drift on cache during window 3. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0004 — auth lane
Shift lead noted routine telemetry drift on auth during window 4. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0005 — billing lane
Shift lead noted routine telemetry drift on billing during window 5. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0006 — search lane
Shift lead noted routine telemetry drift on search during window 6. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0007 — notify lane
Shift lead noted routine telemetry drift on notify during window 7. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0008 — api lane
Shift lead noted routine telemetry drift on api during window 8. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0009 — db lane
Shift lead noted routine telemetry drift on db during window 9. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0010 — worker lane
Shift lead noted routine telemetry drift on worker during window 10. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0011 — cache lane
Shift lead noted routine telemetry drift on cache during window 11. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0012 — auth lane
Shift lead noted routine telemetry drift on auth during window 12. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0013 — billing lane
Shift lead noted routine telemetry drift on billing during window 13. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0014 — search lane
Shift lead noted routine telemetry drift on search during window 14. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0015 — notify lane
Shift lead noted routine telemetry drift on notify during window 15. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0016 — api lane
Shift lead noted routine telemetry drift on api during window 16. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0017 — db lane
Shift lead noted routine telemetry drift on db during window 17. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0018 — worker lane
Shift lead noted routine telemetry drift on worker during window 18. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0019 — cache lane
Shift lead noted routine telemetry drift on cache during window 19. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0020 — auth lane
Shift lead noted routine telemetry drift on auth during window 20. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0021 — billing lane
Shift lead noted routine telemetry drift on billing during window 21. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0022 — search lane
Shift lead noted routine telemetry drift on search during window 22. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0023 — notify lane
Shift lead noted routine telemetry drift on notify during window 23. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0024 — api lane
Shift lead noted routine telemetry drift on api during window 24. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0025 — db lane
Shift lead noted routine telemetry drift on db during window 25. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0026 — worker lane
Shift lead noted routine telemetry drift on worker during window 26. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0027 — cache lane
Shift lead noted routine telemetry drift on cache during window 27. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0028 — auth lane
Shift lead noted routine telemetry drift on auth during window 28. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0029 — billing lane
Shift lead noted routine telemetry drift on billing during window 29. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0030 — search lane
Shift lead noted routine telemetry drift on search during window 30. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0031 — notify lane
Shift lead noted routine telemetry drift on notify during window 31. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0032 — api lane
Shift lead noted routine telemetry drift on api during window 32. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0033 — db lane
Shift lead noted routine telemetry drift on db during window 33. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0034 — worker lane
Shift lead noted routine telemetry drift on worker during window 34. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0035 — cache lane
Shift lead noted routine telemetry drift on cache during window 35. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0036 — auth lane
Shift lead noted routine telemetry drift on auth during window 36. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0037 — billing lane
Shift lead noted routine telemetry drift on billing during window 37. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0038 — search lane
Shift lead noted routine telemetry drift on search during window 38. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0039 — notify lane
Shift lead noted routine telemetry drift on notify during window 39. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0040 — api lane
Shift lead noted routine telemetry drift on api during window 40. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0041 — db lane
Shift lead noted routine telemetry drift on db during window 41. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0042 — worker lane
Shift lead noted routine telemetry drift on worker during window 42. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0043 — cache lane
Shift lead noted routine telemetry drift on cache during window 43. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0044 — auth lane
Shift lead noted routine telemetry drift on auth during window 44. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0045 — billing lane
Shift lead noted routine telemetry drift on billing during window 45. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0046 — search lane
Shift lead noted routine telemetry drift on search during window 46. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0047 — notify lane
Shift lead noted routine telemetry drift on notify during window 47. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0048 — api lane
Shift lead noted routine telemetry drift on api during window 48. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0049 — db lane
Shift lead noted routine telemetry drift on db during window 49. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0050 — worker lane
Shift lead noted routine telemetry drift on worker during window 50. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0051 — cache lane
Shift lead noted routine telemetry drift on cache during window 51. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0052 — auth lane
Shift lead noted routine telemetry drift on auth during window 52. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0053 — billing lane
Shift lead noted routine telemetry drift on billing during window 53. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0054 — search lane
Shift lead noted routine telemetry drift on search during window 54. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0055 — notify lane
Shift lead noted routine telemetry drift on notify during window 55. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0056 — api lane
Shift lead noted routine telemetry drift on api during window 56. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0057 — db lane
Shift lead noted routine telemetry drift on db during window 57. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0058 — worker lane
Shift lead noted routine telemetry drift on worker during window 58. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0059 — cache lane
Shift lead noted routine telemetry drift on cache during window 59. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0060 — auth lane
Shift lead noted routine telemetry drift on auth during window 60. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0061 — billing lane
Shift lead noted routine telemetry drift on billing during window 61. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0062 — search lane
Shift lead noted routine telemetry drift on search during window 62. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0063 — notify lane
Shift lead noted routine telemetry drift on notify during window 63. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0064 — api lane
Shift lead noted routine telemetry drift on api during window 64. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0065 — db lane
Shift lead noted routine telemetry drift on db during window 65. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0066 — worker lane
Shift lead noted routine telemetry drift on worker during window 66. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0067 — cache lane
Shift lead noted routine telemetry drift on cache during window 67. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0068 — auth lane
Shift lead noted routine telemetry drift on auth during window 68. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0069 — billing lane
Shift lead noted routine telemetry drift on billing during window 69. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0070 — search lane
Shift lead noted routine telemetry drift on search during window 70. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0071 — notify lane
Shift lead noted routine telemetry drift on notify during window 71. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0072 — api lane
Shift lead noted routine telemetry drift on api during window 72. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0073 — db lane
Shift lead noted routine telemetry drift on db during window 73. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

> **Incident note (2025-11-02 — #INC-8841)** Sam: flagged.jsonl only has 3 lines again. summary says flagged_count=3 but I count 6 warn+error in events.json.


### Bridge shift 0074 — worker lane
Shift lead noted routine telemetry drift on worker during window 74. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0075 — cache lane
Shift lead noted routine telemetry drift on cache during window 75. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0076 — auth lane
Shift lead noted routine telemetry drift on auth during window 76. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0077 — billing lane
Shift lead noted routine telemetry drift on billing during window 77. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0078 — search lane
Shift lead noted routine telemetry drift on search during window 78. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0079 — notify lane
Shift lead noted routine telemetry drift on notify during window 79. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0080 — api lane
Shift lead noted routine telemetry drift on api during window 80. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0081 — db lane
Shift lead noted routine telemetry drift on db during window 81. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0082 — worker lane
Shift lead noted routine telemetry drift on worker during window 82. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0083 — cache lane
Shift lead noted routine telemetry drift on cache during window 83. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0084 — auth lane
Shift lead noted routine telemetry drift on auth during window 84. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0085 — billing lane
Shift lead noted routine telemetry drift on billing during window 85. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0086 — search lane
Shift lead noted routine telemetry drift on search during window 86. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0087 — notify lane
Shift lead noted routine telemetry drift on notify during window 87. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0088 — api lane
Shift lead noted routine telemetry drift on api during window 88. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0089 — db lane
Shift lead noted routine telemetry drift on db during window 89. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0090 — worker lane
Shift lead noted routine telemetry drift on worker during window 90. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0091 — cache lane
Shift lead noted routine telemetry drift on cache during window 91. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0092 — auth lane
Shift lead noted routine telemetry drift on auth during window 92. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0093 — billing lane
Shift lead noted routine telemetry drift on billing during window 93. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0094 — search lane
Shift lead noted routine telemetry drift on search during window 94. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0095 — notify lane
Shift lead noted routine telemetry drift on notify during window 95. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0096 — api lane
Shift lead noted routine telemetry drift on api during window 96. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0097 — db lane
Shift lead noted routine telemetry drift on db during window 97. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0098 — worker lane
Shift lead noted routine telemetry drift on worker during window 98. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0099 — cache lane
Shift lead noted routine telemetry drift on cache during window 99. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0100 — auth lane
Shift lead noted routine telemetry drift on auth during window 100. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0101 — billing lane
Shift lead noted routine telemetry drift on billing during window 101. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0102 — search lane
Shift lead noted routine telemetry drift on search during window 102. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0103 — notify lane
Shift lead noted routine telemetry drift on notify during window 103. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0104 — api lane
Shift lead noted routine telemetry drift on api during window 104. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0105 — db lane
Shift lead noted routine telemetry drift on db during window 105. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0106 — worker lane
Shift lead noted routine telemetry drift on worker during window 106. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0107 — cache lane
Shift lead noted routine telemetry drift on cache during window 107. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0108 — auth lane
Shift lead noted routine telemetry drift on auth during window 108. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0109 — billing lane
Shift lead noted routine telemetry drift on billing during window 109. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0110 — search lane
Shift lead noted routine telemetry drift on search during window 110. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0111 — notify lane
Shift lead noted routine telemetry drift on notify during window 111. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0112 — api lane
Shift lead noted routine telemetry drift on api during window 112. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0113 — db lane
Shift lead noted routine telemetry drift on db during window 113. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.


> **Incident note (2025-11-02 — #INC-8841)** Devon: ts_ms values in flagged output are all 0. grep shows event['timestamp'] in export_report.py — our payload uses ts_ms.

### Bridge shift 0114 — worker lane
Shift lead noted routine telemetry drift on worker during window 114. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0115 — cache lane
Shift lead noted routine telemetry drift on cache during window 115. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0116 — auth lane
Shift lead noted routine telemetry drift on auth during window 116. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0117 — billing lane
Shift lead noted routine telemetry drift on billing during window 117. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0118 — search lane
Shift lead noted routine telemetry drift on search during window 118. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0119 — notify lane
Shift lead noted routine telemetry drift on notify during window 119. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0120 — api lane
Shift lead noted routine telemetry drift on api during window 120. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0121 — db lane
Shift lead noted routine telemetry drift on db during window 121. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0122 — worker lane
Shift lead noted routine telemetry drift on worker during window 122. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0123 — cache lane
Shift lead noted routine telemetry drift on cache during window 123. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0124 — auth lane
Shift lead noted routine telemetry drift on auth during window 124. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0125 — billing lane
Shift lead noted routine telemetry drift on billing during window 125. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0126 — search lane
Shift lead noted routine telemetry drift on search during window 126. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0127 — notify lane
Shift lead noted routine telemetry drift on notify during window 127. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0128 — api lane
Shift lead noted routine telemetry drift on api during window 128. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0129 — db lane
Shift lead noted routine telemetry drift on db during window 129. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0130 — worker lane
Shift lead noted routine telemetry drift on worker during window 130. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0131 — cache lane
Shift lead noted routine telemetry drift on cache during window 131. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0132 — auth lane
Shift lead noted routine telemetry drift on auth during window 132. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0133 — billing lane
Shift lead noted routine telemetry drift on billing during window 133. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0134 — search lane
Shift lead noted routine telemetry drift on search during window 134. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0135 — notify lane
Shift lead noted routine telemetry drift on notify during window 135. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0136 — api lane
Shift lead noted routine telemetry drift on api during window 136. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0137 — db lane
Shift lead noted routine telemetry drift on db during window 137. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0138 — worker lane
Shift lead noted routine telemetry drift on worker during window 138. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0139 — cache lane
Shift lead noted routine telemetry drift on cache during window 139. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0140 — auth lane
Shift lead noted routine telemetry drift on auth during window 140. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0141 — billing lane
Shift lead noted routine telemetry drift on billing during window 141. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0142 — search lane
Shift lead noted routine telemetry drift on search during window 142. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0143 — notify lane
Shift lead noted routine telemetry drift on notify during window 143. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0144 — api lane
Shift lead noted routine telemetry drift on api during window 144. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0145 — db lane
Shift lead noted routine telemetry drift on db during window 145. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0146 — worker lane
Shift lead noted routine telemetry drift on worker during window 146. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0147 — cache lane
Shift lead noted routine telemetry drift on cache during window 147. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0148 — auth lane
Shift lead noted routine telemetry drift on auth during window 148. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0149 — billing lane
Shift lead noted routine telemetry drift on billing during window 149. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0150 — search lane
Shift lead noted routine telemetry drift on search during window 150. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0151 — notify lane
Shift lead noted routine telemetry drift on notify during window 151. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0152 — api lane
Shift lead noted routine telemetry drift on api during window 152. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0153 — db lane
Shift lead noted routine telemetry drift on db during window 153. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0154 — worker lane

> **Incident note (2025-11-03 — #INC-8841)** Riley: Dashboard pager shows oldest error first. flagged.jsonl sorted ascending; runbook says descending.

Shift lead noted routine telemetry drift on worker during window 154. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0155 — cache lane
Shift lead noted routine telemetry drift on cache during window 155. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0156 — auth lane
Shift lead noted routine telemetry drift on auth during window 156. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0157 — billing lane
Shift lead noted routine telemetry drift on billing during window 157. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0158 — search lane
Shift lead noted routine telemetry drift on search during window 158. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0159 — notify lane
Shift lead noted routine telemetry drift on notify during window 159. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0160 — api lane
Shift lead noted routine telemetry drift on api during window 160. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0161 — db lane
Shift lead noted routine telemetry drift on db during window 161. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0162 — worker lane
Shift lead noted routine telemetry drift on worker during window 162. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0163 — cache lane
Shift lead noted routine telemetry drift on cache during window 163. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0164 — auth lane
Shift lead noted routine telemetry drift on auth during window 164. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0165 — billing lane
Shift lead noted routine telemetry drift on billing during window 165. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0166 — search lane
Shift lead noted routine telemetry drift on search during window 166. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0167 — notify lane
Shift lead noted routine telemetry drift on notify during window 167. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0168 — api lane
Shift lead noted routine telemetry drift on api during window 168. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0169 — db lane
Shift lead noted routine telemetry drift on db during window 169. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0170 — worker lane
Shift lead noted routine telemetry drift on worker during window 170. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0171 — cache lane
Shift lead noted routine telemetry drift on cache during window 171. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0172 — auth lane
Shift lead noted routine telemetry drift on auth during window 172. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0173 — billing lane
Shift lead noted routine telemetry drift on billing during window 173. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0174 — search lane
Shift lead noted routine telemetry drift on search during window 174. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0175 — notify lane
Shift lead noted routine telemetry drift on notify during window 175. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0176 — api lane
Shift lead noted routine telemetry drift on api during window 176. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0177 — db lane
Shift lead noted routine telemetry drift on db during window 177. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0178 — worker lane
Shift lead noted routine telemetry drift on worker during window 178. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0179 — cache lane
Shift lead noted routine telemetry drift on cache during window 179. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0180 — auth lane
Shift lead noted routine telemetry drift on auth during window 180. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0181 — billing lane
Shift lead noted routine telemetry drift on billing during window 181. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0182 — search lane
Shift lead noted routine telemetry drift on search during window 182. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0183 — notify lane
Shift lead noted routine telemetry drift on notify during window 183. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0184 — api lane
Shift lead noted routine telemetry drift on api during window 184. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0185 — db lane
Shift lead noted routine telemetry drift on db during window 185. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0186 — worker lane
Shift lead noted routine telemetry drift on worker during window 186. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0187 — cache lane
Shift lead noted routine telemetry drift on cache during window 187. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0188 — auth lane
Shift lead noted routine telemetry drift on auth during window 188. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0189 — billing lane
Shift lead noted routine telemetry drift on billing during window 189. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0190 — search lane
Shift lead noted routine telemetry drift on search during window 190. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0191 — notify lane
Shift lead noted routine telemetry drift on notify during window 191. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0192 — api lane
Shift lead noted routine telemetry drift on api during window 192. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0193 — db lane
Shift lead noted routine telemetry drift on db during window 193. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0194 — worker lane
Shift lead noted routine telemetry drift on worker during window 194. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.

> **Incident note (2025-11-04 — #INC-8841)** Sam: Rebuilt container, same behavior. Do not rewrite summary.json by hand — fix export_report.py.

Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0195 — cache lane
Shift lead noted routine telemetry drift on cache during window 195. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0196 — auth lane
Shift lead noted routine telemetry drift on auth during window 196. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0197 — billing lane
Shift lead noted routine telemetry drift on billing during window 197. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0198 — search lane
Shift lead noted routine telemetry drift on search during window 198. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0199 — notify lane
Shift lead noted routine telemetry drift on notify during window 199. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0200 — api lane
Shift lead noted routine telemetry drift on api during window 200. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0201 — db lane
Shift lead noted routine telemetry drift on db during window 201. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0202 — worker lane
Shift lead noted routine telemetry drift on worker during window 202. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0203 — cache lane
Shift lead noted routine telemetry drift on cache during window 203. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0204 — auth lane
Shift lead noted routine telemetry drift on auth during window 204. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0205 — billing lane
Shift lead noted routine telemetry drift on billing during window 205. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0206 — search lane
Shift lead noted routine telemetry drift on search during window 206. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0207 — notify lane
Shift lead noted routine telemetry drift on notify during window 207. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0208 — api lane
Shift lead noted routine telemetry drift on api during window 208. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0209 — db lane
Shift lead noted routine telemetry drift on db during window 209. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0210 — worker lane
Shift lead noted routine telemetry drift on worker during window 210. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0211 — cache lane
Shift lead noted routine telemetry drift on cache during window 211. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0212 — auth lane
Shift lead noted routine telemetry drift on auth during window 212. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0213 — billing lane
Shift lead noted routine telemetry drift on billing during window 213. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0214 — search lane
Shift lead noted routine telemetry drift on search during window 214. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0215 — notify lane
Shift lead noted routine telemetry drift on notify during window 215. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0216 — api lane
Shift lead noted routine telemetry drift on api during window 216. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0217 — db lane
Shift lead noted routine telemetry drift on db during window 217. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0218 — worker lane
Shift lead noted routine telemetry drift on worker during window 218. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0219 — cache lane
Shift lead noted routine telemetry drift on cache during window 219. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0220 — auth lane
Shift lead noted routine telemetry drift on auth during window 220. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0221 — billing lane
Shift lead noted routine telemetry drift on billing during window 221. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0222 — search lane
Shift lead noted routine telemetry drift on search during window 222. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0223 — notify lane
Shift lead noted routine telemetry drift on notify during window 223. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0224 — api lane
Shift lead noted routine telemetry drift on api during window 224. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0225 — db lane
Shift lead noted routine telemetry drift on db during window 225. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0226 — worker lane
Shift lead noted routine telemetry drift on worker during window 226. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0227 — cache lane
Shift lead noted routine telemetry drift on cache during window 227. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0228 — auth lane
Shift lead noted routine telemetry drift on auth during window 228. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0229 — billing lane
Shift lead noted routine telemetry drift on billing during window 229. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0230 — search lane
Shift lead noted routine telemetry drift on search during window 230. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0231 — notify lane
Shift lead noted routine telemetry drift on notify during window 231. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0232 — api lane
Shift lead noted routine telemetry drift on api during window 232. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0233 — db lane
Shift lead noted routine telemetry drift on db during window 233. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

> **Incident note (2025-12-01 — #INC-9012)** Devon: Maybe switch to CSV export — out of scope for this sprint.


### Bridge shift 0234 — worker lane
Shift lead noted routine telemetry drift on worker during window 234. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0235 — cache lane
Shift lead noted routine telemetry drift on cache during window 235. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0236 — auth lane
Shift lead noted routine telemetry drift on auth during window 236. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0237 — billing lane
Shift lead noted routine telemetry drift on billing during window 237. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0238 — search lane
Shift lead noted routine telemetry drift on search during window 238. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0239 — notify lane
Shift lead noted routine telemetry drift on notify during window 239. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0240 — api lane
Shift lead noted routine telemetry drift on api during window 240. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0241 — db lane
Shift lead noted routine telemetry drift on db during window 241. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0242 — worker lane
Shift lead noted routine telemetry drift on worker during window 242. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0243 — cache lane
Shift lead noted routine telemetry drift on cache during window 243. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0244 — auth lane
Shift lead noted routine telemetry drift on auth during window 244. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0245 — billing lane
Shift lead noted routine telemetry drift on billing during window 245. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0246 — search lane
Shift lead noted routine telemetry drift on search during window 246. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0247 — notify lane
Shift lead noted routine telemetry drift on notify during window 247. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0248 — api lane
Shift lead noted routine telemetry drift on api during window 248. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0249 — db lane
Shift lead noted routine telemetry drift on db during window 249. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0250 — worker lane
Shift lead noted routine telemetry drift on worker during window 250. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0251 — cache lane
Shift lead noted routine telemetry drift on cache during window 251. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0252 — auth lane
Shift lead noted routine telemetry drift on auth during window 252. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0253 — billing lane
Shift lead noted routine telemetry drift on billing during window 253. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0254 — search lane
Shift lead noted routine telemetry drift on search during window 254. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0255 — notify lane
Shift lead noted routine telemetry drift on notify during window 255. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0256 — api lane
Shift lead noted routine telemetry drift on api during window 256. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0257 — db lane
Shift lead noted routine telemetry drift on db during window 257. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0258 — worker lane
Shift lead noted routine telemetry drift on worker during window 258. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0259 — cache lane
Shift lead noted routine telemetry drift on cache during window 259. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0260 — auth lane
Shift lead noted routine telemetry drift on auth during window 260. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0261 — billing lane
Shift lead noted routine telemetry drift on billing during window 261. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0262 — search lane
Shift lead noted routine telemetry drift on search during window 262. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0263 — notify lane
Shift lead noted routine telemetry drift on notify during window 263. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0264 — api lane
Shift lead noted routine telemetry drift on api during window 264. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0265 — db lane
Shift lead noted routine telemetry drift on db during window 265. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0266 — worker lane
Shift lead noted routine telemetry drift on worker during window 266. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0267 — cache lane
Shift lead noted routine telemetry drift on cache during window 267. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0268 — auth lane
Shift lead noted routine telemetry drift on auth during window 268. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0269 — billing lane
Shift lead noted routine telemetry drift on billing during window 269. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0270 — search lane
Shift lead noted routine telemetry drift on search during window 270. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0271 — notify lane
Shift lead noted routine telemetry drift on notify during window 271. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0272 — api lane
Shift lead noted routine telemetry drift on api during window 272. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0273 — db lane
Shift lead noted routine telemetry drift on db during window 273. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0274 — worker lane
Shift lead noted routine telemetry drift on worker during window 274. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.


> **Incident note (2026-01-15 — #INC-9012)** Riley: Confirmed events.json schema unchanged: id, ts_ms, level, service, message.

### Bridge shift 0275 — cache lane
Shift lead noted routine telemetry drift on cache during window 275. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0276 — auth lane
Shift lead noted routine telemetry drift on auth during window 276. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0277 — billing lane
Shift lead noted routine telemetry drift on billing during window 277. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0278 — search lane
Shift lead noted routine telemetry drift on search during window 278. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0279 — notify lane
Shift lead noted routine telemetry drift on notify during window 279. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0280 — api lane
Shift lead noted routine telemetry drift on api during window 280. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0281 — db lane
Shift lead noted routine telemetry drift on db during window 281. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0282 — worker lane
Shift lead noted routine telemetry drift on worker during window 282. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0283 — cache lane
Shift lead noted routine telemetry drift on cache during window 283. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0284 — auth lane
Shift lead noted routine telemetry drift on auth during window 284. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.
### Bridge shift 0285 — billing lane
Shift lead noted routine telemetry drift on billing during window 285. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0286 — search lane
Shift lead noted routine telemetry drift on search during window 286. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0287 — notify lane
Shift lead noted routine telemetry drift on notify during window 287. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0288 — api lane
Shift lead noted routine telemetry drift on api during window 288. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0289 — db lane
Shift lead noted routine telemetry drift on db during window 289. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0290 — worker lane
Shift lead noted routine telemetry drift on worker during window 290. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0291 — cache lane
Shift lead noted routine telemetry drift on cache during window 291. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0292 — auth lane
Shift lead noted routine telemetry drift on auth during window 292. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0293 — billing lane
Shift lead noted routine telemetry drift on billing during window 293. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0294 — search lane
Shift lead noted routine telemetry drift on search during window 294. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0295 — notify lane
Shift lead noted routine telemetry drift on notify during window 295. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0296 — api lane
Shift lead noted routine telemetry drift on api during window 296. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0297 — db lane
Shift lead noted routine telemetry drift on db during window 297. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0298 — worker lane
Shift lead noted routine telemetry drift on worker during window 298. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0299 — cache lane
Shift lead noted routine telemetry drift on cache during window 299. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0300 — auth lane
Shift lead noted routine telemetry drift on auth during window 300. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0301 — billing lane
Shift lead noted routine telemetry drift on billing during window 301. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0302 — search lane
Shift lead noted routine telemetry drift on search during window 302. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0303 — notify lane
Shift lead noted routine telemetry drift on notify during window 303. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0304 — api lane
Shift lead noted routine telemetry drift on api during window 304. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0305 — db lane
Shift lead noted routine telemetry drift on db during window 305. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0306 — worker lane
Shift lead noted routine telemetry drift on worker during window 306. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0307 — cache lane

> **Incident note (2026-02-20 — #INC-9200)** Sam: warn rows still missing after partial patch that only fixed timestamp field.

Shift lead noted routine telemetry drift on cache during window 307. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0308 — auth lane
Shift lead noted routine telemetry drift on auth during window 308. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0309 — billing lane
Shift lead noted routine telemetry drift on billing during window 309. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0310 — search lane
Shift lead noted routine telemetry drift on search during window 310. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0311 — notify lane
Shift lead noted routine telemetry drift on notify during window 311. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0312 — api lane
Shift lead noted routine telemetry drift on api during window 312. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0313 — db lane
Shift lead noted routine telemetry drift on db during window 313. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0314 — worker lane
Shift lead noted routine telemetry drift on worker during window 314. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0315 — cache lane
Shift lead noted routine telemetry drift on cache during window 315. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0316 — auth lane
Shift lead noted routine telemetry drift on auth during window 316. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0317 — billing lane
Shift lead noted routine telemetry drift on billing during window 317. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0318 — search lane
Shift lead noted routine telemetry drift on search during window 318. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0319 — notify lane
Shift lead noted routine telemetry drift on notify during window 319. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0320 — api lane
Shift lead noted routine telemetry drift on api during window 320. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0321 — db lane
Shift lead noted routine telemetry drift on db during window 321. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0322 — worker lane
Shift lead noted routine telemetry drift on worker during window 322. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0323 — cache lane
Shift lead noted routine telemetry drift on cache during window 323. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0324 — auth lane
Shift lead noted routine telemetry drift on auth during window 324. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0325 — billing lane
Shift lead noted routine telemetry drift on billing during window 325. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0326 — search lane
Shift lead noted routine telemetry drift on search during window 326. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0327 — notify lane
Shift lead noted routine telemetry drift on notify during window 327. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0328 — api lane
Shift lead noted routine telemetry drift on api during window 328. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0329 — db lane
Shift lead noted routine telemetry drift on db during window 329. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0330 — worker lane
Shift lead noted routine telemetry drift on worker during window 330. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0331 — cache lane
Shift lead noted routine telemetry drift on cache during window 331. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0332 — auth lane
Shift lead noted routine telemetry drift on auth during window 332. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0333 — billing lane
Shift lead noted routine telemetry drift on billing during window 333. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0334 — search lane
Shift lead noted routine telemetry drift on search during window 334. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0335 — notify lane
Shift lead noted routine telemetry drift on notify during window 335. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0336 — api lane
Shift lead noted routine telemetry drift on api during window 336. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0337 — db lane
Shift lead noted routine telemetry drift on db during window 337. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0338 — worker lane
Shift lead noted routine telemetry drift on worker during window 338. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0339 — cache lane
Shift lead noted routine telemetry drift on cache during window 339. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.

> **Incident note (2026-02-21 — #INC-9200)** Devon: Partial patch kept level == 'error' filter — need warn and error in flagged export.

Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0340 — auth lane
Shift lead noted routine telemetry drift on auth during window 340. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0341 — billing lane
Shift lead noted routine telemetry drift on billing during window 341. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0342 — search lane
Shift lead noted routine telemetry drift on search during window 342. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0343 — notify lane
Shift lead noted routine telemetry drift on notify during window 343. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0344 — api lane
Shift lead noted routine telemetry drift on api during window 344. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0345 — db lane
Shift lead noted routine telemetry drift on db during window 345. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0346 — worker lane
Shift lead noted routine telemetry drift on worker during window 346. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0347 — cache lane
Shift lead noted routine telemetry drift on cache during window 347. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0348 — auth lane
Shift lead noted routine telemetry drift on auth during window 348. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0349 — billing lane
Shift lead noted routine telemetry drift on billing during window 349. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0350 — search lane
Shift lead noted routine telemetry drift on search during window 350. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0351 — notify lane
Shift lead noted routine telemetry drift on notify during window 351. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0352 — api lane
Shift lead noted routine telemetry drift on api during window 352. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0353 — db lane
Shift lead noted routine telemetry drift on db during window 353. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0354 — worker lane
Shift lead noted routine telemetry drift on worker during window 354. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0355 — cache lane
Shift lead noted routine telemetry drift on cache during window 355. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0356 — auth lane
Shift lead noted routine telemetry drift on auth during window 356. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0357 — billing lane
Shift lead noted routine telemetry drift on billing during window 357. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0358 — search lane
Shift lead noted routine telemetry drift on search during window 358. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0359 — notify lane
Shift lead noted routine telemetry drift on notify during window 359. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0360 — api lane
Shift lead noted routine telemetry drift on api during window 360. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0361 — db lane
Shift lead noted routine telemetry drift on db during window 361. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0362 — worker lane
Shift lead noted routine telemetry drift on worker during window 362. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0363 — cache lane
Shift lead noted routine telemetry drift on cache during window 363. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0364 — auth lane
Shift lead noted routine telemetry drift on auth during window 364. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0365 — billing lane
Shift lead noted routine telemetry drift on billing during window 365. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0366 — search lane
Shift lead noted routine telemetry drift on search during window 366. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0367 — notify lane
Shift lead noted routine telemetry drift on notify during window 367. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0368 — api lane
Shift lead noted routine telemetry drift on api during window 368. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0369 — db lane
Shift lead noted routine telemetry drift on db during window 369. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0370 — worker lane
Shift lead noted routine telemetry drift on worker during window 370. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0371 — cache lane
Shift lead noted routine telemetry drift on cache during window 371. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

> **Incident note (2026-03-01 — #INC-9200)** Riley: Sort fix reverted during merge conflict — ascending sort landed again.


### Bridge shift 0372 — auth lane
Shift lead noted routine telemetry drift on auth during window 372. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0373 — billing lane
Shift lead noted routine telemetry drift on billing during window 373. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0374 — search lane
Shift lead noted routine telemetry drift on search during window 374. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0375 — notify lane
Shift lead noted routine telemetry drift on notify during window 375. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0376 — api lane
Shift lead noted routine telemetry drift on api during window 376. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0377 — db lane
Shift lead noted routine telemetry drift on db during window 377. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0378 — worker lane
Shift lead noted routine telemetry drift on worker during window 378. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0379 — cache lane
Shift lead noted routine telemetry drift on cache during window 379. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0380 — auth lane
Shift lead noted routine telemetry drift on auth during window 380. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0381 — billing lane
Shift lead noted routine telemetry drift on billing during window 381. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0382 — search lane
Shift lead noted routine telemetry drift on search during window 382. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0383 — notify lane
Shift lead noted routine telemetry drift on notify during window 383. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0384 — api lane
Shift lead noted routine telemetry drift on api during window 384. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0385 — db lane
Shift lead noted routine telemetry drift on db during window 385. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0386 — worker lane
Shift lead noted routine telemetry drift on worker during window 386. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0387 — cache lane
Shift lead noted routine telemetry drift on cache during window 387. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.


> **Incident note (2026-02-22 — #INC-9200)** Riley: Uppercase WARN rows from the legacy bridge feed are not counted — spec says normalize to lowercase before severity tallies.

### Bridge shift 0388 — auth lane
Shift lead noted routine telemetry drift on auth during window 388. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0389 — billing lane
Shift lead noted routine telemetry drift on billing during window 389. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0390 — search lane
Shift lead noted routine telemetry drift on search during window 390. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0391 — notify lane
Shift lead noted routine telemetry drift on notify during window 391. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0392 — api lane
Shift lead noted routine telemetry drift on api during window 392. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0393 — db lane
Shift lead noted routine telemetry drift on db during window 393. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0394 — worker lane
Shift lead noted routine telemetry drift on worker during window 394. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0395 — cache lane
Shift lead noted routine telemetry drift on cache during window 395. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0396 — auth lane
Shift lead noted routine telemetry drift on auth during window 396. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0397 — billing lane
Shift lead noted routine telemetry drift on billing during window 397. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0398 — search lane
Shift lead noted routine telemetry drift on search during window 398. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0399 — notify lane
Shift lead noted routine telemetry drift on notify during window 399. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

### Bridge shift 0400 — api lane

> **Incident note (2026-02-23 — #INC-9200)** Sam: Replay batch had duplicate event ids with different ts_ms values; we should keep the newest ts_ms per id before summaries.

Shift lead noted routine telemetry drift on api during window 400. Pager noise stayed within SLO; export dashboard lag was attributed to stale cache refresh, not the service-log pipeline. Follow-up ticket closed as monitoring-only.
Historical CSV migration threads from 2023 are archived and non-authoritative for current JSON export acceptance. Analysts should cross-check against bundled events.json and report_spec.json rather than chat excerpts.

## Vendor Comms Log (redacted)

**Email thread VND-8001:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8201:** No action on duplicate id handling — out of vendor scope for margin platform.


> **Incident note (2026-02-24 — #INC-9200)** Devon: Suppressed paging errors still land in flagged.jsonl — runbook says suppressed rows must be excluded from flagged export.

**Email thread VND-8002:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8202:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8003:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8203:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8004:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8204:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8005:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8205:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8006:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8206:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8007:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8207:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8008:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8208:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8009:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8209:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8010:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8210:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8011:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8211:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8012:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8212:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8013:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8213:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8014:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8214:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8015:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8215:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8016:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8216:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8017:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8217:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8018:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8218:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8019:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8219:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8020:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8220:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8021:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8221:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8022:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8222:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8023:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8223:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8024:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8224:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8025:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8225:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8026:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8226:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8027:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8227:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8028:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8228:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8029:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8229:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8030:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8230:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8031:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8231:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8032:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8232:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8033:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8233:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8034:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8234:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8035:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8235:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8036:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8236:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8037:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8237:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8038:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8238:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8039:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8239:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8040:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8240:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8041:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8241:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8042:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8242:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8043:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8243:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8044:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8244:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8045:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8245:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8046:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8246:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8047:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8247:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8048:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8248:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8049:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8249:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8050:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8250:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8051:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8251:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8052:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8252:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8053:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8253:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8054:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8254:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8055:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8255:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8056:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8256:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8057:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8257:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8058:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8258:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8059:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8259:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8060:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8260:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8061:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8261:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8062:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8262:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8063:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8263:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8064:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8264:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8065:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8265:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8066:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8266:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8067:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8267:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8068:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8268:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8069:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8269:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8070:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8270:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8071:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8271:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8072:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8272:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8073:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8273:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8074:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8274:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8075:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8275:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8076:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8276:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8077:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8277:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8078:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8278:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8079:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8279:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8080:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8280:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8081:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8281:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8082:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8282:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8083:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8283:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8084:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8284:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8085:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8285:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8086:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8286:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8087:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8287:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8088:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8288:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8089:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8289:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8090:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8290:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8091:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8291:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8092:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8292:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8093:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8293:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8094:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8294:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8095:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8295:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8096:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8296:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8097:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8297:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8098:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8298:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8099:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8299:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8100:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8300:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8101:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8301:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8102:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8302:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8103:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8303:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8104:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8304:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8105:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8305:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8106:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8306:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8107:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8307:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8108:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8308:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8109:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8309:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8110:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8310:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8111:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8311:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8112:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8312:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8113:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8313:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8114:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8314:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8115:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8315:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8116:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8316:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8117:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8317:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8118:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8318:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8119:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8319:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8120:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8320:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8121:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8321:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8122:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8322:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8123:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8323:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8124:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8324:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8125:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8325:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8126:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8326:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8127:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8327:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8128:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8328:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8129:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8329:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8130:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8330:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8131:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8331:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8132:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8332:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8133:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8333:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8134:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8334:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8135:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8335:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8136:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8336:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8137:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8337:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8138:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8338:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8139:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8339:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8140:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8340:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8141:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8341:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8142:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8342:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8143:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8343:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8144:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8344:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8145:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8345:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8146:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8346:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8147:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8347:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8148:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8348:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8149:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8349:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8150:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8350:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8151:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8351:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8152:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8352:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8153:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8353:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8154:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8354:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8155:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8355:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8156:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8356:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8157:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8357:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8158:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8358:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8159:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8359:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8160:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8360:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8161:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8361:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8162:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8362:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8163:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8363:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8164:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8364:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8165:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8365:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8166:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8366:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8167:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8367:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8168:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8368:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8169:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8369:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8170:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8370:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8171:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8371:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8172:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8372:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8173:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8373:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8174:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8374:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8175:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8375:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8176:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8376:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8177:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8377:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8178:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8378:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8179:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8379:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8180:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8380:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8181:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8381:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8182:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8382:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8183:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8383:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8184:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8384:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8185:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8385:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8186:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8386:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8187:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8387:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8188:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8388:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8189:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8389:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8190:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8390:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8191:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8391:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8192:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8392:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8193:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8393:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8194:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8394:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8195:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8395:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8196:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8396:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8197:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8397:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8198:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8398:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8199:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8399:** No action on duplicate id handling — out of vendor scope for margin platform.

**Email thread VND-8200:** Vendor acknowledged intermittent WARN alias casing in upstream feeds; platform team requested lowercase normalization in downstream exporters.
**Email thread VND-8400:** No action on duplicate id handling — out of vendor scope for margin platform.

## Runbook Excerpts (historical)

Section 4.2 — Flagged export ordering: dashboard paging expects newest events first.
Section 4.3 — Severity inclusion: review queue includes warn and error class events.
Section 4.7 — Suppressed events: excluded from flagged.jsonl while still contributing to summary totals where applicable.
Section 5.1 — Timestamp field: canonical source field is ts_ms epoch milliseconds.

## Closing Notes
Treat chat noise as non-authoritative. The bundled `/app/data/events.json`, `/app/workflow/export_report.py`, and `/app/docs/report_spec.json` govern acceptance.

## Quarterly Review Minutes (noise)

Q2 2025 review item 1: export latency within budget; no pipeline change requested.
Q3 2025 review item 2: export latency within budget; no pipeline change requested.
Q4 2025 review item 3: export latency within budget; no pipeline change requested.
Q1 2026 review item 4: export latency within budget; no pipeline change requested.
Q2 2026 review item 5: export latency within budget; no pipeline change requested.
Q3 2026 review item 6: export latency within budget; no pipeline change requested.
Q4 2026 review item 7: export latency within budget; no pipeline change requested.
Q1 2027 review item 8: export latency within budget; no pipeline change requested.
Q2 2027 review item 9: export latency within budget; no pipeline change requested.
Q3 2027 review item 10: export latency within budget; no pipeline change requested.
Q4 2027 review item 11: export latency within budget; no pipeline change requested.
Q1 2028 review item 12: export latency within budget; no pipeline change requested.
Q2 2028 review item 13: export latency within budget; no pipeline change requested.
Q3 2028 review item 14: export latency within budget; no pipeline change requested.
Q4 2028 review item 15: export latency within budget; no pipeline change requested.
Q1 2029 review item 16: export latency within budget; no pipeline change requested.
Q2 2029 review item 17: export latency within budget; no pipeline change requested.
Q3 2029 review item 18: export latency within budget; no pipeline change requested.
Q4 2029 review item 19: export latency within budget; no pipeline change requested.
Q1 2020 review item 20: export latency within budget; no pipeline change requested.
Q2 2020 review item 21: export latency within budget; no pipeline change requested.
Q3 2020 review item 22: export latency within budget; no pipeline change requested.
Q4 2020 review item 23: export latency within budget; no pipeline change requested.
Q1 2021 review item 24: export latency within budget; no pipeline change requested.
Q2 2021 review item 25: export latency within budget; no pipeline change requested.
Q3 2021 review item 26: export latency within budget; no pipeline change requested.
Q4 2021 review item 27: export latency within budget; no pipeline change requested.
Q1 2022 review item 28: export latency within budget; no pipeline change requested.
Q2 2022 review item 29: export latency within budget; no pipeline change requested.
Q3 2022 review item 30: export latency within budget; no pipeline change requested.
Q4 2022 review item 31: export latency within budget; no pipeline change requested.
Q1 2023 review item 32: export latency within budget; no pipeline change requested.
Q2 2023 review item 33: export latency within budget; no pipeline change requested.
Q3 2023 review item 34: export latency within budget; no pipeline change requested.
Q4 2023 review item 35: export latency within budget; no pipeline change requested.
Q1 2024 review item 36: export latency within budget; no pipeline change requested.
Q2 2024 review item 37: export latency within budget; no pipeline change requested.
Q3 2024 review item 38: export latency within budget; no pipeline change requested.
Q4 2024 review item 39: export latency within budget; no pipeline change requested.
Q1 2025 review item 40: export latency within budget; no pipeline change requested.
Q2 2025 review item 41: export latency within budget; no pipeline change requested.
Q3 2025 review item 42: export latency within budget; no pipeline change requested.
Q4 2025 review item 43: export latency within budget; no pipeline change requested.
Q1 2026 review item 44: export latency within budget; no pipeline change requested.
Q2 2026 review item 45: export latency within budget; no pipeline change requested.
Q3 2026 review item 46: export latency within budget; no pipeline change requested.
Q4 2026 review item 47: export latency within budget; no pipeline change requested.
Q1 2027 review item 48: export latency within budget; no pipeline change requested.
Q2 2027 review item 49: export latency within budget; no pipeline change requested.
Q3 2027 review item 50: export latency within budget; no pipeline change requested.
Q4 2027 review item 51: export latency within budget; no pipeline change requested.
Q1 2028 review item 52: export latency within budget; no pipeline change requested.
Q2 2028 review item 53: export latency within budget; no pipeline change requested.
Q3 2028 review item 54: export latency within budget; no pipeline change requested.
Q4 2028 review item 55: export latency within budget; no pipeline change requested.
Q1 2029 review item 56: export latency within budget; no pipeline change requested.
Q2 2029 review item 57: export latency within budget; no pipeline change requested.
Q3 2029 review item 58: export latency within budget; no pipeline change requested.
Q4 2029 review item 59: export latency within budget; no pipeline change requested.
Q1 2020 review item 60: export latency within budget; no pipeline change requested.

