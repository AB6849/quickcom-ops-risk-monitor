# API Setup Guide - Daily Data Refresh

This guide shows you how to set up **real, daily-updated data sources** for the dashboard.

## Overview

The system fetches data from public APIs that update daily:
- **Weather**: Open-Meteo API (**COMPLETELY FREE, no API key needed**, updates hourly)
- **Traffic**: TomTom Traffic API (real-time, optional, free tier available)
- **Demand**: Proxy metrics from public sources

## Step 1: Weather Data (NO SETUP NEEDED! )

### Open-Meteo API - Completely Free

 **No API key required!**
 **No registration needed!**
 **Updates hourly!**
 **No rate limits for reasonable use!**

The system automatically uses Open-Meteo API - **no setup required!**

**API Details**:
- Website: https://open-meteo.com/
- Documentation: https://open-meteo.com/en/docs
- Free for commercial and non-commercial use
- Updates every hour

## Step 2: TomTom Traffic API (Optional - Not Required)

### Get Free API Key

1. **Sign up**: https://developer.tomtom.com/
2. **Free tier**: 2,500 requests/day, real-time data
3. **Get API key**: Dashboard → API keys

### Set Environment Variable

```bash
export TOMTOM_API_KEY='your_api_key_here'
```

### Note

If TomTom API key is not set, the system uses realistic traffic patterns based on TomTom Traffic Index (public data).

## Step 3: Test Data Fetching

```bash
# Test fetching data (no API keys needed!)
python3 -c "from src.data_fetcher import fetch_all_data; fetch_all_data()"
```

You should see:
```
  Fetching weather data from Open-Meteo API (FREE, no API key needed)...
   Mumbai: 28.5°C, 0.0mm rain
   Delhi: 15.2°C, 0.0mm rain
  ...
 Data Fetching Complete!
```

**Note**: Weather data works immediately - no setup needed!

## Step 4: Daily Automated Refresh

### Option A: Cron Job (macOS/Linux)

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 9 AM)
0 9 * * * cd /path/to/quickcom-ops-risk-monitor && /path/to/python run_pipeline.py >> logs/daily_refresh.log 2>&1
```

### Option B: Scheduled Task (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 9:00 AM
4. Action: Start a program
   - Program: `python`
   - Arguments: `run_pipeline.py`
   - Start in: `C:\path\to\quickcom-ops-risk-monitor`

### Option C: Manual Script

```bash
# Run daily refresh script
chmod +x daily_refresh.sh
./daily_refresh.sh
```

## Data Sources Summary

### Weather Data
- **Source**: OpenWeatherMap API
- **Update Frequency**: Hourly
- **Free Tier**: 1,000 calls/day
- **Fallback**: Realistic patterns based on IMD data

### Traffic Data
- **Source**: TomTom Traffic API (optional)
- **Update Frequency**: Real-time
- **Free Tier**: 2,500 requests/day
- **Fallback**: Patterns based on TomTom Traffic Index (public)

### Demand Data
- **Source**: Proxy metrics (population, economic indicators)
- **Update Frequency**: Daily (based on day of week, season)
- **Note**: Real demand data is proprietary; uses public metrics

## Verification

### Check Data Files

```bash
# View latest data
head data/raw/weather_india.csv
head data/raw/traffic_india.csv
head data/raw/demand_india.csv
```

### Check Data Freshness

```bash
# Check file modification time
ls -lh data/raw/*.csv

# Should show today's date if refreshed
```

## Troubleshooting

### "API key not found"

**Solution**: Set environment variable:
```bash
export OPENWEATHER_API_KEY='your_key'
```

### "API rate limit exceeded"

**Solution**: 
- Free tier: 1,000 calls/day for OpenWeatherMap
- Wait 24 hours or upgrade to paid tier
- System will use fallback patterns

### "Network error"

**Solution**:
- Check internet connection
- Verify API endpoints are accessible
- System will use fallback patterns

### Data not updating

**Solution**:
1. Check cron job is running: `crontab -l`
2. Check logs: `tail logs/daily_refresh.log`
3. Manually run: `python run_pipeline.py`

## API Costs

### Free Tier (Sufficient for MVP)

- **OpenWeatherMap**: 1,000 calls/day (free)
- **TomTom**: 2,500 requests/day (free)
- **Total Cost**: $0/month

### Paid Tier (For Production)

- **OpenWeatherMap**: $40/month (unlimited)
- **TomTom**: $0.50 per 1,000 requests
- **Estimated**: $50-100/month for 6 cities

## Best Practices

1. **Always set API keys** for real data
2. **Monitor API usage** to avoid rate limits
3. **Set up daily cron job** for automatic refresh
4. **Check logs regularly** for errors
5. **Have fallback patterns** (already implemented)

## Next Steps

1.  Get OpenWeatherMap API key
2.  Set environment variable
3.  Test data fetching
4.  Set up daily cron job
5.  Verify dashboard shows latest data

## Support

- OpenWeatherMap: https://openweathermap.org/faq
- TomTom: https://developer.tomtom.com/support
- Project Issues: Check logs in `logs/` directory

