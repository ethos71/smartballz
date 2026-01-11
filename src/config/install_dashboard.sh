#!/bin/bash
#
# Install Streamlit Dashboard Dependencies
#

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║         Installing Streamlit Dashboard Dependencies                       ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "✓ Virtual environment found"
    source .venv/bin/activate
else
    echo "⚠️  No virtual environment found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
fi

echo ""
echo "Installing packages..."
echo ""

pip install -q streamlit plotly

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                        Installation Complete! ✅                           ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "To use the dashboard:"
echo ""
echo "  1. Run analysis:"
echo "     ./smartballz"
echo ""
echo "  2. Launch dashboard:"
echo "     streamlit run docs/analysis_report.py"
echo ""
echo "  3. Open browser to: http://localhost:8501"
echo ""

