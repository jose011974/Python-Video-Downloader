import blessed
import platform
import os

term = blessed.Terminal()
W,H = term.width, term.height
outputPath = "C:\\yourmotherisaspy.mp4"
mediaPath = "C:\\"

command = 'clear' # Unix
if platform.system() == "Windows": command = 'cls' # Windows
os.system(command)

#20 + 45

text = ["Unsupported URLs.txt", "was not found. Returning to the main menu in:"]

print(term.move_xy(int(W/2 - (20+45)/2), int(H/2)) + term.cadetblue1 + text[0], term.normal + text[1], end='')