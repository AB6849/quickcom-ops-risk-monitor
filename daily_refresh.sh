#!/bin/bash
# Daily Data Refresh Script
# Run this daily (via cron) to fetch latest data and update dashboard

echo "=========================================="
echo "Daily Data Refresh - $(date)"
echo "=========================================="

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run pipeline (fetches data + processes)
echo "Running pipeline..."
python3 run_pipeline.py

# Check if successful
if [ $? -eq 0 ]; then
    echo "[OK] Daily refresh complete!"
    echo "Dashboard will show latest data on next refresh."
else
    echo "[ERROR] Error during refresh. Check logs."
    exit 1
fi

