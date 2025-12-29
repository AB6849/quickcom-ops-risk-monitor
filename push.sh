#!/bin/bash
# Simple push script

echo "=========================================="
echo "Pushing to GitHub"
echo "=========================================="
echo ""

# Check authentication
if gh auth status &>/dev/null; then
    echo "[OK] Already authenticated"
else
    echo "Authenticating with GitHub..."
    echo "This will open your browser for authorization."
    echo ""
    gh auth login --web
fi

# Push
echo ""
echo "Pushing to GitHub..."
if git push -u origin main; then
    echo ""
    echo "=========================================="
    echo "[SUCCESS] Pushed to GitHub!"
    echo "=========================================="
    echo ""
    echo "Repository: https://github.com/AB6849/quickcom-ops-risk-monitor"
    echo ""
    echo "Next: Deploy to Streamlit Cloud"
    echo "1. Go to: https://share.streamlit.io/"
    echo "2. Sign in with GitHub"
    echo "3. Click 'New app'"
    echo "4. Select: quickcom-ops-risk-monitor"
    echo "5. Main file: dashboard.py"
    echo "6. Click 'Deploy'"
    echo ""
    echo "Your public dashboard will be at:"
    echo "https://YOUR-APP-NAME.streamlit.app"
else
    echo ""
    echo "[ERROR] Push failed"
    echo ""
    echo "Alternative: Use Personal Access Token"
    echo "1. Create token: https://github.com/settings/tokens"
    echo "2. Select 'repo' scope"
    echo "3. Run: git remote set-url origin https://YOUR_TOKEN@github.com/AB6849/quickcom-ops-risk-monitor.git"
    echo "4. Run: git push -u origin main"
fi

