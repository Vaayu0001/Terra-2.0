from modules.auth import AuthManager
from modules.gamification import GamificationEngine
from modules.carbon_tracker import CarbonTracker
from modules.swipe_game import EcoSwipeGame
from modules.ai_roast import AIRoaster
from modules.meme_generator import EcoMemeGenerator
from modules.eco_score import ProductEcoScorer
from modules.waste_classifier import WasteClassifier
from modules.leaderboard import CollegeLeaderboard

__all__ = [
    "AuthManager",
    "GamificationEngine",
    "CarbonTracker",
    "EcoSwipeGame",
    "AIRoaster",
    "EcoMemeGenerator",
    "ProductEcoScorer",
    "WasteClassifier",
    "CollegeLeaderboard",
]
