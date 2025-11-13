#!/usr/bin/env python3
"""
Fantasy Baseball AI - Streamlit Sit/Start Report
Interactive dashboard for sit/start recommendations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import glob
import os

# Page config
st.set_page_config(
    page_title="FB-AI Sit/Start Report",
    page_icon="⚾",
    layout="wide"
)

# Title
st.title("⚾ Fantasy Baseball AI - Sit/Start Analysis")
st.markdown("### Last Week of 2025 Season (Sept 28, 2025)")

# Find latest recommendations
rec_files = sorted(glob.glob('data/sitstart_recommendations_*.csv'), reverse=True)

if not rec_files:
    st.error("❌ No recommendations files found!")
    st.stop()

latest_file = rec_files[0]
file_timestamp = latest_file.split('_')[-2] + '_' + latest_file.split('_')[-1].replace('.csv', '')
file_date = datetime.strptime(file_timestamp, '%Y%m%d_%H%M%S')

st.sidebar.markdown(f"**Analysis Date:** {file_date.strftime('%Y-%m-%d %I:%M %p')}")
st.sidebar.markdown(f"**File:** `{os.path.basename(latest_file)}`")

# Load data
@st.cache_data
def load_data(filepath):
    return pd.read_csv(filepath)

df = load_data(latest_file)

# Display summary metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Players", len(df))

with col2:
    starts = len(df[df['recommendation'].str.contains('START', na=False)])
    st.metric("Recommended Starts", starts)

with col3:
    sits = len(df[df['recommendation'].str.contains('SIT', na=False)])
    st.metric("Recommended Sits", sits)

with col4:
    neutral = len(df[df['recommendation'].str.contains('NEUTRAL', na=False)])
    st.metric("Neutral", neutral)

st.markdown("---")

# Score distribution
st.subheader("📊 Score Distribution")
fig_hist = px.histogram(
    df, 
    x='final_score',
    nbins=30,
    title="Distribution of Player Scores",
    labels={'final_score': 'Final Score', 'count': 'Number of Players'},
    color_discrete_sequence=['#1f77b4']
)
fig_hist.update_layout(showlegend=False)
st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")

# Top Starts and Sits
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🌟 Top 10 Starts")
    top_starts = df.nlargest(10, 'final_score')[['player_name', 'final_score', 'recommendation']]
    top_starts.index = range(1, len(top_starts) + 1)
    st.dataframe(top_starts, use_container_width=True)

with col_right:
    st.subheader("🚫 Bottom 10 Sits")
    bottom_sits = df.nsmallest(10, 'final_score')[['player_name', 'final_score', 'recommendation']]
    bottom_sits.index = range(1, len(bottom_sits) + 1)
    st.dataframe(bottom_sits, use_container_width=True)

st.markdown("---")

# Factor Analysis
st.subheader("🔍 Factor Analysis")

# Get all factor columns (those ending with _score and _weight)
score_cols = [col for col in df.columns if col.endswith('_score') and col != 'final_score']
weight_cols = [col for col in df.columns if col.endswith('_weight')]

# Show factor weights
if weight_cols:
    st.markdown("#### Factor Weights")
    
    # Get unique weights for each factor
    factor_weights = {}
    for col in weight_cols:
        factor_name = col.replace('_weight', '')
        # Get the first non-zero weight value
        weight_val = df[col].iloc[0]
        factor_weights[factor_name.title()] = weight_val
    
    # Create bar chart
    fig_weights = px.bar(
        x=list(factor_weights.keys()),
        y=list(factor_weights.values()),
        labels={'x': 'Factor', 'y': 'Weight'},
        title='Factor Importance Weights',
        color_discrete_sequence=['#2ca02c']
    )
    fig_weights.update_layout(showlegend=False)
    st.plotly_chart(fig_weights, use_container_width=True)

st.markdown("---")

# Factor Scores Heatmap
if score_cols:
    st.markdown("#### Factor Scores by Player (Top 20)")
    
    # Prepare data for heatmap - top 20 players
    top_20 = df.nlargest(20, 'final_score')
    
    # Extract just the factor scores
    factor_data = top_20[['player_name'] + score_cols].copy()
    
    # Rename columns for display
    factor_data.columns = ['Player'] + [col.replace('_score', '').title() for col in score_cols]
    
    # Set player name as index
    factor_data = factor_data.set_index('Player')
    
    # Create heatmap
    fig_heatmap = px.imshow(
        factor_data.T,
        labels=dict(x="Player", y="Factor", color="Score"),
        x=factor_data.index,
        y=factor_data.columns,
        aspect="auto",
        color_continuous_scale='RdYlGn'
    )
    fig_heatmap.update_xaxes(side="bottom", tickangle=45)
    st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("---")

# Full data table
st.subheader("📋 Full Player Rankings")

# Add rank column
df_display = df.copy()
df_display['rank'] = range(1, len(df_display) + 1)

# Reorder columns
cols_order = ['rank', 'player_name', 'final_score', 'recommendation'] + score_cols
df_display = df_display[cols_order]

# Rename for display
display_names = {
    'rank': 'Rank',
    'player_name': 'Player',
    'final_score': 'Score',
    'recommendation': 'Recommendation'
}
for col in score_cols:
    display_names[col] = col.replace('_score', '').title() + ' Score'

df_display = df_display.rename(columns=display_names)

# Show table with formatting
st.dataframe(
    df_display.style.format({
        'Score': '{:.3f}',
        **{col: '{:.3f}' for col in df_display.columns if 'Score' in col and col != 'Score'}
    }).background_gradient(subset=['Score'], cmap='RdYlGn'),
    use_container_width=True,
    height=600
)

st.markdown("---")

# Search/Filter
st.subheader("🔎 Search Player")
search_term = st.text_input("Enter player name:")

if search_term:
    filtered = df[df['player_name'].str.contains(search_term, case=False, na=False)]
    
    if len(filtered) > 0:
        st.success(f"Found {len(filtered)} player(s)")
        
        for idx, row in filtered.iterrows():
            with st.expander(f"**{row['player_name']}** - Score: {row['final_score']:.3f}"):
                st.markdown(f"**Recommendation:** {row['recommendation']}")
                
                # Show all factor scores
                st.markdown("**Factor Breakdown:**")
                for col in score_cols:
                    factor_name = col.replace('_score', '').title()
                    weight_col = col.replace('_score', '_weight')
                    
                    score = row[col]
                    weight = row[weight_col] if weight_col in row else 0
                    
                    st.write(f"• {factor_name}: {score:.3f} (weight: {weight:.1%})")
    else:
        st.warning(f"No players found matching '{search_term}'")

# Factor Legend
st.markdown("---")
st.subheader("📖 Factor Analysis Legend")

factor_descriptions = {
    "Vegas": "15-20% impact - Vegas betting lines (O/U totals, implied team runs, win probability)",
    "Statcast": "10-15% impact - Advanced metrics (exit velocity, barrel rate, hard-hit %, xBA, xSLG)",
    "Matchup": "8-12% impact - Historical performance vs specific pitcher/team",
    "Bullpen": "8-12% impact - Opponent bullpen strength and fatigue levels",
    "Platoon": "8-12% impact - L/R handedness matchup advantages",
    "Home/Away": "5-8% impact - Home field advantage and home/road splits",
    "Injury": "5-8% impact - Player health status, DTD, recently returned from IL",
    "Park": "5-8% impact - Ballpark factors (hitter/pitcher friendly dimensions)",
    "Recent Form": "5-8% impact - Last 7/14/30 day performance trends",
    "Wind": "5-8% impact - Wind speed/direction (out = hitter boost, in = pitcher boost)",
    "Rest": "3-5% impact - Days off since last game (fresher = better)",
    "Temperature": "3-5% impact - Warmer weather helps offense (ball travels farther)",
    "Lineup": "3-5% impact - Batting order position (1-3 = more ABs)",
    "Umpire": "3-5% impact - Umpire strike zone tendencies",
    "Pitch Mix": "3-5% impact - Pitcher's arsenal vs batter's strengths",
    "Time": "1-3% impact - Day vs night game performance splits",
    "Humidity": "1-3% impact - Humidity and elevation effects on ball flight",
    "Defense": "1-3% impact - Defensive positioning shifts, quality of opponents' defense",
    "Monthly": "1-3% impact - Performance by month (Apr/May/June/July/Aug/Sept splits)",
    "Momentum": "1-3% impact - Team win/loss streaks and recent performance",
}

# Display in columns
col1, col2 = st.columns(2)

factors_list = list(factor_descriptions.items())
mid_point = len(factors_list) // 2

with col1:
    for factor, desc in factors_list[:mid_point]:
        st.markdown(f"**{factor}:** {desc}")

with col2:
    for factor, desc in factors_list[mid_point:]:
        st.markdown(f"**{factor}:** {desc}")

st.markdown("---")
st.info("""
**💡 How to Use These Scores:**
- **2.0+**: Elite matchup - Must start
- **0.5 to 2.0**: Favorable - Strong start candidate
- **-0.5 to 0.5**: Neutral - Consider other factors
- **-2.0 to -0.5**: Unfavorable - Bench candidate
- **Below -2.0**: Terrible matchup - Bench

**Note:** Weights are auto-tuned based on historical performance for your specific players.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    <p>Fantasy Baseball AI | Powered by 20+ Factor Analysis | Auto-Fetched Yahoo Rosters</p>
    <p>All scores range -2 to +2 | Higher = Better matchup | Weights optimized per player</p>
</div>
""", unsafe_allow_html=True)
