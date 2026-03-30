"""
Terra 2.0 — Eco Swipe Game Page
Tinder-style swipe game where users classify habits as eco-friendly or not.
"""

import streamlit as st

from ui.components import page_header, metric_row, score_circle
from modules.swipe_game import EcoSwipeGame
from modules.gamification import GamificationEngine


def show():
    """Render the Eco Swipe Game page."""
    if not st.session_state.get("logged_in"):
        st.warning("Please log in first.")
        st.session_state["page"] = "login"
        st.rerun()
        return

    page_header("Eco Swipe Game", "Swipe right for eco, left for not!", "🃏")

    user_id = st.session_state.get("user_id")

    # Initialize game state
    if "swipe_questions" not in st.session_state or not st.session_state["swipe_questions"]:
        st.session_state["swipe_questions"] = []
    if "swipe_idx" not in st.session_state:
        st.session_state["swipe_idx"] = 0
    if "swipe_score" not in st.session_state:
        st.session_state["swipe_score"] = 0
    if "swipe_answers" not in st.session_state:
        st.session_state["swipe_answers"] = []
    if "swipe_game_over" not in st.session_state:
        st.session_state["swipe_game_over"] = False
    if "swipe_answered" not in st.session_state:
        st.session_state["swipe_answered"] = False

    questions = st.session_state["swipe_questions"]
    idx = st.session_state["swipe_idx"]
    game_over = st.session_state["swipe_game_over"]

    # ═══════ Start Screen ═══════
    if not questions and not game_over:
        st.markdown(f"""
        <div class="terra-card-glow" style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🃏</div>
            <h2 style="color: #F5F0E8; margin: 0;">Ready to Swipe?</h2>
            <p style="color: #7EC8E3; margin-top: 0.5rem;">
                10 habits will appear one by one.<br>
                Swipe <strong style="color: #2ECC71;">ECO ✅</strong> or
                <strong style="color: #EF4444;">NOT ECO ❌</strong>
            </p>
            <p style="color: #F4C430; font-size: 0.85rem; margin-top: 1rem;">
                +10 XP per correct answer • +30 XP for completing!
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎮 Start Game!", use_container_width=True, key="swipe_start"):
            st.session_state["swipe_questions"] = EcoSwipeGame.get_game_questions(10)
            st.session_state["swipe_idx"] = 0
            st.session_state["swipe_score"] = 0
            st.session_state["swipe_answers"] = []
            st.session_state["swipe_game_over"] = False
            st.session_state["swipe_answered"] = False
            st.rerun()
        return

    # ═══════ Game Over Screen ═══════
    if game_over:
        correct = st.session_state["swipe_score"]
        total = len(questions) if questions else 10
        score_data = EcoSwipeGame.calculate_final_score(correct, total)

        st.markdown(f"""
        <div class="terra-card-glow" style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🏁</div>
            <h2 style="color: #F5F0E8; margin: 0;">Game Over!</h2>
            <p style="color: #F4C430; font-size: 1.3rem; font-weight: 700; margin-top: 0.5rem;">
                {score_data['grade']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # Score display
        col_score, col_stats = st.columns([1, 2])

        with col_score:
            score_circle(
                float(correct), float(total),
                "Correct Answers",
                "#2ECC71" if score_data["accuracy"] >= 70 else "#F59E0B"
            )

        with col_stats:
            metric_row([
                {"label": "Accuracy", "value": f"{score_data['accuracy']}%", "emoji": "🎯", "delta": ""},
                {"label": "XP Earned", "value": f"+{score_data['xp_total']}", "emoji": "⭐", "delta": ""},
            ])

        st.markdown("")

        # Answer review
        st.markdown("""
        <h3 style="color: #7EC8E3;">📝 Answer Review</h3>
        """, unsafe_allow_html=True)

        answers = st.session_state.get("swipe_answers", [])
        for i, ans in enumerate(answers, 1):
            icon = "✅" if ans["correct"] else "❌"
            color = "#2ECC71" if ans["correct"] else "#EF4444"
            st.markdown(f"""
            <div class="terra-card" style="padding: 0.8rem 1.2rem; margin-bottom: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 0.8rem;">
                    <span style="font-size: 1.2rem;">{icon}</span>
                    <div>
                        <div style="color: #F5F0E8; font-weight: 600;">
                            {ans['habit']['emoji']} {ans['habit']['habit']}
                        </div>
                        <div style="color: {color}; font-size: 0.8rem;">
                            {'Eco-friendly ✅' if ans['habit']['eco_friendly'] else 'Not eco-friendly ❌'}
                            — {ans['habit']['explanation']}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        if st.button("🔄 Play Again!", use_container_width=True, key="swipe_replay"):
            st.session_state["swipe_questions"] = []
            st.session_state["swipe_idx"] = 0
            st.session_state["swipe_score"] = 0
            st.session_state["swipe_answers"] = []
            st.session_state["swipe_game_over"] = False
            st.session_state["swipe_answered"] = False
            st.rerun()
        return

    # ═══════ Active Game ═══════
    if idx >= len(questions):
        # All questions answered — save and show results
        correct = st.session_state["swipe_score"]
        total = len(questions)
        score_data = EcoSwipeGame.calculate_final_score(correct, total)

        EcoSwipeGame.save_score(user_id, score_data)

        # Award XP for correct answers and game completion
        for _ in range(correct):
            GamificationEngine.award_xp(user_id, "swipe_correct")
        xp_result = GamificationEngine.award_xp(user_id, "swipe_game_complete")

        if xp_result.get("leveled_up"):
            st.toast(f"🎉 Level Up! You're now {xp_result['level_name']}!")

        for badge in xp_result.get("new_badges", []):
            st.toast(f"🏅 New Badge: {badge['name']}")

        st.toast(f"⭐ +{score_data['xp_total'] + 30} total XP earned!")

        st.session_state["swipe_game_over"] = True
        st.rerun()
        return

    current_q = questions[idx]

    # Progress indicator
    progress = (idx) / len(questions)
    st.progress(progress)
    st.markdown(f"""
    <div style="text-align: center; color: #7EC8E3; font-size: 0.85rem; margin-bottom: 1rem;">
        Question {idx + 1} of {len(questions)} • Score: {st.session_state['swipe_score']}/{idx}
    </div>
    """, unsafe_allow_html=True)

    # Habit card
    st.markdown(f"""
    <div class="terra-card-glow" style="text-align: center; padding: 2.5rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">{current_q['emoji']}</div>
        <h2 style="color: #F5F0E8; margin: 0; font-size: 1.5rem;">
            {current_q['habit']}
        </h2>
        <p style="color: #7EC8E3; margin-top: 1rem; font-size: 1rem;">
            Is this eco-friendly? 🌿
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Answer buttons
    if not st.session_state.get("swipe_answered", False):
        col_eco, col_not = st.columns(2)

        with col_eco:
            if st.button("✅ ECO FRIENDLY", use_container_width=True, key=f"swipe_eco_{idx}"):
                result = EcoSwipeGame.check_answer(current_q, True)
                _handle_answer(result, current_q)

        with col_not:
            if st.button("❌ NOT ECO", use_container_width=True, key=f"swipe_not_{idx}"):
                result = EcoSwipeGame.check_answer(current_q, False)
                _handle_answer(result, current_q)
    else:
        # Show feedback for answered question
        last_answer = st.session_state["swipe_answers"][-1] if st.session_state["swipe_answers"] else None
        if last_answer:
            if last_answer["correct"]:
                st.markdown(f"""
                <div class="terra-card" style="text-align: center; padding: 1rem;
                     border-left: 4px solid #2ECC71;">
                    <div style="font-size: 1.5rem;">✅ Correct! +10 XP</div>
                    <div style="color: #F5F0E8; margin-top: 0.5rem;">
                        {current_q['explanation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="terra-card" style="text-align: center; padding: 1rem;
                     border-left: 4px solid #EF4444;">
                    <div style="font-size: 1.5rem;">❌ Incorrect!</div>
                    <div style="color: #F5F0E8; margin-top: 0.5rem;">
                        {current_q['explanation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if st.button("Next Question ➡️", use_container_width=True, key=f"swipe_next_{idx}"):
            st.session_state["swipe_idx"] += 1
            st.session_state["swipe_answered"] = False
            st.rerun()


def _handle_answer(result: dict, question: dict):
    """Process an answer and update state."""
    if result["correct"]:
        st.session_state["swipe_score"] += 1

    st.session_state["swipe_answers"].append({
        "correct": result["correct"],
        "habit": question,
        "xp": result["xp"],
    })
    st.session_state["swipe_answered"] = True
    st.rerun()
