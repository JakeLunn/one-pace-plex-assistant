"""Module for calling the onepace.net API to retrieve episode information"""
import re
import requests
from enum import Enum

BUILD_ID_REGEX = re.compile(r"\"buildId\".+?\"(?P<BuildId>.+?)\"")

MediaType = Enum('MediaType', ['ARC', 'EPISODE'])

class TranslationNotFoundException(Exception):
    """Exception for when a translation is not found"""

def __generate_cover_url(media_type: MediaType, title: str):
    """Generate a cover url given a title"""
    titlef = title
    titlef = titlef.replace(' ', '-')
    titlef = titlef.replace('\'', '')
    media_area = 'episodes'
    if media_type == MediaType.ARC:
        titlef = titlef + "-arc"
        media_area = 'arcs'
    cover_url = f"/images/{media_area}/cover-{titlef}.jpg".lower()
    return cover_url

def get_build() -> str:
    """Get the Build Id from onepace.net"""
    response = requests.get("https://onepace.net", timeout=10)
    response.raise_for_status()
    return BUILD_ID_REGEX.search(response.text).group("BuildId")


def get_arcs() -> list:
    """Get the One Pace episodes from the API"""
    build_id = get_build()
    response = requests.get(
        f"https://onepace.net/_next/data/{build_id}/en/watch.json", timeout=10
    )
    response.raise_for_status()
    arcs = response.json()["pageProps"]["arcs"]
    return arcs


def get_image(media_type: MediaType, title: str) -> bytes:
    """Download Image from the One Pace Servers"""
    url = __generate_cover_url(media_type, title)
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
