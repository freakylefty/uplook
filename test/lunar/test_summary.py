import unittest
# Import the functions directly from the uploaded script
from uplook.lunar.summary import fraction_to_percent_string, get_lunar_summary


class TestSummaryFunctions(unittest.TestCase):

    ## Test Cases for fraction_to_percent_string

    def test_rounding_up(self):
        """Test rounding up to the nearest whole percentage."""
        # 0.509 rounds up to 51
        self.assertEqual(fraction_to_percent_string(0.509), "51%")
        # 0.126 rounds up to 13
        self.assertEqual(fraction_to_percent_string(0.126), "13%")

    def test_rounding_down(self):
        """Test rounding down to the nearest whole percentage."""
        # 0.504 rounds down to 50
        self.assertEqual(fraction_to_percent_string(0.504), "50%")
        # 0.994 rounds down to 99
        self.assertEqual(fraction_to_percent_string(0.994), "99%")

    def test_edge_cases_zero_and_one(self):
        """Test 0% and 100% boundary conditions."""
        self.assertEqual(fraction_to_percent_string(0.001), "0%")
        self.assertEqual(fraction_to_percent_string(0.999), "100%")

    def test_exact_integers(self):
        """Test fractions that result in exact whole numbers."""
        self.assertEqual(fraction_to_percent_string(0.25), "25%")
        self.assertEqual(fraction_to_percent_string(0.5), "50%")

    ## Test Cases for get_lunar_summary

    def test_full_moon_summary(self):
        """Test output for a Full Moon scenario."""
        # 0.9999 should round to 100%
        expected = ["Lunar profile for 2025-12-25: Full Moon (100% illuminated)"]
        result = get_lunar_summary("Full Moon", 0.9999, "2025-12-25")
        self.assertEqual(result, expected)

    def test_waning_crescent_summary(self):
        """Test output for a Waning Crescent scenario with specific rounding."""
        # 0.111 -> 11%
        expected = ["Lunar profile for 2025-11-25: Waning Crescent (11% illuminated)"]
        result = get_lunar_summary("Waning Crescent", 0.111, "2025-11-25")
        self.assertEqual(result, expected)

    def test_first_quarter_summary(self):
        """Test output for a First Quarter scenario with rounding up."""
        # 0.5049 -> 50%
        expected = ["Lunar profile for 2026-03-05: First Quarter (50% illuminated)"]
        result = get_lunar_summary("First Quarter", 0.5049, "2026-03-05")
        self.assertEqual(result, expected)

    def test_new_moon_summary(self):
        """Test output for a New Moon scenario (near 0)."""
        # 0.0001 -> 0%
        expected = ["Lunar profile for 2026-03-12: New Moon (0% illuminated)"]
        result = get_lunar_summary("New Moon", 0.0001, "2026-03-12")
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()