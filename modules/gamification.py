"""
Terra 2.0 — Gamification Engine
Manages XP awards, level calculations, and badge achievements.
"""

from datetime import datetime

from sqlalchemy import select, func

from config import XP_RULES, XP_PER_LEVEL, LEVEL_NAMES
from database.db_setup import (
    get_engine, get_session,
    User, Achievement, FootprintLog, SwipeScore, WasteLog, EcoSearch, MemeLog
)
from modules.auth import AuthManager


# Badge definitions: (badge_name, badge_icon, condition_check_function_name)
BADGE_DEFINITIONS = [
    {"name": "First Steps 🌱", "icon": "🌱",
     "description": "Log your first carbon footprint",
     "check": "first_footprint"},
    {"name": "Carbon Conscious 📊", "icon": "📊",
     "description": "Log 5 carbon footprints",
     "check": "five_footprints"},
    {"name": "Eco Warrior 🛡️", "icon": "🛡️",
     "description": "Log 10 carbon footprints",
     "check": "ten_footprints"},
    {"name": "Swipe Starter 🃏", "icon": "🃏",
     "description": "Complete your first swipe game",
     "check": "first_swipe"},
    {"name": "Swipe Master 🎯", "icon": "🎯",
     "description": "Score 8/10 or higher in swipe game",
     "check": "swipe_master"},
    {"name": "Meme Lord 😂", "icon": "😂",
     "description": "Create 5 memes",
     "check": "five_memes"},
    {"name": "Waste Wizard ♻️", "icon": "♻️",
     "description": "Classify 10 waste items",
     "check": "ten_waste"},
    {"name": "Product Guru 🔍", "icon": "🔍",
     "description": "Search 10 product eco scores",
     "check": "ten_searches"},
    {"name": "Streak Fire 🔥", "icon": "🔥",
     "description": "Maintain a 7-day login streak",
     "check": "seven_streak"},
    {"name": "Level 5 Club 🌿", "icon": "🌿",
     "description": "Reach level 5",
     "check": "level_five"},
    {"name": "Level 10 Elite 🌳", "icon": "🌳",
     "description": "Reach level 10",
     "check": "level_ten"},
    {"name": "XP Hunter 💎", "icon": "💎",
     "description": "Earn 1000 total XP",
     "check": "xp_1000"},
    {"name": "Green Machine 🤖", "icon": "🤖",
     "description": "Earn 5000 total XP",
     "check": "xp_5000"},
    {"name": "Low Carbon Hero 🦸", "icon": "🦸",
     "description": "Log a footprint under 3 kg CO2",
     "check": "low_carbon"},
    {"name": "Roast Survivor 🔥", "icon": "🔥",
     "description": "Get roasted by AI",
     "check": "first_roast"},
]


class GamificationEngine:
    """Manages XP awards, level calculations, and badge achievements."""

    @staticmethod
    def award_xp(user_id: int, action: str) -> dict:
        """
        Award XP for an action, check for new badges.
        Returns {"xp_earned": int, "leveled_up": bool,
                 "new_badges": list, "level_name": str}
        """
        xp_amount = XP_RULES.get(action, 0)
        if xp_amount == 0:
            return {
                "xp_earned": 0,
                "leveled_up": False,
                "new_badges": [],
                "level_name": "",
            }

        result = AuthManager.update_xp(user_id, xp_amount)
        new_badges = GamificationEngine.check_and_award_badges(user_id)

        return {
            "xp_earned": xp_amount,
            "leveled_up": result["leveled_up"],
            "new_badges": new_badges,
            "level_name": result["level_name"],
        }

    @staticmethod
    def calculate_level(xp: int) -> dict:
        """
        Calculate level info from XP.
        Returns {"level": int, "name": str,
                 "progress_pct": float, "xp_to_next": int}
        """
        level = min(xp // XP_PER_LEVEL + 1, 30)
        if level >= 30:
            return {
                "level": 30,
                "name": LEVEL_NAMES[29],
                "progress_pct": 100.0,
                "xp_to_next": 0,
            }
        progress_pct = (xp % XP_PER_LEVEL) / XP_PER_LEVEL * 100
        xp_to_next = XP_PER_LEVEL - (xp % XP_PER_LEVEL)
        return {
            "level": level,
            "name": LEVEL_NAMES[level - 1],
            "progress_pct": round(progress_pct, 1),
            "xp_to_next": xp_to_next,
        }

    @staticmethod
    def check_and_award_badges(user_id: int) -> list:
        """
        Check all badge conditions and award any not yet earned.
        Returns list of newly awarded badge dicts.
        """
        engine = get_engine()
        new_badges = []

        with get_session(engine) as session:
            # Get existing badges
            existing = session.execute(
                select(Achievement.badge_name).where(Achievement.user_id == user_id)
            ).scalars().all()
            existing_set = set(existing)

            # Get user stats
            user = session.execute(
                select(User).where(User.id == user_id)
            ).scalar_one_or_none()
            if user is None:
                return []

            # Count various activities
            footprint_count = session.execute(
                select(func.count(FootprintLog.id)).where(
                    FootprintLog.user_id == user_id
                )
            ).scalar() or 0

            swipe_count = session.execute(
                select(func.count(SwipeScore.id)).where(
                    SwipeScore.user_id == user_id
                )
            ).scalar() or 0

            best_swipe = session.execute(
                select(func.max(SwipeScore.correct)).where(
                    SwipeScore.user_id == user_id
                )
            ).scalar() or 0

            meme_count = session.execute(
                select(func.count(MemeLog.id)).where(
                    MemeLog.user_id == user_id
                )
            ).scalar() or 0

            waste_count = session.execute(
                select(func.count(WasteLog.id)).where(
                    WasteLog.user_id == user_id
                )
            ).scalar() or 0

            search_count = session.execute(
                select(func.count(EcoSearch.id)).where(
                    EcoSearch.user_id == user_id
                )
            ).scalar() or 0

            min_footprint = session.execute(
                select(func.min(FootprintLog.total_kg)).where(
                    FootprintLog.user_id == user_id
                )
            ).scalar()

            # Check each badge
            badge_checks = {
                "first_footprint": footprint_count >= 1,
                "five_footprints": footprint_count >= 5,
                "ten_footprints": footprint_count >= 10,
                "first_swipe": swipe_count >= 1,
                "swipe_master": best_swipe >= 8,
                "five_memes": meme_count >= 5,
                "ten_waste": waste_count >= 10,
                "ten_searches": search_count >= 10,
                "seven_streak": user.streak >= 7,
                "level_five": user.level >= 5,
                "level_ten": user.level >= 10,
                "xp_1000": user.xp >= 1000,
                "xp_5000": user.xp >= 5000,
                "low_carbon": (min_footprint is not None and min_footprint < 3.0),
                "first_roast": True,  # Awarded directly when roast happens
            }

            for badge_def in BADGE_DEFINITIONS:
                badge_name = badge_def["name"]
                check_key = badge_def["check"]

                if badge_name in existing_set:
                    continue

                # Special case: first_roast is only awarded directly
                if check_key == "first_roast":
                    continue

                if badge_checks.get(check_key, False):
                    new_achievement = Achievement(
                        user_id=user_id,
                        badge_name=badge_name,
                        badge_icon=badge_def["icon"],
                        earned_at=datetime.utcnow(),
                    )
                    session.add(new_achievement)
                    new_badges.append({
                        "name": badge_name,
                        "icon": badge_def["icon"],
                        "description": badge_def["description"],
                    })

            session.commit()

        return new_badges

    @staticmethod
    def award_specific_badge(user_id: int, badge_check_key: str) -> dict | None:
        """Award a specific badge by its check key if not already earned."""
        engine = get_engine()
        with get_session(engine) as session:
            for badge_def in BADGE_DEFINITIONS:
                if badge_def["check"] == badge_check_key:
                    existing = session.execute(
                        select(Achievement).where(
                            Achievement.user_id == user_id,
                            Achievement.badge_name == badge_def["name"]
                        )
                    ).scalar_one_or_none()

                    if existing is not None:
                        return None

                    new_achievement = Achievement(
                        user_id=user_id,
                        badge_name=badge_def["name"],
                        badge_icon=badge_def["icon"],
                        earned_at=datetime.utcnow(),
                    )
                    session.add(new_achievement)
                    session.commit()
                    return {
                        "name": badge_def["name"],
                        "icon": badge_def["icon"],
                        "description": badge_def["description"],
                    }
        return None

    @staticmethod
    def get_user_badges(user_id: int) -> list:
        """Get all badges earned by user."""
        engine = get_engine()
        with get_session(engine) as session:
            achievements = session.execute(
                select(Achievement).where(Achievement.user_id == user_id)
            ).scalars().all()

            return [
                {
                    "name": a.badge_name,
                    "icon": a.badge_icon,
                    "earned_at": a.earned_at.isoformat() if a.earned_at else "",
                }
                for a in achievements
            ]
