# Quick Start Guide - Interview Dashboard

## Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Up Daily Data (Optional but Recommended)
For **real, daily-updated data** from public APIs:

```bash
# Get free OpenWeatherMap API key: https://openweathermap.org/api
export OPENWEATHER_API_KEY='your_api_key_here'

# Optional: TomTom Traffic API key
export TOMTOM_API_KEY='your_api_key_here'
```

**See `API_SETUP.md` for detailed instructions.**

### Step 3: Generate Data & Launch Dashboard

**macOS/Linux** (use `python3`):
```bash
# Generate data (fetches from APIs if keys are set)
python3 run_pipeline.py

# Launch dashboard
streamlit run dashboard.py
```

**Or use the convenience script**:
```bash
./run pipeline    # Run pipeline
./run dashboard   # Launch dashboard
./run view        # View outputs
```

**Windows** (use `python`):
```bash
python run_pipeline.py
streamlit run dashboard.py
```

The dashboard will automatically open in your browser!

**Note**: The pipeline automatically fetches daily data from public APIs when API keys are set.

## What You'll See

- **Key Metrics**: Total cities, risk distribution, average scores
- **High-Risk Alerts**: Cities requiring immediate attention
- **Interactive Charts**: Risk scores, distribution, trends
- **Detailed Table**: Complete risk scores with filters
- **Export Options**: Download data as CSV

## Daily Refresh

1. Run pipeline: `python run_pipeline.py`
2. Click "Refresh Dashboard" in sidebar
3. Or restart dashboard to see latest data

## Interview Tips

1. **Before Interview**: Test dashboard, prepare talking points
2. **During Demo**: Show interactivity, explain business value
3. **Key Points**: Risk scoring logic, operations use cases, refresh capability

## Full Documentation

- `DASHBOARD_GUIDE.md` - Complete dashboard documentation
- `HOW_TO_VIEW_OUTPUTS.md` - CLI output viewing
- `README.md` - System overview

## Troubleshooting

**Dashboard shows "No Data"**
→ Run `python run_pipeline.py` first

**Charts not displaying**
→ Install plotly: `pip install plotly`

**Port already in use**
→ Use different port: `streamlit run dashboard.py --server.port 8502`

