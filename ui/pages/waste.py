"""
Terra 2.0 — Waste Classifier Page
Classify waste items and get disposal instructions.
"""

import streamlit as st
from sqlalchemy import select

from ui.components import page_header, eco_tip_card
from modules.waste_classifier import WasteClassifier
from modules.gamification import GamificationEngine
from database.db_setup import get_engine, get_session, WasteLog


def show():
    """Render the Waste Classifier page."""
    if not st.session_state.get("logged_in"):
        st.warning("Please log in first.")
        st.session_state["page"] = "login"
        st.rerun()
        return

    page_header("Waste Classifier", "Know where your waste belongs!", "♻️")

    user_id = st.session_state.get("user_id")

    # ═══════ Search Input ═══════
    st.markdown("""
    <h3 style="color: #7EC8E3;">🔍 What do you want to dispose?</h3>
    """, unsafe_allow_html=True)

    search_query = st.text_input(
        "Enter waste item name",
        placeholder="e.g., banana peel, old phone, battery...",
        key="waste_search_input"
    )

    # ═══════ Quick Tap Buttons ═══════
    st.markdown("""
    <p style="color: rgba(245, 240, 232, 0.5); font-size: 0.8rem;">
        Quick tap common items:
    </p>
    """, unsafe_allow_html=True)

    quick_items = WasteClassifier.get_quick_items()
    quick_cols = st.columns(min(len(quick_items), 4))

    for i, (col, item) in enumerate(zip(quick_cols * 2, quick_items)):
        col_idx = i % 4
        with st.columns(4)[col_idx]:
            if st.button(
                f"{item['name'][:15]}",
                key=f"waste_quick_{item['name']}",
                use_container_width=True
            ):
                st.session_state["waste_search_input"] = item["name"]
                st.rerun()

    st.markdown("")

    # ═══════ Classification Results ═══════
    if search_query and search_query.strip():
        result = WasteClassifier.classify(search_query.strip())

        if result is None:
            st.markdown("""
            <div class="terra-card" style="text-align: center; padding: 2rem;">
                <div style="font-size: 2rem;">🤔</div>
                <div style="color: #F5F0E8; margin-top: 0.5rem;">
                    Couldn't identify this item. Try a different name!
                </div>
                <div style="color: rgba(245, 240, 232, 0.5); font-size: 0.85rem; margin-top: 0.3rem;">
                    Hint: Use simple names like "plastic bottle" or "banana peel"
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Save log and award XP
            WasteClassifier.save_log(user_id, result["name"], result["category"])
            xp_result = GamificationEngine.award_xp(user_id, "waste_classified")

            if xp_result.get("xp_earned", 0) > 0:
                st.toast(f"⭐ +{xp_result['xp_earned']} XP for classifying waste!")

            for badge in xp_result.get("new_badges", []):
                st.toast(f"🏅 New Badge: {badge['name']}")

            # ═══════ Result Card ═══════
            color = result.get("color", "#6B7280")

            st.markdown(f"""
            <div class="terra-card-glow" style="padding: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <div style="
                        background: {color};
                        width: 60px; height: 60px;
                        border-radius: 16px;
                        display: flex; align-items: center; justify-content: center;
                        font-size: 1.5rem;
                    ">♻️</div>
                    <div>
                        <h3 style="color: #F5F0E8; margin: 0; text-transform: capitalize;">
                            {result['name']}
                        </h3>
                        <div style="color: {color}; font-weight: 600; font-size: 1rem;">
                            {result['category']}
                        </div>
                    </div>
                </div>

                <div style="
                    background: {color}22;
                    border: 1px solid {color}44;
                    border-radius: 12px;
                    padding: 1rem;
                    text-align: center;
                    margin-bottom: 1rem;
                ">
                    <div style="color: #F5F0E8; font-size: 0.85rem;">Dispose in</div>
                    <div style="color: {color}; font-size: 1.5rem; font-weight: 700;">
                        🗑️ {result['bin']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ═══════ Disposal Instructions ═══════
            instructions = result.get("instructions", [])
            if instructions:
                st.markdown("""
                <h4 style="color: #2ECC71; margin-top: 1rem;">📋 Disposal Instructions</h4>
                """, unsafe_allow_html=True)

                for i, instruction in enumerate(instructions, 1):
                    st.markdown(f"""
                    <div class="terra-card" style="
                        padding: 0.8rem 1.2rem;
                        margin-bottom: 0.4rem;
                        border-left: 3px solid {color};
                    ">
                        <span style="color: {color}; font-weight: 700; margin-right: 0.5rem;">
                            {i}.
                        </span>
                        <span style="color: #F5F0E8;">{instruction}</span>
                    </div>
                    """, unsafe_allow_html=True)

            # ═══════ Do NOT Mix Warning ═══════
            do_not_mix = result.get("do_not_mix", [])
            if do_not_mix:
                mix_items = " • ".join([f"🚫 {item}" for item in do_not_mix])
                st.markdown(f"""
                <div style="
                    background: rgba(239, 68, 68, 0.15);
                    border: 1px solid rgba(239, 68, 68, 0.4);
                    border-radius: 12px;
                    padding: 1rem;
                    margin-top: 1rem;
                ">
                    <div style="color: #EF4444; font-weight: 700; margin-bottom: 0.3rem;">
                        ⚠️ Do NOT Mix With
                    </div>
                    <div style="color: #F5F0E8; font-size: 0.9rem;">
                        {mix_items}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ═══════ Additional Info ═══════
            col_time, col_fact = st.columns(2)

            with col_time:
                st.markdown(f"""
                <div class="terra-card" style="text-align: center; padding: 1rem; margin-top: 1rem;">
                    <div style="color: #7EC8E3; font-size: 0.85rem;">⏱️ Decomposition Time</div>
                    <div style="color: #F4C430; font-size: 1.2rem; font-weight: 700; margin-top: 0.3rem;">
                        {result.get('decompose_time', 'Unknown')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_fact:
                st.markdown(f"""
                <div class="terra-card" style="text-align: center; padding: 1rem; margin-top: 1rem;">
                    <div style="color: #7EC8E3; font-size: 0.85rem;">🎉 Fun Fact</div>
                    <div style="color: #F5F0E8; font-size: 0.85rem; margin-top: 0.3rem;">
                        {result.get('fun_fact', 'No fact available')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # ═══════ My Waste Log ═══════
    st.markdown("""
    <h3 style="color: #7EC8E3;">📋 My Waste Classification Log</h3>
    """, unsafe_allow_html=True)

    engine = get_engine()
    with get_session(engine) as session:
        logs = session.execute(
            select(WasteLog)
            .where(WasteLog.user_id == user_id)
            .order_by(WasteLog.logged_at.desc())
            .limit(20)
        ).scalars().all()

        if logs:
            for log in logs:
                cat_color = WasteClassifier.CATEGORY_COLORS.get(
                    log.category, "#6B7280"
                )
                st.markdown(f"""
                <div style="
                    background: rgba(45, 74, 62, 0.3);
                    border-left: 3px solid {cat_color};
                    border-radius: 8px;
                    padding: 0.5rem 1rem;
                    margin-bottom: 0.3rem;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">
                    <span style="color: #F5F0E8; text-transform: capitalize;">
                        {log.item_name}
                    </span>
                    <span style="color: {cat_color}; font-size: 0.8rem;">
                        {log.category}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="terra-card" style="text-align: center; padding: 1.5rem;
                 color: rgba(245, 240, 232, 0.5);">
                No waste items classified yet. Start searching above! ♻️
            </div>
            """, unsafe_allow_html=True)
