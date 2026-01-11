# SmartBallz - Analysis Reports

This directory contains Streamlit dashboards and analysis reports.

## 📊 Available Reports

### Sit/Start Analysis Dashboard

**File:** `analysis_report.py`

Interactive dashboard to visualize sit/start recommendations and factor analysis results.

**Features:**
- 📊 Overview metrics and summary statistics
- 🎯 Interactive recommendations table
- 📈 Score distribution charts
- 🔍 Factor analysis breakdown
- ⭐ Top/bottom performers
- 👤 Detailed player analysis with radar charts

**Prerequisites:**

```bash
pip install streamlit plotly
```

**Usage:**

1. First, run the sit/start analysis to generate data:
   ```bash
   ./smartballz
   ```

2. Launch the Streamlit dashboard:
   ```bash
   streamlit run docs/analysis_report.py
   ```

3. Open your browser to http://localhost:8501

**Screenshots:**

The dashboard includes:
- **Overview Page**: Summary metrics and top performers
- **Recommendations Table**: Sortable, color-coded player list
- **Score Distribution**: Histogram showing performance spread
- **Factor Analysis**: Bar charts of all 20 factors
- **Player Details**: Radar chart and breakdown for each player

## 📁 File Structure

```
docs/
├── README.md                  # This file
├── analysis_report.py         # Streamlit dashboard
├── DAILY_WORKFLOW.md          # Daily usage guide
└── copilot-last-instructions.txt
```

## 🚀 Quick Start

```bash
# Install dependencies
pip install streamlit plotly

# Run analysis
./smartballz

# View results
streamlit run docs/analysis_report.py
```

## 📖 Dashboard Pages

### 1. Overview
- Total players analyzed
- Favorable/Neutral/Unfavorable counts
- Average score
- Top 10 starts and sits

### 2. Recommendations
- Full sortable table
- Color-coded scores
- Top 5 factor scores per player
- Status emojis

### 3. Score Distribution
- Histogram of all scores
- Threshold markers
- Performance categories

### 4. Factor Analysis
- Average scores per factor
- Weight information
- Color-coded bars

### 5. Top Performers
- Best 10 players to start
- Worst 10 players to sit
- Detailed recommendations

### 6. Player Details
- Individual player deep dive
- Radar chart of all factors
- Factor contribution table
- Weighted scoring breakdown

## 🎨 Color Coding

- 🌟 **Dark Green**: Very Favorable (+1.5 to +2.0)
- ✅ **Light Green**: Favorable (+0.5 to +1.5)
- ⚖️ **Yellow**: Neutral (-0.5 to +0.5)
- ⚠️ **Light Red**: Unfavorable (-1.5 to -0.5)
- 🚫 **Dark Red**: Very Unfavorable (-2.0 to -1.5)

## 🔄 Refreshing Data

After running a new analysis with `./smartballz`, simply refresh the Streamlit app in your browser to see updated results.

## 💡 Tips

- Use the sidebar to navigate between pages
- Click column headers in tables to sort
- Hover over charts for detailed information
- Select specific players for detailed analysis
- Export data using Streamlit's download features

## 🐛 Troubleshooting

**No data found:**
- Ensure you've run `./smartballz` first
- Check that `data/sitstart_recommendations_*.csv` exists

**Import errors:**
- Install missing packages: `pip install streamlit plotly pandas`

**Port already in use:**
- Specify different port: `streamlit run docs/analysis_report.py --server.port 8502`

## 📝 Future Enhancements

- [ ] Historical trend analysis
- [ ] Player comparison tool
- [ ] Factor weight tuning interface
- [ ] Waiver wire recommendations dashboard
- [ ] Export to PDF
- [ ] Email reports
