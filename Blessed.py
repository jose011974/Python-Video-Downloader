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

def createOutputFolder(currentDir):
    outputDir = str(Path(currentDir + r'/output'))
    boolVal = True
    # Create the output folder
    while boolVal:
        try:
            if not os.path.isdir(outputDir):
                os.mkdir(outputDir)
                boolVal = False
            else:
                boolVal = False
        
        except PermissionError:
            clear()
            print(term.brown1 + "Error: Missing required permissions. Please make sure you have read and write access to" + term.normal +
            term.cadetblue1 + currentDir, + term.normal + "in order to create the neccessary folders.\n To try again, type y. If you would" +
            "rather instead use the path the script is located at, type 'n'.\nTo return to the main menu, type 'menu'\n")

            userInput = input(">> ")

            if userInput == "y":
                continue
            elif userInput == "n":
                return
            elif userInput == "menu":
                return

def clear():
    command = 'clear' # Unix
    if platform.system() == "Windows": command = 'cls' # Windows
    os.system(command)

    title()

def configuration():

    updateDependencies()

    global term
    global W,H
    term = blessed.Terminal()
    W,H = term.width, term.height
    distroID = distro.name(pretty=True)
    distroID = "Linux Version: " + distroID

    while True:
        clear()

        # Creates required files and folders.
        scriptPath = os.path.dirname(__file__)
        URLTextPath = str(Path(scriptPath + r'/URL.txt'))
        UnsuppURLPath = str(Path(scriptPath + r'/Unsupported URLs.txt'))
        outputPath = str(Path(scriptPath + r'/output'))

        if not os.path.exists(URLTextPath):
            fp = open(URLTextPath, 'x')
            fp.close()
        if not os.path.exists(UnsuppURLPath):
            fp = open(UnsuppURLPath, 'x')
            fp.close()
        if not os.path.exists(outputPath):
            os.mkdir(outputPath)

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

def convert(filename, filenamePath):
    outputPath = str(Path(filenamePath + r'/output')) # Output path
    outputFile = str(Path(outputPath + r'/' + filename)) # Output file
    inputFile = str(Path(filenamePath + r'/' + filename)) # Input file
    ext = os.path.splitext(filename) # Extension
    codec = ""
    
    now = datetime.datetime.now()
    text = "Time the Process started: " + now.strftime('%I:%M %p')
    print(term.move_xy(int(W/2 - len(text)/2), int(H/2 + 4)) + text + "\n")

    if ext[1] == ".gif" or ext[1] == ".webm" or ext[1] == ".mp4":
        # Setup paths and codec options
        outputFile = str(Path(outputPath + r'/' + os.path.basename(ext[0]) + ".mp4"))
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

def countdown(i):
    curLocation = term.get_location()
    W = curLocation[1]
    H = curLocation[0]

    while i >= 0:
        print(term.move_xy(W + 1,H) + "(" + str(i) + ")")
        time.sleep(1)
        i = i - 1

def countStrings(text):
    num = 0
    res = char.str_len(text)
    for ele in res:
        num = num + ele

    return num

def errorHandler(origError, uri):
    
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    error = ansi_escape.sub('', origError)

    error = error[7:]
    # I have no idea how to create a proper error handler without making my own version of youtube-dl. So this is the next best solution.
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

        print("ERROR 0: An unknown error has occured. Please create an issue at https://github.com/jose011974/Download-Compress-Media/issues and \n")
        print("include the URL and error message found below in your issue:\n")
        print(uri, "\n")
        print(error)
    elif errorNumber == 1:
        clear()

        print("ERROR 1: Youtube-DL was unable to find a valid media source. Try again with a direct link to the media source, instead of the hosted page.\n")
        print("You can try right clicking the media and click 'Copy Video/Image Address'. Otherwise you will have to use the ", end='')
        print("Inspect Element tool (F12). If you are still getting this error, that URL is not supported.\n")
        print("URL:", uri)

    elif errorNumber == 2:
        clear()

        print("ERROR 2: Youtube-DL was unable to download the media. Please try the direct link to the media instead.\n")
        print("URL:", uri)

    elif errorNumber == 3:
        clear()

        print("ERROR 3: The URL was not accessable. Please make sure the link is accessable through a browser. If it is, then submit an issue on the Github\n")
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
                spoilMedia(1)
            elif userInput == 6:
                spoilMedia(0)
            elif userInput == 7:
                openUnsupportedURLs()

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

        countdown(3)
        clear()

        # Iterate through the files in filePathList and determine if they need compression
        for fullFilePath in filePathList:
            currentPos = currentPos+1
            fullFilePath = str(Path(fullFilePath)).encode('ascii','ignore').decode('ascii')
            filename = os.path.basename(fullFilePath)
            filePath = os.path.dirname(fullFilePath)
            convFile = str(Path(mediaPath + r'/output/' + filename)) # Output file path

            if os.path.isfile(fullFilePath):
                if getFileSize(fullFilePath) > 8192.00:
                        text = "Current file: "
                        text2 = " | " + str(getFileSize(fullFilePath)) + " MB | File " + str(currentPos) + " of " + str(totalFiles) + "\n"
                        print(term.move_xy(int(W/2 - (len(text) + len(filename) + len(text2))/2), int(H/2 - 2)) + text + 
                        term.cadetblue1 + filename + term.normal + text2)
                        # print("\nCompressing " + term.cadetblue1 + filename + term.normal + " | " + str(getFileSize(fullFilePath)) + " MB | File " + str(currentPos) + " of " + str(totalFiles) + "\n")
                        convert(filename, filePath)
                else:
                    shutil.copy(fullFilePath, convFile)
        
        clear()      
        text = ["Procedure complete. The files are located at:", 
                "Note: The files may still be large. If that is the case, segment the files or use a different program/service.", 
                "Press Enter to continue."]

        print(
            term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 3)) + text[0],
            term.move_xy(int(W/2 - (len(mediaPath))/2), int(H/2 - 1)) + term.cadetblue1 + mediaPath + term.normal,
            term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 1)) + text[1],
            )

        countdown(5)
        print(term.move_xy(int(W/2 - len(text[2])/2), int(H/2 + 3)) + text[2])
        input()

        clear()
        break

def multipleURLConvert():
    eMessage = ""
    notFile = True
    mediaPath = os.getcwd()
    outputPath = str(Path(mediaPath + r'/output'))
    UnhandledURLs = list()
    URIList = list()
    largeFileCount = 0
    currentPos = 1
        
    while notFile:
        clear()
        text = ["Please create a file called", "URL.txt",  "at", "and insert a URL at each line. Press enter when you are ready.", 
        "To return to the main menu, type 'menu'"]

        print(
            term.move_xy(int(W/2 - 38/2), int(H/2 - 2)) + text[0],
            term.cadetblue1 + text[1] + term.normal,
            text[2],
            term.move_xy(int(W/2 - len(mediaPath)/2), int(H/2)) + term.cadetblue1 + mediaPath + term.normal,
            term.move_xy(int(W/2 - len(text[3])/2), int(H/2 + 2)) + text[3],
            term.move_xy(int(W/2 - len(text[4])/2), int(H/2 + 4)) + text[4] + "\n\n"
            )

        userInput = input(">>")
        print()

        if userInput.lower() == "menu":
            return

        # Open the URL.txt file and create a list of URL's
        if os.path.isfile(mediaPath + r'/' + "URL.txt"):
            for line in fileinput.FileInput("URL.txt",inplace=1):
                if line.rstrip():
                    URIList.append(line)

            totalURLs = len(URIList)

            if totalURLs == 0:
                clear()

                text = ["There were no URL's found in", "URL.txt.", "Please make sure that there are URL's and that you have read/write permissions " +
                "set correctly.", "Press enter to return to the menu."]
                
                print(
                    term.move_xy(int(W/2 - 130/2), int(H/2 - 1)) + text[0],
                    term.cadetblue1 + text[1] + term.normal,
                    text[2],
                    term.move_xy(int(W/2 - len(text[3])/2), int(H/2 + 1)) + text[3]
                    )

                input("")
                break  
            
            # For each URL, download the media and determine if it needs compression
            for uriLine in URIList:
                uri = uriLine.rstrip()
                if validators.url(uri):
                    text = ["URI Found:", "[Youtube-DL]"]
                    
                    clear()
                    print(
                        term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 2)) + text[0],
                        term.move_xy(int(W/2 - len(uri)/2), int(H/2)) + term.cadetblue1 + uri + term.normal,
                        term.move_xy(int(W/2 - (len(str(currentPos)) + len(str(totalURLs)) + 10)/2), int(H/2 + 2)), currentPos, "out of", totalURLs,
                        "\n\n" + text[1]
                    )

                    # Download the media file
                    try:
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([uri])
                        # Obtain the file paths for creating the temp and output folders
                        filename = downFileName.encode('ascii','ignore').decode('ascii')
                        currentPos = currentPos+1
                    except FileExistsError:
                            os.remove(filename)
                            currentPos = currentPos+1
                    except:
                        if eMessage != "suppress":
                            eMessage = errorHandler(errorMessage, uri)
                        UnhandledURLs.append(uri + "\n")
                        currentPos = currentPos+1

                        clear()
                        text = "ERROR: unable to download last URL, skipping."

                        print(term.move_xy(int(W/2 - len(text[0])/2), int(H/2)) + term.brown1 + text + term.normal)
                        countdown(3)

            # Check if there are any files over 8MB
            filePathList = getListOfFiles(mediaPath)

            for fullFilePath in filePathList:
                fullFilePath = str(Path(fullFilePath)).encode('ascii','ignore').decode('ascii')
                if getFileSize(fullFilePath) > 8192.00:
                    largeFileCount = largeFileCount+1
            
            # Ask the user if they want to compress any files over 8MB
            if largeFileCount > 0:
                clear()
                text = "Download complete. Do you wish to compress the media? (y/n)"
                print(term.move_xy(int(W/2 - len(text)/2), int(H/2)) + text, end='\n\n')
            
                userInput = input(">> ")

                if userInput.lower() == "y":
                    currentPos = 0
                    
                    # Iterate through filePathList and determine if the file needs conversion
                    for fullFilePath in filePathList:
                        filename = str(Path(os.path.basename(fullFilePath)))
                        filePath = str(Path(os.path.dirname(fullFilePath)))
                        fullOutPath = str(Path(mediaPath + r'/output'))
                        fullOutFileName = str(Path(fullOutPath + r'/' + filename))
                        currentPos = currentPos+1

                        if os.path.isfile(fullFilePath):
                            if getFileSize(fullFilePath) > 8192.00:
                                convert(filename, filePath)
                                os.remove(fullFilePath)
                                clear()
                            else:
                                os.replace(fullFilePath, fullOutFileName)
        else:
            clear()
            text = ["URL.txt", "was not found. Please create", "and try again.", "Press enter to continue."]

            print(
                term.move_xy(int(W/2 - 59/2), int(H/2 - 1)), term.cadetblue1 + text[0] + term.normal, 
                text[1],
                term.cadetblue1 + text[0] + term.normal,
                text[2],
                term.move_xy(int(W/2 - len(text[3])/2), int(H/2 + 1)), text[3]
            )
            input()
            return

        clear()

        if len(UnhandledURLs) > 0:

            unsupportedURL = open("Unsupported URLs.txt", "w")
            unsupportedURL.writelines(UnhandledURLs)
            unsupportedURL.close()

            text = ["Procedure complete.", "Downloaded media has been saved to:", "Unavailable URLs have been saved to", "Unsupported URLs.txt", 
            "Press enter to continue"]

            print(
                term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 3)) + text[0],
                term.move_xy(int(W/2 - (len(text[1]) + len(outputPath))/2), int(H/2 - 1)) + term.palegreen + text[1], term.cadetblue1 + outputPath + term.normal,
                term.move_xy(int(W/2 - (len(text[2]) + len(mediaPath))/2), int(H/2 + 1)) + term.palegreen + text[2] + term.cadetblue1  + ":", mediaPath + term.normal
                )
            countdown(5)
            print(term.move_xy(int(W/2 - len(text[4])/2), int(H/2 + 3)) + text[4])

            input()
            clear()
        break

def openUnsupportedURLs():
    UnsupURLTextFile = str(Path(os.path.dirname(__file__) + r'/Unsupported URLs.txt'))

    if not os.path.isfile(UnsupURLTextFile):
        clear()

        text = ["Unsupported URLs.txt", "was not found. Returning to the main menu in:"]
        print(term.move_xy(int(W/2 - (20+45)/2), int(H/2)) + term.cadetblue1 + text[0], term.normal + text[1], end='')
        countdown(5)
        return

    counter = 1
    URLCounter = 0
    clear()

    text = ["All of the URLs in 'Unsupported URLs.txt' will be opened 10 at a time.", "Press enter to continue."]

    print(
        term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 1)) + text[0],
        term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 1)) + text[1]
    )
    input()

    URLs = list()
    for line in fileinput.FileInput(UnsupURLTextFile,inplace=1):
        if line.rstrip():
            URLs.append(line)

    if len(URLs) == 0:
        clear()

        text = ["There were no URLs detected.", "Press enter to continue."]

        print(
            term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 1)) + text[0],
            term.move_xy(int(W/2 - len(text[0])/2), int(H/2 + 1)) + text[1]
        )
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

def singleFileConvert():
    clear()
    notLoaded = True

    currentDir = os.getcwd()
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

        if userInput.lower() == "menu":
            exitStatus = 1
            break
        
        # Determine if a full path was entered or only a filename
        try: 
            if os.path.dirname(userInput) == "": # Filename was entered
                filename = userInput
                filePath = currentDir
                fullFilePath = str(Path(currentDir + r'/' + filename))
                outputDir = str(Path(currentDir + r'/output'))
            else: # Full path was entered
                filename = str(Path(os.path.basename(userInput) ))
                filePath = str(Path(os.path.dirname(userInput)))
                fullFilePath = str(Path(userInput))
                outputDir = str(Path(filePath + r'/output'))
                outputFile = str(Path(filePath + r'/output/' + filename))
                createOutputFolder(filePath)

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
            text = "Compressing"
            print(term.move_xy(int(W/2 - (len(text) + len(filename))/2), int(H/2)) + text, term.cadetblue1 + filename, term.normal)
            convert(filename, filePath)

            clear()
            text = ["The media file has been sucessfully compressed and is located at", "Returning to the main menu in"]
            print(
                term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 2)) + text[0], 
                term.move_xy(int(W/2 - len(outputDir)/2), int(H/2 )), term.bluecadet1 + outputDir, term.normal, "\n",
                term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 2)) + text[1], end=''
            )
            countdown(5)
            os.remove(fullFilePath)

        elif exitStatus == 0:
            clear()
            text = "The file did not need to be compressed. Returning to the main menu in"
            print(term.move_xy(int(W/2 - len(text)/2), int(H/2)) + text, end='')
            countdown(3)
            os.rename(fullFilePath, outputFile)
    except Exception as e:
        if userInput.lower() == "menu":
            clear()
            pass

def singleURLConvert():
    clear()
    notFile = True

    mediaPath = os.path.dirname(__file__)
    outputPath = str(Path(mediaPath + r'/output'))
    
    while notFile:
        url = "https://static1.e621.net/data/sample/89/85/8985342ea8ff4e4c4692f55e082aadb1.jpg"
        print(
            "Please enter a URL, then press enter.\n\nTo return to the main menu, type 'menu', then press enter.\n\n" +
            "Example URL:", term.link(url, url), "\n" + term.move_right(13) + "(CTRL click to open)", end='\n\n'
            )

        uri = input(">> ")
        print()

        if uri.lower() == "menu":
            return

        # Check if the URL is valid
        if not validators.url(uri):
            clear()
            print(term.brown1 + "The URL is not valid. Please check the syntax and try again.", term.normal, end='\n\n')
        else:
            clear()
            text = ["URI found:", uri, "| Downloading...", "[Youtube-DL]"]
            num = countStrings(text)
            print(term.move_xy(int(W/2 - num/2), int(H/2)), text[0], term.cadetblue1 + text[1], term.normal + text[2], "\n\n" + text[3])

            try:
                # Download the media file
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([uri])

                    filenamePath = str(Path(mediaPath + r'/' + downFileName.encode('ascii','ignore').decode('ascii')))
                    filename = os.path.basename(filenamePath)
                    outFile = str(Path(outputPath + r'/' + filename))

                    # Create an output directory
                    if not os.path.isdir(outputPath):
                        os.mkdir("output")
            except:
                errorHandler(errorMessage, uri)
                return

            fileSize = getFileSize(filenamePath)

            if fileSize > 8192.00:
                clear()
                text = "Download complete. Do you wish to compress the media? (y/n)"
                print(term.move_xy(int(W/2 - len(text)/2), int(H/2)) + text, end='\n\n')

                userInput = input(">> ")

                if userInput.lower() == "y":
                    clear()
                    text = "Compressing"
                    print(term.move_xy(int(W/2 - (len(text) + len(filename))/2), int(H/2)) + text, term.cadetblue1 + filename, term.normal)
                    convert(filename, filenamePath)

                    clear()
                    text = ["The media file has been sucessfully compressed and is located at", "Returning to the main menu in"]
                    print(
                        term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 2)) + text[0], 
                        term.move_xy(int(W/2 - len(outFile)/2), int(H/2 )), term.cadetblue1 + outFile, term.normal, "\n",
                        term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 2)) + text[1], end=''
                    )

                    countdown(5)
                    return
                else:
                    clear()
                    return
            else:
                try:
                    os.rename(filenamePath, outFile)
                except FileExistsError:
                    clear()

                    text = ["A file with the name", "already exists. Would you like to overwrite it? (Y/N)\n"]
                    textLength = countStrings(text) + len(filename)
                    
                    print(term.move_xy(int(W/2 - textLength/2), int(H/2)) + text[0], term.cadetblue1, filename, term.normal, text[1], end='\n\n')
                    userInput = input(">> ")

                    if userInput.lower() == "y":
                        shutil.copy(filenamePath, outFile)
                    elif userInput.lower() == "n":
                        clear()
                        return
                
            clear()

            text = ["Media successfully downloaded and is located at", "Returning to main menu in"]

            print(
                term.move_xy(int(W/2 - 47/2), int(H/2 - 2)) + text[0] + "\n\n", 
                term.move_xy(int(W/2 - len(outputPath)/2), int(H/2)) + term.cadetblue1, outputPath, term.normal, 
                term.move_xy(int(W/2 - 38/2), int(H/2 + 2)) + text[1], end=''
                )
            
            countdown(5)
            return

def spoilMedia(option):
    clear()

    mediaPath = workingDirectory()
    filePathList = getListOfFiles(mediaPath)

    if option == "spoil":
        text = ["I will now append 'SPOILER' to the files in", "Press enter to continue"]
        print(
            term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 2)) + text[0],
            term.move_xy(int(W/2 - len(mediaPath)/2), int(H/2)) + term.cadetblue1 + mediaPath + term.normal
        )
        countdown(3)
        print
        input(term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 2)) + text[1])

        for file in filePathList:
            os.replace(file, mediaPath + r'/' + "SPOILER_" + os.path.basename(file))
            pass
    elif option == "no spoil":

        text = ["I will now remove 'SPOILER' from the files in", "Press enter to continue"]
        print(
            term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 2)) + text[0],
            term.move_xy(int(W/2 - len(mediaPath)/2), int(H/2)) + term.cadetblue1 + mediaPath + term.normal
        )
        countdown(3)
        print(term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 2)) + text[1])
        input()

        for file in filePathList:
            newFileName = os.path.basename(file)
            os.replace(file, mediaPath + r'/' + newFileName[8:])
            pass

    clear()

    text = ["Procedure complete. The files are located at:", 
    "Note: The files may still be large. If that is the case, segment the files or use a different program/service.", 
    "Press Enter to continue."]

    print(
        term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 3)) + text[0],
        term.move_xy(int(W/2 - (len(mediaPath))/2), int(H/2 - 1)) + term.cadetblue1 + mediaPath + term.normal,
        term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 1)) + text[1],
        )

    countdown(5)
    print(term.move_xy(int(W/2 - len(text[2])/2), int(H/2 + 3)) + text[2])
    input()

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
        currentDir = str(Path(os.path.dirname(__file__)))
        text = "(CTRL click to open the path)"

        print("Please enter the directory that contains the media you wish to convert:\n")
        print("To return to the main menu, type 'menu'\n")
        print(
            "Current directory:", term.cadetblue1 + term.link(currentDir, currentDir) + "\n" + term.normal +
             term.move_x(0) + term.move_right(19) + text, end='\n\n'
        )

        newDirectory = input(">> ")

        if newDirectory.lower() == "menu":
            return "menu"
        else:
            newDirectory = str(Path(newDirectory)) # Change the media directory to the user specified directory

        if os.path.isdir(newDirectory):
            # Double triple check the user specified directory is correct
            clear()
            print("You have entered", term.cadetblue1 + term.link(newDirectory, newDirectory), term.normal + "Is this correct? [y/n]\n")
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
                createOutputFolder(newDirectory)
                return newDirectory
        else:
            clear()
            print(term.brown1 + "You have entered an invalid path. Please try again.\n" + term.normal)

# Logger for Youtube-DL
class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        global errorMessage
        errorMessage = msg

def downloadStatus(d):
    if d['status'] == 'finished': # Download status complete
        global downFileName
        origFileName = d['filename']

        print("\nDownloading complete.\n")
        downFileName = origFileName.encode('ascii','ignore').decode('ascii')


# Parameters for Youtube-DL.
# See https://github.com/ytdl-org/youtube-dl/blob/5014bd67c22b421207b2650d4dc874b95b36dda1/youtube_dl/YoutubeDL.py#L141
ydl_opts = {
    'outtmpl': f'%(id)s.%(ext)s',
    'restrictfilenames': True,
    'logger': MyLogger(),
    'progress_hooks': [downloadStatus],
}

# ---------------------------------

import distro
import magic
import psutil
import validators
import youtube_dl
import blessed
import datetime

from numpy import char
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