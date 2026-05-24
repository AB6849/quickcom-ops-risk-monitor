"""
Next-day risk forecasting using exponential smoothing.

Provides a 1-day-ahead risk prediction for every city so operations teams
can pre-position resources before conditions deteriorate, rather than reacting
after SLA breaches have already occurred.

Technique: Exponentially Weighted Moving Average (EWMA) — simple, interpretable,
and robust for short time series (7–14 days of history).
"""

import pandas as pd
import numpy as np

from config import RISK_SCORE_THRESHOLDS


def _classify(score: float) -> str:
    if score <= RISK_SCORE_THRESHOLDS['low']:
        return 'Low'
    elif score <= RISK_SCORE_THRESHOLDS['medium']:
        return 'Medium'
    return 'High'


def forecast_next_day(risk_df: pd.DataFrame, alpha: float = 0.4) -> pd.DataFrame:
    """
    Forecast each city's risk score for the day after the latest date.

    Higher alpha = more weight on recent observations (more reactive).
    Lower alpha = smoother, slower to react to sudden changes.
    alpha=0.4 balances responsiveness with noise reduction.

    Args:
        risk_df: Historical risk scores. Must have 'date', 'city', 'risk_score'.
        alpha: EWMA smoothing factor (0 < alpha <= 1).

    Returns:
        DataFrame with columns:
          city, forecast_date, forecast_risk, forecast_classification,
          trend (float: positive = worsening, negative = improving)
    """
    df = risk_df.sort_values(['city', 'date']).copy()

    records = []
    for city, city_df in df.groupby('city'):
        city_df = city_df.sort_values('date')
        if len(city_df) < 2:
            continue

        scores = city_df['risk_score'].values
        # EWMA over historical scores
        ewma = city_df['risk_score'].ewm(alpha=alpha, adjust=False).mean()
        forecast = float(np.clip(ewma.iloc[-1], 0, 100))

        # Trend: difference between last EWMA value and 3 days ago (or start)
        lookback = min(3, len(ewma) - 1)
        trend = float(ewma.iloc[-1] - ewma.iloc[-(lookback + 1)])

        next_date = city_df['date'].max() + pd.Timedelta(days=1)

        records.append({
            'city': city,
            'forecast_date': next_date,
            'forecast_risk': round(forecast, 1),
            'forecast_classification': _classify(forecast),
            'trend': round(trend, 2),
        })

    return pd.DataFrame(records).sort_values('forecast_risk', ascending=False).reset_index(drop=True)


def save_forecast(forecast_df: pd.DataFrame, output_path: str) -> None:
    """Save forecast DataFrame to CSV."""
    forecast_df.to_csv(output_path, index=False)
