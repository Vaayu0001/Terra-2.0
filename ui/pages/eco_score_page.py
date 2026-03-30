"""
Terra 2.0 — Eco Score Page
Search any product to see its eco-friendliness score and alternatives.
"""

import streamlit as st
import plotly.graph_objects as go

from ui.components import page_header, score_circle, eco_tip_card
from modules.eco_score import ProductEcoScorer
from modules.gamification import GamificationEngine


def show():
    """Render the Eco Score page."""
    if not st.session_state.get("logged_in"):
        st.warning("Please log in first.")
        st.session_state["page"] = "login"
        st.rerun()
        return

    page_header("Eco Score", "Rate any product's environmental impact", "📦")

    user_id = st.session_state.get("user_id")

    # ═══════ Product Search ═══════
    st.markdown("""
    <h3 style="color: #7EC8E3;">🔍 Search a Product</h3>
    """, unsafe_allow_html=True)

    query = st.text_input(
        "Enter product name",
        placeholder="e.g., plastic bottle, bamboo toothbrush, beef...",
        key="eco_search_input"
    )

    # Quick search suggestions
    st.markdown("""
    <p style="color: rgba(245, 240, 232, 0.5); font-size: 0.8rem;">
        Try: plastic bottle, bamboo toothbrush, beef, LED bulb, electric car
    </p>
    """, unsafe_allow_html=True)

    suggestion_items = ["plastic water bottle", "bamboo toothbrush",
                        "beef (1kg)", "LED bulb", "fast fashion item", "bicycle"]
    suggestion_cols = st.columns(len(suggestion_items))
    for col, item in zip(suggestion_cols, suggestion_items):
        with col:
            if st.button(item.split("(")[0].strip()[:12], key=f"eco_suggest_{item}",
                         use_container_width=True):
                st.session_state["eco_search_input"] = item
                st.rerun()

    if query and query.strip():
        results = ProductEcoScorer.search(query.strip())

        if not results:
            st.markdown("""
            <div class="terra-card" style="text-align: center; padding: 2rem;">
                <div style="font-size: 2rem;">🔍</div>
                <div style="color: #F5F0E8; margin-top: 0.5rem;">
                    No products found. Try a different search term.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Award XP for first result
            first = results[0]
            ProductEcoScorer.save_search(user_id, first["name"], first["score"])
            xp_result = GamificationEngine.award_xp(user_id, "product_searched")
            if xp_result.get("xp_earned", 0) > 0:
                st.toast(f"⭐ +{xp_result['xp_earned']} XP for researching products!")

            for badge in xp_result.get("new_badges", []):
                st.toast(f"🏅 New Badge: {badge['name']}")

            # Display results
            for product in results:
                score = product["score"]
                color = ProductEcoScorer.get_score_color(score)
                label = ProductEcoScorer.get_score_label(score)
                co2_equiv = ProductEcoScorer.co2_to_equivalent(product["co2_kg"])

                st.markdown("---")

                col_score, col_details = st.columns([1, 3])

                with col_score:
                    score_circle(
                        float(score), 10.0,
                        label, color
                    )

                with col_details:
                    st.markdown(f"""
                    <div class="terra-card" style="padding: 1.2rem;">
                        <h3 style="color: #F5F0E8; margin: 0; text-transform: capitalize;">
                            {product['name']}
                        </h3>
                        <div style="color: #7EC8E3; font-size: 0.85rem; margin-top: 0.3rem;">
                            📂 {product.get('category', 'General')} •
                            {'♻️ Recyclable' if product.get('recyclable') else '🚫 Not easily recyclable'}
                        </div>
                        <div style="color: {color}; font-weight: 600; margin-top: 0.5rem;">
                            🌡️ CO2 Impact: {co2_equiv}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Facts
                facts = product.get("facts", [])
                if facts:
                    st.markdown("""
                    <h4 style="color: #F4C430; margin-top: 0.5rem;">📚 Did You Know?</h4>
                    """, unsafe_allow_html=True)
                    for fact in facts:
                        st.markdown(f"""
                        <div style="color: #F5F0E8; padding: 0.3rem 0; font-size: 0.9rem;">
                            💡 {fact}
                        </div>
                        """, unsafe_allow_html=True)

                # Alternatives
                alts = product.get("alternatives", [])
                if alts:
                    st.markdown("""
                    <h4 style="color: #2ECC71; margin-top: 0.5rem;">🌿 Eco Alternatives</h4>
                    """, unsafe_allow_html=True)
                    alt_cols = st.columns(min(len(alts), 3))
                    for col, alt in zip(alt_cols, alts[:3]):
                        with col:
                            st.markdown(f"""
                            <div class="terra-card" style="text-align: center; padding: 0.8rem;">
                                <span style="color: #2ECC71;">✅ {alt}</span>
                            </div>
                            """, unsafe_allow_html=True)

                # Certifications
                certs = product.get("certifications", [])
                if certs:
                    cert_text = " • ".join([f"🏷️ {c}" for c in certs])
                    st.markdown(f"""
                    <div style="color: #7EC8E3; font-size: 0.8rem; margin-top: 0.5rem;">
                        {cert_text}
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")

    # ═══════ Compare Mode ═══════
    st.markdown("""
    <h3 style="color: #7EC8E3;">⚖️ Compare Products</h3>
    <p style="color: rgba(245, 240, 232, 0.6);">Select up to 3 products to compare</p>
    """, unsafe_allow_html=True)

    from config import PRODUCT_ECO_DB
    all_products = sorted(PRODUCT_ECO_DB.keys())

    selected_products = st.multiselect(
        "Select products to compare",
        options=all_products,
        max_selections=3,
        key="eco_compare_select"
    )

    if selected_products and len(selected_products) >= 2:
        # Comparison chart
        scores = []
        co2_values = []
        names = []

        for prod_name in selected_products:
            prod = PRODUCT_ECO_DB[prod_name]
            scores.append(prod["score"])
            co2_values.append(prod["co2_kg"])
            names.append(prod_name.title())

        # Score comparison bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=names,
                y=scores,
                marker_color=[ProductEcoScorer.get_score_color(s) for s in scores],
                text=[f"{s}/10" for s in scores],
                textposition="auto",
                textfont=dict(color="#F5F0E8", size=14),
                name="Eco Score",
            )
        ])

        fig.update_layout(
            title=dict(text="Eco Score Comparison", font=dict(color="#F5F0E8")),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F5F0E8"),
            yaxis=dict(
                range=[0, 11],
                gridcolor="rgba(46,204,113,0.1)",
                title="Eco Score"
            ),
            xaxis=dict(gridcolor="rgba(46,204,113,0.1)"),
            height=350,
            margin=dict(t=40, b=40, l=40, r=20),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Comparison table
        st.markdown("""
        <h4 style="color: #F4C430;">📊 Detailed Comparison</h4>
        """, unsafe_allow_html=True)

        header_cols = st.columns([2] + [1] * len(selected_products))
        with header_cols[0]:
            st.markdown("**Metric**")
        for i, name in enumerate(selected_products):
            with header_cols[i + 1]:
                st.markdown(f"**{name.title()[:15]}**")

        metrics_to_compare = ["score", "co2_kg", "recyclable", "category"]
        metric_labels = ["Eco Score", "CO2 (kg)", "Recyclable", "Category"]

        for metric, label in zip(metrics_to_compare, metric_labels):
            row_cols = st.columns([2] + [1] * len(selected_products))
            with row_cols[0]:
                st.markdown(f"*{label}*")
            for i, prod_name in enumerate(selected_products):
                prod = PRODUCT_ECO_DB[prod_name]
                val = prod.get(metric, "—")
                if isinstance(val, bool):
                    val = "♻️ Yes" if val else "🚫 No"
                elif isinstance(val, float):
                    val = f"{val:.2f}"
                with row_cols[i + 1]:
                    st.markdown(str(val))
