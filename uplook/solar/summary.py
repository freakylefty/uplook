def get_solar_summary(daily_summary, lon, lat, date_str):
    lines = []
    lines.append(f"Solar profile for {date_str} at latitude {lat}, longitude {lon}")
    if (len(daily_summary) == 0):
        lines.append("No sunrise or sunset to report today!")
    else:
        lines.append(f"Sunrise: {daily_summary[0]}, Zenith: {daily_summary[1]}, Sunset: {daily_summary[2]}")
    return lines
