"""Plex module for One Pace Plex Importer"""
from argparse import Namespace
from plexapi.server import PlexServer
from modules.onepacenet import get_arcs, extract_description, extract_title

def process_season(season):
    """Process a Plex season with One Pace metadata"""
    print(f"Processing season: {season.title} ({season.ratingKey})")
    onepace_arcs = get_arcs()
    matching_arc = next(
        (arc for arc in onepace_arcs if arc["part"] == season.seasonNumber), None
    )
    if matching_arc is None:
        print(f"Could not find matching season for {season.title}")
        return
    arc_title = extract_title(matching_arc)
    arc_description = extract_description(matching_arc)
    formatted_arc_title = f"{matching_arc['part']:02d} - {arc_title}"
    if season.title != formatted_arc_title:
        print(f"Changing season title {season.title} -> {formatted_arc_title}")
        season.edit(**{"title.value": formatted_arc_title})
    if season.summary != arc_description:
        print(f"Changing season description -> {arc_description}")
        season.edit(**{"summary.value": arc_description})
    for episode in season.episodes():
        process_episode(matching_arc, episode)


def process_episode(arc, episode):
    """Process a Plex episode with One Pace metadata"""
    print(f"Processing episode: {episode.title} ({episode.ratingKey})")
    matching_onepace_episode = next(
        (
            onepace_episode
            for onepace_episode in arc["episodes"]
            if onepace_episode["part"] == episode.episodeNumber
        ),
        None,
    )
    if matching_onepace_episode is None:
        print(f"Could not find matching episode for {episode.title}")
        return
    onepace_title = extract_title(matching_onepace_episode)
    onepace_description = extract_description(matching_onepace_episode)
    if episode.title != onepace_title:
        print(f"Changing episode title {episode.title} -> {onepace_title}")
        episode.edit(**{"title.value": onepace_title})
    if episode.summary != onepace_description:
        print(f"Changing episode description -> {onepace_description}")
        episode.edit(**{"summary.value": onepace_description})


def run(args: Namespace) -> None:
    """Run the Plex module"""
    plex = PlexServer(args.plex_host, args.plex_token)
    show = next(iter(plex.library.section(args.plex_library).searchShows(
            title=args.one_piece_show_name)),
            None,
        )
    if show is None:
        print(f"Could not find show {args.one_piece_show_name}")
        return
    print(f"Found show: {show.title} ({show.ratingKey})")
    if args.change_show_name and show.title != "One Pace":
        print("Changing show name to One Pace")
        show.edit(**{"title.value": "One Pace"})
    for season in show.seasons():
        process_season(season)
