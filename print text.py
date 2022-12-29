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

text = ["Procedure complete.", "Downloaded media has been saved to:", "Unavailable URLs have been saved to", "Unsupported URLs.txt", 
            "Press enter to continue."]

print(
    term.move_xy(int(W/2 - len(text[0])/2), int(H/2 - 3)) + text[0],
    term.move_xy(int(W/2 - (len(text[1]) + len(outputPath))/2), int(H/2 - 1)) + term.palegreen + text[1], term.cadetblue1 + outputPath + term.normal,
    term.move_xy(int(W/2 - (len(text[2]) + len(mediaPath) + len(text[3]))/2), int(H/2 + 1)) + term.palegreen + text[2] + term.cadetblue1  + ":", 
    mediaPath + text[3] + term.normal
    )

print(term.move_xy(int(W/2 - len(text[4])/2), int(H/2 + 3)) + text[4])