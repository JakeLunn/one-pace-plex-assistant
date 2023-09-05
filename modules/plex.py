'''Plex module for One Pace Plex Importer'''
from argparse import Namespace
from plexapi.server import PlexServer
from plexapi.library import ShowSection
from modules.onepacenet import get_arcs, extract_description, extract_title


def __get_show(plex: PlexServer, library: str, show_name: str) -> ShowSection:
    '''Get the show from Plex'''
    return plex.library.section(library).searchShows(title=show_name)[0]


def run(args: Namespace) -> None:
    '''Run the Plex module'''
    plex = PlexServer(args.plex_host, args.plex_token)

    show = __get_show(plex, args.plex_library, args.one_piece_show_name)
    print(f"Found show: {show.title} ({show.ratingKey})")

    if args.change_show_name and show.title != 'One Pace':
        print(f"Changing show name to One Pace")
        show.edit(**{'title.value': 'One Pace'})

    onepace_arcs = get_arcs()

    for season in show.seasons():
        print(f"Processing season: {season.title} ({season.ratingKey})")
        for episode in season.episodes():
            print(f"Processing episode: {episode.title} ({episode.ratingKey})")
            for arc in onepace_arcs:
                if arc['part'] == season.seasonNumber:
                    arc_title = extract_title(arc)
                    arc_description = extract_description(arc)
                    formatted_arc_title = f"{arc['part']:02d} - {arc_title}"
                    if season.title != formatted_arc_title:
                        print(f"Changing season title to {formatted_arc_title}")
                        season.edit(**{'title.value': formatted_arc_title})
                    if season.summary != arc_description:
                        print(
                            f"Changing season description to {arc_description}")
                        season.edit(**{'summary.value': arc_description})
                    for onepace_episode in arc['episodes']:
                        if onepace_episode['part'] == episode.episodeNumber:
                            onepace_description = extract_description(onepace_episode)
                            onepace_title = extract_title(onepace_episode)
                            print(
                                f"Matched season {arc['part']} episode {onepace_episode['part']} -> season {season.title} episode {episode.episodeNumber}")
                            if episode.title != onepace_title:
                                print(
                                    f"Changing episode title to {onepace_title}")
                                episode.edit(
                                    **{'title.value': onepace_title})
                            if episode.summary != onepace_description:
                                print(
                                    f"Changing episode description to {onepace_description}")
                                episode.edit(
                                    **{'summary.value': onepace_description})
                            break
