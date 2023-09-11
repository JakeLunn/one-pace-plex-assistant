"""A command-line application for assisting with importing One Pace episodes into Plex"""
import argparse
from argparse import ArgumentParser
from modules.plex import run as plex_run
from modules.local_media import run as media_run

SETUP_PLEX_COMMAND = "setup-plex"
SETUP_MEDIA_COMMAND = "setup-media"


def add_plex_parser(subparsers):
    """Add the plex parser to the subparsers"""
    subparser = subparsers.add_parser(
        SETUP_PLEX_COMMAND,
        help="Upload metadata for One Piece to Plex (titles, descriptions, etc.)",
    )
    subparser.add_argument(
        "-t", "--plex-token",
        required=True,
        help="Your Plex token \
        (see https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)",
    )
    subparser.add_argument(
        "-ph", "--plex-host",
        required=True,
        help="Your Plex host \
            (e.g. http://localhost:32400, https://plex.mydomain.com, etc.)",
    )
    subparser.add_argument(
        "-l", "--plex-library",
        required=False,
        help='The name of the Plex library that contains \
                                        One Piece/One Pace episodes \
                                        (default: "TV")',
        default="TV",
    )
    subparser.add_argument(
        "--one-piece-show-name",
        required=False,
        help="The name of the One Piece show in Plex \
                                        (if you have elected to change it)",
        default="One Piece",
    )
    subparser.add_argument(
        "--change-show-name",
        required=False,
        default=False,
        help='Should the show name be changed to \
                                        "One Pace" in Plex? (default: False)',
        action="store_true",
    )


def add_media_parser(subparsers):
    """Add the media parser to the subparsers"""
    subparser = subparsers.add_parser(
        SETUP_MEDIA_COMMAND,
        help="Create folders for One Pace episodes for the Plex library",
    )
    subparser.add_argument(
        "-s", "--source-dir",
        required=True,
        help="The directory containing the initial downloaded \
                                        One Pace episodes from onepace.net \
                                        Warning: Do NOT change the original file names of \
                                        the downloaded episodes",
    )
    subparser.add_argument(
        "-t", "--target-dir", required=True, help="The directory to create the folders in"
    )


def create_parsers() -> ArgumentParser:
    """Create the parsers for the command-line application"""
    parser = argparse.ArgumentParser(
        prog="onepace-plex-importer",
        description="A command-line assistant for importing One Pace episodes into Plex",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    add_plex_parser(subparsers)
    add_media_parser(subparsers)
    return parser


def main():
    """Main function"""
    parser = create_parsers()
    args = parser.parse_args()
    if args.command == SETUP_PLEX_COMMAND:
        plex_run(args)
    elif args.command == SETUP_MEDIA_COMMAND:
        media_run(args)
    else:
        parser.print_help()


main()
