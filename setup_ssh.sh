#!/bin/bash
# Setup SSH for GitHub

echo "=== Setting up SSH for GitHub ==="
echo ""

# Generate SSH key if it doesn't exist
if [ ! -f ~/.ssh/id_ed25519 ]; then
    echo "Generating SSH key..."
    ssh-keygen -t ed25519 -C "github" -f ~/.ssh/id_ed25519 -N ""
    echo "[OK] SSH key generated"
else
    echo "[OK] SSH key already exists"
fi

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add key to ssh-agent
ssh-add ~/.ssh/id_ed25519

# Display public key
echo ""
echo "=========================================="
echo "Your SSH Public Key:"
echo "=========================================="
cat ~/.ssh/id_ed25519.pub
echo ""
echo "=========================================="
echo ""
echo "Add this key to GitHub:"
echo "1. Go to: https://github.com/settings/keys"
echo "2. Click 'New SSH key'"
echo "3. Title: quickcom-ops-risk-monitor"
echo "4. Paste the key above"
echo "5. Click 'Add SSH key'"
echo ""
read -p "Press Enter after adding the key to GitHub..."

# Change remote to SSH
git remote set-url origin git@github.com:AB6849/quickcom-ops-risk-monitor.git

# Test connection
echo ""
echo "Testing SSH connection..."
ssh -T git@github.com 2>&1 | head -3

# Push
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
fi
