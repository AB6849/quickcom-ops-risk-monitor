# Deploy Dashboard to Streamlit Cloud (Public Access)

This guide shows you how to deploy your dashboard to Streamlit Cloud so anyone with the link can access it.

## What is Streamlit Cloud?

- **Free hosting** for Streamlit apps
- **Public sharing** - anyone with link can view
- **Automatic updates** when you push to GitHub
- **No server management** required
- Perfect for interviews and demos

## Prerequisites

1. GitHub account (free)
2. Your code pushed to a GitHub repository

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Ensure all files are committed**:
   ```bash
   git add .
   git commit -m "Ready for Streamlit Cloud deployment"
   ```

2. **Push to GitHub**:
   ```bash
   git push origin main
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**: https://share.streamlit.io/

2. **Sign in** with your GitHub account

3. **Click "New app"**

4. **Fill in the details**:
   - **Repository**: Select your `quickcom-ops-risk-monitor` repository
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `dashboard.py`
   - **App URL**: Choose a custom subdomain (e.g., `quickcom-risk-monitor`)

5. **Click "Deploy"**

### Step 3: Configure (Optional)

If you want to use API keys (optional since Open-Meteo is free):

1. In Streamlit Cloud dashboard, go to your app
2. Click "Settings" (⚙️ icon)
3. Go to "Secrets" tab
4. Add your API keys:
   ```toml
   TOMTOM_API_KEY = "your_key_here"
   ```

### Step 4: Share Your Dashboard

Once deployed, you'll get a public URL like:
```
https://quickcom-risk-monitor.streamlit.app
```

**Share this link with anyone** - no login required!

## Automatic Updates

- Every time you push to GitHub, Streamlit Cloud automatically redeploys
- Your dashboard stays up-to-date with latest code
- No manual deployment needed

## Troubleshooting

### App won't start

**Check**:
1. `dashboard.py` is in the root directory
2. `requirements.txt` includes all dependencies
3. Data files exist (or app handles missing data gracefully)

### Data not showing

**Solution**: 
- The app needs data files. Options:
  1. Include sample data in the repository
  2. Run pipeline in Streamlit Cloud (add to app startup)
  3. Use GitHub Actions to generate data daily

### Slow loading

**Solution**:
- Streamlit Cloud free tier has resource limits
- Consider upgrading to paid tier for production
- Or optimize data loading (use caching)

## Alternative: Include Sample Data

To ensure the dashboard works immediately:

1. **Commit sample output files**:
   ```bash
   git add outputs/
   git commit -m "Add sample data for demo"
   git push
   ```

2. **Or generate data on first load** (see next section)

## Auto-Generate Data on First Load

You can modify the dashboard to automatically run the pipeline if data doesn't exist:

```python
# Add to dashboard.py
if not risk_file.exists():
    # Auto-generate data
    import subprocess
    subprocess.run(['python', 'run_pipeline.py'])
    # Reload
    st.rerun()
```

## Best Practices

1. **Include sample data** in repository for immediate demo
2. **Set up GitHub Actions** to refresh data daily
3. **Use secrets** for API keys (don't commit them)
4. **Test locally** before deploying
5. **Monitor usage** in Streamlit Cloud dashboard

## Cost

- **Free tier**: Unlimited apps, public sharing
- **Team tier**: $20/month (for private apps, team features)
- **For interviews**: Free tier is perfect!

## Next Steps

1. Deploy to Streamlit Cloud
2. Share the public link
3. Set up daily data refresh (optional)
4. Monitor and iterate

Your dashboard will be accessible to anyone with the link!

