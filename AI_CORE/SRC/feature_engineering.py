# ============================================
# ASTROVITAL AI — VITALX CORE V1
# src/feature_engineering.py
# Developer: Gouragopal Mohapatra
# © 2026 Gouragopal Mohapatra — All Rights Reserved
# ============================================

import numpy as np
import pandas as pd


def engineer_features(df):
    """
    Apply all feature engineering steps.
    Input: Raw physiological dataframe
    Output: DataFrame with engineered features
    """
    df = df.copy()

    # Pulse Pressure
    if 'Systolic_BP_mmHg' in df.columns and \
       'Diastolic_BP_mmHg' in df.columns:
        df['Pulse_Pressure'] = (
            df['Systolic_BP_mmHg'] -
            df['Diastolic_BP_mmHg']
        ).round(4)

    # Cardio Risk Index
    hr_col = [c for c in df.columns
              if 'heart' in c.lower()]
    if hr_col and 'Systolic_BP_mmHg' in df.columns:
        df['Cardio_Risk_Index'] = (
            df[hr_col[0]] *
            df['Systolic_BP_mmHg'] / 1000
        ).round(4)

    # Sleep Deficit
    if 'Sleep_Hours' in df.columns:
        df['Sleep_Deficit'] = (
            7.0 - df['Sleep_Hours']
        ).round(2)

    # Musculo Risk
    ml_col = [c for c in df.columns
              if 'muscle' in c.lower()]
    if ml_col and 'Bone_Density_Loss' in df.columns:
        df['Musculo_Risk'] = (
            df[ml_col[0]] +
            df['Bone_Density_Loss'] * 10
        ).round(4)

    # Radiation Risk Per Day
    if 'Radiation_mSv' in df.columns and \
       'Mission_Duration_Days' in df.columns:
        df['Radiation_Risk_Per_Day'] = (
            df['Radiation_mSv'] /
            df['Mission_Duration_Days']
        ).round(6)

    # Overall Risk Score
    if 'Cardio_Risk_Index' in df.columns:
        df['Overall_Risk_Score'] = (
            (df['Cardio_Risk_Index'] /
             (df['Cardio_Risk_Index'].max()+1e-9))*0.25 +
            (df.get('Sleep_Deficit',
              pd.Series(np.zeros(len(df)))) /
             (df.get('Sleep_Deficit',
              pd.Series(np.ones(len(df)))).max()+1e-9))*0.20 +
            (df.get('Musculo_Risk',
              pd.Series(np.zeros(len(df)))) /
             (df.get('Musculo_Risk',
              pd.Series(np.ones(len(df)))).max()+1e-9))*0.20 +
            (df['Radiation_mSv'] /
             (df['Radiation_mSv'].max()+1e-9))*0.20 +
            (1 - df['Immune_Score']/100)*0.15
        ).round(4)

    # Space Stress Index
    if 'Overall_Risk_Score' in df.columns and \
       'Radiation_mSv' in df.columns:
        df['Space_Stress_Index'] = (
            df['Overall_Risk_Score'] *
            df['Radiation_mSv'] / 100
        ).round(4)

    # Critical Risk Gap
    if 'Overall_Risk_Score' in df.columns and \
       'Sleep_Deficit' in df.columns:
        df['Critical_Risk_Gap'] = (
            df['Overall_Risk_Score'] -
            df['Sleep_Deficit'] /
            (df['Sleep_Deficit'].max()+1e-9)
        ).round(4)

    # Vascular Impact
    if 'Pulse_Pressure' in df.columns and \
       'Cardio_Risk_Index' in df.columns:
        df['Vascular_Impact'] = (
            df['Pulse_Pressure'] *
            df['Cardio_Risk_Index'] / 100
        ).round(4)

    return df