"""
src/fetch.py - Fetch Playlist and Video Information with YouTube API.

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

import os
import googleapiclient.discovery
from youtube_title_parse import get_artist_title as extract


def fetch_songs(playlist_id:str, dev_key:str) -> dict:
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = dev_key)

    playlist_items_api = youtube.playlistItems()
    request = playlist_items_api.list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=playlist_id
    )

    playlist = [] # initalize an empty list to store only relevant information. i.e. video title, video id 

    # iteratively fetch all items inside the playlist due to pagination. For more info see: https://googleapis.github.io/google-api-python-client/docs/pagination.html
    while request is not None:
        response = request.execute()
        
        # collecting relevant information in a dictionary and appending it in the playlist list
        for i in (response["items"]):
            if i['snippet']['title'].lower() in ["private video", "deleted video"]: # Check for private/deleted videos
                continue 
            try:
                # Parse the title to extract only the artist and title.
                artist, title = extract(i['snippet']['title'])
            except TypeError:
                # Fallback if youtube_title_parse is not able to parse a title.
                artist, title = (i['snippet']['videoOwnerChannelTitle'], i['snippet']['title'])
            
            video = {
                'id':  i['contentDetails']['videoId'],
                'title': title.replace("/", "-"), # special case
                'artist': artist.replace(" - Topic", ""), # special case
                'index': (i['snippet']['position']+1)
            }
            playlist.append(video)
        
        # requesting next page
        request = playlist_items_api.list_next(request, response)

    return playlist


def fetch_playlist(playlist_IDs: list, dev_key:str) -> list[dict]:
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = dev_key)
   
    playlist_api = youtube.playlists()
    request = playlist_api.list(
        part="snippet,contentDetails",
        maxResults=50,
        id=",".join(playlist_IDs)
    )

    playlists = [] # initalize an empty list to store only relevant information. i.e. video title, video id 

    # iteratively fetch all items inside the playlist due to pagination. For more info see: https://googleapis.github.io/google-api-python-client/docs/pagination.html
    while request is not None:
        response = request.execute()
        
        # collecting relevant information in a dictionary and appending it in the playlist list
        for i in (response["items"]):
            playlist = {
                'id':  i['id'],
                'title': i['snippet']['localized']['title'],
                'count': i['contentDetails']['itemCount']
            }
            playlists.append(playlist)
        
        # requesting next page
        request = playlist_api.list_next(request, response)

    return playlists

