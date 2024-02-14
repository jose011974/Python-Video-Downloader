import platform
import os
import blessed
import shutil

from pathlib import Path

os.chdir(Path(__file__).parent.resolve()) 

term = blessed.Terminal()
W,H = term.width, term.height
media_path = str(Path(os.getcwd() + r'/test'))

url_text_path = ""


def clear():
    # Clear the screen

    command = 'clear' # Unix
    if platform.system() == "Windows": command = 'cls' # Windows
    os.system(command)

    title()

def title():

    # Create a title bar based on the console window size

    title = "[Python Video Downloader.py v1.05 - 'The best downloader in town!']"
    consoleSize = shutil.get_terminal_size()
    col = int(consoleSize[0])-len(title)

    for x in range(0, int(col/2)):
        print("-", end = '')

    print(title, end = '')

    for x in range(0, int(col/2)):
        print("-", end='')

    print("\n")

clear()

print(term.brown1 + "ERROR 5:" + term.normal, "The URL could not be authenticated as a valid session was not found.\n\n" +
                "You will need to have Chrome or Firefox installed in their default location, signed into the respective website,",
                 "and try again. We apologize for any inconvenience.")

input()