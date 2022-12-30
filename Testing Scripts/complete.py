import blessed
import os
import platform
import time

def clear():
    # Change the clear screen command based on OS.
    command = 'clear' # Unix
    if platform.system() == "Windows": command = 'cls' # Windows
    os.system(command)

def countdown(curLocation):
    W = curLocation[1]
    H = curLocation[0]

    i = 3
    while i >= 1:
        print(term.move_xy(W + 1,H) + "(" + str(i) + ")")
        time.sleep(1)
        i = i - 1

term = blessed.Terminal()
W,H = term.width, term.height

clear()

text = "Procedure complete. The finished file is located at:"
path = os.path.dirname(__file__)
text2 = "Note: The file may still be too large. If that is the case, use a different program/service."
text3 = "Please press Enter to continue."

print(
    term.move_xy(int(W/2 - len(text)/2), int(H/2 - 2)) + text +
    term.cadetblue1 + term.move_xy(int(W/2 - len(path)/2), int(H/2)) + path + term.normal +
    term.move_xy(int(W/2 - len(text2)/2), int(H/2 + 2)) + text2, end=''
    )

countdown(term.get_location())

print(term.move_xy(int(W/2 - len(text3)/2), int(H/2 + 4)) + text3, end='')

input()