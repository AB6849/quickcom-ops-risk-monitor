"""
Streamlit Dashboard for India Quick-Commerce Operational Risk Monitor

A professional dashboard for displaying operational risk scores and alerts.
Perfect for interview demonstrations.

Run with: streamlit run dashboard.py

Last updated: 2025-12-30
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime, timedelta
import sys
import time
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Quick-Commerce Risk Monitor",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for modern, wow-inducing design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Main App Background & Typography */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #080B11 !important;
        color: #E2E8F0 !important;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #171b2d 0%, #090d16 65%, #04060b 100%) !important;
    }
    
    /* Sidebar styling with glassmorphism */
    [data-testid="stSidebar"] {
        background-color: rgba(13, 17, 28, 0.75) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
        color: #FFFFFF !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        margin-top: 1rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 0.5rem;
    }
    
    /* Main Header with Gradient */
    .main-header {
        font-size: 2.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, #C084FC 0%, #6366F1 50%, #38BDF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        letter-spacing: -0.03em;
    }
    
    /* Section Headers */
    h2, h3, [data-testid="stMarkdownContainer"] h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #090d16;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.6);
    }
    
    /* Premium Button */
    .stButton > button {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 0.5rem !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.5) !important;
        background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    }
    
    /* Streamlit widgets tweaks */
    div[data-baseweb="select"] > div {
        background-color: rgba(17, 24, 39, 0.6) !important;
        border-color: rgba(255, 255, 255, 0.08) !important;
        color: #FFFFFF !important;
    }
    
    div[role="listbox"] {
        background-color: #0d111c !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    /* Info Box Overrides */
    .stInfo, div[data-testid="stNotification"] {
        background: rgba(99, 102, 241, 0.08) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-left: 4px solid #6366F1 !important;
        color: #E2E8F0 !important;
        border-radius: 0.5rem !important;
    }
    
    /* DataFrame Styling */
    div[data-testid="stDataFrame"] {
        background: rgba(17, 24, 39, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 0.75rem !important;
        padding: 0.5rem !important;
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
    
    # Helper to style Plotly charts with a premium SaaS theme
    def apply_premium_plotly_layout(fig, height=350):
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="'Plus Jakarta Sans', 'Outfit', sans-serif", size=12, color='#94A3B8'),
            margin=dict(l=50, r=20, t=30, b=45),
            height=height,
            xaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.05)',
                linecolor='rgba(255, 255, 255, 0.06)',
                zeroline=False,
                title_font=dict(size=11, color='#64748B'),
                tickfont=dict(color='#94A3B8')
            ),
            yaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.05)',
                linecolor='rgba(255, 255, 255, 0.06)',
                zeroline=False,
                title_font=dict(size=11, color='#64748B'),
                tickfont=dict(color='#94A3B8')
            ),
            legend=dict(
                bgcolor='rgba(15, 23, 42, 0.6)',
                bordercolor='rgba(255, 255, 255, 0.05)',
                borderwidth=1,
                font=dict(size=10, color='#94A3B8')
            )
        )
    
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
    st.markdown("### Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_cities = len(filtered_df)
    high_risk = len(filtered_df[filtered_df['risk_classification'] == 'High'])
    medium_risk = len(filtered_df[filtered_df['risk_classification'] == 'Medium'])
    low_risk = len(filtered_df[filtered_df['risk_classification'] == 'Low'])
    avg_risk_score = filtered_df['risk_score'].mean() if len(filtered_df) > 0 else 0.0
    
    def render_custom_metric(title, value, risk_class=None, suffix=""):
        accent_color = "#3B82F6"
        glow_shadow = "rgba(59, 130, 246, 0.15)"
        if risk_class == "High":
            accent_color = "#EF4444"
            glow_shadow = "rgba(239, 68, 68, 0.2)"
        elif risk_class == "Medium":
            accent_color = "#F59E0B"
            glow_shadow = "rgba(245, 158, 11, 0.2)"
        elif risk_class == "Low":
            accent_color = "#10B981"
            glow_shadow = "rgba(16, 185, 129, 0.2)"
        elif title == "Avg Risk Score":
            val_num = float(value)
            if val_num > 60:
                accent_color = "#EF4444"
                glow_shadow = "rgba(239, 68, 68, 0.2)"
            elif val_num > 30:
                accent_color = "#F59E0B"
                glow_shadow = "rgba(245, 158, 11, 0.2)"
            else:
                accent_color = "#10B981"
                glow_shadow = "rgba(16, 185, 129, 0.2)"

        st.markdown(f"""
            <div style="
                background: rgba(17, 24, 39, 0.5);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-top: 3px solid {accent_color};
                border-radius: 0.75rem;
                padding: 1.25rem;
                box-shadow: 0 4px 20px {glow_shadow};
                text-align: center;
                transition: all 0.3s ease;
                margin-bottom: 1rem;
            " class="metric-box">
                <div style="color: #94A3B8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">{title}</div>
                <div style="font-size: 2.25rem; font-weight: 800; color: #FFFFFF; text-shadow: 0 0 10px {glow_shadow};">{value}{suffix}</div>
            </div>
        """, unsafe_allow_html=True)

    with col1:
        render_custom_metric("Total Cities", total_cities)
    with col2:
        render_custom_metric("High Risk", high_risk, "High")
    with col3:
        render_custom_metric("Medium Risk", medium_risk, "Medium")
    with col4:
        render_custom_metric("Low Risk", low_risk, "Low")
    with col5:
        render_custom_metric("Avg Risk Score", f"{avg_risk_score:.1f}")
    
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
            # Generate alert reasons from filtered data using raw feature values
            if len(date_alerts) > 0:
                def _build_reason(row):
                    parts = []
                    if row.get('traffic_risk', 0) >= 60:
                        parts.append(f"High congestion ({row.get('congestion_level', 0):.2f})")
                    if row.get('weather_risk', 0) >= 60:
                        if row.get('rainfall_mm', 0) >= 15.0:
                            parts.append(f"Heavy rainfall ({row.get('rainfall_mm', 0):.1f}mm)")
                        if row.get('temperature', 25.0) >= 40.0 or row.get('temperature', 25.0) <= 10.0:
                            parts.append(f"Extreme temperature ({row.get('temperature', 0):.1f}°C)")
                        if not (row.get('rainfall_mm', 0) >= 15.0 or row.get('temperature', 25.0) >= 40.0 or row.get('temperature', 25.0) <= 10.0):
                            parts.append(f"Adverse weather")
                    if row.get('demand_risk', 0) >= 60:
                        parts.append(f"Demand surge ({row.get('demand_index', 0):.2f})")
                    return "; ".join(parts) if parts else "Multiple risk factors combined"
                date_alerts['alert_reason'] = date_alerts.apply(_build_reason, axis=1)
    
    # Display alerts for selected date with Enhanced Design
    if len(date_alerts) > 0:
        st.markdown("### High-Risk Alerts")
        
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
                                background: rgba(239, 68, 68, 0.08);
                                backdrop-filter: blur(12px);
                                -webkit-backdrop-filter: blur(12px);
                                border: 1px solid rgba(239, 68, 68, 0.25);
                                border-left: 5px solid #F43F5E;
                                border-radius: 0.75rem;
                                padding: 1.25rem;
                                box-shadow: 0 8px 24px -10px rgba(239, 68, 68, 0.3);
                                margin-bottom: 1rem;
                            " class="alert-box">
                                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                                    <h3 style="color: #FFFFFF; margin: 0; font-size: 1.3rem; font-weight: 700;">{alert['city']}</h3>
                                    <span style="background: #F43F5E; color: #FFFFFF; font-size: 0.75rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: 0.25rem; letter-spacing: 0.05em;">CRITICAL</span>
                                </div>
                                <div style="display: flex; align-items: baseline; margin-bottom: 0.75rem;">
                                    <span style="color: #F43F5E; font-size: 2rem; font-weight: 800; line-height: 1;">{alert['risk_score']:.1f}</span>
                                    <span style="color: #94A3B8; font-size: 0.8rem; margin-left: 0.5rem;">/ 100 Risk Score</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 0.5rem; color: #E2E8F0; font-size: 0.85rem; background: rgba(0,0,0,0.2); padding: 0.6rem; border-radius: 0.5rem;">
                                    <svg style="flex-shrink: 0; width: 14px; height: 14px; margin-top: 2px; fill: #F43F5E;" viewBox="0 0 24 24">
                                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                                    </svg>
                                    <span>{alert.get('alert_reason', 'Multiple risk factors')}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Main Content - Two Columns
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Risk Score by City (Bar Chart) - Top 20
        st.markdown("### Top 20 Cities by Risk Score")
        
        if len(filtered_df) > 0:
            # Sort by risk score (highest first) and take top 20
            chart_df = filtered_df.sort_values('risk_score', ascending=False).head(20)
            # Reverse for display (highest at top in horizontal bar)
            chart_df = chart_df.sort_values('risk_score', ascending=True)
            
            # Create color mapping
            colors = []
            for risk in chart_df['risk_classification']:
                if risk == 'High':
                    colors.append('#F43F5E')
                elif risk == 'Medium':
                    colors.append('#F59E0B')
                else:
                    colors.append('#10B981')
            
            fig = go.Figure(data=[
                go.Bar(
                    y=chart_df['city'],
                    x=chart_df['risk_score'],
                    orientation='h',
                    marker=dict(color=colors, line=dict(color='rgba(0,0,0,0)', width=0)),
                    text=[f" {score:.1f}" for score in chart_df['risk_score']],
                    textposition='outside',
                    hovertemplate='<b>%{y}</b><br>Risk Score: %{x:.1f}<br>Classification: %{customdata}<extra></extra>',
                    customdata=chart_df['risk_classification']
                )
            ])
            
            # Apply layout helper and customize
            apply_premium_plotly_layout(fig, height=600)
            fig.update_layout(
                xaxis_title="Risk Score",
                yaxis_title="City",
                showlegend=False,
                xaxis_range=[0, 107], # Extra padding for text labels
                margin=dict(l=110, r=20, t=10, b=40),
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show note about total cities
            if len(filtered_df) > 20:
                st.caption(f"Showing top 20 of {len(filtered_df)} cities. See full list in 'Detailed Risk Scores' table below.")
        else:
            st.info("No data available for selected filters.")
    
    with col_right:
        # Risk Distribution (Pie Chart)
        st.markdown("### Risk Distribution")
        
        if len(filtered_df) > 0:
            risk_dist = filtered_df['risk_classification'].value_counts()
            
            fig = px.pie(
                values=risk_dist.values,
                names=risk_dist.index,
                color=risk_dist.index,
                color_discrete_map={
                    'High': '#F43F5E',
                    'Medium': '#F59E0B',
                    'Low': '#10B981'
                },
                hole=0.6
            )
            
            fig.update_traces(
                textposition='outside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
                marker=dict(line=dict(color='rgba(255,255,255,0.08)', width=1.5))
            )
            
            apply_premium_plotly_layout(fig, height=400)
            fig.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5,
                ),
                margin=dict(l=20, r=20, t=10, b=80),
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for selected filters.")
    
    st.markdown("---")
    
    # Risk Components Analysis
    st.markdown("### Risk Components Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Component Comparison
        st.markdown("### Average Risk by Component")
        
        if len(filtered_df) > 0:
            components = ['traffic_risk', 'weather_risk', 'demand_risk']
            component_names = ['Traffic', 'Weather', 'Demand']
            avg_risks = [filtered_df[comp].mean() for comp in components]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=component_names,
                    y=avg_risks,
                    marker_color=['#6366F1', '#3B82F6', '#06B6D4'],
                    text=[f"{val:.1f}" for val in avg_risks],
                    textposition='outside'
                )
            ])
            
            apply_premium_plotly_layout(fig, height=300)
            fig.update_layout(
                yaxis_title="Average Risk Score",
                showlegend=False,
                yaxis_range=[0, 107]
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk Trend Over Time
        st.markdown("### Risk Trend (Last 7 Days)")
        
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
                    'High': '#F43F5E',
                    'Medium': '#F59E0B',
                    'Low': '#10B981'
                },
                markers=True,
                line_shape='spline'
            )
            
            fig.update_traces(line=dict(width=3))
            apply_premium_plotly_layout(fig, height=300)
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Number of Cities",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(tickangle=-45)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No trend data available. Run pipeline to generate historical data.")
    
    st.markdown("---")
    
    # Detailed Table
    st.markdown("### Detailed Risk Scores")
    
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
                return ['background-color: rgba(244, 63, 94, 0.12); color: #FFA3B1'] * len(row)
            elif row['risk_classification'] == 'Medium':
                return ['background-color: rgba(245, 158, 11, 0.12); color: #FFE0A3'] * len(row)
            else:
                return ['background-color: rgba(16, 185, 129, 0.12); color: #A3FFD6'] * len(row)
        
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

    # ── Anomaly Detection Results ────────────────────────────────────────────
    st.markdown("### ML Anomaly Detection")
    st.caption(
        "Cities flagged by IsolationForest as having an unusual combination "
        "of traffic, weather, and demand — even if no single factor breaches a threshold."
    )

    if 'is_anomaly' in filtered_df.columns:
        anomalies = filtered_df[filtered_df['is_anomaly']].sort_values('anomaly_score', ascending=False)
        if len(anomalies) > 0:
            display_anomaly_cols = [c for c in
                ['city', 'city_tier', 'anomaly_score', 'risk_score', 'risk_classification',
                 'traffic_risk', 'weather_risk', 'demand_risk']
                if c in anomalies.columns]
            anomaly_display = anomalies[display_anomaly_cols].copy()
            for col in ['anomaly_score', 'risk_score', 'traffic_risk', 'weather_risk', 'demand_risk']:
                if col in anomaly_display.columns:
                    anomaly_display[col] = anomaly_display[col].round(1)
            st.dataframe(anomaly_display, use_container_width=True)
            st.caption(f"{len(anomalies)} anomalous cities detected today (IsolationForest, contamination=5%)")
        else:
            st.success("No anomalous cities detected for the selected date/filters.")
    else:
        st.info("Anomaly scores not available — re-run the pipeline to generate them.")

    st.markdown("---")

    # ── Next-Day Risk Forecast ────────────────────────────────────────────────
    st.markdown("### Next-Day Risk Forecast")
    st.caption("Predicted risk scores for tomorrow using Exponentially Weighted Moving Average (EWMA, alpha=0.4).")

    forecast_file = Path('outputs/forecast_tomorrow.csv')
    if forecast_file.exists():
        forecast_df = pd.read_csv(forecast_file, parse_dates=['forecast_date'])

        # Filter to selected cities if any are chosen
        if selected_cities and len(selected_cities) < len(risk_df['city'].unique()):
            forecast_df = forecast_df[forecast_df['city'].isin(selected_cities)]

        col_f1, col_f2 = st.columns(2)

        with col_f1:
            # Top 15 forecast bar chart
            top_forecast = forecast_df.head(15).sort_values('forecast_risk', ascending=True)
            forecast_colors = []
            for cls in top_forecast['forecast_classification']:
                if cls == 'High':
                    forecast_colors.append('#F43F5E')
                elif cls == 'Medium':
                    forecast_colors.append('#F59E0B')
                else:
                    forecast_colors.append('#10B981')
 
            fig_f = go.Figure(data=[go.Bar(
                y=top_forecast['city'],
                x=top_forecast['forecast_risk'],
                orientation='h',
                marker=dict(color=forecast_colors, line=dict(color='rgba(0,0,0,0)', width=0)),
                text=[f" {s:.1f}" for s in top_forecast['forecast_risk']],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Forecast: %{x:.1f}<extra></extra>',
            )])
            apply_premium_plotly_layout(fig_f, height=450)
            fig_f.update_layout(
                xaxis_title="Forecast Risk Score",
                showlegend=False,
                xaxis_range=[0, 107], # Extra padding for text labels
                margin=dict(l=110, r=20, t=10, b=40),
            )
            st.markdown("**Top 15 Cities — Tomorrow's Forecast**")
            st.plotly_chart(fig_f, use_container_width=True)

        with col_f2:
            # Trend table: worsening cities
            trend_cols = [c for c in ['city', 'forecast_risk', 'forecast_classification', 'trend']
                          if c in forecast_df.columns]
            trend_display = forecast_df[trend_cols].copy()
            if 'trend' in trend_display.columns:
                trend_display = trend_display.sort_values('trend', ascending=False)
                trend_display['trend'] = trend_display['trend'].apply(
                    lambda t: f"+{t:.1f} (worsening)" if t > 1 else (f"{t:.1f} (improving)" if t < -1 else f"{t:.1f} (stable)")
                )
            st.markdown("**Full Forecast Table**")
            st.dataframe(trend_display, use_container_width=True, height=450)

        next_date = forecast_df['forecast_date'].iloc[0].strftime('%Y-%m-%d') if len(forecast_df) else 'N/A'
        high_count = (forecast_df['forecast_classification'] == 'High').sum()
        st.caption(f"Forecast date: {next_date}  |  Cities predicted High risk: {high_count}")
    else:
        st.info("Forecast not available — re-run the pipeline to generate `outputs/forecast_tomorrow.csv`.")

    st.markdown("---")

    # ── Data Freshness Indicator ──────────────────────────────────────────────
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

