def fraction_to_percent_string(fraction):
    """
    Converts a decimal fraction (e.g., 0.51) to a rounded whole-number
    percentage string (e.g., "51%").

    Args:
        fraction (float): The decimal fraction (e.g., 0.0 to 1.0).

    Returns:
        str: The percentage string, rounded to the nearest whole number.
    """
    # Multiply by 100 to get the percentage value
    percent_value = fraction * 100

    # Round the value to the nearest whole number
    rounded_percent = round(percent_value)

    # Format as a string with the percentage sign
    return f"{rounded_percent}%"

def render_lunar_summary(phase, fraction, date_str):
    """
    Renders the current Lunar state as a simple one-line summary
    """
    percent = fraction_to_percent_string(fraction)
    print(f"Lunar profile for {date_str}: {phase} ({percent} illuminated)")

