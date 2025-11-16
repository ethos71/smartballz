"""
Summary Metrics Component

Displays high-level summary metrics for recommendations.
"""

import streamlit as st
import pandas as pd


def render_summary_metrics(df_summary: pd.DataFrame):
    """
    Render summary metrics section
    
    Args:
        df_summary: DataFrame with recommendations data
    """
    st.markdown("---")
    
    # Summary metrics with help popup
    col1, col2, col3, col4, col_help = st.columns([2, 2, 2, 2, 1])
    
    with col1:
        st.metric("Total Players", len(df_summary))
    
    with col2:
        starts = len(df_summary[df_summary['recommendation'].str.contains('START', na=False)])
        st.metric("Recommended Starts", starts)
    
    with col3:
        sits = len(df_summary[df_summary['recommendation'].str.contains('SIT', na=False)])
        st.metric("Recommended Sits", sits)
    
    with col4:
        neutral = len(df_summary[df_summary['recommendation'].str.contains('NEUTRAL', na=False)])
        st.metric("Neutral", neutral)
    
    with col_help:
        st.write("")  # Spacer
        with st.popover("ℹ️"):
            st.markdown("""
            ### What These Numbers Mean
            
            **Total Players:** The complete count of players on your selected fantasy team roster.
            
            **Recommended Starts:** Players with favorable matchup conditions based on our 20-factor analysis.
            - **🌟 Strong Start** (score ≥ 0.15): Top-tier matchups, definitely start
            - **✅ Favorable** (score ≥ 0.05): Good matchups, strong start candidates
            
            **Recommended Sits:** Players with unfavorable matchup conditions.
            - **⚠️ Unfavorable** (score ≥ -0.15): Poor matchups, consider benching
            - **🚫 Bench** (score < -0.15): Very poor matchups, definitely bench
            
            **Neutral:** Players with average matchup conditions (score between -0.05 and +0.05).
            - Consider other factors like recent form, importance of game, roster constraints
            
            ### How We Calculate
            Each player receives a **final score** based on 20 factors:
            ```
            Final Score = Σ(Factor Score × Factor Weight)
            ```
            
            ### Real-World Example
            Aaron Judge with final score of +0.24:
            - Wind blowing out (+2.0 × 0.045) = +0.09
            - Favorable park (+0.5 × 0.056) = +0.028
            - Hot streak (+1.0 × 0.046) = +0.046
            - Plus 17 other factors...
            - **Total: +0.24 → 🌟 STRONG START**
            
            ### Decision Guidelines
            - **≥ 15 Starts recommended?** Good matchup week, be aggressive
            - **< 10 Starts recommended?** Tough week, be selective
            - **High Neutral count?** More decisions left to your judgment
            """)
    
    st.markdown("---")
