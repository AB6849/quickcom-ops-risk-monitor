#!/bin/bash
# Quick push script with multiple auth options

echo "=== GitHub Push Helper ==="
echo ""

# Check if GitHub CLI is available
if command -v gh &> /dev/null; then
    echo "[OK] GitHub CLI found"
    echo "Authenticating with GitHub CLI..."
    gh auth login --web
    echo ""
    echo "Pushing to GitHub..."
    git push -u origin main
    if [ $? -eq 0 ]; then
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
    fi
else
    echo "[INFO] GitHub CLI not installed"
    echo ""
    echo "Option 1: Install GitHub CLI (Recommended)"
    echo "  brew install gh"
    echo "  gh auth login"
    echo "  git push -u origin main"
    echo ""
    echo "Option 2: Use Personal Access Token"
    echo "  1. Create token: https://github.com/settings/tokens"
    echo "  2. Select 'repo' scope"
    echo "  3. Copy token"
    echo "  4. Run: git remote set-url origin https://YOUR_TOKEN@github.com/AB6849/quickcom-ops-risk-monitor.git"
    echo "  5. Run: git push -u origin main"
    echo ""
    echo "Option 3: Use SSH"
    echo "  Run: ./setup_ssh.sh"
fi
