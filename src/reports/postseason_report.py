#!/usr/bin/env python3
"""
Postseason Roster Lock Analysis

Special dashboard for postseason play with roster lock rules:
- No adds/drops allowed after roster locks
- Can only replace players on IL (Injured List)
- Focus on maximizing locked roster
- Monitor IL status daily
- Optimize lineup with available players only

Usage:
    streamlit run src/reports/postseason_report.py
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


# Page configuration
st.set_page_config(
    page_title="Postseason Roster Lock Analysis",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main postseason dashboard"""
    
    st.title("🏆 Postseason Roster Lock Analysis")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Postseason Settings")
        
        st.info("""
        **Roster Lock Rules:**
        - ❌ No adds/drops after lock
        - ✅ IL replacements only
        - 🔒 Roster is locked
        - 📊 Optimize with current players
        """)
        
        st.markdown("---")
        
        # Roster lock date
        lock_date = st.date_input(
            "Roster Lock Date:",
            value=datetime(2026, 10, 1)
        )
        
        st.metric("Days Since Lock", (datetime.now().date() - lock_date).days)
        
        st.markdown("---")
        
        # IL replacement tracking
        st.subheader("🏥 IL Replacements")
        il_count = st.number_input("Players on IL:", min_value=0, value=0)
        
        if il_count > 0:
            st.success(f"✅ {il_count} replacement(s) available")
        else:
            st.info("No IL spots available")
        
        st.markdown("---")
        st.caption("Postseason Roster Lock Dashboard")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔒 Locked Roster",
        "🏥 IL Monitor",
        "⚾ Daily Lineups",
        "📊 Performance Tracking",
        "🎯 Playoff Strategy"
    ])
    
    # TAB 1: Locked Roster
    with tab1:
        st.header("🔒 Your Locked Postseason Roster")
        st.markdown("Players available for the remainder of postseason")
        
        st.warning("⚠️ **Roster is LOCKED** - No adds/drops except IL replacements")
        
        # Sample roster structure
        st.subheader("📋 Position Players")
        
        position_players = {
            "C": ["Salvador Perez"],
            "1B": ["Christian Walker"],
            "2B": ["Ozzie Albies"],
            "3B": ["José Ramírez"],
            "SS": ["Bobby Witt Jr."],
            "OF": ["Ronald Acuña Jr.", "Juan Soto", "Kyle Tucker"],
            "UTIL": ["Bryce Harper", "Yordan Alvarez"],
            "BENCH": ["Michael Busch", "Spencer Torkelson"]
        }
        
        for pos, players in position_players.items():
            with st.expander(f"**{pos}** - {len(players)} player(s)"):
                for player in players:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"• {player}")
                    with col2:
                        st.success("Active")
        
        st.markdown("---")
        
        st.subheader("⚾ Starting Pitchers")
        
        starting_pitchers = [
            "Gerrit Cole", "Spencer Strider", "Zack Wheeler",
            "Logan Webb", "Pablo López", "Hunter Brown"
        ]
        
        for pitcher in starting_pitchers:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"• {pitcher}")
            with col2:
                st.success("Active")
        
        st.markdown("---")
        
        st.subheader("💨 Relief Pitchers")
        
        relief_pitchers = ["Emmanuel Clase", "Félix Bautista", "Ryan Helsley"]
        
        for pitcher in relief_pitchers:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"• {pitcher}")
            with col2:
                st.success("Active")
    
    # TAB 2: IL Monitor
    with tab2:
        st.header("🏥 Injury List (IL) Monitor")
        st.markdown("Track IL status to identify replacement opportunities")
        
        st.info("""
        **IL Replacement Rules:**
        - Only way to add new players after roster lock
        - Must have player officially placed on IL
        - Replacement must happen immediately
        - Cannot drop healthy players
        """)
        
        st.markdown("---")
        
        # IL Tracking
        st.subheader("🚨 Current IL Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Players on IL", 0, delta=0)
            st.metric("Available IL Spots", 2)
        
        with col2:
            st.metric("Replacement Budget", "Unlimited")
            st.metric("Days Until Next Check", 1)
        
        st.markdown("---")
        
        # Monitor List
        st.subheader("⚠️ Players to Monitor")
        st.markdown("Players with injury concerns or day-to-day status")
        
        injury_watch = [
            {
                "player": "Ronald Acuña Jr.",
                "status": "DTD - Hamstring",
                "risk": "MEDIUM",
                "action": "Monitor daily"
            },
            {
                "player": "Spencer Strider",
                "status": "Probable",
                "risk": "LOW",
                "action": "Should play"
            }
        ]
        
        for player_data in injury_watch:
            risk_color = "🟡" if player_data['risk'] == "MEDIUM" else "🟢"
            
            with st.expander(f"{risk_color} **{player_data['player']}** - {player_data['status']}"):
                st.write(f"**Risk Level:** {player_data['risk']}")
                st.write(f"**Action:** {player_data['action']}")
                
                if player_data['risk'] == "MEDIUM":
                    st.warning("Check status before each game!")
        
        st.markdown("---")
        
        # IL Replacement Candidates
        st.subheader("🎯 Best Available Replacements")
        st.markdown("Top waiver options if IL spot opens")
        
        replacements_by_pos = {
            "C": ["Will Smith", "Adley Rutschman"],
            "1B": ["Josh Naylor", "Ryan Mountcastle"],
            "OF": ["Riley Greene", "Jarren Duran"],
            "SP": ["Bryce Miller", "Taj Bradley"]
        }
        
        for pos, candidates in replacements_by_pos.items():
            with st.expander(f"**{pos} Replacements**"):
                for candidate in candidates:
                    st.write(f"• {candidate}")
    
    # TAB 3: Daily Lineups
    with tab3:
        st.header("⚾ Daily Lineup Optimization")
        st.markdown("Maximize production with locked roster")
        
        st.success("✅ Focus: Set optimal lineup with available players only")
        
        # Today's recommendations
        st.subheader("🗓️ Today's Lineup Recommendations")
        
        game_date = st.date_input("Game Date:", value=datetime.now())
        
        st.markdown("---")
        
        # Starting lineup
        st.write("### Recommended Starters")
        
        starters = [
            {"player": "Bobby Witt Jr.", "pos": "SS", "matchup": "vs RHP", "rating": "🟢 START"},
            {"player": "Ronald Acuña Jr.", "pos": "OF", "matchup": "vs RHP", "rating": "🟢 START"},
            {"player": "Juan Soto", "pos": "OF", "matchup": "vs LHP", "rating": "🟢 START"},
            {"player": "José Ramírez", "pos": "3B", "matchup": "vs RHP", "rating": "🟢 START"},
            {"player": "Bryce Harper", "pos": "UTIL", "matchup": "vs RHP", "rating": "🟢 START"},
        ]
        
        for starter in starters:
            col1, col2, col3, col4 = st.columns([2, 1, 2, 1])
            with col1:
                st.write(f"**{starter['player']}**")
            with col2:
                st.write(starter['pos'])
            with col3:
                st.write(starter['matchup'])
            with col4:
                st.success(starter['rating'])
        
        st.markdown("---")
        
        # Bench decisions
        st.write("### Bench vs Start Decisions")
        
        bench_decisions = [
            {"player": "Michael Busch", "matchup": "vs LHP", "rec": "🟡 CONSIDER", "reason": "Platoon disadvantage"},
            {"player": "Spencer Torkelson", "matchup": "OFF DAY", "rec": "🔴 BENCH", "reason": "Team not playing"},
        ]
        
        for decision in bench_decisions:
            with st.expander(f"{decision['rec']} **{decision['player']}** - {decision['matchup']}"):
                st.write(f"**Reason:** {decision['reason']}")
        
        st.markdown("---")
        
        # Pitching decisions
        st.subheader("⚾ Pitching Decisions")
        
        pitcher_decisions = [
            {"pitcher": "Gerrit Cole", "opp": "vs SEA", "rec": "🟢 START", "ip": "7.0", "k": "9"},
            {"pitcher": "Hunter Brown", "opp": "@ LAD", "rec": "🟡 RISKY", "ip": "5.0", "k": "6"},
            {"pitcher": "Pablo López", "opp": "OFF DAY", "rec": "⚪ N/A", "ip": "-", "k": "-"},
        ]
        
        for pitcher in pitcher_decisions:
            col1, col2, col3, col4 = st.columns([2, 2, 1, 2])
            with col1:
                st.write(f"**{pitcher['pitcher']}**")
            with col2:
                st.write(pitcher['opp'])
            with col3:
                if pitcher['rec'] == "🟢 START":
                    st.success(pitcher['rec'])
                elif pitcher['rec'] == "🟡 RISKY":
                    st.warning(pitcher['rec'])
                else:
                    st.info(pitcher['rec'])
            with col4:
                st.write(f"Proj: {pitcher['ip']} IP, {pitcher['k']} K")
    
    # TAB 4: Performance Tracking
    with tab4:
        st.header("📊 Postseason Performance Tracking")
        st.markdown("Monitor how your locked roster is performing")
        
        # Stats summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Team Batting Avg", ".268", delta="+.012")
        with col2:
            st.metric("Home Runs", 15, delta="+3")
        with col3:
            st.metric("Stolen Bases", 8, delta="+2")
        with col4:
            st.metric("Team ERA", "3.45", delta="-0.23")
        
        st.markdown("---")
        
        # Top performers
        st.subheader("🌟 Top Postseason Performers")
        
        top_performers = [
            {"player": "Bobby Witt Jr.", "avg": ".325", "hr": 4, "rbi": 12, "sb": 3},
            {"player": "Ronald Acuña Jr.", "avg": ".310", "hr": 3, "rbi": 8, "sb": 4},
            {"player": "Gerrit Cole", "w": 2, "era": "2.15", "k": 23, "ip": "16.2"},
        ]
        
        for performer in top_performers:
            st.success(f"⭐ **{performer['player']}**")
            if 'avg' in performer:
                st.write(f"AVG: {performer['avg']}, HR: {performer['hr']}, RBI: {performer['rbi']}, SB: {performer['sb']}")
            else:
                st.write(f"W: {performer['w']}, ERA: {performer['era']}, K: {performer['k']}, IP: {performer['ip']}")
        
        st.markdown("---")
        
        # Underperformers
        st.subheader("📉 Needs Improvement")
        
        st.warning("Players not meeting expectations in postseason")
        
        underperformers = [
            {"player": "Kyle Tucker", "avg": ".185", "note": "Cold streak, keep starting"},
            {"player": "Hunter Brown", "era": "5.40", "note": "Consider benching vs tough matchups"},
        ]
        
        for under in underperformers:
            with st.expander(f"⚠️ **{under['player']}**"):
                st.write(f"**Stats:** {under.get('avg', under.get('era'))}")
                st.info(f"**Strategy:** {under['note']}")
    
    # TAB 5: Playoff Strategy
    with tab5:
        st.header("🎯 Postseason Strategy Guide")
        st.markdown("Maximize your locked roster's potential")
        
        st.info("""
        **Key Principles for Roster Lock Postseason:**
        
        Since you can't add/drop (except IL), success depends on:
        1. **Daily lineup optimization** - Start your best matchups
        2. **IL monitoring** - Watch injury reports closely
        3. **Platoon advantages** - Leverage L/R splits
        4. **Pitching matchups** - Start vs weak offenses
        5. **Games played** - Maximize at-bats
        """)
        
        st.markdown("---")
        
        # Strategy by position
        st.subheader("📋 Position-by-Position Strategy")
        
        strategies = {
            "Catchers": "Start daily - catching is thin, maximize games",
            "Corner IF": "Platoon if possible, prioritize hot bats",
            "Middle IF": "Start your studs, they're locked in",
            "Outfield": "Most depth here, rotate based on matchups",
            "Starting Pitchers": "Pick your spots, quality over quantity",
            "Relief Pitchers": "Start closers for saves, avoid setup men"
        }
        
        for position, strategy in strategies.items():
            with st.expander(f"**{position}**"):
                st.write(strategy)
        
        st.markdown("---")
        
        # Matchup priorities
        st.subheader("🎯 Matchup Priorities")
        
        st.write("**Green Light (Always Start):**")
        st.success("• Elite bats vs weak pitching")
        st.success("• Aces vs weak offenses")
        st.success("• Proven closers")
        
        st.write("\n**Yellow Light (Evaluate):**")
        st.warning("• Platoon disadvantages")
        st.warning("• Slumping hitters vs aces")
        st.warning("• Back-end starters vs elite offenses")
        
        st.write("\n**Red Light (Likely Bench):**")
        st.error("• Bad matchups + cold bat")
        st.error("• Injured/GTD players")
        st.error("• Pitchers facing elite lineups")
        
        st.markdown("---")
        
        # Daily checklist
        st.subheader("✅ Daily Checklist")
        
        daily_tasks = [
            "Check injury reports (IL opportunities)",
            "Review today's starting pitchers",
            "Check lineup cards (batting order)",
            "Evaluate L/R matchups",
            "Set optimal lineup before first game",
            "Monitor weather (postponements)",
            "Track IL status changes"
        ]
        
        for i, task in enumerate(daily_tasks, 1):
            st.checkbox(f"{i}. {task}", key=f"task_{i}")
    
    # Footer
    st.markdown("---")
    st.caption("Postseason Roster Lock Dashboard | fb-ai - Fantasy Baseball AI")


if __name__ == "__main__":
    main()
