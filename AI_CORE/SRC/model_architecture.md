# ASTROVITAL AI — VITALX CORE V1
## Model Architecture Documentation

**Developer:** Gouragopal Mohapatra  
**Date:** May 2026  
**© 2026 Gouragopal Mohapatra — All Rights Reserved**

---

## Overview

VITALX CORE V1 implements 3 innovations connected
as one end-to-end pipeline.

---

## Innovation 3 — Sensor Correction

### Part 1 — Multivariate Regression
| Property | Detail |
|---|---|
| Algorithm | Ridge Regression |
| Wrapper | MultiOutputRegressor |
| Alpha | 1.0 |
| Input | 9 noisy sensor parameters |
| Output | Drift-corrected signals |
| R2 Score | 0.823 |

### Part 2 — Signal Separation
| Property | Detail |
|---|---|
| Algorithm | RandomForestClassifier |
| n_estimators | 100 |
| max_depth | 10 |
| class_weight | balanced |
| Output | REAL / NOISY labels |

---

## Innovation 6 — Biomarker Discovery

| Property | Detail |
|---|---|
| Algorithm | RandomForestClassifier |
| n_estimators | 200 |
| max_depth | 15 |
| min_samples_split | 5 |
| class_weight | balanced |
| Features In | 14 parameters |
| Output | Ranked importance scores |

---

## Innovation 1 — Edge CDSS

### Primary Model
| Property | Detail |
|---|---|
| Algorithm | RandomForestClassifier |
| n_estimators | 200 |
| max_depth | 15 |
| class_weight | balanced |
| Imbalance | SMOTE k_neighbors=3 |
| Threshold | 0.27 (tuned) |
| Accuracy | 85.25% |
| RED Recall | 75.86% |

### Explainer Layer
| Property | Detail |
|---|---|
| Algorithm | DecisionTreeClassifier |
| max_depth | 5 |
| criterion | entropy |
| Purpose | White-box IF/THEN rules |

---

## Performance Summary

| Innovation | Metric | Value |
|---|---|---|
| Innovation 3 | R2 Score | 0.823 |
| Innovation 6 | CV Mean | > 0.83 |
| Innovation 1 | Accuracy | 85.25% |
| Innovation 1 | RED Recall | 75.86% |
| Innovation 1 | Macro F1 | 80.33% |

---

## Edge Deployment

- Cloud required: **NO**
- Inference time: **< 10ms**
- Threshold: **0.27**
- CMO override: **Always active**

---

*© 2026 Gouragopal Mohapatra — All Rights Reserved*