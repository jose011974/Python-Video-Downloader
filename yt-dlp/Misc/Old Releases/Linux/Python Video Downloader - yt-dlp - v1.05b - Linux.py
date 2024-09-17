#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
    Project Name: Python Video Downloader with yt-dlp support
    Date of Creation: 1/15/2023
    Last Updated: 2/1/24
    Python Version: Supports 3.7+
    Version: 1.05

    Updates:

        * Core Functionality
            * You no longer need to bake cookies to use this program
            * Scanning directories uses a comprehensive list vs manually scanning each file and directory
            * The title finally reflects the current script version
            * URL.txt no longer clears after scanning
            * Pip is now upgraded when updating dependencies
            * Certain menus have been re-formatted
            * Added extra error handling routines (errors can and will occur)
            * Change default CRF value to 20, users will need to use a different service if the file is still too large.
                * You can use programs such as Handbrake or ffmpeg.
            * Spoilering and Un-Spoilering no longer overwrite those with or without the prefix in their respective modes
                * For example, Spoiling no longer appends the prefix twice. Instead of 'SPOILER_SPOILER_filename' now you get
                  'SPOILER_filename' and vice versa
            * Tried to update error messages to be clear and concise. 

        * Misc
            * Variable names now use the following syntax: test_variable vs testVariable
            * Attempted to add useful comments and format code to be easier to read
            * Cleaned up unnecessary code
            * 'suppress' when encountering errors actually works now (turns out its been broken for a while, oopsie)

        * Hotfix - 2/12/24
            * NSFW Tweets are now handled properly if:
                * No active Twitter session is found in a supported browser
                * No supported browsers are detected in their default locations
                * Chrome is running while baking the cookies 
                    * An update does not allow external programs to access cookies while Chrome is running
"""

# Load startup libraries

import os
import platform
import shutil
import subprocess
import sys
import time
import webbrowser

from pathlib import Path

# Changes the working directory to the running script directory and turns slashes into backslashes

os.chdir(Path(__file__).parent.resolve()) 

# Used to filter out non-media files

file_types = (".jpeg", "jpg", ".png", ".gif", ".mp4", ".webm")

def clear():
    # Clear the screen

    command = 'clear' # Unix
    if platform.system() == "Windows": command = 'cls' # Windows
    os.system(command)

    title()

def convert(filename, filenamePath):
    output_path = str(Path(filenamePath + r'/output'))
    out_file = str(Path(output_path + r'/' + filename))
    in_file = str(Path(filenamePath + r'/' + filename))
    ext = os.path.splitext(filename)
    codec = ""
    
    # Show the time compression started.
    clear()
    now = datetime.datetime.now()
    text = ["Processing", "Time the Process started: " + now.strftime('%I:%M %p')]
    print(
        term.move_xy(int(W/2 - (len(text[0]) + len(filename))/2), int(H/2 + -4)) + text[0], term.cadetblue1 + filename + term.normal,
        term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 4)) + text[1])
    
    # Compress video
    if ext[1] == ".gif" or ext[1] == ".webm" or ext[1] == ".mp4":
        # Setup paths and codec options - TODO: Come up with a better algorithm as these parameters increase file size
        out_file = str(Path(output_path + r'/' + os.path.basename(ext[0]) + ".mp4"))
        codec = "-c:v libx264 -crf 20 -pix_fmt yuv420p"

        # Begin compression
        if platform.system() == "Windows":
            ff_path = "C:/ffmpeg/ffmpeg.exe"
            os.system(ff_path + ' -i "' + in_file + '" ' + codec + ' "' + out_file + '"') # Windows
        elif platform.system() == "Linux":
            os.system("ffmpeg" + ' -i "' + in_file + '" ' + codec + ' "' + out_file + '"') # Linux / Other OS

    # Compress images
    elif ext[1] == ".jpg":
        im = Image.open(in_file)
        im.save(out_file, optimize=True, quality="keep")
    elif ext[1] == ".png":
        im = Image.open(in_file)
        im.save(out_file, optimize=True)

    return out_file

def check_cookies(uri):
    # A website may require authentication in order to download media. This function checks Firefox and Chrome to determine if the website has
    # an active session. Other browsers are pending.

    browsers = ["chrome", "firefox"]
    counter = 0
    error_flag = ""

    # We try to download the URI using Chrome or Firefox by passing the respective name into yt-dlp

    while True:
        try:
            ydl_opts["cookiesfrombrowser"] = [browsers[counter], None, None, None]
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([uri])

            error_flag = "success"

            break

        except PermissionError:
            clear()

            print(term.brown1 + "ERROR: 'Chrome is Dumb':" + term.normal, 
                  "Due to recent updates, external programs are unable to access cookies from Google Chrome unless the browser is closed.\n\n" + 
                  "If you wish to download the current URL, please close Google Chrome fully and type 'retry'. Otherwise press enter to skip it.\n\n" +
                  "You may type 'suppress' to suppress future errors.")
            
            user_input = input(">> ")

            if user_input.lower() == "suppress":
                return "suppress"
            elif user_input.lower() == "retry":
                continue
            elif user_input.lower() == "":
                return "no_permission"
            else:
                clear()

                print("An invalid entry was deteced. Please try again.", end='')
                countdown(3)
                continue
            
        except FileNotFoundError:
            error_flag = "no_browser"
            counter = counter + 1
        except yt_dlp.DownloadError:
            error_flag = "no_session"
            counter = counter + 1

        if counter == 2:
            break
    
    return error_flag

def countdown(i):
    # Print a countdown timer by getting the location of the cursor and moving one unit on the X axis, 
    # then using a while loop to decriment the specified time
    cur_location = term.get_location()
    W = cur_location[1]
    H = cur_location[0]
    
    while i >= 0:
        print(term.move_xy(W + 1,H) + "(" + str(i) + ")")
        time.sleep(1)
        i = i - 1

def countStrings(text):
    # Counts chars in a list
    # num - counter
    # res - result
    # ele - element

    num = 0
    res = char.str_len(text)
    for ele in res:
        num = num + ele

    return num   

def errorHandler(error, uri):
    # yt-dlp provides a more sophisicated error handler. 
    # This function strips out the first 8 characters of the error message, then iterates through the error till a : is found, 
    # at which point the remaining string is compared to a list of pre-defined error messages, 
    # and the appropriate explination of why the error occured is shown to the user.

    counter = -1
    error_message = ""
    error = error[7:]

    # Find a : and remove the prefix of the error message
    for element in error:
        counter = counter + 1
        if element == ":": 
            error_message = error[counter + 2:]
            break
    
    # Show the user an explination of the error and any possible steps they can take to resolve it.

    clear()
    
    if error_message == "":
        print(term.brown1 + "ERROR 0:" + term.normal, "An unknown error has occured. Please create an issue at https://github.com/jose011974/Download-Compress-Media/issues and \n")
        print("include the URL and error message found below in your issue:\n")
        print(uri, "\n")
        print(error)

    # The tweet does not contain a video file, and cannot be downloaded. This is a yt-dlp issue, not mine

    elif error_message == "No video could be found in this tweet":
        print(term.brown1 + "ERROR 1:" + term.normal, "The tweet does not contain a video.",
              "yt-dlp cannot download images for whatever reason. Pester them to fix the issue, not me.")

    # Author of tweet has been suspended (banned)

    elif error_message == "Error(s) while querying API: User has been suspended.":
        print(term.brown1 + "ERROR 2:" + term.normal, "The user that posted this tweet has been suspended,",
              "and all tweets are no longer accessible by the public.")
        print("\nURL:", uri)

    # The Tweet was not found. You may need to sign in because Elon.

    elif error_message == "Unable to download webpage: HTTP Error 404: Not Found (caused by <HTTPError 404: 'Not Found'>); please report this issue on  https://github.com/yt-dlp/yt-dlp/issues?q= , filling out the appropriate issue template. Confirm you are on the latest version using  yt-dlp -U":
        result = check_cookies(uri)
        clear()

        if result == "no_browser":
            print(term.brown1 + "ERROR 404-a:" + term.normal, "The Tweet could not be found. This may be fixed by signing into a Twitter account.",
                    "However, a valid browser was not found.\n\n" +
                    "You must install Chrome or Firefox and log in to download this tweet. We apologize for any inconvenience.")        
        elif result == "no_session":
            print(term.brown1 + "ERROR 404-a:" + term.normal, "The Tweet could not be found. This may be fixed by signing into a Twitter account.",
                    "However, valid session could not be authenticated.\n\n" + 
                    "You'll need to sign into Twitter using either Chrome or Firefox. We apologize for any inconvenience.")
        elif result == "no_permission":
            return ""
        elif result == "suppress":
            return "suppress"
        else:
            return "success"
    
    # The JSON data for the tweet could not be found. You may need to sign in because Elon

    elif error_message == "Unable to download JSON metadata: HTTP Error 404: Not Found (caused by <HTTPError 404: 'Not Found'>); please report this issue on  https://github.com/yt-dlp/yt-dlp/issues?q= , filling out the appropriate issue template. Confirm you are on the latest version using  yt-dlp -U":
        if result == "no_browser":
            print(term.brown1 + "ERROR 404-b:" + term.normal, "The Tweet's JSON data could not be found.",
                    "This may be fixed by signing into a Twitter account, however, a valid browser could not be found.\n\n" +
                    "You must install either Chrome or Firefox and log in to download this tweet. We apologize for any inconvenience.")        
        elif result == "no_session":
            print(term.brown1 + "ERROR 404-b:" + term.normal, "The Tweet's JSON data could not be found.",
                    "This may be fixed by signing into a Twitter account. However, a valid Twitter session could not be authenticated.\n\n" +
                    "You'll need to sign into Twitter using either Chrome or Firefox. We apologize for any inconvenience.")
        elif result == "no_permission":
            return ""
        elif result == "suppress":
            return "suppress"
        else:
            return "success"
    
    # The tweet could not be found. You may need to sign in because Elon.

    elif error_message == "HTTP Error 404: Not Found":
        result = check_cookies(uri)
        clear()

        if result == "no_browser":
            print(term.brown1 + "ERROR 404-c:" + term.normal, "The Tweet could not be found.",
                    "This may be fixed by signing into a Twitter account. However, a valid browser could not be found.\n\n" +
                    "You must install either Chrome or Firefox and log in to download this tweet. We apologize for any inconvenience.")        
        elif result == "no_session":
            print(term.brown1 + "ERROR 404-c:" + term.normal, "The Tweet could not be found.",
                    "This may be fixed by signing into a Twitter account. However, a valid Twitter session could not be authenticated.\n\n" +
                    "You'll need to sign into Twitter using either Chrome or Firefox. We apologize for any inconvenience.")
        elif result == "no_permission":
            return ""
        elif result == "suppress":
            return "suppress"
        else:
            return "success"
        
    # Viewing NSFW tweets requires a Twitter account to view. You need to sign in to view tweets because Elon.

    elif error_message == "Requested tweet may only be available when logged in. Use --cookies, --cookies-from-browser, --username and --password, --netrc-cmd, or --netrc (twitter) to provide account credentials":
        result = check_cookies(uri)
        clear()

        if result == "no_browser":
            print(term.brown1 + "ERROR 4a:" + term.normal, "Twitter requires you to log in to view most NSFW tweets.",
                    "However, a valid browser could not be found.\n\n"
                    "You must install either Chrome or Firefox and log in to download this tweet. We apologize for any inconvenience.")
        elif result == "no_session":
            print(term.brown1 + "ERROR 4b:" + term.normal, "Twitter requires you to log in to see most NSFW tweets.",
                    "However, a valid Twitter session could not be authenticated.\n\n" +
                    "You'll need to sign into Twitter using either Chrome or Firefox. We apologize for any inconvenience.")
        elif result == "no_permission":
            return ""
        elif result == "suppress":
            return "suppress"
        else:
            return "success"

    # Viewing NSFW tweets requires a twitter account to view. You need to sign in to Twitter because Elon.

    elif error_message == "NSFW tweet requires authentication. Use --cookies, --cookies-from-browser, --username and --password, --netrc-cmd, or --netrc (twitter) to provide account credentials":
        result = check_cookies(uri)
        clear()

        if result == "no_browser":
            print(term.brown1 + "ERROR 4c:" + term.normal, "Twitter requires you to log in to view most NSFW tweets.\n\n" + 
                    "A valid browser could not be found.\n\n" + 
                    "You must install either Chrome or Firefox and log in to download this tweet. We apologize for any inconvenience.")
        elif result == "no_session":
            print(term.brown1 + "ERROR 4d:" + term.normal, "Twitter now requires you to log in to see most NSFW tweets.",
                    "However, a valid Twitter session could not be authenticated.\n\n" +
                    "You'll need to sign into Twitter using either Chrome or Firefox. We apologize for any inconvenience.")
        elif result == "no_permission":
            return ""
        elif result == "suppress":
            return "suppress"
        else:
            return "success"

    # Cookies could not be found. This may occur when a supported browser is not installed in the default location.
    # Regardless, check_cookies will scan Chrome and Firefox in their default locations for a valid session.
        
    elif error_message == "Profile Folder not Found.":
        result = check_cookies(uri)
        clear()

        if result == "no_browser":
            print(term.brown1 + "ERROR 5a:" + term.normal, "The URL could not be authenticated as Chrome or Firefox are not installed.\n\n" + 
                  "In order to download this URL, you will need to install Chrome or Firefox in their default location\n\n" +
                "and log in to the respective website. We apologize for any inconvenience.")
        elif result == "no_session":
            print(term.brown1 + "ERROR 5b:" + term.normal, "The URL could not be authenticated as a valid session was not found.\n\n" +
                "You will need to have Chrome or Firefox installed in their default location, signed into the respective website,",
                 "and try again. We apologize for any inconvenience.")
        elif result == "no_permission":
            return ""
        elif result == "suppress":
            return "suppress"
        else:
            return "success"
    
    # A fatal error has occured. Just in case its with a specific tweet, we allow the program to continue exectution.
        
    else:
        print(term.brown1 + "ERROR 0a:" + term.normal, "An fatal error has occured. Please create an issue at https://github.com/jose011974/Download-Compress-Media/issues and \n")
        print("include the URL and error message found below in your issue:\n")
        print(uri, "\n")
        print(error)

    print("\nIf you would like to supress error messages, type 'suppress', otherwise, press enter to continue.\n")

    user_input = input(">> ")

    if user_input.lower() == "suppress":
        return user_input
            
    clear()

def getFileSize(file):
    # Get the file size and convert to MB

    file_size = os.path.getsize(file)
    file_size = float("{:.2f}".format(file_size / 1024))

    return file_size

def getListOfFiles(folder): 
    # Using a comprehensive list, we can filter out valid file names and return them as a list

    # Scan the folder provided by the user
    file_list = os.listdir(folder)

    # For each element in f, check if f is a valid file by:
        # 1. Checking if the joined path (folder + f) points to a file
        # 2. The lowercase version of the file ends with any specified extension in file_types
    filenames = [
    f
    for f in file_list
        if os.path.isfile(
            os.path.join(folder, f))
            and
            f.lower().endswith(file_types)
    ]

    return filenames

    # Credit to the original source code: 
    # https://github.com/PySimpleGUI/PySimpleGUI/blob/1fa911cafee687ef50e024b580d5351c398ef7d1/DemoPrograms/Demo_Img_Viewer.py#L36


def main():
    while True:

        os.chdir(Path(__file__).parent.resolve()) # Change the path back to the path the script is running from

        clear()

        print(
            "This script provides the ability to download and compress local/online media. Single and multiple file/URL modes are avaiable to you." +
            "\n\nThe following media types have been tested: " + term.cadetblue1 + "jpg/jpeg, png, gif, mp4, and webm." + term.normal +
            "\n\nAny other formats should work, however they have been untested. " + term.orangered + "\n\nProceed at your own risk. " + 
            "I am not responsible for any loss of data due to neglect. This script is in beta, so bugs WILL be present." + term.normal +
            "\n\nPlease type the option that works best for you and press enter:\n\n" + term.cadetblue1 + "Note: Compression only works on files " +
            "larger than 25 MB, as Discord, a popular messaging service, does not allow regular accounts to upload files larger than 25 MB without paying.\n" + term.normal
        )
        
        print("1. Single File")
        print("2. Multiple Files")
        print("3. Single URL")
        print("4. Multiple URLs")
        print("5. Spoil Media")
        print("6. No Spoil Media")
        print("7. Open Unsupported URLs")
        print("8. Help")
        print("9. Exit")
        print("0. Update Dependencies\n")

        try:
            user_input = int(input(">> "))

            if user_input == 1:
                if no_comp == True:
                    noFFMPEG(0)
                elif no_comp == False:
                    singleFileConvert()
            elif user_input == 2:
                if no_comp == True:
                    noFFMPEG(0)
                elif no_comp == False:
                    multipleFileConvert()
            elif user_input == 3:
                singleURLConvert()
            elif user_input == 4:
                multipleURLConvert()
            elif user_input == 5:
                spoilMedia(1)
            elif user_input == 6:
                spoilMedia(0)
            elif user_input == 7:
                openUnsupportedURLs()

            elif user_input == 8:
                webbrowser.open("https://github.com/jose011974/Download-Compress-Media", new=1)

                clear()

                print("The Github page should have opened. If it did not, please go to https://github.com/jose011974/Download-Compress-Media (CTRL click to open)\n")
                print("Press enter to continue.\n")
                input()

            elif user_input == 9:
                clear()
                print("Exiting...\n")
                sys.exit()
            elif user_input == 0:
                clear()

                text = "Updating Dependencies..."
                print(term.move_xy(int(W/2 - len(text)/2), int(H/2)) + term.darkseagreen1 + text + term.normal + "\n")
                time.sleep(1)

                packages = ["blessed", "numpy", "python-magic", "Pillow", "psutil", "requests", "validators", "yt-dlp"]
                if platform.system() == "Windows":
                    packages.append("python-magic-bin")

                for p in packages:
                    try:
                        subprocess.check_call([sys.executable, "-m", "pip", "install", p, "--upgrade", "--user"])
                    except Exception as e:
                        clear()

                        print("An error has occured while updating packages:\n\n", e, "\n\n Please create an issue at",
                              "https://github.com/jose011974/Python-Video-Downloader/issues")
                
                 # In case there is an update available for pip, we install it.
                try:
                    if platform.system() == "Linux":
                        subprocess.check_call(['python3', '-m', 'pip', 'install', '--upgrade', 'pip'])
                    elif platform.system() == "Windows":
                        subprocess.check_call(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])
                except Exception as e:
                    clear()

                    print("An error has occuired when upgrading pip. Pip will not be upgraded.")

                clear()
                text = "Dependencies updated."
                print(term.move_xy(int(W/2 - len(text)/2), int(H/2)) + term.darkseagreen1 + text + term.normal, end='')

                countdown(3)
            
            clear()
        except ValueError:
            clear()
            print("You have entered an invalid entry. Please try again.\n")
            continue

def multipleFileConvert():
    # Set-up paths
    media_path = str(Path(workingDirectory()))

    if media_path == "menu":
        clear()
        return

    clear()
    text = ["Counting files...", "(The program may freeze for a few seconds if there are a large amount of files)"]
    print(
        term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 1)) + 
        text[0] +
        term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 1)) + 
        text[1]
        )

    filenames = getListOfFiles(media_path)
    total_files = len(filenames)
    current_pos = 0
    
    clear()

    text = ["Located", "files. Processing..."]
    print(term.move_xy(int(W/2 - 23/2), int(H/2)) + text[0], term.cadetblue1 + str(total_files) + term.normal, text[1], end='')

    countdown(3)
    clear()

    # Iterate through the files in filenames and determine if they need compression
    for filename in filenames:
        current_pos = current_pos+1
        duplicate_file = str(Path(output_path + r'/old_' + filename))
        new_file = str(Path(output_path + r'/' + filename))

        if os.path.isfile(filename):
            if getFileSize(filename) > 25600.00:
                    text = "Current file: "
                    text2 = " | " + str(getFileSize(filename)) + " MB | File " + str(current_pos) + " of " + str(total_files) + "\n"
                    print(term.move_xy(int(W/2 - (len(text) + len(filename) + len(text2))/2), int(H/2 - 2)) + text + 
                    term.cadetblue1 + filename + term.normal + text2)
                    convert(filename, media_path)
                    # Leave the old files in case the converted files have issues
                    shutil.move(filename, duplicate_file)
            else:
                # Move the files as they did not need compression
                shutil.move(filename, new_file)
    
    clear()       
    text = ["Procedure complete. The files are located at:", 
            "Note: The files may still be large. If that is the case, segment the files or use a different program/service.", 
            "Press Enter to continue."]

    print(
        term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 3)) + text[0],
        term.move_xy(int(W/2 - (len(media_path))/2), int(H/2 - 1)) + term.cadetblue1 + media_path + term.normal,
        term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 1)) + text[1], end=''
        )

    countdown(5)
    print(term.move_xy(int(W/2 - len(text[2])/2), int(H/2 + 3)) + text[2])
    input()

    clear()

def multipleURLConvert():
    error_message = ""
    non_file = True
    media_path = os.getcwd()
    out_path = str(Path(media_path + r'/output'))
    url_txt_path = str(Path(media_path + r"/URL.txt"))
    unhand_url_txt_path = str(Path(media_path + r"/Unsupported URLs.txt"))
    unhandled_urls = list()
    uri_list= list()
    large_file_count = 0
    current_pos = 1
        
    while non_file:
        clear()
        text = ["This program uses a text file called", 
                "URL.txt", 
                "to download multiple URL links.", 
                "Please open", 
                "and type a URL in each line. Save the text file and press enter when you are ready.",
                "To return to the main menu, type 'menu'"]

        # 85 comes from adding the lengths of index 0-3 together

        # Output:

        # This program uses a text file called 'URL.txt' to download multiple URL links. Please open
        # $path
        # and type a URL in each line. Save the text file and press enter when you are ready."
        # To return to the main meny, type 'menu'
        print(
            term.move_xy(int(W/2 - 85/2), int(H/2 - 2)) + text[0], term.cadetblue1 + text[1] + term.normal, text[2], text[3],
            term.move_xy(int(W/2 - len(media_path)/2), int(H/2)) + term.cadetblue1 + media_path + r'/' + text[1], term.normal,
            term.move_xy(int(W/2 - len(text[4])/2), int(H/2 + 2)) + text[4],
            term.move_xy(int(W/2 - len(text[5])/2), int(H/2 + 4)) + text[5] + "\n\n"
            )

        user_input = input(">> ")
        print()

        if user_input.lower() == "menu":
            return

        # Open URL.txt and create a list of URL's
        if os.path.isfile(url_txt_path):
            with open(url_txt_path, 'r') as file:
                lines = file.readlines()

            for line in lines:
                uri_list.append(line.strip())

            total_urls = len(uri_list)

            if total_urls == 0:
                clear()

                text = ["There were no URL's found in", "URL.txt.", "Please make sure that there are URL's and that you have read/write permissions" +
                "set correctly.", "Press enter to return to the menu."]

                # Output:

                # There were no URL's found in URL.txt. Please make sure that there are URL's and that you have read/write permissions"
                # set correctly.
                # Press enter to return to the main menu
                
                print(
                    term.move_xy(int(W/2 - 130/2), int(H/2 - 1)) + text[0],
                    term.cadetblue1 + text[1] + term.normal,
                    text[2],
                    term.move_xy(int(W/2 - len(text[3])/2), int(H/2 + 1)) + text[3]
                    )

                input("")
                break  
            
            # For each URL, download the media and determine if it needs compression
            for uri in uri_list:
                if validators.url(uri):
                    text = ["URI Found:", "[yt-dlp]"]

                    # Output:

                    # URI Found: $uri
                    # $current_pos out of $total_urls
                    #[yt-dlp]

                    
                    clear()
                    print(
                        term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 2)) + text[0],
                        term.move_xy(int(W/2 - len(uri)/2), int(H/2)) + term.cadetblue1 + uri + term.normal,
                        term.move_xy(int(W/2 - (len(str(current_pos)) + len(str(total_urls)) + 10)/2), int(H/2 + 2)), current_pos, "out of", total_urls,
                        "\n\n" + text[1]
                    )

                    time.sleep(1)
                    ydl_opts["cookiesfrombrowser"] = None

                    # Download the media file using the parameters set in ydl_opts, then increment current_pos by 1
                    try:
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([uri])
                        current_pos = current_pos+1
                    except FileExistsError:
                        os.remove(filename)
                        current_pos = current_pos+1
                    except PermissionError as e:
                        error_message = errorHandler(e.args[0], uri)

                        if error_message == "success":
                            current_pos = current_pos+1
                            continue

                        current_pos = current_pos+1

                        clear()
                        text = "ERROR: unable to download last URL, skipping."

                        print(term.move_xy(int(W/2 - len(text)/2), int(H/2)) + term.brown1 + text + term.normal, end='')
                        countdown(3)
                    except yt_dlp.DownloadError as e:
                        error_message = errorHandler(e.args[0], uri)

                        if error_message == "success":
                            current_pos = current_pos+1
                            continue

                        current_pos = current_pos+1

                        clear()
                        text = "ERROR: unable to download last URL, skipping."

                        print(term.move_xy(int(W/2 - len(text)/2), int(H/2)) + term.brown1 + text + term.normal, end='')
                        countdown(3)
                    except Exception as e:
                        try:
                            if error_message != "suppress":
                                error_message = errorHandler(e.args[0], uri)
                                unhandled_urls.append(uri + "\n")
                            current_pos = current_pos+1
                        except UnboundLocalError:
                            clear()
                            print("A fatal error has occured. The URL cannot be downloaded because:\n")
                            print(str(e) + "\n")
                            print("Please create an issue at the GitHub support page for this program. If the error is self-explanitory, " +
                                    "creating an issue is NOT required.\n")
                            print("GitHub support page: https://github.com/jose011974/Python-Video-Downloader/issues\n")
                            print("Press enter to continue.\n")
                            input()

                            if error_message == "success":
                                current_pos = current_pos+1
                                continue

                            current_pos = current_pos+1

                            clear()
                            text = "ERROR: unable to download last URL, skipping."

                            print(term.move_xy(int(W/2 - len(text)/2), int(H/2)) + term.brown1 + text + term.normal, end='')
                            countdown(3)

            # If ffmpeg is not available, do not allow the user to compress media.
            if no_comp == True:
                noFFMPEG(1)
                return

            filename_list = getListOfFiles(media_path)

            # Check if there are any files over 8MB
            for filename in filename_list:
                filename = str(Path(filename)).encode('ascii','ignore').decode('ascii')
                if getFileSize(filename) > 25600.00:
                    large_file_count = large_file_count+1
            
            # Ask the user if they want to compress any files over 8MB
            if large_file_count > 0:
                clear()
                text = "Download complete. Do you wish to compress the media? (y/n)"
                print(term.move_xy(int(W/2 - len(text)/2), int(H/2)) + text, end='\n\n')
            
                user_input = input(">> ")

                if user_input.lower() == "yes" or user_input.lower() == "y":
                    current_pos = 0
                    
                    # Iterate through filePathList and determine if the file needs conversion
                    for filename in filename_list:
                        file_path = str(Path(os.path.dirname(filename)))
                        downloaded_file = str(Path(out_path + r'/' + filename))
                        current_pos = current_pos+1

                        if os.path.isfile(filename):
                            if getFileSize(filename) > 25600.00:
                                convert(filename, file_path)
                                os.remove(filename)
                                clear()
                            else:
                                shutil.move(filename, downloaded_file)
                else:
                    # Iterate through the file list and move the media to the 'output' folder
                    for filename in filename_list:
                        file_path = str(Path(os.path.dirname(filename)))
                        downloaded_file = str(Path(out_path + r'/' + filename))

                        shutil.move(filename, downloaded_file)
            else:
                # Iterate through the file list and move the media to the 'output' folder
                for filename in filename_list:
                    file_path = str(Path(os.path.dirname(filename)))
                    downloaded_file = str(Path(out_path + r'/' + filename))

                    shutil.move(filename, downloaded_file)
                    # os.remove(filename)
        else:
            clear()
            text = ["URL.txt", "was not found. Please create", "and try again.", "Press enter to continue."]

            # Output:

            # URL.txt was not found.
            # Please create URL.txt and try again.
            # Press enter to continue

            print(
                term.move_xy(int(W/2 - 59/2), int(H/2 - 1)), term.cadetblue1 + text[0] + term.normal, 
                text[1],
                term.cadetblue1 + text[0] + term.normal,
                text[2],
                term.move_xy(int(W/2 - len(text[3])/2), int(H/2 + 1)), text[3], end='')
            input()
            return

        clear()

        text = ["Procedure complete.", "Downloaded media has been saved to:", "Press enter to continue"]

        # Output:

        # Procedure Complete.
        # Downloaded media has been saved to: $path
        # Press enter to continue
        print(
            term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 3)) + text[0], 
            term.move_xy(int(W/2 - (len(text[1]) + len(out_path))/2), int(H/2 - 1)) + term.palegreen + text[1], term.cadetblue1 + out_path + term.normal,
            term.move_xy(int(W/2 - len(text[2])/2), int(H/2 + 1)) + text[2], end='')
        input()

        if len(unhandled_urls) > 0:

            unsupportedURL = open(unhand_url_txt_path, "w")
            unsupportedURL.writelines(unhandled_urls)
            unsupportedURL.close()

            text = ["Unsaved URLs have been saved to", "Unsupported URLs.txt", "Press enter to continue."]
            
            # Output:

            # Unsaved URLs have been saved to
            # $path/Unsupported URLs.txt
            # Press enter to continue

            print(
                term.move_xy(int(W/2 - (len(text[0]) + len(media_path) + len(text[1]))/2), int(H/2 + 1)) + term.palegreen + text[0] + term.cadetblue1  + ":", 
                media_path + r'/' + text[1]  + term.normal,
                term.move_xy(int(W/2 - len(text[2])/2), int(H/2 + 3)) + text[2], end='')
            input()

        clear()

        text = ["Would you like to clear", "URL.txt", "?", "(y/n)"]

        print(term.move_xy(int(W/2 - countStrings(text)/2), int(H/2 + 1)), 
            term.palegreen + text[0], 
            term.cadetblue1 + text[1] + term.palegreen + text[2], 
            text[3] + term.normal, "\n"
            )
        
        user_input = input(">> ")
        
        if user_input.lower() == "yes" or user_input == "y":
            with open(url_txt_path, 'w') as file:
                file.write("")

            clear()

            text = ["URL.txt", "has been cleared. Returning to main menu in"]

            print(term.move_xy(int(W/2 - countStrings(text)/2), int(H/2 + 1)), 
                  term.cadetblue1 + text[0], 
                  term.palegreen + text[1] + term.normal, end='')

        elif user_input.lower() == "no" or user_input == "n" or user_input == "":

            clear()

            text = ["URL.txt", "has", "NOT", "been cleared. Returning to main menu in"]

            print(
                term.move_xy(int(W/2 - countStrings(text)/2), int(H/2 + 1)),
            term.cadetblue1 + text[0],
            term.palegreen + text[1],
            term.red + text[2], 
            term.palegreen + text[3] + term.normal, end='')

        countdown(3)

        break

def noFFMPEG(i):

    clear()
    text = "FFMPEG is not installed. This option has been disabled.", "FFMPEG is not installed. You are unable to compress media at this time."

    print(
        term.move_xy(int(W/2 - len(text[i])/2), 
                     int(H/2)) + term.brown1 + text[i] + term.normal, end='')
    countdown(3)

def openUnsupportedURLs():
    un_url_textfile = 'Unsupported URLs.txt'

    if not os.path.isfile(un_url_textfile):
        clear()

        text = ["Unsupported URLs.txt", "was not found. Returning to the main menu in:"]
        print(term.move_xy(int(W/2 - 65/2),
                           int(H/2)) + term.cadetblue1 + text[0],
                           term.normal + text[1], end='')
        countdown(5)
        return
    
    URLs = list()
    with open('Unsupported URLs.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        URLs.append(line.strip())

    if len(URLs) == 0:
        clear()

        text = ["There were no URLs detected.", "Press enter to continue."]

        print(
            term.move_xy(int(W/2 - len(text[0])/2), 
                         int(H/2 - 1)) + text[0],
            term.move_xy(int(W/2 - len(text[1])/2), 
                         int(H/2 + 1)) + text[1])
        input()
        return

    counter = 1
    url_counter = 0
    clear()

    text = ["All of the URLs in 'Unsupported URLs.txt' will be opened 10 at a time.", "Press enter to continue."]

    print(
        term.move_xy(int(W/2 - len(text[0])/2), 
                     int(H/2 - 1)) + text[0],
        term.move_xy(int(W/2 - len(text[1])/2), 
                     int(H/2 + 1)) + text[1]
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
            url_counter = url_counter + 1

        if url_counter >= 10:
            clear()
            print("Opened 10 URLs. Press enter to continue.")
            input()
            url_counter = 0

    clear()
    print("Process complete. Press enter to continue.")

def singleFileConvert():
    not_loaded = True
    current_dir = os.getcwd()
    full_file_path = ""
    filename = ""
    file_path = ""
    exit_status = 0

    clear()
        
    while not_loaded:
        example_paths = [r"C:\Your Mother is a Spy.mp4", r"/media/Blunt/Your Mother is a spy.mp4"]

        print("Please enter the path of the file. If the file is in the same directory as this script, type the file name instead.")
        print("\nTo return to the main menu, type 'menu'.\n")

        if platform.system() == "Windows":
            print("Example:", term.cadetblue1 + example_paths[0] + "\n" + term.normal) 
        else:
            print("Example:", term.cadetblue1 + example_paths[1] + "\n" + term.normal)

        user_input = input(">> ").encode('ascii','ignore').decode('ascii')

        if user_input.lower() == "menu":
            exitStatus = 1
            break
        
        # Determine if a full path was entered or only a filename
        try: 
            if os.path.dirname(user_input) == "": # Filename was entered
                filename = user_input
                file_path = current_dir
                full_file_path = str(Path(current_dir + r'/' + filename))
                output_dir = str(Path(current_dir + r'/output'))
            # Full path was entered
            else: 
                filename = str(Path(os.path.basename(user_input) ))
                file_path = str(Path(os.path.dirname(user_input)))
                full_file_path = str(Path(user_input))
                output_dir = str(Path(file_path + r'/output'))
                output_file = str(Path(output_dir + r'/' + filename))

            if os.path.isfile(full_file_path):
                not_loaded = False
            else:
                clear()
                if full_file_path == "":
                    print(term.brown1 + "No path was entered. Please try again.\n" + term.normal)
                    continue
                elif user_input == "":
                    clear()
                    print(term.brown1 + "Nothing was entered. Please try again.\n" + term.normal)
                    continue
                else:
                    print(term.cadetblue1 + full_file_path + term.normal + " " + term.brown1 + "was not found. \n\nPlease make sure the filename was typed correctly and try again.\n")
                    print("If the filename has some special characters such as emojis, you must rename the file to remove such characters.\n" + term.normal)
                    continue

            if not_loaded == True:
                full_file_path = ""
                filename = ""
                file_path = ""

                clear()
                print(term.cadetblue1 + full_file_path, term.brown1 + "is not a valid media file. Please try again.\n")
        except UnboundLocalError as e:
            clear()
            print(term.brown1 + "No valid file name or path was entered. Please try again.\n")

    try:
        # Create output folder if it doesn't exist
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # Determine if the media file needs compression
        if getFileSize(full_file_path) > 25600.00:
            clear()
            text = "Compressing"
            print(term.move_xy(int(W/2 - (len(text) + len(filename))/2), int(H/2)) + text, 
                               term.cadetblue1 + filename, term.normal)
            time.sleep(1)
            convert(filename, file_path)

            clear()
            text = ["The media file has been sucessfully compressed and is located at", "Returning to the main menu in"]

            # Output:

            # The media file has successfully compressed and is located at:
            # $path
            # Returning to the main menu in $countdown
            print(
                term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 2)) + text[0], 
                term.move_xy(int(W/2 - len(output_dir)/2), int(H/2 )), term.bluecadet1 + output_dir + term.normal, "\n",
                term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 2)) + text[1], end=''
            )
            countdown(5)
            os.remove(full_file_path)

        elif exit_status == 0:
            clear()
            text = "The file did not need to be compressed. Returning to the main menu in"
            print(term.move_xy(int(W/2 - len(text)/2), int(H/2)) + text, end='')
            countdown(3)
            os.rename(full_file_path, output_file)
    except Exception as e:
        if user_input.lower() == "menu":
            clear()
            pass

def singleURLConvert():
    media_path = os.getcwd()
    output_path = str(Path(media_path + r'/output'))
    not_a_file = True
    error_message = ""
    
    clear()
    
    while not_a_file:

        # This url is no longer active. If anyone manages to find what this image was, let me know!
        # https://static1.e621.net/data/sample/89/85/8985342ea8ff4e4c4692f55e082aadb1.jpg

        url = "https://static1.e621.net/data/e9/3d/e93d6b83f964b3f85e4716c8a862ca67.png"
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
            # This snippet allows the text in the tuple to accomodate various URI sizes.
            clear()
            text = ["URI found:", uri, "| Downloading...", "[yt-dlp]"]
            num = countStrings(text)
            print(term.move_xy(int(W/2 - num/2), int(H/2)), text[0], term.cadetblue1 + text[1], term.normal + text[2], "\n\n" + text[3])

            try:
                # Download the media file
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([uri])
                    time.sleep(1)

            except FileNotFoundError:
                error_message = "No cookies for you!: Profile Folder not Found."
                errorHandler(error_message, uri)
            except Exception as e:
                try:
                    if error_message != "suppress":
                        error_message = errorHandler(e.args[0], uri)

                        clear()
                        text = "ERROR: unable to download last URL, skipping."

                        print(term.move_xy(int(W/2 - len(text)/2), int(H/2)) + term.brown1 + text + term.normal, end='')
                        countdown(3)
                        return
                except Exception as e:
                    clear()
                    print("A fatal error has occured. The URL cannot be downloaded because:\n")
                    print(str(e.args[0]) + "\n")
                    print("Please create an issue at the GitHub support page for this program. If the error is self-explanitory, " +
                            "creating an issue is NOT required.\n")
                    print("GitHub support page: https://github.com/jose011974/Python-Video-Downloader/issues\n")
                    print("Press enter to continue.\n")
                    input()
            
            if error_message == "":
                file_path_list = getListOfFiles(media_path)

                for full_path in file_path_list:
                    file_path = os.path.dirname(full_path)
                    filename = os.path.basename(full_path)
                    out_file = str(Path(output_path + r'/' + filename))

                    file_size = getFileSize(full_path)

                    if file_size > 25600.00:
                        if no_comp == True:
                            noFFMPEG(1)
                            return

                        clear()
                        text = "Download complete. Do you wish to compress the media? (y/n)"
                        print(term.move_xy(int(W/2 - len(text)/2), int(H/2)) + text, end='\n\n')

                        user_input = input(">> ")

                        if user_input.lower() == "y":
                            clear()
                            text = "Compressing"
                            print(term.move_xy(int(W/2 - (len(text) + len(filename))/2), int(H/2)) + 
                                  text, 
                                  term.cadetblue1 + filename, 
                                  term.normal)
                            convert(filename, file_path)

                            clear()
                            text = ["The media file has been sucessfully compressed and is located at", "Returning to the main menu in"]
                            print(
                                term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 2)) + text[0], 
                                term.move_xy(int(W/2 - len(out_file)/2), int(H/2)), term.normal, "\n",
                                term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 2)) + text[1], end=''
                            )

                            countdown(5)
                            return
                        else:
                            try:
                                shutil.move(full_path, out_file)
                            except shutil.SameFileError:
                                clear()

                                text = ["A file with the name", "already exists. Would you like to overwrite it? (Y/N)\n"]
                                text_length = countStrings(text) + len(filename)
                                
                                print(term.move_xy(int(W/2 - text_length/2), int(H/2)) + 
                                      text[0], 
                                      term.cadetblue1, filename, term.normal, 
                                      text[1], end='\n\n')
                                user_input = input(">> ")

                                if user_input.lower() == "y":
                                    shutil.move(full_path, out_file)
                                elif user_input.lower() == "n":
                                    clear()

                                return
                    else:
                        try:
                            shutil.move(full_path, out_file)
                        except shutil.SameFileError:
                            clear()

                            text = ["A file with the name", "already exists. Would you like to overwrite it? (Y/N)\n"]
                            text_length = countStrings(text) + len(filename)
                            
                            print(term.move_xy(int(W/2 - text_length/2), int(H/2)) + 
                                  text[0], term.cadetblue1, filename, term.normal, 
                                  text[1], end='\n\n')
                            user_input = input(">> ")

                            if user_input.lower() == "y":
                                shutil.move(full_path, out_file)
                            elif user_input.lower() == "n":
                                clear()
                                return
                        
                clear()

                text = ["Media successfully downloaded and is located at", "Returning to main menu in"]

                print(
                    term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 2)) + text[0] + "\n\n", 
                    term.move_xy(int(W/2 - len(output_path)/2), int(H/2)) + term.cadetblue1, output_path, term.normal, 
                    term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 2)) + text[1], end=''
                    )
                
                countdown(5)
                return
            else:
                text = ["Media unsuccessfully downloaded.", "Returning to main menu in"]

                clear()

                print(
                    term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 1)) + text[0] + "\n\n", 
                    term.move_xy(int(W/2 - len(text[1])/2) - 2, int(H/2 + 2)) + term.red + text[1] + term.normal, end=''
                    )
                
                countdown(5)
                return


def spoilMedia(option):
    clear()

    media_path = workingDirectory()

    if media_path == "menu":
        return

    file_list = getListOfFiles(media_path)

    if option == 1:
        text = ["I will now apply the 'SPOILER_' prefix to the files in", "Files with the prefix in place will not be touched.",
                "Press enter to continue"]
        print(
            term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 3)) + text[0],
            term.move_xy(int(W/2 - len(media_path)/2), int(H/2 - 1)) + term.cadetblue1 + media_path + term.normal, 
            term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 1)) + text[1], end=''
        )
        print
        input(term.move_xy(int(W/2 - len(text[2])/2), int(H/2 + 3)) + text[2])

        for file in file_list:
            if file.startswith("SPOILER_"):
                pass
            else:
                os.replace(file, "SPOILER_" + file)

    elif option == 0:
        text = ["I will now remove the 'SPOILER_' prefix to the files in", "Files without the prefix in place will not be touched.",
                        "Press enter to continue"]
        print(
            term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 3)) + text[0],
            term.move_xy(int(W/2 - len(media_path)/2), int(H/2 - 1)) + term.cadetblue1 + media_path + term.normal, 
            term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 1)) + text[1], end=''
        )
        print
        input(term.move_xy(int(W/2 - len(text[2])/2), int(H/2 + 3)) + text[2])

        for file in file_list:
            if file.startswith("SPOILER_"):
                new_filename = file[len("SPOILER_"):]
                os.replace(file, new_filename)
                pass
            else:
                pass
            

    clear()

    text = ["Procedure complete. The files are located at:", "Press Enter to continue."]

    print(
        term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 2)) + text[0],
        term.move_xy(int(W/2 - (len(media_path))/2), int(H/2)) + term.cadetblue1 + media_path + term.normal, end=''
        )

    print(term.move_xy(int(W/2 - len(text[1])/2), int(H/2 + 2)) + text[1])
    input()

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

def updateDependencies():
    try:
        clear()
        print("Checking for pip installation...\n")

        subprocess.run(['pip3'])
        clear()
        print("pip was sucessfuly detected... checking dependencies...\n")
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    except FileNotFoundError:
        try:
            import requests
        except ModuleNotFoundError:
            clear()
            print("I was unable to detect an installation of pip, or it is not in your system's PATH.")

            if platform.system() == "Windows":
                print("\nYour OS is: Windows.\n\nA simple way to install pip, is via a script. Please go to: https://bootstrap.pypa.io/get-pip.py",
                "\n\nIf you see a large wall of text, copy and paste the code into a text file and save it as 'get-pip.py'",
                "\n\nIf you do not use the .py extension, the script will not run. Once pip is installed, run this script again.",
                "\n\nIf you encounter any issues, please go to: https://github.com/jose011974/Download-Compress-Media/wiki/Create-a-Bug-Report\n")
            elif platform.system() == "Linux":
                print("\nYour system is: Linux.\n\nThe recommended way to install pip is via your terminal. You can find common commands below:",
                "\n\nUbuntu: sudo apt install python3-pip\n",
                "\nCentOS/Fedora/Redhat: sudo dnf install python3\n",
                "\nArch/Manjaro: sudo pacman -S python-pip\n",
                "\nOpenSUSE: sudo zypper install python3-pip\n",
                "\n\nIf you would like to install pip using a script, please go to https://bootstrap.pypa.io/get-pip.py\n")
            
            input("Press enter to exit.")
            
            sys.exit()

        url = "https://bootstrap.pypa.io/get-pip.py"
        response = requests.get(url, allow_redirects=True)
        pip_file = str(Path(os.getcwd() + r'/' + "get-pip.py"))

        print("\npip, python's package manager, is not installed on your system. I will attempt to download and install it for you.\n")
        time.sleep(3)

        if not response.status_code == 200:
            command = 'clear' # Unix
            if platform.system() == "Windows": command = 'cls' # Windows
            os.system(command)

            print("I was unable to download pip. Please install pip manually (Google is your friend) or from " +
            "https://bootstrap.pypa.io/get-pip.py and execute the script. Exiting...")
            sys.exit()
        try:
            open(pip_file, 'wb').write(response.content)
            if platform.system() == "Linux": 
                print("\n\nA pip install script must be executed in order to install pip. \n\nDue to security restrictions,",
                "the get-pip.py script is not able to be executed by default. \n\nIn order to allow execution, administrator access is required. \n\nIf you feel comfortable",
                "allowing admin access, type 'y' then press enter. Otherwise, type 'n' and press enter to exit the script.",
                "\n\nYou will need to execute the script manually. The script is located at:", pip_file)
                
                user_input = input(">> ")

                print()

                if user_input.lower() == "yes" or user_input == "y":
                    subprocess.call(['sudo', 'chmod', '777', 'get-pip.py'])
                    subprocess.check_call([os.system("python3 ./get-pip.py")])
                elif user_input.lower() == "no" or user_input == "n":
                    print("\nExiting...")
                    sys.exit()
                else:
                    print("\nYou have entered an invalid entry. Please execute the script again.")
                    sys.exit()
                
            elif platform.system() == "Windows":
                subprocess.check_call([os.system("python get-pip.py")])
                print("\nPip should have installed sucessfully. If pip did not install successfully, or you keep seeing this message, you will want to",
                      "troubleshoot your installation. Please go to: https://github.com/jose011974/Python-Video-Downloader/issues to create",
                      "an issue.")
                sys.exit()

        except subprocess.CalledProcessError as e:
            print("\nAn unknown error has occured. Please file a bug report at",
            "https://github.com/jose011974/Download-Compress-Media/wiki/Create-a-Bug-Report",
            "and be sure to include a copy of the terminal output.\n\n",
            "Error:\n\n",
            str(e))
            
            sys.exit()
        except TypeError as e:
            print("\nPip should have installed sucessfully. If pip did not install successfully, or you keep seeing this message, you will want to",
                    "troubleshoot your installation. Please go to: https://github.com/jose011974/Python-Video-Downloader/issues to create",
                    "an issue.")
            sys.exit()

    packages = ["blessed", "numpy", "python-magic", "Pillow", "psutil", "requests", "validators", "yt-dlp"]

    # Turns out the library needed for magic on Windows has been out of date since 2009. 
    # These new packages are up to date and will work with Windows 10.
    if platform.system() == "Windows":
        packages.append("python-magic-bin")

    # Check if the packages are installed

    for p in packages:
        if not p in installed_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", p])
            except Exception as e:
                print(e)
    clear()
    print("Dependencies validated. It is recommended to update your dependencies every few weeks.")
    time.sleep(2)

def workingDirectory():
    # Changes the current working directory to the user supplied directory

    current_dir = os.getcwd()
    clear()

    while True:
        
        text = "(CTRL click to open the path)"

        print("Please type the directory path that contains the media you wish to convert:\n")
        print("To return to the main menu, type 'menu'\n")
        print(
            "Current directory:", term.cadetblue1 + term.link(current_dir, current_dir) + "\n" + term.normal +
             term.move_x(0) + term.move_right(19) + text, end='\n\n'
        )

        user_dir = input(">> ")

        if user_dir.lower() == "menu":
            return "menu"
        else:
            # Check if the user specified path is valid and double triple check the user entered the correct path
            user_dir = str(Path(user_dir))

            if os.path.isdir(user_dir):
                clear()
                print("You have entered", term.cadetblue1 + term.link(user_dir, user_dir), term.normal + "Is this correct? [y/n]\n")
                print("To return to the main menu, type 'menu'\n")

                user_input = input(">> ").lower()

                if user_input == "yes" or user_input == "y" or user_input == "":
                    while True:
                        try:
                            # Create an 'output' folder at the user specified path and return the value to the function
                            clear()
                            try:
                                os.mkdir(Path(user_dir + r'/output'))
                            except FileExistsError:
                                pass

                            print("Source media location changed to:", term.cadetblue1 + user_dir + "\n" + term.normal)
                            os.chdir(user_dir)
                            return user_dir
                        except PermissionError: # Uh oh.
                            clear()
                            print(
                                term.brown1 + "An error has occured: Missing read/write permissions.\n\n" + term.normal + "Please make sure you have read and write access to " + 
                                term.normal + term.cadetblue1 + current_dir + term.normal + " in order to allow critical functions to operate without issue. \n\n" +
                                "To try again, type y. If you would rather instead use the path the script is located at, type 'n'. " +
                                "To return to the main menu, type 'menu'\n\n" + term.turquoise + "If you keep seeing this screen, you may need to troubleshoot further.\n" + 
                                "Go to the GitHub page for more information." + term.normal
                            )

                            user_input = input(">> ").lower()

                            if user_input == "yes" or user_input == "y":
                                continue
                            elif user_input == "no" or user_input == "n":
                                return current_dir
                            elif user_input == "menu":
                                return "menu"
                            else:
                                # The program exits as there are no permissions to read/write anyways
                                clear()
                                print(term.brown1 + "Invalid entry entered. Exiting.\n" + term.normal)
                                sys.exit()
            else:
                clear()
                print(term.brown1 + "You have entered an invalid path. Please try again.\n" + term.normal)

# Logger for yt-dlp
class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        global error_message
        error_message = msg

def downloadStatus(d):
    if d['status'] == 'finished': # Download status complete
        
        #downFileList.append(d['filename'])

        print("\nDownloading complete.\n")

# Parameters for yt-dlp.
# See https://github.com/yt-dlp/yt-dlp/blob/5ab3534d44231f7711398bc3cfc520e2efd09f50/yt_dlp/YoutubeDL.py#L159
ydl_opts = {
    'outtmpl': f'%(id)s.%(ext)s',
    'restrictfilenames': True,
    'no_color': True,
    'logger': MyLogger(),
    'progress_hooks': [downloadStatus],
}

# ---------------------------------

updateDependencies()

# The magic package has some weird quirks with it. Restarting fixes these quirks. Usually.

try:
    import magic
except:
    clear()
    title()

    print("In order to complete dependency installation, you must restart this script.\n\n",
          "If you keep seeing this message, restart your computer.")
    sys.exit()

# Just in case this chunk is required in the future, it will stay.

# while True:

#     packages = ['python-magic', 'python-magic-bin']

#     try:
#         import magic
#         break
#     except ImportError:
#         clear()

#         print("For whatever reason, the libraries required for image detection were not installed. I will now attempt to remove and reinstall the packages containing",
#         "the libraries. Please don't bug me for a fix, this has never happened before and I don't even know what's causing it.\n\nIf you keep seeing this text after",
#         "a minute has passed, you may want to try using another program until I find a fix.")
#         time.sleep(3)
#         for p in packages:
#             subprocess.run([sys.executable, '-m', 'pip', 'uninstall', p, '-y'])
#         time.sleep(1)
#         for p in packages:
#             subprocess.run([sys.executable, '-m', 'pip', 'install', p])

import blessed
import datetime
import validators
import yt_dlp

from numpy import char
from PIL import Image
from shutil import which

global no_comp
global error_message

term = blessed.Terminal()
W,H = term.width, term.height
no_comp = False

while True:
    clear()

    # Creates required files and folders.
    # url_text_path - A text file used to iterate through multuple URLs for download
    # Unsupported URLs.txt - When a download fails or a URL is not supported by yt-dlp, it is added to this text file
    # output_path - Stores any downloaded files as to not clog the main directory

    url_text_path = str(Path('URL.txt'))
    unsupp_url_path = str(Path('Unsupported URLs.txt'))
    output_path = str(Path('output'))

    try:
        if not os.path.exists(url_text_path):
            fp = open(url_text_path, 'x')
            fp.close()
        if not os.path.exists(unsupp_url_path):
            fp = open(unsupp_url_path, 'x')
            fp.close()
        if not os.path.exists(output_path):
            os.mkdir(output_path)
    except PermissionError: # No read/write permissions
        clear()
        print(
            term.brown1 + "An error has occured: Missing read/write permissions.\n\n" + term.normal + "Please make sure you have read and write access to " + 
            term.normal + term.cadetblue1 + os.getcwd() + term.normal + " in order to allow critical functions to operate without issue. \n\n" +
            "To try again, type y. If you would rather instead use the path the script is located at, type 'n'. " +
            "To return to the main menu, type 'menu'\n\n" + term.turquoise + "If you keep seeing this screen, you may need to troubleshoot further.\n" + 
            "Go to the GitHub page for more information." + term.normal
            )
        
        sys.exit()

    if platform.system() == "Windows":
        ff_path = "C:/ffmpeg/ffmpeg.exe"
        try:
            if not os.path.isfile(ff_path):
                raise Exception()
        except Exception:
            no_comp = True

            clear()
            text = ["You do not have ffmpeg installed. Please make sure it is installed at C:\\ffmpeg\\ffmpeg.exe.",
            "Compression features will not work if you choose to proceed.", "You can download ffmpeg from: https://ffmpeg.org/download.html", "Press enter to continue."]

            print(
                term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 3)) + text[0],
                term.move_xy(int(W/2 - len(text[1])/2), int(H/2 - 1)) + term.bold + term.orangered + text[1] + term.normal,
                term.move_xy(int(W/2 - len(text[2])/2), int(H/2 + 1)) + text[2],
                term.move_xy(int(W/2 - len(text[3])/2), int(H/2 + 3)) + text[3]
            )
            input()

    elif platform.system() == "Linux":
        try:
            if which("ffmpeg") is None:
                raise Exception()
        except Exception:
            no_comp = True

            clear()
            text = ["You do not have ffmpeg installed. Please make sure it is installed via your package manager or via your terminal with help from Google.",
            "Compression features will not work if you choose to proceed.", "You can also download ffmpeg from: https://ffmpeg.org/download.html", "Press enter to continue."]

            print(
                term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 3)) + text[0],
                term.move_xy(int(W/2 - len(text[1])/2), int(H/2 - 1)) + term.bold + term.orangered + text[1] + term.normal,
                term.move_xy(int(W/2 - len(text[2])/2), int(H/2 + 1)) + text[2],
                term.move_xy(int(W/2 - len(text[3])/2), int(H/2 + 3)) + text[3]
            )
            input()

    main()