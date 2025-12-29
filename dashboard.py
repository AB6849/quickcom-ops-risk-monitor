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
import time

# Page configuration
st.set_page_config(
    page_title="Quick-Commerce Risk Monitor",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .high-risk {
        color: #d62728;
        font-weight: bold;
    }
    .medium-risk {
        color: #ff7f0e;
        font-weight: bold;
    }
    .low-risk {
        color: #2ca02c;
        font-weight: bold;
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
    # Header
    st.markdown('<h1 class="main-header">India Quick-Commerce Operational Risk Monitor</h1>', unsafe_allow_html=True)
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
    
    # Key Metrics Row
    st.header("Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_cities = len(filtered_df)
    high_risk = len(filtered_df[filtered_df['risk_classification'] == 'High'])
    medium_risk = len(filtered_df[filtered_df['risk_classification'] == 'Medium'])
    low_risk = len(filtered_df[filtered_df['risk_classification'] == 'Low'])
    avg_risk_score = filtered_df['risk_score'].mean()
    
    with col1:
        st.metric("Total Cities", total_cities)
    with col2:
        st.metric("High Risk", high_risk, delta=None)
    with col3:
        st.metric("Medium Risk", medium_risk, delta=None)
    with col4:
        st.metric("Low Risk", low_risk, delta=None)
    with col5:
        st.metric("Avg Risk Score", f"{avg_risk_score:.1f}", delta=None)
    
    st.markdown("---")
    
    # Alerts Section
    if len(alerts_df) > 0:
        st.header("High-Risk Alerts")
        
        alert_cols = st.columns(len(alerts_df))
        for idx, (_, alert) in enumerate(alerts_df.iterrows()):
            with alert_cols[idx % len(alert_cols)]:
                st.error(f"**{alert['city']}**")
                st.write(f"Risk Score: **{alert['risk_score']:.1f}**")
                st.caption(alert.get('alert_reason', 'Multiple risk factors'))
        
        st.markdown("---")
    
    # Main Content - Two Columns
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Risk Score by City (Bar Chart)
        st.subheader("Risk Scores by City")
        
        if len(filtered_df) > 0:
            # Sort by risk score
            chart_df = filtered_df.sort_values('risk_score', ascending=True)
            
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
                    hovertemplate='<b>%{y}</b><br>Risk Score: %{x:.1f}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                xaxis_title="Risk Score",
                yaxis_title="City",
                height=400,
                showlegend=False,
                xaxis_range=[0, 100]
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for selected filters.")
    
    with col_right:
        # Risk Distribution (Pie Chart)
        st.subheader("Risk Distribution")
        
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
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for selected filters.")
    
    st.markdown("---")
    
    # Risk Components Analysis
    st.header("Risk Components Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Component Comparison
        st.subheader("Average Risk by Component")
        
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
        st.subheader("Risk Trend (Last 7 Days)")
        
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
    st.header("Detailed Risk Scores")
    
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

