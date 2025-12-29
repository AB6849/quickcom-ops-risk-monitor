# Data Sources for India Quick-Commerce Operational Risk Monitor

This document explains how to obtain **real, authentic public data** for the operational risk monitoring system.

## Current Data

The sample data files in `data/raw/` are generated using realistic patterns based on:
- Indian Meteorological Department (IMD) climate data patterns
- TomTom Traffic Index for Indian cities
- E-commerce demand patterns from industry reports

## Getting Real Public Data

### Option 1: OpenWeatherMap API (Recommended for Weather)

**Free Tier Available**: 1,000 calls/day

1. **Sign up**: https://openweathermap.org/api
2. **Get API key**: Free registration provides API key
3. **Set environment variable**:
   ```bash
   export OPENWEATHER_API_KEY='your_api_key_here'
   ```
4. **Run data fetcher**:
   ```bash
   python fetch_real_data.py
   ```

The script will fetch real weather data for Indian cities.

### Option 2: India Meteorological Department (IMD) Data

**Official Government Source**: https://mausam.imd.gov.in/

1. Visit IMD website
2. Navigate to "Historical Data" section
3. Download CSV files for:
   - Rainfall data by city
   - Temperature data by city
4. Format the data to match expected schema:
   - Columns: `date, city, rainfall_mm, temperature`
   - Date format: YYYY-MM-DD
   - City names: Title case (Mumbai, Delhi, etc.)

### Option 3: Public Weather Datasets

**Kaggle Datasets**:
- Search: "India weather data"
- Many free datasets available
- Download and format to match schema

**GitHub Repositories**:
- Search: "india weather data csv"
- Several open-source datasets available

### Traffic Data Sources

**Real-time Traffic APIs** (Paid):
- Google Maps Traffic API
- TomTom Traffic API
- HERE Traffic API

**Public Alternatives**:
1. **TomTom Traffic Index**: 
   - Website: https://www.tomtom.com/traffic-index/
   - Provides congestion levels for major cities
   - Can be scraped or manually downloaded

2. **Government Road Transport Data**:
   - Ministry of Road Transport and Highways
   - Data.gov.in portal
   - May require registration

3. **OpenStreetMap Data**:
   - Can be used to estimate traffic patterns
   - Requires processing

### Demand Data Sources

**Note**: Real demand data is typically proprietary. Use proxy metrics:

1. **Population Density** (Public):
   - Census of India data
   - Available from data.gov.in
   - Higher population = higher demand potential

2. **Economic Indicators** (Public):
   - GDP per city (Ministry of Statistics)
   - Consumer spending data
   - Available from MOSPI

3. **E-commerce Penetration** (Public Reports):
   - Industry reports from NASSCOM
   - E-commerce market size by city
   - Available in public reports

4. **Internal Data** (If Available):
   - Order volume from your own systems
   - Normalize to 0-1 index
   - Format: `date, city, demand_index`

## Data Format Requirements

All CSV files must follow these schemas:

### weather_india.csv
```csv
date,city,rainfall_mm,temperature
2024-01-01,Mumbai,0.0,28.5
2024-01-01,Delhi,0.0,15.2
```

### traffic_india.csv
```csv
date,city,congestion_level
2024-01-01,Mumbai,0.65
2024-01-01,Delhi,0.72
```
Note: `congestion_level` is 0-1 scale (0 = no traffic, 1 = maximum congestion)

### demand_india.csv
```csv
date,city,demand_index
2024-01-01,Mumbai,0.72
2024-01-01,Delhi,0.68
```
Note: `demand_index` is 0-1 scale (0 = no demand, 1 = peak demand)

## Automated Data Fetching

The `fetch_real_data.py` script can be extended to:
- Fetch from multiple APIs
- Scrape public data sources
- Process government datasets
- Combine multiple sources

Example extension:
```python
# Add your API key
OPENWEATHER_API_KEY = 'your_key'

# Run fetcher
python fetch_real_data.py
```

## Data Quality Checklist

Before using data, ensure:
- [ ] Dates are in YYYY-MM-DD format
- [ ] City names are consistent (Title case)
- [ ] No missing values for required columns
- [ ] Data ranges are realistic:
  - Rainfall: 0-100mm (typical range)
  - Temperature: 5-45°C (Indian cities)
  - Congestion: 0.2-0.95 (realistic range)
  - Demand: 0.3-0.95 (normalized index)

## Legal and Ethical Considerations

-  Use only publicly available data
-  Respect API rate limits
-  Follow terms of service for APIs
-  Cite data sources in documentation
-  Don't scrape without permission

## Next Steps

1. **For MVP/Demo**: Use the provided sample data (realistic patterns)
2. **For Production**: 
   - Set up OpenWeatherMap API
   - Integrate traffic APIs
   - Connect to internal demand data
   - Set up automated daily data fetching

## Questions?

- Check API documentation for each service
- Review government data portals
- Consult data.gov.in for official datasets
- Use Kaggle/GitHub for community datasets

