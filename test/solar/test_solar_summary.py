import pytest
from uplook.solar.summary import get_solar_summary


@pytest.mark.parametrize(
    "daily_summary,lon,lat,date_str,expected_contains",
    [
        ([], 0.0, 0.0, "2025-11-20", "No sunrise or sunset to report today!"),
        (
            ["06:45", "12:00", "17:30"],
            -0.1278,
            51.5074,
            "2025-11-20",
            "Sunrise: 06:45, Zenith: 12:00, Sunset: 17:30",
        ),
    ],
)
def test_get_solar_summary_parametrized(daily_summary, lon, lat, date_str, expected_contains):
    lines = get_solar_summary(daily_summary, lon, lat, date_str)
    # First line should always contain the date and coordinates
    assert lines[0].startswith(f"Solar profile for {date_str} at latitude {lat}, longitude {lon}")
    # The remainder should include the expected string
    assert any(expected_contains in line for line in lines)

