"""
Terra 2.0 — My Profile Page
Displays avatar, stats, badges, XP history, and level progress.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from sqlalchemy import select, func

from ui.components import page_header, level_progress_bar, metric_row
from modules.auth import AuthManager
from modules.gamification import GamificationEngine
from modules.carbon_tracker import CarbonTracker
from database.db_setup import (
    get_engine, get_session,
    SwipeScore, MemeLog, EcoSearch, WasteLog, FootprintLog
)


def show():
    """Render the My Profile page."""
    if not st.session_state.get("logged_in"):
        st.warning("Please log in first.")
        st.session_state["page"] = "login"
        st.rerun()
        return

    page_header("My Profile", "Your eco journey at a glance", "👤")

    user_id = st.session_state.get("user_id")

    # Refresh user data
    user_data = AuthManager.get_user(user_id)
    if not user_data:
        st.error("User not found!")
        return

    username = user_data["username"]
    email = user_data["email"]
    college = user_data["college"]
    role = user_data["role"]
    xp = user_data["xp"]
    level = user_data["level"]
    streak = user_data["streak"]
    avatar_seed = user_data.get("avatar_seed", username)
    created_at = user_data.get("created_at", "")
    level_info = GamificationEngine.calculate_level(xp)

    # ═══════ Profile Header ═══════
    col_avatar, col_info = st.columns([1, 3])

    with col_avatar:
        avatar_url = f"https://api.dicebear.com/7.x/adventurer/svg?seed={avatar_seed}"
        st.markdown(f"""
        <div class="terra-card-glow" style="text-align: center; padding: 1.5rem;">
            <img src="{avatar_url}" width="120" height="120"
                 style="border-radius: 50%; border: 3px solid #2ECC71;
                        box-shadow: 0 0 20px rgba(46, 204, 113, 0.3);">
            <div style="
                font-size: 1.2rem;
                font-weight: 700;
                color: #F5F0E8;
                margin-top: 0.8rem;
            ">{username}</div>
            <div style="color: #2ECC71; font-size: 0.85rem;">{role.capitalize()}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_info:
        st.markdown(f"""
        <div class="terra-card" style="padding: 1.5rem;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <div style="color: #7EC8E3; font-size: 0.8rem;">📧 Email</div>
                    <div style="color: #F5F0E8;">{email}</div>
                </div>
                <div>
                    <div style="color: #7EC8E3; font-size: 0.8rem;">🏫 College</div>
                    <div style="color: #F5F0E8;">{college}</div>
                </div>
                <div>
                    <div style="color: #7EC8E3; font-size: 0.8rem;">📅 Joined</div>
                    <div style="color: #F5F0E8;">{created_at[:10] if created_at else 'N/A'}</div>
                </div>
                <div>
                    <div style="color: #7EC8E3; font-size: 0.8rem;">🔥 Streak</div>
                    <div style="color: #F4C430; font-weight: 700;">{streak} days</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ═══════ Level & XP Card ═══════
    st.markdown("""
    <h3 style="color: #F4C430;">⭐ Level & Experience</h3>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="terra-card-glow" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2.5rem; font-weight: 700; color: #F4C430;">
            Level {level}
        </div>
        <div style="font-size: 1.2rem; color: #2ECC71; font-weight: 600;">
            {level_info['name']}
        </div>
        <div style="color: #7EC8E3; font-size: 0.9rem; margin: 0.5rem 0;">
            Total XP: {xp:,}
        </div>
    </div>
    """, unsafe_allow_html=True)

    level_progress_bar(xp)

    st.markdown("")

    # ═══════ Stats Summary ═══════
    st.markdown("""
    <h3 style="color: #7EC8E3;">📊 Activity Summary</h3>
    """, unsafe_allow_html=True)

    engine = get_engine()
    with get_session(engine) as session:
        footprint_count = session.execute(
            select(func.count(FootprintLog.id)).where(
                FootprintLog.user_id == user_id
            )
        ).scalar() or 0

        swipe_count = session.execute(
            select(func.count(SwipeScore.id)).where(
                SwipeScore.user_id == user_id
            )
        ).scalar() or 0

        best_swipe = session.execute(
            select(func.max(SwipeScore.correct)).where(
                SwipeScore.user_id == user_id
            )
        ).scalar() or 0

        meme_count = session.execute(
            select(func.count(MemeLog.id)).where(
                MemeLog.user_id == user_id
            )
        ).scalar() or 0

        search_count = session.execute(
            select(func.count(EcoSearch.id)).where(
                EcoSearch.user_id == user_id
            )
        ).scalar() or 0

        waste_count = session.execute(
            select(func.count(WasteLog.id)).where(
                WasteLog.user_id == user_id
            )
        ).scalar() or 0

    metric_row([
        {"label": "Footprints Logged", "value": str(footprint_count), "emoji": "🌿", "delta": ""},
        {"label": "Swipe Games", "value": str(swipe_count), "emoji": "🃏", "delta": f"Best: {best_swipe}/10"},
        {"label": "Memes Created", "value": str(meme_count), "emoji": "😂", "delta": ""},
        {"label": "Products Searched", "value": str(search_count), "emoji": "🔍", "delta": ""},
    ])

    st.markdown("")

    metric_row([
        {"label": "Waste Classified", "value": str(waste_count), "emoji": "♻️", "delta": ""},
        {"label": "XP to Next Level", "value": str(level_info["xp_to_next"]), "emoji": "🎯", "delta": ""},
        {"label": "Level Progress", "value": f"{level_info['progress_pct']}%", "emoji": "📈", "delta": ""},
        {"label": "Total XP", "value": f"{xp:,}", "emoji": "💎", "delta": ""},
    ])

    st.markdown("")

    # ═══════ Badges Grid ═══════
    st.markdown("""
    <h3 style="color: #F4C430;">🏅 My Badges</h3>
    """, unsafe_allow_html=True)

    badges = GamificationEngine.get_user_badges(user_id)

    if badges:
        badge_cols = st.columns(min(len(badges), 4))
        for i, badge in enumerate(badges):
            col_idx = i % 4
            with st.columns(4)[col_idx]:
                st.markdown(f"""
                <div class="badge-item" style="margin-bottom: 0.5rem;">
                    <div style="font-size: 2rem;">{badge['icon']}</div>
                    <div style="
                        color: #F5F0E8;
                        font-size: 0.75rem;
                        font-weight: 600;
                        margin-top: 0.3rem;
                    ">{badge['name']}</div>
                    <div style="
                        color: rgba(245, 240, 232, 0.4);
                        font-size: 0.65rem;
                    ">{badge.get('earned_at', '')[:10]}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="terra-card" style="text-align: center; padding: 1.5rem;
             color: rgba(245, 240, 232, 0.5);">
            No badges earned yet. Complete activities to unlock badges! 🏅
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ═══════ XP History / Footprint Trend ═══════
    st.markdown("""
    <h3 style="color: #7EC8E3;">📈 Footprint History</h3>
    """, unsafe_allow_html=True)

    history = CarbonTracker.get_history(user_id)
    if not history.empty and len(history) >= 2:
        fig = px.line(
            history.sort_values("date"),
            x="date",
            y=["transport_kg", "food_kg", "energy_kg", "shopping_kg", "total_kg"],
            title="Carbon Footprint Over Time",
            labels={"date": "Date", "value": "CO2 (kg)", "variable": "Category"},
            markers=True,
        )

        color_map = {
            "transport_kg": "#7EC8E3",
            "food_kg": "#2ECC71",
            "energy_kg": "#F4C430",
            "shopping_kg": "#FF6B35",
            "total_kg": "#F5F0E8",
        }
        for trace in fig.data:
            if trace.name in color_map:
                trace.line.color = color_map[trace.name]

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F5F0E8"),
            xaxis=dict(gridcolor="rgba(46,204,113,0.1)"),
            yaxis=dict(gridcolor="rgba(46,204,113,0.1)"),
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                font=dict(color="#F5F0E8"),
            ),
            height=400,
            margin=dict(t=40, b=40, l=40, r=20),
            title=dict(font=dict(color="#F5F0E8")),
        )
        st.plotly_chart(fig, use_container_width=True)
    elif not history.empty:
        st.markdown("""
        <div class="terra-card" style="text-align: center; padding: 1.5rem;
             color: rgba(245, 240, 232, 0.5);">
            📈 Log more footprints to see your trend over time!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="terra-card" style="text-align: center; padding: 1.5rem;
             color: rgba(245, 240, 232, 0.5);">
            📈 No footprint data yet. Start tracking! 🌿
        </div>
        """, unsafe_allow_html=True)
