# Daily Automation Guide

This guide shows you how to run the pipeline automatically every day to keep your dashboard updated with fresh data.

## Option 1: GitHub Actions (Recommended - Runs in Cloud)

**Best for**: Automatic daily runs without keeping your computer on

### Setup

1. **The workflow already exists** at `.github/workflows/daily_refresh.yml`
2. **It runs daily at 9 AM UTC** (2:30 PM IST)
3. **It automatically commits and pushes** updated data to GitHub
4. **Streamlit Cloud will auto-update** with the new data

### Enable GitHub Actions

1. Go to your GitHub repository: https://github.com/AB6849/quickcom-ops-risk-monitor
2. Click **"Actions"** tab
3. Click **"Daily Data Refresh"** workflow
4. Click **"Enable workflow"** (if not already enabled)

### Manual Trigger

You can also trigger it manually:
1. Go to **Actions** tab
2. Click **"Daily Data Refresh"**
3. Click **"Run workflow"** button
4. Select branch: **main**
5. Click **"Run workflow"**

### Schedule

- **Current schedule**: Daily at 9:00 AM UTC (2:30 PM IST)
- **To change**: Edit `.github/workflows/daily_refresh.yml` and modify the cron schedule

### Benefits

- ✅ Runs automatically in the cloud
- ✅ No need to keep your computer on
- ✅ Automatically commits data to GitHub
- ✅ Streamlit Cloud auto-updates
- ✅ Free (GitHub Actions free tier: 2,000 minutes/month)

---

## Option 2: Local Cron Job (macOS/Linux)

**Best for**: Running on your local machine daily

### Setup

1. **Open crontab editor**:
   ```bash
   crontab -e
   ```

2. **Add this line** (runs daily at 9:00 AM):
   ```bash
   0 9 * * * cd /Users/mac/Documents/quickcom-ops-risk-monitor && /Users/mac/Documents/quickcom-ops-risk-monitor/venv/bin/python3 /Users/mac/Documents/quickcom-ops-risk-monitor/run_pipeline.py >> /Users/mac/Documents/quickcom-ops-risk-monitor/logs/daily_refresh.log 2>&1
   ```

3. **Or use the daily refresh script**:
   ```bash
   0 9 * * * /Users/mac/Documents/quickcom-ops-risk-monitor/daily_refresh.sh >> /Users/mac/Documents/quickcom-ops-risk-monitor/logs/daily_refresh.log 2>&1
   ```

### Create logs directory

```bash
mkdir -p /Users/mac/Documents/quickcom-ops-risk-monitor/logs
```

### Verify cron job

```bash
# List your cron jobs
crontab -l

# Check logs
tail -f /Users/mac/Documents/quickcom-ops-risk-monitor/logs/daily_refresh.log
```

### Schedule Times

- `0 9 * * *` = 9:00 AM daily
- `0 6 * * *` = 6:00 AM daily
- `0 0 * * *` = Midnight daily
- `0 9 * * 1-5` = 9:00 AM on weekdays only

---

## Option 3: Manual Script (Quick Daily Run)

**Best for**: Running manually when needed

### Run the script

```bash
cd /Users/mac/Documents/quickcom-ops-risk-monitor
source venv/bin/activate
./daily_refresh.sh
```

Or directly:

```bash
cd /Users/mac/Documents/quickcom-ops-risk-monitor
source venv/bin/activate
python3 run_pipeline.py
```

---

## Option 4: macOS LaunchAgent (Background Service)

**Best for**: Running as a background service on macOS

### Create LaunchAgent

1. **Create the plist file**:
   ```bash
   nano ~/Library/LaunchAgents/com.quickcom.dailyrefresh.plist
   ```

2. **Add this content**:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.quickcom.dailyrefresh</string>
       <key>ProgramArguments</key>
       <array>
           <string>/Users/mac/Documents/quickcom-ops-risk-monitor/venv/bin/python3</string>
           <string>/Users/mac/Documents/quickcom-ops-risk-monitor/run_pipeline.py</string>
       </array>
       <key>StartCalendarInterval</key>
       <dict>
           <key>Hour</key>
           <integer>9</integer>
           <key>Minute</key>
           <integer>0</integer>
       </dict>
       <key>StandardOutPath</key>
       <string>/Users/mac/Documents/quickcom-ops-risk-monitor/logs/daily_refresh.log</string>
       <key>StandardErrorPath</key>
       <string>/Users/mac/Documents/quickcom-ops-risk-monitor/logs/daily_refresh_error.log</string>
   </dict>
   </plist>
   ```

3. **Load the service**:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.quickcom.dailyrefresh.plist
   ```

4. **Start the service**:
   ```bash
   launchctl start com.quickcom.dailyrefresh
   ```

5. **Check status**:
   ```bash
   launchctl list | grep quickcom
   ```

---

## Recommended Setup

**For most users**: Use **GitHub Actions (Option 1)**

- ✅ No local machine needed
- ✅ Automatic and reliable
- ✅ Free
- ✅ Auto-updates Streamlit Cloud

**If you want local control**: Use **Cron Job (Option 2)**

- ✅ Runs on your schedule
- ✅ Full control
- ✅ Requires your machine to be on

---

## Testing Your Setup

### Test GitHub Actions

1. Go to Actions tab
2. Click "Run workflow"
3. Check the logs to see if it runs successfully

### Test Cron Job

```bash
# Run manually first
cd /Users/mac/Documents/quickcom-ops-risk-monitor
source venv/bin/activate
python3 run_pipeline.py

# If successful, cron will work too
```

---

## Troubleshooting

### GitHub Actions not running

1. Check if workflow is enabled in Actions tab
2. Check workflow file syntax: `.github/workflows/daily_refresh.yml`
3. Check GitHub Actions usage limits (free tier: 2,000 min/month)

### Cron job not running

1. Check cron service: `sudo launchctl list | grep cron`
2. Check logs: `tail -f logs/daily_refresh.log`
3. Verify path: Use absolute paths in crontab
4. Check permissions: `chmod +x daily_refresh.sh`

### Data not updating

1. Check if pipeline ran: `ls -lh outputs/daily_city_risk.csv`
2. Check file timestamp: Should be today's date
3. Manually run: `python3 run_pipeline.py`
4. Check for errors in logs

---

## Next Steps

1. **Choose your method** (GitHub Actions recommended)
2. **Test it** by running manually first
3. **Verify** data updates in dashboard
4. **Monitor** logs for first few days

Your dashboard will now stay updated with fresh data every day!

