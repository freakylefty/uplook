import argparse
from datetime import datetime, UTC
from solar.elevation import get_daily_solar_profile, get_daily_solar_summary
from solar.chart import render_solar_chart
from solar.summary import render_solar_summary
from solar.table import render_solar_table
from lunar.phase import get_moon_phase
from lunar.summary import render_lunar_summary
from lunar.image import render_lunar_phase

def setup_arg_parser():
    """
    Sets up the argument parser with 'solar' and 'lunar' subparsers
    """
    # 1. Main Parser Setup
    parser = argparse.ArgumentParser(
        description="Calculate and output solar and/or lunar data"
    )

    # Arguments common to both solar and lunar commands (only --date is common)
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        '--date',
        type=str,
        default=None,
        help="Optional: Date in YYYY-MM-DD format. Defaults to today's UTC date."
    )

    # 2. Subparser Initialization
    subparsers = parser.add_subparsers(
        dest='command',
        required=True,
        help='The subcommand to run (solar or lunar)'
    )

    # 3. Solar Subparser
    solar_parser = subparsers.add_parser(
        'solar',
        parents=[common_parser],  # Inherit --date
        help='Calculate and output hourly solar elevation data.'
    )
    # --- Location is REQUIRED for Solar calculations ---
    solar_parser.add_argument(
        '--lon',
        type=float,
        required=True,
        help="The longitude of the location in decimal degrees (e.g., -0.12)."
    )
    solar_parser.add_argument(
        '--lat',
        type=float,
        required=True,
        help="The latitude of the location in decimal degrees (e.g., 51.51)."
    )
    # --- Solar Output Configuration ---
    solar_parser.add_argument(
        '--type',
        type=str,
        required=False,
        default='summary',
        choices=['chart', 'summary', 'table'],
        help='Output type, one of: chart, table or summary'
    )
    solar_parser.add_argument(
        '--rows',
        type=int,
        default=5,
        help="The vertical height of the chart in rows (default: 5)."
    )
    solar_parser.add_argument(
        '--data-char',
        type=str,
        default='.',
        help="The character used to mark the sun's position (default: '.')."
    )
    solar_parser.add_argument(
        '--current-char',
        type=str,
        default='O',
        help="The character used to mark the current hour (default: 'O')."
    )

    # 4. Lunar Subparser
    lunar_parser = subparsers.add_parser(
        'lunar',
        parents=[common_parser],  # Inherit --date
        help='Calculate and output the Moon phase for a given date.'
    )
    # --- Lunar Output Configuration ---
    lunar_parser.add_argument(
        '--type',
        type=str,
        required=False,
        default='summary',
        choices=['image', 'summary', 'combined'],
        help='Output type, one of: image, summary, combined'
    )
    lunar_parser.add_argument(
        '--char',
        type=str,
        default='#',
        help="The character used for the moon image (default: '#')."
    )

    return parser

def main():
    parser = setup_arg_parser()
    args = parser.parse_args()

    if args.date is None:
        today_utc = datetime.now(UTC)
        date_used = today_utc.strftime("%Y-%m-%d")
    else:
        date_used = args.date

    if (args.command == 'lunar'):
        # Render lunar data
        phase_name, fraction = get_moon_phase(date_used)
        match args.type:
            case 'image':
                render_lunar_phase(phase_name, char=args.char)
            case 'summary':
                render_lunar_summary(phase_name, fraction, date_used)
            case 'combined':
                render_lunar_summary(phase_name, fraction, date_used)
                render_lunar_phase(phase_name, char=args.char)

    elif (args.command == 'solar'):
        # Render solar data
        daily_profile = get_daily_solar_profile(args.lon, args.lat, date_used)
        daily_summary = get_daily_solar_summary(args.lon, args.lat, date_used)
        render_solar_summary(daily_summary, args.lon, args.lat, date_used)
        match args.type:
            case 'chart':
                render_solar_chart(daily_profile, args.rows, args.data_char, args.current_char)
            case 'table':
                render_solar_table(daily_profile)

if __name__ == "__main__":
    main()