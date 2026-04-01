"""
Terra 2.0 — World-Class Login/Signup Page
Beautiful centered card design with smooth transitions and modern UX.
"""

import streamlit as st
from modules.auth import AuthManager


def show():
    """Render the stunning login/signup page."""
    
    # Center the login card using columns
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        # Logo section
        st.markdown("""
        <div style="text-align:center; padding: 40px 0 32px 0; margin-bottom: 0;">
            <div style="font-size: 56px; margin-bottom: 12px; animation: pulse 2s ease infinite;">🌿</div>
            <h1 style="font-size: 32px; font-weight: 800; color: #2C2C2C; margin: 0; font-family: 'Plus Jakarta Sans', sans-serif;">
                Terra 2.0
            </h1>
            <p style="color: #9A9A9A; margin-top: 8px; font-size: 15px; font-weight: 500;">
                Your planet. Your impact.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs for login/signup
        tab_login, tab_signup = st.tabs(["🔑 Sign In", "📝 Create Account"])
        
        with tab_login:
            _render_login_form()
        
        with tab_signup:
            _render_signup_form()
        
        st.markdown("")
        
        # Feature pills
        st.markdown("""
        <div style="
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            margin-top: 24px;
            padding-top: 16px;
            border-top: 1px solid #E8E0D5;
        ">
            <span class="badge-pill">🌿 Carbon Tracker</span>
            <span class="badge-pill">🎮 Eco Games</span>
            <span class="badge-pill">🏆 Leaderboard</span>
            <span class="badge-pill">🤖 AI Roast</span>
        </div>
        """, unsafe_allow_html=True)


def _render_login_form():
    """Render the login form."""
    with st.form("login_form", border=False):
        st.markdown("""
        <div style="padding: 8px 0;">
            <label style="display: block; color: #5C5C5C; font-size: 13px; font-weight: 600; margin-bottom: 8px;">
                👤 Username
            </label>
        </div>
        """, unsafe_allow_html=True)
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            label_visibility="collapsed",
            key="login_username"
        )
        
        st.markdown("""
        <div style="padding: 12px 0 8px 0;">
            <label style="display: block; color: #5C5C5C; font-size: 13px; font-weight: 600; margin-bottom: 8px;">
                🔒 Password
            </label>
        </div>
        """, unsafe_allow_html=True)
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            label_visibility="collapsed",
            key="login_password"
        )
        
        st.markdown("<div style='padding: 12px 0;'></div>", unsafe_allow_html=True)
        
        submit = st.form_submit_button(
            "🚀 Continue with Terra",
            use_container_width=True,
            key="login_submit"
        )
        
        if submit:
            if not username or not password:
                st.markdown("""
                <div style="
                    background: #FEF3F2;
                    border: 1.5px solid #FCCAB1;
                    border-radius: 12px;
                    padding: 12px 16px;
                    color: #B42318;
                    font-weight: 500;
                    font-size: 14px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-top: 16px;
                ">
                    <span>❌</span>
                    <span>Please fill in all fields</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                with st.spinner("🔐 Signing you in..."):
                    result = AuthManager.login(username.strip(), password)
                    
                    if result is not None:
                        st.session_state["logged_in"] = True
                        st.session_state["user_id"] = result["user_id"]
                        st.session_state["username"] = result["username"]
                        st.session_state["college"] = result.get("college", "")
                        st.session_state["xp"] = result.get("xp", 0)
                        st.session_state["level"] = result.get("level", 1)
                        st.session_state["role"] = result.get("role", "student")
                        st.session_state["streak"] = result.get("streak", 0)
                        st.session_state["page"] = "home"
                        
                        # Set query param for session persistence on refresh
                        st.query_params["uid"] = str(result["user_id"])
                        
                        st.markdown("""
                        <div style="
                            background: #F0FDF4;
                            border: 1.5px solid #86EFAC;
                            border-radius: 12px;
                            padding: 12px 16px;
                            color: #15803D;
                            font-weight: 500;
                            font-size: 14px;
                            display: flex;
                            align-items: center;
                            gap: 10px;
                            margin-top: 16px;
                        ">
                            <span>✅</span>
                            <span>Welcome back! Redirecting...</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.balloons()
                        st.rerun()
                    else:
                        st.markdown("""
                        <div style="
                            background: #FEF3F2;
                            border: 1.5px solid #FCCAB1;
                            border-radius: 12px;
                            padding: 12px 16px;
                            color: #B42318;
                            font-weight: 500;
                            font-size: 14px;
                            display: flex;
                            align-items: center;
                            gap: 10px;
                            margin-top: 16px;
                        ">
                            <span>❌</span>
                            <span>Invalid username or password</span>
                        </div>
                        """, unsafe_allow_html=True)


def _render_signup_form():
    """Render the signup form."""
    with st.form("signup_form", border=False):
        st.markdown("""
        <div style="padding: 8px 0;">
            <label style="display: block; color: #5C5C5C; font-size: 13px; font-weight: 600; margin-bottom: 8px;">
                👤 Username
            </label>
        </div>
        """, unsafe_allow_html=True)
        username = st.text_input(
            "Username",
            placeholder="Choose a username",
            label_visibility="collapsed",
            key="reg_username"
        )
        
        st.markdown("""
        <div style="padding: 12px 0 8px 0;">
            <label style="display: block; color: #5C5C5C; font-size: 13px; font-weight: 600; margin-bottom: 8px;">
                📧 Email
            </label>
        </div>
        """, unsafe_allow_html=True)
        email = st.text_input(
            "Email",
            placeholder="your@email.com",
            label_visibility="collapsed",
            key="reg_email"
        )
        
        st.markdown("""
        <div style="padding: 12px 0 8px 0;">
            <label style="display: block; color: #5C5C5C; font-size: 13px; font-weight: 600; margin-bottom: 8px;">
                🔒 Password
            </label>
        </div>
        """, unsafe_allow_html=True)
        password = st.text_input(
            "Password",
            type="password",
            placeholder="At least 6 characters",
            label_visibility="collapsed",
            key="reg_password"
        )
        
        st.markdown("""
        <div style="padding: 12px 0 8px 0;">
            <label style="display: block; color: #5C5C5C; font-size: 13px; font-weight: 600; margin-bottom: 8px;">
                🔐 Confirm Password
            </label>
        </div>
        """, unsafe_allow_html=True)
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter password",
            label_visibility="collapsed",
            key="reg_confirm"
        )
        
        st.markdown("""
        <div style="padding: 12px 0 8px 0;">
            <label style="display: block; color: #5C5C5C; font-size: 13px; font-weight: 600; margin-bottom: 8px;">
                🎓 College / University
            </label>
        </div>
        """, unsafe_allow_html=True)
        college = st.text_input(
            "College",
            placeholder="e.g., IIT Madras, SRM University",
            label_visibility="collapsed",
            key="reg_college"
        )
        
        st.markdown("""
        <div style="padding: 12px 0 8px 0;">
            <label style="display: block; color: #5C5C5C; font-size: 13px; font-weight: 600; margin-bottom: 8px;">
                💼 Role
            </label>
        </div>
        """, unsafe_allow_html=True)
        role = st.selectbox(
            "Select your role",
            ["student", "faculty", "researcher", "enthusiast"],
            label_visibility="collapsed",
            key="reg_role"
        )
        
        st.markdown("<div style='padding: 12px 0;'></div>", unsafe_allow_html=True)
        
        submit = st.form_submit_button(
            "📝 Create My Account",
            use_container_width=True,
            key="signup_submit"
        )
        
        if submit:
            if not all([username, email, password, confirm_password, college]):
                st.markdown("""
                <div style="
                    background: #FEF3F2;
                    border: 1.5px solid #FCCAB1;
                    border-radius: 12px;
                    padding: 12px 16px;
                    color: #B42318;
                    font-weight: 500;
                    font-size: 14px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-top: 16px;
                ">
                    <span>❌</span>
                    <span>Please fill in all fields</span>
                </div>
                """, unsafe_allow_html=True)
            elif len(password) < 6:
                st.markdown("""
                <div style="
                    background: #FEF3F2;
                    border: 1.5px solid #FCCAB1;
                    border-radius: 12px;
                    padding: 12px 16px;
                    color: #B42318;
                    font-weight: 500;
                    font-size: 14px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-top: 16px;
                ">
                    <span>❌</span>
                    <span>Password must be at least 6 characters</span>
                </div>
                """, unsafe_allow_html=True)
            elif password != confirm_password:
                st.markdown("""
                <div style="
                    background: #FEF3F2;
                    border: 1.5px solid #FCCAB1;
                    border-radius: 12px;
                    padding: 12px 16px;
                    color: #B42318;
                    font-weight: 500;
                    font-size: 14px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-top: 16px;
                ">
                    <span>❌</span>
                    <span>Passwords don't match</span>
                </div>
                """, unsafe_allow_html=True)
            elif "@" not in email:
                st.markdown("""
                <div style="
                    background: #FEF3F2;
                    border: 1.5px solid #FCCAB1;
                    border-radius: 12px;
                    padding: 12px 16px;
                    color: #B42318;
                    font-weight: 500;
                    font-size: 14px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-top: 16px;
                ">
                    <span>❌</span>
                    <span>Please enter a valid email</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                with st.spinner("📝 Creating your account..."):
                    result = AuthManager.register(
                        username.strip(),
                        email.strip(),
                        password,
                        college.strip(),
                        role,
                    )
                    
                    if result["success"]:
                        st.markdown("""
                        <div style="
                            background: #F0FDF4;
                            border: 1.5px solid #86EFAC;
                            border-radius: 12px;
                            padding: 12px 16px;
                            color: #15803D;
                            font-weight: 500;
                            font-size: 14px;
                            display: flex;
                            align-items: center;
                            gap: 10px;
                            margin-top: 16px;
                        ">
                            <span>✅</span>
                            <span>Account created! Sign in to continue.</span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                    else:
                        st.markdown(f"""
                        <div style="
                            background: #FEF3F2;
                            border: 1.5px solid #FCCAB1;
                            border-radius: 12px;
                            padding: 12px 16px;
                            color: #B42318;
                            font-weight: 500;
                            font-size: 14px;
                            display: flex;
                            align-items: center;
                            gap: 10px;
                            margin-top: 16px;
                        ">
                            <span>❌</span>
                            <span>{result['error']}</span>
                        </div>
                        """, unsafe_allow_html=True)
