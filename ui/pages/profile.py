"""
Terra 2.0 — My Profile Page (Redesigned)
Beautiful profile dashboard with warm light theme colors and impressive layout.
"""

import streamlit as st
from sqlalchemy import select, func

from modules.auth import AuthManager
from modules.gamification import GamificationEngine
from modules.carbon_tracker import CarbonTracker
from database.db_setup import (
    get_engine, get_session,
    SwipeScore, MemeLog, EcoSearch, WasteLog, FootprintLog
)


def show():
    """Render the impressive profile page."""
    if not st.session_state.get("logged_in"):
        st.warning("Please log in first.")
        st.session_state["page"] = "login"
        st.rerun()
        return

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

    # ═══════ HERO CARD ═══════
    xp_for_next = level_info.get("xp_to_next", 500)
    xp_current = xp % xp_for_next if xp_for_next else 0
    xp_percent = min(100, int((xp_current / xp_for_next * 100) if xp_for_next else 0))

    avatar_url = f"https://api.dicebear.com/7.x/adventurer/svg?seed={avatar_seed}"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #3D7A5E 0%, #6BAF8A 100%);
         border-radius: 20px; padding: 32px; color: white; margin-bottom: 24px;">
        <div style="display:flex; align-items:center; gap:20px;">
            <img src="{avatar_url}" width="72" height="72"
                 style="border-radius:50%; border: 3px solid rgba(255,255,255,0.5);">
            <div style="flex: 1;">
                <div style="font-size:26px; font-weight:800">{username}</div>
                <div style="opacity:0.85; font-size:14px">Level {level} Earth Guardian · ID #{user_id}</div>
                <div style="margin-top:10px; background:rgba(255,255,255,0.2); border-radius:999px; height:8px; overflow:hidden">
                    <div style="width:{xp_percent}%; height:100%; background:white; border-radius:999px; transition: width 0.3s ease;"></div>
                </div>
                <div style="font-size:12px; opacity:0.75; margin-top:4px">{xp:,} / {xp + xp_for_next:,} XP to next level</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════ STATS ROW ═══════
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔥 Day Streak", f"{streak} days")
    with col2:
        # Get carbon saved (sum of all footprints for now)
        history = CarbonTracker.get_history(user_id)
        total_carbon = history["total_kg"].sum() if not history.empty else 0.0
        st.metric("🌱 Carbon Logged", f"{total_carbon:.1f} kg")
    with col3:
        st.metric("⭐ Level", f"{level}")
    with col4:
        st.metric("🎯 Total XP", f"{xp:,}")

    st.markdown("")

    # ═══════ ACTIVITY SUMMARY ═══════
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="color: #3D7A5E; font-weight: 800; margin-bottom: 16px; font-family: 'Plus Jakarta Sans', sans-serif;">
            📊 Activity Summary
        </h2>
    </div>
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

    # Activity stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    stats_data = [
        ("🌿", "Footprints", footprint_count, "Logged"),
        ("🃏", "Swipe Games", swipe_count, f"Best: {best_swipe or 0}"),
        ("😂", "Memes", meme_count, "Created"),
        ("♻️", "Waste Items", waste_count, "Classified"),
    ]
    
    for col, (emoji, label, value, delta) in zip([col1, col2, col3, col4], stats_data):
        with col:
            st.markdown(f"""
            <div class="terra-card" style="text-align: center; padding: 20px; background: linear-gradient(135deg, #FAF7F2 0%, #F2EDE4 100%);">
                <div style="font-size: 28px; margin-bottom: 8px;">{emoji}</div>
                <div style="font-size: 24px; font-weight: 700; color: #3D7A5E;">{value}</div>
                <div style="font-size: 12px; color: #5C5C5C; font-weight: 600; margin-top: 4px;">{label}</div>
                <div style="font-size: 11px; color: #9A9A9A; margin-top: 4px;">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")

    # ═══════ BADGES SECTION ═══════
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="color: #3D7A5E; font-weight: 800; margin-bottom: 16px; font-family: 'Plus Jakarta Sans', sans-serif;">
            🏅 My Badges
        </h2>
    </div>
    """, unsafe_allow_html=True)

    badges = GamificationEngine.get_user_badges(user_id)

    if badges:
        # Show badges in 4-column grid
        badge_cols = st.columns(min(len(badges), 4))
        for i, badge in enumerate(badges):
            col_idx = i % 4
            with badge_cols[col_idx]:
                badge_icon = badge.get('icon', '🏅')
                badge_name = badge.get('name', 'Badge')
                badge_desc = badge.get('description', '')
                
                st.markdown(f"""
                <div class="terra-card" style="text-align: center; padding: 20px; border: 2px solid #D4A853;">
                    <div style="font-size: 40px; margin-bottom: 8px;">{badge_icon}</div>
                    <div style="font-weight: 700; font-size: 14px; color: #2C2C2C; margin-bottom: 6px;">
                        {badge_name}
                    </div>
                    <div style="font-size: 11px; color: #9A9A9A;">
                        {badge_desc}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="terra-card" style="text-align: center; padding: 32px; background: #F2EDE4;">
            <div style="font-size: 2rem; margin-bottom: 8px;">🌟</div>
            <p style="color: #5C5C5C; font-weight: 600; margin: 0;">
                Complete activities to earn badges!
            </p>
            <p style="color: #9A9A9A; font-size: 0.9rem; margin-top: 4px;">
                Play games, log footprints, and explore to unlock achievements.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ═══════ PROFILE INFO CARD ═══════
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="color: #3D7A5E; font-weight: 800; margin-bottom: 16px; font-family: 'Plus Jakarta Sans', sans-serif;">
            ℹ️ Profile Information
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="terra-card" style="padding: 20px;">
            <div style="color: #9A9A9A; font-size: 12px; font-weight: 600; margin-bottom: 8px;">📧 EMAIL</div>
            <div style="color: #2C2C2C; font-weight: 600; margin-bottom: 16px;">{email}</div>
            
            <div style="color: #9A9A9A; font-size: 12px; font-weight: 600; margin-bottom: 8px;">🏫 COLLEGE</div>
            <div style="color: #2C2C2C; font-weight: 600; margin-bottom: 16px;">{college if college else '—'}</div>
            
            <div style="color: #9A9A9A; font-size: 12px; font-weight: 600; margin-bottom: 8px;">💼 ROLE</div>
            <div style="color: #2C2C2C; font-weight: 600;">{role.capitalize()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        joined_date = created_at[:10] if created_at else "—"
        st.markdown(f"""
        <div class="terra-card" style="padding: 20px;">
            <div style="color: #9A9A9A; font-size: 12px; font-weight: 600; margin-bottom: 8px;">📅 JOINED</div>
            <div style="color: #2C2C2C; font-weight: 600; margin-bottom: 16px;">{joined_date}</div>
            
            <div style="color: #9A9A9A; font-size: 12px; font-weight: 600; margin-bottom: 8px;">🎓 USER ID</div>
            <div style="color: #2C2C2C; font-weight: 600; margin-bottom: 16px;">#{user_id}</div>
            
            <div style="color: #9A9A9A; font-size: 12px; font-weight: 600; margin-bottom: 8px;">⭐ MEMBER STATUS</div>
            <div style="color: #3D7A5E; font-weight: 700;">Active Member</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ═══════ ACTION BUTTONS ═══════
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🏠 Back to Home", use_container_width=True, key="profile_home"):
            st.session_state["page"] = "home"
            st.rerun()
    
    with col2:
        if st.button("⚙️ Settings", use_container_width=True, key="profile_settings"):
            st.info("Settings coming soon! 🚀")
    
    with col3:
        if st.button("🚪 Sign Out", use_container_width=True, key="profile_logout"):
            st.query_params.clear()
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
