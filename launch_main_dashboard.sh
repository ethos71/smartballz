#!/bin/bash
# Launch the Main Fantasy Baseball AI Dashboard Hub

echo "⚾ Starting Fantasy Baseball AI Dashboard Hub..."
echo "=================================================="
echo ""

# Activate virtual environment
source .venv/bin/activate

# Launch Streamlit main dashboard
streamlit run src/reports/main_dashboard.py

# Note: Dashboard will open automatically in your browser
# URL: http://localhost:8501
