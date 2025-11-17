def render_solar_table(daily_profile):
    """
    Renders the solar elevation profile as a simple ASCII table.
    """

    # Print the table header
    print("{:<10} {:>10}".format("Time (UTC)", "Angle (Deg)"))
    print("-" * 21)

    # Print the data rows
    for entry in daily_profile:
        print("{:<10} {:>10.2f}".format(entry["time"], entry["angle_deg"]))
    print("-" * 21)
