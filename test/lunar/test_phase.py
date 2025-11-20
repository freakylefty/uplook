import pytest
from uplook.lunar.phase import get_moon_phase, determine_phase_name
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


@pytest.mark.parametrize(
    "fraction,age,expected",
    [
        # New Moon
        (0.0, 0.0, "New Moon"),
        (0.005, 1.0, "New Moon"),
        # Full Moon
        (1.0, 14.77, "Full Moon"),
        (0.995, 14.77, "Full Moon"),
        # Waxing Crescent (fraction < 0.49 and age < full_moon_age)
        (0.1, 5.0, "Waxing Crescent"),
        # Waning Crescent (fraction < 0.49 and age >= full_moon_age)
        (0.2, 20.0, "Waning Crescent"),
        # Waxing Gibbous (fraction > 0.51 and age < full_moon_age)
        (0.6, 10.0, "Waxing Gibbous"),
        # Waning Gibbous (fraction > 0.51 and age >= full_moon_age)
        (0.8, 20.0, "Waning Gibbous"),
        # First Quarter (near 50% and age < full_moon_age)
        (0.5, 10.0, "First Quarter"),
        # Last Quarter (near 50% and age >= full_moon_age)
        (0.5, 20.0, "Last Quarter"),
    ],
)
def test_determine_phase_name_parametrized(fraction, age, expected):
    name = determine_phase_name(fraction, age)
    assert name == expected
