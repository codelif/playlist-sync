#!/bin/sh

DIRECTORY="$(dirname $(readlink -f $0))"
LAUNCHER="#!/usr/bin/env python3\nimport sys\nsys.path.insert(1, '$DIRECTORY')\nfrom ypsync import main\nif __name__ == '__main__':\n\tsys.exit(main())"
LOCAL=~/.local/bin
mkdir -p $LOCAL
echo -e $LAUNCHER > $LOCAL/ypsync
chmod +x $LOCAL/ypsync
mkdir -p ~/.ypsync
echo -e "ypsync successfully installed. Next steps:\n\t1. Make sure ~/.local/bin is in PATH environment variable.\n\t2. Add playlists in '~/.ypsync/yplaylists' to start syncing. \n\t3. Add API key in environment variable 'YOUTUBE_TOKEN' or edit ypsync.py and hardcode it.\n\t4. If you ever move the folder where this script resides then you have to re-run this script."

