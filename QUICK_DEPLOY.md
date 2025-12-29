# Quick Deploy Guide - Make Dashboard Public

## 3-Step Deployment to Streamlit Cloud

### Step 1: Push to GitHub (2 minutes)

```bash
# If not already a git repo
git init
git add .
git commit -m "Ready for public deployment"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/quickcom-ops-risk-monitor.git
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud (2 minutes)

1. Go to: **https://share.streamlit.io/**
2. Sign in with **GitHub**
3. Click **"New app"**
4. Fill in:
   - **Repository**: `quickcom-ops-risk-monitor`
   - **Branch**: `main`
   - **Main file**: `dashboard.py`
   - **App URL**: Choose a name (e.g., `quickcom-risk-monitor`)
5. Click **"Deploy"**

### Step 3: Share Your Link (1 minute)

Once deployed, you'll get a public URL:
```
https://YOUR-APP-NAME.streamlit.app
```

**Share this link** - anyone can view it, no login needed!

## What Happens

- **First visit**: Dashboard auto-generates data (1-2 min)
- **Subsequent visits**: Instant load (cached)
- **Auto-updates**: Every GitHub push = automatic redeploy

## Optional: Include Sample Data

For faster first load, commit sample data:

```bash
# Generate data
python3 run_pipeline.py

# Commit data files
git add outputs/ data/processed/
git commit -m "Add sample data"
git push
```

## That's It!

Your dashboard is now publicly accessible. Perfect for interviews and demos!

