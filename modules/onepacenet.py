'''Module for calling the onepace.net API to retrieve episode information'''
import requests


def get_arcs() -> list:
    '''Get the One Pace episodes from the API'''
    response = requests.get(
        'https://onepace.net/_next/data/3ivGuB-QWFxGji410gfuK/en/watch.json', timeout=10)
    arcs = response.json()['pageProps']['arcs']
    return arcs

def extract_title(media) -> str:
    '''Extract the title from the One Pace episode'''
    for translation in media['translations']:
        if translation['language_code'] == 'en':
            return translation['title']
    return ''

def extract_description(media) -> str:
    '''Extract the description from the One Pace episode'''
    for translation in media['translations']:
        if translation['language_code'] == 'en':
            return translation['description']
    return ''
