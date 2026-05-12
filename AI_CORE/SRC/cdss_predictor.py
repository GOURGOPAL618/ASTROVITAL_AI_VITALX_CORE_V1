# ============================================
# ASTROVITAL AI — VITALX CORE V1
# src/cdss_predictor.py
# Developer: Gouragopal Mohapatra
# © 2026 Gouragopal Mohapatra — All Rights Reserved
# ============================================

import numpy as np
import joblib
import os


def load_models(model_hangar_path='../MODEL_HANGAR'):
    """Load all CDSS models from MODEL_HANGAR."""
    models = {
        'cdss':     joblib.load(
            os.path.join(model_hangar_path,
                         'innovation1_cdss_model.pkl')),
        'encoder':  joblib.load(
            os.path.join(model_hangar_path,
                         'innovation1_label_encoder.pkl')),
        'features': joblib.load(
            os.path.join(model_hangar_path,
                         'innovation1_features.pkl')),
        'explainer':joblib.load(
            os.path.join(model_hangar_path,
                         'innovation1_dt_explainer.pkl')),
    }
    return models


def predict(df, models, threshold=0.27):
    """
    Run CDSS prediction on input dataframe.
    Returns: decisions, probabilities
    """
    features  = models['features']
    cdss      = models['cdss']
    le        = models['encoder']

    # Align features
    available = [f for f in features
                 if f in df.columns]
    X = df[available].values

    # Pad missing features
    if X.shape[1] < len(features):
        pad = np.zeros((
            X.shape[0],
            len(features) - X.shape[1]
        ))
        X = np.hstack([X, pad])

    # Predict
    red_idx = list(le.classes_).index('RED')
    probas  = cdss.predict_proba(X)
    preds   = np.array([
        red_idx if p[red_idx] >= threshold
        else np.argmax(p)
        for p in probas
    ])
    decisions = le.inverse_transform(preds)

    return decisions, probas


def format_output(decisions, probas, le, threshold=0.27):
    """Format CDSS output for display."""
    red_idx = list(le.classes_).index('RED')
    results = []

    actions = {
        'GREEN':  'CLEARED — Proceed with mission',
        'YELLOW': 'HOLD — Enhanced monitoring required',
        'RED':    'ABORT — Immediate CMO assessment'
    }

    for decision, proba in zip(decisions, probas):
        icon = "🟢" if decision == "GREEN" else \
               "🟡" if decision == "YELLOW" else "🔴"
        results.append({
            'decision':      decision,
            'icon':          icon,
            'action':        actions[decision],
            'red_prob':      round(proba[red_idx]*100, 1),
            'threshold_pct': round(threshold*100, 0),
            'confidence': {
                cls: round(prob*100, 1)
                for cls, prob in zip(le.classes_, proba)
            }
        })

    return results