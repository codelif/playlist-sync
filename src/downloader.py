from __future__ import unicode_literals
from mutagen.easyid3 import EasyID3
import yt_dlp as youtube_dl
import os


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def update_metadata(media_file: str, title: str, artist: str):
    audio = EasyID3(media_file)
    audio['title'] = title
    audio['artist'] = artist
    audio.save()


def my_hook(d):
    if d['status'] == 'downloading':
        # print(os.path.getsize(file_name)/1024+'KB / '+size+' KB downloaded!', end='\r')
        print ("downloading "  + str(round(float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1))+"%", end='\r')
    if d['status'] == 'finished':
        print('Downloaded \'%s\', converting ...' % os.path.basename(d['filename']))


def downloader(videos, playlist, output_folder):
    for video in videos:
        filename = f'{output_folder}/{playlist["title"]} (Youtube)/{video["artist"]} - {video["title"]}.mp3'
        ydl_opts = {
            'writethumbnail': True,
            'format': 'bestaudio/best',
            'outtmpl': f'{playlist["title"]} (Youtube)/{video["artist"]} - {video["title"]}.%(ext)s',
            'paths': {'temp':'~/.tmp', 'home': output_folder},
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {'key': 'FFmpegMetadata', 'add_metadata': 'True'},
            {
                'key': 'EmbedThumbnail',
                'already_have_thumbnail': False
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([video['id']])
                update_metadata(filename, video['title'], video['artist']) # update with more refined metadata
                
            except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError) as e: # skip if this error is raised. It is usually raised when the video has DRM or not available in your country.
                print("Error occured while trying to download '%s'. Skipping..." % f"https://youtu.be/{video['id']}")
                continue
                
