"""
Terra 2.0 — Eco Swipe Game
Tinder-style swipe game for eco habits. 50 habits from config.
"""

import random
from datetime import datetime

from config import SWIPE_HABITS
from database.db_setup import get_engine, get_session, SwipeScore


class EcoSwipeGame:
    """Manages the Eco Swipe Game with 50 habits."""

    @staticmethod
    def get_game_questions(n: int = 10) -> list:
        """Return n random habits from the full dataset."""
        available = min(n, len(SWIPE_HABITS))
        return random.sample(SWIPE_HABITS, available)

    @staticmethod
    def check_answer(habit: dict, user_answer: bool) -> dict:
        """
        Check if user's answer matches the habit's eco_friendly status.
        Returns {"correct": bool, "explanation": str, "xp": int}
        """
        correct = user_answer == habit.get("eco_friendly", False)
        return {
            "correct": correct,
            "explanation": habit.get("explanation", ""),
            "xp": habit.get("xp", 10) if correct else 0,
        }

    @staticmethod
    def calculate_final_score(correct: int, total: int) -> dict:
        """
        Calculate final score with grade.
        Returns {"score": int, "total": int, "accuracy": float,
                 "xp_total": int, "grade": str}
        """
        if total == 0:
            return {
                "score": 0,
                "total": 0,
                "accuracy": 0.0,
                "xp_total": 0,
                "grade": "Newbie",
            }

        accuracy = (correct / total) * 100
        xp_total = correct * 10

        if accuracy >= 90:
            grade = "Eco Legend 🌍"
        elif accuracy >= 70:
            grade = "Eco Expert 🌿"
        elif accuracy >= 50:
            grade = "Eco Learner 📚"
        else:
            grade = "Eco Newbie 🌱"

        return {
            "score": correct,
            "total": total,
            "accuracy": round(accuracy, 1),
            "xp_total": xp_total,
            "grade": grade,
        }

    @staticmethod
    def save_score(user_id: int, score_data: dict) -> bool:
        """Save swipe game score to database."""
        engine = get_engine()
        try:
            with get_session(engine) as session:
                score_entry = SwipeScore(
                    user_id=user_id,
                    score=score_data.get("score", 0),
                    correct=score_data.get("score", 0),
                    total_rounds=score_data.get("total", 10),
                    xp_earned=score_data.get("xp_total", 0),
                    played_at=datetime.utcnow(),
                )
                session.add(score_entry)
                session.commit()
                return True
        except Exception:
            return False
