def render_solar_summary(daily_summary, lon, lat, date_str):
    print(f"Solar profile for {date_str} at latitude {lat}, longitude {lon}")
    if (len(daily_summary) == 0):
        print("No sunrise or sunset to report today!")
    else:
        print(f"Sunrise: {daily_summary[0]}, Zenith: {daily_summary[1]}, Sunset: {daily_summary[2]}")
