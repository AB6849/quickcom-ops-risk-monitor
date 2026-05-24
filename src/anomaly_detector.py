"""
Anomaly detection for operational risk monitoring.

Uses IsolationForest to find cities whose traffic/weather/demand combination
is statistically unusual — catching edge cases the rule-based thresholds miss.

For example: a city with moderate traffic AND moderate rain AND elevated demand
may not breach any single threshold yet still be anomalous because all three
signals are elevated simultaneously.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


FEATURE_COLS = ['traffic_risk', 'weather_risk', 'demand_risk']


def detect_anomalies(risk_df: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    """
    Detect cities with anomalous risk patterns using IsolationForest.

    Operates on the full historical dataset so the model learns what
    'normal' looks like before flagging today's outliers.

    Args:
        risk_df: DataFrame with traffic_risk, weather_risk, demand_risk columns.
        contamination: Expected fraction of anomalies (default 5%).

    Returns:
        DataFrame with two new columns:
          - is_anomaly (bool): True if city/date is anomalous
          - anomaly_score (float 0–1): Higher = more anomalous
    """
    df = risk_df.copy()

    if len(df) < 10 or not all(c in df.columns for c in FEATURE_COLS):
        df['is_anomaly'] = False
        df['anomaly_score'] = 0.0
        return df

    features = df[FEATURE_COLS].fillna(0).values

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    clf = IsolationForest(
        contamination=contamination,
        n_estimators=200,
        random_state=42,
    )
    clf.fit(features_scaled)

    # score_samples returns negative values; more negative = more anomalous
    raw_scores = clf.score_samples(features_scaled)
    labels = clf.predict(features_scaled)  # -1 anomaly, +1 normal

    # Normalise to 0–1 where 1 = most anomalous
    score_range = raw_scores.max() - raw_scores.min()
    if score_range > 0:
        normalised = (raw_scores.max() - raw_scores) / score_range
    else:
        normalised = np.zeros_like(raw_scores)

    df['is_anomaly'] = labels == -1
    df['anomaly_score'] = np.round(normalised, 3)

    return df


def get_anomaly_summary(risk_df: pd.DataFrame, date: str = None) -> pd.DataFrame:
    """
    Return anomalous cities for a given date, sorted by anomaly score.

    Args:
        risk_df: DataFrame already containing is_anomaly and anomaly_score.
        date: ISO date string (default: latest date in dataset).

    Returns:
        DataFrame of anomalous city rows for that date.
    """
    df = risk_df.copy()

    if 'is_anomaly' not in df.columns:
        df = detect_anomalies(df)

    if date:
        df = df[df['date'] == pd.to_datetime(date)]
    else:
        df = df[df['date'] == df['date'].max()]

    return (
        df[df['is_anomaly']]
        .sort_values('anomaly_score', ascending=False)
        .reset_index(drop=True)
    )
