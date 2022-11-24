from configparser import ConfigParser, DuplicateOptionError, NoOptionError, NoSectionError


class InvalidPlaylist(Exception): pass
class NoPlaylists(Exception): pass


def validate_config(path:str):
    buffer = ConfigParser()
    buffer.read(path)
    
    config = {}
    try:
        config.update({"key": buffer.get('settings', 'api-key')})
    except (NoOptionError, NoSectionError):
        print("ERROR: No API Key in config.ini. Please provide a Youtube API Key in config.ini. For more info: Read the DOCS on how to setup ypsync.")
        exit()
    
    p = {}
    try:
        playlists = list(buffer.items('playlists'))
    except DuplicateOptionError:
        print("ERROR: Check config.ini file for duplicate options in the playlists section. For more info: Read the DOCS on how to setup ypsync.")
        exit()
    except NoSectionError:
        print("ERROR: Playlists section has not been setup properly. For more info: Read the DOCS on how to setup ypsync.")
    
    try:
        if not playlists:
            raise NoPlaylists("No playlists in config.ini")
        for playlist in playlists:
            index = int(playlist[0].split('-')[-1])
            play_id = playlist[1]
            if len(play_id) != 34:
                raise InvalidPlaylist("Not 34-characters in length")
            p.update({index:play_id})
        if len(set(p.values())) != len(p.values()):
            print("WARN: Some of the playlists in config.ini are duplicates. Please ensure there are no duplicates.")
            oldp = p
            p = {}
            for i,v in oldp.items():
                if v not in list(p.values()):
                    p.update({i:v})
            
            
        config.update({"playlists":p})
    except ValueError:
        print("ERROR: Check if you have properly setup playlists. Playlists should be in format 'playlist-{index} = {playlist-id}'. For more info: Read the DOCS on how to setup ypsync..")
        exit()
    except InvalidPlaylist:
        print("ERROR: One of the playlists in config.ini is invalid. Please ensure that you have entered a valid 34-character Youtube Playlist. For more info: Read the DOCS on how to setup ypsync..")
        exit()
    except NoPlaylists:
        print("No Playlists in config.ini. Please add a playlist ID in config.ini to start. For more info: Read the DOCS on how to setup ypsync..")
        exit()
    
    
    return config


def get_api_key(config: dict):
    return config["key"]

def get_playlists(config:dict):
    return list(config["playlists"].values())







