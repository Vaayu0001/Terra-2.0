"""
Terra 2.0 — College Leaderboard Page
Displays inter-college rankings with podium and bar chart.
"""

import streamlit as st
import plotly.graph_objects as go

from ui.components import page_header
from modules.leaderboard import CollegeLeaderboard
from modules.auth import AuthManager


def show():
    """Render the College Leaderboard page."""
    if not st.session_state.get("logged_in"):
        st.warning("Please log in first.")
        st.session_state["page"] = "login"
        st.rerun()
        return

    page_header("College Leaderboard", "See which college leads the green revolution!", "🏆")

    user_id = st.session_state.get("user_id")
    college = st.session_state.get("college", "")

    # Update current user's college stats
    if college:
        user_data = AuthManager.get_user(user_id)
        xp = user_data["xp"] if user_data else 0
        CollegeLeaderboard.update_college(college, xp, 0.0)

    # Get rankings
    rankings = CollegeLeaderboard.get_rankings()

    if rankings.empty:
        st.markdown("""
        <div class="terra-card-glow" style="text-align: center; padding: 3rem;">
            <div style="font-size: 3rem;">🏆</div>
            <h3 style="color: #F5F0E8;">No colleges ranked yet!</h3>
            <p style="color: #7EC8E3;">
                Start earning XP to put your college on the leaderboard!
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    # ═══════ Top 3 Podium ═══════
    st.markdown("""
    <h3 style="text-align: center; color: #F4C430; margin-bottom: 1.5rem;">
        🥇 Top Colleges
    </h3>
    """, unsafe_allow_html=True)

    top_3 = rankings.head(3)

    if len(top_3) >= 3:
        # Podium layout: 2nd, 1st, 3rd
        col2, col1, col3 = st.columns([1, 1.2, 1])

        podium_data = [
            (col1, top_3.iloc[0], "🥇", "#F4C430", "2.5rem", "200px"),
            (col2, top_3.iloc[1], "🥈", "#C0C0C0", "2rem", "160px"),
            (col3, top_3.iloc[2], "🥉", "#CD7F32", "2rem", "130px"),
        ]

        for col, data, medal, color, font_size, height in podium_data:
            with col:
                is_user_college = data["college_name"] == college
                border_color = "#2ECC71" if is_user_college else f"rgba(46, 204, 113, 0.2)"
                glow = "0 0 30px rgba(46, 204, 113, 0.3)" if is_user_college else "none"

                st.markdown(f"""
                <div class="terra-card" style="
                    text-align: center;
                    padding: 1.5rem 1rem;
                    min-height: {height};
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    border-color: {border_color};
                    box-shadow: {glow};
                ">
                    <div style="font-size: {font_size}; margin-bottom: 0.3rem;">{medal}</div>
                    <div style="
                        font-size: 1rem;
                        font-weight: 700;
                        color: {color};
                        word-wrap: break-word;
                    ">{data['college_name']}</div>
                    <div style="
                        font-size: 1.3rem;
                        font-weight: 700;
                        color: #2ECC71;
                        margin: 0.5rem 0;
                    ">{data['total_xp']:,} XP</div>
                    <div style="color: #7EC8E3; font-size: 0.8rem;">
                        👥 {data['member_count']} members
                    </div>
                    <div style="color: rgba(245,240,232,0.5); font-size: 0.75rem; margin-top: 0.2rem;">
                        📊 Avg: {data['avg_footprint']:.1f} kg/day
                    </div>
                </div>
                """, unsafe_allow_html=True)
    elif len(top_3) >= 1:
        # Show whatever we have
        for i, (_, data) in enumerate(top_3.iterrows()):
            medals = ["🥇", "🥈", "🥉"]
            st.markdown(f"""
            <div class="terra-card" style="text-align: center; padding: 1.5rem;">
                <span style="font-size: 2rem;">{medals[i]}</span>
                <span style="color: #F5F0E8; font-weight: 700; font-size: 1.1rem; margin-left: 0.5rem;">
                    {data['college_name']}
                </span>
                <span style="color: #2ECC71; font-weight: 600; margin-left: 1rem;">
                    {data['total_xp']:,} XP
                </span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")

    # ═══════ User's College Rank ═══════
    if college:
        user_rank = CollegeLeaderboard.get_user_college_rank(college)
        if user_rank > 0:
            st.markdown(f"""
            <div class="terra-card-glow" style="text-align: center; padding: 1rem;">
                <span style="color: #7EC8E3; font-size: 0.9rem;">Your college</span>
                <span style="color: #F5F0E8; font-weight: 700; font-size: 1.1rem; margin: 0 0.5rem;">
                    {college}
                </span>
                <span style="color: #F4C430; font-size: 0.9rem;">
                    is ranked #{user_rank} 🎉
                </span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")

    # ═══════ Full Rankings Bar Chart ═══════
    st.markdown("""
    <h3 style="color: #7EC8E3; margin-bottom: 1rem;">📊 Full Rankings</h3>
    """, unsafe_allow_html=True)

    # Bar chart
    bar_colors = []
    for _, row in rankings.iterrows():
        if row["college_name"] == college:
            bar_colors.append("#2ECC71")
        else:
            bar_colors.append("#7EC8E3")

    fig = go.Figure(data=[
        go.Bar(
            x=rankings["college_name"],
            y=rankings["total_xp"],
            marker_color=bar_colors,
            text=rankings["total_xp"].apply(lambda x: f"{x:,}"),
            textposition="auto",
            textfont=dict(color="#F5F0E8", size=12),
        )
    ])

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F5F0E8"),
        xaxis=dict(
            gridcolor="rgba(46,204,113,0.1)",
            title="College",
            tickangle=-45,
        ),
        yaxis=dict(
            gridcolor="rgba(46,204,113,0.1)",
            title="Total XP",
        ),
        height=400,
        margin=dict(t=20, b=100, l=60, r=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ═══════ Full Table ═══════
    st.markdown("""
    <h3 style="color: #7EC8E3; margin-bottom: 1rem;">📋 Detailed Rankings</h3>
    """, unsafe_allow_html=True)

    for _, row in rankings.iterrows():
        is_user = row["college_name"] == college
        border = "2px solid #2ECC71" if is_user else "1px solid rgba(46,204,113,0.2)"
        bg = "rgba(46,204,113,0.15)" if is_user else "rgba(45,74,62,0.4)"

        medals = {1: "🥇", 2: "🥈", 3: "🥉"}
        rank_display = medals.get(row["rank"], f"#{row['rank']}")

        st.markdown(f"""
        <div style="
            background: {bg};
            border: {border};
            border-radius: 12px;
            padding: 0.8rem 1.2rem;
            margin-bottom: 0.4rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div>
                <span style="font-size: 1.2rem; margin-right: 0.5rem;">{rank_display}</span>
                <span style="color: #F5F0E8; font-weight: 600;">{row['college_name']}</span>
                {'<span style="color: #2ECC71; font-size: 0.75rem; margin-left: 0.5rem;">(You)</span>' if is_user else ''}
            </div>
            <div style="display: flex; gap: 1.5rem; align-items: center;">
                <span style="color: #F4C430; font-weight: 600;">{row['total_xp']:,} XP</span>
                <span style="color: #7EC8E3; font-size: 0.85rem;">👥 {row['member_count']}</span>
                <span style="color: rgba(245,240,232,0.5); font-size: 0.8rem;">
                    📊 {row['avg_footprint']:.1f} kg/day
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
