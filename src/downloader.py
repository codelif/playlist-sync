from __future__ import unicode_literals
import yt_dlp as youtube_dl
import os


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'downloading':
        # print(os.path.getsize(file_name)/1024+'KB / '+size+' KB downloaded!', end='\r')
        print ("downloading "  + str(round(float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1))+"%", end='\r')
    if d['status'] == 'finished':
        print('Downloaded \'%s\', converting ...' % os.path.basename(d['filename']))


def downloader(videos, playlist, output_folder):
    for video in videos:
        ydl_opts = {
            'writethumbnail': True,
            'format': 'bestaudio/best',
            'outtmpl': f'{playlist} (Youtube)/{video["title"]} - {video["artist"]}.%(ext)s',
            'paths': {'temp':'/tmp', 'home': output_folder},
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
            except youtube_dl.utils.ExtractorError as e: # skip if this error is raised. It is usually raised when the video has DRM or not available in your country.
                print("Error occured while trying to download '%s'. Skipping..." % f"https://youtu.be/{video['id']}")
                continue
                
            

            
if __name__ == "__main__":
    from fetch import fetch_playlist, fetch_songs

    playlist = fetch_playlist(["PLrG0epTyFPvyJw_a-cFu3Xxp9ertchISl"])
    videos = fetch_songs(playlist[0]["id"])

    downloader(videos, playlist[0]["title"], "~/Music_Test")

