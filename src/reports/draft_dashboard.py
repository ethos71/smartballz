#!/usr/bin/env python3
"""
Streamlit Draft Preparation Dashboard

Interactive dashboard for viewing 2026 draft preparation analysis.
Includes ability to regenerate rankings on demand.

Usage:
    streamlit run src/reports/draft_dashboard.py
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
import sys
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from reports.draft_preparation_report import DraftPreparationReport


# Page configuration
st.set_page_config(
    page_title="2026 Draft Preparation Dashboard",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_draft_data():
    """Load the latest draft report data"""
    data_file = Path("data/draft_report_2026.json")
    if data_file.exists():
        with open(data_file, 'r') as f:
            return json.load(f)
    return None


def generate_new_report():
    """Generate a new draft report"""
    with st.spinner("🔄 Generating new draft analysis..."):
        report = DraftPreparationReport()
        draft_data = report.generate_full_report()
        report.export_to_json()
        return draft_data


def main():
    """Main dashboard"""
    
    # Header
    st.title("⚾ 2026 Fantasy Baseball Draft Preparation")
    st.markdown("---")
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎛️ Controls")
        
        if st.button("🔄 Regenerate Rankings", use_container_width=True, type="primary"):
            draft_data = generate_new_report()
            st.session_state['draft_data'] = draft_data
            st.success("✅ Rankings updated!")
            st.rerun()
        
        st.markdown("---")
        
        st.header("📊 Quick Stats")
        draft_data = load_draft_data()
        if draft_data:
            st.metric("Value Picks", len(draft_data['value_picks']))
            st.metric("Top Rookies", len(draft_data['rookies_and_prospects']['ready_now']))
            st.metric("Sleepers", len(draft_data['sleepers']))
            st.metric("Injury Risks", len(draft_data['injury_risks']))
            
            gen_date = datetime.fromisoformat(draft_data['generated_date'])
            st.caption(f"Last updated: {gen_date.strftime('%b %d, %Y %I:%M %p')}")
        
        st.markdown("---")
        st.header("📁 Resources")
        st.markdown("""
        - [Full Report](../../data/draft_report_2026.json)
        - [Prep Guide](../../docs/2026_SEASON_PREPARATION.md)
        - [Cheat Sheet](../../docs/DRAFT_CHEAT_SHEET_2026.md)
        """)
    
    # Load data
    draft_data = load_draft_data()
    
    if not draft_data:
        st.error("❌ No draft data found. Click 'Regenerate Rankings' to create.")
        return
    
    # Main content tabs
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
        else:
            st.info("No value picks identified yet")
    
    # TAB 2: Rookies & Prospects
    with tab2:
        st.header("🚀 Rookies & Prospects")
        
        rookies = draft_data['rookies_and_prospects']
        
        # Ready Now
        st.subheader("🌟 Ready for Opening Day")
        ready_now = rookies['ready_now']
        
        if ready_now:
            for player in ready_now:
                with st.expander(f"**{player['player']}** - {player['position']}, {player['team']} (Age {player['age']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**ETA:** {player['eta']}")
                        st.write(f"**Draft Round:** {player['draft_round']}")
                        st.write(f"**Impact:** {player['projected_impact']}")
                    
                    with col2:
                        st.write(f"**Tools:** {player['tools']}")
                        st.info(player['notes'])
        
        st.markdown("---")
        
        # Call-Up Candidates
        st.subheader("📅 Mid-Season Call-Up Candidates")
        callups = rookies['call_up_candidates']
        
        if callups:
            for player in callups:
                with st.expander(f"**{player['player']}** - {player['position']}, {player['team']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**ETA:** {player['eta']}")
                        st.write(f"**Draft Round:** {player['draft_round']}")
                    
                    with col2:
                        st.write(f"**Tools:** {player['tools']}")
                        st.info(player['notes'])
        
        st.markdown("---")
        
        # Dynasty Targets
        st.subheader("🏆 Dynasty League Targets")
        dynasty = rookies['dynasty_targets']
        
        if dynasty:
            for player in dynasty:
                with st.expander(f"**{player['player']}** - {player['position']}, {player['team']}"):
                    st.write(f"**ETA:** {player['eta']}")
                    st.write(f"**Tools:** {player['tools']}")
                    st.write(f"**Impact:** {player['projected_impact']}")
                    st.info(player['notes'])
    
    # TAB 3: Sleepers
    with tab3:
        st.header("💎 Sleeper Picks")
        st.markdown("Late-round gems with high upside potential")
        
        sleepers = draft_data['sleepers']
        
        if sleepers:
            for sleeper in sleepers:
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
        else:
            st.info("No sleepers identified yet")
    
    # TAB 4: Injury Risks
    with tab4:
        st.header("⚠️ Injury Risks")
        st.markdown("Players to avoid or draft with extreme caution")
        
        injury_risks = draft_data['injury_risks']
        
        if injury_risks:
            for risk in injury_risks:
                # Color code by risk level
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
        else:
            st.info("No major injury risks identified")
    
    # TAB 5: Auction Values
    with tab5:
        st.header("💰 Auction Draft Values")
        st.markdown("Recommended spending for $260 budget")
        
        auction = draft_data['auction_values']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🌟 Tier 1 Studs")
            for player in auction['tier_1']:
                st.metric(
                    label=f"{player['player']} ({player['position']})",
                    value=f"${player['value']}"
                )
        
        with col2:
            st.subheader("⭐ Tier 2 Stars")
            for player in auction['tier_2']:
                st.metric(
                    label=f"{player['player']} ({player['position']})",
                    value=f"${player['value']}"
                )
        
        with col3:
            st.subheader("💎 Bargain Targets")
            for player in auction['bargain_targets']:
                st.metric(
                    label=player['player'],
                    value=f"${player['value']}",
                    delta=f"Fair: ${player['fair_value']}",
                    delta_color="off"
                )
    
    # TAB 6: Draft Strategy
    with tab6:
        st.header("📋 Draft Strategy")
        
        strategy = draft_data['draft_strategy']
        
        # Early Rounds
        st.subheader("🏆 Early Rounds (1-3)")
        st.write(f"**Strategy:** {strategy['early_rounds']['strategy']}")
        st.write(f"**Positions to Target:** {', '.join(strategy['early_rounds']['positions_to_target'])}")
        st.write(f"**Avoid:** {strategy['early_rounds']['avoid']}")
        st.info(strategy['early_rounds']['notes'])
        
        st.markdown("---")
        
        # Middle Rounds
        st.subheader("⚡ Middle Rounds (4-10)")
        st.write(f"**Strategy:** {strategy['middle_rounds']['strategy']}")
        st.write(f"**Positions to Target:** {', '.join(strategy['middle_rounds']['positions_to_target'])}")
        st.write(f"**Target Types:** {strategy['middle_rounds']['target_types']}")
        st.info(strategy['middle_rounds']['notes'])
        
        st.markdown("---")
        
        # Late Rounds
        st.subheader("🚀 Late Rounds (11+)")
        st.write(f"**Strategy:** {strategy['late_rounds']['strategy']}")
        st.write(f"**Positions to Target:** {', '.join(strategy['late_rounds']['positions_to_target'])}")
        st.write(f"**Target Types:** {strategy['late_rounds']['target_types']}")
        st.info(strategy['late_rounds']['notes'])
        
        st.markdown("---")
        
        # Key Principles
        st.subheader("🔑 Key Draft Principles")
        for principle in strategy['key_principles']:
            st.success(f"✅ {principle}")
    
    # TAB 7: Keeper Analysis
    with tab7:
        st.header("🔒 Keeper League Analysis")
        st.markdown("Understanding which elite players will be kept vs available")
        
        if 'keeper_analysis' not in draft_data:
            st.warning("Keeper analysis not available. Click 'Regenerate Rankings' to update.")
        else:
            keeper = draft_data['keeper_analysis']
            
            # Scarcity Analysis
            st.subheader("📊 Positional Scarcity in Keeper Leagues")
            
            scarcity = keeper['available_targets']['scarcity_analysis']
            
            for pos, data in scarcity.items():
                level = data['scarcity_level']
                
                # Color code by scarcity
                if level == 'EXTREME':
                    color = "🔴"
                elif level == 'HIGH':
                    color = "🟡"
                else:
                    color = "🟢"
                
                with st.expander(f"{color} **{pos}** - {level} Scarcity"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Total Elite", data['total_elite'])
                        st.metric("Likely Kept", data['likely_kept'])
                        st.metric("Available", data['available'])
                    
                    with col2:
                        st.info(f"**Strategy:** {data['recommendation']}")
            
            st.markdown("---")
            
            # Likely Keepers
            st.subheader("🔒 Players Likely to be Kept")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Elite Tier (Rd 1-2):**")
                for player in keeper['likely_keepers']['elite_tier']:
                    st.write(f"• {player}")
                
                st.write("\n**First Base:**")
                for player in keeper['likely_keepers']['first_base']:
                    st.write(f"• {player}")
            
            with col2:
                st.write("**Shortstop:**")
                for player in keeper['likely_keepers']['shortstop'][:3]:
                    st.write(f"• {player}")
                
                st.write("\n**Outfield (Top):**")
                for player in keeper['likely_keepers']['outfield'][:4]:
                    st.write(f"• {player}")
            
            st.markdown("---")
            
            # Draft Impact
            st.subheader("🎯 Keeper League Draft Impact")
            impact = keeper['draft_impact']
            
            st.warning(f"**ADP Shift:** {impact['effective_adp_shift']}")
            st.info(f"**Compression:** {impact['strategy']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"**Focus Positions:** {', '.join(impact['focus_positions'])}")
            with col2:
                st.info(f"**Wait Positions:** {', '.join(impact['wait_positions'])}")
    
    # TAB 8: Positional Recommendations  
    with tab8:
        st.header("🎯 Recommendations by Position")
        st.markdown("Detailed targets for each position in keeper league format")
        
        if 'positional_recommendations' not in draft_data:
            st.warning("Positional recommendations not available. Click 'Regenerate Rankings' to update.")
        else:
            pos_rec = draft_data['positional_recommendations']
            
            # FIRST BASE - Featured prominently
            st.subheader("⚾ FIRST BASE - TOP PRIORITY")
            first_base = pos_rec['1B']
            
            st.error(f"**Scarcity:** {first_base['scarcity']}")
            st.success(f"**Strategy:** {first_base['strategy']}")
            
            # Tier 1
            st.write("### 🌟 Tier 1 - Best Available")
            for player in first_base['tier_1_available']:
                with st.expander(f"**{player['player']}** ({player['team']}) - Rounds {player['target_round']}"):
                    st.write(f"**Projection:** {player['proj']}")
                    st.info(f"**Why:** {player['why']}")
            
            # Tier 2
            st.write("### ⭐ Tier 2 - Solid Options")
            for player in first_base['tier_2_targets']:
                with st.expander(f"**{player['player']}** ({player['team']}) - Rounds {player['target_round']}"):
                    st.write(f"**Projection:** {player['proj']}")
                    st.info(f"**Why:** {player['why']}")
            
            # Breakout Bets
            st.write("### 🚀 Breakout Candidates")
            for player in first_base['breakout_bets']:
                with st.expander(f"**{player['player']}** ({player['team']}) - Rounds {player['target_round']}"):
                    st.write(f"**Projection:** {player['proj']}")
                    st.info(f"**Why:** {player['why']}")
            
            # Avoid
            st.write("### ❌ Players to Avoid")
            for avoid in first_base['avoid']:
                st.error(f"• {avoid}")
            
            st.markdown("---")
            
            # SECOND BASE
            st.subheader("⚾ SECOND BASE")
            second_base = pos_rec['2B']
            
            st.error(f"**Scarcity:** {second_base['scarcity']}")
            st.warning(f"**Strategy:** {second_base['strategy']}")
            
            st.write("### Top Available:")
            for player in second_base['top_available']:
                with st.expander(f"**{player['player']}** ({player['team']}) - Rounds {player['target_round']}"):
                    st.write(f"**Projection:** {player['proj']}")
                    st.info(f"**Why:** {player['why']}")
            
            st.write("### Late Round Fliers:")
            for player in second_base['late_round_fliers']:
                with st.expander(f"**{player['player']}** ({player['team']}) - Rounds {player['target_round']}"):
                    st.write(f"**Projection:** {player['proj']}")
                    st.info(f"**Why:** {player['why']}")
            
            st.markdown("---")
            
            # SHORTSTOP
            st.subheader("⚾ SHORTSTOP")
            shortstop = pos_rec['SS']
            
            st.error(f"**Scarcity:** {shortstop['scarcity']}")
            st.warning(f"**Strategy:** {shortstop['strategy']}")
            
            for player in shortstop['realistic_targets']:
                with st.expander(f"**{player['player']}** ({player['team']}) - Rounds {player['target_round']}"):
                    st.write(f"**Projection:** {player['proj']}")
                    st.info(f"**Why:** {player['why']}")
            
            st.markdown("---")
            
            # OUTFIELD
            st.subheader("⚾ OUTFIELD")
            outfield = pos_rec['OF']
            
            st.success(f"**Scarcity:** {outfield['scarcity']}")
            st.info(f"**Strategy:** {outfield['strategy']}")
            
            for tip in outfield['wait_for_value']:
                st.write(f"• {tip}")
    
    # Footer
    st.markdown("---")
    st.caption("Generated by fb-ai - Fantasy Baseball AI | Last updated: " + 
               datetime.fromisoformat(draft_data['generated_date']).strftime('%B %d, %Y %I:%M %p'))


if __name__ == "__main__":
    main()
