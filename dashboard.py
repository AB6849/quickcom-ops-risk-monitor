"""
Streamlit Dashboard for India Quick-Commerce Operational Risk Monitor

A professional dashboard for displaying operational risk scores and alerts.
Perfect for interview demonstrations.

Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime, timedelta
import sys
import time

# Page configuration
st.set_page_config(
    page_title="Quick-Commerce Risk Monitor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for modern, wow-inducing design
st.markdown("""
    <style>
    /* Main Header with Gradient */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    
    /* Metric Cards with Glassmorphism */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* High Risk Styling */
    .high-risk {
        color: #ff1744;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(255, 23, 68, 0.3);
    }
    
    /* Medium Risk Styling */
    .medium-risk {
        color: #ff9800;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(255, 152, 0, 0.3);
    }
    
    /* Low Risk Styling */
    .low-risk {
        color: #4caf50;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(76, 175, 80, 0.3);
    }
    
    /* Alert Cards */
    .alert-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        border-radius: 1rem;
        padding: 1.5rem;
        color: white;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .alert-card:hover {
        transform: scale(1.02);
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.5);
    }
    
    /* Section Headers */
    h2, h3 {
        color: #2c3e50;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Chart Container */
    .chart-container {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Metric Value Styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Info Boxes */
    .stInfo {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border-left: 4px solid #667eea;
        border-radius: 0.5rem;
    }
    
    /* Main Container Background */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load data function
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_risk_data():
    """Load risk data from CSV files."""
    risk_file = Path('outputs/daily_city_risk.csv')
    alerts_file = Path('outputs/alerts_today.csv')
    
    if not risk_file.exists():
        # Try to generate data if it doesn't exist (for Streamlit Cloud)
        # This allows the dashboard to work even without pre-committed data
        try:
            import subprocess
            with st.spinner("Generating data... This may take 1-2 minutes on first load."):
                result = subprocess.run(
                    [sys.executable, 'run_pipeline.py'], 
                    capture_output=True, 
                    text=True, 
                    timeout=180,
                    cwd=Path(__file__).parent
                )
                if result.returncode == 0 and risk_file.exists():
                    st.success("Data generated successfully! Refreshing...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Data generation failed. Please ensure all dependencies are installed.")
                    if result.stderr:
                        st.code(result.stderr[:500])  # Show first 500 chars of error
        except subprocess.TimeoutExpired:
            st.error("Data generation timed out. Please commit sample data to repository.")
        except Exception as e:
            st.warning(f"Could not auto-generate data: {e}")
            st.info("Tip: Commit sample data files to repository for faster loading.")
        return None, None
    
    risk_df = pd.read_csv(risk_file, parse_dates=['date'])
    alerts_df = pd.read_csv(alerts_file, parse_dates=['date']) if alerts_file.exists() else pd.DataFrame()
    
    return risk_df, alerts_df

# Main dashboard
def main():
    # Header with enhanced design
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 class="main-header">India Quick-Commerce Operational Risk Monitor</h1>
            <p style="color: #7f8c8d; font-size: 1.2rem; margin-top: -1rem;">
                Real-time operational risk monitoring across 162+ Indian cities
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data
    risk_df, alerts_df = load_risk_data()
    
    if risk_df is None:
        st.error("Output files not found! Please run the pipeline first:")
        st.code("python run_pipeline.py", language="bash")
        st.info("The dashboard will automatically refresh once data is available.")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("Dashboard Controls")
        
        # Date selector
        available_dates = sorted(risk_df['date'].unique(), reverse=True)
        selected_date = st.selectbox(
            "Select Date",
            available_dates,
            index=0,
            format_func=lambda x: x.strftime('%Y-%m-%d')
        )
        
        # City filter
        all_cities = sorted(risk_df['city'].unique())
        selected_cities = st.multiselect(
            "Filter Cities",
            all_cities,
            default=all_cities
        )
        
        # Risk level filter
        risk_levels = st.multiselect(
            "Filter Risk Levels",
            ['Low', 'Medium', 'High'],
            default=['Low', 'Medium', 'High']
        )
        
        st.markdown("---")
        st.header("Refresh Data")
        if st.button("Refresh Dashboard", type="primary"):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.info("**Tip**: Click 'Refresh Dashboard' after running the pipeline to see latest data.")
    
    # Filter data
    filtered_df = risk_df[
        (risk_df['date'] == selected_date) &
        (risk_df['city'].isin(selected_cities)) &
        (risk_df['risk_classification'].isin(risk_levels))
    ].copy()
    
    # Key Metrics Row with Enhanced Styling
    st.markdown("### 📊 Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_cities = len(filtered_df)
    high_risk = len(filtered_df[filtered_df['risk_classification'] == 'High'])
    medium_risk = len(filtered_df[filtered_df['risk_classification'] == 'Medium'])
    low_risk = len(filtered_df[filtered_df['risk_classification'] == 'Low'])
    avg_risk_score = filtered_df['risk_score'].mean()
    
    with col1:
        st.metric(
            "Total Cities", 
            total_cities,
            help="Total number of cities being monitored"
        )
    with col2:
        st.metric(
            "High Risk", 
            high_risk, 
            delta=None,
            delta_color="inverse",
            help="Cities requiring immediate attention"
        )
    with col3:
        st.metric(
            "Medium Risk", 
            medium_risk, 
            delta=None,
            help="Cities needing monitoring"
        )
    with col4:
        st.metric(
            "Low Risk", 
            low_risk, 
            delta=None,
            help="Cities operating normally"
        )
    with col5:
        st.metric(
            "Avg Risk Score", 
            f"{avg_risk_score:.1f}", 
            delta=None,
            help="Average risk score across all cities"
        )
    
    st.markdown("---")
    
    # Alerts Section - Filter by selected date
    # Get high-risk cities for the selected date
    date_alerts = filtered_df[filtered_df['risk_classification'] == 'High'].copy()
    
    # If we have alerts from the alerts file for this date, use those (they have alert_reason)
    if len(alerts_df) > 0:
        alerts_for_date = alerts_df[alerts_df['date'] == selected_date].copy()
        if len(alerts_for_date) > 0:
            # Use alerts from file (has alert_reason)
            date_alerts = alerts_for_date.copy()
        else:
            # Generate alert reasons from filtered data
            if len(date_alerts) > 0:
                date_alerts['alert_reason'] = date_alerts.apply(
                    lambda row: f"High traffic congestion ({row.get('traffic_risk', 0):.2f}); "
                               f"Heavy rainfall ({row.get('weather_risk', 0):.1f}mm); "
                               f"Demand surge ({row.get('demand_risk', 0):.2f})" 
                               if 'traffic_risk' in row else "Multiple risk factors",
                    axis=1
                )
    
    # Display alerts for selected date with Enhanced Design
    if len(date_alerts) > 0:
        st.markdown("### 🚨 High-Risk Alerts")
        
        # Sort by risk score (highest first)
        date_alerts = date_alerts.sort_values('risk_score', ascending=False)
        
        # Create columns for alerts (max 3 per row for better visibility)
        num_alerts = len(date_alerts)
        cols_per_row = min(3, num_alerts)
        num_rows = (num_alerts + cols_per_row - 1) // cols_per_row
        
        for row in range(num_rows):
            alert_cols = st.columns(cols_per_row)
            for col_idx in range(cols_per_row):
                alert_idx = row * cols_per_row + col_idx
                if alert_idx < num_alerts:
                    alert = date_alerts.iloc[alert_idx]
                    with alert_cols[col_idx]:
                        # Custom alert card with gradient
                        st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
                                border-radius: 1rem;
                                padding: 1.5rem;
                                color: white;
                                box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
                                margin-bottom: 1rem;
                            ">
                                <h3 style="color: white; margin: 0 0 0.5rem 0; font-size: 1.5rem;">{alert['city']}</h3>
                                <p style="color: white; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">{alert['risk_score']:.1f}</p>
                                <p style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem; margin: 0.5rem 0 0 0;">{alert.get('alert_reason', 'Multiple risk factors')}</p>
                            </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Main Content - Two Columns
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Risk Score by City (Bar Chart) - Top 20
        st.markdown("### 📈 Top 20 Cities by Risk Score")
        
        if len(filtered_df) > 0:
            # Sort by risk score (highest first) and take top 20
            chart_df = filtered_df.sort_values('risk_score', ascending=False).head(20)
            # Reverse for display (highest at top in horizontal bar)
            chart_df = chart_df.sort_values('risk_score', ascending=True)
            
            # Create color mapping
            colors = []
            for risk in chart_df['risk_classification']:
                if risk == 'High':
                    colors.append('#d62728')
                elif risk == 'Medium':
                    colors.append('#ff7f0e')
                else:
                    colors.append('#2ca02c')
            
            fig = go.Figure(data=[
                go.Bar(
                    y=chart_df['city'],
                    x=chart_df['risk_score'],
                    orientation='h',
                    marker=dict(color=colors),
                    text=[f"{score:.1f}" for score in chart_df['risk_score']],
                    textposition='outside',
                    hovertemplate='<b>%{y}</b><br>Risk Score: %{x:.1f}<br>Classification: %{customdata}<extra></extra>',
                    customdata=chart_df['risk_classification']
                )
            ])
            
            # Fixed height for top 20 (20 cities * 30px = 600px)
            fig.update_layout(
                xaxis_title="Risk Score",
                yaxis_title="City",
                height=600,
                showlegend=False,
                xaxis_range=[0, 100],
                margin=dict(l=150, r=50, t=20, b=50),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Arial, sans-serif", size=12),
                xaxis=dict(
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    gridwidth=1,
                    showgrid=True
                ),
                yaxis=dict(
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    gridwidth=1,
                    showgrid=True
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show note about total cities
            if len(filtered_df) > 20:
                st.caption(f"Showing top 20 of {len(filtered_df)} cities. See full list in 'Detailed Risk Scores' table below.")
        else:
            st.info("No data available for selected filters.")
    
    with col_right:
        # Risk Distribution (Pie Chart)
        st.markdown("### 🥧 Risk Distribution")
        
        if len(filtered_df) > 0:
            risk_dist = filtered_df['risk_classification'].value_counts()
            
            fig = px.pie(
                values=risk_dist.values,
                names=risk_dist.index,
                color=risk_dist.index,
                color_discrete_map={
                    'High': '#d62728',
                    'Medium': '#ff7f0e',
                    'Low': '#2ca02c'
                }
            )
            
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
                marker=dict(line=dict(color='#FFFFFF', width=2))
            )
            
            fig.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05,
                    font=dict(size=12)
                ),
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Arial, sans-serif", size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for selected filters.")
    
    st.markdown("---")
    
    # Risk Components Analysis
    st.markdown("### 🔍 Risk Components Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Component Comparison
        st.markdown("### 📊 Average Risk by Component")
        
        if len(filtered_df) > 0:
            components = ['traffic_risk', 'weather_risk', 'demand_risk']
            component_names = ['Traffic', 'Weather', 'Demand']
            avg_risks = [filtered_df[comp].mean() for comp in components]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=component_names,
                    y=avg_risks,
                    marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                    text=[f"{val:.1f}" for val in avg_risks],
                    textposition='outside'
                )
            ])
            
            fig.update_layout(
                yaxis_title="Average Risk Score",
                height=300,
                showlegend=False,
                yaxis_range=[0, 100]
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk Trend Over Time
        st.markdown("### 📉 Risk Trend (Last 7 Days)")
        
        # Get last 7 days of data
        trend_start = selected_date - timedelta(days=7)
        trend_df = risk_df[
            (risk_df['date'] >= trend_start) &
            (risk_df['date'] <= selected_date) &
            (risk_df['city'].isin(selected_cities))
        ]
        
        if len(trend_df) > 0:
            # Aggregate by date and risk classification
            trend_agg = trend_df.groupby(['date', 'risk_classification']).size().reset_index(name='count')
            
            # Ensure all risk levels are present (fill missing with 0)
            all_dates = sorted(trend_df['date'].unique())
            all_risk_levels = ['Low', 'Medium', 'High']
            
            # Create complete dataframe
            complete_data = []
            for date in all_dates:
                for risk_level in all_risk_levels:
                    count = trend_agg[
                        (trend_agg['date'] == date) & 
                        (trend_agg['risk_classification'] == risk_level)
                    ]['count'].values
                    complete_data.append({
                        'date': date,
                        'risk_classification': risk_level,
                        'count': count[0] if len(count) > 0 else 0
                    })
            
            trend_complete = pd.DataFrame(complete_data)
            
            fig = px.line(
                trend_complete,
                x='date',
                y='count',
                color='risk_classification',
                color_discrete_map={
                    'High': '#d62728',
                    'Medium': '#ff7f0e',
                    'Low': '#2ca02c'
                },
                markers=True,
                line_shape='linear'
            )
            
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Number of Cities",
                height=300,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(tickangle=-45)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No trend data available. Run pipeline to generate historical data.")
    
    st.markdown("---")
    
    # Detailed Table
    st.markdown("### 📋 Detailed Risk Scores")
    
    if len(filtered_df) > 0:
        # Prepare display columns
        display_cols = ['city', 'city_tier', 'risk_score', 'risk_classification',
                       'traffic_risk', 'weather_risk', 'demand_risk']
        display_cols = [col for col in display_cols if col in filtered_df.columns]
        
        display_df = filtered_df[display_cols].copy()
        display_df = display_df.sort_values('risk_score', ascending=False)
        
        # Format risk scores
        for col in ['risk_score', 'traffic_risk', 'weather_risk', 'demand_risk']:
            if col in display_df.columns:
                display_df[col] = display_df[col].round(1)
        
        # Style the dataframe
        def highlight_risk(row):
            if row['risk_classification'] == 'High':
                return ['background-color: #ffcccc'] * len(row)
            elif row['risk_classification'] == 'Medium':
                return ['background-color: #fff4cc'] * len(row)
            else:
                return ['background-color: #ccffcc'] * len(row)
        
        styled_df = display_df.style.apply(highlight_risk, axis=1)
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        # Download button
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name=f"risk_scores_{selected_date.strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No data available for selected filters.")
    
    st.markdown("---")
    
    # Data Freshness Indicator
    st.markdown("---")
    st.header("Data Freshness")
    
    col1, col2, col3 = st.columns(3)
    
    # Check when data was last updated
    risk_file = Path('outputs/daily_city_risk.csv')
    raw_weather = Path('data/raw/weather_india.csv')
    
    if risk_file.exists():
        risk_mtime = datetime.fromtimestamp(risk_file.stat().st_mtime)
        hours_old = (datetime.now() - risk_mtime).total_seconds() / 3600
        
        with col1:
            if hours_old < 24:
                st.success(f"Risk Data: {hours_old:.1f} hours old")
            elif hours_old < 48:
                st.warning(f"Risk Data: {hours_old:.1f} hours old")
            else:
                st.error(f"Risk Data: {hours_old:.1f} hours old")
            st.caption(f"Last updated: {risk_mtime.strftime('%Y-%m-%d %H:%M')}")
    
    if raw_weather.exists():
        weather_mtime = datetime.fromtimestamp(raw_weather.stat().st_mtime)
        hours_old = (datetime.now() - weather_mtime).total_seconds() / 3600
        
        with col2:
            if hours_old < 2:
                st.success(f"Weather Data: {hours_old:.1f} hours old")
            elif hours_old < 24:
                st.warning(f"Weather Data: {hours_old:.1f} hours old")
            else:
                st.error(f"Weather Data: {hours_old:.1f} hours old")
            st.caption(f"Last updated: {weather_mtime.strftime('%Y-%m-%d %H:%M')}")
    
    with col3:
        st.info("**Tip**: Run `python run_pipeline.py` to fetch latest data from APIs")
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>Dashboard refreshes automatically. Click 'Refresh Dashboard' in sidebar after running pipeline.</p>
        <p>Dashboard loaded: {}</p>
        <p>Data sources: Open-Meteo API (hourly), TomTom API (real-time)</p>
    </div>
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)

if __name__ == '__main__':
    main()

