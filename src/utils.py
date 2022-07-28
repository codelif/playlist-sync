import ffmpeg
import os
import json

def get_video_id(media_file: str) -> str:
    return ffmpeg.probe(media_file)['format']['tags']['purl'].split("=")[-1]

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



def update_sync_file(obj: dict, path: str):
    with open(path, "w+") as f:
        json.dump(obj, f)



