def get_lunar_phase(phase_name, char='#'):
    """
    Outputs a simple 5-row ASCII drawing of the moon phase.

    Args:
        phase_name (str): The descriptive name of the moon phase.
        char (str): The character to use for drawing the illuminated part.
    """

    # A dictionary mapping phase names to ASCII art patterns
    # The ' ' represents the dark part of the moon or the background.

    # Note on Waxing/Waning:
    # - Waxing (growing brighter): Light is on the right side.
    # - Waning (shrinking darker): Light is on the left side.

    moon_patterns = {
        # Fully Dark / Fully Light
        "New Moon": ["     ", "     ", "     ", "     ", "     "],
        "Full Moon": [" ### ", "#####", "#####", "#####", " ### "],

        # Quarters (Half Light)
        "First Quarter": [" ### ", "###  ", "##   ", "###  ", " ### "],  # Light on the right (Waxing)
        "Last Quarter": [" ### ", "  ###", "   ##", "  ###", " ### "],  # Light on the left (Waning)

        # Crescents (Less than half)
        "Waxing Crescent": ["  #  ", " #   ", " #   ", " #   ", "  #  "],  # Small light on the right (Waxing)
        "Waning Crescent": ["  #  ", "   # ", "   # ", "   # ", "  #  "],  # Small light on the left (Waning)

        # Gibbous (More than half)
        "Waxing Gibbous": [" ### ", "#####", "#### ", "#####", " ### "],  # Large light on the right (Waxing)
        "Waning Gibbous": [" ### ", "#####", " ####", "#####", " ### "]  # Large light on the left (Waning)
    }

    # Normalize the phase name for dictionary lookup (e.g., handles "First Quarter")
    try:
        pattern = moon_patterns[phase_name]
    except KeyError:
        pattern = moon_patterns["Full Moon"]

    # Replace the placeholder '#' with the user's chosen character
    # Pad the side with spaces for the crescent/gibbous/quarter patterns
    lines = []
    for line in pattern:
        rendered_line = line.replace('#', char)
        lines.append(f"    {rendered_line}")

    return lines