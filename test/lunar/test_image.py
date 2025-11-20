import pytest
from uplook.lunar.image import get_lunar_phase


@pytest.mark.parametrize(
    "phase,char,expected",
    [
        (
            "Full Moon",
            None,
            [
                "     ### ",
                "    #####",
                "    #####",
                "    #####",
                "     ### "
            ],
        ),
        (
            "New Moon",
            None,
            [" " * 9] * 5,
        ),
        (
            "Waxing Crescent",
            "*",
            [
                "      *  ",
                "     *   ",
                "     *   ",
                "     *   ",
                "      *  "
            ],
        ),
        (
            "not-a-phase",
            "@",
            [
                "     @@@ ",
                "    @@@@@",
                "    @@@@@",
                "    @@@@@",
                "     @@@ "
            ],
        ),
    ],
)
def test_get_lunar_phase_parametrized(phase, char, expected):
    if char is None:
        out = get_lunar_phase(phase)
    else:
        out = get_lunar_phase(phase, char)

    assert out == expected
