# Fantasy Baseball AI - Dashboard Demo

## 🎯 Dashboard Overview

The Fantasy Baseball AI Streamlit dashboard provides comprehensive sit/start recommendations powered by 20 factor analyses across 1,106+ MLB players.

**Access:** http://localhost:8501

---

## 📊 Dashboard Sections

### 1. Summary Metrics
View at-a-glance performance metrics for today's recommended starts:
- **Total Recommended Starts**
- **Average Confidence Score**
- **High Confidence Plays** (>75%)
- **Top Factor Contributions**

### 2. Current Roster Performance
Interactive table showing your rostered players with:
- Player names and positions
- Weighted scores across all 20 factors
- Confidence levels
- **Sit/Start recommendations**

**Features:**
- ✓ Sortable columns
- ✓ Color-coded confidence (Green: Start, Red: Sit)
- ✓ Filter by position

### 3. Top Starts & Sits
**Top 10 Starts:** Players with the highest weighted scores
**Top 10 Sits:** Players with the lowest weighted scores

Each entry shows:
- Player name and team
- Weighted score
- Key contributing factors
- Matchup details

### 4. Player Weight Breakdown
Deep dive into individual player analysis:
- Select any player from dropdown
- View all 20 factor scores
- See factor weights applied
- Understand recommendation reasoning

**20 Factor Analyses Include:**
1. Wind Analysis
2. Historical Matchup
3. Home/Away Venue
4. Rest Day Impact
5. Injury/Recovery
6. Umpire Strike Zone
7. Platoon Advantage
8. Temperature
9. Pitch Mix
10. Park Factors
11. Lineup Position
12. Time of Day
13. Defensive Positions
14. Recent Form/Streaks
15. Bullpen Fatigue
16. Humidity & Elevation
17. Monthly Splits
18. Team Momentum
19. Statcast Metrics
20. Vegas Odds

### 5. Factor Analysis Details
Explore specific factor analyses:
- Choose from 20 different analyses
- View raw scores for all players
- Filter and sort results
- Download data as CSV

### 6. Full Rankings
Complete player rankings with:
- All rostered players ranked by score
- Comprehensive factor breakdown
- Export functionality

### 7. Waiver Wire Recommendations
**Powered by 1,106 player analysis**
- Top waiver wire targets for the week
- Players with favorable upcoming schedules
- Coors Field advantage plays
- Drop candidates from your roster

**Key Features:**
- Schedule analysis (next 7-14 days)
- Park factor advantages
- Matchup favorability
- Improvement over current roster

### 8. Opponent Analysis
Analyze opponent rosters:
- Load opponent's roster
- Compare against your team
- Identify strengths/weaknesses
- Strategic matchup planning

---

## 🚀 Quick Start

1. **Start the Dashboard:**
   ```bash
   streamlit run streamlit_report.py
   ```

2. **Access the Dashboard:**
   Open http://localhost:8501 in your browser

3. **Navigate Sections:**
   - Use the sidebar to jump between analyses
   - Click on player names for detailed breakdowns
   - Export data using download buttons

4. **Make Decisions:**
   - Review Summary Metrics for quick overview
   - Check Top Starts/Sits for easy decisions
   - Dive into Player Weight Breakdown for complex cases
   - Use Waiver Wire section for weekly pickups

---

## 📈 Performance

- **Analysis Speed:** 2.2 minutes for 1,106 players
- **Data Coverage:** All 30 MLB teams
- **Update Frequency:** Run daily or before game time
- **Factor Analyses:** 20 comprehensive factors

---

## 🎥 Demo Screenshots

<!-- Add screenshots here -->
<!-- Example structure:

### Dashboard Home
![Dashboard Overview](docs/screenshots/dashboard-home.png)

### Sit/Start Recommendations
![Sit Start](docs/screenshots/sit-start.png)

### Waiver Wire Analysis
![Waiver Wire](docs/screenshots/waiver-wire.png)

### Player Breakdown
![Player Analysis](docs/screenshots/player-breakdown.png)

-->

---

## 💡 Pro Tips

1. **Daily Workflow:**
   - Run `python src/scripts/roster/daily_sitstart.py` 30 minutes before first pitch
   - Review dashboard for sit/start decisions
   - Check waiver wire section for weekly pickups

2. **Deep Analysis:**
   - Use Player Weight Breakdown to understand close calls
   - Compare similar players side-by-side
   - Review Factor Analysis Details for specific situations

3. **Waiver Strategy:**
   - Focus on players with Coors Field games
   - Look for favorable 7-day schedules
   - Check opponent matchups (Vegas odds factor)

4. **Customization:**
   - Adjust factor weights in config files
   - Run backtests to optimize weights for your league
   - Export data for external analysis

---

## 🔧 Technical Details

**Built With:**
- Streamlit (Interactive Dashboard)
- Pandas (Data Processing)
- Python 3.12+

**Data Sources:**
- MLB Schedule & Stats
- Weather Data
- Vegas Odds
- Statcast Metrics

**Refresh Rate:** Real-time dashboard updates as analysis files are generated

---

## 📝 Notes

- Dashboard uses most recent analysis files from `data/` directory
- All 20 factor analyses must complete for full recommendations
- Run `src/scripts/fa/run_all_fa.py` to regenerate analysis data
- Waiver wire analysis uses 14-day schedule window for optimal performance

---

*For detailed setup and configuration, see main [README.md](../README.md)*
