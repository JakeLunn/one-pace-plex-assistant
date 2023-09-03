'''Plex module for One Pace Plex Importer'''
import sys
from dataclasses import dataclass
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from argparse import Namespace
import requests


@dataclass
class Library:
    '''Plex library data class'''
    key: str
    title: str


@dataclass
class Show:
    '''Plex show data class'''
    rating_key: str
    title: str


class PlexService:
    '''Plex class for One Pace Plex Importer'''

    def __init__(self, plex_token: str, plex_host: str, plex_library: str):
        self.plex_token = plex_token
        self.plex_host = plex_host
        self.plex_library = plex_library

    def post_metadata(self,
                      show_name: str,
                      change_show_name: bool) -> None:
        '''Post metadata to Plex'''
        return None

    def get_libraries(self) -> list[Library]:
        '''Get the Plex library sections'''
        response = requests.get(
            f'{self.plex_host}/library/sections?includeMeta=1&X-Plex-Token={self.plex_token}', timeout=10, headers={"Accept": "application/json"})
        if response.status_code == 401:
            print('Invalid Plex token')
            return None
        print(response.text)
        data = response.json()
        libraries = [Library(**{k: v for k, v in section.items() if k in ['key', 'title']})
                     for section in data['MediaContainer']['Directory']]
        return libraries

    def get_shows(self, library: Library) -> list[Show]:
        '''Get the show from the Plex library'''
        response = requests.get(
            f'{self.plex_host}/library/sections/{library.key}/all\
                ?type=2\
                &includeMeta=1\
                &X-Plex-Token={self.plex_token}',
            timeout=10,
            headers={"Accept": "application/json"})
        if response.status_code == 401:
            print('Invalid Plex token')
            return None
        print(response.text)
        data = response.json()
        shows = [Show(**{k: v for k, v in show.items() if k in ['ratingKey', 'title']})
                 for show in data['MediaContainer']['Metadata']]

        return shows


def __get_library(plex_service: PlexService, library_name: str) -> Library:
    libraries = plex_service.get_libraries()
    if libraries is None:
        print('Failed to get Plex libraries')
        sys.exit(1)
    libraries = [section for section
                 in libraries
                 if section.title == library_name]
    if len(libraries) == 0:
        print(f'Failed to find Plex library: {library_name}')
        sys.exit(1)
    library = libraries[0]
    return library


def __get_show(plex_service: PlexService, library: Library, show_name: str) -> Show:
    shows = plex_service.get_shows(library)

    shows = [show for show in shows if show.title == show_name]

    if len(shows) == 0:
        print(f'Failed to find show with name: {show_name}')
        sys.exit(1)

    show = shows[0]

    return show


def run(args: Namespace) -> None:
    '''Run the Plex module'''
    plex_service = PlexService(
        args.plex_token, args.plex_host, args.plex_library)

    library = __get_library(plex_service, args.plex_library)
    print(f"Found library: {library.title} ({library.key})")

    show = __get_show(plex_service, library, args.one_piece_show_name)
    print(f"Found show: {show.title} ({show.rating_key})")
