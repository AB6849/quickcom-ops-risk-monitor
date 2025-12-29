# Daily Data Refresh System

## Overview

The system is designed to fetch **authentic, daily-updated data** from public APIs, ensuring your dashboard always shows live, current information.

## Data Sources (All Refresh Daily)

### 1. Weather Data 
- **Source**: Open-Meteo API
- **Update Frequency**: **Hourly** (real-time)
- **Cost**: **COMPLETELY FREE** (no API key needed!)
- **Setup**: **No setup required** - works automatically!
- **Fallback**: Realistic patterns based on IMD climate data

### 2. Traffic Data 
- **Source**: TomTom Traffic API (optional)
- **Update Frequency**: **Real-time**
- **Free Tier**: 2,500 requests/day
- **Setup**: Set `TOMTOM_API_KEY` environment variable (optional)
- **Fallback**: Patterns based on TomTom Traffic Index (public data)

### 3. Demand Data 
- **Source**: Proxy metrics (public sources)
- **Update Frequency**: **Daily** (based on day of week, season)
- **Based on**: Population density, economic indicators, e-commerce patterns
- **Note**: Real demand data is proprietary; uses public metrics

## How It Works

### Automatic Daily Refresh

1. **Pipeline Integration**: The `run_pipeline.py` script automatically fetches data before processing
2. **API Calls**: Fetches latest data from OpenWeatherMap and TomTom APIs
3. **Data Processing**: Cleans, processes, and computes risk scores
4. **Dashboard Update**: Dashboard shows latest data on refresh

### Manual Refresh

```bash
# Run pipeline (fetches + processes)
python run_pipeline.py

# Dashboard will show latest data
streamlit run dashboard.py
```

### Automated Daily Refresh (Recommended)

Set up a cron job or scheduled task to run daily:

```bash
# macOS/Linux: Add to crontab
0 9 * * * cd /path/to/quickcom-ops-risk-monitor && python run_pipeline.py

# Or use the daily refresh script
./daily_refresh.sh
```

## Data Freshness Indicators

The dashboard shows:
-  **Fresh** (< 24 hours): Green indicator
-  **Stale** (24-48 hours): Yellow warning
-  **Outdated** (> 48 hours): Red alert

## API Setup

### Quick Setup (5 minutes)

1. **Get OpenWeatherMap API Key**:
   - Visit: https://openweathermap.org/api
   - Sign up (free)
   - Get API key from dashboard

2. **Set Environment Variable**:
   ```bash
   export OPENWEATHER_API_KEY='your_key_here'
   ```

3. **Test**:
   ```bash
   python run_pipeline.py
   ```

4. **Verify**: Check `data/raw/weather_india.csv` has today's date

### Full Setup

See `API_SETUP.md` for:
- Detailed API setup instructions
- TomTom Traffic API setup (optional)
- Cron job configuration
- Troubleshooting guide

## Data Flow

```
Daily Refresh Flow:
┌─────────────────┐
│ Public APIs     │  (OpenWeatherMap, TomTom)
│ (Hourly/Real-time)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ data_fetcher.py │  (Fetches latest data)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ data/raw/*.csv  │  (Raw data files)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ run_pipeline.py │  (Processes data)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ outputs/*.csv   │  (Risk scores, alerts)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ dashboard.py    │  (Displays live data)
└─────────────────┘
```

## Verification

### Check Data Freshness

```bash
# Check file modification times
ls -lh data/raw/*.csv

# Should show today's date
```

### Check API Status

```bash
# Test API connection
python -c "from src.data_fetcher import fetch_weather_openweathermap; fetch_weather_openweathermap()"
```

### View Latest Data

```bash
# Check latest weather data
head data/raw/weather_india.csv

# Should show today's date in first column
```

## Best Practices

1.  **Set API keys** for real data
2.  **Run daily refresh** (automated via cron)
3.  **Monitor API usage** (free tiers have limits)
4.  **Check data freshness** in dashboard
5.  **Have fallback patterns** (already implemented)

## Troubleshooting

### Data Not Updating

**Check**:
1. API keys set correctly: `echo $OPENWEATHER_API_KEY`
2. Cron job running: `crontab -l`
3. Logs: Check for errors in output

**Solution**:
```bash
# Manually run pipeline
python run_pipeline.py

# Check if data files updated
ls -lh data/raw/*.csv
```

### API Rate Limits

**Symptoms**: API errors, fallback to patterns

**Solution**:
- Wait 24 hours (free tier resets daily)
- Upgrade to paid tier if needed
- System automatically uses fallback patterns

### Dashboard Shows Old Data

**Solution**:
1. Run pipeline: `python run_pipeline.py`
2. Click " Refresh Dashboard" in sidebar
3. Or restart dashboard

## Cost

### Free Tier (Sufficient for MVP)
- OpenWeatherMap: 1,000 calls/day
- TomTom: 2,500 requests/day
- **Total**: $0/month

### Production (Optional)
- OpenWeatherMap: $40/month (unlimited)
- TomTom: $0.50 per 1,000 requests
- **Estimated**: $50-100/month for 6 cities

## Next Steps

1.  Set up OpenWeatherMap API key
2.  Test data fetching
3.  Set up daily cron job
4.  Verify dashboard shows fresh data
5.  Monitor data freshness indicators

## Support

- **API Setup**: See `API_SETUP.md`
- **Dashboard**: See `DASHBOARD_GUIDE.md`
- **General**: See `README.md`

