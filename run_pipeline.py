#!/usr/bin/env python3
"""
Main execution script for India Quick-Commerce Operational Risk Monitor

Pipeline steps:
  0. Fetch daily data from public APIs
  1. Data ingestion and cleaning
  2. Feature engineering (rolling 7-day windows)
  3. Rule-based risk scoring and alert generation
  4. ML anomaly detection (IsolationForest on risk components)
  5. Next-day risk forecasting (EWMA)

Usage:
    python run_pipeline.py
"""

import logging
import sys
from pathlib import Path
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(levelname)-8s  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
log = logging.getLogger(__name__)

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from risk_engine import run_risk_engine
from data_fetcher import fetch_all_data
from anomaly_detector import detect_anomalies
from forecaster import forecast_next_day, save_forecast


def run_data_ingestion():
    """Run data ingestion and cleaning."""
    log.info("STEP 1: Data Ingestion and Cleaning")

    raw_data_dir = Path('data/raw')
    processed_data_dir = Path('data/processed')
    processed_data_dir.mkdir(parents=True, exist_ok=True)

    weather_df = pd.read_csv(raw_data_dir / 'weather_india.csv')
    traffic_df = pd.read_csv(raw_data_dir / 'traffic_india.csv')
    demand_df = pd.read_csv(raw_data_dir / 'demand_india.csv')

    log.info("Loaded raw data — weather%s  traffic%s  demand%s",
             weather_df.shape, traffic_df.shape, demand_df.shape)
    
    # Clean column names
    def clean_column_names(df):
        df = df.copy()
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        return df
    
    weather_df = clean_column_names(weather_df)
    traffic_df = clean_column_names(traffic_df)
    demand_df = clean_column_names(demand_df)
    
    # Normalize city names
    def normalize_city_names(df, city_col='city'):
        df = df.copy()
        df[city_col] = df[city_col].str.strip().str.title()
        return df
    
    weather_df = normalize_city_names(weather_df)
    traffic_df = normalize_city_names(traffic_df)
    demand_df = normalize_city_names(demand_df)
    
    # Parse dates
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    traffic_df['date'] = pd.to_datetime(traffic_df['date'])
    demand_df['date'] = pd.to_datetime(demand_df['date'])
    
    # Handle missing values
    def handle_missing_values(df, dataset_name):
        df = df.copy()
        df = df.sort_values(['city', 'date'])
        
        if dataset_name == 'weather':
            df['rainfall_mm'] = df.groupby('city')['rainfall_mm'].ffill().fillna(0)
            df['temperature'] = df.groupby('city')['temperature'].transform(lambda x: x.interpolate(method='linear', limit_direction='both'))
            df['temperature'] = df.groupby('city')['temperature'].ffill()
        elif dataset_name == 'traffic':
            df['congestion_level'] = df.groupby('city')['congestion_level'].ffill()
            city_medians = df.groupby('city')['congestion_level'].transform('median')
            df['congestion_level'] = df['congestion_level'].fillna(city_medians)
        elif dataset_name == 'demand':
            df['demand_index'] = df.groupby('city')['demand_index'].ffill()
            city_medians = df.groupby('city')['demand_index'].transform('median')
            df['demand_index'] = df['demand_index'].fillna(city_medians)
        
        return df
    
    weather_df = handle_missing_values(weather_df, 'weather')
    traffic_df = handle_missing_values(traffic_df, 'traffic')
    demand_df = handle_missing_values(demand_df, 'demand')
    
    # Save cleaned data
    weather_df.to_csv(processed_data_dir / 'weather_cleaned.csv', index=False)
    traffic_df.to_csv(processed_data_dir / 'traffic_cleaned.csv', index=False)
    demand_df.to_csv(processed_data_dir / 'demand_cleaned.csv', index=False)

    log.info("Data ingestion complete — cleaned files saved to %s", processed_data_dir)
    return weather_df, traffic_df, demand_df


def run_feature_engineering(weather_df, traffic_df, demand_df):
    """Run feature engineering."""
    log.info("STEP 2: Feature Engineering")

    processed_data_dir = Path('data/processed')
    
    # Create rolling features
    def create_rolling_features(df, value_col, window=7, group_col='city'):
        df = df.copy()
        df = df.sort_values([group_col, 'date']).reset_index(drop=True)
        
        rolling_col = f'{value_col}_7d_avg'
        df[rolling_col] = df.groupby(group_col)[value_col].transform(
            lambda x: x.rolling(window=window, min_periods=1).mean()
        )
        
        rolling_max_col = f'{value_col}_7d_max'
        df[rolling_max_col] = df.groupby(group_col)[value_col].transform(
            lambda x: x.rolling(window=window, min_periods=1).max()
        )
        
        return df
    
    traffic_df = create_rolling_features(traffic_df, 'congestion_level', window=7)
    weather_df = create_rolling_features(weather_df, 'rainfall_mm', window=7)
    demand_df = create_rolling_features(demand_df, 'demand_index', window=7)
    
    # Merge datasets
    daily_features = weather_df[['date', 'city', 'rainfall_mm', 'rainfall_mm_7d_avg', 
                                  'rainfall_mm_7d_max', 'temperature']].copy()
    
    daily_features = daily_features.merge(
        traffic_df[['date', 'city', 'congestion_level', 'congestion_level_7d_avg', 
                    'congestion_level_7d_max']],
        on=['date', 'city'],
        how='outer'
    )
    
    daily_features = daily_features.merge(
        demand_df[['date', 'city', 'demand_index', 'demand_index_7d_avg', 
                   'demand_index_7d_max']],
        on=['date', 'city'],
        how='outer'
    )
    
    daily_features = daily_features.sort_values(['date', 'city']).reset_index(drop=True)
    
    # Handle missing values in merged dataset
    for col in daily_features.columns:
        if col not in ['date', 'city']:
            daily_features[col] = daily_features.groupby('city')[col].ffill()
            daily_features[col] = daily_features.groupby('city')[col].bfill()
            if daily_features[col].dtype in ['float64', 'int64']:
                daily_features[col] = daily_features[col].fillna(0)
    
    # Save feature table
    output_path = processed_data_dir / 'daily_city_features.csv'
    daily_features.to_csv(output_path, index=False)

    log.info(
        "Feature engineering complete — %d records, %d cities, %s to %s",
        len(daily_features),
        daily_features['city'].nunique(),
        daily_features['date'].min().date(),
        daily_features['date'].max().date(),
    )
    return daily_features


def run_anomaly_detection(risk_df: pd.DataFrame, output_dir: str) -> pd.DataFrame:
    """Step 4: ML anomaly detection on risk components."""
    log.info("STEP 4: Anomaly Detection (IsolationForest)")

    enriched = detect_anomalies(risk_df)

    output_path = Path(output_dir) / 'daily_city_risk.csv'
    enriched.to_csv(output_path, index=False)

    n_anomalies = enriched[enriched['date'] == enriched['date'].max()]['is_anomaly'].sum()
    log.info("Anomaly detection complete — %d anomalous cities today", n_anomalies)

    return enriched


def run_forecasting(risk_df: pd.DataFrame, output_dir: str) -> pd.DataFrame:
    """Step 5: Next-day risk forecasting (EWMA)."""
    log.info("STEP 5: Next-Day Risk Forecasting (EWMA)")

    forecast_df = forecast_next_day(risk_df)

    output_path = Path(output_dir) / 'forecast_tomorrow.csv'
    save_forecast(forecast_df, str(output_path))

    high_forecast = (forecast_df['forecast_classification'] == 'High').sum()
    next_date = forecast_df['forecast_date'].iloc[0].date() if len(forecast_df) else 'N/A'
    log.info("Forecast for %s: %d cities predicted High risk", next_date, high_forecast)

    return forecast_df


def main():
    """Run the complete five-step pipeline."""
    log.info("=" * 55)
    log.info("India Quick-Commerce Operational Risk Monitor")
    log.info("=" * 55)

    # Step 0: Fetch daily data
    log.info("STEP 0: Fetching Daily Data from Public Sources")
    try:
        fetch_all_data(use_real_apis=True)
    except Exception as e:
        log.warning("Error fetching data: %s — continuing with existing files", e)

    # Step 1: Data ingestion
    weather_df, traffic_df, demand_df = run_data_ingestion()

    # Step 2: Feature engineering
    daily_features = run_feature_engineering(weather_df, traffic_df, demand_df)

    # Step 3: Rule-based risk scoring
    log.info("STEP 3: Risk Scoring and Alert Generation")
    risk_df, alerts_df = run_risk_engine('data/processed/daily_city_features.csv', 'outputs')

    # Step 4: ML anomaly detection
    risk_df = run_anomaly_detection(risk_df, 'outputs')

    # Step 5: Next-day forecasting
    forecast_df = run_forecasting(risk_df, 'outputs')

    # Summary
    log.info("=" * 55)
    log.info("PIPELINE COMPLETE")
    log.info("=" * 55)

    latest_date = risk_df['date'].max()
    latest = risk_df[risk_df['date'] == latest_date]
    dist = latest['risk_classification'].value_counts().to_dict()
    log.info("Risk distribution %s: High=%d  Medium=%d  Low=%d",
             latest_date.date(),
             dist.get('High', 0), dist.get('Medium', 0), dist.get('Low', 0))

    if len(alerts_df) > 0:
        log.info("%d high-risk alert(s):", len(alerts_df))
        for _, row in alerts_df.iterrows():
            log.info("  [ALERT] %s  score=%.1f  %s", row['city'], row['risk_score'], row.get('alert_reason', ''))
    else:
        log.info("No high-risk alerts today.")

    log.info("Outputs: outputs/daily_city_risk.csv, alerts_today.csv, forecast_tomorrow.csv")


if __name__ == '__main__':
    main()

