# India Quick-Commerce Operational Risk Monitor

A production-ready MVP system for monitoring operational risk in Indian quick-commerce operations using public datasets. This system provides near-real-time risk scoring and alerts to help operations teams proactively manage delivery capacity and service quality.

## Problem Statement

Quick-commerce companies in India face significant operational challenges:
- **Traffic congestion** causes delivery delays and SLA breaches
- **Weather conditions** (especially monsoon rains) disrupt delivery operations
- **Demand surges** strain operational capacity and lead to service degradation

Without real-time visibility into these risk factors, operations teams struggle to:
- Proactively allocate resources to high-risk cities
- Adjust delivery time expectations (SLAs) based on conditions
- Prevent service quality degradation before it impacts customers

This system addresses these challenges by providing daily operational risk scores and alerts for cities across India.

## System Overview

The system processes three key data streams:
1. **Weather Data**: Rainfall and temperature by city
2. **Traffic Data**: Congestion levels by city
3. **Demand Data**: Order demand index by city

These are combined using rolling 7-day features to compute a composite operational risk score (0-100) for each city, classified as Low, Medium, or High risk.

## Data Sources

The system uses pre-downloaded CSV datasets that can be sourced from authentic public sources:

### Weather Data
- **Open-Meteo API** (**COMPLETELY FREE, no API key needed**, **updates hourly**) - https://open-meteo.com/
  - Real-time weather data
  - Updates automatically every hour
  - **No registration or API key required!**
  - No rate limits for reasonable use
- **Fallback**: Realistic patterns based on IMD climate data
- Format: `date, city, rainfall_mm, temperature`

### Traffic Data
- **TomTom Traffic API** (Free tier: 2,500 requests/day, **real-time updates**) - https://developer.tomtom.com/
  - Real-time traffic congestion data
  - Set `TOMTOM_API_KEY` environment variable (optional)
- **Fallback**: Patterns based on TomTom Traffic Index (public data)
- Format: `date, city, congestion_level` (0-1 scale)

### Demand Data
- **Internal order data** (normalized to 0-1 index) - from your systems
- **Proxy metrics**: Population density, GDP per city (Census/MOSPI data)
- **E-commerce reports**: NASSCOM industry reports
- Format: `date, city, demand_index` (0-1 scale)

**Getting Real Daily Data**: 
- **See `API_SETUP.md`** for step-by-step API setup
- Set `OPENWEATHER_API_KEY` environment variable for real weather (updates hourly)
- Set `TOMTOM_API_KEY` for real traffic data (optional, real-time)
- The pipeline automatically fetches daily data when run
- **For daily automated refresh**: Set up cron job (see `API_SETUP.md`)

## Architecture

```
data/raw/                    # Raw CSV datasets
  ├── weather_india.csv
  ├── traffic_india.csv
  └── demand_india.csv

notebooks/                   # Data processing notebooks
  ├── 01_data_ingestion.ipynb      # Data cleaning and normalization
  └── 02_feature_engineering.ipynb # Rolling features and merging

src/                         # Core modules
  ├── config.py             # City tiers, SLA thresholds, risk weights
  └── risk_engine.py       # Risk scoring engine

data/processed/             # Processed datasets
  ├── weather_cleaned.csv
  ├── traffic_cleaned.csv
  ├── demand_cleaned.csv
  └── daily_city_features.csv

outputs/                    # Risk monitoring outputs
  ├── daily_city_risk.csv  # Daily risk scores for all cities
  └── alerts_today.csv     # High-risk alerts (for today)
```

## Installation

### Local Setup

```bash
# Clone or navigate to the project directory
cd quickcom-ops-risk-monitor

# Install dependencies
pip install -r requirements.txt

# Run pipeline to generate data
python3 run_pipeline.py

# Launch dashboard locally
streamlit run dashboard.py
```

### Public Deployment (Streamlit Cloud)

**Make your dashboard publicly accessible in 5 minutes:**

1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Deploy your repository
4. Get public link to share

See `STREAMLIT_CLOUD_SETUP.md` for detailed instructions.

**Public Link Format**: `https://YOUR-APP-NAME.streamlit.app`

## Usage

### Quick Start

**1. Install dependencies:**
```bash
pip install pandas numpy
# OR
pip install -r requirements.txt
```

**2. Run the complete pipeline:**

**macOS/Linux**:
```bash
python3 run_pipeline.py
# OR use convenience script:
./run pipeline
```

**Windows**:
```bash
python run_pipeline.py
```

This will:
1. Load and clean raw data
2. Create rolling 7-day features
3. Compute risk scores
4. Generate alerts for high-risk cities
5. Save outputs to `outputs/`

**3. View the outputs:**

**Option A: Interactive Dashboard (Recommended for Interviews)**
```bash
# Install dashboard dependencies
pip install streamlit plotly

# Launch dashboard
streamlit run dashboard.py
```
The dashboard opens automatically in your browser with interactive visualizations, metrics, and alerts.

**Option B: Command Line Viewer**
```bash
python view_outputs.py
```

**Option C: View CSV Files**
```bash
cat outputs/alerts_today.csv
head outputs/daily_city_risk.csv
```

**See `DASHBOARD_GUIDE.md` for dashboard instructions and `HOW_TO_VIEW_OUTPUTS.md` for detailed CLI instructions.**

### Step-by-Step Execution

Alternatively, run notebooks individually:

1. **Data Ingestion**: Run `notebooks/01_data_ingestion.ipynb`
   - Cleans column names
   - Normalizes city names
   - Parses dates
   - Handles missing values
   - Saves cleaned data to `data/processed/`

2. **Feature Engineering**: Run `notebooks/02_feature_engineering.ipynb`
   - Creates rolling 7-day averages
   - Merges all datasets
   - Saves feature table to `data/processed/daily_city_features.csv`

3. **Risk Scoring**: The pipeline automatically runs the risk engine, or run directly:
   ```python
   from src.risk_engine import run_risk_engine
   risk_df, alerts_df = run_risk_engine(
       'data/processed/daily_city_features.csv',
       'outputs'
   )
   ```

## Risk Scoring Logic

The system computes a composite risk score (0-100) using weighted components:

### Risk Components

1. **Traffic Risk (40% weight)**
   - Congestion level 0-1 scale
   - Uses max of current day or 7-day average
   - Thresholds:
     - < 0.3: Low risk (0-20 points)
     - 0.3-0.6: Medium risk (20-50 points)
     - 0.6-0.8: High risk (50-80 points)
     - > 0.8: Critical risk (80-100 points)

2. **Weather Risk (35% weight)**
   - Rainfall impact (primary factor)
   - Temperature extremes (additive)
   - Thresholds:
     - < 5mm: Low risk (0-15 points)
     - 5-15mm: Medium risk (15-40 points)
     - 15-30mm: High risk (40-70 points)
     - > 30mm: Critical risk (70-100 points)
   - Temperature: +10 points for cold (<10°C), +15 points for extreme heat (>40°C)

3. **Demand Risk (25% weight)**
   - Demand index 0-1 scale
   - Thresholds:
     - < 0.5: Low risk (0-10 points)
     - 0.5-0.7: Medium risk (10-30 points)
     - 0.7-0.85: High risk (30-60 points)
     - > 0.85: Surge risk (60-100 points)

### Risk Classification

- **Low Risk** (0-30): Normal operations, no action needed
- **Medium Risk** (31-60): Monitor closely, may need resource allocation
- **High Risk** (61-100): Immediate action required, alerts generated

## City Tiers

Cities are classified into tiers based on population and market size:

- **Tier 1**: Mumbai, Delhi, Bangalore, Hyderabad, Chennai, Kolkata, Pune
- **Tier 2**: Ahmedabad, Jaipur, Surat, Lucknow, Kanpur, Nagpur, Indore, Thane, Bhopal, Visakhapatnam, Patna, Vadodara
- **Tier 3**: Other major cities

SLA thresholds vary by tier (Tier 1 has stricter targets).

## Outputs

### daily_city_risk.csv

Daily risk scores for all cities with:
- Date, city, city tier
- Individual risk components (traffic, weather, demand)
- Combined risk score (0-100)
- Risk classification (Low/Medium/High)
- Raw feature values

### alerts_today.csv

High-risk alerts for the latest date, including:
- City and risk score
- Alert reason (human-readable explanation)
- All risk components

## How Operations Teams Use This

### Daily Workflow

1. **Morning Review** (9:00 AM)
   - Run pipeline: `python run_pipeline.py`
   - Review `outputs/alerts_today.csv` for high-risk cities
   - Check `outputs/daily_city_risk.csv` for medium-risk cities

2. **Resource Allocation**
   - High-risk cities: Deploy additional delivery partners, increase fleet allocation
   - Medium-risk cities: Monitor closely, prepare backup resources

3. **SLA Management**
   - Adjust delivery time expectations for high-risk cities
   - Communicate delays proactively to customers
   - Update customer-facing ETAs based on risk scores

4. **Capacity Planning**
   - Use demand risk component to forecast capacity needs
   - Pre-position inventory in high-demand cities
   - Scale up customer support for high-risk periods

### Example Alert Response

**Alert**: Mumbai - High Risk (Score: 78)
- **Reason**: High traffic congestion (0.85); Heavy rainfall (42.5mm)
- **Action**: 
  - Deploy 20% additional delivery partners
  - Extend delivery SLA from 15min to 25min
  - Activate backup warehouse for overflow orders
  - Send proactive customer notifications about delays

## Assumptions and Limitations

### Assumptions

1. **Data Availability**: Assumes daily data updates for all three sources
2. **City Coverage**: Currently covers 6 major cities (extensible to all Indian cities)
3. **Real-time Processing**: System processes data once daily (can be extended to hourly)
4. **Risk Weights**: Based on industry experience (traffic > weather > demand)
5. **Rolling Window**: 7-day window balances responsiveness with stability

### Limitations

1. **No Historical Learning**: Rule-based system, not ML-based (no learning from past outcomes)
2. **Static Thresholds**: Risk thresholds are fixed, not adaptive to city-specific patterns
3. **No External Events**: Doesn't account for festivals, strikes, or other one-off events
4. **Single Risk Score**: Doesn't differentiate between different types of operational impact
5. **No Predictive Component**: Only evaluates current conditions, doesn't forecast future risk

### Future Enhancements

- **Machine Learning**: Train models on historical delivery performance vs. risk scores
- **City-Specific Models**: Different thresholds/weights per city based on local patterns
- **Event Detection**: Integrate calendar data for festivals, holidays, special events
- **Predictive Risk**: Forecast risk 24-48 hours ahead using weather forecasts
- **Multi-Metric Risk**: Separate risk scores for delivery time, order fulfillment, customer satisfaction

## Code Quality

- **Modular Design**: Separate modules for config, risk engine, data processing
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Graceful handling of missing data
- **Extensibility**: Easy to add new risk factors or cities
- **Interview-Ready**: Clean, production-quality code suitable for technical discussions

## Technical Details

### Rolling Features

The system uses rolling 7-day windows to:
- Smooth out daily fluctuations
- Capture sustained trends (not just one-off spikes)
- Provide stable risk signals for operational decision-making

### Missing Data Handling

- Forward fill within city groups (assumes continuity)
- Backward fill for edge cases
- Default to 0 for numeric columns if all else fails
- Temperature uses linear interpolation for smoother handling

### Performance

- Processes ~200 records (6 cities × 31 days) in < 1 second
- Scales linearly with number of cities and date range
- Can handle 100+ cities and 1 year of data efficiently

## License

This is a demonstration MVP. Use as needed for evaluation and learning purposes.

## Contact

For questions or enhancements, please refer to the code documentation or extend the system as needed.

