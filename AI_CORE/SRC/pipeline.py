# ============================================
# ASTROVITAL AI — VITALX CORE V1
# src/pipeline.py
# Developer: Gouragopal Mohapatra
# © 2026 Gouragopal Mohapatra — All Rights Reserved
# ============================================

import numpy as np
import pandas as pd
import joblib
import os

from feature_engineering import engineer_features
from cdss_predictor import load_models, predict, format_output


SENSOR_PARAMS = [
    'Heart_Rate_bpm', 'Systolic_BP_mmHg',
    'Diastolic_BP_mmHg', 'Sleep_Hours',
    'Oxygen_Saturation', 'Muscle_Loss_percent',
    'Bone_Density_Loss', 'Radiation_mSv',
    'Immune_Score'
]

BEST_THRESHOLD = 0.27


def load_innovation3(model_hangar='../MODEL_HANGAR'):
    """Load Innovation 3 models."""
    return {
        'reg':      joblib.load(os.path.join(
            model_hangar,
            'innovation3_sensor_model.pkl')),
        'rf':       joblib.load(os.path.join(
            model_hangar,
            'innovation3_signal_model.pkl')),
        'encoder':  joblib.load(os.path.join(
            model_hangar,
            'innovation3_label_encoder.pkl')),
    }


def run_innovation3(df_noisy, models_i3):
    """
    Stage 1 — Sensor correction.
    Input : Noisy dataframe
    Output: Corrected + filtered dataframe
    """
    avail = [s for s in SENSOR_PARAMS
             if s in df_noisy.columns]
    X = df_noisy[avail].values

    # Part 1 — Regression correction
    try:
        X_corrected = models_i3['reg'].predict(X)
        df_corrected = pd.DataFrame(
            X_corrected, columns=avail
        )
    except Exception:
        df_corrected = df_noisy[avail].copy()

    # Part 2 — Signal separation
    try:
        quality = models_i3['rf'].predict(X_corrected)
        labels  = models_i3['encoder'].inverse_transform(
            quality
        )
        real_mask = labels == 'REAL'
        df_clean  = df_corrected[real_mask].copy()
        df_clean  = df_clean.reset_index(drop=True)
    except Exception:
        df_clean = df_corrected.copy()

    return df_clean


def run_full_pipeline(df_raw,
                      model_hangar='../MODEL_HANGAR',
                      threshold=BEST_THRESHOLD):
    """
    Full VitalX Core V1 Pipeline.

    Input : Raw noisy physiological dataframe
    Output: CDSS decisions + formatted results

    Stages:
        1. Innovation 3 — Sensor correction
        2. Feature engineering
        3. Innovation 1 — CDSS decision
    """

    print("=" * 55)
    print("  AstroVital AI — VitalX Core v1.0")
    print("  Full Pipeline Running...")
    print("=" * 55)

    # Stage 1 — Innovation 3
    print("\n[Stage 1] Innovation 3 — Sensor Correction")
    models_i3  = load_innovation3(model_hangar)
    df_clean   = run_innovation3(df_raw, models_i3)
    print(f"  ✅ Clean records: {len(df_clean)}")

    # Stage 2 — Feature Engineering
    print("\n[Stage 2] Feature Engineering")
    df_fe = engineer_features(df_clean)
    print(f"  ✅ Features: {df_fe.shape[1]} columns")

    # Stage 3 — Innovation 1 CDSS
    print("\n[Stage 3] Innovation 1 — CDSS Decision")
    models_cdss         = load_models(model_hangar)
    decisions, probas   = predict(
        df_fe, models_cdss, threshold
    )
    results = format_output(
        decisions, probas,
        models_cdss['encoder'],
        threshold
    )

    # Summary
    g  = sum(d == 'GREEN'  for d in decisions)
    yw = sum(d == 'YELLOW' for d in decisions)
    r  = sum(d == 'RED'    for d in decisions)
    t  = len(decisions)

    print(f"\n{'='*55}")
    print(f"  CDSS OUTPUT SUMMARY")
    print(f"{'='*55}")
    print(f"  🟢 GREEN:  {g} ({g/t*100:.1f}%)")
    print(f"  🟡 YELLOW: {yw} ({yw/t*100:.1f}%)")
    print(f"  🔴 RED:    {r} ({r/t*100:.1f}%)")
    print(f"{'='*55}")
    print(f"  ⚠️  CMO OVERRIDE AUTHORITY ACTIVE")
    print(f"{'='*55}")

    return decisions, probas, results


if __name__ == "__main__":
    # Quick test
    import pandas as pd

    df_test = pd.read_csv(
        '../DATA_VAULT/SENSOR_INTAKE/astrovital_dataset_v1.csv'
    ).head(10)

    decisions, probas, results = run_full_pipeline(df_test)

    print("\nSample Decisions:")
    for i, r in enumerate(results[:3]):
        print(f"  Record {i+1}: {r['icon']} {r['decision']}"
              f" — RED P: {r['red_prob']}%")