"""
Current Roster Performance Component

Displays roster performance stats over 7/14/30 day periods,
split by Hitters, SP, and RP.
"""

import streamlit as st
import pandas as pd
import glob
from datetime import datetime, timedelta


def render_current_roster_performance(roster, period_stats):
    """
    Render current roster performance section with tabs for different time periods
    
    Args:
        roster: DataFrame with roster data
        period_stats: Tuple of (stats_7d, stats_14d, stats_30d) DataFrames
    """
    if roster is None or period_stats is None:
        return
    
    # Header with help icon
    col_header, col_help = st.columns([0.95, 0.05])
    with col_header:
        st.markdown('<div class="section-header-container"><h2>📊 Current Roster Performance</h2></div>', unsafe_allow_html=True)
    with col_help:
        with st.popover("ℹ️"):
            st.markdown("""
        ### What You're Seeing
            
            This section shows your **actual performance statistics** over recent time periods (7/14/30 days).
            Unlike the sit/start recommendations which are **predictive**, these are **historical results**.
            
            ### Key Statistics Explained
            
            **Status:**
            - **✅ Active:** Players in your starting lineup (first ~60% of roster)
            - **🪑 Bench:** Players on your bench (last ~40% of roster)
            
            **Position:** Yahoo-style abbreviations (C, 1B, 2B, 3B, SS, OF, SP, RP, etc.)
            
            **Games:** Number of games the player appeared in during the period
            
            **Batting Stats (Hitters):**
            - **AB:** At Bats
            - **H:** Hits
            - **R:** Runs scored
            - **RBI:** Runs Batted In
            - **HR:** Home Runs
            - **SB:** Stolen Bases
            - **AVG:** Batting Average (H ÷ AB)
            - **OPS:** On-Base Plus Slugging (combines OBP + SLG)
            
            **OPS Color Gradient:**
            - 🟢 Green: High OPS (excellent performance)
            - 🟡 Yellow: Medium OPS (average performance)
            - 🔴 Red: Low OPS (poor performance)
            
            ### How to Use This Data
            
            **7-Day View:** Most recent form, use for immediate decisions
            - Hot streaks appear here first
            - Quick identification of slumping players
            
            **14-Day View:** Balanced view of recent performance
            - Filters out single-game outliers
            - Good for trend identification
            
            **30-Day View:** Broader performance context
            - Shows consistency vs volatility
            - Helps identify seasonal trends
            
            ### Real-World Example
            ```
            Player: Aaron Judge
            7-Day:  .350 AVG, 1.200 OPS (🟢 Hot - keep starting!)
            14-Day: .310 AVG, 1.050 OPS (🟢 Consistent performer)
            30-Day: .290 AVG, 0.950 OPS (🟢 Solid season)
            ```
            
            ### Tips
            - Compare across time periods to spot trends
            - Green OPS players = safer starts
            - Bench players with poor stats may need roster moves
            - Players in Yahoo roster order = same order as your Yahoo team
            """)
    
    stats_7d, stats_14d, stats_30d = period_stats
    
    # Create tabs for different periods
    tab1, tab2, tab3 = st.tabs(["Last 7 Days", "Last 14 Days", "Last 30 Days"])
    
    with tab1:
        _render_period_stats(stats_7d, "7 Days")
    
    with tab2:
        _render_period_stats(stats_14d, "14 Days")
    
    with tab3:
        _render_period_stats(stats_30d, "30 Days")
    
    st.markdown("---")


def _render_period_stats(stats_df, period_name):
    """Render stats for a specific time period"""
    if stats_df.empty:
        st.info(f"No stats available for last {period_name}")
        return
    
    # Split into Hitters and Pitchers
    hitters = stats_df[~stats_df['position'].isin(['SP', 'RP', 'SP,RP', 'P'])].copy()
    pitchers = stats_df[stats_df['position'].isin(['SP', 'RP', 'SP,RP', 'P'])].copy()
    
    # Render Hitters Section
    if not hitters.empty:
        st.markdown(f"### 🔨 Hitters - Last {period_name}")
        _render_hitters_table(hitters)
    
    # Render Pitchers Section
    if not pitchers.empty:
        st.markdown(f"### ⚾ Pitchers - Last {period_name}")
        
        # Separate SP and RP
        sp = pitchers[pitchers['position'].str.contains('SP')].copy()
        rp = pitchers[pitchers['position'].str.contains('RP') & ~pitchers['position'].str.contains('SP')].copy()
        
        if not sp.empty:
            st.markdown("**Starting Pitchers (SP)**")
            _render_pitchers_table(sp)
        
        if not rp.empty:
            st.markdown("**Relief Pitchers (RP)**")
            _render_pitchers_table(rp)


def _render_hitters_table(hitters_df):
    """Render hitters stats table"""
    # Add Yahoo player links
    try:
        roster_files = sorted(glob.glob('data/yahoo_fantasy_rosters_*.csv'), reverse=True)
        if roster_files:
            yahoo_roster = pd.read_csv(roster_files[0])
            if 'player_key' in yahoo_roster.columns:
                player_key_map = dict(zip(yahoo_roster['player_name'], yahoo_roster['player_key']))
                hitters_df['player_key'] = hitters_df['player_name'].map(player_key_map).fillna('')
                hitters_df['yahoo_link'] = hitters_df['player_key'].apply(
                    lambda pk: f"https://baseball.fantasysports.yahoo.com/b1/3119/3/{pk.split('.')[-1]}" 
                    if pk and '.' in str(pk) else ''
                )
    except:
        hitters_df['yahoo_link'] = ''
    
    # Add roster order column
    hitters_df['#'] = range(1, len(hitters_df) + 1)
    
    display_cols = ['#', 'player_name', 'yahoo_link', 'status', 'position', 'team', 'games', 'ab', 'h', 'r', 'rbi', 'hr', 'sb', 'avg', 'ops']
    hitters_display = hitters_df[[col for col in display_cols if col in hitters_df.columns]].copy()
    
    if 'avg' in hitters_display.columns:
        hitters_display['avg'] = hitters_display['avg'].round(3)
    if 'ops' in hitters_display.columns:
        hitters_display['ops'] = hitters_display['ops'].round(3)
    
    st.dataframe(
        hitters_display,
        column_config={
            "#": st.column_config.NumberColumn("#", width="small"),
            "yahoo_link": st.column_config.LinkColumn("Yahoo", display_text="🔗", width="small"),
            "avg": st.column_config.NumberColumn("AVG", format="%.3f"),
            "ops": st.column_config.NumberColumn("OPS", format="%.3f"),
        },
        use_container_width=True,
        height=400,
        hide_index=True
    )


def _render_pitchers_table(pitchers_df):
    """Render pitchers stats table"""
    # Add Yahoo player links
    try:
        roster_files = sorted(glob.glob('data/yahoo_fantasy_rosters_*.csv'), reverse=True)
        if roster_files:
            yahoo_roster = pd.read_csv(roster_files[0])
            if 'player_key' in yahoo_roster.columns:
                player_key_map = dict(zip(yahoo_roster['player_name'], yahoo_roster['player_key']))
                pitchers_df['player_key'] = pitchers_df['player_name'].map(player_key_map).fillna('')
                pitchers_df['yahoo_link'] = pitchers_df['player_key'].apply(
                    lambda pk: f"https://baseball.fantasysports.yahoo.com/b1/3119/3/{pk.split('.')[-1]}" 
                    if pk and '.' in str(pk) else ''
                )
    except:
        pitchers_df['yahoo_link'] = ''
    
    pitchers_df['#'] = range(1, len(pitchers_df) + 1)
    
    display_cols = ['#', 'player_name', 'yahoo_link', 'status', 'team', 'games']
    pitchers_display = pitchers_df[[col for col in display_cols if col in pitchers_df.columns]].copy()
    
    st.dataframe(
        pitchers_display,
        column_config={
            "#": st.column_config.NumberColumn("#", width="small"),
            "yahoo_link": st.column_config.LinkColumn("Yahoo", display_text="🔗", width="small"),
        },
        use_container_width=True,
        height=250,
        hide_index=True
    )
