import clipboard
import shutil
import platform
import os
import time
import validators
import sys

from pynput import mouse

global URI
URI = []

def clear():
    command = 'clear' # Unix
    if platform.system() == "Windows": command = 'cls' # Windows
    os.system(command)

    title()

def title():

    # Create a title bar based on the console window size

    title = "[Image URL Grabber v0.1 - 'The best grabber in town!']"
    consoleSize = shutil.get_terminal_size()
    col = int(consoleSize[0])-len(title)

    for x in range(0, int(col/2)):
        print("-", end = '')

    print(title, end = '')

    for x in range(0, int(col/2)):
        print("-", end='')

    print("\n")


def read_clipboard():
    try:
        clipboard_data = clipboard.paste()
        return clipboard_data
    except Exception as e:
        return f"An error occurred: {e}"
    
def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        if pressed:
            pass
        else:
            time.sleep(0.4)
            cboard = read_clipboard()

            if cboard == "" or cboard == " ":
                pass
            else:
                if validators.url(cboard):
                    URI.append(cboard)
                    print("URL:", cboard)
                    clipboard.copy('')
        
    if button == mouse.Button.middle:
        if pressed:
            pass
        else:
            os.chdir(os.path.dirname(__file__))
            filename = "IMG URL.txt"

            with open(filename, 'w') as file:
                for i in URI:
                    file.write(i + "\n")

            clear()
            print("IMG URL.txt created! Exiting...")
            listener.stop()
            sys.exit()

def main():

    clear()

    print("Do you wish to empty your clipboard? (y/n)\n")
    userInput = input(">> ")
    if userInput.lower() == "y":
        clipboard.copy('')
    
        print("\nClipboard has been cleared.\n")
    time.sleep(3)

    clear()

    print("NOTE: Pressing left click at this point will add whatever URL you have in your clipboard to the program list.\n")

    print("This program allows you to easily create a URL.txt file for Python Video Downloader by PineCone.\n")
    print("Instructions: Copy a URL, left click anywhere, and you will see the URL you copied. Press the middle mouse button when you are done.")
    print("Note: Pressing left click will freeze your mouse for less than a second. There is also a clipboard filter, meaning that only URL's will be written.\n")

main()

with mouse.Listener(on_click=on_click) as listener:
        listener.join()