#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created by: Jose M. with Python 3.10.4 and Visual Studio Code
# You are free to modify this as you see fit. All I ask is that you leave the line at the top or credit me somewhere. Thank you.

# Import packages that allow screen clearing and package dependency finding.
import os
import platform
import subprocess
import sys

#Change the clear screen command based on OS.
command = 'clear' # Unix
if platform.system() == "Windows": command = 'cls' # Windows
os.system(command)

# List the installed packages
try:
    # Remove the version number from the package name
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
# Uh oh.
except subprocess.CalledProcessError:
    print()
    print("ERROR: The subprocess package exited with an error. This most likely means you do not have pip installed.")
    print()
    if platform.system() == "Windows":
        print("Please make sure pip is installed and try again. Otherwise, consult the internet as pip should be installed by default...")
    else:
        print("Depending on the exact issue, the following may fix the error you are facing.")
        print()
        print("First, make sure pip is installed by entering the following command in a terminal:")
        print("Ubuntu/Debian: sudo apt install python3-pip")
        print()
        print("If the above did not fix it, then try this command:")
        print()
        print("curl -sS https://bootstrap.pypa.io/get-pip.py | python3")
        print()
        print("This updates your pip to a newer version according to this post: https://stackoverflow.com/a/69527217")

packages = ["discord.py", "python-magic", "moviepy", "Pillow", "psutil", "validators", "wget", "youtube-dl"]

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
        print("Dependency " + p + " satisfied.")

# Import the rest of the packages that range from changing text color to downloading videos.
from colorama import Fore, Back, Style, init
import fileinput
import magic
import psutil
import shutil
import re
import requests
import time
import validators
import webbrowser
import youtube_dl

from pathlib import Path

init(autoreset=True) # Initialize colorama

fileTypes = [".jpeg", ".png", ".gif", ".mp4", ".webm"]

def clear():
    # Change the clear screen command based on OS.
    command = 'clear' # Unix
    if platform.system() == "Windows": command = 'cls' # Windows
    os.system(command)

    title()

def convert(filename, fullFilePath, mediaPath):
    convPath = str(Path(mediaPath + r'/output')) # Output path
    outputFile = str(Path(convPath + r'/' + filename))    # Output file
    oldFile = ""

    createTempFolder(convPath, mediaPath)

    clear()

    ext = os.path.splitext(fullFilePath)
    codec = ""

    if ext[1] == ".gif":
        oldFile = outputFile
        outputFile = convPath + r'/' + os.path.basename(ext[0]) + ".webm"
        codec = "-c:v libvpx-vp9"
    elif ext[1] == ".png":
        outputFile = convPath + r'/' + os.path.basename(ext[0]) + ".jpg"
    
    inputFile = str(Path(fullFilePath))
    outputFile = str(Path(outputFile))
        
    if platform.system() == "Windows":
        ffPath = "C:/ffmpeg/ffmpeg.exe"
        os.system(ffPath + ' -i "' + inputFile + '" -r 24 ' + codec + ' "' + outputFile + '"') # Windows
    else:
        os.system("ffmpeg" + ' -i "' + inputFile + '" -r 24 ' + codec + ' "' + outputFile + '"') # Linux / Other OS
        try: # Delete GIF file
            os.remove(oldFile)
        except:
            pass

    # Check if the filesize is under 8MB. If not, ask the user if they wish to compress the file via an algorithm that is not ready yet.
    fileSize = getFileSize(outputFile)

    if fileSize < 8192.00:
        return
    elif fileSize > 8192.00:
        print("\n", filename, "was unable to be compressed below 8MB. Please try another program / service.\n")
        print("Please press enter to continue")
        input()



def checkIfProcessRunning(processName):
    # For whatever reason, sometimes a video conversion process is stalled. This function kills any and all ffmpeg processes as you cannot move a file
    # that is in use by a process.

    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                # Expire the process.
                p = psutil.Process(proc.pid)
                p.terminate()
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): # Uh oh.
            pass
    return False

def createTempFolder(convPath, mediaPath):
    boolVal = True
    # Create the output folder
    while boolVal:
        try:
            if not os.path.isdir(convPath):
                os.mkdir(convPath)
                boolVal = False
            else:
                boolVal = False
        
        except PermissionError: # Uh oh.
            clear()
            print(Back.RED + "Error: Missing required permissions. Please make sure you have read and write access to", end='')
            print(Back.MAGENTA + Fore.BLACK + mediaPath, "in order to create the neccessary folders.\n")
            print("To try again, type y. If you would rather instead use the path the script is located at, type 'n'.\n")
            print("To return to the main menu, type 'menu'\n")

            userInput = input(">> ")

            if userInput == "y":
                continue
            elif userInput == "n" or userInput == "menu":
                return

def errorHandler(origError, uri):
    
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    error = ansi_escape.sub('', origError)

    error = error[7:]
    # So I have no idea how to create a proper error handler without making my own version of youtube-dl. So this is the next best solution.
    # I strip out the trash and leave the error message behind, then I detect the error message and assign an error code.

    counter = -1
    errorNumber = -1
    errorMessage = ""

    # Iterate over the error message
    for element in error:
        counter = counter + 1
        if element == ";": 
            errorMessage = error[:counter]
            break

    if errorMessage == "":
        errorMessage = error
    
    # Check the error code and assign an error code to it

    if errorMessage == "There's no video in this tweet." or "Unable to extract video url": 
        errorNumber = 1
    elif errorMessage == "Unsupported URL: " + uri:
        errorNumber = 2
    elif errorMessage == "Unable to download JSON metadata: HTTP Error 404: Not Found (caused by <HTTPError 404: 'Not Found'>)":
        errorNumber = 3
    else:
        errorNumber = 0
    
    if errorNumber == 0:
        clear()

        print("An unknown error has occured. Please create an issue at https://github.com/jose011974/Download-Compress-Media/issues and \n")
        print("include the URL and error message found below in your issue:\n")
        print(uri, "\n")
        print(error)
    elif errorNumber == 1:
        clear()

        print("Youtube-DL was unable to find a valid media source. Try again with a direct link to the media source, instead of the hosted page.\n")
        print("You can try right clicking the media and click 'Copy Video/Image Address'. Otherwise you will have to use the ", end='')
        print("Inspect Element tool (F12). If you are still getting this error, that URL is not supported.\n")
        print("URL:", uri)

    elif errorNumber == 2:
        clear()

        print("Youtube-DL was unable to download the media. Please try the direct link to the media instead.\n")
        print("URL:", uri)

    elif errorNumber == 3:
        clear()

        print("The URL was not accessable. Please make sure the link is accessable through a browser. If it is, then submit an issue on the Github\n")
        print("URL:", uri)
        
    print("\nIf you would like to supress error messages, type 'suppress', otherwise, press enter to continue.\n")

    userInput = input(">>")

    if userInput.lower() == "suppress":
        return "suppress"
    
    clear()

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

def multipleFileConvert():

    notFile = True
    mediaPath = workingDirectory()
    convPath = str(Path(mediaPath + r'/output')) # Output path
    createTempFolder(convPath, mediaPath)
    
    if mediaPath == "menu":
        clear()
        return
        
    while notFile:
        print("\nI will now attempt to find media files and compress them if required.\n")
        print("Press enter to continue.\n")

        input()

        filePathList = getListOfFiles(mediaPath)
        totalFiles = len(filePathList)
        currentPos = 0
        
        clear()
        print("Found a total of", totalFiles, "files. Processing...")

        time.sleep(2)

        # Iterate through the files in filePathList and determine if they need compression
        for fullFilePath in filePathList:
            currentPos = currentPos+1
            fullFilePath = str(Path(fullFilePath)).encode('ascii','ignore').decode('ascii')
            filename = os.path.basename(fullFilePath)
            convFile = str(Path(mediaPath + r'/output/' + filename)) # Output file path

            if os.path.isfile(fullFilePath):
                if getFileSize(fullFilePath) > 8192.00:
                        print("\nCompressing", Back.MAGENTA + filename, "-", getFileSize(fullFilePath), "MB - File", str(currentPos), "of", str(totalFiles) + "\n")
                        convert(filename, fullFilePath, mediaPath)
                        os.remove(fullFilePath)
                else:
                    os.replace(fullFilePath, convFile)

        clear()
        print("All media files were compressed successfully. They are located at:", Back.MAGENTA + Fore.BLACK + mediaPath + r'/output' + "\n")
        print("Press enter to continue.\n")

        input()
        clear()
        break

def multipleURLConvert():
    eMessage = ""
    notFile = True
    mediaPath = os.getcwd()
    outputPath = str(Path(mediaPath + r'/output'))
    UnhandledURLs = list()
        
    while notFile:
        clear()
        print("Please create a file called", Back.MAGENTA + Fore.WHITE + "URL.txt", "in", Back.MAGENTA + Fore.WHITE + mediaPath, "and add a URL to each line. Press enter when you are ready.\n")
        print("If you wish to return to the main menu, type 'menu'\n")

        userInput = input(">> ")
        print()

        if userInput.lower() == "menu" or userInput.lower() == "exit":
            clear()
            return

        # Open the URL.txt file and create a list of URL's
        if os.path.isfile(mediaPath + r'/' + "URL.txt"):
            URLPathList = list()

            for line in fileinput.FileInput("URL.txt",inplace=1):
                if line.rstrip():
                    URLPathList.append(line)

            currentPos = 1
            largeFileCount = 0
            totalURLs = len(URLPathList)

            if totalURLs == 0:
                clear()
                print("There were no URL's found in URL.txt. Please make sure that there are URL's and that you have read/write permissions to the file.\n")
                print("Press enter to return to the menu.\n")
                input(">> ")
                clear()
                break  
            
            # For each URL, download the media and determine if it needs compression
            for uriLine in URLPathList:
                uri = uriLine.rstrip()
                if validators.url(uri):
                    print("URI found:", uri, Back.MAGENTA + Fore.WHITE + "File " + str(currentPos) + r'/' + str(totalURLs - 1) + Style.RESET_ALL + "\n")
                    print("Downloading...\n")
                    print("[Youtube-DL]")

                    # Download the media file
                    try:
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([uri])
                        # Obtain the file paths for creating the temp and output folders
                        filename = downFileName.encode('ascii','ignore').decode('ascii')
                        tempPath = str(Path(mediaPath + r'/temp'))
                        filePath = str(Path(tempPath + r'/' + filename))
                        currentPos = currentPos+1

                        # Create a temp and output directory
                        if not os.path.isdir(tempPath):
                            os.mkdir(tempPath)
                        os.replace(filename, filePath)
                        if not os.path.isdir(outputPath):
                            os.mkdir("output")
                    except:
                        if eMessage != "suppress":
                            eMessage = errorHandler(errorMessage, uri)
                        UnhandledURLs.append(uri + "\n")
                        currentPos = currentPos+1

                        clear()
                        print(Back.RED + "ERROR: unable to download last URL, skipping.\n")

            # Check if there are any files over 8MB
            filePathList = getListOfFiles(mediaPath)
            totalFiles = len(filePathList)

            for fullFilePath in filePathList:
                fullFilePath = str(Path(fullFilePath)).encode('ascii','ignore').decode('ascii')
                if getFileSize(fullFilePath) > 8192.00:
                    largeFileCount = largeFileCount+1
            
            # Ask the user if they want to compress any files over 8MB
            if largeFileCount > 0:
                print(Back.MAGENTA + Fore.WHITE + str(largeFileCount), "out of", Back.MAGENTA + Fore.WHITE + str(totalFiles), "media files are larger ", end='')
                print("than 8 MB. If you wish to send the media over Discord you cannot unless you have Nitro (why would you) or are in a server ", end='')
                print("that is boosted. For now, compression will half the resolution of the media. In the future, an algorithm will be ", end='')
                print("implimented to find the best compression method.\n")
                print("Do you wish to compress the media now? [y/n]\n")
            
                userInput = input(">> ")

                if userInput.lower() == "y":
                    currentPos = 0
                    
                    # Iterate through filePathList and determine if the file needs conversion
                    for fullFilePath in filePathList:
                        fullFilePath = str(Path(fullFilePath)).encode('ascii','ignore').decode('ascii')
                        filename = os.path.basename(fullFilePath)
                        currentPos = currentPos+1
                        if os.path.isfile(fullFilePath):
                            if getFileSize(fullFilePath) > 8192.00:
                                convert(filename, fullFilePath, mediaPath)
                                os.remove(fullFilePath)
                            else:
                                os.replace(fullFilePath, str(Path(outputPath + r'/' + filename))) 

        else:
            clear()
            print(Back.MAGENTA + "URL.txt" + Style.RESET_ALL + "was not found. Please try again.\n")
            continue
        
        # Try to cleanup any remaining files in the temp folder. Remove the temp folder once it is empty
        clear()
        print("Attempting to cleanup...\n")
        counter = 0
        while True:
            try:
                # Copy any files in the temp folder to the output folder
                filePathList = getListOfFiles(tempPath)
                for fullFilePath in filePathList:
                    fullFilePath = str(Path(fullFilePath)).encode('ascii','ignore').decode('ascii')
                    filename = os.path.basename(fullFilePath)
                    os.replace(fullFilePath, str(Path(outputPath + r'/' + filename)))

                time.sleep(1)
                shutil.rmtree(tempPath)
                break
            except PermissionError: # Uh oh
                if counter != 0:
                    clear()
                    if checkIfProcessRunning('ffmpeg'):
                        print('A stalled video conversion has been detected. Attempting to terminate...')
                    else:
                        print(Back.RED + Fore.White + "An error occured while removing/moving temporary files. Save any remaining files in the temp folder.\n")
                        print("Press enter to continue.")
                        input()
                    break
                else:
                    print("Attempting to remove temporary files...")
                    time.sleep(2)
                    counter = counter + 1

        clear()

        UnhandledCount = len(UnhandledURLs)
        if UnhandledCount > 0:

            unsupportedURL = open("Unsupported URLs.txt", "w")
            unsupportedURL.writelines(UnhandledURLs)
            unsupportedURL.close()

            print("There are some URLs that I was unable to access. They have been saved into a text file called 'Unsupported URLs.txt'. It is ", end='')
            print("located in the same directory as the script.\n")
        
        print("Operation(s) complete. The media files are located at:", Back.MAGENTA + Fore.WHITE + outputPath)
        print("\nPress enter to continue.")

        input()
        clear()
        break

def spoil():
    clear()

    mediaPath = workingDirectory()

    print("I will now append 'SPOILER' to the files in " + Back.MAGENTA + mediaPath)
    print("\nPress enter to continue")
    input()

    filePathList = getListOfFiles(mediaPath)

    for file in filePathList:
        ext = os.path.splitext(file)
        os.replace(file, mediaPath + r'/' + "SPOILER_" + os.path.basename(file) + ext[1])
        pass

    clear()

    print("Process complete. Check", Back.MAGENTA + mediaPath, "for the renamed files.\n")
    print("Press enter to continue.\n")
    input()
    

def singleFileConvert():
    clear()
    notFile = True

    currentDir = str(Path(os.getcwd()))
    fullFilePath = ""
    filename = ""
    filePath = ""
        
    while notFile:
        examplePath = [r"C:\Your Mother is a Spy.mp4", r"/media/Blunt/Your Mother is a spy.mp4"]
        print("Please enter the path of the file you would like to compress. If the file is in the same directory as this script, ", end='')
        print("just type the file name.\n\nTo return to the main menu, type 'menu'.\n")
        if platform.system() == "Windows": print("Example:", Back.MAGENTA + examplePath[0] + "\n") 
        else: print("Example:", Back.MAGENTA + examplePath[1] + "\n")

        userInput = input(">> ").encode('ascii','ignore').decode('ascii')

        if userInput.lower() == "menu":
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
                notFile = False
            else:
                clear()
                if fullFilePath == "":
                    print(Back.RED + "No path was entered. Please try again.\n")
                    continue
                elif userInput == "":
                    clear()
                    print(Back.RED + "Nothing was entered. Please try again.\n")
                    continue
                else:
                    print(Back.MAGENTA + fullFilePath + Style.RESET_ALL + " " + Back.RED + "was not found. Please make sure the filename was typed correctly and try again.\n")
                    print("If the filename has some special characters such as emojis, you must rename the file to remove such characters.\n")
                    continue

            if notFile == True:
                fullFilePath = ""
                filename = ""
                filePath = ""

                clear()
                print(Fore.CYAN + fullFilePath, Back.RED + "is not a valid media file. Please try again.\n")
        except UnboundLocalError as e:
            clear()
            print(Back.RED + "No valid file name or path was entered. Please try again.\n")

    try:

        # Determine if the media file needs compression
        if getFileSize(fullFilePath) > 8192.00:
            clear()
            print("File", Back.MAGENTA + filename, "was found. Compressing...\n")
            convert(filename, fullFilePath, filePath)
            clear()
            print("File was compressed successfully! It is located at", Back.MAGENTA + filePath + "/output/\n")
            os.remove(fullFilePath)
        else:
            clear()
            print("The file did not need compression. Exiting...")
            time.sleep(4)
    except Exception as e:
        if userInput.lower() == "menu":
            clear()
            pass
        else:
            print(e)

def singleURLConvert():
    notFile = True

    mediaPath = os.getcwd()
    outputPath = str(Path(mediaPath + r'/output'))
    tempPath = str(Path(mediaPath + r'/temp'))
        
    while notFile:
        clear()
        print("Please enter the URL of the media file to download and compress(optional): \n")
        print("Example: https://static1.e621.net/data/sample/89/85/8985342ea8ff4e4c4692f55e082aadb1.jpg\n")

        uri = input(">> ")
        print()

        # Check if the URL is valid
        if not validators.url(uri):
            print("\nThe URL is not valid. Please check the spelling and try again.")
        else:
            print("URI found:", uri)
            print("Downloading...\n")
            print("[Youtube-DL]")

            try:
                # Download the media file
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([uri])

                    filename = downFileName.encode('ascii','ignore').decode('ascii')
                    tempFilePath = str(Path(tempPath + r'/' + filename))

                    # Create a temp and output directory
                    if not os.path.isdir(tempPath):
                        os.mkdir(tempPath)
                    os.replace(filename, tempFilePath)
                    if not os.path.isdir(outputPath):
                        os.mkdir("output")
            except:
                errorHandler(errorMessage, uri)
                return

            fileSize = getFileSize(tempFilePath)
            outputFullFilePath = str(Path(mediaPath + r'/' + "output" + r'/' + filename))

            if fileSize > 8192.00:
                print("The media file has been sucessfully downloaded and is located at", Back.MAGENTA + Fore.BLACK + outputFullFilePath + Style.RESET_ALL + "\n")
                print("If you do not have Discord Nitro (why would you), then you are unable to send the image to anyone ", end='')
                print("unless you're in a server that has been boosted.) \n")
                print("Do you wish to compress the media now? [y/n]\n")

                userInput = input(">> ")
                print()

                if userInput.lower() == "y":
                    convert(filename, tempFilePath, mediaPath)
                    os.remove(tempFilePath)

                    clear()
                    print("The media file has been sucessfully compressed and is located at", Back.MAGENTA + Fore.BLACK + outputFullFilePath + "\n")
                    return
                else:
                    os.rename(tempFilePath, outputFullFilePath)
                    clear()
                    return
            else:
                os.rename(tempFilePath, outputFullFilePath)
                clear()
                print("Media successfully downloaded and is located at", Back.MAGENTA + Fore.BLACK + outputFullFilePath + "\n")
                return

def title():

    # Create a title bar based on the console window size

    title = "[MediaConverter.py v1.0 - Download and compress media]"
    consoleSize = shutil.get_terminal_size()
    col, row = int(consoleSize[0])-len(title), int(consoleSize[1])

    for x in range(0, int(col/2)):
        print("-", end = '')

    print(title, end = '')

    for x in range(0, int(col/2)):
        print("-", end='')

    print("\n")

def workingDirectory():
    # This function allows the program to find the folder where the media they want to convert is located.
    clear()
    while True:
        currentDir = str(Path(os.getcwd())) # Get the running directory

        print("Please enter the directory that contains the media you wish to convert:\n")
        print("To return to the main menu, type 'menu'\n")
        print("Current directory:", Back.MAGENTA + currentDir + "\n")

        newDirectory = input(">> ")

        if newDirectory.lower() == "menu":
            return "menu"
        else:
            newDirectory = str(Path(newDirectory)) # Change the media directory to the user specified directory

        if os.path.isdir(newDirectory):
            # Double triple check the user specified directory is correct
            clear()
            print("You have entered", Back.MAGENTA + newDirectory,"Is this correct? [y/n]\n")
            print("To return to the main menu, type 'menu'\n")

            userInput = input(">> ")
            userInput = userInput.lower()

            if userInput == "y":
                clear()
                print("Source media location changed to:", Back.MAGENTA + newDirectory + "\n")
                return newDirectory
            elif userInput == "n":
                clear()
            elif userInput == "menu":
                return "menu"
            else:
                clear()
                print("Source media location changed to:", Back.MAGENTA + newDirectory + "\n")
                return newDirectory
        else:
            clear()
            print("You have entered an invalid path. Please try again.\n")

def downloadStatus(d):
    if d['status'] == 'finished': # Download status complete
        global downFileName
        origFileName = d['filename']

        print("\nDownloading complete.\n")

        downFileName = origFileName.encode('ascii','ignore').decode('ascii')

# Logger for Youtube-DL
class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        global errorMessage
        errorMessage = msg

# Parameters for Youtube-DL.
# See https://github.com/ytdl-org/youtube-dl/blob/5014bd67c22b421207b2650d4dc874b95b36dda1/youtube_dl/YoutubeDL.py#L141
ydl_opts = {
    'outtmpl': f'%(id)s.%(ext)s',
    'restrictfilenames': True,
    'logger': MyLogger(),
    'progress_hooks': [downloadStatus],
}

def main():
    while True:

        print("This script provides the ability to download and compress local/online media. Single and multiple file/URL modes are", end=' ')
        print("avaiable to you.\n\nThe following media types have been tested:", Back.MAGENTA + Fore.WHITE + "jpg/jpeg, png, gif, mp4, and webm.")
        print("Any other formats should work, however they have been untested. Proceed at your own risk.\n")
        print("Please select the option that works best for you.\n")
        
        print("1. Single File")
        print("2. Multiple Files")
        print("3. Single URL")
        print("4. Multiple URLs")
        print("5. Spoil media")
        print("6. Open Unsupported URLs")
        print("7. Help")
        print("8. Exit\n")

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
                spoil()
            elif userInput == 6:
                counter = 1
                clear()

                print("I will now go ahead and open any unsupported links in 'Unsupported URLs.txt'. I will open them all at once, with ", end='')
                print("a short pause in between just in case you have over 2000 URLs.\n")
                print("If you want to stop the opening process, press CTRL and C on your keyboard at the same time.\n")
                print("Press enter to continue.")
                
                input()

                URLs = list()

                for line in fileinput.FileInput("Unsupported URLs.txt",inplace=1):
                    if line.rstrip():
                        URLs.append(line)

                if len(URLs) == 0:
                    clear()

                    print("There were no URLs detected.\n")
                    print("Press enter to continue.")
                    input()

                for URL in URLs:
                    clear()

                    print("OPENING", counter, "OUT OF", len(URLs))
                    webbrowser.open(URL, new=0, autoraise=False)
                    time.sleep(0.4)
                    counter = counter + 1

            elif userInput == 7:
                webbrowser.open("https://github.com/jose011974/Download-Compress-Media", new=1)

                clear()

                print("The Github page should have opened. If it did not, please go to https://github.com/jose011974/Download-Compress-Media\n")
                print("Press enter to continue.\n")
                input()

            elif userInput == 8:
                clear()
                print("Exiting...\n")
                sys.exit()
            
            clear()
        except ValueError:
            clear()
            print("You have entered an invalid entry. Please try again.\n")
            continue

while True:
    clear()

    main()