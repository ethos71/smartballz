#!/usr/bin/env python3
"""
SmartBallz - Main Dashboard Hub

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
    page_title="SmartBallz Dashboard",
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
        st.caption("smartballz - SmartBallz")
    
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
    
    # Load and display FULL draft dashboard
    try:
        from reports.draft_dashboard import load_draft_data
        
        draft_data = load_draft_data()
        
        if not draft_data:
            st.warning("⚠️ No draft data found. Generate rankings first!")
            if st.button("Generate Draft Rankings", type="primary"):
                st.info("Run: `python src/reports/draft_preparation_report.py`")
            return
        
        # Show full dashboard with all tabs
        st.markdown("---")
        
        # Create all tabs
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "🌟 Value Picks",
            "🚀 Rookies & Prospects",
            "💎 Sleepers",
            "⚠️ Injury Risks",
            "💰 Auction Values",
            "📋 Draft Strategy",
            "🔒 Keeper Analysis",
            "🎯 By Position"
        ])
        
        # TAB 1: Value Picks
        with tab1:
            st.header("🌟 Top Value Picks")
            st.markdown("Players being drafted lower than their projected value")
            
            value_picks = draft_data['value_picks']
            
            if value_picks:
                for pick in value_picks:
                    col1, col2, col3 = st.columns([3, 1, 2])
                    
                    with col1:
                        st.subheader(f"{pick['player']}")
                        st.caption(f"{pick['position']} | {pick['team']}")
                    
                    with col2:
                        st.metric("ADP", pick['adp'])
                        st.metric("Should Be", pick['projected_rank'], 
                                 delta=f"-{pick['value_gap']} rounds",
                                 delta_color="inverse")
                    
                    with col3:
                        st.info(f"**Why:** {pick['reason']}")
                    
                    st.markdown("---")
        
        # TAB 2: Rookies & Prospects
        with tab2:
            st.header("🚀 Rookies & Prospects")
            
            rookies = draft_data['rookies_and_prospects']
            
            st.subheader("🌟 Ready for Opening Day")
            for player in rookies['ready_now']:
                with st.expander(f"**{player['player']}** - {player['position']}, {player['team']} (Age {player['age']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**ETA:** {player['eta']}")
                        st.write(f"**Draft Round:** {player['draft_round']}")
                        st.write(f"**Impact:** {player['projected_impact']}")
                    with col2:
                        st.write(f"**Tools:** {player['tools']}")
                        st.info(player['notes'])
        
        # TAB 3: Sleepers
        with tab3:
            st.header("💎 Sleeper Picks")
            
            for sleeper in draft_data['sleepers']:
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.subheader(f"{sleeper['player']}")
                    st.caption(f"{sleeper['position']} | {sleeper['team']}")
                    st.write(f"**Upside:** {sleeper['upside']}")
                    st.success(sleeper['reason'])
                    if 'risk' in sleeper:
                        st.warning(f"⚠️ {sleeper['risk']}")
                with col2:
                    st.metric("ADP", sleeper['adp'])
                    st.metric("Target Round", sleeper['target_round'])
                st.markdown("---")
        
        # TAB 4: Injury Risks
        with tab4:
            st.header("⚠️ Injury Risks")
            
            for risk in draft_data['injury_risks']:
                if risk['risk_level'] == 'EXTREME':
                    container = st.error
                elif risk['risk_level'] == 'HIGH':
                    container = st.warning
                else:
                    container = st.info
                
                with container(f"**{risk['player']}** - {risk['position']} (ADP {risk['adp']})"):
                    st.write(f"**Risk Level:** {risk['risk_level']}")
                    st.write(f"**History:** {risk['injury_history']}")
                    st.write(f"**Recommendation:** {risk['recommendation']}")
                st.markdown("---")
        
        # TAB 5: Auction Values
        with tab5:
            st.header("💰 Auction Draft Values")
            
            auction = draft_data['auction_values']
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("🌟 Tier 1 Studs")
                for player in auction['tier_1']:
                    st.metric(f"{player['player']} ({player['position']})", f"${player['value']}")
            
            with col2:
                st.subheader("⭐ Tier 2 Stars")
                for player in auction['tier_2']:
                    st.metric(f"{player['player']} ({player['position']})", f"${player['value']}")
            
            with col3:
                st.subheader("💎 Bargain Targets")
                for player in auction['bargain_targets']:
                    st.metric(player['player'], f"${player['value']}", 
                             delta=f"Fair: ${player['fair_value']}", delta_color="off")
        
        # TAB 6: Draft Strategy  
        with tab6:
            st.header("📋 Draft Strategy")
            
            strategy = draft_data['draft_strategy']
            
            st.subheader("🏆 Early Rounds (1-3)")
            st.write(f"**Strategy:** {strategy['early_rounds']['strategy']}")
            st.write(f"**Positions:** {', '.join(strategy['early_rounds']['positions_to_target'])}")
            st.info(strategy['early_rounds']['notes'])
            
            st.markdown("---")
            
            st.subheader("⚡ Middle Rounds (4-10)")
            st.write(f"**Strategy:** {strategy['middle_rounds']['strategy']}")
            st.write(f"**Positions:** {', '.join(strategy['middle_rounds']['positions_to_target'])}")
            st.info(strategy['middle_rounds']['notes'])
            
            st.markdown("---")
            
            st.subheader("🚀 Late Rounds (11+)")
            st.write(f"**Strategy:** {strategy['late_rounds']['strategy']}")
            st.write(f"**Positions:** {', '.join(strategy['late_rounds']['positions_to_target'])}")
            st.info(strategy['late_rounds']['notes'])
            
            st.markdown("---")
            st.subheader("🔑 Key Principles")
            for principle in strategy['key_principles']:
                st.success(f"✅ {principle}")
        
        # TAB 7: Keeper Analysis
        with tab7:
            if 'keeper_analysis' in draft_data:
                st.header("🔒 Keeper League Analysis")
                keeper = draft_data['keeper_analysis']
                
                st.subheader("📊 Positional Scarcity")
                scarcity = keeper['available_targets']['scarcity_analysis']
                
                for pos, data in scarcity.items():
                    level = data['scarcity_level']
                    color = "🔴" if level == 'EXTREME' else "🟡" if level == 'HIGH' else "🟢"
                    
                    with st.expander(f"{color} **{pos}** - {level} Scarcity"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Total Elite", data['total_elite'])
                            st.metric("Likely Kept", data['likely_kept'])
                            st.metric("Available", data['available'])
                        with col2:
                            st.info(f"**Strategy:** {data['recommendation']}")
            else:
                st.info("Keeper analysis not available")
        
        # TAB 8: By Position
        with tab8:
            if 'positional_recommendations' in draft_data:
                st.header("🎯 Recommendations by Position")
                pos_rec = draft_data['positional_recommendations']
                
                # First Base - Featured
                st.subheader("⚾ FIRST BASE - TOP PRIORITY")
                first_base = pos_rec['1B']
                
                st.error(f"**Scarcity:** {first_base['scarcity']}")
                st.success(f"**Strategy:** {first_base['strategy']}")
                
                st.write("### 🌟 Tier 1 - Best Available")
                for player in first_base['tier_1_available']:
                    with st.expander(f"**{player['player']}** ({player['team']}) - Rounds {player['target_round']}"):
                        st.write(f"**Projection:** {player['proj']}")
                        st.info(f"**Why:** {player['why']}")
                
                st.write("### ⭐ Tier 2 - Solid Options")
                for player in first_base['tier_2_targets']:
                    with st.expander(f"**{player['player']}** ({player['team']}) - Rounds {player['target_round']}"):
                        st.write(f"**Projection:** {player['proj']}")
                        st.info(f"**Why:** {player['why']}")
            else:
                st.info("Positional recommendations not available")
                
    except Exception as e:
        st.error(f"Error loading draft dashboard: {e}")
        import traceback
        st.code(traceback.format_exc())


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
