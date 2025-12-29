#!/usr/bin/env python3
"""
Main execution script for India Quick-Commerce Operational Risk Monitor

This script runs the complete pipeline:
1. Fetch daily data from public APIs (refreshes daily)
2. Data ingestion and cleaning
3. Feature engineering
4. Risk scoring and alert generation

Usage:
    python run_pipeline.py

For daily automated runs, set up cron job or scheduled task.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from risk_engine import run_risk_engine
from data_fetcher import fetch_all_data


def run_data_ingestion():
    """Run data ingestion and cleaning."""
    print("=" * 60)
    print("STEP 1: Data Ingestion and Cleaning")
    print("=" * 60)
    
    raw_data_dir = Path('data/raw')
    processed_data_dir = Path('data/processed')
    processed_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Load raw data
    print("\nLoading raw data...")
    weather_df = pd.read_csv(raw_data_dir / 'weather_india.csv')
    traffic_df = pd.read_csv(raw_data_dir / 'traffic_india.csv')
    demand_df = pd.read_csv(raw_data_dir / 'demand_india.csv')
    
    print(f"  - Weather: {weather_df.shape}")
    print(f"  - Traffic: {traffic_df.shape}")
    print(f"  - Demand: {demand_df.shape}")
    
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
    
    print("\n[OK] Data ingestion complete!")
    print(f"  Cleaned data saved to: {processed_data_dir}")
    
    return weather_df, traffic_df, demand_df


def run_feature_engineering(weather_df, traffic_df, demand_df):
    """Run feature engineering."""
    print("\n" + "=" * 60)
    print("STEP 2: Feature Engineering")
    print("=" * 60)
    
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
    
    print("\nCreating rolling 7-day features...")
    traffic_df = create_rolling_features(traffic_df, 'congestion_level', window=7)
    weather_df = create_rolling_features(weather_df, 'rainfall_mm', window=7)
    demand_df = create_rolling_features(demand_df, 'demand_index', window=7)
    print("[OK] Rolling features created")
    
    # Merge datasets
    print("\nMerging datasets...")
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
    
    print(f"[OK] Feature engineering complete!")
    print(f"  Feature table saved to: {output_path}")
    print(f"  Total records: {len(daily_features)}")
    print(f"  Date range: {daily_features['date'].min().date()} to {daily_features['date'].max().date()}")
    print(f"  Unique cities: {daily_features['city'].nunique()}")
    
    return daily_features


def main():
    """Main execution function."""
    print("\n" + "=" * 60)
    print("India Quick-Commerce Operational Risk Monitor")
    print("=" * 60)
    
    # Step 0: Fetch daily data from public APIs
    print("\n" + "=" * 60)
    print("STEP 0: Fetching Daily Data from Public Sources")
    print("=" * 60)
    try:
        fetch_all_data(use_real_apis=True)
    except Exception as e:
        print(f"[WARNING] Error fetching data: {e}")
        print("   Continuing with existing data files...")
    
    # Step 1: Data ingestion
    weather_df, traffic_df, demand_df = run_data_ingestion()
    
    # Step 2: Feature engineering
    daily_features = run_feature_engineering(weather_df, traffic_df, demand_df)
    
    # Step 3: Risk scoring
    print("\n" + "=" * 60)
    print("STEP 3: Risk Scoring and Alert Generation")
    print("=" * 60)
    
    features_path = 'data/processed/daily_city_features.csv'
    output_dir = 'outputs'
    
    risk_df, alerts_df = run_risk_engine(features_path, output_dir)
    
    # Print summary
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)
    
    latest_date = risk_df['date'].max()
    latest_risk = risk_df[risk_df['date'] == latest_date]
    
    print(f"\nRisk distribution for {latest_date.date()}:")
    print(latest_risk['risk_classification'].value_counts().to_string())
    
    if len(alerts_df) > 0:
        print(f"\n[ALERT] {len(alerts_df)} High-Risk Alert(s) Generated:")
        print("\n" + alerts_df[['city', 'risk_score', 'alert_reason']].to_string(index=False))
    else:
        print("\n[OK] No high-risk alerts today.")
    
    print(f"\nOutput files:")
    print(f"  - outputs/daily_city_risk.csv")
    print(f"  - outputs/alerts_today.csv")


if __name__ == '__main__':
    main()

