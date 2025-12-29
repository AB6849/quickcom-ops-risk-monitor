# Quick Push - Two Options

I've set up SSH, but you need to add the key to GitHub first. Here are your options:

## Option 1: Add SSH Key (Recommended)

**Your SSH Public Key:**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBWw+zeSZLymwvgBZ/kn39j1bjmT94vjWQLiE6FSQAPx github-push
```

**Steps:**
1. Go to: https://github.com/settings/keys
2. Click "New SSH key"
3. Title: `quickcom-ops-risk-monitor`
4. Paste the key above
5. Click "Add SSH key"

**Then push:**
```bash
git push -u origin main
```

## Option 2: Use Personal Access Token (Faster)

1. **Create Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Name: `quickcom-ops-risk-monitor`
   - Check `repo` scope
   - Generate and **copy the token**

2. **Push with Token:**
   ```bash
   git remote set-url origin https://YOUR_TOKEN@github.com/AB6849/quickcom-ops-risk-monitor.git
   git push -u origin main
   ```
   (Replace `YOUR_TOKEN` with your actual token)

## After Pushing

Your repository will be at:
```
https://github.com/AB6849/quickcom-ops-risk-monitor
```

Then deploy to Streamlit Cloud:
1. Go to: https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select: `quickcom-ops-risk-monitor`
5. Main file: `dashboard.py`
6. Click "Deploy"

Your public dashboard:
```
https://YOUR-APP-NAME.streamlit.app
```

