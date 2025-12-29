# GitHub Authentication Setup

You need to authenticate with GitHub to push. Here are the options:

## Option 1: Personal Access Token (PAT) - Recommended

### Step 1: Create Personal Access Token
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: `quickcom-ops-risk-monitor`
4. Select scopes: Check `repo` (full control of private repositories)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)

### Step 2: Use Token to Push
```bash
# When prompted for password, paste the token
git push -u origin main
```

Or configure git to use token:
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/AB6849/quickcom-ops-risk-monitor.git
git push -u origin main
```

## Option 2: SSH Keys (More Secure)

### Step 1: Generate SSH Key
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter to accept default location
# Optionally set a passphrase
```

### Step 2: Add SSH Key to GitHub
```bash
# Copy public key
cat ~/.ssh/id_ed25519.pub
# Copy the output
```

Then:
1. Go to: https://github.com/settings/keys
2. Click "New SSH key"
3. Paste the key
4. Click "Add SSH key"

### Step 3: Change Remote to SSH
```bash
git remote set-url origin git@github.com:AB6849/quickcom-ops-risk-monitor.git
git push -u origin main
```

## Option 3: GitHub CLI (Easiest)

```bash
# Install GitHub CLI
brew install gh

# Authenticate
gh auth login

# Then push
git push -u origin main
```

## Quick Fix: Use Token in URL

If you have a token, you can push directly:
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/AB6849/quickcom-ops-risk-monitor.git
git push -u origin main
```

Replace `YOUR_TOKEN` with your actual token.

