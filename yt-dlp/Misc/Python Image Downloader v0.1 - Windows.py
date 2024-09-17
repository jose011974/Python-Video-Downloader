import requests
import os
import shutil
import platform
import blessed
import validators
import time
import magic

from datetime import datetime
from pathlib import Path
from numpy import char

os.chdir(Path(__file__).parent.resolve())

term = blessed.Terminal()
W,H = term.width, term.height

file_types = (".jpeg", "jpg", ".png", ".gif", ".mp4", ".webm")

def clear():
    # Clear the screen

    command = 'clear' # Unix
    if platform.system() == "Windows": command = 'cls' # Windows
    os.system(command)

    title()

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

def getFileExtension(filename):

    # Identify file type. You cannot just rely on the extension alone.

    fileMIME = magic.from_file(filename, mime=True)
    fileMIME = fileMIME[6:len(fileMIME)]
    fileExt = os.path.splitext(filename)

    return fileExt[1], fileMIME

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

def multipleURLDownload():
    
    non_file = True
    media_path = os.getcwd()
    out_path = str(Path(media_path + r'/output'))
    url_txt_path = str(Path(media_path + r"/IMG URL.txt"))
    uri_list= list()
    current_pos = 1

    while non_file:

        # Open URL.txt and create a list of URL's
        if os.path.isfile(url_txt_path):
            with open(url_txt_path, 'r') as file:
                lines = file.readlines()

            for line in lines:
                if '?format=jpg&name=small' in line:
                    # Replace '?format=jpg&name=small' with '?format=png'
                    updated_line = line.replace('?format=jpg&name=small', '?format=png')
                    uri_list.append(updated_line.strip())
                elif '?format=jpg&name=360x360' in line:
                    # Replace '?format=jpg&name=360x360' with '?format=png'
                    updated_line = line.replace('?format=jpg&name=360x360', '?format=png')
                    uri_list.append(updated_line.strip())
                else:
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
                    text = ["URI Found:"]

                    # Output:

                    # URI Found: $uri
                    # $current_pos out of $total_urls
                    #[yt-dlp]
                    
                    clear()
                    print(
                        term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 2)) + text[0],
                        term.move_xy(int(W/2 - len(uri)/2), int(H/2)) + term.cadetblue1 + uri + term.normal,
                        term.move_xy(int(W/2 - (len(str(current_pos)) + len(str(total_urls)) + 10)/2), int(H/2 + 2)), current_pos, "out of", total_urls
                    )

                    time.sleep(1)

                    # Download the image and name the file using the current time.
                    print("[PID]\nRequesting image...")
                    img_data = requests.get(uri).content
                    now = datetime.now()
                    filename = now.strftime("%m%d%y-%I%M%S")
                    
                    print("Writing file...")
                    f = open(str(filename + str(now.microsecond)[:2] + ".png"), 'wb')
                    f.write(img_data)
                    f.close()
                    print("Closing file...")
                    time.sleep(1)

                    current_pos = current_pos + 1

            filename_list = getListOfFiles(media_path)
            
            for filename in filename_list:
                downloaded_file = str(Path(out_path + r'/' + filename))
                shutil.move(filename, downloaded_file)
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

        clear()

        text = ["Would you like to clear", "IMG URL.txt", "?", "(y/n)"]

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

            text = ["IMG URL.txt", "has been cleared. Exiting in"]

            print(term.move_xy(int(W/2 - countStrings(text)/2), int(H/2 + 1)), 
                    term.cadetblue1 + text[0], 
                    term.palegreen + text[1] + term.normal, end='')

        elif user_input.lower() == "no" or user_input == "n" or user_input == "":

            clear()

            text = ["IMG URL.txt", "has", "NOT", "been cleared. Exiting in"]

            print(
                term.move_xy(int(W/2 - countStrings(text)/2), int(H/2 + 1)),
            term.cadetblue1 + text[0],
            term.palegreen + text[1],
            term.red + text[2], 
            term.palegreen + text[3] + term.normal, end='')

        countdown(3)
        clear()
        print("Exiting...")

        break

def title():

    # Create a title bar based on the console window size

    title = "[Python Image Downloader v0.1 - 'The best downloader in town!']"
    consoleSize = shutil.get_terminal_size()
    col = int(consoleSize[0])-len(title)

    for x in range(0, int(col/2)):
        print("-", end = '')

    print(title, end = '')

    for x in range(0, int(col/2)):
        print("-", end='')

    print("\n")

try:
    output_path = str(Path('output'))

    if not os.path.exists(output_path):
        os.mkdir(output_path)
        
    multipleURLDownload()
except Exception as e:
    clear()

    print("An exeption has occured:\n\n" + e)

    input()