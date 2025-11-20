import pytest
import math

from uplook.solar.chart import get_solar_chart


@pytest.mark.parametrize(
    "current_hour,daily_profile,requested_rows,expected_rows",
    [
        # requested_rows < 2 -> clamped to 2
        (
            6,
            [
                {"hour": 6, "time": "06:00", "angle_deg": 15.0},
                {"hour": 12, "time": "12:00", "angle_deg": 45.0},
            ],
            1,
            2,
        ),
        # requested_rows > 30 -> clamped to 30
        (
            12,
            [
                {"hour": 6, "time": "06:00", "angle_deg": 5.0},
                {"hour": 12, "time": "12:00", "angle_deg": 80.0},
                {"hour": 18, "time": "18:00", "angle_deg": 20.0},
            ],
            100,
            30,
        ),
        # normal case: requested_rows respected when within range
        (
            12,
            [
                {"hour": 6, "time": "06:00", "angle_deg": 15.0},
                {"hour": 12, "time": "12:00", "angle_deg": 45.0},
                {"hour": 18, "time": "18:00", "angle_deg": 10.0},
            ],
            6,
            6,
        ),
    ],
)
def test_get_solar_chart_row_count_and_labels(current_hour, daily_profile, requested_rows, expected_rows):
    chart = get_solar_chart(daily_profile, requested_rows, "*", "X", current_hour=current_hour)

    assert isinstance(chart, list)
    # chart should have expected_rows rows plus one footer separator
    assert len(chart) == expected_rows + 1

    # Determine chart ceiling as the implementation does (only angles > 0)
    max_elev = max(p['angle_deg'] for p in daily_profile if p['angle_deg'] > 0)
    chart_ceiling = math.ceil(max_elev / 10.0) * 10

    # Top label should include the ceiling value
    assert str(chart_ceiling) in chart[0]
    # Bottom (last row before footer) should include 0° label
    assert "0°" in chart[-2]

    # current_char should appear if the current hour has a positive angle
    hours_with_positive = {p['hour'] for p in daily_profile if p['angle_deg'] > 0}
    if current_hour in hours_with_positive:
        assert any("X" in line for line in chart)
    else:
        # If current hour not in positive-hours, still ensure data_char present for plotted hours
        assert any("*" in line for line in chart)


def test_get_solar_chart_boundary_angle_includes_ceiling_row():
    # Create a profile where one angle equals the ceiling
    # Use requested rows = 5
    profile = [
        {"hour": 10, "time": "10:00", "angle_deg": 20.0},
        {"hour": 12, "time": "12:00", "angle_deg": 50.0},  # max -> ceiling 50 -> round up to 50
        {"hour": 14, "time": "14:00", "angle_deg": 30.0},
    ]
    requested_rows = 5
    current_hour = 12

    chart = get_solar_chart(profile, requested_rows, "+", "@", current_hour=current_hour)

    assert isinstance(chart, list)
    # The top row should include the hour 12 plotted with current_char '@'
    assert any("@" in line for line in chart), f"Expected current_char '@' in chart rows: {chart}"
    # Ensure the ceiling is 50 (max is 50 -> ceil to nearest 10 == 50)
    assert "50°" in chart[0]


def test_get_solar_chart_returns_none_when_sun_below_horizon():
    # All negative angles -> function should return an informational message in a list
    profile = [{"hour": h, "time": f"{h:02d}:00", "angle_deg": -1.0} for h in range(24)]
    result = get_solar_chart(profile, 6, "*", "X", current_hour=0)
    assert isinstance(result, list)
    assert any("sun is below the horizon" in line for line in result)
