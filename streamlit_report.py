#!/usr/bin/env python3
"""
Fantasy Baseball AI - Streamlit Sit/Start Report (Modular Version)
Interactive dashboard for sit/start recommendations

This is the modular version - all major sections extracted into components.
"""

import streamlit as st
import pandas as pd
import sys
import glob
import os
from datetime import datetime
import subprocess
import time

# Add src to path for imports
sys.path.insert(0, 'src')

# Import components
from scripts.streamlit_components.config import setup_page_config, apply_custom_css
from scripts.streamlit_components.data_loaders import (
    load_roster_file, 
    load_recommendations,
    get_available_teams,
    load_recommendations_data
)
from scripts.streamlit_components.summary_metrics import render_summary_metrics
from scripts.streamlit_components.current_roster_performance import render_current_roster_performance
from scripts.streamlit_components.top_starts_sits import render_top_starts_sits
from scripts.streamlit_components.player_weight_breakdown import render_player_weight_breakdown
from scripts.streamlit_components.factor_analysis import render_factor_analysis
from scripts.streamlit_components.full_rankings import render_full_rankings
from scripts.streamlit_components.waiver_wire_section import render_waiver_wire
from scripts.streamlit_components.opponent_analysis_section import render_opponent_analysis
from scripts.opponent_analysis import analyze_opponent_roster

# Page config
st.set_page_config(
    page_title="FB-AI Sit/Start Report",
    page_icon="⚾",
    layout="wide"
)

# Apply custom CSS
st.markdown("""
<style>
    /* Section container with border */
    .section-container {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 0;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    /* Section header with border */
    .section-header-container {
        background-color: transparent;
        padding: 15px 20px;
        border-bottom: 2px solid #e0e0e0;
        margin: 0;
    }
    .section-header-container h2 {
        margin: 0;
        padding: 0;
        color: #1f1f1f;
    }
    
    /* Section content area */
    .section-content {
        padding: 20px;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Helper function for styled section headers
def section_header(text, icon=""):
    st.markdown(f'<div class="section-header-container"><h2>{icon} {text}</h2></div>', unsafe_allow_html=True)

# Auto-refresh every 5 minutes
st_autorefresh = st.sidebar.empty()
with st_autorefresh:
    refresh_interval = 300  # 5 minutes in seconds
    st.markdown(f"🔄 Auto-refresh: {refresh_interval//60} min")
    time.sleep(0.1)

# Check if waiver wire needs to be run (daily at 8am) - NON-BLOCKING
def check_and_run_daily_waiver():
    """Check if waiver wire analysis needs to run, show button if needed"""
    from datetime import datetime, time as dtime
    import os
    
    waiver_files = sorted(glob.glob('data/waiver_wire_*.csv'), reverse=True)
    now = datetime.now()
    today_8am = datetime.combine(now.date(), dtime(8, 0))
    
    should_run = False
    
    if not waiver_files:
        if now >= today_8am:
            should_run = True
    else:
        latest_file = waiver_files[0]
        file_mtime = datetime.fromtimestamp(os.path.getmtime(latest_file))
        if file_mtime < today_8am and now >= today_8am:
            should_run = True
    
    if should_run:
        st.sidebar.warning("⚠️ Waiver wire data needs update")
        if st.sidebar.button("🔄 Run Waiver Wire Analysis", key="btn_daily_waiver"):
            with st.sidebar:
                with st.spinner("Running waiver wire analysis..."):
                    try:
                        subprocess.run(
                            ["python3", "src/scripts/daily_sitstart.py", "--date", "2025-09-28", "--skip-tune"],
                            cwd="/home/dominick/workspace/fantasy-baseball-ai",
                            check=True,
                            capture_output=True
                        )
                        st.success("✅ Daily waiver wire analysis complete!")
                        st.rerun()
                    except subprocess.CalledProcessError as e:
                        st.error(f"❌ Waiver wire analysis failed: {e}")


# Title
st.title("⚾ Fantasy Baseball AI - Sit/Start Analysis")
st.markdown("### Last Week of 2025 Season (Sept 28, 2025)")

# Get file metadata for sidebar (moved up to display at top)
rec_files_for_sidebar = sorted(glob.glob('data/sitstart_recommendations_*.csv'), reverse=True)
if rec_files_for_sidebar:
    latest_file_for_sidebar = rec_files_for_sidebar[0]
    file_timestamp = latest_file_for_sidebar.split('_')[-2] + '_' + latest_file_for_sidebar.split('_')[-1].replace('.csv', '')
    file_date = datetime.strptime(file_timestamp, '%Y%m%d_%H%M%S')
    
    st.sidebar.markdown(f"**Analysis Date:** {file_date.strftime('%Y-%m-%d %I:%M %p')}")
    st.sidebar.markdown(f"**File:** `{os.path.basename(latest_file_for_sidebar)}`")
    st.sidebar.markdown("---")

# Load roster to get team names
roster_data = load_roster_file()
if roster_data is not None and 'fantasy_team' in roster_data.columns:
    available_teams = sorted(roster_data['fantasy_team'].unique().tolist())
    selected_team = st.sidebar.selectbox(
        "Select Fantasy Team",
        available_teams,
        index=0
    )
    
    # Add Yahoo Fantasy link
    st.sidebar.markdown(f"**Team:** {selected_team}")
    st.sidebar.markdown("[🔗 Open Yahoo Fantasy Baseball](https://baseball.fantasysports.yahoo.com)")
    
    # Add action buttons
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Actions")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.sidebar.button("🔄 Rerun Analysis", help="Regenerate recommendations with current settings", use_container_width=True, key="btn_rerun"):
            st.sidebar.info("Rerun analysis functionality - implementation in progress")
    
    with col2:
        if st.sidebar.button("📥 Refresh Data", help="Reload data from files", use_container_width=True, key="btn_refresh"):
            st.cache_data.clear()
            st.rerun()
    
    # Waiver Wire Button - full width under other buttons
    # Check for ongoing all-player analysis
    def check_all_player_analysis_progress():
        """Check if all-player analysis is running and return progress"""
        import subprocess as sp
        
        # Check if process is running
        try:
            result = sp.run(['pgrep', '-f', 'run_all_fa.py --all-players'], 
                          capture_output=True, text=True)
            if result.returncode != 0:
                return None  # Not running
            
            # Count completed files
            all_player_files = sorted(glob.glob('data/*all_players_2025*.csv'))
            # Exclude the source data file
            all_player_files = [f for f in all_player_files if 'mlb_all_players' not in f]
            completed = len(all_player_files)
            
            # Try to get current step from log
            try:
                with open('/tmp/all_players_run_fixed.log', 'r') as f:
                    lines = f.readlines()
                    for line in reversed(lines[-50:]):
                        if '/20' in line and line.strip().startswith(tuple('0123456789')):
                            current_step = line.strip()
                            break
                    else:
                        current_step = "Processing..."
            except:
                current_step = "Processing..."
            
            return {
                'completed': completed,
                'total': 20,
                'current_step': current_step
            }
        except:
            return None
    
    progress = check_all_player_analysis_progress()
    
    if progress:
        # Analysis is running - show progress
        progress_pct = progress['completed'] / progress['total']
        st.sidebar.info(f"⏳ All-Player Analysis Running")
        st.sidebar.progress(progress_pct, text=f"{progress['completed']}/20 factors complete")
        st.sidebar.caption(f"📊 {progress['current_step']}")
        
        if st.sidebar.button("🔍 Waiver Wire (Analysis in Progress)", 
                           help="All-player analysis must complete first", 
                           use_container_width=True, 
                           key="btn_waiver",
                           disabled=True):
            pass
    else:
        # Check if analysis has been run
        all_player_files = sorted(glob.glob('data/*all_players_2025*.csv'))
        all_player_files = [f for f in all_player_files if 'mlb_all_players' not in f]
        
        if len(all_player_files) >= 20:
            # Analysis complete - show status
            st.sidebar.success(f"✅ All-Player Analysis Complete ({len(all_player_files)} factors)")
            button_text = "🔍 Waiver Wire"
        else:
            # Not run yet
            st.sidebar.warning(f"⚠️ Run all-player analysis first ({len(all_player_files)}/20 factors)")
            button_text = "🔍 Waiver Wire (Need Analysis)"
        
        if st.sidebar.button(button_text, help="Analyze top free agents", use_container_width=True, key="btn_waiver"):
            st.sidebar.info("Running waiver wire analysis...")

    
    # Opponent Analysis Button
    if st.sidebar.button("🎯 Analyze Opponent", help="Run 20-factor analysis on your weekly matchup opponent", use_container_width=True, key="btn_opponent"):
        with st.spinner(f"Analyzing opponent roster for {selected_team}..."):
            # Extract league_id and team_key from selected team if needed
            # For now, we'll use session state to store the result
            opponent_df = analyze_opponent_roster(
                league_id=st.session_state.get('league_id', ''),
                my_team_key=st.session_state.get('team_key', selected_team)
            )
            if opponent_df is not None:
                st.session_state['opponent_analysis'] = opponent_df
                st.session_state['opponent_name'] = opponent_df['opponent_team'].iloc[0] if len(opponent_df) > 0 else "Unknown"
                st.success(f"✅ Opponent analysis complete! Analyzed {len(opponent_df)} players")
                st.rerun()
            else:
                st.error("❌ Failed to analyze opponent roster")
    
    # Check if daily waiver wire analysis needs to run
    check_and_run_daily_waiver()

else:
    st.error("❌ No roster data found! Please ensure Yahoo roster data is available.")
    st.stop()
    selected_team = None

# Load recommendations
rec_files = sorted(glob.glob('data/sitstart_recommendations_*.csv'), reverse=True)
if not rec_files:
    st.error("❌ No recommendations files found!")
    st.stop()

latest_file = rec_files[0]

# Load data for summary metrics
if 'df_summary' not in st.session_state:
    with st.spinner("Loading recommendations..."):
        st.session_state.df_summary = load_recommendations_data(latest_file, selected_team)

df_summary = st.session_state.df_summary

# SECTION 1: Summary Metrics
render_summary_metrics(df_summary)

st.markdown("---")

# SECTION 2: Current Roster Performance
# Load roster and stats (inline from original - this section needs its own data)
@st.cache_data
def load_roster_stats(team_filter):
    from datetime import timedelta
    
    # Get latest roster
    roster_files = sorted(glob.glob('data/yahoo_fantasy_rosters_*.csv'), reverse=True)
    if not roster_files:
        return None, None
    
    roster = pd.read_csv(roster_files[0])
    
    # Filter by fantasy team
    if team_filter and 'fantasy_team' in roster.columns:
        roster = roster[roster['fantasy_team'] == team_filter]
    
    # Load game logs
    try:
        game_logs = pd.read_csv('data/mlb_game_logs_2025.csv')
        game_logs['game_date'] = pd.to_datetime(game_logs['game_date'])
        
        # Calculate stats for last 7, 14, 30 days from Sept 28
        target_date = pd.to_datetime('2025-09-28')
        
        # Use helper from data_loaders
        from scripts.streamlit_components.data_loaders import calculate_period_stats
        
        stats_7d = calculate_period_stats(game_logs, roster, target_date, 7)
        stats_14d = calculate_period_stats(game_logs, roster, target_date, 14)
        stats_30d = calculate_period_stats(game_logs, roster, target_date, 30)
        
        return roster, (stats_7d, stats_14d, stats_30d)
    except:
        return roster, None

roster, period_stats = load_roster_stats(selected_team)
render_current_roster_performance(roster, period_stats)

# SECTION 3: Top Starts & Bottom Sits
render_top_starts_sits(df_summary)

# SECTION 4: Player Weight Breakdown
render_player_weight_breakdown(df_summary)

# SECTION 5: Factor Analysis
render_factor_analysis(df_summary)

# SECTION 6: Full Player Rankings
render_full_rankings(df_summary)

# SECTION 7: Waiver Wire
render_waiver_wire()

# SECTION 8: Opponent Analysis (if available)
if 'opponent_analysis' in st.session_state and st.session_state['opponent_analysis'] is not None:
    render_opponent_analysis(
        st.session_state['opponent_analysis'],
        st.session_state.get('opponent_name', 'Opponent Team')
    )

# SECTION 9: Factor Analysis Legend
st.markdown("---")
st.markdown("## 📖 Factor Analysis Legend")
st.markdown("---")

with st.expander("ℹ️ View Complete Factor Descriptions", expanded=False):
    st.markdown("""
    ### Understanding the 20+ Factors That Drive Sit/Start Decisions
    
    Each factor is assigned a weight based on its historical importance to player performance. 
    The weighted factors combine to create your final sit/start score.
    
    ---
    
    #### 🎰 High Impact Factors (15-20% weight)
    
    **Vegas (15-20%)**
    - **What it measures:** Betting market expectations for game outcomes
    - **Data sources:** Over/Under totals, implied team runs, win probability
    - **Why it matters:** Vegas lines aggregate all available information and are highly predictive
    - **Example:** A team with 5.5 implied runs is a much better play than one with 3.0 runs
    
    ---
    
    #### 📊 Major Impact Factors (10-15% weight)
    
    **Statcast (10-15%)**
    - **What it measures:** Advanced batted ball and pitch quality metrics
    - **Data sources:** Exit velocity, barrel rate, hard-hit %, xBA, xSLG, expected stats
    - **Why it matters:** Shows true underlying skill independent of luck
    - **Example:** A hitter with 95+ mph avg exit velo is elite even if batting .240
    
    ---
    
    #### ⚾ Moderate Impact Factors (8-12% weight)
    
    **Matchup (8-12%)**
    - **What it measures:** Historical performance vs specific pitcher/team
    - **Data sources:** Career stats vs opponent, recent matchup history
    - **Why it matters:** Some players consistently mash certain pitchers
    - **Example:** Player hitting .400 with 3 HR in 10 career AB vs today's starter
    
    **Bullpen (8-12%)**
    - **What it measures:** Opponent bullpen strength and fatigue
    - **Data sources:** Bullpen ERA, recent usage, days since rest
    - **Why it matters:** Weak/tired bullpens lead to more runs late in games
    - **Example:** Bullpen that pitched 3 straight days is vulnerable
    
    **Platoon (8-12%)**
    - **What it measures:** Left/Right handedness matchup advantages
    - **Data sources:** L vs R and R vs L splits for both hitters and pitchers
    - **Why it matters:** Some players have massive platoon splits (100+ OPS points)
    - **Example:** Lefty hitter facing RHP when he hits .310 vs RHP but .220 vs LHP
    
    ---
    
    #### 🏟️ Notable Impact Factors (5-8% weight)
    
    **Home/Away (5-8%)**
    - **What it measures:** Home field advantage and venue familiarity
    - **Data sources:** Home vs road splits for players and teams
    - **Why it matters:** Many players perform significantly better at home
    - **Example:** Hitter with .280 avg at home vs .240 on road
    
    **Injury (5-8%)**
    - **What it measures:** Player health status and injury recovery
    - **Data sources:** DTD status, recently returned from IL, injury reports
    - **Why it matters:** Injured or recently injured players underperform
    - **Example:** Player returning from IL may be limited or rusty
    
    **Park (5-8%)**
    - **What it measures:** Ballpark dimensions and run-scoring environment
    - **Data sources:** Park factors for runs, HRs, dimensions, altitude
    - **Why it matters:** Coors Field vs Petco Park is a huge difference
    - **Example:** Game in Coors (high altitude) = +20% run scoring
    
    **Recent Form (5-8%)**
    - **What it measures:** Last 7/14/30 day performance trends
    - **Data sources:** Rolling averages of key stats
    - **Why it matters:** Hot/cold streaks tend to persist short-term
    - **Example:** Player hitting .350 with 5 HR in last 14 days is on fire
    
    **Wind (5-8%)**
    - **What it measures:** Wind speed and direction impact on ball flight
    - **Data sources:** Weather forecasts, wind speed/direction at game time
    - **Why it matters:** Wind blowing out helps offense, in helps pitchers
    - **Example:** 15 mph wind blowing out to center = more HRs
    
    ---
    
    #### 📈 Supporting Impact Factors (3-5% weight)
    
    **Rest (3-5%)**
    - **What it measures:** Days off since last game
    - **Data sources:** Game logs, rest days
    - **Why it matters:** Fresh players perform better, especially power hitters
    - **Example:** Player after 2 days rest vs playing 10 straight
    
    **Temperature (3-5%)**
    - **What it measures:** Game-time temperature
    - **Data sources:** Weather forecasts
    - **Why it matters:** Warmer weather = ball travels farther
    - **Example:** 85°F game vs 55°F game = 10-15 ft difference on fly balls
    
    **Lineup (3-5%)**
    - **What it measures:** Batting order position
    - **Data sources:** Published lineups
    - **Why it matters:** 1-3 hitters get ~1 more AB per game than 7-9
    - **Example:** Leadoff hitter gets ~4.5 PA vs cleanup ~4.2 vs #9 ~3.8
    
    **Umpire (3-5%)**
    - **What it measures:** Home plate umpire strike zone tendencies
    - **Data sources:** Umpire scorecards, historical zone data
    - **Why it matters:** Some umps call +1 inch larger/smaller zone
    - **Example:** Umpire with tight zone favors hitters; large zone favors pitchers
    
    **Pitch Mix (3-5%)**
    - **What it measures:** How pitcher's arsenal matches hitter's strengths/weaknesses
    - **Data sources:** Pitch type frequencies, hitter results vs pitch types
    - **Why it matters:** Some hitters crush fastballs but struggle vs breaking balls
    - **Example:** Fastball hitter vs pitcher who throws 70% offspeed
    
    ---
    
    #### 🔍 Minor Impact Factors (1-3% weight)
    
    **Time (1-3%)**
    - **What it measures:** Day vs night game performance
    - **Data sources:** Day/night splits
    - **Why it matters:** Some players have significant day/night splits
    - **Example:** Player hitting .290 in day games vs .250 at night
    
    **Humidity (1-3%)**
    - **What it measures:** Humidity and elevation effects on ball flight
    - **Data sources:** Weather data, stadium altitude
    - **Why it matters:** High humidity = thicker air = less distance
    - **Example:** 90% humidity in Miami vs 20% in Denver
    
    **Defense (1-3%)**
    - **What it measures:** Defensive positioning and opponent defense quality
    - **Data sources:** Shift data, team defensive metrics
    - **Why it matters:** Better defense = fewer hits allowed
    - **Example:** Playing vs elite defensive team reduces BABIP
    
    **Monthly (1-3%)**
    - **What it measures:** Performance by calendar month
    - **Data sources:** April/May/June/July/Aug/Sept splits
    - **Why it matters:** Some players are slow/hot starters
    - **Example:** Player with .320 Aug average but .250 April average
    
    **Momentum (1-3%)**
    - **What it measures:** Team win/loss streaks
    - **Data sources:** Recent team performance
    - **Why it matters:** Teams on hot streaks tend to continue briefly
    - **Example:** Team on 7-game win streak has confidence boost
    
    ---
    
    ### 💡 How to Use These Scores:
    
    - **+2.0 or higher:** 🌟 Elite matchup - MUST START
    - **+0.5 to +2.0:** ✅ Favorable - Strong start candidate  
    - **-0.5 to +0.5:** ⚖️ Neutral - Consider other factors (roster depth, categories)
    - **-2.0 to -0.5:** ⚠️ Unfavorable - Bench candidate
    - **Below -2.0:** 🚫 Terrible matchup - BENCH
    
    ### 🎯 Key Insights:
    
    1. **Weights are auto-tuned** based on historical performance for your specific players
    2. **Factors work together** - one strong positive can't overcome multiple negatives
    3. **Context matters** - a -0.3 score for your worst bench player is different than for your ace
    4. **Trust the data** - the model uses 3+ years of historical data for optimization
    5. **Check the details** - click on individual players to see which factors are driving their score
    
    ---
    
    **Remember:** These factors are weighted and combined using machine learning (XGBoost) to produce 
    the most accurate sit/start predictions possible. The system learns from thousands of games to 
    understand which factors matter most for each player type.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><strong>Fantasy Baseball AI</strong> | Powered by 20+ Factor Analysis | Auto-Fetched Yahoo Rosters</p>
    <p style="font-size: 0.9em;">All scores range -2 to +2 | Higher = Better matchup | Weights optimized per player</p>
</div>
""", unsafe_allow_html=True)
