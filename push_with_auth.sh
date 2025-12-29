#!/bin/bash
# Script to push with authentication help

echo "=========================================="
echo "GitHub Push with Authentication"
echo "=========================================="
echo ""

# Check if remote is configured
if ! git remote get-url origin &>/dev/null; then
    echo "[ERROR] Remote not configured"
    exit 1
fi

REMOTE_URL=$(git remote get-url origin)
echo "Remote URL: $REMOTE_URL"
echo ""

echo "Choose authentication method:"
echo "1. Personal Access Token (PAT)"
echo "2. SSH Key"
echo "3. GitHub CLI"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "To use Personal Access Token:"
        echo "1. Create token at: https://github.com/settings/tokens"
        echo "2. Select 'repo' scope"
        echo "3. Copy the token"
        echo ""
        read -p "Enter your token: " token
        if [ ! -z "$token" ]; then
            git remote set-url origin "https://${token}@github.com/AB6849/quickcom-ops-risk-monitor.git"
            echo "[OK] Remote updated with token"
            echo "Pushing..."
            git push -u origin main
        else
            echo "[ERROR] Token required"
        fi
        ;;
    2)
        echo ""
        echo "Setting up SSH..."
        if [ ! -f ~/.ssh/id_ed25519.pub ] && [ ! -f ~/.ssh/id_rsa.pub ]; then
            echo "No SSH key found. Generating..."
            ssh-keygen -t ed25519 -C "github" -f ~/.ssh/id_ed25519 -N ""
        fi
        
        if [ -f ~/.ssh/id_ed25519.pub ]; then
            echo ""
            echo "Your SSH public key:"
            cat ~/.ssh/id_ed25519.pub
            echo ""
            echo "Add this key to GitHub:"
            echo "1. Go to: https://github.com/settings/keys"
            echo "2. Click 'New SSH key'"
            echo "3. Paste the key above"
            echo ""
            read -p "Press Enter after adding key to GitHub..."
            
            git remote set-url origin git@github.com:AB6849/quickcom-ops-risk-monitor.git
            echo "Pushing..."
            git push -u origin main
        fi
        ;;
    3)
        echo ""
        if ! command -v gh &> /dev/null; then
            echo "Installing GitHub CLI..."
            brew install gh
        fi
        echo "Authenticating with GitHub CLI..."
        gh auth login
        echo "Pushing..."
        git push -u origin main
        ;;
    *)
        echo "[ERROR] Invalid choice"
        exit 1
        ;;
esac
