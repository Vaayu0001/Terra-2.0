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


# ═══════ LOGIN / REGISTER PAGE ═══════
def show_auth_page():
    """Render the login/register page."""

    col_brand, col_form = st.columns([1, 1], gap="large")

    with col_brand:
        st.markdown("""
        <div style="
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
            padding: 3rem 1rem;
        ">
            <div style="
                font-size: 6rem;
                animation: pulse 2s ease infinite;
            ">🌍</div>
            <h1 style="
                font-size: 3rem;
                margin: 1rem 0 0.5rem 0;
                background: linear-gradient(135deg, #2ECC71, #7EC8E3);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 700;
            ">Terra 2.0</h1>
            <p style="
                color: #7EC8E3;
                font-size: 1.2rem;
                text-align: center;
                max-width: 400px;
            ">Your planet needs a glow-up. Start here.</p>
            <div style="
                margin-top: 2rem;
                color: rgba(245, 240, 232, 0.5);
                font-size: 0.85rem;
                text-align: center;
            ">
                🌿 Carbon Tracker • 🔥 AI Roast • 🃏 Eco Swipe<br>
                🏆 Leaderboard • 😂 Meme Factory • 📦 Eco Score<br>
                ♻️ Waste Classifier • 🎮 XP & Badges
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        st.markdown("""
        <div class="terra-card-glow" style="padding: 2rem;">
            <h2 style="text-align: center; color: #F5F0E8; margin-bottom: 1rem;">
                Join the Movement 🌱
            </h2>
        </div>
        """, unsafe_allow_html=True)

        auth_tab = st.radio(
            "Choose action",
            ["🔑 Login", "📝 Register"],
            horizontal=True,
            key="auth_tab",
            label_visibility="collapsed"
        )

        if auth_tab == "🔑 Login":
            _show_login_form()
        else:
            _show_register_form()


def _show_login_form():
    """Render the login form."""
    with st.form("login_form"):
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        submitted = st.form_submit_button(
            "🔑 Login",
            use_container_width=True
        )

        if submitted:
            if not username or not password:
                st.error("Please fill in all fields!")
            else:
                user = AuthManager.login(username.strip(), password)
                if user:
                    # Award daily login XP
                    xp_result = GamificationEngine.award_xp(
                        user["user_id"], "daily_login"
                    )

                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = user["user_id"]
                    st.session_state["username"] = user["username"]
                    st.session_state["college"] = user["college"]
                    st.session_state["role"] = user["role"]
                    st.session_state["xp"] = user["xp"] + xp_result.get("xp_earned", 0)
                    st.session_state["level"] = xp_result.get("new_level", user["level"])
                    st.session_state["streak"] = user["streak"]
                    st.session_state["page"] = "home"
                    st.rerun()
                else:
                    st.error("Invalid username or password!")


def _show_register_form():
    """Render the registration form."""
    with st.form("register_form"):
        username = st.text_input(
            "Username",
            placeholder="Choose a unique username",
            key="reg_username"
        )
        email = st.text_input(
            "Email",
            placeholder="your@email.com",
            key="reg_email"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Min 6 characters",
            key="reg_password"
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter password",
            key="reg_confirm"
        )
        college = st.text_input(
            "College / University",
            placeholder="e.g., IIT Madras, SRM University",
            key="reg_college"
        )
        role = st.selectbox(
            "Role",
            ["student", "faculty", "researcher", "enthusiast"],
            key="reg_role"
        )

        submitted = st.form_submit_button(
            "📝 Create Account",
            use_container_width=True
        )

        if submitted:
            if not all([username, email, password, confirm_password, college]):
                st.error("Please fill in all fields!")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters!")
            elif password != confirm_password:
                st.error("Passwords don't match!")
            elif "@" not in email:
                st.error("Please enter a valid email!")
            else:
                result = AuthManager.register(
                    username.strip(),
                    email.strip(),
                    password,
                    college.strip(),
                    role,
                )

                if result["success"]:
                    st.success("🎉 Account created! Please log in.")
                    st.balloons()
                else:
                    st.error(f"Registration failed: {result['error']}")


# ═══════ SIDEBAR ═══════
def show_sidebar():
    """Render the sidebar with navigation."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 2rem;">🌍</div>
            <h2 style="
                margin: 0.3rem 0;
                background: linear-gradient(135deg, #2ECC71, #7EC8E3);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 1.5rem;
            ">Terra 2.0</h2>
        </div>
        """, unsafe_allow_html=True)

        # User info
        username = st.session_state.get("username", "User")
        xp = st.session_state.get("xp", 0)
        level_info = GamificationEngine.calculate_level(xp)

        avatar_url = f"https://api.dicebear.com/7.x/adventurer/svg?seed={username}"
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <img src="{avatar_url}" width="60" height="60"
                 style="border-radius: 50%; border: 2px solid #2ECC71;">
            <div style="color: #F5F0E8; font-weight: 600; margin-top: 0.3rem;">
                {username}
            </div>
            <div style="color: #F4C430; font-size: 0.8rem;">
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
        current_label = "🏠 Home"
        for label, key in pages.items():
            if key == current_page:
                current_label = label
                break

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
        <div style="text-align: center; color: rgba(245, 240, 232, 0.6); font-size: 0.8rem;">
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
