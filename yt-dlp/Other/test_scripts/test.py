import os

from pathlib import Path

path = '/media/smoke/files/programming stuffs/git projects/python video downloader/yt-dlp/test'

path = str(Path(path))

if os.path.isdir(path):
    print("E")
else:
    print("F")