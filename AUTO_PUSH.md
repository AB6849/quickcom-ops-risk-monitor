# Auto-Push to GitHub

I've created a script to help you push to GitHub. Here are your options:

## Option 1: Use the Script (Easiest)

Run:
```bash
./push_to_github.sh
```

The script will:
1. Ask for your GitHub username
2. Add the remote
3. Push the code
4. Show you the repository link

## Option 2: Manual Push

If you prefer to do it manually:

### Step 1: Create Repository on GitHub
1. Go to: https://github.com/new
2. Repository name: `quickcom-ops-risk-monitor`
3. Make it **PUBLIC**
4. **Don't** initialize with README
5. Click "Create repository"

### Step 2: Push Code
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/quickcom-ops-risk-monitor.git
git branch -M main
git push -u origin main
```

### Step 3: Get Your Repository Link
After pushing, your repository will be at:
```
https://github.com/YOUR_USERNAME/quickcom-ops-risk-monitor
```

## Option 3: Install GitHub CLI (Most Automated)

If you install GitHub CLI, I can create the repo automatically:

```bash
# Install GitHub CLI (macOS)
brew install gh

# Authenticate
gh auth login

# Then I can create and push automatically
```

## After Pushing

Once your code is on GitHub:

1. **Deploy to Streamlit Cloud**:
   - Go to: https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select: `quickcom-ops-risk-monitor`
   - Main file: `dashboard.py`
   - Click "Deploy"

2. **Get Public Dashboard Link**:
   ```
   https://YOUR-APP-NAME.streamlit.app
   ```

## Current Status

✅ Git repository initialized
✅ All files committed
✅ Sample data included
✅ Ready to push

**Next**: Run `./push_to_github.sh` or follow manual steps above.

