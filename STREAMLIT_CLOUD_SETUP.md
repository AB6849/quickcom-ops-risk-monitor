# Quick Setup: Deploy to Streamlit Cloud

## Fastest Way to Make Dashboard Public

### Option 1: Streamlit Cloud (Recommended - 5 minutes)

1. **Push code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/quickcom-ops-risk-monitor.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**:
   - Go to: https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file: `dashboard.py`
   - Click "Deploy"

3. **Get your public link**:
   - Format: `https://YOUR-APP-NAME.streamlit.app`
   - Share with anyone!

### Option 2: Include Sample Data (For Immediate Demo)

Before deploying, commit sample data so dashboard works immediately:

```bash
# Ensure outputs exist
python3 run_pipeline.py

# Commit everything including data
git add .
git commit -m "Add sample data for public demo"
git push
```

### Option 3: Auto-Generate on First Load

The dashboard is configured to automatically run the pipeline if data doesn't exist. This works on Streamlit Cloud but may take 1-2 minutes on first load.

## What Gets Deployed

- Dashboard UI (dashboard.py)
- All source code (src/)
- Configuration files
- Sample data (if committed)
- Requirements (requirements.txt)

## Public Access

Once deployed:
- **Anyone with the link** can view the dashboard
- **No login required**
- **No API keys needed** (Open-Meteo is free)
- **Automatic updates** when you push to GitHub

## Daily Refresh (Optional)

Set up GitHub Actions to refresh data daily:
- See `.github/workflows/daily_refresh.yml`
- Automatically runs pipeline and commits new data
- Dashboard always shows latest data

## Troubleshooting

**Dashboard shows "No Data"**:
- Wait 1-2 minutes (first load generates data)
- Or commit sample data to repository

**Slow first load**:
- Normal - generating data takes time
- Subsequent loads are fast (cached)

**Need to update dashboard**:
- Just push to GitHub
- Streamlit Cloud auto-updates

## Share Your Dashboard

Once deployed, share this link:
```
https://YOUR-APP-NAME.streamlit.app
```

Perfect for interviews and demos!

