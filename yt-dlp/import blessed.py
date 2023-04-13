import blessed
import os
import platform

term = blessed.Terminal()

def clear():
    command = 'clear' # Unix
    if platform.system() == "Windows": command = 'cls' # Windows
    os.system(command)

clear()

print(
        term.brown1 + "ERROR 404:" + term.normal, "The URL could not be accessed. Please make sure that the URL points to a valid address.\n\n" +
        term.brown1 + "NOTE:" + term.normal, "If you are trying to download a video from Twitter, and it is age restricted, you are going to have to pass cookies in order to download the video. " +
        "If you are skilled enough, you can edit the script and include the cookies yourself. Otherwise, you will have to wait until I can automatucally find the cookies " +
        "for you, or use another program.\n\n" +
        "If you are not trying to download an age restricted Twitter video, and you can access the video in question, then you may then create an issue at https://github.com/jose011974/Download-Compress-Media/issues")