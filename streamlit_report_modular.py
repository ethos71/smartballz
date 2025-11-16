#!/usr/bin/env python3
"""
Fantasy Baseball AI - Streamlit Sit/Start Report (Modular Version)

This is the main entry point that orchestrates all components.
Each major section is now in its own module for better maintainability.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import streamlit as st
import pandas as pd
import glob
from datetime import datetime

# Import component modules
from scripts.streamlit_components.config import setup_page_config, apply_custom_css, section_header
from scripts.streamlit_components.summary_metrics import render_summary_metrics
from scripts.streamlit_components.current_roster_performance import render_current_roster_performance
from scripts.streamlit_components.top_starts_sits import render_top_starts_sits

# Setup page
setup_page_config()
apply_custom_css()

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.df = None

# Auto-refresh indicator
st_autorefresh = st.sidebar.empty()
with st_autorefresh:
    refresh_interval = 300  # 5 minutes in seconds
    st.markdown(f"🔄 Auto-refresh: {refresh_interval//60} min")

# Title
st.title("⚾ Fantasy Baseball AI - Sit/Start Analysis")
st.markdown("### Last Week of 2025 Season (Sept 28, 2025)")

# Team selection and sidebar (keeping existing logic)
@st.cache_data
def load_roster_file():
    roster_files = sorted(glob.glob('data/yahoo_fantasy_rosters_*.csv'), reverse=True)
    if roster_files:
        return pd.read_csv(roster_files[0])
    return None

roster_data = load_roster_file()
selected_team = None

if roster_data is not None and 'fantasy_team' in roster_data.columns:
    available_teams = sorted(roster_data['fantasy_team'].unique().tolist())
    selected_team = st.sidebar.selectbox(
        "Select Fantasy Team",
        available_teams,
        index=0
    )
    
    st.sidebar.markdown(f"**Team:** {selected_team}")
    st.sidebar.markdown("[🔗 Open Yahoo Fantasy Baseball](https://baseball.fantasysports.yahoo.com)")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Actions")
    
    # Sidebar buttons (simplified - keeping core functionality)
    if st.sidebar.button("🔄 Rerun Analysis", use_container_width=True):
        st.sidebar.info("Running analysis...")
        # Add analysis logic here
    
    if st.sidebar.button("📥 Refresh Roster", use_container_width=True):
        st.sidebar.info("Refreshing roster...")
        # Add roster refresh logic here

# Load recommendations
rec_files = sorted(glob.glob('data/sitstart_recommendations_*.csv'), reverse=True)

if rec_files:
    latest_file = rec_files[0]
    df_summary = pd.read_csv(latest_file)
    
    # Filter by team if needed
    if selected_team:
        try:
            roster_files = sorted(glob.glob('data/yahoo_fantasy_rosters_*.csv'), reverse=True)
            if roster_files:
                roster = pd.read_csv(roster_files[0])
                if 'fantasy_team' in roster.columns:
                    team_players = roster[roster['fantasy_team'] == selected_team]['player_name'].tolist()
                    df_summary = df_summary[df_summary['player_name'].isin(team_players)]
        except:
            pass
    
    # Render Summary Metrics
    render_summary_metrics(df_summary)
    
    # Render Current Roster Performance
    @st.cache_data
    def load_roster_stats(team_filter):
        from scripts.streamlit_components.data_loaders import calculate_period_stats
        
        roster_files = sorted(glob.glob('data/yahoo_fantasy_rosters_*.csv'), reverse=True)
        if not roster_files:
            return None, None
        
        roster = pd.read_csv(roster_files[0])
        
        if team_filter and 'fantasy_team' in roster.columns:
            roster = roster[roster['fantasy_team'] == team_filter]
        
        try:
            game_logs = pd.read_csv('data/mlb_game_logs_2025.csv')
            game_logs['game_date'] = pd.to_datetime(game_logs['game_date'])
            
            target_date = pd.to_datetime('2025-09-28')
            
            stats_7d = calculate_period_stats(game_logs, roster, target_date, 7)
            stats_14d = calculate_period_stats(game_logs, roster, target_date, 14)
            stats_30d = calculate_period_stats(game_logs, roster, target_date, 30)
            
            return roster, (stats_7d, stats_14d, stats_30d)
        except:
            return roster, None
    
    roster, period_stats = load_roster_stats(selected_team)
    render_current_roster_performance(roster, period_stats)
    
    # Load full data for remaining sections
    @st.cache_data
    def load_data(filepath, team_filter):
        from scripts.streamlit_components.data_loaders import load_recommendations_data
        return load_recommendations_data(filepath, team_filter)
    
    if not st.session_state.data_loaded or st.session_state.df is None:
        with st.spinner("⏳ Loading data..."):
            df = load_data(latest_file, selected_team)
            st.session_state.df = df
            st.session_state.data_loaded = True
    else:
        df = st.session_state.df
    
    # Render Top Starts & Bottom Sits
    render_top_starts_sits(df)
    
    # TODO: Add remaining sections
    st.markdown("---")
    st.info("⚙️ Additional sections (Player Weight Breakdown, Factor Analysis, Full Rankings, Waiver Wire, Legend) coming soon...")
    
else:
    st.error("❌ No recommendations files found!")
    st.stop()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    <p>Fantasy Baseball AI | Powered by 20+ Factor Analysis | Auto-Fetched Yahoo Rosters</p>
    <p>All scores range -2 to +2 | Higher = Better matchup | Weights optimized per player</p>
</div>
""", unsafe_allow_html=True)
