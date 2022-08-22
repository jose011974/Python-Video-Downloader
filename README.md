I have no idea how to use Github. Please forgive me.

# Download-Compress-Media

The only purpose for this script existing is to:

* Download media when the Discord embed fails to load
* Compress media under 8 MB because fuck Discord Nitro
* Download media from websites that do not have a native download button (I'M LOOKING AT YOU TWITTER)
* add SPOLIER to the beginning of a file name to send files that may be NOT SAFE for work to your co-workers or friends on Discord.

# Pre-reqs

You will need Python 3+. This script is INCOMPATABLE with ANY version of Python 2.

This script uses Youtube-DL to download the files. For Windows systems you need Microsoft Visual C++ 2010 Service Pack 1 Redistributable Package (x86).

I have tested the script using KDE Neon 5.25 (Ubuntu 20.04 LTS) with Python 3.10.6. I have yet to try it on Windows, however it should work regardless. Mac is untested as I do not have one and will never own one. If anyone would like to help me test it on a Mac, please let me know via an issue.

The script will automatically download the required python libraries and update them as necssary.

Just in case something doesnt work, here are all of the libraries used in the script:

* from colorama import Fore, Back, Style, init
* from pathlib import Path
* from PIL import Image
* magic
* moviepy.editor as mp
* moviepy.video.fx.all as vfx
* os
* platform
* psutil
* shutil
* random
* requests
* subprocess
* sys
* sys
* time
* validators
* youtube_dl

# Usage

I recommend you put this script inside a folder as for the time being, single file downloads and compression output the file to the same location the script is in.

Using the script is simple, open it either in a terminal (Linux) or double click (Windows) and the script will automatically check for the required libraries and download+update if necessary.

If no errors occur, then you will be presented with a menu consisting of the following choices:

 * 1. Single File
 * 2. Multiple Files
 * 3. Single URL
 * 4. Multiple URLs
 * 5. Spoil media
 * 6. Help
 * 7. Exit

The choices should be self explanitory. I have tried to make the process simple and efficient. 

# Downloading

The process for downloading files is simple.

1. Select single URL or multiple URL

2a. Single URL: Paste in the URL in question and press enter. The program will attempt to download the file and, if required, ask if you want to compress it in order to send the file on Discord for non-Nitro users

2b. Multiple URLs: Create a text file called URL.txt in the same directory as the script and paste every URL in separate lines. Then the script will attempt to go through each URL and download the files, and if required, ask you if you want to compress any files over 8 MB because of discord non-nitro limits.

Example:

example.com

example.org

IamArealURL.co

ur.mom

# Spoiling Media

If you want to send files on discord but you don't want to scare them by sending an NFT, you can choose to spoil them. The script will append SPOILER to the prefix of the file name and allow you to send more than one file and have them all spoiled so they don't hate you immediately.

# Errors

I have a basic error handing system in place. Right now only 2 error codes exist as those are the only ones I have encountered.

The errors are pretty self explaintory. If you think an error should not have occured, please create an issue with:

* Python version
* Dependency versions
* OS type and version
* URL that you tried to download
* Error message

# Credits / License

The scrpit was created in Visual Studio Code with Python 3.10.6

I only wish that you give me credit as the author if you decide to distribute my script.

If there is anything that can be improved, please let me know. While I took a basic python course in high school back in 2016-2017, most of my programming skills are self taught through lots of trial and error.
