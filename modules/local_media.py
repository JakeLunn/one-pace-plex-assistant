"""Process local media files for One Pace episodes"""
import os
import re
import shutil
from typing import List
from dataclasses import dataclass
from argparse import Namespace
from modules.onepacenet import get_arcs, get_image, extract_title

__FILE_MATCH_REGEX = r"\[(One Pace)\]\[(?P<Chapters>.+?)\](?P<Arc>.+?)(?P<Episode>\d{1,2})?\s\[(?P<Quality>\d{3,4}p)\]\[(?P<Hash>.+?)\]\.mkv"
REGEX = re.compile(__FILE_MATCH_REGEX)


@dataclass
class FileInfo:
    """Dataclass for file information"""

    name: str
    full_name: str


class Episode:
    """Represents an Episode of One Pace"""

    title: str
    episode_number: str
    resolution: str
    arc_title: str
    source_file: FileInfo
    target_directory: str
    target_file: FileInfo
    cover_url: str

    def __init__(
        self,
        title: str,
        episode_number: str,
        resolution: str,
        arc_title: str,
        source_file: FileInfo,
        target_directory: str,
        target_file=None,
        cover_url=None,
    ):
        self.title = title
        self.episode_number = episode_number
        self.resolution = resolution
        self.arc_title = arc_title
        self.source_file = source_file
        self.target_directory = target_directory
        file_name = f"One.Pace.{arc_title}.E{episode_number:02d}.{resolution}.mkv"
        self.cover_url = (
            cover_url or f"/images/episodes/cover-{title.replace(' ', '-')}.jpg".lower()
        )
        self.target_file = target_file or FileInfo(
            name=file_name,
            full_name=os.path.join(target_directory, file_name),
        )

    def copy_source_to_destination(self):
        """Copy the source file to the destination"""
        if not os.path.exists(self.target_directory):
            os.makedirs(self.target_directory)
        shutil.copy(self.source_file.full_name, self.target_file.full_name)
        print(f"Copied {self.source_file.name} to {self.target_file.name}")

    def copy_cover_to_destination(self):
        """Copy the cover file from onepace.net to the destination"""
        file_name = f"One.Pace.{self.arc_title}.E{self.episode_number:02d}.{self.resolution}.jpg"
        file_full_name = os.path.join(self.target_directory, file_name)
        if os.path.exists(file_full_name):
            return
        image_data = get_image(self.cover_url)
        with open(file_full_name, "wb") as file:
            file.write(image_data)
        print(f"Copied cover for {self.title} from onepace.net to target directory")


def search_directory(directory) -> List[FileInfo]:
    """Search a directory for One Pace episodes"""
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".mkv"):
                files.append(FileInfo(filename, os.path.join(root, filename)))
    return files


def get_episode(target_dir: str, arcs, file: FileInfo) -> Episode:
    """Get the episode for the provided file"""
    data = REGEX.match(file.name)
    if data is None:
        print(
            f"Skipping {file.name} as it does not match expected name format.\
                \nPlease ensure that the original file name has not been changed!"
        )
        return None
    file_arc = data.group("Arc").strip()
    file_episode = data.group("Episode").strip()
    file_quality = data.group("Quality").strip()
    matching_arc = next((a for a in arcs if extract_title(a) == file_arc), None)
    if matching_arc is None:
        print(f"Could not find matching arc for {file_arc} on onepace.net")
        return None
    print(f"Found matching arc for {file_arc}")
    matching_episode = next(
        (e for e in matching_arc["episodes"] if e["part"] == int(file_episode)),
        None,
    )
    if matching_episode is None:
        print(
            f"Could not find matching episode for {file_arc}/{file_episode} on onepace.net"
        )
        return None
    print(f"Found matching episode for {file_arc}/{file_episode} on onepace.net")
    episode = Episode(
        title=matching_episode["invariant_title"],
        episode_number=matching_episode["part"],
        resolution=file_quality,
        arc_title=extract_title(matching_arc),
        source_file=file,
        target_directory=os.path.join(target_dir, f"Season {matching_arc['part']:02d}"),
    )
    return episode


def copy_arc_cover_to_destination(target_directory: str, arc):
    """Copy the cover file from onepace.net to the destination"""
    part = arc["part"]
    title = arc["invariant_title"]
    file_name = f"Season{part:02d}.jpg"
    target_directory = os.path.join(target_directory, f"Season {part:02d}")
    file_full_name = os.path.join(target_directory, file_name)
    url = f"/images/arcs/cover-{title.replace(' ', '-')}-arc.jpg".lower()
    if os.path.exists(file_full_name):
        return  # Already exists
    image_data = get_image(url)
    with open(file_full_name, "wb") as file:
        file.write(image_data)
    print(f"Copied cover for {title} from onepace.net to target directory")


def run(args: Namespace):
    """Create folders for One Pace episodes for the Plex library"""
    arcs = get_arcs()
    files = search_directory(args.source_dir)
    print(f"Found {len(files)} .mkv files in {args.source_dir}")
    file_arcs = []
    for file in files:
        episode = get_episode(args.target_dir, arcs, file)
        if episode is None:
            continue
        existing_file_arc = next(
            (a for a in file_arcs if extract_title(a) == episode.arc_title), None
        )
        matching_arc = next(
            (a for a in arcs if extract_title(a) == episode.arc_title), None
        )
        if existing_file_arc is None:
            file_arcs.append(matching_arc)
        episode.copy_source_to_destination()
        episode.copy_cover_to_destination()
    for arc in file_arcs:
        copy_arc_cover_to_destination(args.target_dir, arc)