"""
Streamlit Component: Opponent Analysis Section
Display opponent team's 20-factor analysis results
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def render_opponent_analysis(opponent_df: pd.DataFrame, opponent_name: str):
    """
    Render opponent's team analysis with same visualizations
    
    Args:
        opponent_df: DataFrame with opponent player scores
        opponent_name: Name of opponent team
    """
    
    st.markdown("---")
    st.markdown(f"## 🎯 Opponent Analysis: {opponent_name}")
    
    with st.expander("ℹ️ About Opponent Analysis"):
        st.markdown("""
        This section runs the same 20-factor analysis on your weekly matchup opponent's roster.
        Use this to:
        - **Identify their weak spots** - Players they're starting with poor matchups
        - **Compare strategies** - See how their players stack up against yours
        - **Predict performance** - Estimate their likely point production this week
        """)
    
    if opponent_df is None or len(opponent_df) == 0:
        st.warning("No opponent data available")
        return
    
    # Summary metrics
    st.markdown("### 📊 Opponent Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    hitters = opponent_df[opponent_df['position'].isin(['C', '1B', '2B', '3B', 'SS', 'OF', 'Util', 'DH'])]
    pitchers = opponent_df[opponent_df['position'].isin(['SP', 'RP', 'P'])]
    
    with col1:
        st.metric("Total Players", len(opponent_df))
    with col2:
        st.metric("Hitters", len(hitters))
    with col3:
        st.metric("Pitchers", len(pitchers))
    with col4:
        avg_score = opponent_df['final_score'].mean()
        st.metric("Avg Score", f"{avg_score:.3f}")
    
    # Top/Bottom performers
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌟 Their Best Matchups")
        top_5 = opponent_df.nlargest(5, 'final_score')[['player_name', 'position', 'final_score', 'recommendation']]
        st.dataframe(top_5, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("#### 🚫 Their Worst Matchups")
        bottom_5 = opponent_df.nsmallest(5, 'final_score')[['player_name', 'position', 'final_score', 'recommendation']]
        st.dataframe(bottom_5, hide_index=True, use_container_width=True)
    
    # Score distribution
    st.markdown("### 📈 Score Distribution")
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=hitters['final_score'],
        name='Hitters',
        marker_color='lightblue',
        opacity=0.7
    ))
    
    fig.add_trace(go.Histogram(
        x=pitchers['final_score'],
        name='Pitchers',
        marker_color='lightcoral',
        opacity=0.7
    ))
    
    fig.update_layout(
        barmode='overlay',
        xaxis_title='Score',
        yaxis_title='Number of Players',
        title='Opponent Score Distribution by Position Type',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Full roster table
    st.markdown("### 📋 Full Opponent Roster")
    
    display_df = opponent_df[['player_name', 'position', 'final_score', 'recommendation']].copy()
    display_df = display_df.sort_values('final_score', ascending=False)
    display_df['final_score'] = display_df['final_score'].round(3)
    
    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = opponent_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Opponent Analysis CSV",
        data=csv,
        file_name=f"opponent_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
