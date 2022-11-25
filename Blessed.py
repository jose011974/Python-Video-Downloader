import fileinput
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import webbrowser

from pathlib import Path

def clear():
    print(term.clear + term.home, end='')

    title()

def countdown(curLocation):
    W = curLocation[1]
    H = curLocation[0]

    i = 3
    while i >= 1:
        print(term.move_xy(W + 1,H) + "(" + str(i) + ")")
        time.sleep(1)
        i = i - 1

def main():
    while True:

        clear()

        print(

            "This script provides the ability to download and compress local/online media. Single and multiple file/URL modes are", end=' ' +
            "avaiable to you.\n\nThe following media types have been tested: " + term.fuchsia + "jpg/jpeg, png, gif, mp4, and webm.\n" + term.normal +
            "\nAny other formats should work, however they have been untested. " + term.orangered + "Proceed at your own risk.\n" + term.normal +
            "\nPlease select the option that works best for you:\n\n"

        )
        
        print("1. Single File")
        print("2. Multiple Files")
        print("3. Single URL")
        print("4. Multiple URLs")
        print("5. Spoil Media")
        print("6. No Spoil Media")
        print("7. Open Unsupported URLs")
        print("8. Help")
        print("9. Exit\n")

        try:
            userInput = int(input(">> "))

            if userInput == 1:
                singleFileConvert()
            elif userInput == 2:
                multipleFileConvert()
            elif userInput == 3: 
                singleURLConvert()
            elif userInput == 4:
                multipleURLConvert()
            elif userInput == 5:
                spoil("spoil")
            elif userInput == 6:
                spoil("no spoil")
            elif userInput == 7:
                counter = 1
                URLCounter = 0
                clear()

                print("All of the URLs in 'Unsupported URLs.txt' will be opened 10 at a time.\n")
                print("Press enter to continue.")
                
                input()

                URLs = list()

                for line in fileinput.FileInput(str(Path(os.path.dirname(__file__) + r'/Unsupported URLs.txt',inplace=1))):
                    if line.rstrip():
                        URLs.append(line)

                if len(URLs) == 0:
                    clear()

                    print("There were no URLs detected.\n")
                    print("Press enter to continue.")
                    input()

                while True:
                    if counter == len(URLs) + 1:
                        break

                    for URL in URLs:
                        clear()

                        print("OPENING", counter, "OUT OF", len(URLs))
                        webbrowser.open(URL, new=0, autoraise=False)
                        time.sleep(0.4)
                        counter = counter + 1
                        URLCounter = URLCounter + 1

                    if URLCounter >= 10:
                        clear()
                        print("Opened 10 URLs. Press enter to continue.")
                        input()
                        URLCounter = 0
                
                clear()
                print("Process complete. Press enter to continue.")

            elif userInput == 8:
                webbrowser.open("https://github.com/jose011974/Download-Compress-Media", new=1)

                clear()

                print("The Github page should have opened. If it did not, please go to https://github.com/jose011974/Download-Compress-Media\n")
                print("Press enter to continue.\n")
                input()

            elif userInput == 9:
                clear()
                print("Exiting...\n")
                sys.exit()
            
            clear()
        except ValueError:
            clear()
            print("You have entered an invalid entry. Please try again.\n")
            continue

def title():

    # Create a title bar based on the console window size

    title = "[MediaConverter.py v1.1.0 - Download and compress media]"
    consoleSize = shutil.get_terminal_size()
    col = int(consoleSize[0])-len(title)

    for x in range(0, int(col/2)):
        print("-", end = '')

    print(title, end = '')

    for x in range(0, int(col/2)):
        print("-", end='')

    print("\n")

def updateDependencies():

    try:
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    except subprocess.CalledProcessError:
        
        import requests

        os.chdir(os.path.dirname(__file__))
        url = "https://bootstrap.pypa.io/get-pip.py"
        response = requests.get(url, allow_redirects=True)

        print("pip, python's package manager, is not installed. I will attempt to download and install it for you.\n\n")

        time.sleep(3)

        if not response.status_code == 200:
            command = 'clear' # Unix
            if platform.system() == "Windows": command = 'cls' # Windows
            os.system(command)

            print("Unable to download pip. Please install pip manually or from https://bootstrap.pypa.io/get-pip.py and execute the script. Aborting.")
            sys.exit()
        try:
            subprocess.check_call([os.system("./get-pip.py")])
            print("I was unable to detect any errors when installing pip. Please restart the script and try again. If you still see this screen, try installing " + 
            "pip manually by opening https://bootstrap.pypa.io/get-pip.py and running the script that downloads. Please note you must be an administrator to " +
            "install pip")

        except:
            command = 'clear' # Unix
            if platform.system() == "Windows": command = 'cls' # Windows
            os.system(command)

            print("An unknown error has occured. Please file a bug report at https://github.com/jose011974/Download-Compress-Media/wiki/Create-a-Bug-Report")

    packages = ["python-magic", "Pillow", "youtube-dl"]

    # Turns out the library needed for magic on Windows has been out of date since 2009. These are up to date and will work with Windows 10.
    if platform.system() == "Windows":
        packages.append("python-magic-bin")

    # Check if the packages are installed
    for p in packages:
        if not p in installed_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", p])
            #Uh oh.
            except Exception as e:
                print(e)
        elif p in installed_packages:
            print(term.move_xy(int(W/2 - 35/2), int(H/2)) + "Loading " + p)
            time.sleep(0.3)

    clear()
    print(term.move_xy(int(W/2 - 35/2), int(H/2)) + "Dependencies loaded.", end='')
    countdown(term.get_location())



updateDependencies()

import distro
import magic
import psutil
import validators
import youtube_dl

term = blessed.Terminal()
W,H = term.width, term.height
distroID = distro.name(pretty=True)
distroID = "Linux Version: " + distroID

while True:
    clear()

    # Creates required files and folders.
    scriptPath = os.path.dirname(__file__)
    URLTextPath = str(Path(scriptPath + r'/URLs.txt'))
    UnsuppURLPath = str(Path(scriptPath + r'/Unsupported URLs.txt'))
    outputPath = str(Path(scriptPath + r'/output'))
    tempPath = str(Path(scriptPath + r'/temp'))

    if not os.path.exists(URLTextPath):
        fp = open(URLTextPath, 'x')
        fp.close()
    if not os.path.exists(UnsuppURLPath):
        fp = open(UnsuppURLPath, 'x')
        fp.close()
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    if not os.path.exists(tempPath):
        os.mkdir(tempPath)

    os.chdir(os.path.dirname(__file__))

    if platform.system() == "Windows":
        ffPath = "C:/ffmpeg/ffmpeg.exe"
        try:
            if not os.path.isfile(ffPath):
                raise Exception()
        except Exception:
            clear()
            print(

                term.move_xy(int(W/2 - 79/2), int(H/2 - 2)) + "You do not have ffmpeg installed. Please make sure it is installed in C:/ffmpeg/" +
                term.move_xy(int(W/2 - 59/2), int(H/2)) + term.bold + term.orangered + "Compression features will not work if you choose to proceed." + term.normal +
                term.move_xy(int(W/2 - 23/2), int(H/2 + 2)) + "Press enter to continue."

            )
            input()

    main()