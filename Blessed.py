# term.cadetblue1
# term.brown1
# term.move_xy(int(W/2 - len(text variable goes here)/2), int(H/2))

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

fileTypes = [".jpeg", ".png", ".gif", ".mp4", ".webm"]

def createOutputFolder(mediaPath):
    mediaPath = str(Path(mediaPath + r'/output/'))
    boolVal = True
    # Create the output folder
    while boolVal:
        try:
            if not os.path.isdir(mediaPath):
                os.mkdir(mediaPath)
                boolVal = False
            else:
                boolVal = False
        
        except PermissionError:
            clear()
            print(term.brown1 + "Error: Missing required permissions. Please make sure you have read and write access to" + term.normal +
            term.cadetblue1 + mediaPath, + term.normal + "in order to create the neccessary folders.\n To try again, type y. If you would" +
            "rather instead use the path the script is located at, type 'n'.\nTo return to the main menu, type 'menu'\n")

            userInput = input(">> ")

            if userInput == "y":
                continue
            elif userInput == "n" or userInput == "menu":
                return

def clear():
    command = 'clear' # Unix
    if platform.system() == "Windows": command = 'cls' # Windows
    os.system(command)

    title()

def configuration():

    updateDependencies()

    global term
    term = blessed.Terminal()
    global W,H
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

def convert(filename, fullFilePath, mediaPath):
    convPath = str(Path(mediaPath + r'/output')) # Output path
    outputFile = str(Path(convPath + r'/' + filename))    # Output file
    inputFile = str(Path(fullFilePath))
    outputFile = str(Path(outputFile))
    ext = os.path.splitext(fullFilePath)
    codec = ""
    
    now = datetime.datetime.now()
    text = "Time the Process started: " + now.strftime('%I:%M %p')
    print(term.move_xy(int(W/2 - len(text)/2), int(H/2 + 4)) + text + "\n")

    createOutputFolder(mediaPath)

    if ext[1] == ".gif" or ext[1] == ".webm" or ext[1] == ".mp4":
        # Setup paths and codec options
        outputFile = convPath + r'/' + os.path.basename(ext[0]) + ".mp4"
        codec = "-c:v libx264 -crf 28 -pix_fmt yuv420p"

        # Begin Conversion
        if platform.system() == "Windows":
            ffPath = "C:/ffmpeg/ffmpeg.exe"
            os.system(ffPath + ' -i "' + inputFile + '" ' + codec + ' "' + outputFile + '"') # Windows
        else:
            os.system("ffmpeg" + ' -i "' + inputFile + '" ' + codec + ' "' + outputFile + '"') # Linux / Other OS

    elif ext[1] == ".jpg":
        im = Image.open(inputFile)
        im.save(outputFile, optimize=True, quality="keep")
    elif ext[1] == ".png":
        im = Image.open(inputFile)
        im.save(outputFile, optimize=True)

    return outputFile

def countdown():
    curLocation = term.get_location()
    W = curLocation[1]
    H = curLocation[0]

    i = 3
    while i >= 0:
        print(term.move_xy(W + 1,H) + "(" + str(i) + ")")
        time.sleep(1)
        i = i - 1

def getFileExtension(filename):

    fileMIME = magic.from_file(filename, mime=True) # Identify the file type
    fileMIME = fileMIME[6:len(fileMIME)]
    fileExt = os.path.splitext(filename)

    return fileExt[1], fileMIME

def getFileSize(file):
    fileSize = os.path.getsize(file) # Get the size of a file
    fileSize = float("{:.2f}".format(fileSize / 1024)) # Convert the output from bytes to MB

    return fileSize

def getListOfFiles(dirName):
    global folderCounter
    folderCounter = 0
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            folderCounter = folderCounter + 1
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            # If the entry is a media file, append it to the list of files
            ext, fileMIME = getFileExtension(fullPath)
            for extension in fileTypes:
                if extension == ext or fileMIME == extension[1:5]:
                        allFiles.append(fullPath)

# The following allows the algorithm to scan subdirectores properly
    if folderCounter != 0:
        folderCounter = folderCounter - 1
        return allFiles
    elif folderCounter == 0:
        return allFiles

def main():
    while True:

        clear()

        print(
            "This script provides the ability to download and compress local/online media. Single and multiple file/URL modes are avaiable to you." +
            "\n\nThe following media types have been tested: " + term.cadetblue1 + "jpg/jpeg, png, gif, mp4, and webm." + term.normal +
            "\n\nAny other formats should work, however they have been untested. " + term.orangered + "\n\nProceed at your own risk. " + 
            "I am not responsible for any loss of data due to neglect. This script is in beta, so bugs WILL be present." + term.normal +
            "\n\nPlease type the option that works best for you and press enter:\n\n" + term.cadetblue1 + "Note: Compression only works on files " +
            "larger than 8 MB, as Discord, a popular messaging service, does not allow regular accounts to upload files larger than 8 MB without paying.\n" + term.normal
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

def multipleFileConvert():

    notFile = True
    mediaPath = str(Path(workingDirectory()))
    
    if mediaPath == "menu":
        clear()
        return
        
    while notFile:

        clear()
        text = "Counting files..."
        print(term.move_xy(int(W/2 - len(text)/2), int(H/2)) + text)

        filePathList = getListOfFiles(mediaPath)
        totalFiles = len(filePathList)
        currentPos = 0
        
        clear()
        text = "Located "
        text2 = " files. Processing..."
        textLength = len(text) + len(str(totalFiles)) + len(text2)
        print(term.move_xy(int(W/2 - textLength/2), int(H/2)) + text + term.cadetblue1 + str(totalFiles) + term.normal + text2, end='')

        countdown()
        clear()

        # Iterate through the files in filePathList and determine if they need compression
        for fullFilePath in filePathList:
            currentPos = currentPos+1
            fullFilePath = str(Path(fullFilePath)).encode('ascii','ignore').decode('ascii')
            filename = os.path.basename(fullFilePath)
            convFile = str(Path(mediaPath + r'/output/' + filename)) # Output file path

            if os.path.isfile(fullFilePath):
                if getFileSize(fullFilePath) > 8192.00:
                        text = "Current file: "
                        text2 = " | " + str(getFileSize(fullFilePath)) + " MB | File " + str(currentPos) + " of " + str(totalFiles) + "\n"
                        print(term.move_xy(int(W/2 - (len(text) + len(filename) + len(text2))/2), int(H/2 - 2)) + text + 
                        term.cadetblue1 + filename + term.normal + text2)
                        # print("\nCompressing " + term.cadetblue1 + filename + term.normal + " | " + str(getFileSize(fullFilePath)) + " MB | File " + str(currentPos) + " of " + str(totalFiles) + "\n")
                        convert(filename, fullFilePath, mediaPath)
                else:
                    shutil.copy(fullFilePath, convFile)
        
        clear()      
        text = "Procedure complete. The files is located at:"
        path = os.path.dirname(fullFilePath)
        text2 = "Note: The files may still be large. If that is the case, segment the files or use a different program/service."
        text3 = "Please press Enter to continue."

        print(
            term.move_xy(int(W/2 - len(text)/2), int(H/2 - 2)) + text +
            term.cadetblue1 + term.move_xy(int(W/2 - (len(path) + 21)/2), int(H/2)) + term.link(path, path) + term.normal + " (CTRL click to open)" +
            term.move_xy(int(W/2 - len(text2)/2), int(H/2 + 2)) + text2, end=''
            )

        countdown()
        print(term.move_xy(int(W/2 - len(text3)/2), int(H/2 + 4)) + text3, end='')
        input()

        clear()
        break

def singleFileConvert():
    clear()
    notLoaded = True

    currentDir = str(Path(os.getcwd()))
    fullFilePath = ""
    filename = ""
    filePath = ""
    exitStatus = 0
        
    while notLoaded:
        examplePath = [r"C:\Your Mother is a Spy.mp4", r"/media/Blunt/Your Mother is a spy.mp4"]

        print("Please enter the path of the file. If the file is in the same directory as this script, type the file name instead.")
        print("\nTo return to the main menu, type 'menu'.\n")
        if platform.system() == "Windows": print("Example:", term.cadetblue1 + examplePath[0] + "\n" + term.normal) 
        else: print("Example:", term.cadetblue1 + examplePath[1] + "\n" + term.normal)

        userInput = input(">> ").encode('ascii','ignore').decode('ascii')

        if userInput.lower() == "menu" or userInput.lower() == "exit":
            exitStatus = 1
            break
        
        # Determine if a full path was entered or only a filename
        try: 
            if os.path.dirname(userInput) == "": # Filename was entered
                filename = userInput
                filePath = currentDir
                fullFilePath = str(Path(currentDir + r'/' + filename))
            else: # Full path was entered
                filename = os.path.basename(userInput) 
                filePath = os.path.dirname(userInput)
                fullFilePath = str(Path(filePath + r'/' + filename))

            if os.path.isfile(fullFilePath):
                notLoaded = False
            else:
                clear()
                if fullFilePath == "":
                    print(term.brown1 + "No path was entered. Please try again.\n" + term.normal)
                    continue
                elif userInput == "":
                    clear()
                    print(term.brown1 + "Nothing was entered. Please try again.\n" + term.normal)
                    continue
                else:
                    print(term.cadetblue1 + fullFilePath + term.normal + " " + term.brown1 + "was not found. \n\nPlease make sure the filename was typed correctly and try again.\n")
                    print("If the filename has some special characters such as emojis, you must rename the file to remove such characters.\n" + term.normal)
                    continue

            if notLoaded == True:
                fullFilePath = ""
                filename = ""
                filePath = ""

                clear()
                print(term.cadetblue1 + fullFilePath, term.brown1 + "is not a valid media file. Please try again.\n")
        except UnboundLocalError as e:
            clear()
            print(term.brown1 + "No valid file name or path was entered. Please try again.\n")

    try:
        # Determine if the media file needs compression
        if getFileSize(fullFilePath) > 8192.00:
            clear()

            text = "The file: "
            text2 = " was found. Processing...\n\n"
            textLength = len(text) + len(filename) + len(text2) + 21
            
            print(
                term.move_xy(int(W/2 - textLength/2), int(H/2 - 2)) + text + term.cadetblue1 + term.link(fullFilePath, filename) + term.normal +
                " (CTRL click to open)" + text2, end=''
                )
            outputFile = convert(filename, fullFilePath, filePath)
            clear()
            
            text = "Procedure complete. The file is located at:"
            path = os.path.dirname(outputFile)
            text2 = "Note: The file may still be large. If that is the case, segment the file or use a different program/service."
            text3 = "Please press Enter to continue."

            print(
                term.move_xy(int(W/2 - len(text)/2), int(H/2 - 2)) + text +
                term.cadetblue1 + term.move_xy(int(W/2 - (len(path) + 21)/2), int(H/2)) + term.link(path, path) + term.normal + " (CTRL click to open)" +
                term.move_xy(int(W/2 - len(text2)/2), int(H/2 + 2)) + text2, end=''
                )

            countdown()

            print(term.move_xy(int(W/2 - len(text3)/2), int(H/2 + 4)) + text3, end='')

            input()

        elif exitStatus == 0:
            clear()
            text = "The file did not need to be compressed. Exiting..."
            print(term.move_xy(int(W/2 - len(text)/2), int(H/2)) + text, end='')
            countdown()
    except Exception as e:
        if userInput.lower() == "menu" or userInput.lower() == "exit":
            clear()
            pass
        else:
            print(e)

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

    clear()
    print("Validating Dependency Requirements...\n")

    try:
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    except subprocess.CalledProcessError:
        import requests

        os.chdir(os.path.dirname(__file__))
        url = "https://bootstrap.pypa.io/get-pip.py"
        response = requests.get(url, allow_redirects=True)

        print("pip, python's package manager, is not installed. I will attempt to download and install it for you. (3)\n\n")
        time.sleep(3)

        if not response.status_code == 200:
            command = 'clear' # Unix
            if platform.system() == "Windows": command = 'cls' # Windows
            os.system(command)

            print("I was unable to download pip. Please install pip manually (Google is your friend) or from " +
            "https://bootstrap.pypa.io/get-pip.py and execute the script. Exiting...")
            sys.exit()
        try:
            subprocess.check_call([os.system("./get-pip.py")])
            print("Pip should have installed without error. Please run this script again. If you keep seeing this message, you may want to try " +
            "adding your python installation to your PATH or read through the terminal and see if there are any errors. Exiting...")
            sys.exit()

        except:
            command = 'clear' # Unix
            if platform.system() == "Windows": command = 'cls' # Windows
            os.system(command)

            print("An unknown error has occured. Please file a bug report at " +
            "https://github.com/jose011974/Download-Compress-Media/wiki/Create-a-Bug-Report and be sure to include a copy of the terminal output.")

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
            time.sleep(0.3)

    clear()
    print("Dependencies validated.")
    time.sleep(1)

def workingDirectory():
    # Sets the directory to where media is located for multi-file operations
    clear()
    while True:
        currentDir = str(Path(os.path.dirname(__file__))) # Get the running directory

        print("Please enter the directory that contains the media you wish to convert:\n")
        print("To return to the main menu, type 'menu'\n")
        print("Current directory:", term.cadetblue1 + currentDir + "\n" + term.normal)

        newDirectory = input(">> ")

        if newDirectory.lower() == "menu" or newDirectory.lower == "exit":
            return "menu"
        else:
            newDirectory = str(Path(newDirectory)) # Change the media directory to the user specified directory

        if os.path.isdir(newDirectory):
            # Double triple check the user specified directory is correct
            clear()
            print("You have entered", term.cadetblue1 + newDirectory, term.normal + "Is this correct? [y/n]\n")
            print("To return to the main menu, type 'menu'\n")

            userInput = input(">> ")
            userInput = userInput.lower()

            if userInput == "y":
                clear()
                print("Source media location changed to:", term.cadetblue1 + newDirectory + "\n" + term.normal)
                return newDirectory
            elif userInput == "n":
                clear()
            elif userInput == "menu":
                return "menu"
            else:
                clear()
                print("Source media location changed to:", term.cadetblue1 + newDirectory + "\n" + term.normal)
                return newDirectory
        else:
            clear()
            print(term.brown1 + "You have entered an invalid path. Please try again.\n" + term.normal)

# ---------------------------------

import distro
import magic
import psutil
import validators
import youtube_dl
import blessed
import datetime

from PIL import Image

debug = 1

if debug == 0:

    try:
        configuration()
    except Exception as e:
        clear()

        print("An error has occured. Please take note of the error and create a bug report at " +
        "https://github.com/jose011974/Download-Compress-Media/wiki/Create-a-Bug-Report\n\n" + str(e))
elif debug == 1:
    configuration()