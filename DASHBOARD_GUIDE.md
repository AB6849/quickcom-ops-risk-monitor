# Streamlit Dashboard Guide

A professional, interview-ready dashboard for the India Quick-Commerce Operational Risk Monitor.

## Features

 **Interactive Visualizations**
- Risk scores by city (bar charts)
- Risk distribution (pie charts)
- Risk trends over time (line charts)
- Component analysis (traffic, weather, demand)

 **Real-time Metrics**
- Total cities monitored
- High/Medium/Low risk counts
- Average risk score
- High-risk alerts

 **Daily Refresh**
- Automatic data refresh
- Manual refresh button
- Date selector for historical views

 **Professional Design**
- Clean, modern UI
- Color-coded risk levels
- Responsive layout
- Export capabilities

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- pandas, numpy (data processing)
- streamlit (dashboard framework)
- plotly (interactive charts)

### 2. Generate Data (First Time)

```bash
python run_pipeline.py
```

This creates the output files that the dashboard reads.

### 3. Launch Dashboard

```bash
# Option 1: Direct command
streamlit run dashboard.py

# Option 2: Using the script
chmod +x run_dashboard.sh
./run_dashboard.sh

# Option 3: With custom port
streamlit run dashboard.py --server.port 8502
```

The dashboard will automatically open in your browser at `http://localhost:8501`

## Daily Refresh Workflow

### For Interviews/Demonstrations

1. **Morning Routine** (9:00 AM):
   ```bash
   # 1. Run pipeline with latest data
   python run_pipeline.py
   
   # 2. Launch dashboard
   streamlit run dashboard.py
   ```

2. **Dashboard Auto-Refresh**:
   - Data is cached for 1 hour
   - Click " Refresh Dashboard" button in sidebar to see latest data
   - Or restart the dashboard after running pipeline

3. **For Live Demo**:
   - Keep dashboard running
   - Run pipeline in another terminal
   - Click refresh button in dashboard

### Automated Daily Refresh (Optional)

Create a cron job or scheduled task:

```bash
# Add to crontab (runs daily at 9 AM)
0 9 * * * cd /path/to/quickcom-ops-risk-monitor && python run_pipeline.py
```

## Dashboard Sections

### 1. Key Metrics
- Total cities monitored
- Risk level distribution (High/Medium/Low)
- Average risk score

### 2. High-Risk Alerts
- Prominent display of cities requiring immediate attention
- Risk score and reason for alert

### 3. Risk Scores by City
- Horizontal bar chart
- Color-coded by risk level
- Sorted by risk score

### 4. Risk Distribution
- Pie chart showing proportion of cities in each risk category

### 5. Risk Components Analysis
- Average risk by component (traffic, weather, demand)
- 7-day trend visualization

### 6. Detailed Table
- Complete risk scores for all cities
- Sortable and filterable
- Export to CSV

## Sidebar Controls

- **Date Selector**: View historical data or latest date
- **City Filter**: Select specific cities to analyze
- **Risk Level Filter**: Filter by Low/Medium/High
- **Refresh Button**: Manually refresh data

## Interview Tips

### Before the Interview

1. **Prepare Data**:
   ```bash
   # Ensure you have recent data
   python run_pipeline.py
   ```

2. **Test Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```
   - Verify all visualizations load
   - Check that alerts are displayed
   - Test filters and interactions

3. **Prepare Talking Points**:
   - Explain the risk scoring logic
   - Discuss how operations teams use this
   - Show how to interpret the visualizations
   - Demonstrate the refresh capability

### During the Interview

1. **Start with Overview**:
   - Show key metrics
   - Highlight high-risk alerts
   - Explain the risk classification

2. **Demonstrate Interactivity**:
   - Use date selector to show historical trends
   - Filter by cities
   - Show risk component breakdown

3. **Explain Use Cases**:
   - How ops teams use this daily
   - Resource allocation decisions
   - SLA management
   - Proactive risk mitigation

4. **Show Technical Details**:
   - Explain the data pipeline
   - Discuss the risk scoring algorithm
   - Show how to refresh data

## Customization

### Change Colors

Edit `dashboard.py` and modify the color mappings:

```python
color_discrete_map={
    'High': '#d62728',    # Red
    'Medium': '#ff7f0e',  # Orange
    'Low': '#2ca02c'      # Green
}
```

### Add More Metrics

Add new metrics in the "Key Metrics" section:

```python
with col6:
    st.metric("New Metric", value)
```

### Modify Charts

All charts use Plotly, so you can customize:
- Chart types
- Colors
- Annotations
- Hover information

## Troubleshooting

### Dashboard Shows "No Data"

**Solution**: Run the pipeline first:
```bash
python run_pipeline.py
```

### Charts Not Displaying

**Solution**: Check that plotly is installed:
```bash
pip install plotly
```

### Dashboard Won't Start

**Solution**: Check port availability:
```bash
# Use different port
streamlit run dashboard.py --server.port 8502
```

### Data Not Refreshing

**Solution**: 
1. Clear cache: Click " Refresh Dashboard"
2. Or restart dashboard after running pipeline

## Performance

- **Data Caching**: 1 hour cache for fast loading
- **Large Datasets**: Handles 100+ cities efficiently
- **Real-time Updates**: Instant refresh on button click

## Deployment Options

### Local Development
```bash
streamlit run dashboard.py
```

### Cloud Deployment (Streamlit Cloud)
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy automatically

### Docker (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "dashboard.py"]
```

## Best Practices

1. **Always run pipeline before demo**
2. **Test dashboard before interview**
3. **Have backup screenshots ready**
4. **Explain the business value, not just technical details**
5. **Show how it integrates with operations workflow**

## Next Steps

- Add more visualizations (heatmaps, geographic maps)
- Integrate with real-time data APIs
- Add user authentication
- Create mobile-responsive version
- Add alert notifications

## Support

For issues or questions:
- Check `HOW_TO_VIEW_OUTPUTS.md` for data pipeline help
- Review Streamlit documentation: https://docs.streamlit.io
- Check Plotly documentation: https://plotly.com/python

