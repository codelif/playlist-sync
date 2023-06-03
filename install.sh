#!/bin/sh

LOCAL=~/.local/bin
DIRECTORY="$(dirname "$(readlink -f "$0")")"

LAUNCHER="#!/usr/bin/env python3
import sys
sys.path.insert(1, '$DIRECTORY')
from ypsync import main
if __name__ == '__main__':
    sys.exit(main())"


if [ "$1" = "-v" ]
then
    echo "[INFO] Setting up launcher scripts..."
fi
mkdir -p $LOCAL
echo "$LAUNCHER" > $LOCAL/ypsync
chmod +x $LOCAL/ypsync

if [ "$1" = "-v" ]
then
    echo "[INFO] Setting up config folders..."
fi
mkdir -p ~/.config/ypsync

if command -v pip > /dev/null 2>&1
then
    echo "[INFO] Installing requirements... (requires pip)"
    
    if [ "$1" = "-v" ]
    then 
        pip install -r "$DIRECTORY/requirements.txt"
    else
        pip install -r "$DIRECTORY/requirements.txt" > /dev/null 2>&1
    fi
else
    echo "[ERROR] Please install pip and add it to PATH"
    exit 1
fi


# Greeting
cat << EOF


ypsync successfully installed. Please ensure ffmpeg is installed for youtube-dl to work.
    Next steps:
    1. Make sure ~/.local/bin is in PATH environment variable.
    2. Add playlists in '~/.config/ypsync/config.ini' to start syncing.
    3. If you ever move the folder where this script resides then you have to re-run this script.
EOF

