"""
Terra 2.0 — Carbon Footprint Tracker Page
4-step wizard: Transport → Food → Energy → Shopping → Results
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from ui.components import page_header, score_circle, eco_tip_card, metric_row
from modules.carbon_tracker import CarbonTracker
from modules.gamification import GamificationEngine
from config import TRANSPORT_FACTORS, FOOD_FACTORS, SHOPPING_FACTORS


def show():
    """Render the Carbon Footprint Tracker page."""
    if not st.session_state.get("logged_in"):
        st.warning("Please log in first.")
        st.session_state["page"] = "login"
        st.rerun()
        return

    page_header("Carbon Footprint Tracker", "Measure your daily impact on the planet", "🌿")

    user_id = st.session_state.get("user_id")

    # Initialize carbon wizard state
    if "carbon_step" not in st.session_state:
        st.session_state["carbon_step"] = 1
    if "carbon_data" not in st.session_state:
        st.session_state["carbon_data"] = {}

    step = st.session_state["carbon_step"]

    # Progress indicator
    steps = ["🚗 Transport", "🍽️ Food", "⚡ Energy", "🛍️ Shopping", "📊 Results"]
    cols = st.columns(len(steps))
    for i, (col, step_name) in enumerate(zip(cols, steps), 1):
        with col:
            if i < step:
                color = "#2ECC71"
                icon = "✅"
            elif i == step:
                color = "#F4C430"
                icon = "🔵"
            else:
                color = "rgba(245, 240, 232, 0.3)"
                icon = "⚪"
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 1.2rem;">{icon}</div>
                <div style="font-size: 0.7rem; color: {color};">{step_name}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ═══════ Step 1: Transport ═══════
    if step == 1:
        st.markdown("""
        <h3 style="color: #7EC8E3;">🚗 Step 1: Transport</h3>
        <p style="color: rgba(245, 240, 232, 0.7);">How did you travel today?</p>
        """, unsafe_allow_html=True)

        transport_modes = st.multiselect(
            "Select transport modes used today",
            options=list(TRANSPORT_FACTORS.keys()),
            default=["Bus"],
            key="carbon_transport_modes"
        )

        transport_total = 0.0
        transport_details = {}

        for mode in transport_modes:
            km = st.slider(
                f"Distance by {mode} (km)",
                min_value=0.0, max_value=200.0, value=10.0, step=0.5,
                key=f"carbon_km_{mode}"
            )
            emission = CarbonTracker.calculate_transport(mode, km)
            transport_details[mode] = {"km": km, "emission": emission}
            transport_total += emission

        st.markdown(f"""
        <div class="terra-card" style="text-align: center; padding: 1rem;">
            <div style="color: #7EC8E3; font-size: 0.85rem;">Transport Total</div>
            <div style="color: #F5F0E8; font-size: 1.8rem; font-weight: 700;">
                {transport_total:.2f} kg CO2
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Next → Food 🍽️", key="carbon_next_1"):
            st.session_state["carbon_data"]["transport_kg"] = transport_total
            st.session_state["carbon_data"]["transport_details"] = transport_details
            st.session_state["carbon_step"] = 2
            st.rerun()

    # ═══════ Step 2: Food ═══════
    elif step == 2:
        st.markdown("""
        <h3 style="color: #7EC8E3;">🍽️ Step 2: Food</h3>
        <p style="color: rgba(245, 240, 232, 0.7);">What's your diet like?</p>
        """, unsafe_allow_html=True)

        diet_type = st.radio(
            "Your diet type",
            options=list(FOOD_FACTORS.keys()),
            index=2,  # Default to Vegetarian
            key="carbon_diet"
        )

        meals = st.number_input(
            "Number of meals today",
            min_value=1, max_value=6, value=3,
            key="carbon_meals"
        )

        food_total = CarbonTracker.calculate_food(diet_type, meals)

        st.markdown(f"""
        <div class="terra-card" style="text-align: center; padding: 1rem;">
            <div style="color: #7EC8E3; font-size: 0.85rem;">Food Total</div>
            <div style="color: #F5F0E8; font-size: 1.8rem; font-weight: 700;">
                {food_total:.2f} kg CO2
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("← Back", key="carbon_back_2"):
                st.session_state["carbon_step"] = 1
                st.rerun()
        with col_next:
            if st.button("Next → Energy ⚡", key="carbon_next_2"):
                st.session_state["carbon_data"]["food_kg"] = food_total
                st.session_state["carbon_data"]["diet_type"] = diet_type
                st.session_state["carbon_step"] = 3
                st.rerun()

    # ═══════ Step 3: Energy ═══════
    elif step == 3:
        st.markdown("""
        <h3 style="color: #7EC8E3;">⚡ Step 3: Energy</h3>
        <p style="color: rgba(245, 240, 232, 0.7);">Your electricity usage today</p>
        """, unsafe_allow_html=True)

        ac_hours = st.slider(
            "AC usage (hours today)", 0.0, 24.0, 2.0, 0.5,
            key="carbon_ac"
        )
        fan_hours = st.slider(
            "Fan usage (hours today)", 0.0, 24.0, 8.0, 0.5,
            key="carbon_fan"
        )
        light_hours = st.slider(
            "Lighting (hours today)", 0.0, 24.0, 6.0, 0.5,
            key="carbon_light"
        )
        other_kwh = st.number_input(
            "Other appliances (kWh estimate)",
            min_value=0.0, max_value=50.0, value=1.0, step=0.5,
            key="carbon_other"
        )

        # Rough kWh estimates
        ac_kwh = ac_hours * 1.5  # Average AC
        fan_kwh = fan_hours * 0.075  # Average fan
        light_kwh = light_hours * 0.01 * 5  # 5 LEDs average
        total_kwh = ac_kwh + fan_kwh + light_kwh + other_kwh

        energy_total = CarbonTracker.calculate_energy(total_kwh)

        st.markdown(f"""
        <div class="terra-card" style="text-align: center; padding: 1rem;">
            <div style="color: #7EC8E3; font-size: 0.85rem;">
                Energy Total ({total_kwh:.1f} kWh)
            </div>
            <div style="color: #F5F0E8; font-size: 1.8rem; font-weight: 700;">
                {energy_total:.2f} kg CO2
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("← Back", key="carbon_back_3"):
                st.session_state["carbon_step"] = 2
                st.rerun()
        with col_next:
            if st.button("Next → Shopping 🛍️", key="carbon_next_3"):
                st.session_state["carbon_data"]["energy_kg"] = energy_total
                st.session_state["carbon_step"] = 4
                st.rerun()

    # ═══════ Step 4: Shopping ═══════
    elif step == 4:
        st.markdown("""
        <h3 style="color: #7EC8E3;">🛍️ Step 4: Shopping</h3>
        <p style="color: rgba(245, 240, 232, 0.7);">Any purchases today?</p>
        """, unsafe_allow_html=True)

        shopping_items = {}
        for item_name in SHOPPING_FACTORS:
            qty = st.number_input(
                f"{item_name} (quantity)",
                min_value=0, max_value=20, value=0,
                key=f"carbon_shop_{item_name}"
            )
            if qty > 0:
                shopping_items[item_name] = qty

        shopping_total = CarbonTracker.calculate_shopping(shopping_items)

        st.markdown(f"""
        <div class="terra-card" style="text-align: center; padding: 1rem;">
            <div style="color: #7EC8E3; font-size: 0.85rem;">Shopping Total</div>
            <div style="color: #F5F0E8; font-size: 1.8rem; font-weight: 700;">
                {shopping_total:.2f} kg CO2
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("← Back", key="carbon_back_4"):
                st.session_state["carbon_step"] = 3
                st.rerun()
        with col_next:
            if st.button("Calculate My Footprint 📊", key="carbon_calculate"):
                st.session_state["carbon_data"]["shopping_kg"] = shopping_total

                # Calculate totals
                results = CarbonTracker.get_total(
                    st.session_state["carbon_data"].get("transport_kg", 0),
                    st.session_state["carbon_data"].get("food_kg", 0),
                    st.session_state["carbon_data"].get("energy_kg", 0),
                    shopping_total,
                )
                st.session_state["carbon_data"]["results"] = results

                # Save to database
                CarbonTracker.save_log(user_id, results)

                # Award XP
                xp_result = GamificationEngine.award_xp(user_id, "footprint_logged")
                st.session_state["xp"] = xp_result.get("xp_earned", 0) + st.session_state.get("xp", 0)

                if xp_result.get("leveled_up"):
                    st.toast(f"🎉 Level Up! You're now {xp_result['level_name']}!")
                else:
                    st.toast(f"⭐ +{xp_result['xp_earned']} XP for logging your footprint!")

                for badge in xp_result.get("new_badges", []):
                    st.toast(f"🏅 New Badge: {badge['name']}")

                st.session_state["carbon_step"] = 5
                st.rerun()

    # ═══════ Step 5: Results ═══════
    elif step == 5:
        results = st.session_state.get("carbon_data", {}).get("results", {})

        if not results:
            st.warning("No results found. Please complete the tracker first.")
            if st.button("Start Over 🔄"):
                st.session_state["carbon_step"] = 1
                st.session_state["carbon_data"] = {}
                st.rerun()
            return

        st.markdown("""
        <h3 style="color: #2ECC71; text-align: center;">📊 Your Carbon Footprint Results</h3>
        """, unsafe_allow_html=True)

        # Score circle
        col_score, col_info = st.columns([1, 2])

        with col_score:
            score_circle(
                results["total_kg"], 15.0,
                "Daily CO2 (kg)",
                results["rating_color"]
            )

        with col_info:
            st.markdown(f"""
            <div class="terra-card-glow" style="padding: 1.2rem;">
                <div style="font-size: 1.5rem; font-weight: 700; color: {results['rating_color']};">
                    {results['rating_emoji']} {results['rating']} Impact
                </div>
                <div style="color: #F5F0E8; margin-top: 0.5rem; font-size: 0.9rem;">
                    {results['comparison_text']}
                </div>
                <div style="color: #7EC8E3; margin-top: 0.3rem; font-size: 0.85rem;">
                    🇮🇳 India average: {results['india_avg']} kg CO2/day
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        # Category breakdown metrics
        metric_row([
            {"label": "Transport", "value": f"{results['transport_kg']:.2f} kg", "emoji": "🚗", "delta": ""},
            {"label": "Food", "value": f"{results['food_kg']:.2f} kg", "emoji": "🍽️", "delta": ""},
            {"label": "Energy", "value": f"{results['energy_kg']:.2f} kg", "emoji": "⚡", "delta": ""},
            {"label": "Shopping", "value": f"{results['shopping_kg']:.2f} kg", "emoji": "🛍️", "delta": ""},
        ])

        st.markdown("")

        # Donut chart
        col_donut, col_trend = st.columns(2)

        with col_donut:
            fig_donut = go.Figure(data=[go.Pie(
                labels=["Transport", "Food", "Energy", "Shopping"],
                values=[
                    results["transport_kg"],
                    results["food_kg"],
                    results["energy_kg"],
                    results["shopping_kg"],
                ],
                hole=0.6,
                marker=dict(
                    colors=["#7EC8E3", "#2ECC71", "#F4C430", "#FF6B35"]
                ),
                textinfo="percent+label",
                textfont=dict(size=12, color="#F5F0E8"),
            )])
            fig_donut.update_layout(
                title=dict(text="Emissions Breakdown", font=dict(color="#F5F0E8", size=16)),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#F5F0E8"),
                showlegend=False,
                height=350,
                margin=dict(t=40, b=20, l=20, r=20),
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        with col_trend:
            # Historical trend
            history = CarbonTracker.get_history(user_id)
            if not history.empty and len(history) > 1:
                fig_trend = px.line(
                    history.sort_values("date"),
                    x="date", y="total_kg",
                    title="Your Footprint Trend",
                    labels={"date": "Date", "total_kg": "CO2 (kg)"},
                    markers=True,
                )
                fig_trend.update_traces(
                    line=dict(color="#2ECC71", width=3),
                    marker=dict(size=8),
                )
                fig_trend.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#F5F0E8"),
                    xaxis=dict(gridcolor="rgba(46,204,113,0.1)"),
                    yaxis=dict(gridcolor="rgba(46,204,113,0.1)"),
                    height=350,
                    margin=dict(t=40, b=20, l=20, r=20),
                    title=dict(font=dict(color="#F5F0E8", size=16)),
                )
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                st.markdown("""
                <div class="terra-card" style="text-align: center; padding: 2rem;">
                    <div style="color: #7EC8E3;">📈 Track more days to see your trend!</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")

        # Tips
        tips = CarbonTracker.generate_tips(results)
        st.markdown("""
        <h3 style="color: #2ECC71;">💡 Personalised Tips</h3>
        """, unsafe_allow_html=True)
        for tip in tips:
            eco_tip_card(tip)

        st.markdown("")

        # PDF Download
        col_pdf, col_reset = st.columns(2)
        with col_pdf:
            username = st.session_state.get("username", "user")
            try:
                path = CarbonTracker.generate_pdf_report(username, results)
                with open(path, "rb") as f:
                    st.download_button(
                        "📄 Download PDF Report",
                        f,
                        file_name=f"terra_report_{username}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
            except (OSError, IOError) as e:
                st.error(f"Could not generate PDF: {e}")

        with col_reset:
            if st.button("🔄 Track Another Day", use_container_width=True):
                st.session_state["carbon_step"] = 1
                st.session_state["carbon_data"] = {}
                st.rerun()
