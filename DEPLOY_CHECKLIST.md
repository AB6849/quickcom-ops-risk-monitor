# Deployment Checklist - Make Dashboard Public

## Quick Steps (5 minutes)

### 1. Prepare Repository
- [ ] Initialize git (if not done): `git init`
- [ ] Add all files: `git add .`
- [ ] Commit: `git commit -m "Ready for deployment"`
- [ ] Create GitHub repository
- [ ] Push: `git push origin main`

### 2. Generate Sample Data (Recommended)
```bash
# Run pipeline to create sample outputs
python3 run_pipeline.py

# Commit the data files
git add outputs/ data/processed/
git commit -m "Add sample data for public demo"
git push
```

### 3. Deploy to Streamlit Cloud
- [ ] Go to https://share.streamlit.io/
- [ ] Sign in with GitHub
- [ ] Click "New app"
- [ ] Select repository: `quickcom-ops-risk-monitor`
- [ ] Main file: `dashboard.py`
- [ ] App URL: Choose a name (e.g., `quickcom-risk-monitor`)
- [ ] Click "Deploy"

### 4. Get Public Link
- [ ] Copy your public URL: `https://YOUR-APP-NAME.streamlit.app`
- [ ] Share with anyone!

## What Happens

1. **First Load**: 
   - If data exists: Dashboard loads immediately
   - If no data: Auto-generates (takes 1-2 minutes)

2. **Subsequent Loads**: 
   - Fast (cached data)
   - Shows latest data from repository

3. **Auto-Updates**:
   - Every GitHub push = automatic redeploy
   - No manual steps needed

## Optional: Daily Auto-Refresh

Enable GitHub Actions for daily data refresh:
- File: `.github/workflows/daily_refresh.yml` (already created)
- Automatically runs pipeline daily
- Commits new data
- Dashboard always shows latest data

## Troubleshooting

**Dashboard shows "No Data"**:
- Wait 1-2 minutes (first load generates data)
- Or commit sample data before deploying

**Slow first load**:
- Normal - generating 31 cities × 8 days of data takes time
- Subsequent loads are instant

**Need to update**:
- Just push to GitHub
- Streamlit Cloud redeploys automatically

## Your Public Dashboard

Once deployed, share this link:
```
https://YOUR-APP-NAME.streamlit.app
```

**No login required** - anyone can view!

