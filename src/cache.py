import os
import json
from utils import ensure_folder, ensure_sync_file


CACHE_FILE = os.path.expanduser("~/.cache/ypsync")
ensure_folder(CACHE_FILE)


def cache_playlist(name: str, play_id: str):
    path = os.path.join(CACHE_FILE, "playlists.json")
    ensure_sync_file(path)
    
    with open(path, "r+") as f:
        obj = json.load(f)
        print(obj)
        obj[play_id] = name
        f.truncate(0)
        f.seek(0)
        json.dump(obj, f)
        
