"""
Terra 2.0 — Meme Factory Page
Create and download eco-themed memes using PIL templates.
"""

import streamlit as st

from ui.components import page_header
from modules.meme_generator import EcoMemeGenerator
from modules.gamification import GamificationEngine


def show():
    """Render the Meme Factory page."""
    if not st.session_state.get("logged_in"):
        st.warning("Please log in first.")
        st.session_state["page"] = "login"
        st.rerun()
        return

    page_header("Meme Factory", "Create viral eco memes and share the message!", "😂")

    user_id = st.session_state.get("user_id")

    # ═══════ Template Selection ═══════
    st.markdown("""
    <h3 style="color: #7EC8E3;">🎨 Choose a Template</h3>
    """, unsafe_allow_html=True)

    template_options = {
        "drake": "🔥 Drake Pointing (Approve/Disapprove)",
        "distracted": "👀 Distracted Boyfriend",
        "this_is_fine": "☕ This Is Fine",
        "change_my_mind": "🪧 Change My Mind",
        "always_has_been": "🧑‍🚀 Always Has Been",
        "brain_size": "🧠 Expanding Brain (4 panels)",
    }

    selected_template = st.radio(
        "Template",
        options=list(template_options.keys()),
        format_func=lambda x: template_options[x],
        key="meme_template",
        horizontal=True,
    )

    st.markdown("")

    # ═══════ Caption Suggestions ═══════
    captions = EcoMemeGenerator.ECO_CAPTIONS.get(selected_template, [])

    if captions:
        st.markdown("""
        <h4 style="color: #F4C430;">💡 Suggestion Chips</h4>
        """, unsafe_allow_html=True)

        suggestion_cols = st.columns(min(len(captions), 3))
        for i, (col, cap) in enumerate(zip(suggestion_cols, captions[:3])):
            with col:
                if isinstance(cap, tuple) and len(cap) >= 2:
                    label = f"{cap[0][:25]}..." if len(cap[0]) > 25 else cap[0]
                    if st.button(f"💡 {label}", key=f"meme_suggestion_{i}",
                                 use_container_width=True):
                        st.session_state["meme_top_text"] = cap[0]
                        if len(cap) > 1:
                            st.session_state["meme_bottom_text"] = cap[1]
                        st.rerun()

    st.markdown("")

    # ═══════ Text Inputs ═══════
    if selected_template == "brain_size":
        st.markdown("""
        <p style="color: #7EC8E3; font-size: 0.85rem;">
            For Expanding Brain, enter 4 items separated by commas
        </p>
        """, unsafe_allow_html=True)
        top_text = st.text_input(
            "Panel texts (comma-separated)",
            value=st.session_state.get("meme_top_text", ""),
            placeholder="e.g., Using plastic bags, Reusable bags, Growing own veggies, Zero-waste",
            key="meme_top_input"
        )
        bottom_text = ""
    elif selected_template in ["this_is_fine", "change_my_mind"]:
        top_text = st.text_input(
            "Main text",
            value=st.session_state.get("meme_top_text", ""),
            placeholder="Enter your meme text...",
            key="meme_top_input"
        )
        bottom_text = ""
    else:
        top_text = st.text_input(
            "Top text / Panel 1",
            value=st.session_state.get("meme_top_text", ""),
            placeholder="Enter top text...",
            key="meme_top_input"
        )
        bottom_text = st.text_input(
            "Bottom text / Panel 2",
            value=st.session_state.get("meme_bottom_text", ""),
            placeholder="Enter bottom text...",
            key="meme_bottom_input"
        )

    st.markdown("")

    # ═══════ Generate Button ═══════
    if st.button("🎨 Generate Meme!", use_container_width=True, key="meme_generate"):
        if not top_text.strip():
            st.warning("Please enter some text for your meme!")
        else:
            with st.spinner("🎨 Creating your masterpiece..."):
                img = EcoMemeGenerator.generate_meme(
                    selected_template,
                    top_text.strip(),
                    bottom_text.strip() if bottom_text else ""
                )

                # Save to session state
                img_bytes = EcoMemeGenerator.image_to_bytes(img)
                st.session_state["meme_generated_image"] = img_bytes

                # Save log
                EcoMemeGenerator.save_log(
                    user_id, selected_template,
                    top_text.strip(), bottom_text.strip() if bottom_text else ""
                )

                # Award XP
                xp_result = GamificationEngine.award_xp(user_id, "meme_generated")

                if xp_result.get("leveled_up"):
                    st.toast(f"🎉 Level Up! You're now {xp_result['level_name']}!")
                else:
                    st.toast(f"⭐ +{xp_result['xp_earned']} XP for creating a meme!")

                for badge in xp_result.get("new_badges", []):
                    st.toast(f"🏅 New Badge: {badge['name']}")

    # ═══════ Display Generated Meme ═══════
    if "meme_generated_image" in st.session_state:
        st.markdown("")
        st.markdown("""
        <h3 style="color: #2ECC71; text-align: center;">🎉 Your Meme</h3>
        """, unsafe_allow_html=True)

        col_img, col_actions = st.columns([2, 1])

        with col_img:
            st.image(
                st.session_state["meme_generated_image"],
                use_container_width=True,
                caption="Terra 2.0 Eco Meme 🌍"
            )

        with col_actions:
            st.download_button(
                "📥 Download Meme",
                data=st.session_state["meme_generated_image"],
                file_name=f"terra_meme_{selected_template}.png",
                mime="image/png",
                use_container_width=True,
            )

            st.markdown("""
            <div class="terra-card" style="text-align: center; padding: 1rem; margin-top: 1rem;">
                <div style="color: #7EC8E3; font-size: 0.85rem;">
                    📤 Share on social media<br>with #Terra2 🌍
                </div>
            </div>
            """, unsafe_allow_html=True)
