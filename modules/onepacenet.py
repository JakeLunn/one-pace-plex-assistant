"""Module for calling the onepace.net API to retrieve episode information"""
import re
import requests

BUILD_ID_REGEX = re.compile(r"\"buildId\".+?\"(?P<BuildId>.+?)\"")


class TranslationNotFoundException(Exception):
    """Exception for when a translation is not found"""


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
