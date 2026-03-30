"""
Terra 2.0 — AI Roast My Lifestyle Page
Users select their habits, then get roasted by AI in Gen Z slang.
"""

import streamlit as st

from ui.components import page_header, render_terra_card
from modules.ai_roast import AIRoaster
from modules.gamification import GamificationEngine


def show():
    """Render the AI Roast page."""
    if not st.session_state.get("logged_in"):
        st.warning("Please log in first.")
        st.session_state["page"] = "login"
        st.rerun()
        return

    page_header("AI Roast My Lifestyle", "Get savage (but helpful) eco feedback", "🔥")

    user_id = st.session_state.get("user_id")
    roaster = AIRoaster()

    # ═══════ Habit Selection ═══════
    st.markdown("""
    <h3 style="color: #7EC8E3;">🗂️ Select Your Habits</h3>
    <p style="color: rgba(245, 240, 232, 0.6);">Be honest — the AI can sense cap 💀</p>
    """, unsafe_allow_html=True)

    habits = {}

    col1, col2 = st.columns(2)

    with col1:
        if st.checkbox("🚗 I drive alone to college", key="roast_drive"):
            habits["Transport"] = "Drives alone daily"

        if st.checkbox("🥩 I eat meat at every meal", key="roast_meat"):
            habits["Diet"] = "Heavy meat eater"

        if st.checkbox("❄️ I blast AC at 18°C", key="roast_ac"):
            habits["Energy"] = "AC at 18°C all day"

        if st.checkbox("🧴 I buy single-use plastic bottles", key="roast_plastic"):
            habits["Plastic use"] = "Buys single-use plastic daily"

    with col2:
        if st.checkbox("👗 I buy fast fashion weekly", key="roast_fashion"):
            habits["Fashion"] = "Fast fashion every week"

        if st.checkbox("🚿 My showers are 30+ minutes", key="roast_shower"):
            habits["Water"] = "30-min showers daily"

        if st.checkbox("📱 I get a new phone every year", key="roast_phone"):
            habits["E-waste"] = "New phone every year"

        if st.checkbox("🍕 I order food delivery daily", key="roast_delivery"):
            habits["Food delivery"] = "Daily delivery orders"

    st.markdown("")

    # ═══════ Severity Slider ═══════
    severity = st.slider(
        "🔥 Roast intensity",
        min_value=1, max_value=5, value=3,
        help="1 = Gentle nudge, 5 = Full savage mode",
        key="roast_severity"
    )

    severity_labels = {1: "Mild 😊", 2: "Warm 🙂", 3: "Spicy 🌶️",
                       4: "Hot 🔥", 5: "SAVAGE 💀"}
    st.markdown(f"""
    <div style="text-align: center; color: #F4C430; font-size: 0.9rem;">
        Intensity: {severity_labels.get(severity, "Spicy")}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # ═══════ Roast Button ═══════
    if st.button("🔥 ROAST ME!", use_container_width=True, key="roast_button"):
        if not habits:
            st.warning("Select at least one habit to get roasted! No cap.")
        else:
            habits["Intensity"] = f"Level {severity}/5"

            with st.spinner("🤖 AI is cooking your roast... 🍳"):
                roast_text = roaster.roast_lifestyle(habits)

            # Display roast
            st.markdown(f"""
            <div class="terra-card-glow" style="padding: 1.5rem;">
                <div style="font-size: 1.2rem; font-weight: 600; color: #FF6B35; margin-bottom: 0.8rem;">
                    🔥 Your Eco Roast
                </div>
                <div style="color: #F5F0E8; line-height: 1.8; font-size: 0.95rem;">
                    {roast_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Award XP
            xp_result = GamificationEngine.award_xp(user_id, "roast_received")

            # Award roast badge
            from modules.gamification import GamificationEngine as GE
            GE.award_specific_badge(user_id, "first_roast")

            if xp_result.get("leveled_up"):
                st.toast(f"🎉 Level Up! You're now {xp_result['level_name']}!")
            else:
                st.toast(f"⭐ +{xp_result['xp_earned']} XP for surviving the roast!")

            for badge in xp_result.get("new_badges", []):
                st.toast(f"🏅 New Badge: {badge['name']}")

            st.markdown("")

            # Share button
            st.markdown("""
            <h4 style="color: #7EC8E3;">📤 Share Your Roast</h4>
            """, unsafe_allow_html=True)
            st.code(roast_text, language=None)
            st.caption("Copy the text above and share with friends! 😂")

    st.markdown("---")

    # ═══════ Eco Advice Section ═══════
    st.markdown("""
    <h3 style="color: #2ECC71;">🌿 Ask Eco Advice</h3>
    <p style="color: rgba(245, 240, 232, 0.6);">Got a sustainability question? Ask away!</p>
    """, unsafe_allow_html=True)

    eco_question = st.text_input(
        "Your eco question",
        placeholder="e.g., How can I reduce my water usage?",
        key="roast_eco_question"
    )

    if st.button("🌱 Get Advice", key="roast_advice_btn"):
        if eco_question.strip():
            with st.spinner("🤔 Thinking..."):
                advice = roaster.eco_advice(eco_question)

            st.markdown(f"""
            <div class="terra-card" style="padding: 1.5rem;">
                <div style="font-size: 1rem; font-weight: 600; color: #2ECC71; margin-bottom: 0.5rem;">
                    🌿 Eco Advice
                </div>
                <div style="color: #F5F0E8; line-height: 1.7; font-size: 0.95rem;">
                    {advice}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Please enter a question first!")
