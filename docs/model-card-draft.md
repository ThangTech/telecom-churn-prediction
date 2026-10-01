# Model Card — Draft

Audit status: **PASS / FINAL for Week 4 coursework**. Exact Customer Value formula and post-refit capacity precision remain documented limitations.

## Model

Logistic Regression probability classifier.

- class_weight: None
- C: 10
- random_state: 42
- final fit partition: train + validation, after every decision was frozen
- final evaluation: one test evaluation only; test was not rerun during correction

## Intended Use

Rank and prioritize telecom customers who may churn so a care team can offer appropriate support within a defined contact capacity.

## Not Intended For

- discriminatory pricing;
- automatically denying or terminating service;
- harassing customers or making excessive contact;
- treating churn probability as a factual diagnosis;
- causal conclusions about why a customer churns;
- use on another population without new validation.

## Dataset

Iranian Churn Dataset, UCI Machine Learning Repository dataset 563. The repository file contains 3,150 rows. UCI states that all non-target attributes aggregate the first nine months and Churn records status at the end of month 12.

Frozen split: train 1,890; validation 630; test 630. Duplicate content is grouped so it cannot cross partitions.

## Prediction Task

Use the nine-month observation window to predict the probability of churn after the three-month planning gap.

## Features

Final 13-feature set:

Call Failure, Complains, Subscription Length, Charge Amount, Seconds of Use, Frequency of use, Frequency of SMS, Distinct Called Numbers, Age Group, Tariff Plan, Status, Age, Customer Value.

Churn is the target. row_id is technical and never enters the model.

Feature-set approval is **FINAL**. Status is KEEP because UCI defines it as active/non-active and places every non-target attribute in the first-nine-month observation window. Customer Value is KEEP because UCI calls it the calculated value of customer, explicitly lists it among non-target attributes and places all non-target attributes in the same observation window. The exact formula/component fields are not published; formula unknown is a limitation, not evidence of leakage. No feature was changed after test.

## Output

- churn probability in [0,1];
- LOW, MEDIUM or HIGH care-team priority according to frozen capacity thresholds.

## Preprocessing

Numeric features use median imputation and StandardScaler. Categorical features use most-frequent imputation and OneHotEncoder(handle_unknown="ignore"). Preprocessing is part of the pipeline and is not refit on held-out data.

## Model Selection

Six configurations were compared with the same five grouped, stratified folds on train only:

- C ∈ {0.1, 1, 10};
- class_weight ∈ {None, balanced};
- primary metric: mean train-CV PR_AUC;
- secondary metrics: AP, ROC_AUC, Brier, precision, recall and F1.

The selected candidate was unweighted Logistic Regression with C=10. Validation was not used to replace the train-CV-selected model.

This grid was rerun after the feature list changed from 11 to 13. The selected 13-feature run had mean CV PR_AUC 0.752463 ± 0.069578 and mean AP 0.755157 ± 0.068643.

## Thresholds

Thresholds were selected from validation before any test prediction:

| Capacity | Frozen threshold | Validation coverage | Validation precision | Validation recall | Validation F1 |
|---|---:|---:|---:|---:|---:|
| LOW, about 10% | 0.476833 | 10.00% | 0.761905 | 0.484848 | 0.592593 |
| MEDIUM, about 20% | 0.343183 | 20.00% | 0.595238 | 0.757576 | 0.666667 |
| HIGH, about 30% | 0.165057 | 30.16% | 0.468421 | 0.898990 | 0.615917 |

MEDIUM is the primary threshold because the assumed care-team capacity is approximately 20% of customers. Capacity must be re-agreed if operational resources change.

Protocol caveat: thresholds were selected from validation probabilities of a model fitted on train only. The final model was then refitted on train+validation and the same absolute threshold was applied once to test. Refit can shift the probability scale, so threshold 0.343183 does not guarantee exactly 20% coverage on test/new data. It remains the valid frozen threshold; its capacity interpretation is approximate after refit. No test coverage was used to adjust it.

## Validation Metrics

For the train-fit candidate on validation:

- PR_AUC: 0.760070
- AP: 0.761101
- ROC_AUC: 0.936493
- Brier: 0.069941

At the primary MEDIUM threshold: precision 0.595238, recall 0.757576 and F1 0.666667.

## Test Metrics

The test set was evaluated once after freeze. The final pipeline was fit on train+validation without using test for tuning.

- PR_AUC: 0.796582
- AP: 0.798105
- ROC_AUC: 0.949951
- Brier: 0.062798
- Precision: 0.678261
- Recall: 0.787879
- F1: 0.728972
- TN=494, FP=37, FN=21, TP=78

Classification metrics use the frozen primary threshold 0.343183.

These values are retained unchanged. The correction changed only metadata and interpretation; model, C, thresholds and test metrics were not changed. Test was not used for tuning.

## Calibration

Test Brier score is 0.062798. The lowest-probability bin contains 410 samples and slightly overpredicts risk (mean 0.0181 versus observed 0.0049). Mid-range bins show both under- and overprediction. Bins 6–8 contain only 3, 3 and 7 samples, so their apparent deviations are not reliable. The model was not recalibrated after test inspection.

## Error Analysis

Subscription Length boundaries were fitted on train+validation predictors at 32 and 37. The low group has lower precision (0.462) and more false positives (21) than the other groups. Each tenure group has seven false negatives. This is descriptive, not evidence of causation.

Charge Amount boundaries were fitted at 0 and 1. The low group is larger and has a higher churn rate, producing most absolute errors (FP=36, FN=13). Medium/high groups contain few churn cases, so their recall estimates are uncertain.

## Coefficient Interpretation

Positive coefficients are associated with higher model log-odds; negative coefficients with lower model log-odds, conditional on the rest of the transformed design matrix. They do not establish causality.

Largest positive coefficients include Customer Value, Age Group 2, Complains=1, Age Group 3 and Call Failure. Largest negative coefficients include Frequency of SMS, Frequency of use, Age Group 1, Complains=0 and Age Group 5.

Numeric coefficients refer to a one-standard-deviation change because numeric inputs are standardized. One-hot coefficients must be interpreted cautiously because all category levels are represented and correlated features can redistribute weight.

## Limitations

- Only 3,150 records from one dataset/population.
- Exact Customer Value formula is not published on the UCI dataset page.
- Status and Customer Value are temporally eligible according to UCI observation-window metadata. Exact Customer Value formula is unknown and should be documented if the provider releases it.
- Calibration bins can be small.
- Capacity thresholds depend on the validation distribution and may drift.
- Group metrics can be unstable when a group contains few churn cases.
- Coefficients are associational, not causal.
- No fairness claim is made; subgroup governance requires separate analysis.
- Test results must not be reused for further tuning.
- Thresholds were selected on a train-fit model and transferred unchanged to a train+validation-refit model; probability-scale drift can change achieved capacity.
- Realized coverage can differ from validation target capacity after train+validation refit; this is a deployment-monitoring limitation, not test leakage.

## Ethical Use

Use scores only to prioritize helpful, proportionate customer outreach. Provide human review, respect communication preferences, monitor disparate impact and avoid punitive actions based on predicted churn.
