"""
Terra 2.0 — Home Dashboard Page
Displays welcome hero, live AQI, quick stats, navigation grid,
recent activity, and eco tip of the day.
"""

import streamlit as st
from datetime import datetime

from ui.components import page_header, metric_row, eco_tip_card, render_terra_card
from api.climate_api import ClimateAPI
from modules.auth import AuthManager
from modules.gamification import GamificationEngine
from modules.carbon_tracker import CarbonTracker
from modules.leaderboard import CollegeLeaderboard
from config import DEFAULT_LAT, DEFAULT_LON, DEFAULT_CITY

# Eco tips pool — rotates by day of year
ECO_TIPS = [
    "Turn off lights when you leave a room — saves 44 kWh/year per bulb!",
    "A 5-minute shower uses 45L less water than a 15-minute one.",
    "Choosing the bus over a car saves 6x less CO2 per trip.",
    "Eating one plant-based meal a day saves 2.5 kg CO2 daily.",
    "Unplugging chargers when not in use saves ~100 kWh/year per device.",
    "Thrift shopping saves 82% of the water used to make new clothing.",
    "Composting food waste diverts methane from landfills (28x more potent than CO2).",
    "Using a reusable bottle saves ~156 plastic bottles per year.",
    "Setting your AC to 24°C instead of 18°C uses 3x less energy.",
    "Carpooling with 3 friends reduces your commute emissions by 75%.",
    "LED bulbs use 75% less energy and last 25x longer than incandescent.",
    "One tree absorbs approximately 22 kg of CO2 per year.",
    "Buying local produce cuts food transport emissions by up to 50%.",
    "A single recycled plastic bottle saves enough energy to power a 60W bulb for 6 hours.",
    "Carrying cloth bags replaces ~700 plastic bags in their lifetime.",
    "Cycling or walking for short trips = zero emissions + better health!",
    "Fixing broken items instead of replacing reduces manufacturing waste.",
    "Bar soap uses 5x less packaging and energy than liquid soap.",
    "Growing your own vegetables means zero food miles and zero packaging!",
    "Choosing stairs over elevator saves 2-5% of building energy use.",
    "4K streaming uses 7x more energy than HD — switch when possible.",
    "Rainwater harvesting can meet 100% of household needs in monsoon.",
    "One pair of jeans requires 7,600 litres of water to produce.",
    "Recycling aluminium uses 95% less energy than making it from scratch.",
    "Donating old clothes extends garment life by 2 years = 24% less CO2.",
    "Coffee grounds repel slugs and add nitrogen to soil — great for gardens!",
    "Used cooking oil can be converted into biodiesel that powers vehicles.",
    "Glass can be recycled indefinitely without losing quality!",
    "A safety razor lasts a lifetime — only replace the recyclable metal blades.",
    "Oat milk produces 80% less CO2 than cow's milk.",
    "Wool dryer balls reduce drying time by 25-50% and last 1000+ loads.",
]


def show():
    """Render the home dashboard page."""
    if not st.session_state.get("logged_in"):
        st.warning("Please log in first.")
        st.session_state["page"] = "login"
        st.rerun()
        return

    user_id = st.session_state.get("user_id")
    username = st.session_state.get("username", "Explorer")
    college = st.session_state.get("college", "")

    # Refresh user data
    user_data = AuthManager.get_user(user_id)
    if user_data:
        st.session_state["xp"] = user_data["xp"]
        st.session_state["level"] = user_data["level"]

    xp = st.session_state.get("xp", 0)
    level = st.session_state.get("level", 1)
    level_info = GamificationEngine.calculate_level(xp)

    # ═══════ Welcome Hero ═══════
    st.markdown(f"""
    <div class="terra-card-glow" style="text-align: center; padding: 2rem;">
        <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🌍</div>
        <h1 style="
            font-size: 2rem;
            margin: 0;
            background: linear-gradient(135deg, #2ECC71, #7EC8E3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">Welcome back, {username}! 👋</h1>
        <p style="color: #7EC8E3; margin-top: 0.5rem; font-size: 1.1rem;">
            Level {level} — {level_info['name']} • {xp} XP
        </p>
        <p style="color: rgba(245, 240, 232, 0.6); font-size: 0.85rem; margin-top: 0.3rem;">
            Your planet needs a glow-up. Start here. 🌱
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # ═══════ Live AQI & Weather Widget ═══════
    col_aqi, col_weather = st.columns(2)

    with col_aqi:
        try:
            aqi_data = ClimateAPI.get_aqi(DEFAULT_LAT, DEFAULT_LON)
            st.markdown(f"""
            <div class="terra-card" style="text-align: center;">
                <div style="font-size: 0.8rem; color: #7EC8E3; margin-bottom: 0.3rem;">
                    🏙️ Air Quality — {DEFAULT_CITY}
                </div>
                <div style="font-size: 2.5rem; font-weight: 700; color: {aqi_data['color']};">
                    {aqi_data['emoji']} {aqi_data['aqi']}
                </div>
                <div style="color: {aqi_data['color']}; font-weight: 600; font-size: 1rem;">
                    {aqi_data['category']}
                </div>
                <div style="color: rgba(245, 240, 232, 0.6); font-size: 0.75rem; margin-top: 0.3rem;">
                    PM2.5: {aqi_data['pm2_5']} µg/m³ • PM10: {aqi_data['pm10']} µg/m³
                </div>
            </div>
            """, unsafe_allow_html=True)
        except (ValueError, KeyError):
            st.markdown("""
            <div class="terra-card" style="text-align: center;">
                <div style="color: #7EC8E3;">🏙️ AQI data unavailable</div>
            </div>
            """, unsafe_allow_html=True)

    with col_weather:
        try:
            weather_data = ClimateAPI.get_weather(DEFAULT_LAT, DEFAULT_LON)
            st.markdown(f"""
            <div class="terra-card" style="text-align: center;">
                <div style="font-size: 0.8rem; color: #7EC8E3; margin-bottom: 0.3rem;">
                    🌡️ Weather — {DEFAULT_CITY}
                </div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #F4C430;">
                    {weather_data['emoji']} {weather_data['temperature']}°C
                </div>
                <div style="color: #F5F0E8; font-weight: 600; font-size: 1rem;">
                    {weather_data['description']}
                </div>
                <div style="color: rgba(245, 240, 232, 0.6); font-size: 0.75rem; margin-top: 0.3rem;">
                    💧 {weather_data['humidity']}% humidity • 💨 {weather_data['wind_speed']} km/h
                </div>
            </div>
            """, unsafe_allow_html=True)
        except (ValueError, KeyError):
            st.markdown("""
            <div class="terra-card" style="text-align: center;">
                <div style="color: #7EC8E3;">🌡️ Weather data unavailable</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")

    # ═══════ Quick Stats ═══════
    # Get today's footprint
    history = CarbonTracker.get_history(user_id)
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_fp = 0.0
    if not history.empty and "date" in history.columns:
        today_data = history[history["date"] == today_str]
        if not today_data.empty:
            today_fp = today_data["total_kg"].iloc[0]

    # Get streak
    streak = st.session_state.get("streak", 0)
    if user_data:
        streak = user_data.get("streak", 0)

    # College rank
    college_rank = CollegeLeaderboard.get_user_college_rank(college) if college else 0
    rank_display = f"#{college_rank}" if college_rank > 0 else "—"

    metric_row([
        {"label": "Today's Footprint", "value": f"{today_fp:.1f} kg", "emoji": "🌿", "delta": ""},
        {"label": "Current Level", "value": f"Lv.{level}", "emoji": "⭐", "delta": level_info["name"]},
        {"label": "College Rank", "value": rank_display, "emoji": "🏆", "delta": college or ""},
        {"label": "Login Streak", "value": f"{streak} days", "emoji": "🔥", "delta": ""},
    ])

    st.markdown("")

    # ═══════ Navigation Grid ═══════
    st.markdown("""
    <h3 style="text-align: center; color: #7EC8E3; margin-bottom: 1rem;">
        🧭 Explore Terra 2.0
    </h3>
    """, unsafe_allow_html=True)

    nav_items = [
        ("🌿", "Carbon Tracker", "carbon", "Track your daily footprint"),
        ("🔥", "AI Roast", "roast", "Get roasted by AI"),
        ("🃏", "Eco Swipe", "swipe", "Swipe left or right"),
        ("🏆", "Leaderboard", "leaderboard", "College vs College"),
        ("😂", "Meme Factory", "meme", "Create eco memes"),
        ("📦", "Eco Score", "eco_score", "Rate any product"),
        ("♻️", "Waste Classifier", "waste", "Where does it go?"),
        ("👤", "My Profile", "profile", "View your journey"),
    ]

    # 4 columns x 2 rows
    for row_start in range(0, len(nav_items), 4):
        cols = st.columns(4)
        for i, col in enumerate(cols):
            idx = row_start + i
            if idx < len(nav_items):
                emoji, label, page_key, desc = nav_items[idx]
                with col:
                    if st.button(f"{emoji} {label}", key=f"home_nav_{page_key}",
                                 use_container_width=True):
                        st.session_state["page"] = page_key
                        st.rerun()
                    st.markdown(f"""
                    <p style="text-align: center; color: rgba(245, 240, 232, 0.5);
                              font-size: 0.7rem; margin-top: -0.5rem;">
                        {desc}
                    </p>
                    """, unsafe_allow_html=True)

    st.markdown("")

    # ═══════ Eco Tip of the Day ═══════
    day_of_year = datetime.now().timetuple().tm_yday
    tip_idx = day_of_year % len(ECO_TIPS)
    st.markdown("""
    <h3 style="color: #2ECC71; margin-bottom: 0.5rem;">🌿 Eco Tip of the Day</h3>
    """, unsafe_allow_html=True)
    eco_tip_card(ECO_TIPS[tip_idx])

    st.markdown("")

    # ═══════ Recent Activity Feed ═══════
    st.markdown("""
    <h3 style="color: #7EC8E3; margin-bottom: 0.5rem;">📰 Recent Activity</h3>
    """, unsafe_allow_html=True)

    activities = []

    # Recent footprints
    if not history.empty:
        for _, row in history.head(3).iterrows():
            activities.append(
                f"🌿 Logged footprint: <strong>{row['total_kg']:.1f} kg CO2</strong> on {row['date']}"
            )

    # Recent badges
    badges = GamificationEngine.get_user_badges(user_id)
    for badge in badges[-3:]:
        activities.append(
            f"🏅 Earned badge: <strong>{badge['name']}</strong>"
        )

    if activities:
        for activity in activities[:5]:
            st.markdown(f"""
            <div class="terra-card" style="padding: 0.8rem 1.2rem; margin-bottom: 0.5rem;">
                <span style="color: #F5F0E8; font-size: 0.85rem;">{activity}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="terra-card" style="text-align: center; padding: 1.5rem; color: rgba(245,240,232,0.5);">
            <p>No recent activity yet. Start exploring! 🚀</p>
        </div>
        """, unsafe_allow_html=True)
