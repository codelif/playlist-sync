import ffmpeg
import os
import shutil
import json


def get_video_id(media_file: str) -> str:
    return ffmpeg.probe(media_file)['format']['tags']['purl'].split("=")[-1]


def ensure_folder(path: str):
    if os.path.exists(path):
        if not os.path.isdir(path):
            print("Given path is not a directory")
            exit(1)
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
                f.write("{}")

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
        exit(1)

    if len(playlists) == 0:
        print("ERROR: Playlist File is empty. Enter a playlist ID in playlist file at '%s' to continue." % path)
        exit(1)
    
    return playlists


def update_sync_file(obj: dict, path: str):
    with open(path, "w+") as f:
        json.dump(obj, f, sort_keys=True, indent=4)


def delete_playlist(music_dir: str, playlist_title: str):
    try:
        shutil.rmtree(os.path.join(music_dir, f"{playlist_title} (Youtube)")) # try deleting playlist
    except FileNotFoundError:
        pass # playlist does not exist
