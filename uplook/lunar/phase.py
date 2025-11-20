import ephem


def get_moon_phase(date_str):
    """
    Calculates the illuminated fraction and descriptive phase name of the moon
    for a given date. Assumes date is provided in 'YYYY-MM-DD' format.

    Args:
        date_str (str): The date to calculate the phase for.

    Returns:
        string: The name of the Lunar phase on the provided date
    """

    # 1. Handle default date (Today in UTC)
    # Use midnight UTC for the specified date
    date_str_pyephem = date_str.replace('-', '/') + " 00:00:00"

    # 2. Compute Moon position
    moon = ephem.Moon()
    moon.compute(date_str_pyephem)

    # 3. Key Values
    fraction = moon.moon_phase  # Illuminated fraction (0.0 to 1.0)
    age = moon.phase  # Age in days (0.0 to ~29.53)

    # Cycle markers
    full_moon_age = 14.77

    # 4. Determine Descriptive Phase Name

    if fraction < 0.01:
        phase_name = "New Moon"
    elif fraction > 0.99:
        phase_name = "Full Moon"
    elif fraction < 0.49:
        # Less than half illuminated: Crescent
        if age < full_moon_age:
            phase_name = "Waxing Crescent"
        else:
            phase_name = "Waning Crescent"
    elif fraction > 0.51:
        # More than half illuminated: Gibbous
        if age < full_moon_age:
            phase_name = "Waxing Gibbous"
        else:
            phase_name = "Waning Gibbous"
    elif 0.499 < fraction < 0.501:
        # ~half illuminated: Half moon
        phase_name = "Half Moon"
    else:
        # Near 50% illuminated: Quarter
        if age < full_moon_age:
            phase_name = "First Quarter"
        else:
            phase_name = "Last Quarter"

    return phase_name, fraction