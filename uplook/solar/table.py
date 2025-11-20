def get_solar_table(daily_profile):
    """
    Renders the solar elevation profile as a simple ASCII table.
    """

    lines = []

    # Print the table header
    lines.append("{:<10} {:>10}".format("Time (UTC)", "Angle (Deg)"))
    lines.append("-" * 21)

    # Print the data rows
    for entry in daily_profile:
        lines.append("{:<10} {:>10.2f}".format(entry["time"], entry["angle_deg"]))
    lines.append("-" * 21)
    return lines
