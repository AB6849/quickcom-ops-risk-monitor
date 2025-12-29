#!/bin/bash
# Script to prepare repository for Streamlit Cloud deployment

echo "=========================================="
echo "Preparing for Streamlit Cloud Deployment"
echo "=========================================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Generate sample data
echo ""
echo "Step 1: Generating sample data..."
python3 run_pipeline.py

if [ $? -eq 0 ]; then
    echo ""
    echo "[OK] Sample data generated successfully!"
    echo ""
    echo "Step 2: Ready to commit and push to GitHub"
    echo ""
    echo "Next steps:"
    echo "1. git add ."
    echo "2. git commit -m 'Ready for Streamlit Cloud deployment'"
    echo "3. git push origin main"
    echo "4. Go to https://share.streamlit.io/ and deploy"
    echo ""
    echo "Your dashboard will be publicly accessible at:"
    echo "https://YOUR-APP-NAME.streamlit.app"
else
    echo ""
    echo "[ERROR] Failed to generate data. Check errors above."
    exit 1
fi

