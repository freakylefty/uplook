import math
from datetime import datetime, UTC


def get_solar_chart(daily_profile, chart_rows, data_char, current_char):
    """
    Renders the solar elevation profile as a simple ASCII chart.
    """

    # 1. Filter out values below the horizon (elevation <= 0)
    sun_above_horizon = [p for p in daily_profile if p['angle_deg'] > 0]

    if not sun_above_horizon:
        print("\nNote: The sun is below the horizon for the entire day at this location/date.")
        return

    # 2. Determine the chart ceiling (max elevation rounded up to nearest 10)
    max_elevation = max(p['angle_deg'] for p in sun_above_horizon)
    # Round up to the nearest 10
    chart_ceiling = math.ceil(max_elevation / 10.0) * 10

    # Get the current hour in UTC for marking
    current_utc_hour = datetime.now(UTC).hour

    # 3. Scale and Plotting

    if chart_rows < 2:
        chart_rows = 2
    if chart_rows > 30:
        chart_rows = 30
    # Calculate the height interval for each row
    height_interval = chart_ceiling / chart_rows

    # Generate the chart rows from top (max angle) to bottom (0 degrees)
    chart_output = []

    for row_index in range(chart_rows):
        # Calculate the angle represented by the bottom of the current row segment
        angle_low = (chart_rows - 1 - row_index) * height_interval
        # Calculate the angle represented by the top of the current row segment
        angle_high = angle_low + height_interval

        row_content = []

        # Iterate through all 24 hours (columns)
        for hour_data in daily_profile:
            angle = hour_data['angle_deg']
            hour = hour_data['hour']

            # Check if the angle falls within the current row segment
            if angle_low < angle <= angle_high:
                # Determine the character to use
                if hour == current_utc_hour:
                    char = current_char
                else:
                    char = data_char
                row_content.append(char)
            else:
                # Space for hours not in this row segment or below 0 degrees
                row_content.append(' ')

                # Determine the Y-axis label
        if row_index == 0:
            # Top row label is the ceiling
            label = f"{chart_ceiling}°"
        elif row_index == chart_rows - 1:
            # Bottom row label is 0 degrees
            label = "0° "
        else:
            # Intermediate rows are unlabeled
            label = "   "

        chart_output.append(f"{label} | {' '.join(row_content)}")

    # 4. Generate the footer

    # Separator line
    separator = " " * 4 + "-" * 48
    chart_output.append(separator)
    return chart_output
    # X-axis labels
    x_axis_labels = "    00:00" + " " * 34 + "23:00"

    # Print the chart
    chart = "\n".join(chart_output) + "\n" + separator # + "\n" + x_axis_labels
    print(chart)
