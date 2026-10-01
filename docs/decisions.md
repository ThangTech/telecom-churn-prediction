# Project Decisions

## D-001 — Preserve duplicate content

Keep all 3,150 source records by default. The repository contains no authoritative evidence that the 300 excess repeated rows are collection errors. Use grouped stratified splitting so identical full-row contents cannot cross evaluation boundaries.

## D-002 — Leakage is temporal

Do not infer leakage safety from correlation, churn rate, uniqueness, coefficients, or feature importance. UCI metadata states all non-target attributes are aggregated over the first nine months, before the month-12 churn label. `Status` and `Customer Value` are therefore eligible for the Week 3 feature set; the exact Customer Value formula remains a documentation caveat, not evidence of future-data leakage.

## D-003 — Stable identity and split

Create `row_id` at load from source-row order. Use it for pairwise-disjoint and coverage assertions. Never include it in model features. Split with `random_state=42`, target stratification and duplicate-content grouping.

## D-004 — Dictionary is authoritative for executable schema checks

Use `column_name`, `data_type`, `description`, and `role` as required fields. Missing/duplicate fields, invalid roles, invalid types, target errors and CSV mismatches fail loudly. No schema fallback is allowed.

## D-005 — Checksum difference is line-ending-only; source provenance remains open

The CRLF checkout hashes to MD5 `e5362c3e5787dadd4e21eb606509bc03` and SHA256 `90d5fb6bd1630cd4de4b4d28fcf8b4cb92a8f6ab7484605b0799d47386f7dbe1`. Normalizing only line endings to LF produces MD5 `07311e7080c0fb5b0ce94f5977abc4d5`, exactly matching the supplied reference. Parsed rows and `row_id`/split membership are unchanged, so line endings are not a reason to regenerate the split. Source is UCI dataset 563; repository download date is not recorded.

## D-006 — Week 3 feature eligibility aligned to UCI temporal metadata

UCI defines `Status` as active/non-active, explicitly lists `Customer Value` among the non-target attributes, and states that every non-target attribute is aggregated from the first nine months before the month-12 churn label. Both are therefore KEEP and the evaluated 13-feature set is FINAL. The exact Customer Value formula is not published; this is retained as a documentation limitation, not treated as evidence of leakage. Week 3 reran all six configurations across five train-only folds after the feature change. The already-reported test was not rerun.
