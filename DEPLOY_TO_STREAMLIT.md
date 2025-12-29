# Deploy to Streamlit Cloud - Get Public Dashboard Link

## ✅ Code is on GitHub!

Your repository: **https://github.com/AB6849/quickcom-ops-risk-monitor**

## Deploy to Streamlit Cloud (2 minutes)

### Step 1: Go to Streamlit Cloud
Visit: **https://share.streamlit.io/**

### Step 2: Sign In
- Click "Sign in"
- Sign in with **GitHub**
- Authorize Streamlit Cloud

### Step 3: Create New App
1. Click **"New app"** button
2. Fill in:
   - **Repository**: `AB6849/quickcom-ops-risk-monitor`
   - **Branch**: `main`
   - **Main file path**: `dashboard.py`
   - **App URL**: `quickcom-risk-monitor` (or your choice)
3. Click **"Deploy"**

### Step 4: Wait for Deployment
- Takes 1-2 minutes
- Streamlit Cloud will:
  - Install dependencies
  - Run the dashboard
  - Generate data (if needed)

### Step 5: Get Your Public Link
Once deployed, your dashboard will be at:
```
https://quickcom-risk-monitor.streamlit.app
```
(Or whatever URL you chose)

## Your Public Dashboard

**Share this link** - anyone can view it, no login required!

Features:
- ✅ 31 cities monitored
- ✅ All risk levels (High, Medium, Low)
- ✅ Interactive charts
- ✅ Real-time data from Open-Meteo
- ✅ 7-day trends
- ✅ Export capabilities

## Auto-Updates

Every time you push to GitHub, Streamlit Cloud automatically redeploys your dashboard!

## Troubleshooting

**Dashboard shows "No Data"**:
- Wait 1-2 minutes (first load generates data)
- Or check Streamlit Cloud logs

**Deployment fails**:
- Check that `dashboard.py` is in root directory
- Verify `requirements.txt` has all dependencies
- Check Streamlit Cloud logs for errors

## That's It!

Your dashboard is now publicly accessible! 🎉

