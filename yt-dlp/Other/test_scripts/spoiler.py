import os

from pathlib import Path

os.chdir(Path(__file__).parent.resolve())
folder = Path(os.getcwd() + r'/test')
filelist = os.listdir(folder)

file_types = (".jpeg", ".png", ".gif", ".mp4", ".webm")

filenames = [
f
for f in filelist
    if os.path.isfile(
        os.path.join(folder, f))
        and
        f.lower().endswith(file_types)
]

for file in filenames:
    if file.startswith("SPOILER_"):
        print(file, "E")
    else:
        print(file, "F")