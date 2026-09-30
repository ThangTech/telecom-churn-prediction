# Iranian Churn Dataset

## Dataset in this repository

- File: `data/raw/Customer Churn.csv`
- Rows: 3,150
- Raw columns: 14 (13 candidate features and target `Churn`)
- Missing values: 0
- Duplicate content: 300 excess rows across 165 groups; retained by default
- Technical identity: `row_id` is added by `load_raw_data()` from stable source-row order and is not written into the raw file

Official source: UCI Machine Learning Repository, Iranian Churn dataset (ID 563): https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset. DOI: https://doi.org/10.24432/C5JW3Z. UCI reports 3,150 instances, 13 features and no missing values. Repository download date is not recorded.

Citation: *Iranian Churn [Dataset]. (2020). UCI Machine Learning Repository. https://doi.org/10.24432/C5JW3Z.* UCI currently lists the dataset under CC BY 4.0; usage must retain appropriate attribution.

## Prediction point

UCI states that every attribute except `Churn` is aggregated from the first nine months; churn is the customer state at the end of month 12, with a three-month planning gap. `Status` is defined as 1=active and 2=non-active. `Customer Value` is defined as the calculated value of the customer. This establishes temporal availability for both features, although UCI does not publish the exact Customer Value formula on the dataset page.

## Checksum and provenance

The checkout uses CRLF line endings. Normalizing only those line endings to LF produces the supplied reference MD5:

| Artifact | Algorithm | Checksum | State |
|---|---|---|---|
| Exact checkout file `data/raw/Customer Churn.csv` (CRLF) | MD5 | `e5362c3e5787dadd4e21eb606509bc03` | Recomputed locally |
| Exact checkout file `data/raw/Customer Churn.csv` (CRLF) | SHA256 | `90d5fb6bd1630cd4de4b4d28fcf8b4cb92a8f6ab7484605b0799d47386f7dbe1` | Recomputed locally; matches Week 3 config |
| Same checkout bytes normalized to LF | MD5 | `07311e7080c0fb5b0ce94f5977abc4d5` | Matches supplied reference MD5 |
| Same checkout bytes normalized to LF | SHA256 | `72a4a660cba4166bab4f0c24e930d5453d1917e208c9ce2ed16b841347350dd3` | Recomputed locally |

The byte-level checksum difference is therefore explained by LF/CRLF conversion. Parsing still yields the same 3,150 rows and stable `row_id`/split membership, so no new split is created.

## Reproducible workflow

```powershell
python scripts/validate_week2.py
python -m unittest discover -s tests -v
python scripts/eda_train.py
```

The split keeps every source record, groups identical content into one partition, stratifies by `Churn`, uses `random_state=42`, and targets approximately 60/20/20. Validation and test are not used for EDA or preprocessing decisions.
