"""
src/mpd_hot_reload.py - Updates MPD Library with minimal interruption.

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

from mpd import MPDClient


def get_client() -> MPDClient:
    client = MPDClient()
    client.connect("localhost", 6600)
    
    return client


def hotreload_mpd(client: MPDClient):
    # save current settings in buffer.
    status = client.status()
    curr = client.currentsong()
    
    # analyse MPD settings to take the appropriate route.
    
    playlist, song = curr["file"].split("/")
    
    
    client.update()
    client.clear()
    client.add(playlist)
    
    index = 0 
    for i,v in enumerate(client.playlist()):
        if song in v:
            index = i

    client.play()
    if status["state"] == 'pause':
        client.pause()
                            #remove buffer from exact value.
    client.seek(index, round(float(status['elapsed']) - 0.25, 3)) # 
    
    print("Updated MPD! Could you tell?")
    

if __name__ == "__main__":
    hotreload_mpd(get_client())
    
