#!/usr/bin/env python3
"""
Fantasy Baseball AI - Main Dashboard Hub

Central dashboard that provides navigation between:
- Draft Preparation Dashboard (pre-season)
- Day-to-Day Season Dashboard (in-season)

Usage:
    streamlit run src/reports/main_dashboard.py
"""

import streamlit as st
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Page configuration
st.set_page_config(
    page_title="Fantasy Baseball AI Dashboard",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main dashboard hub with navigation"""
    
    # Sidebar navigation
    with st.sidebar:
        st.title("⚾ FB-AI Dashboard")
        st.markdown("---")
        
        # Dashboard selector
        dashboard_choice = st.radio(
            "Select Dashboard:",
            [
                "🏟️ Draft Preparation",
                "📊 Day-to-Day Season",
                "🏆 Postseason (Roster Lock)"
            ],
            index=0
        )
        
        st.markdown("---")
        
        # Info based on selection
        if "Draft" in dashboard_choice:
            st.info("""
            **Draft Preparation Dashboard**
            
            Pre-season analysis for 2026:
            - Player rankings by position
            - Keeper league analysis
            - Value picks & sleepers
            - Rookies & prospects
            - Auction values
            - Draft strategy
            """)
        elif "Postseason" in dashboard_choice:
            st.warning("""
            **Postseason Roster Lock**
            
            October playoffs mode:
            - 🔒 Roster is locked
            - ❌ No adds/drops allowed
            - ✅ IL replacements only
            - ⚾ Daily lineup optimization
            - 📊 Performance tracking
            - 🎯 Playoff strategy
            """)
        else:
            st.info("""
            **Day-to-Day Season Dashboard**
            
            In-season analysis:
            - Daily sit/start recommendations
            - Current roster performance
            - Factor analysis breakdown
            - Waiver wire targets
            - Matchup analysis
            - Weekly projections
            """)
        
        st.markdown("---")
        st.caption("fb-ai - Fantasy Baseball AI")
    
    # Main content based on selection
    if "Draft" in dashboard_choice:
        show_draft_dashboard()
    elif "Postseason" in dashboard_choice:
        show_postseason_dashboard()
    else:
        show_season_dashboard()


def show_draft_dashboard():
    """Display draft preparation dashboard"""
    st.title("🏟️ 2026 Draft Preparation Dashboard")
    
    st.markdown("""
    ### Welcome to the Draft Preparation Dashboard!
    
    This dashboard is optimized for **pre-season draft preparation** and includes:
    
    - 🌟 **Value Picks** - Players being drafted below their value
    - 🚀 **Rookies & Prospects** - Top newcomers to target
    - 💎 **Sleepers** - Late-round gems with upside
    - ⚠️ **Injury Risks** - Players to avoid
    - 💰 **Auction Values** - Pricing recommendations
    - 📋 **Draft Strategy** - Round-by-round guidance
    - 🔒 **Keeper Analysis** - League-specific scarcity analysis
    - 🎯 **By Position** - Detailed recommendations (1B featured!)
    
    ---
    """)
    
    # Load and display draft dashboard components
    try:
        from reports.draft_dashboard import load_draft_data
        
        draft_data = load_draft_data()
        
        if draft_data:
            # Quick stats at top
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Value Picks", len(draft_data.get('value_picks', [])))
            with col2:
                rookies = draft_data.get('rookies_and_prospects', {}).get('ready_now', [])
                st.metric("Top Rookies", len(rookies))
            with col3:
                st.metric("Sleepers", len(draft_data.get('sleepers', [])))
            with col4:
                st.metric("Injury Risks", len(draft_data.get('injury_risks', [])))
            
            st.markdown("---")
            
            # Quick action button
            st.info("💡 **Tip:** Use the full Draft Dashboard for complete analysis with all tabs and features!")
            
            if st.button("🚀 Open Full Draft Dashboard", type="primary", use_container_width=True):
                st.markdown("""
                To access the full draft dashboard with all features, run:
                ```bash
                ./launch_draft_dashboard.sh
                ```
                Or directly:
                ```bash
                streamlit run src/reports/draft_dashboard.py
                ```
                The full dashboard will open at: http://localhost:8502
                """)
        else:
            st.warning("No draft data found. Generate rankings first!")
            
            if st.button("Generate Draft Rankings"):
                st.info("Run: `python src/reports/draft_preparation_report.py`")
                
    except Exception as e:
        st.error(f"Error loading draft data: {e}")
        st.info("Make sure draft_dashboard.py is available in src/reports/")


def show_season_dashboard():
    """Display day-to-day season dashboard"""
    st.title("📊 Day-to-Day Season Dashboard")
    
    st.markdown("""
    ### Welcome to the In-Season Dashboard!
    
    This dashboard is optimized for **daily fantasy management** during the season:
    
    - ⚾ **Today's Recommendations** - Who to start/sit
    - 📈 **Roster Performance** - Track your team's stats
    - 🎯 **Factor Analysis** - Detailed player breakdowns
    - 💫 **Waiver Wire** - Best available adds
    - 📊 **Matchup Analysis** - Opponent scouting
    - 🏆 **Weekly Projections** - Plan ahead
    
    ---
    """)
    
    # Load and display season dashboard components
    try:
        from reports.streamlit_components import data_loaders
        
        st.info("""
        **Season Dashboard Features:**
        
        The day-to-day season dashboard provides:
        - Real-time sit/start analysis based on 20 factors
        - Current roster performance tracking
        - Waiver wire recommendations
        - Opponent analysis and matchup data
        - Factor weight breakdowns
        - Full player rankings
        
        💡 **Coming Soon:** Full integration with live season data!
        """)
        
        # Placeholder for season data
        st.warning("⚠️ Season dashboard will be active once 2026 season starts!")
        
        if st.button("🚀 Open Full Season Dashboard", type="primary", use_container_width=True):
            st.markdown("""
            To access the full season dashboard, run:
            ```bash
            streamlit run src/reports/day_to_day_season.py
            ```
            The dashboard will open at: http://localhost:8503
            """)
        
    except Exception as e:
        st.error(f"Error loading season dashboard: {e}")
        st.info("Season dashboard components will be available during the season.")


def show_postseason_dashboard():
    """Display postseason roster lock dashboard"""
    st.title("🏆 Postseason Roster Lock Analysis")
    
    st.markdown("""
    ### Welcome to the Postseason Dashboard!
    
    This dashboard is optimized for **playoff fantasy management** with roster lock:
    
    - 🔒 **Locked Roster** - View all available players
    - 🏥 **IL Monitor** - Track injuries for replacement opportunities
    - ⚾ **Daily Lineups** - Optimize with current roster only
    - 📊 **Performance Tracking** - Monitor postseason stats
    - 🎯 **Playoff Strategy** - Maximize locked roster potential
    
    ---
    
    ### 🚨 Postseason Rules:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error("""
        **❌ NO ADDS/DROPS**
        
        Roster is locked.
        Cannot add players
        from waiver wire.
        """)
    
    with col2:
        st.success("""
        **✅ IL ONLY**
        
        Can replace players
        who go on Injured List.
        Must be official IL.
        """)
    
    with col3:
        st.info("""
        **🎯 OPTIMIZE**
        
        Set best lineup daily.
        Leverage matchups.
        Track injuries closely.
        """)
    
    st.markdown("---")
    
    # Load postseason dashboard
    try:
        st.info("""
        **Postseason Dashboard Features:**
        
        The roster lock dashboard provides:
        - Complete locked roster view with player status
        - IL monitoring and replacement tracking
        - Daily lineup optimization recommendations
        - Postseason performance analytics
        - Playoff-specific strategy guides
        
        💡 **Critical:** Check IL status daily for replacement opportunities!
        """)
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Roster Size", 25, help="Total players locked")
        with col2:
            st.metric("On IL", 0, delta=0, help="Players you can replace")
        with col3:
            st.metric("Days Since Lock", 15, help="Postseason days elapsed")
        with col4:
            st.metric("Games Remaining", 8, help="Matchups left")
        
        st.markdown("---")
        
        if st.button("🚀 Open Full Postseason Dashboard", type="primary", use_container_width=True):
            st.markdown("""
            To access the full postseason dashboard with all features, run:
            ```bash
            streamlit run src/reports/postseason_report.py
            ```
            The dashboard will open at: http://localhost:8504
            
            **Features include:**
            - Complete roster view with status indicators
            - IL replacement candidate rankings
            - Daily lineup recommendations by matchup
            - Performance tracking and analytics
            - Playoff strategy optimization tools
            """)
        
    except Exception as e:
        st.error(f"Error loading postseason dashboard: {e}")
        st.info("Postseason dashboard will be available during playoffs.")


if __name__ == "__main__":
    main()
