# Iranian Churn Dataset

## Dataset in this repository

- File: `data/raw/Customer Churn.csv`
- Rows: 3,150
- Raw columns: 14 (13 candidate features and target `Churn`)
- Missing values: 0
- Duplicate content: 300 excess rows across 165 groups; retained by default
- Technical identity: `row_id` is added by `load_raw_data()` from stable source-row order and is not written into the raw file

The repository does not contain a ZIP/source artifact, download script, or transformation script that explains the origin of the checked-in CSV. Source URL, license/citation, and the precise feature definitions remain pending authoritative verification.

## Prediction point

The course specification describes using information from the first nine months to predict churn in the following three months. The CSV has no timestamps. Feature availability must therefore be justified from metadata, not inferred from correlation.

`Status` and `Customer Value` do not have sufficient definition/lineage evidence in this repository. They remain pending verification and are excluded from the default model feature list.

## Checksum and provenance

Two different checksums are recorded and must not be conflated:

| Artifact | Algorithm | Checksum | State |
|---|---|---|---|
| Exact checked-in file `data/raw/Customer Churn.csv` | MD5 | `e5362c3e5787dadd4e21eb606509bc03` | Recomputed locally |
| Supplied source/reference CSV artifact | MD5 | `07311e7080c0fb5b0ce94f5977abc4d5` | Does not match repository file |

Provenance verification is pending. Do not claim that these hashes describe the same artifact.

## Reproducible workflow

```powershell
python scripts/validate_week2.py
python -m unittest discover -s tests -v
python scripts/eda_train.py
```

The split keeps every source record, groups identical content into one partition, stratifies by `Churn`, uses `random_state=42`, and targets approximately 60/20/20. Validation and test are not used for EDA or preprocessing decisions.
