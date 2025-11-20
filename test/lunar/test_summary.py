import pytest
from uplook.lunar.summary import fraction_to_percent_string, get_lunar_summary


@pytest.mark.parametrize(
    "fraction,expected",
    [
        (0.509, "51%"),
        (0.126, "13%"),
        (0.504, "50%"),
        (0.994, "99%"),
        (0.001, "0%"),
        (0.999, "100%"),
        (0.25, "25%"),
        (0.5, "50%"),
    ],
)
def test_fraction_to_percent_string_parametrized(fraction, expected):
    assert fraction_to_percent_string(fraction) == expected


@pytest.mark.parametrize(
    "phase,frac,date,expected",
    [
        ("Full Moon", 0.9999, "2025-12-25", "Lunar profile for 2025-12-25: Full Moon (100% illuminated)"),
        ("Waning Crescent", 0.111, "2025-11-25", "Lunar profile for 2025-11-25: Waning Crescent (11% illuminated)"),
        ("First Quarter", 0.5049, "2026-03-05", "Lunar profile for 2026-03-05: First Quarter (50% illuminated)"),
        ("New Moon", 0.0001, "2026-03-12", "Lunar profile for 2026-03-12: New Moon (0% illuminated)"),
    ],
)
def test_get_lunar_summary_parametrized(phase, frac, date, expected):
    result = get_lunar_summary(phase, frac, date)
    assert result == [expected]
