import pytest
from uplook.solar.table import get_solar_table


@pytest.mark.parametrize(
    "daily_profile, expected_substrings",
    [
        # Empty profile: only header and footer should be present
        (
            [],
            ["Time (UTC)", "-"],
        ),
        # Populated profile: check times and formatted angle values (2 decimal places)
        (
            [
                {"hour": 0, "time": "00:00", "angle_deg": 0.0},
                {"hour": 12, "time": "12:00", "angle_deg": 45.1234},
            ],
            ["00:00", "12:00", "0.00", "45.12"],
        ),
    ],
)
def test_get_solar_table_parametrized(daily_profile, expected_substrings):
    table = get_solar_table(daily_profile)

    # Basic structure: header, separator, rows..., footer
    assert isinstance(table, list)
    assert "Time (UTC)" in table[0]
    assert table[1].startswith("-")
    assert table[-1].startswith("-")

    # Ensure expected substrings appear somewhere in the table output
    for subs in expected_substrings:
        assert any(subs in line for line in table), f"Expected '{subs}' in table output: {table}"


def test_get_solar_table_alignment_and_row_count():
    profile = [
        {"hour": 0, "time": "00:00", "angle_deg": 0.0},
        {"hour": 6, "time": "06:00", "angle_deg": 10.5},
        {"hour": 12, "time": "12:00", "angle_deg": 45.1},
        {"hour": 18, "time": "18:00", "angle_deg": 9.876},
    ]
    table = get_solar_table(profile)

    # header + separator + 4 rows + footer = 7 lines
    assert len(table) == 7

    # Check angle formatting (two decimals) and that times are present
    assert any("00:00" in line and "0.00" in line for line in table)
    assert any("06:00" in line and "10.50" in line for line in table)
    assert any("12:00" in line and "45.10" in line for line in table)
    assert any("18:00" in line and "9.88" in line for line in table)

