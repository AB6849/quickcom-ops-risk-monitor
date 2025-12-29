# How to View Outputs

This guide shows you how to run the pipeline and view the risk monitoring outputs.

## Step 1: Install Dependencies

### Option A: Using pip (if allowed)
```bash
pip install pandas numpy
```

### Option B: Using virtual environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Option C: Using conda
```bash
conda install pandas numpy
```

## Step 2: Run the Pipeline

```bash
python run_pipeline.py
```

This will:
1. Load and clean raw data
2. Create rolling 7-day features
3. Compute risk scores
4. Generate alerts
5. Save outputs to `outputs/` directory

## Step 3: View the Outputs

### Option A: Use the Output Viewer Script

```bash
python view_outputs.py
```

This displays:
- Daily risk scores for all cities
- High-risk alerts
- Historical trends
- Risk distribution

### Option B: View CSV Files Directly

The outputs are saved as CSV files in the `outputs/` directory:

#### 1. Daily City Risk (`outputs/daily_city_risk.csv`)

Contains risk scores for all cities and dates:
- `date`: Date of the risk assessment
- `city`: City name
- `city_tier`: Tier classification (Tier 1, 2, or 3)
- `traffic_risk`: Traffic risk component (0-100)
- `weather_risk`: Weather risk component (0-100)
- `demand_risk`: Demand risk component (0-100)
- `risk_score`: Combined risk score (0-100)
- `risk_classification`: Low, Medium, or High

**View in terminal:**
```bash
# View latest risk scores
python3 -c "import pandas as pd; df = pd.read_csv('outputs/daily_city_risk.csv', parse_dates=['date']); print(df[df['date'] == df['date'].max()].to_string())"

# View all data
head -20 outputs/daily_city_risk.csv
```

**View in Excel/Google Sheets:**
- Open `outputs/daily_city_risk.csv` in Excel or Google Sheets
- Filter by date to see latest scores
- Sort by `risk_score` to see highest risk cities

#### 2. Alerts Today (`outputs/alerts_today.csv`)

Contains only high-risk cities for the latest date:
- `date`: Date of the alert
- `city`: City name
- `city_tier`: Tier classification
- `risk_score`: Combined risk score
- `risk_classification`: Always "High"
- `alert_reason`: Human-readable explanation
- Individual risk components

**View in terminal:**
```bash
cat outputs/alerts_today.csv
```

**View in Excel/Google Sheets:**
- Open `outputs/alerts_today.csv`
- This shows only cities requiring immediate attention

### Option C: Use Python/Pandas

```python
import pandas as pd

# Load risk scores
risk_df = pd.read_csv('outputs/daily_city_risk.csv', parse_dates=['date'])

# Get latest date
latest_date = risk_df['date'].max()
latest_risk = risk_df[risk_df['date'] == latest_date]

# View high-risk cities
high_risk = latest_risk[latest_risk['risk_classification'] == 'High']
print(high_risk[['city', 'risk_score', 'alert_reason']])

# View all cities sorted by risk
print(latest_risk.sort_values('risk_score', ascending=False))
```

## Understanding the Outputs

### Risk Score Interpretation

- **0-30 (Low Risk)**:  Normal operations, no action needed
- **31-60 (Medium Risk)**:  Monitor closely, may need resource allocation
- **61-100 (High Risk)**:  Immediate action required, alerts generated

### Risk Components

1. **Traffic Risk (40% weight)**
   - Based on congestion levels
   - Higher congestion = higher delivery delays

2. **Weather Risk (35% weight)**
   - Based on rainfall and temperature
   - Heavy rain = operational disruptions

3. **Demand Risk (25% weight)**
   - Based on demand index
   - High demand = capacity strain

### Example Output

```
Latest Date: 2024-01-31
Risk Distribution:
    Low: 2 cities
    Medium: 3 cities
    High: 1 city

High-Risk Alerts:
   Mumbai - Risk Score: 78.5
   Reason: High traffic congestion (0.85); Heavy rainfall (42.5mm)
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"

**Solution**: Install dependencies first:
```bash
pip install pandas numpy
```

### "Output files not found"

**Solution**: Run the pipeline first:
```bash
python run_pipeline.py
```

### "No high-risk alerts today"

**This is normal!** It means all cities are operating within acceptable risk levels.

## Quick Reference

```bash
# 1. Install dependencies
pip install pandas numpy

# 2. Run pipeline
python run_pipeline.py

# 3. View outputs
python view_outputs.py

# OR view CSV files directly
cat outputs/alerts_today.csv
head outputs/daily_city_risk.csv
```

## Next Steps

- Review high-risk alerts daily
- Adjust resource allocation based on risk scores
- Monitor trends over time
- Integrate with your operations dashboard

