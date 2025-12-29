"""
Operational Risk Scoring Engine for India Quick-Commerce

This module implements a rule-based risk scoring system that evaluates
operational risk for quick-commerce operations across Indian cities.

Risk factors considered:
1. Traffic congestion - delays delivery times
2. Weather (rainfall) - affects delivery operations and safety
3. Demand surge - strains operational capacity

The risk score is computed on a 0-100 scale and classified as Low, Medium, or High.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple
import sys

# Import configuration
from config import (
    RISK_WEIGHTS,
    TRAFFIC_THRESHOLDS,
    WEATHER_THRESHOLDS,
    DEMAND_THRESHOLDS,
    TEMPERATURE_THRESHOLDS,
    RISK_SCORE_THRESHOLDS,
    get_city_tier,
    get_sla_thresholds
)


def compute_traffic_risk_score(congestion_level: float, congestion_7d_avg: float) -> float:
    """
    Compute traffic risk score component (0-100).
    
    Logic:
    - High congestion directly impacts delivery times
    - We consider both current congestion and 7-day average
    - Congestion > 0.8 is critical (severe delays expected)
    - Congestion 0.6-0.8 is high risk
    - Congestion 0.3-0.6 is medium risk
    - Congestion < 0.3 is low risk
    
    Args:
        congestion_level: Current day congestion level (0-1)
        congestion_7d_avg: 7-day average congestion level
        
    Returns:
        Traffic risk score (0-100)
    """
    # Use the higher of current or 7-day average (captures sustained issues)
    effective_congestion = max(congestion_level, congestion_7d_avg)
    
    if effective_congestion >= TRAFFIC_THRESHOLDS['high']:
        # Critical congestion: 80-100 points
        # Scale from 80 to 100 based on how much above 0.8
        excess = (effective_congestion - TRAFFIC_THRESHOLDS['high']) / (1.0 - TRAFFIC_THRESHOLDS['high'])
        score = 80 + (excess * 20)
        return min(100, score)
    
    elif effective_congestion >= TRAFFIC_THRESHOLDS['medium']:
        # High congestion: 50-80 points
        # Scale from 50 to 80
        excess = (effective_congestion - TRAFFIC_THRESHOLDS['medium']) / (
            TRAFFIC_THRESHOLDS['high'] - TRAFFIC_THRESHOLDS['medium']
        )
        score = 50 + (excess * 30)
        return score
    
    elif effective_congestion >= TRAFFIC_THRESHOLDS['low']:
        # Medium congestion: 20-50 points
        excess = (effective_congestion - TRAFFIC_THRESHOLDS['low']) / (
            TRAFFIC_THRESHOLDS['medium'] - TRAFFIC_THRESHOLDS['low']
        )
        score = 20 + (excess * 30)
        return score
    
    else:
        # Low congestion: 0-20 points
        excess = effective_congestion / TRAFFIC_THRESHOLDS['low']
        score = excess * 20
        return score


def compute_weather_risk_score(rainfall_mm: float, rainfall_7d_avg: float, 
                               temperature: float) -> float:
    """
    Compute weather risk score component (0-100).
    
    Logic:
    - Heavy rainfall (>30mm) severely impacts delivery operations
    - Moderate rainfall (15-30mm) causes delays
    - Light rainfall (<5mm) has minimal impact
    - Extreme temperatures also affect operations
    
    Args:
        rainfall_mm: Current day rainfall in mm
        rainfall_7d_avg: 7-day average rainfall
        temperature: Current temperature in Celsius
        
    Returns:
        Weather risk score (0-100)
    """
    # Use the higher of current or 7-day average rainfall
    effective_rainfall = max(rainfall_mm, rainfall_7d_avg)
    
    # Rainfall risk component
    if effective_rainfall >= WEATHER_THRESHOLDS['high']:
        # Critical rainfall: 70-100 points
        excess = (effective_rainfall - WEATHER_THRESHOLDS['high']) / 50.0  # Assume max ~80mm
        score = 70 + (min(excess, 1.0) * 30)
    elif effective_rainfall >= WEATHER_THRESHOLDS['medium']:
        # High rainfall: 40-70 points
        excess = (effective_rainfall - WEATHER_THRESHOLDS['medium']) / (
            WEATHER_THRESHOLDS['high'] - WEATHER_THRESHOLDS['medium']
        )
        score = 40 + (excess * 30)
    elif effective_rainfall >= WEATHER_THRESHOLDS['low']:
        # Medium rainfall: 15-40 points
        excess = (effective_rainfall - WEATHER_THRESHOLDS['low']) / (
            WEATHER_THRESHOLDS['medium'] - WEATHER_THRESHOLDS['low']
        )
        score = 15 + (excess * 25)
    else:
        # Low rainfall: 0-15 points
        excess = effective_rainfall / WEATHER_THRESHOLDS['low']
        score = excess * 15
    
    # Temperature risk component (additive)
    temp_risk = 0
    if temperature <= TEMPERATURE_THRESHOLDS['cold_risk']:
        # Cold weather risk: add up to 10 points
        temp_risk = (TEMPERATURE_THRESHOLDS['cold_risk'] - temperature) / 10.0 * 10
    elif temperature >= TEMPERATURE_THRESHOLDS['hot_risk']:
        # Extreme heat risk: add up to 15 points
        temp_risk = (temperature - TEMPERATURE_THRESHOLDS['hot_risk']) / 10.0 * 15
    
    # Combine rainfall and temperature risks (capped at 100)
    total_score = min(100, score + temp_risk)
    return total_score


def compute_demand_risk_score(demand_index: float, demand_7d_avg: float) -> float:
    """
    Compute demand risk score component (0-100).
    
    Logic:
    - High demand surge (>0.85) strains operational capacity
    - Elevated demand (0.7-0.85) requires attention
    - Normal demand (<0.5) is low risk
    
    Args:
        demand_index: Current day demand index (0-1)
        demand_7d_avg: 7-day average demand index
        
    Returns:
        Demand risk score (0-100)
    """
    # Use the higher of current or 7-day average (captures sustained surge)
    effective_demand = max(demand_index, demand_7d_avg)
    
    if effective_demand >= DEMAND_THRESHOLDS['high']:
        # Surge demand: 60-100 points
        excess = (effective_demand - DEMAND_THRESHOLDS['high']) / (1.0 - DEMAND_THRESHOLDS['high'])
        score = 60 + (excess * 40)
        return min(100, score)
    
    elif effective_demand >= DEMAND_THRESHOLDS['medium']:
        # High demand: 30-60 points
        excess = (effective_demand - DEMAND_THRESHOLDS['medium']) / (
            DEMAND_THRESHOLDS['high'] - DEMAND_THRESHOLDS['medium']
        )
        score = 30 + (excess * 30)
        return score
    
    elif effective_demand >= DEMAND_THRESHOLDS['low']:
        # Medium demand: 10-30 points
        excess = (effective_demand - DEMAND_THRESHOLDS['low']) / (
            DEMAND_THRESHOLDS['medium'] - DEMAND_THRESHOLDS['low']
        )
        score = 10 + (excess * 20)
        return score
    
    else:
        # Low demand: 0-10 points
        excess = effective_demand / DEMAND_THRESHOLDS['low']
        score = excess * 10
        return score


def compute_combined_risk_score(traffic_score: float, weather_score: float, 
                                demand_score: float) -> float:
    """
    Compute weighted combined risk score.
    
    Args:
        traffic_score: Traffic risk component (0-100)
        weather_score: Weather risk component (0-100)
        demand_score: Demand risk component (0-100)
        
    Returns:
        Combined risk score (0-100)
    """
    combined = (
        traffic_score * RISK_WEIGHTS['traffic'] +
        weather_score * RISK_WEIGHTS['weather'] +
        demand_score * RISK_WEIGHTS['demand']
    )
    return min(100, max(0, combined))


def classify_risk(risk_score: float) -> str:
    """
    Classify risk score into Low, Medium, or High.
    
    Args:
        risk_score: Combined risk score (0-100)
        
    Returns:
        Risk classification string
    """
    if risk_score <= RISK_SCORE_THRESHOLDS['low']:
        return 'Low'
    elif risk_score <= RISK_SCORE_THRESHOLDS['medium']:
        return 'Medium'
    else:
        return 'High'


def compute_risk_scores(features_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute operational risk scores for all cities and dates.
    
    Args:
        features_df: DataFrame with daily city features
        
    Returns:
        DataFrame with risk scores and classifications
    """
    df = features_df.copy()
    
    # Compute individual risk components
    df['traffic_risk'] = df.apply(
        lambda row: compute_traffic_risk_score(
            row['congestion_level'],
            row.get('congestion_level_7d_avg', row['congestion_level'])
        ),
        axis=1
    )
    
    df['weather_risk'] = df.apply(
        lambda row: compute_weather_risk_score(
            row['rainfall_mm'],
            row.get('rainfall_mm_7d_avg', row['rainfall_mm']),
            row['temperature']
        ),
        axis=1
    )
    
    df['demand_risk'] = df.apply(
        lambda row: compute_demand_risk_score(
            row['demand_index'],
            row.get('demand_index_7d_avg', row['demand_index'])
        ),
        axis=1
    )
    
    # Compute combined risk score
    df['risk_score'] = df.apply(
        lambda row: compute_combined_risk_score(
            row['traffic_risk'],
            row['weather_risk'],
            row['demand_risk']
        ),
        axis=1
    )
    
    # Classify risk
    df['risk_classification'] = df['risk_score'].apply(classify_risk)
    
    # Add city tier information
    df['city_tier'] = df['city'].apply(get_city_tier)
    
    # Select output columns
    output_cols = [
        'date', 'city', 'city_tier',
        'traffic_risk', 'weather_risk', 'demand_risk',
        'risk_score', 'risk_classification',
        'congestion_level', 'rainfall_mm', 'temperature', 'demand_index'
    ]
    
    # Only include columns that exist
    output_cols = [col for col in output_cols if col in df.columns]
    
    return df[output_cols]


def generate_alerts(risk_df: pd.DataFrame, date: str = None) -> pd.DataFrame:
    """
    Generate alerts for high-risk cities.
    
    Args:
        risk_df: DataFrame with risk scores
        date: Specific date to filter (default: latest date)
        
    Returns:
        DataFrame with high-risk alerts
    """
    df = risk_df.copy()
    
    # Filter to specified date or latest date
    if date:
        df = df[df['date'] == pd.to_datetime(date)]
    else:
        latest_date = df['date'].max()
        df = df[df['date'] == latest_date]
    
    # Filter to high-risk cities only
    alerts = df[df['risk_classification'] == 'High'].copy()
    
    # Sort by risk score (highest first)
    alerts = alerts.sort_values('risk_score', ascending=False)
    
    # Add alert details
    alerts['alert_reason'] = alerts.apply(
        lambda row: _generate_alert_reason(row),
        axis=1
    )
    
    return alerts


def _generate_alert_reason(row: pd.Series) -> str:
    """
    Generate human-readable alert reason.
    
    Args:
        row: Series with risk components
        
    Returns:
        Alert reason string
    """
    reasons = []
    
    if row['traffic_risk'] >= 60:
        reasons.append(f"High traffic congestion ({row['congestion_level']:.2f})")
    
    if row['weather_risk'] >= 60:
        reasons.append(f"Heavy rainfall ({row['rainfall_mm']:.1f}mm)")
    
    if row['demand_risk'] >= 60:
        reasons.append(f"Demand surge ({row['demand_index']:.2f})")
    
    if not reasons:
        # Even if individual components aren't high, combined risk is high
        reasons.append("Multiple risk factors combined")
    
    return "; ".join(reasons)


def run_risk_engine(features_path: str, output_dir: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Main function to run the risk engine end-to-end.
    
    Args:
        features_path: Path to daily city features CSV
        output_dir: Directory to save outputs
        
    Returns:
        Tuple of (risk_df, alerts_df)
    """
    # Load features
    features_df = pd.read_csv(features_path, parse_dates=['date'])
    
    # Compute risk scores
    risk_df = compute_risk_scores(features_df)
    
    # Generate alerts
    alerts_df = generate_alerts(risk_df)
    
    # Save outputs
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    risk_df.to_csv(output_path / 'daily_city_risk.csv', index=False)
    alerts_df.to_csv(output_path / 'alerts_today.csv', index=False)
    
    print(f"Risk scores saved to: {output_path / 'daily_city_risk.csv'}")
    print(f"Alerts saved to: {output_path / 'alerts_today.csv'}")
    print(f"\nTotal cities monitored: {risk_df['city'].nunique()}")
    print(f"Date range: {risk_df['date'].min().date()} to {risk_df['date'].max().date()}")
    print(f"High-risk alerts today: {len(alerts_df)}")
    
    return risk_df, alerts_df


if __name__ == '__main__':
    # Default paths
    features_path = '../data/processed/daily_city_features.csv'
    output_dir = '../outputs'
    
    # Run risk engine
    risk_df, alerts_df = run_risk_engine(features_path, output_dir)
    
    # Print summary
    print("\n=== Risk Summary ===")
    latest_date = risk_df['date'].max()
    latest_risk = risk_df[risk_df['date'] == latest_date]
    
    print(f"\nRisk distribution for {latest_date.date()}:")
    print(latest_risk['risk_classification'].value_counts())
    
    if len(alerts_df) > 0:
        print("\n=== High-Risk Alerts ===")
        print(alerts_df[['city', 'risk_score', 'alert_reason']].to_string(index=False))
    else:
        print("\nNo high-risk alerts today.")

