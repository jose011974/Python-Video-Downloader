import platform
import os
import shutil
import blessed

def clear():
    # Clear the screen

    command = 'clear' # Unix
    if platform.system() == "Windows": command = 'cls' # Windows
    os.system(command)

    title()

def title():

    # Create a title bar based on the console window size

    title = "[Python Video Downloader.py v1.06 - 'The best downloader in town!']"
    consoleSize = shutil.get_terminal_size()
    col = int(consoleSize[0])-len(title)

    for x in range(0, int(col/2)):
        print("-", end = '')

    print(title, end = '')

    for x in range(0, int(col/2)):
        print("-", end='')

    print("\n")

clear()

text = [""]