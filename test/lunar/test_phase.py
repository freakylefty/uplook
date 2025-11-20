import pytest
from uplook.lunar.phase import get_moon_phase
from uplook.lunar.summary import fraction_to_percent_string


@pytest.mark.parametrize(
    "date,expected_phase,expected_percent",
    [
        ("2025-11-20", "New Moon", "0%"),
        ("2025-11-24", "Waxing Crescent", "12%"),
        ("2025-11-29", "Waxing Gibbous", "58%"),
        ("2025-12-05", "Full Moon", "100%"),
        ("2025-12-10", "Waning Gibbous", "69%"),
        ("2025-12-15", "Waning Crescent", "22%"),
    ],
)
def test_get_moon_phase_parametrized(date, expected_phase, expected_percent):
    phase_name, fraction = get_moon_phase(date)
    assert phase_name == expected_phase
    assert fraction_to_percent_string(fraction) == expected_percent
