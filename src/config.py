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


class Parser:
    
    def __init__(self, config_file:str, comment_char:str='#') -> None:
        """Parse config files

        Args:
            config_file (str): Config file path
            comment_char (str, optional): Comment character to ignore. Defaults to '#'.
        """        
        self.COMMENT_TOKEN = comment_char

        with open(config_file) as f:
            raw_config = f.read()
        self.raw_config_lines = self.__split_lines_and_whitespace(raw_config)
        

    def __split_lines_and_whitespace(self, string) -> list[str]:
        rc_lines = []
        for i in string.splitlines():
            if i:
                rc_lines.append(i)
        return rc_lines
    

    def get_sections(self) -> dict[str, tuple]:
        sections = {}

        cur_section = ['', -1]
        for i,line in enumerate(self.raw_config_lines):
            line = self.__remove_comments(line)
            if line.startswith('[') and line.endswith(']'):

                if cur_section[0]:
                    entries = self.raw_config_lines[cur_section[1]+1:i]
                    sections.update({cur_section[0]: self.__parse_entries(entries)})
                
                cur_section = [line.strip("[]"), i]

            is_last_line = i+1 == len(self.raw_config_lines)
            if is_last_line and cur_section[0]:
                entries = self.raw_config_lines[cur_section[1]+1:i+1]
                sections.update({cur_section[0]: self.__parse_entries(entries)})
        
        return sections


    def __parse_entries(self, entries: list[str]) -> tuple[dict, list]:

        assignments = {}
        flags = []
        for line in entries:
            if line.startswith(self.COMMENT_TOKEN):
                continue
            
            splited = self.__remove_comments(line).split('=')
                    
            if len(splited) == 1:
                flags.append(splited[0])
            elif len(splited) == 2:
                assignments.update({splited[0]: splited[1]})
            else:
                pass #invalid format

        return (assignments, flags)

    def __remove_comments(self, line:str) -> str:
        for i,v in enumerate(line):
            if v == self.COMMENT_TOKEN:
                line = line[:i]

        return line.strip()


class InvalidPlaylist(Exception): pass
class NoPlaylists(Exception): pass


def validate_config(path:str):
    buffer = Parser(path).get_sections()
    
    try:
        playlists = buffer["playlists"][1]
        if not playlists:
            raise NoPlaylists("No playlists in config.ini")
    except KeyError:
        print("ERROR: Playlists section has not been setup properly. For more info: Read the DOCS on how to setup ypsync.")
        exit(1)        
    except NoPlaylists:
        print("No Playlists in config.ini. Please add a playlist ID in config.ini to start. For more info: Read the DOCS on how to setup ypsync..")
        exit(1)
    
    
    return playlists









