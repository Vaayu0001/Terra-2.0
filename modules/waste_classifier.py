"""
Terra 2.0 — Waste Classifier Module
Classifies waste items using fuzzy matching against the waste database.
"""

import difflib
from datetime import datetime

from config import WASTE_DB
from database.db_setup import get_engine, get_session, WasteLog


class WasteClassifier:
    """Classifies waste items and provides disposal instructions."""

    CATEGORY_COLORS = {
        "Wet/Organic": "#22C55E",
        "Dry/Recyclable": "#3B82F6",
        "Hazardous": "#EF4444",
        "E-Waste": "#F59E0B",
        "Medical": "#A855F7",
        "Sanitary": "#6B7280",
    }

    @staticmethod
    def classify(item_name: str) -> dict | None:
        """
        Classify a waste item by name.
        Returns waste dict with "name" and "color" added, or None.
        """
        item_lower = item_name.lower().strip()

        # Exact match
        if item_lower in WASTE_DB:
            result = WASTE_DB[item_lower].copy()
            result["name"] = item_lower
            result["color"] = WasteClassifier.CATEGORY_COLORS.get(
                result["category"], "#6B7280"
            )
            return result

        # Fuzzy match
        all_keys = list(WASTE_DB.keys())
        matches = difflib.get_close_matches(
            item_lower, all_keys, n=1, cutoff=0.5
        )

        if matches:
            best_match = matches[0]
            result = WASTE_DB[best_match].copy()
            result["name"] = best_match
            result["color"] = WasteClassifier.CATEGORY_COLORS.get(
                result["category"], "#6B7280"
            )
            return result

        # Substring match
        for key in all_keys:
            if item_lower in key or key in item_lower:
                result = WASTE_DB[key].copy()
                result["name"] = key
                result["color"] = WasteClassifier.CATEGORY_COLORS.get(
                    result["category"], "#6B7280"
                )
                return result

        return None

    @staticmethod
    def get_quick_items() -> list:
        """Return common quick-access items for the UI."""
        quick_keys = [
            "banana peel", "old phone", "battery",
            "cardboard box", "medicine tablets",
            "plastic bottle", "glass bottle", "newspaper",
        ]
        items = []
        for key in quick_keys:
            if key in WASTE_DB:
                item = WASTE_DB[key].copy()
                item["name"] = key
                item["color"] = WasteClassifier.CATEGORY_COLORS.get(
                    item["category"], "#6B7280"
                )
                items.append(item)
        return items

    @staticmethod
    def get_all_categories() -> dict:
        """Return category summary with counts."""
        categories = {}
        for key, item in WASTE_DB.items():
            cat = item["category"]
            if cat not in categories:
                categories[cat] = {
                    "count": 0,
                    "color": WasteClassifier.CATEGORY_COLORS.get(cat, "#6B7280"),
                    "items": [],
                }
            categories[cat]["count"] += 1
            categories[cat]["items"].append(key)
        return categories

    @staticmethod
    def save_log(user_id: int, item: str, category: str) -> None:
        """Save waste classification to database."""
        engine = get_engine()
        try:
            with get_session(engine) as session:
                log = WasteLog(
                    user_id=user_id,
                    item_name=item,
                    category=category,
                    logged_at=datetime.utcnow(),
                )
                session.add(log)
                session.commit()
        except Exception:
            pass  # Non-critical logging
