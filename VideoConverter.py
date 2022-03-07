import magic
import moviepy.editor as mp
import os
import platform
import shutil
import sys
import time
import validators
import youtube_dl

from pathlib import Path
from PIL import Image

global fileTypes 
fileTypes = ["jpg", "jpeg", "png", "gif", "mp4", "webm"]

def clear():
    command = 'clear' # Unix
    if platform.system() == "Windows": command = 'cls' # Windows
    os.system(command)

def workingDirectory():
    clear()
    while True:
        currentDir = str(Path(os.getcwd()))
        
        print("The current directory is:", currentDir)
        print()
        print("Is this the correct directory? [y/n]")
        print()

        userInput = input(">>")
        userInput = userInput.lower()

        if userInput == "y":
            clear()

            print("I will use '", currentDir, "' from now on. If you would like to change the directoy at any time, type 'change' at any prompt.")
            print()

            return currentDir
        elif userInput == "n":
            clear()
            while True:
                print("Please enter the correct directory:")
                print()
                print("Current directory:", currentDir)
                print()

                newDirectory = str(Path(input(">> ")))

                if os.path.isdir(newDirectory):
                    clear()
                    print("You have entered '", newDirectory, "' Is this correct? [y/n]")
                    print()

                    userInput = input(">>")
                    userInput = userInput.lower()

                    if userInput == "y":
                        clear()
                        print("I will use '", newDirectory, "' from now on.")
                        print()
                        return newDirectory
                    elif userInput == "n":
                        clear()
                    else:
                        return
                else:
                    clear()
                    print("You have entered an invalid path. Please try again.")
                    print()
        else:
            clear()
            print("Invalid selection. Please try again.")
            print()

def convert(filename, filePath, mediaPath, ext):

    convPath = str(mediaPath + r'/output')
    newFile = str(convPath + r'/' + filename)

    if not os.path.isdir(convPath):
        os.mkdir(convPath)
    else:
        if ext == "gif":
            newFile = newFile.replace("gif", "mp4")
        if os.path.isfile(newFile):
            return

    fileSize = getFileSize(filePath)

    try:
        if fileSize < 8192.00:
            os.replace(filePath, newFile)
            return
    except Exception as e:
        return

    if ext == "jpg" or ext == "jpeg":
        image_file = Image.open(filePath)
        image_file.save(newFile, quality=95)
    elif ext == "png":
        image_file = Image.open(filePath)
        width, height = image_file.size
        size = int(width/2), int(height/2)
        im_resized = image_file.resize(size, Image.ANTIALIAS)
        im_resized.save(newFile, "PNG")
    elif ext == "gif":
        clip = mp.VideoFileClip(filePath)
        width, height = clip.size
        newFile = newFile.replace("gif", "mp4")
        clip.write_videofile(newFile, codec='libx264', preset='medium', threads='4')
    elif ext == "webm":
        clip = mp.VideoFileClip(filePath)
        width, height = clip.size
        clip_resized = clip.resize(width=width/2, height=height/2)
        clip_resized.write_videofile(newFile, codec='libvpx', preset='medium', threads='4')
    elif ext == "mp4":
        clip = mp.VideoFileClip(filePath)
        width, height = clip.size
        clip_resized = clip.resize(width=width/2, height=height/2)
        clip_resized.write_videofile(newFile, codec='libx264', preset='medium', threads='4')

    fileSize = getFileSize(newFile)

    if fileSize < 8192.00:
        return
    elif fileSize > 8192.00:
        print("placeholder for future algorithm prompt")
        input()

def getFileExtension(filename):
    fileExt = magic.from_file(filename, mime=True) # Identify the file type
    fileExt = fileExt[6:len(fileExt)] # Save the file type

    return fileExt

def getFileSize(file):
    fileSize = os.path.getsize(file) # Get the size of a file
    fileSize = float("{:.2f}".format(fileSize / 1024)) # Convert the output from bytes to MB

    return fileSize

def getListOfFiles(dirName):
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
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    
    return allFiles

def quantity():
    while True:
        print("Are you going to compress one file or multiple files?")
        print()
        print("1. One file")
        print("2. Multiple files")
        print()

        try:
            userInput = int(input(">>"))
        except ValueError:
            print()
            print("Invalid selection. Please try again.")
            print()
            return 0

        if userInput == 1:
            return "single"
        elif userInput == 2:
            return "multiple"
        else:
            print()
            print("You have entered an invalid entry. Please try again.")
            print()
           

def multipleFileConvert():
    notFile = True

    mediaPath = workingDirectory()
        
    while notFile:
        print("I will now attempt to find media files and compress them if required.")
        print()
        print("Press enter to continue.")
        print()

        input()

        filePathList = getListOfFiles(mediaPath)
        totalFiles = len(filePathList)
        currentPos = 0
        
        clear()
        print("Found a total of", totalFiles, "files. Processing...")

        time.sleep(2)

        for fullFilePath in filePathList:
            currentPos = currentPos+1
            fullFilePath = str(Path(fullFilePath)).encode('ascii','ignore').decode('ascii')
            filename = os.path.basename(fullFilePath)

            if os.path.isfile(fullFilePath):
                ext = getFileExtension(fullFilePath)
                for extension in fileTypes:
                    if ext == extension:
                        print("Compressing", filename, "-", getFileSize(fullFilePath), "MB - File", str(currentPos), "of", str(totalFiles))
                        print()
                        convert(filename, fullFilePath, mediaPath, ext)
                        break
        
        clear()
        print()
        print("All media files were processed successfully. They are located at:", mediaPath + r'/output')
        print()
        print("Press enter to continue.")
        print()

        input()
        clear()
        break

def multipleURLConvert():
    notFile = True

    mediaPath = workingDirectory()
        
    while notFile:
        print("Please create a file called ' URL.txt ' and add a URL to each line. Then press enter when you are ready.")
        print()

        input()

        if os.path.isfile(mediaPath + r'/' + "URL.txt"):

            textfileURL = open('URL.txt', 'r')
            URLPathList = textfileURL.readlines()
            
            currentPos = 0
            totalURLs = len(URLPathList)
            
            for uriLine in URLPathList:
                uri = uriLine[1:].rstrip()
                if validators.url(uri):
                    print("URI found:", uri)
                    print("Downloading...")
                    print()
                    print("[Youtube-DL]")
                    # Download the media file
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([uri])

                    filename = downFileName.encode('ascii','ignore').decode('ascii')
                    tempPath = str(Path(mediaPath + r'/temp'))
                    filePath = tempPath + r'/' + filename
                    currentPos = currentPos+1

                    if not os.path.isdir(tempPath):
                        os.mkdir(tempPath)
                    os.replace(filename, filePath)

                    if os.path.isfile(filePath):
                        ext = getFileExtension(filePath)
                        for extension in fileTypes:
                            if ext == extension:
                                convert(filename, filePath, mediaPath, ext)
                                break
        else:
            clear()

            print("' URL.txt ' was not found. Please try again.")
            print()

        clear()
        shutil.rmtree(tempPath)
        print()
        print("All media files were processed successfully. They are located at:", mediaPath + r'/output')
        print()
        print("Press enter to continue.")
        print()

        input()
        clear()
        break

def singleFileConvert():
    clear()
    notFile = True

    currentPath = str(Path(os.getcwd()))
        
    while notFile:
        examplePath = [r"C:\Your Mother is a Spy.mp4", r"/media/Blunt/Your Mother is a spy.mp4"]
        print("Please enter the path of the file you would like to compress. If the file is in the same directory as this script, just type the file name:")
        print()
        if platform.system() == "Windows": print("Example:", examplePath[0]) 
        else: print("Example:", examplePath[1])
        print()

        userInput = input(">> ").encode('ascii','ignore').decode('ascii')

        if os.path.dirname(userInput) == '':
            filename = userInput
            filePath = str(Path(currentPath + r'/' + filename))
        else:
            filename = os.path.basename(userInput)
            filePath = os.path.dirname(userInput)

        if os.path.isfile(filePath):
            ext = getFileExtension(filePath)
            for extension in fileTypes:
                if ext == extension:
                    notFile = False
                    break
            if notFile == True:
                print()
                print("'", filePath, "' is not a valid media file. Please try again. If you are sure the file is valid, it may be corrupt.")
                print()
        else:
            clear()
            print("'", filePath, "' was not found. Please make sure the filename was typed correctly and try again. If the filename has some special")
            print("characters such as emojis, you must rename the file to remove such characters.")
            print()

    if getFileSize(filePath) > 8192.00:
        clear()
        print("File", filename, "was found.")
        convert(filename, filePath, currentPath, ext)
    else:
        clear()

        print("The file specified did not need compression. Exiting...")
        time.sleep(4)
    
    clear()
    print("File was compressed successfully! It is located at", currentPath + '/output/')
    print()

def singleURLConvert():
    notFile = True

    mediaPath = workingDirectory()
        
    while notFile:
        print("Please enter the URL of the media file to download and compress: ")
        print()
        print("Example: https://static1.e621.net/data/sample/89/85/8985342ea8ff4e4c4692f55e082aadb1.jpg")
        print()

        uri = input(">> ")

        if not validators.url(uri):
            print()
            print("The URL is not valid. Please check the spelling and try again.")
        else:
            print("URI found:", uri)
            print("Downloading...")
            print()
            print("[Youtube-DL]")
            # Download the media file
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([uri])

            filename = downFileName.encode('ascii','ignore').decode('ascii')
            
            fileExt = getFileExtension(filename)
            fileSize = getFileSize(filename)

            if fileSize > 8192.00:
                convert(filename, fileExt, mediaPath)
            else:
                clear()

                print("Download complete. Exiting...")
                print()
                time.sleep(4)
                notFile = False

def main():
    convType = 0

    print("Please type a number that matches your selection, then press your enter key.")
    print()
    print("1. Local compression")
    print("2. Online compression")
    print("3. Exit")
    
    print()

    try:
        userInput = int(input(">>"))
    except ValueError:
        clear()
        print("Invalid selection. Please try again.")
        print()
        return

    print()

    if userInput == 1:
        clear()
        while convType == 0:
            convType = quantity()
        if convType == "single": 
            singleFileConvert()
        elif convType == "multiple":
            multipleFileConvert()
        else:
            print()
            print("An error has occured: A parameter was set to an unexpected value.")
            print()
            print("Exiting...")
            sys.exit()

    elif userInput == 2:
        clear()
        convType = quantity()
        if convType == "single": 
            singleURLConvert()
        elif convType == "multiple":
            multipleURLConvert()
        else:
            print()
            print("An error has occured: A parameter was set to an unexpected value.")
            print()
            print("Exiting...")
            sys.exit()
    elif userInput == 3:
        print("Exiting...")
        sys.exit()
    else:
        clear()
        print("Invalid selection. Please try again.")
        print()

def downloadStatus(d):
    if d['status'] == 'finished': # If the download progress is complete
        global downFileName
        origFileName = d['filename']

        print()
        print("Downloading complete.")
        print()

        downFileName = origFileName.encode('ascii','ignore').decode('ascii')

# Logger for Youtube-DL
class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

# Parameters for Youtube-DL.
# See https://github.com/ytdl-org/youtube-dl/blob/5014bd67c22b421207b2650d4dc874b95b36dda1/youtube_dl/YoutubeDL.py#L141
ydl_opts = {
    'outtmpl': f'%(title)s.%(ext)s', 
    'restrictfilenames': True, 
    'logger': MyLogger(), 
    'progress_hooks': [downloadStatus], 
}
        
clear()
while True:
    main()