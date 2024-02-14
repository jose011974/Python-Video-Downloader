import os

from pathlib import Path

os.chdir(Path(__file__).parent.resolve())

folder = os.getcwd() + r'/output'
flist0 = os.listdir(folder)
file_types = (".jpeg", ".png", ".gif", ".mp4", ".webm")

# A comprehension list that filters and constructs a new list (filesnames) 
# based on certian conditions applied to an existing list (flist0)

# ChatGPT was used to help with the explanation of this.
# Credit to the original source code: https://github.com/PySimpleGUI/PySimpleGUI/blob/1fa911cafee687ef50e024b580d5351c398ef7d1/DemoPrograms/Demo_Img_Viewer.py#L36

# For each element in f, check if f is a valid file by:
    # 1. Checking if the joined path (folder + f) points to a file
    # 2. The lowercase version of the file ends with any specified extension in file_types

filenames = [
    f
    for f in flist0
        if os.path.isfile(
            os.path.join(folder, f))
            and
            f.lower().endswith(file_types)
]

print(filenames)