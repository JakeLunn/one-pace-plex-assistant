"""Module for calling the onepace.net API to retrieve episode information"""
import requests
from requests import RequestException


def get_arcs() -> list:
    """Get the One Pace episodes from the API"""
    response = requests.get(
        "https://onepace.net/_next/data/3ivGuB-QWFxGji410gfuK/en/watch.json", timeout=10
    )
    arcs = response.json()["pageProps"]["arcs"]
    return arcs


def get_image(url: str):
    """Download Image from the One Pace Servers"""
    response = requests.get(
        f"https://onepace.net/_next/image?url={url}&w=828&q=75", timeout=30
    )
    response.raise_for_status()
    return response.content


def extract_title(media) -> str:
    """Extract the title from the One Pace episode"""
    for translation in media["translations"]:
        if translation["language_code"] == "en":
            return translation["title"]
    return ""


def extract_description(media) -> str:
    """Extract the description from the One Pace episode"""
    for translation in media["translations"]:
        if translation["language_code"] == "en":
            return translation["description"]
    return ""
