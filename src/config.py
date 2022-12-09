"""
src/config.py - Managing configuration file programmatically.

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







