# Project Decisions

## D-001 — Preserve duplicate content

Keep all 3,150 source records by default. The repository contains no authoritative evidence that the 300 excess repeated rows are collection errors. Use grouped stratified splitting so identical full-row contents cannot cross evaluation boundaries.

## D-002 — Leakage is temporal

Do not infer leakage safety from correlation, churn rate, uniqueness, coefficients, or feature importance. `Status` and `Customer Value` remain pending verification and are excluded by `src/features.py`.

## D-003 — Stable identity and split

Create `row_id` at load from source-row order. Use it for pairwise-disjoint and coverage assertions. Never include it in model features. Split with `random_state=42`, target stratification and duplicate-content grouping.

## D-004 — Dictionary is authoritative for executable schema checks

Use `column_name`, `data_type`, `description`, and `role` as required fields. Missing/duplicate fields, invalid roles, invalid types, target errors and CSV mismatches fail loudly. No schema fallback is allowed.

## D-005 — Checksum mismatch remains open

The checked-in CSV hashes to `e5362c3e5787dadd4e21eb606509bc03`; the supplied reference checksum is `07311e7080c0fb5b0ce94f5977abc4d5`. They are documented as different artifacts until source provenance explains the mismatch.
