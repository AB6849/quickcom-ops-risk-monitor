#!/bin/bash
# Script to push to GitHub and get the repository link

echo "=========================================="
echo "Pushing to GitHub"
echo "=========================================="

# Check if remote exists
if git remote get-url origin &>/dev/null; then
    echo "[OK] Remote 'origin' already configured"
    REMOTE_URL=$(git remote get-url origin)
    echo "Remote URL: $REMOTE_URL"
else
    echo ""
    echo "GitHub repository not configured yet."
    echo ""
    echo "Please create a repository on GitHub first:"
    echo "1. Go to: https://github.com/new"
    echo "2. Repository name: quickcom-ops-risk-monitor"
    echo "3. Make it PUBLIC"
    echo "4. Don't initialize with README"
    echo "5. Click 'Create repository'"
    echo ""
    read -p "Enter your GitHub username: " GITHUB_USERNAME
    
    if [ -z "$GITHUB_USERNAME" ]; then
        echo "[ERROR] GitHub username required"
        exit 1
    fi
    
    echo ""
    echo "Adding remote origin..."
    git remote add origin "https://github.com/${GITHUB_USERNAME}/quickcom-ops-risk-monitor.git"
    echo "[OK] Remote added"
fi

# Ensure we're on main branch
git branch -M main

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
if git push -u origin main; then
    echo ""
    echo "=========================================="
    echo "[SUCCESS] Code pushed to GitHub!"
    echo "=========================================="
    echo ""
    
    # Get repository URL
    REPO_URL=$(git remote get-url origin | sed 's/\.git$//' | sed 's/git@github.com:/https:\/\/github.com\//')
    
    echo "Repository URL: $REPO_URL"
    echo ""
    echo "Next: Deploy to Streamlit Cloud"
    echo "1. Go to: https://share.streamlit.io/"
    echo "2. Sign in with GitHub"
    echo "3. Click 'New app'"
    echo "4. Select repository: quickcom-ops-risk-monitor"
    echo "5. Main file: dashboard.py"
    echo "6. Click 'Deploy'"
    echo ""
    echo "Your public dashboard will be at:"
    echo "https://YOUR-APP-NAME.streamlit.app"
    echo ""
else
    echo ""
    echo "[ERROR] Failed to push. Please check:"
    echo "1. Repository exists on GitHub"
    echo "2. You have push access"
    echo "3. Your GitHub credentials are configured"
    echo ""
    echo "If repository doesn't exist, create it at:"
    echo "https://github.com/new"
    exit 1
fi

