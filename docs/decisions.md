# Project Decisions

## D-001 — Preserve duplicate content

Keep all 3,150 source records by default. The repository contains no authoritative evidence that the 300 excess repeated rows are collection errors. Use grouped stratified splitting so identical full-row contents cannot cross evaluation boundaries.

## D-002 — Leakage is temporal

Do not infer leakage safety from correlation, churn rate, uniqueness, coefficients, or feature importance. `Status` and `Customer Value` remain pending verification and are excluded by `src/features.py`.

## D-003 — Stable identity and split

Create `row_id` at load from source-row order. Use it for pairwise-disjoint and coverage assertions. Never include it in model features. Split with `random_state=42`, target stratification and duplicate-content grouping.

## D-004 — Dictionary is authoritative for executable schema checks

Use `column_name`, `data_type`, `description`, and `role` as required fields. Missing/duplicate fields, invalid roles, invalid types, target errors and CSV mismatches fail loudly. No schema fallback is allowed.

## D-005 — Checksum difference is line-ending-only; source provenance remains open

The CRLF checkout hashes to MD5 `e5362c3e5787dadd4e21eb606509bc03` and SHA256 `90d5fb6bd1630cd4de4b4d28fcf8b4cb92a8f6ab7484605b0799d47386f7dbe1`. Normalizing only line endings to LF produces MD5 `07311e7080c0fb5b0ce94f5977abc4d5`, exactly matching the supplied reference. Parsed rows and `row_id`/split membership are unchanged, so line endings are not a reason to regenerate the split. Original download URL, license and citation remain pending.
