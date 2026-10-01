# Week 2 Leakage Audit

Prediction point: use information available during the first nine months to predict churn in the following three months. Statistical association with `Churn` is not evidence of temporal availability.

| feature | definition | source | available before prediction point? | leakage risk | decision | evidence/reason |
|---|---|---|---|---|---|---|
| Call  Failure | Definition not verified; repository labels it a count | Repository data dictionary only | Provisionally yes | Low/unknown | Eligible with metadata caveat | Dictionary labels `observation_window`; authoritative definition is still desirable |
| Complains | Definition not verified; repository labels it a complaint count | Repository data dictionary only | Provisionally yes | Low/unknown | Eligible with metadata caveat | Dictionary labels `observation_window`; no post-outcome derivation is documented |
| Subscription  Length | Definition/unit not authoritatively verified | Repository data dictionary only | Provisionally yes | Low/unknown | Eligible with metadata caveat | Dictionary labels `observation_window` |
| Charge  Amount | Definition and aggregation interval not verified | Repository data dictionary only | Provisionally yes | Medium/unknown | Eligible with metadata caveat | Must remain limited to observation-window charges |
| Seconds of Use | Definition not verified; repository labels it usage | Repository data dictionary only | Provisionally yes | Low/unknown | Eligible with metadata caveat | Dictionary labels `observation_window` |
| Frequency of use | Definition not verified; repository labels it usage count | Repository data dictionary only | Provisionally yes | Low/unknown | Eligible with metadata caveat | Dictionary labels `observation_window` |
| Frequency of SMS | Definition not verified; repository labels it SMS count | Repository data dictionary only | Provisionally yes | Low/unknown | Eligible with metadata caveat | Dictionary labels `observation_window` |
| Distinct Called Numbers | Definition not verified; repository labels it a count | Repository data dictionary only | Provisionally yes | Low/unknown | Eligible with metadata caveat | Dictionary labels `observation_window` |
| Age Group | Ordinal age grouping; exact mapping not verified | Repository data dictionary only | Provisionally yes | Low | Eligible with metadata caveat | Dictionary labels it static; redundant information with Age is a modeling issue, not leakage by itself |
| Tariff Plan | Tariff category; code values not verified | Repository data dictionary only | Provisionally yes | Low/unknown | Eligible with metadata caveat | Dictionary labels it static |
| Status | Subscription status: 1=active, 2=non-active | UCI dataset 563 | Yes; first-nine-month aggregate | Controlled | **KEEP** | UCI places all non-target attributes in the first nine months, before month-12 churn |
| Age | Customer age; reference date not verified | Repository data dictionary only | Provisionally yes | Low | Eligible with metadata caveat | Dictionary labels it static |
| Customer Value | Calculated value of customer; exact formula not listed on UCI page | UCI dataset 563 | Yes; UCI explicitly places every non-target attribute in first-nine-month aggregates | Controlled; formula limitation | **KEEP** | Formula unknown is documented as a limitation, not treated as leakage evidence; no evidence uses churn/outcome |
| Churn | Binary outcome | CSV and repository dictionary | No; outcome window | Certain if used as input | **Target only; excluded from X** | Target must never be an input feature |
| row_id | Stable source-row sequence added by loader | `src/data.py` | Technical only | Identifier leakage/no predictive meaning | **Technical only; excluded from X** | Used only for split identity and audit assertions |

## Evidence used

UCI Iranian Churn dataset (ID 563) states that all attributes except churn aggregate the first nine months, while churn is observed at the end of month 12. This resolves temporal availability for both `Status` and `Customer Value`. The exact Customer Value derivation remains undocumented and is reported as a limitation; absence of a published formula is not evidence of leakage. Model performance, correlation, cross-tabs, uniqueness, SHAP values and coefficients were not used to make either decision.
