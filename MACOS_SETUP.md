# macOS Setup Guide

## Quick Fix for "command not found: python"

On macOS, Python 3 is typically installed as `python3`, not `python`.

### Solution 1: Use `python3` (Recommended)

```bash
# Instead of: python run_pipeline.py
python3 run_pipeline.py

# Instead of: python view_outputs.py
python3 view_outputs.py
```

### Solution 2: Use Convenience Script

```bash
# Make script executable (first time only)
chmod +x run

# Then use:
./run pipeline    # Run the pipeline
./run dashboard   # Launch dashboard
./run view        # View outputs
```

### Solution 3: Create Alias (Optional)

Add to `~/.zshrc` or `~/.bash_profile`:

```bash
alias python=python3
alias pip=pip3
```

Then reload:
```bash
source ~/.zshrc  # or source ~/.bash_profile
```

## Installation Steps

### 1. Check Python Installation

```bash
python3 --version
# Should show: Python 3.x.x
```

If not installed:
```bash
# Install via Homebrew
brew install python3

# Or download from python.org
```

### 2. Install Dependencies

```bash
# Using pip3
pip3 install -r requirements.txt

# Or using python3 -m pip
python3 -m pip install -r requirements.txt
```

### 3. Set Up API Keys (Optional)

```bash
# Add to ~/.zshrc for permanent setup
echo 'export OPENWEATHER_API_KEY="your_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### 4. Run Pipeline

```bash
# Option 1: Direct command
python3 run_pipeline.py

# Option 2: Convenience script
./run pipeline
```

### 5. Launch Dashboard

```bash
# Option 1: Direct command
streamlit run dashboard.py

# Option 2: Convenience script
./run dashboard
```

## Common Issues

### Issue: "pip: command not found"

**Solution**:
```bash
python3 -m pip install -r requirements.txt
```

### Issue: "Permission denied" when running scripts

**Solution**:
```bash
chmod +x run
chmod +x daily_refresh.sh
chmod +x run_dashboard.sh
```

### Issue: "ModuleNotFoundError"

**Solution**:
```bash
# Install dependencies
pip3 install -r requirements.txt

# Or use python3 -m pip
python3 -m pip install -r requirements.txt
```

### Issue: "streamlit: command not found"

**Solution**:
```bash
pip3 install streamlit
# Or
python3 -m pip install streamlit
```

## Recommended Workflow

```bash
# 1. Install dependencies (first time)
pip3 install -r requirements.txt

# 2. Set API keys (optional)
export OPENWEATHER_API_KEY='your_key'

# 3. Run pipeline
python3 run_pipeline.py

# 4. Launch dashboard
streamlit run dashboard.py
```

## Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Now you can use 'python' instead of 'python3'
python run_pipeline.py
```

## Quick Reference

| Command | macOS/Linux | Windows |
|---------|-------------|---------|
| Run pipeline | `python3 run_pipeline.py` | `python run_pipeline.py` |
| Launch dashboard | `streamlit run dashboard.py` | `streamlit run dashboard.py` |
| View outputs | `python3 view_outputs.py` | `python view_outputs.py` |
| Install deps | `pip3 install -r requirements.txt` | `pip install -r requirements.txt` |

## Need Help?

- Check Python version: `python3 --version`
- Check pip version: `pip3 --version`
- Check installed packages: `pip3 list`
- Check script permissions: `ls -l run`

