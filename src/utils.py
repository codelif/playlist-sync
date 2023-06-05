"""
src/utils.py - Miscellaneous functions to be used as a library.

Copyright (C) 2022  Harsh Sharma  <goharsh007@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import ffmpeg
import os
import shutil
import json
import datetime
import sys


def get_video_id(media_file: str) -> str:
    return ffmpeg.probe(media_file)['format']['tags']['purl'].split("=")[-1]


def ensure_folder(path: str):
    if os.path.exists(path):
        if not os.path.isdir(path):
            print("Given path is not a directory")
            sys.exit(1)
        return
    else:
        os.mkdir(path)


def ensure_sync_file(path: str):
    if not os.path.exists(path):
        try:
            os.mkdir(os.path.dirname(path))
        except FileExistsError:
            print("Folder exists already. Creating File..")
        finally:
            with open(path, "w+") as f:
                f.write("{\"app\":\"ypsync\"}\n")


def fetch_sync_file(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def playlist_file(path: str) -> list[str]:
    playlists = []
    if os.path.exists(path):
        with open(path) as f:
            for line in f.readlines():
                if "#" not in line:
                    playlists.append(line.strip())
    else:
        print("ERROR: Playlist File not found. Please create a playlist file at '%s' and enter the playlist IDs to sync." % path)
        sys.exit(1)

    if len(playlists) == 0:
        print("ERROR: Playlist File is empty. Enter a playlist ID in playlist file at '%s' to continue." % path)
        sys.exit(1)

    return playlists


def update_sync_file(obj: dict, path: str):
    with open(path, "w+") as f:
        json.dump(obj, f, sort_keys=True, indent=4)


def delete_playlist(music_dir: str, playlist_title: str):
    try:
        # try deleting playlist
        shutil.rmtree(os.path.join(music_dir, f"{playlist_title} (Youtube)"))
    except FileNotFoundError:
        pass  # playlist does not exist


def dprint(obj):
    # stands for debug print. prints the obj and its type to the terminal.
    print(obj, type(obj), sep=" - ")


def log_string(prefix="", suffix=""):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f"{prefix}{timestamp}{suffix}"

