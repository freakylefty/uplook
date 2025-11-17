import ephem


def calculate_solar_elevation(date_str, time_str, longitude, latitude):
    """
    Calculates the solar angle of elevation for a given date, time, and location.
    Assumes the input time is in UTC (Coordinated Universal Time).
    """
    try:
        # Create an Observer object for the location
        observer = ephem.Observer()
        observer.lon = str(longitude)
        observer.lat = str(latitude)

        # Set the observer's date and time (combined string, assumed UTC)
        observer.date = f"{date_str} {time_str}"

        # Compute the Sun's position relative to the observer
        sun = ephem.Sun()
        sun.compute(observer)

        # Extract the altitude (elevation) and convert from radians to degrees
        elevation_rad = sun.alt
        # pyephem constants are accessed via the library name
        elevation_deg = elevation_rad * (180 / ephem.pi)

        return elevation_deg

    except Exception as e:
        print(f"Error calculating elevation for {date_str} {time_str}: {e}")
        return None

def get_daily_solar_profile(longitude, latitude, date_str):
    """Generates an array of solar elevation angles for every hour (00:00 to 23:00 UTC)."""

    hourly_angles = []

    for hour in range(24):
        time_str = f"{hour:02d}:00"
        angle = calculate_solar_elevation(date_str, time_str, longitude, latitude)

        if angle is not None:
            hourly_angles.append({
                "hour": hour,
                "time": time_str,
                "angle_deg": round(angle, 2)
            })

    return hourly_angles

def get_daily_solar_summary(longitude, latitude, date_str):
    """
    Generates an array containing times for sunrise, solar zenith, and sunset
    for the given date and location.

    Returns:
        list: [<time of sunrise>, <time of solar zenith>, <time of sunset>] in HH:MM format (UTC).
              Returns [] if the sun does not rise or set.
    """
    # 1. Setup Observer
    observer = ephem.Observer()
    observer.lon = str(longitude)
    observer.lat = str(latitude)
    observer.date = date_str  # Use the start of the day for reference

    sun = ephem.Sun()

    # 2. Calculate Events (Sunrise, Sunset, and Transit/Zenith)

    # pyephem methods:
    #   - `next_rising(body)`: Calculates the next time the top of the body is on the horizon.
    #   - `next_transit(body)`: Calculates the next time the body is due South (highest point).
    #   - `next_setting(body)`: Calculates the next time the top of the body is on the horizon.

    # We use next_rising/setting for the date, but must handle the possibility
    # that the event occurs on the *previous* or *next* day.

    try:
        # Check for Sunrise
        # We start the search from the beginning of the day (date_str)
        sunrise_ephem_date = observer.next_rising(sun)

        # Check for Sunset
        # Start search from the calculated sunrise time to ensure we get the *next* setting
        observer.date = sunrise_ephem_date
        sunset_ephem_date = observer.next_setting(sun)

    except ephem.CircumpolarError:
        # Sun is either up all day (Circumpolar Stars) or down all day (Polar Night)
        # In this case, neither rise nor set occurs.
        return []

    # 3. Check if all events fall on the input date

    # Reset observer to the start of the target day
    target_day = ephem.Date(date_str)
    # The day after the target day
    next_day = ephem.Date(target_day + 1)

    # If the rise or set is outside the target day (>= next_day), the events
    # calculated might not be the correct ones for the 00:00-23:59 period of the input date.
    if sunrise_ephem_date >= next_day or sunset_ephem_date >= next_day:
        return []

    # 4. Calculate Transit (Solar Zenith) Time

    # Transit (zenith) must be calculated between the rise and set times
    observer.date = sunrise_ephem_date  # Start search after sunrise
    transit_ephem_date = observer.next_transit(sun)

    # 5. Format Output Times

    # pyephem dates are epoch days; convert to Python datetime objects
    # .datetime() converts to a UTC aware datetime
    sunrise_dt = ephem.Date(sunrise_ephem_date).datetime()
    transit_dt = ephem.Date(transit_ephem_date).datetime()
    sunset_dt = ephem.Date(sunset_ephem_date).datetime()

    # Format to HH:MM (UTC)
    time_format = "%H:%M"

    summary = [
        sunrise_dt.strftime(time_format),
        transit_dt.strftime(time_format),
        sunset_dt.strftime(time_format)
    ]

    return summary
