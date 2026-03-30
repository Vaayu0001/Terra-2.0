"""
Terra 2.0 — Gamification Engine Tests
Tests level calculation, XP progress, and level-up mechanics.
"""

import unittest

from modules.gamification import GamificationEngine
from config import XP_PER_LEVEL, LEVEL_NAMES


class TestGamificationEngine(unittest.TestCase):
    """Test cases for GamificationEngine calculations."""

    def test_level_1_at_zero_xp(self):
        """Test that 0 XP = Level 1."""
        result = GamificationEngine.calculate_level(0)
        self.assertEqual(result["level"], 1)
        self.assertEqual(result["name"], "Seedling")
        self.assertEqual(result["progress_pct"], 0.0)

    def test_level_calculation_at_500xp(self):
        """Test level at exactly 500 XP."""
        result = GamificationEngine.calculate_level(500)
        self.assertEqual(result["level"], 2)
        self.assertEqual(result["name"], "Sprout")

    def test_level_calculation_at_499xp(self):
        """Test level just before level-up threshold."""
        result = GamificationEngine.calculate_level(499)
        self.assertEqual(result["level"], 1)
        self.assertEqual(result["name"], "Seedling")

    def test_level_calculation_at_1000xp(self):
        """Test level at 1000 XP."""
        result = GamificationEngine.calculate_level(1000)
        self.assertEqual(result["level"], 3)
        self.assertEqual(result["name"], "Sapling")

    def test_progress_percentage(self):
        """Test XP progress percentage calculation."""
        result = GamificationEngine.calculate_level(250)
        self.assertAlmostEqual(result["progress_pct"], 50.0, places=1)

    def test_progress_percentage_75(self):
        """Test 75% progress."""
        result = GamificationEngine.calculate_level(375)
        self.assertAlmostEqual(result["progress_pct"], 75.0, places=1)

    def test_xp_to_next_level(self):
        """Test XP remaining to next level."""
        result = GamificationEngine.calculate_level(100)
        self.assertEqual(result["xp_to_next"], 400)

    def test_xp_to_next_at_zero(self):
        """Test XP to next at 0 XP."""
        result = GamificationEngine.calculate_level(0)
        self.assertEqual(result["xp_to_next"], 500)

    def test_max_level_cap(self):
        """Test that level caps at 30."""
        result = GamificationEngine.calculate_level(100000)
        self.assertEqual(result["level"], 30)
        self.assertEqual(result["name"], "Earth Champion")
        self.assertEqual(result["progress_pct"], 100.0)
        self.assertEqual(result["xp_to_next"], 0)

    def test_level_30_exact(self):
        """Test exact XP for level 30."""
        result = GamificationEngine.calculate_level(29 * XP_PER_LEVEL)
        self.assertEqual(result["level"], 30)
        self.assertEqual(result["name"], "Earth Champion")

    def test_all_level_names_exist(self):
        """Test that all 30 level names are defined."""
        self.assertEqual(len(LEVEL_NAMES), 30)
        for name in LEVEL_NAMES:
            self.assertIsInstance(name, str)
            self.assertTrue(len(name) > 0)

    def test_level_names_accessible(self):
        """Test every level returns a valid name."""
        for xp in range(0, 15001, 500):
            result = GamificationEngine.calculate_level(xp)
            self.assertIn(result["name"], LEVEL_NAMES)
            self.assertGreaterEqual(result["level"], 1)
            self.assertLessEqual(result["level"], 30)


if __name__ == "__main__":
    unittest.main()
