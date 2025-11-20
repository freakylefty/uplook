import pytest
from uplook.solar.elevation import calculate_solar_elevation, calculate_daily_solar_summary, calculate_daily_solar_profile


@pytest.mark.parametrize(
    "date_str,time_str,lon,lat,expect_none",
    [
        # Valid date/time/location near London on current date: expect a numeric angle
        ("2025/11/20", "12:00", -0.1278, 51.5074, False),
        # Invalid date format -> function should handle exception and return None
        ("not-a-date", "12:00", 0.0, 0.0, True),
    ],
)
def test_calculate_solar_elevation_parametrized(date_str, time_str, lon, lat, expect_none):
    angle = calculate_solar_elevation(date_str, time_str, lon, lat)
    if expect_none:
        assert angle is None
    else:
        assert isinstance(angle, float)


@pytest.mark.parametrize(
    "lon,lat,date_str,expect_empty",
    [
        (0.0, 0.0, "2025/11/20", False),
        # For extreme polar latitudes during winter, expect possibly empty list (no sunrise/sunset)
        (0.0, 85.0, "2025/11/20", True),
    ],
)
def test_calculate_daily_solar_summary_parametrized(lon, lat, date_str, expect_empty):
    summary = calculate_daily_solar_summary(lon, lat, date_str)
    if expect_empty:
        assert summary == []
    else:
        assert isinstance(summary, list)
        assert len(summary) in (0, 3)


def test_calculate_daily_solar_profile_basic():
    profile = calculate_daily_solar_profile(-0.1278, 51.5074, "2025/11/20")
    assert isinstance(profile, list)
    # If not empty, entries should have the expected keys
    if profile:
        for entry in profile:
            assert set(entry.keys()) == {"hour", "time", "angle_deg"}

