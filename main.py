'''A CLI program for importing One Pace episodes into Plex'''
import argparse
from argparse import ArgumentParser
from modules.plex import run as plex_run

def create_parsers() -> ArgumentParser:
    '''Create the parsers for the CLI'''
    parser = argparse.ArgumentParser(
        prog='onepace-plex-importer',
        description='A command-line assistant for importing One Pace episodes into Plex'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    parser_post_metadata = subparsers.add_parser(
        'post-metadata', help='Upload metadata for One Piece to Plex (titles, descriptions, etc.)')
    parser_post_metadata.add_argument(
        '--plex-token', required=True,
        help='Your Plex token \
        (see https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)')
    parser_post_metadata.add_argument(
        '--plex-host', required=True, help='Your Plex host \
            (e.g. http://localhost:32400, https://plex.mydomain.com, etc.)')
    parser_post_metadata.add_argument('--plex-library', required=False,
                                      help='The name of the Plex library that contains \
                                        One Piece/One Pace episodes \
                                        (default: "TV")', default='TV')
    parser_post_metadata.add_argument('--one-piece-show-name', required=False,
                                      help='The name of the One Piece show in Plex \
                                        (if you have elected to change it)', default='One Piece')
    parser_post_metadata.add_argument('--change-show-name', required=False, default=False,
                                      help='Should the show name be changed to \
                                        "One Pace" in Plex? (default: False)', action='store_true')
    parser_create_folders = subparsers.add_parser(
        'create-folders', help='Create folders for One Pace episodes for the Plex library')
    parser_create_folders.add_argument('--source-dir', required=True,
                                       help='The directory containing the initial downloaded \
                                        One Pace episodes from onepace.net \
                                        Warning: Do NOT change the original file names of \
                                        the downloaded episodes')
    parser_create_folders.add_argument('--target-dir', required=True,
                                       help='The directory to create the folders in')
    return parser


def main():
    '''Main function'''
    parser = create_parsers()
    args = parser.parse_args()
    if args.command == 'post-metadata':
        plex_run(args)
    elif args.command == 'create-folders':
        pass
    else:
        parser.print_help()


main()
