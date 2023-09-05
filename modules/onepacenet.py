"""Module for calling the onepace.net API to retrieve episode information"""
import requests


class TranslationNotFoundException(Exception):
    """Exception for when a translation is not found"""


def get_arcs() -> list:
    """Get the One Pace episodes from the API"""
    response = requests.get(
        "https://onepace.net/_next/data/3ivGuB-QWFxGji410gfuK/en/watch.json", timeout=10
    )
    response.raise_for_status()
    arcs = response.json()["pageProps"]["arcs"]
    return arcs


def get_image(url: str) -> bytes:
    """Download Image from the One Pace Servers"""
    response = requests.get(
        f"https://onepace.net/_next/image?url={url}&w=828&q=75", timeout=30
    )
    response.raise_for_status()
    return response.content

def extract_from_translations(media, language_code: str, key: str) -> str:
    """Extract the title from the One Pace episode"""
    translation = next(
        (
            translation
            for translation in media["translations"]
            if translation["language_code"] == language_code
        ),
        None,
    )
    if translation is None:
        raise TranslationNotFoundException(f"No {language_code} translation found")
    return translation[key]

def extract_title(media) -> str:
    """Extract the title from the One Pace episode"""
    return extract_from_translations(media, "en", "title")

def extract_description(media) -> str:
    """Extract the description from the One Pace episode"""
    return extract_from_translations(media, "en", "description")
