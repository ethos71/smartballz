"""
Player Weight Breakdown Component

Displays factor weights for roster players and waiver wire prospects.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_player_weight_breakdown(df: pd.DataFrame):
    """
    Render player weight breakdown section with roster and waiver wire tabs
    
    Args:
        df: DataFrame with player data including factor scores and weights
    """
    from streamlit_report import section_header
    
    section_header("Player Weight Breakdown", "⚖️")
    st.markdown("View individual factor weights for roster players and top waiver wire prospects")
    
    # Create tabs for roster vs waiver wire
    tab1, tab2 = st.tabs(["📊 Roster Players", "🌟 Top 10 Waiver Wire"])
    
    with tab1:
        _render_roster_players_tab(df)
    
    with tab2:
        _render_waiver_wire_tab()
    
    st.markdown("---")


def _render_roster_players_tab(df):
    """Render roster players factor weight analysis"""
    # Header with help icon
    col_header, col_help = st.columns([10, 1])
    with col_header:
        st.markdown("#### Roster Players - Factor Weight Analysis")
    with col_help:
        with st.popover("ℹ️"):
            st.markdown("""
            ### Factor Score
            A **factor score** represents how favorable a specific matchup factor is for a player on a particular day.
            - **Range:** Typically -1.0 to +2.0 (normalized scale)
            - **Meaning:** 
              - Positive scores (>0) = Favorable conditions
              - Negative scores (<0) = Unfavorable conditions
              - Zero (0) = Neutral/average conditions
            - **Example:** A wind factor score of +2.0 means strong wind blowing out (very favorable for hitters)
            
            ### Factor Weight
            A **factor weight** represents how much importance/influence a specific factor has in the final recommendation.
            - **Range:** 0.0 to 1.0 (percentage)
            - **Purpose:** Determines how much each factor score contributes to the final decision
            - **Calibrated:** Weights are optimized based on historical performance data
            - **Example:** If the wind factor has a weight of 0.15 (15%), it contributes 15% to the final score
            
            ### Weighted Contribution
            **Weighted Contribution = Factor Score × Factor Weight**
            
            This shows the actual impact of each factor on the final recommendation:
            - **Example:** Wind score of +2.0 × weight of 0.15 = +0.30 contribution to final score
            - **Final Score:** Sum of all weighted contributions across 20 factors
            
            ### How to Use This View
            1. **Select a player** from the dropdown to see their specific factor breakdown
            2. **Review Factor Weights** - Which factors matter most for this player?
            3. **Check Factor Scores** - Which conditions are favorable/unfavorable today?
            4. **Analyze Contributions** - Which factors are driving the sit/start decision?
            
            ### Real-World Example
            **Aaron Judge on a windy day:**
            - Wind Score: +2.0 (strong wind out) × Weight: 0.045 = **+0.09 contribution**
            - Vegas Score: +1.5 (high O/U) × Weight: 0.20 = **+0.30 contribution**  
            - Park Score: +0.8 (hitter park) × Weight: 0.06 = **+0.05 contribution**
            - ... (17 more factors)
            - **Final Score: +0.62 → 🌟 STRONG START**
            """)
    
    # Get unique players sorted by final score
    players = df.sort_values('final_score', ascending=False)['player_name'].unique().tolist()
    
    if len(players) == 0:
        st.warning("No player data available")
        return
    
    # Player selection
    selected_player = st.selectbox(
        "Select player to view detailed weights:",
        players,
        key="weight_breakdown_player"
    )
    
    # Get player data
    player_data = df[df['player_name'] == selected_player].iloc[0]
    
    # Get factor columns
    factor_scores = {col.replace('_score', ''): player_data[col] 
                    for col in df.columns if col.endswith('_score') and col != 'final_score'}
    factor_weights = {col.replace('_weight', ''): player_data[col] 
                     for col in df.columns if col.endswith('_weight')}
    
    # Create visualization tabs
    viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Factor Weights", "Factor Scores", "Weighted Contribution to Final Score"])
    
    with viz_tab1:
        _render_factor_weights_chart(factor_weights)
    
    with viz_tab2:
        _render_factor_scores_chart(factor_scores)
    
    with viz_tab3:
        _render_weighted_contribution_chart(factor_scores, factor_weights)


def _render_factor_weights_chart(factor_weights):
    """Render factor weights bar chart"""
    import plotly.graph_objects as go
    
    sorted_weights = dict(sorted(factor_weights.items(), key=lambda x: x[1], reverse=True))
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(sorted_weights.values()),
            y=list(sorted_weights.keys()),
            orientation='h',
            marker=dict(color='lightblue')
        )
    ])
    
    fig.update_layout(
        title="Factor Weights (Importance)",
        xaxis_title="Weight (0-1 scale)",
        yaxis_title="Factor",
        height=600,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def _render_factor_scores_chart(factor_scores):
    """Render factor scores bar chart"""
    import plotly.graph_objects as go
    
    sorted_scores = dict(sorted(factor_scores.items(), key=lambda x: x[1], reverse=True))
    
    # Color by positive/negative
    colors = ['green' if v > 0 else 'red' if v < 0 else 'gray' for v in sorted_scores.values()]
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(sorted_scores.values()),
            y=list(sorted_scores.keys()),
            orientation='h',
            marker=dict(color=colors)
        )
    ])
    
    fig.update_layout(
        title="Factor Scores (Favorability)",
        xaxis_title="Score (-2 to +2 scale)",
        yaxis_title="Factor",
        height=600,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def _render_weighted_contribution_chart(factor_scores, factor_weights):
    """Render weighted contribution chart"""
    import plotly.graph_objects as go
    
    # Calculate weighted contributions
    contributions = {}
    for factor in factor_scores.keys():
        if factor in factor_weights:
            contributions[factor] = factor_scores[factor] * factor_weights[factor]
    
    sorted_contributions = dict(sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True))
    
    # Color by positive/negative
    colors = ['green' if v > 0 else 'red' if v < 0 else 'gray' for v in sorted_contributions.values()]
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(sorted_contributions.values()),
            y=list(sorted_contributions.keys()),
            orientation='h',
            marker=dict(color=colors)
        )
    ])
    
    fig.update_layout(
        title="Weighted Contribution to Final Score",
        xaxis_title="Contribution (Score × Weight)",
        yaxis_title="Factor",
        height=600,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def _render_waiver_wire_tab():
    """Render waiver wire prospects tab"""
    import glob
    import pandas as pd
    
    # Load waiver wire data
    waiver_files = sorted(glob.glob('data/waiver_wire_*.csv'), reverse=True)
    
    if waiver_files:
        waiver_df = pd.read_csv(waiver_files[0])
        
        if len(waiver_df) > 0:
            st.markdown("#### Top 10 Waiver Wire Prospects")
            
            # Get top 10 by final score
            top_waiver = waiver_df.nlargest(10, 'final_score')
            
            # Player selection
            waiver_players = top_waiver['player_name'].tolist()
            selected_waiver = st.selectbox(
                "Select waiver wire player:",
                waiver_players,
                key="waiver_weight_breakdown"
            )
            
            # Get player data
            player_data = waiver_df[waiver_df['player_name'] == selected_waiver].iloc[0]
            
            # Get factor columns
            factor_scores = {col.replace('_score', ''): player_data[col] 
                           for col in waiver_df.columns if col.endswith('_score') and col != 'final_score'}
            factor_weights = {col.replace('_weight', ''): player_data[col] 
                            for col in waiver_df.columns if col.endswith('_weight')}
            
            # Create visualization tabs
            viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Factor Weights", "Factor Scores", "Weighted Contribution"])
            
            with viz_tab1:
                _render_factor_weights_chart(factor_weights)
            
            with viz_tab2:
                _render_factor_scores_chart(factor_scores)
            
            with viz_tab3:
                _render_weighted_contribution_chart(factor_scores, factor_weights)
        else:
            st.info("No waiver wire data available in this analysis")
    else:
        st.info("💡 Waiver wire analysis not yet run. Run with waiver wire analysis enabled to see top free agent prospects.")
