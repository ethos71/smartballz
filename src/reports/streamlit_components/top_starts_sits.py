"""
Top Starts and Bottom Sits Component

Displays top 5 starts and bottom 5 sits, separated by hitters and pitchers.
"""

import streamlit as st
import pandas as pd
from .config import section_header_with_help


def render_top_starts_sits(df: pd.DataFrame):
    """
    Render top starts and bottom sits section
    
    Args:
        df: DataFrame with player data including final_score and player_type
    """
    section_header_with_help(
        "🌟🚫 Top Starts & Bottom Sits",
        """
### How to Read These Recommendations
    
This section shows your **best and worst matchups** for the selected game date, separated by position type.
    
### The 5 Recommendation Levels
    
**🌟 Strong Start (≥ 0.15):**
- Top-tier matchup with multiple favorable factors
- **Action:** Start with high confidence
- **Example:** Aaron Judge vs LHP, wind blowing out, favorable park
    
**✅ Favorable (≥ 0.05):**
- Good matchup with some positive factors
- **Action:** Strong start candidate
- **Example:** Most everyday players on average days
    
**⚖️ Neutral (-0.05 to +0.05):**
- Average matchup, mixed factors
- **Action:** Use other context (roster needs, opponent strength)
- **Example:** Backup catcher vs average pitcher
    
**⚠️ Unfavorable (≥ -0.15):**
- Poor matchup with negative factors
- **Action:** Consider benching if you have alternatives
- **Example:** Slumping hitter vs elite pitcher in pitcher's park
    
**🚫 Bench (< -0.15):**
- Very poor matchup, multiple unfavorable factors
- **Action:** Bench unless no alternatives
- **Example:** Cold hitter vs ace pitcher with bad umpire
    
### Why Separate Hitters and Pitchers?
    
**Hitters:**
- Evaluated on: park factors, pitcher matchup, weather, umpire, hot streaks
- Top 5 = your best offensive plays
- Bottom 5 = consider benching for better options
    
**Pitchers (SP/RP):**
- Evaluated on: opponent strength, park factors, recent performance
- Top 5 = your best pitching matchups
- Bottom 5 = risky starts, high blow-up potential
    
### The Math Behind It
```
Player Score = Σ(Factor Score × Factor Weight)
    
Example - Aaron Judge (+0.24):
Wind:         +2.0 × 0.045 = +0.090
Umpire:       +0.7 × 0.025 = +0.018
Park:         +0.5 × 0.056 = +0.028
Recent Form:  +1.0 × 0.046 = +0.046
... (16 more factors)
= +0.24 → 🌟 STRONG START
```
    
### Real-World Strategy
    
**When You See Strong Starts:**
- Prioritize these players in your lineup
- Consider them for DFS plays
- High confidence plays
    
**When You See Benches:**
- Sit if you have alternatives
- Don't panic-drop - it's just one day
- May still be valuable ROS (rest of season)
    
**Position Abbreviations:**
- C = Catcher, 1B/2B/3B/SS = Infield, OF = Outfield
- SP = Starting Pitcher, RP = Relief Pitcher
    
### Tips
- Start your 🌟 and ✅ players whenever possible
- Bench your 🚫 and ⚠️ players if you have better options
- ⚖️ Neutral players? Use gut feeling or recent stats
- Check opponent's pitcher (for hitters) or lineup (for pitchers)
"""
    )
    
    # Separate hitters and pitchers
    hitters_df = df[df['player_type'] == 'Hitter'].copy()
    pitchers_df = df[df['player_type'] == 'Pitcher'].copy()
    
    # Create two columns for starts/sits
    col_starts, col_sits = st.columns(2)
    
    with col_starts:
        st.markdown("### 🌟 Top 5 Starts")
        _render_top_players(hitters_df, pitchers_df, top=True)
    
    with col_sits:
        st.markdown("### 🚫 Bottom 5 Sits")
        _render_top_players(hitters_df, pitchers_df, top=False)


def _render_top_players(hitters_df, pitchers_df, top=True):
    """Render top or bottom players"""
    # Top 5 Hitters
    if len(hitters_df) > 0:
        st.markdown("**🔨 Hitters**")
        if top:
            selected = hitters_df.nlargest(5, 'final_score')
        else:
            selected = hitters_df.nsmallest(5, 'final_score')
        
        _render_player_table(selected)
    
    # Top 5 Pitchers
    if len(pitchers_df) > 0:
        st.markdown("**⚾ Pitchers**")
        if top:
            selected = pitchers_df.nlargest(5, 'final_score')
        else:
            selected = pitchers_df.nsmallest(5, 'final_score')
        
        _render_player_table(selected)


def _render_player_table(players_df):
    """Render a table of players"""
    display_df = players_df[['player_name', 'player_key', 'position', 'final_score', 'recommendation']].copy()
    display_df.index = range(1, len(display_df) + 1)
    
    # Create Yahoo link
    display_df['player_link'] = display_df.apply(
        lambda row: f"https://baseball.fantasysports.yahoo.com/b1/3119/3/{row['player_key'].split('.')[-1]}" 
        if row['player_key'] and '.' in str(row['player_key']) else '', axis=1
    )
    
    display_df = display_df[['player_name', 'player_link', 'position', 'final_score', 'recommendation']].copy()
    display_df.columns = ['Player', 'Link', 'Position', 'Score', 'Recommendation']
    
    st.dataframe(
        display_df,
        column_config={
            "Link": st.column_config.LinkColumn("Yahoo", display_text="🔗"),
            "Score": st.column_config.NumberColumn("Score", format="%.3f")
        },
        use_container_width=True, 
        height=210
    )
