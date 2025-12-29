#!/usr/bin/env python3
"""
Simple script to view the outputs of the risk monitoring system.

This shows:
1. Daily risk scores for all cities
2. High-risk alerts for today
"""

import pandas as pd
from pathlib import Path

def view_outputs():
    """Display the output files."""
    
    outputs_dir = Path('outputs')
    
    print("=" * 70)
    print("India Quick-Commerce Operational Risk Monitor - Output Viewer")
    print("=" * 70)
    
    # Check if outputs exist
    risk_file = outputs_dir / 'daily_city_risk.csv'
    alerts_file = outputs_dir / 'alerts_today.csv'
    
    if not risk_file.exists():
        print("\n[ERROR] Output files not found!")
        print("\nTo generate outputs, run:")
        print("  python run_pipeline.py")
        print("\nOr install dependencies first:")
        print("  pip install pandas numpy")
        return
    
    # Load and display risk scores
    print("\n" + "=" * 70)
    print("1. DAILY CITY RISK SCORES")
    print("=" * 70)
    
    risk_df = pd.read_csv(risk_file, parse_dates=['date'])
    
    # Show latest date
    latest_date = risk_df['date'].max()
    latest_risk = risk_df[risk_df['date'] == latest_date].copy()
    
    print(f"\nLatest Date: {latest_date.strftime('%Y-%m-%d')}")
    print(f"Total Records: {len(risk_df)}")
    print(f"Cities Monitored: {risk_df['city'].nunique()}")
    
    # Risk distribution
    print("\nRisk Distribution (Latest Date):")
    risk_dist = latest_risk['risk_classification'].value_counts()
    for risk_level, count in risk_dist.items():
        print(f"   {risk_level}: {count} cities")
    
    # Show top cities by risk
    print("\nTop 10 Cities by Risk Score (Latest Date):")
    top_risks = latest_risk.nlargest(10, 'risk_score')[
        ['city', 'risk_score', 'risk_classification', 'traffic_risk', 'weather_risk', 'demand_risk']
    ]
    print(top_risks.to_string(index=False))
    
    # Show all cities for latest date
    print("\nAll Cities - Latest Risk Scores:")
    display_cols = ['city', 'city_tier', 'risk_score', 'risk_classification', 
                    'traffic_risk', 'weather_risk', 'demand_risk']
    display_cols = [col for col in display_cols if col in latest_risk.columns]
    print(latest_risk[display_cols].to_string(index=False))
    
    # Load and display alerts
    print("\n" + "=" * 70)
    print("2. HIGH-RISK ALERTS (Today)")
    print("=" * 70)
    
    if alerts_file.exists():
        alerts_df = pd.read_csv(alerts_file, parse_dates=['date'])
        
        if len(alerts_df) > 0:
            print(f"\n[ALERT] {len(alerts_df)} High-Risk Alert(s) Generated:")
            print("\n" + alerts_df[['city', 'risk_score', 'alert_reason']].to_string(index=False))
            
            print("\nRecommended Actions:")
            for _, alert in alerts_df.iterrows():
                print(f"\n   {alert['city']} (Risk Score: {alert['risk_score']:.1f})")
                print(f"      Reason: {alert['alert_reason']}")
                print(f"      -> Deploy additional delivery partners")
                print(f"      -> Extend delivery SLA expectations")
                print(f"      -> Activate backup resources")
        else:
            print("\n[OK] No high-risk alerts today!")
            print("   All cities are operating within acceptable risk levels.")
    else:
        print("\n[WARNING] Alerts file not found. Run the pipeline to generate alerts.")
    
    # Show historical trends
    print("\n" + "=" * 70)
    print("3. HISTORICAL TRENDS")
    print("=" * 70)
    
    # Risk trends over time
    risk_trends = risk_df.groupby(['date', 'risk_classification']).size().unstack(fill_value=0)
    print("\nRisk Classification Trends (Last 7 Days):")
    print(risk_trends.tail(7).to_string())
    
    # Average risk by city
    print("\nAverage Risk Score by City (All Time):")
    avg_risk = risk_df.groupby('city')['risk_score'].mean().sort_values(ascending=False)
    for city, avg in avg_risk.items():
        print(f"   {city}: {avg:.1f}")
    
    print("\n" + "=" * 70)
    print("[OK] Output viewing complete!")
    print("=" * 70)
    print(f"\nOutput files location: {outputs_dir.absolute()}")
    print(f"   - daily_city_risk.csv: Full risk scores for all cities and dates")
    print(f"   - alerts_today.csv: High-risk alerts for latest date")


if __name__ == '__main__':
    try:
        view_outputs()
    except ImportError:
        print("[ERROR] pandas not installed. Install with: pip install pandas numpy")
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()

