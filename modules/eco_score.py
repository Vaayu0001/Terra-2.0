"""
Terra 2.0 — Product Eco Score Module
Searches products by fuzzy match and returns eco scores.
"""

import difflib
from datetime import datetime

from config import PRODUCT_ECO_DB
from database.db_setup import get_engine, get_session, EcoSearch


class ProductEcoScorer:
    """Searches and scores products for eco-friendliness."""

    @staticmethod
    def search(query: str) -> list:
        """
        Search products by exact match or fuzzy match.
        Returns list of product dicts with "name" added.
        """
        query_lower = query.lower().strip()
        results = []

        # Exact match first
        if query_lower in PRODUCT_ECO_DB:
            product = PRODUCT_ECO_DB[query_lower].copy()
            product["name"] = query_lower
            results.append(product)
            return results

        # Fuzzy match
        all_keys = list(PRODUCT_ECO_DB.keys())
        matches = difflib.get_close_matches(
            query_lower, all_keys, n=5, cutoff=0.4
        )

        for match_key in matches:
            product = PRODUCT_ECO_DB[match_key].copy()
            product["name"] = match_key
            results.append(product)

        # Also check substring matches
        if not results:
            for key in all_keys:
                if query_lower in key or key in query_lower:
                    product = PRODUCT_ECO_DB[key].copy()
                    product["name"] = key
                    results.append(product)
                    if len(results) >= 5:
                        break

        return results

    @staticmethod
    def get_score_color(score: int) -> str:
        """Return hex color based on eco score."""
        if score <= 3:
            return "#EF4444"  # Red
        elif score <= 6:
            return "#F59E0B"  # Amber/Yellow
        else:
            return "#22C55E"  # Green

    @staticmethod
    def co2_to_equivalent(co2_kg: float) -> str:
        """Convert CO2 in kg to human-readable equivalent."""
        if co2_kg < 0.5:
            return f"{co2_kg * 1000:.0f}g CO2"
        elif co2_kg < 5:
            return f"driving {co2_kg / 0.21:.1f} km by car"
        elif co2_kg < 50:
            return f"charging your phone {co2_kg / 0.005:.0f} times"
        else:
            return f"{co2_kg:.0f} kg CO2 — significant impact"

    @staticmethod
    def get_score_label(score: int) -> str:
        """Get descriptive label for eco score."""
        labels = {
            1: "Very Poor",
            2: "Poor",
            3: "Below Average",
            4: "Fair",
            5: "Average",
            6: "Above Average",
            7: "Good",
            8: "Very Good",
            9: "Excellent",
            10: "Outstanding",
        }
        return labels.get(score, "Unknown")

    @staticmethod
    def save_search(user_id: int, product: str, score: int) -> None:
        """Save product search to database."""
        engine = get_engine()
        try:
            with get_session(engine) as session:
                search_log = EcoSearch(
                    user_id=user_id,
                    product_name=product,
                    eco_score=score,
                    searched_at=datetime.utcnow(),
                )
                session.add(search_log)
                session.commit()
        except Exception:
            pass  # Non-critical logging
