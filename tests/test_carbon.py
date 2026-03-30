"""
Terra 2.0 — Carbon Tracker Tests
Tests emission calculations, totals, ratings, and tip generation.
"""

import unittest

from modules.carbon_tracker import CarbonTracker
from config import INDIA_AVG_DAILY_KG


class TestCarbonTracker(unittest.TestCase):
    """Test cases for CarbonTracker calculations."""

    def test_car_transport_calculation(self):
        """Test car (petrol) transport CO2 calculation."""
        # 0.21 kg CO2 per km * 10 km = 2.1 kg
        result = CarbonTracker.calculate_transport("Car (petrol)", 10.0)
        self.assertAlmostEqual(result, 2.1, places=2)

    def test_bus_transport_calculation(self):
        """Test bus transport CO2 calculation."""
        # 0.089 kg CO2 per km * 20 km = 1.78 kg
        result = CarbonTracker.calculate_transport("Bus", 20.0)
        self.assertAlmostEqual(result, 1.78, places=2)

    def test_zero_emission_transport(self):
        """Test zero-emission transport modes."""
        self.assertEqual(CarbonTracker.calculate_transport("Walking", 5.0), 0.0)
        self.assertEqual(CarbonTracker.calculate_transport("Bicycle", 10.0), 0.0)

    def test_vegan_food_calculation(self):
        """Test vegan food CO2 calculation."""
        # Vegan daily = 1.50 kg CO2, per meal = 0.5, 3 meals = 1.5
        result = CarbonTracker.calculate_food("Vegan", 3)
        self.assertAlmostEqual(result, 1.5, places=1)

    def test_heavy_meat_food_calculation(self):
        """Test heavy meat food CO2 calculation."""
        # Heavy meat daily = 7.19, per meal = 2.397, 3 meals = 7.19
        result = CarbonTracker.calculate_food("Heavy meat (daily)", 3)
        self.assertAlmostEqual(result, 7.19, places=1)

    def test_energy_calculation(self):
        """Test energy CO2 calculation."""
        # 5 kWh * 0.82 = 4.1 kg CO2
        result = CarbonTracker.calculate_energy(5.0)
        self.assertAlmostEqual(result, 4.1, places=1)

    def test_shopping_calculation(self):
        """Test shopping CO2 calculation."""
        items = {"Clothing item": 2, "Electronic device": 1}
        # 10*2 + 70*1 = 90 kg
        result = CarbonTracker.calculate_shopping(items)
        self.assertAlmostEqual(result, 90.0, places=1)

    def test_total_below_average(self):
        """Test that low emissions get 'Low' rating."""
        result = CarbonTracker.get_total(0.5, 1.0, 0.5, 0.0)
        self.assertEqual(result["rating"], "Low")
        self.assertTrue(result["total_kg"] < 3.5)

    def test_total_above_average(self):
        """Test that high emissions get 'High' rating."""
        result = CarbonTracker.get_total(3.0, 3.0, 2.5, 1.0)
        self.assertEqual(result["rating"], "High")
        self.assertTrue(result["total_kg"] >= 7.0)

    def test_total_average_rating(self):
        """Test that moderate emissions get 'Average' rating."""
        result = CarbonTracker.get_total(1.5, 2.0, 1.0, 0.5)
        self.assertEqual(result["rating"], "Average")

    def test_comparison_percentage(self):
        """Test India average comparison calculation."""
        result = CarbonTracker.get_total(1.0, 1.0, 0.6, 0.0)
        expected_pct = round((2.6 / INDIA_AVG_DAILY_KG) * 100, 1)
        self.assertAlmostEqual(result["comparison_pct"], expected_pct, places=1)

    def test_tips_generated(self):
        """Test that tips are generated for any result."""
        result = CarbonTracker.get_total(3.0, 2.0, 1.0, 0.5)
        tips = CarbonTracker.generate_tips(result)
        self.assertEqual(len(tips), 5)
        self.assertTrue(all(isinstance(t, str) for t in tips))

    def test_tips_transport_heavy(self):
        """Test that transport-heavy results get transport tips first."""
        result = CarbonTracker.get_total(5.0, 1.0, 0.5, 0.0)
        tips = CarbonTracker.generate_tips(result)
        # First 3 tips should mention transport-related content
        transport_keywords = ["transport", "bus", "cycle", "walk", "carpool", "metro", "commute"]
        first_tip_lower = tips[0].lower()
        has_transport = any(kw in first_tip_lower for kw in transport_keywords)
        self.assertTrue(has_transport)


if __name__ == "__main__":
    unittest.main()
