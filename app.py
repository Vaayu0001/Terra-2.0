"""
Terra 2.0 — Main Application Entry Point
Gamified Environmental Education Platform for Gen Z

Run with: streamlit run app.py
"""

import streamlit as st

# ═══════ PAGE CONFIG — MUST BE FIRST STREAMLIT CALL ═══════
st.set_page_config(
    page_title="Terra 2.0",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════ DATABASE INITIALIZATION ═══════
from database.db_setup import get_engine, init_db

engine = get_engine()
init_db(engine)

# ═══════ CSS INJECTION ═══════
from ui.styles import get_global_css

st.markdown(f"<style>{get_global_css()}</style>", unsafe_allow_html=True)

# ═══════ RENDER PARTICLES ═══════
from ui.components import render_particles

render_particles()

# ═══════ SESSION STATE INITIALIZATION ═══════
defaults = {
    "logged_in": False,
    "user_id": None,
    "username": None,
    "college": None,
    "role": None,
    "xp": 0,
    "level": 1,
    "streak": 0,
    "page": "login",
    "swipe_questions": [],
    "swipe_idx": 0,
    "swipe_score": 0,
    "swipe_answers": [],
    "swipe_game_over": False,
    "swipe_answered": False,
    "carbon_step": 1,
    "carbon_data": {},
    "meme_top_text": "",
    "meme_bottom_text": "",
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ═══════ IMPORTS ═══════
from modules.auth import AuthManager
from modules.gamification import GamificationEngine
from ui.components import level_progress_bar


# ═══════ LOGIN PAGE ═══════
def show_auth_page():
    """Render the login/signup page."""
    from ui.pages.login import show
    show()


# ═══════ SIDEBAR ═══════
def show_sidebar():
    """Render the sidebar with navigation."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0; margin-bottom: 0.5rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🌿</div>
            <h2 style="
                margin: 0;
                color: #3D7A5E;
                font-size: 1.5rem;
                font-weight: 800;
                font-family: 'Plus Jakarta Sans', sans-serif;
            ">Terra 2.0</h2>
        </div>
        """, unsafe_allow_html=True)

        # User info
        username = st.session_state.get("username", "User")
        xp = st.session_state.get("xp", 0)
        level_info = GamificationEngine.calculate_level(xp)

        avatar_url = f"https://api.dicebear.com/7.x/adventurer/svg?seed={username}"
        st.markdown(f"""
        <div style="
            text-align: center;
            margin: 1rem 0;
            padding: 1rem;
            background: #FFFFFF;
            border: 1px solid #E8E0D5;
            border-radius: 12px;
        ">
            <img src="{avatar_url}" width="60" height="60"
                 style="border-radius: 50%; border: 2px solid #3D7A5E; display: block; margin: 0 auto 0.5rem;">
            <div style="color: #2C2C2C; font-weight: 700; margin-bottom: 0.2rem;">
                {username}
            </div>
            <div style="color: #D4A853; font-size: 0.75rem; font-weight: 600;">
                Lv.{level_info['level']} {level_info['name']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        level_progress_bar(xp)

        st.markdown("---")

        # Navigation
        pages = {
            "🏠 Home": "home",
            "🌿 Carbon Tracker": "carbon",
            "🔥 AI Roast": "roast",
            "🃏 Eco Swipe": "swipe",
            "🏆 Leaderboard": "leaderboard",
            "😂 Meme Factory": "meme",
            "📦 Eco Score": "eco_score",
            "♻️ Waste Classifier": "waste",
            "👤 My Profile": "profile",
        }

        current_page = st.session_state.get("page", "home")
        
        selected = st.radio(
            "Navigate",
            options=list(pages.keys()),
            index=list(pages.values()).index(current_page) if current_page in pages.values() else 0,
            key="sidebar_nav",
            label_visibility="collapsed",
        )

        if selected and pages.get(selected) != current_page:
            st.session_state["page"] = pages[selected]
            st.rerun()

        st.markdown("---")

        # Quick stats
        streak = st.session_state.get("streak", 0)
        st.markdown(f"""
        <div style="
            text-align: center;
            color: #5C5C5C;
            font-size: 0.85rem;
            font-weight: 500;
            padding: 1rem;
            background: #F2EDE4;
            border-radius: 10px;
        ">
            🔥 Streak: {streak} days<br>
            ⭐ {xp:,} XP Total
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # Logout button
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ═══════ PAGE ROUTER ═══════
def route_page():
    """Route to the appropriate page based on session state."""
    page = st.session_state.get("page", "home")

    try:
        if page == "home":
            from ui.pages.home import show
            show()
        elif page == "carbon":
            from ui.pages.carbon import show
            show()
        elif page == "roast":
            from ui.pages.roast import show
            show()
        elif page == "swipe":
            from ui.pages.swipe import show
            show()
        elif page == "leaderboard":
            from ui.pages.leaderboard_page import show
            show()
        elif page == "meme":
            from ui.pages.meme import show
            show()
        elif page == "eco_score":
            from ui.pages.eco_score_page import show
            show()
        elif page == "waste":
            from ui.pages.waste import show
            show()
        elif page == "profile":
            from ui.pages.profile import show
            show()
        elif page == "login":
            show_auth_page()
        else:
            from ui.pages.home import show
            show()
    except Exception as e:
        st.error(f"Error loading page: {str(e)}")
        st.info("Returning to home page...")
        st.session_state["page"] = "home"
        st.rerun()


# ═══════ MAIN ═══════
if not st.session_state.get("logged_in"):
    show_auth_page()
else:
    show_sidebar()
    route_page()
