import ephem


def determine_phase_name(fraction, age, full_moon_age=14.77):
    """
    Determine a descriptive lunar phase name from the illuminated fraction and age.

    Args:
        fraction (float): Illuminated fraction (0.0 to 1.0)
        age (float): Age of the moon in days since previous new moon
        full_moon_age (float): Age (in days) that roughly corresponds to full moon

    Returns:
        str: Descriptive phase name
    """

    if fraction < 0.01:
        return "New Moon"
    if fraction > 0.99:
        return "Full Moon"
    if fraction < 0.49:
        # Less than half illuminated: Crescent
        if age < full_moon_age:
            return "Waxing Crescent"
        else:
            return "Waning Crescent"
    if fraction > 0.51:
        # More than half illuminated: Gibbous
        if age < full_moon_age:
            return "Waxing Gibbous"
        else:
            return "Waning Gibbous"
    # Near 50% illuminated: Quarter
    if age < full_moon_age:
        return "First Quarter"
    return "Last Quarter"


def get_moon_phase(date_str):
    """
    Calculates the illuminated fraction and descriptive phase name of the moon
    for a given date. Assumes date is provided in 'YYYY-MM-DD' format.

    Args:
        date_str (str): The date to calculate the phase for.

    Returns:
        phase_name (str): The name of the Lunar phase on the provided date
        fraction (float): The fraction of the moon illuminated
    """

    # 1. Handle default date (Today in UTC)
    # Use midnight UTC for the specified date
    date_str_pyephem = date_str.replace('-', '/') + " 00:00:00"

    # 2. Compute Moon position
    moon = ephem.Moon()
    moon.compute(date_str_pyephem)

    # 3. Key Values
    current_date_ephem = ephem.Date(date_str_pyephem)
    prev_new_moon_date = ephem.previous_new_moon(date_str_pyephem)
    fraction = moon.moon_phase  # Illuminated fraction (0.0 to 1.0)
    age = current_date_ephem - prev_new_moon_date  # Age in days (0.0 to ~29.53)

    # 4. Determine Descriptive Phase Name
    phase_name = determine_phase_name(fraction, age)

    return phase_name, fraction