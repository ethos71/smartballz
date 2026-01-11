#!/bin/bash
# Launch the 2026 Draft Preparation Dashboard

echo "🏟️  Starting Fantasy Baseball Draft Dashboard..."
echo "=================================================="
echo ""

# Activate virtual environment
source .venv/bin/activate

# Launch Streamlit
streamlit run src/reports/draft_dashboard.py

# Note: Dashboard will open automatically in your browser
# URL: http://localhost:8501
