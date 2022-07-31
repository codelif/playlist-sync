import os
import googleapiclient.discovery
from youtube_title_parse import get_artist_title as extract


def fetch_songs(playlist_id:str) -> dict:
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ["YOUTUBE_TOKEN"] # fetch api key from environment variable. You can substitute this with your api key if you are running this locally. To get yours visit: https://developers.google.com/youtube/v3/getting-started#before-you-start. It's free for 10,000 request per month. And you can get one without credit card.

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

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
                'title': title,
                'artist': artist.replace(" - Topic", ""), # special case
                'index': (i['snippet']['position']+1)
            }
            playlist.append(video)
        
        # requesting next page
        request = playlist_items_api.list_next(request, response)

    return playlist


def fetch_playlist(playlist_IDs: list) -> list[dict]:
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ["YOUTUBE_TOKEN"] # fetch api key from environment variable. You can substitute this with your api key if you are running this locally. To get yours visit: https://developers.google.com/youtube/v3/getting-started#before-you-start. It's free for 10,000 request per month. And you can get one without credit card.

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
   
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

