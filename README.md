I have no idea how to use Github. Please forgive me.

# IMPORTANT

Unless otherwise noted, the script will look for files in ***ALL*** subfolders. If you only want to work with a specific set of files, please put them in their own folder.

I am not responsible for any mistakes caused by the script applying a procedure to ALL of your files vs. a few files.

# Download-Compress-Media

**Until someone comes up with a better name, this is what we're working with.**

This script can do the following:

* Download media from the internet using [Youtube-DL](https://github.com/ytdl-org/youtube-dl) as the backend.
* Compress media if it's file size is larger than 8 MB; This will allow you to send the media through Discord if you or the server do not have Nitro/Boosts.
* Append "SPOILER" to file names in order to send them through Discord censored.

# Pre-reqs

You will need [Python 3+](https://www.python.org/downloads/). This script is INCOMPATABLE with ANY version of Python 2.

This script uses Youtube-DL to download the files. For Windows systems you need [Microsoft Visual C++ 2010 Service Pack 1 Redistributable Package (x86)](https://download.microsoft.com/download/1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x86.exe).

I have tested the script using KDE Neon 5.25 (Ubuntu 20.04 LTS) with Python 3.10.6. I have yet to try it on Windows, however it should work regardless. Mac is untested as I do not have one and will never own one. If anyone would like to help me test it on a Mac, please let me know via an issue.

The script will automatically download the required python libraries and update them if required at every startup.

Just in case something doesnt work, here are all of the libraries used in the script:

**Python-Included Libraries:**

*You shouldn't need to download these unless you installed Python wrong or something. These are already included with Python*

* fileinput
* os
* platform
* re
* requests
* shutil
* time
* subprocess
* sys
* webbrowser

**3rd-Party Libraries:**

*These you will have to download from PyPI*

* colorama
* magic
* pathlib
* psutil
* validators
* youtube_dl

# Usage

Using the script is simple, open it either in a terminal (Linux / Mac) or double click (Windows) and the script will run.

If the script does not run, please check the Troubleshooting section below.

If no errors occur, then you will be presented with a menu consisting of the following choices:

 * 1. Single File    - Compress one file
 * 2. Multiple Files - Compress multiple files
 * 3. Single URL     - Download and compress one file
 * 4. Multiple URLs  - Download and compress multiple files
 * 5. Spoil media    - Make media "spoiled" to send on Discord
 * 6. Help           - Opens this page
 * 7. Exit           - I don't need to tell you what this does.

The choices should be self explanitory. I have tried to make the process simple and efficient.

# Downloading

The process for downloading files is simple:

1a. Select single URL or multiple URL

2a. Single URL: Paste in the URL in question and press enter. The program will attempt to download the file and save it in a folder called 'output'

2b. Multiple URLs: Create a text file called URL.txt in the same directory as the script and paste every URL on a new line. You may space out the URLs if it makes you feel better. Then the script will attempt to go through each URL and download the files. The downloaded files get moved to a temp folder, and when the process is complete, they all get moved to a folder called 'output'.

In either case, if the file is larger than 8 MB (8,192 KB), the script will ask if you want to compress it. Multiple URLs will ask for compression when downloading is complete.

# Compression Method

The first version of this script used MoviePy to compress media files. After spending 2-3 months and having a finished product, I read that MoviePy should NOT be used that way and instead should have used FFMPEG.

So this script uses FFMPEG. It uses the input file for figuring out defaults.

For GIF files, the script re-encodes them to WEBM as FFMPEG creates LARGE size GIF files due to how the format works. While websites that can compress GIFs do exist, I have not found one that has an API I can use to upload and download the finished file.

For PNG files, the script always spat an error about an alpha channel and there seems to be no way to remove it. So I instead re-encode the PNG to JPG. If you have a solution to the error in question, please let me know through an issue.

# Spoiling Media

There are times where you don't want the person in question to see the file you have sent right away on Discord. Maybe its a picture of your sweet ride. This is where Spoiling comes in. The script will append "SPOILER" to the prefix and allow you to send files automatically spoiled.

# Errors

I have a basic error handing system in place. There are 4 error messages in place and more will be added as problems arise.

The errors are pretty self explaintory. If you think an error should not have occured, please create an issue with:

* Python version
* Dependency versions
* OS type and version
* URL that you tried to download
* Error message

* Current Error Messages

# Troubleshooting

There may be a few reasons why you run into issues running this script.

## 1. Determine if Python is installed, and what version

* Windows:
  * Open the start menu and type 'cmd'
  * A window with a black background should open. Click on the window and type 'python'
  * You should see the following:
  ![](https://i.imgur.com/YKUT1t4.png)
  * If you do not see the prompt inside the red box and instead see `'python' is not recognized as an internal or external command, operable program or batch file.` then Python is not installed. There are many resourses available to install Python on Windows. Google is your friend.
* Mac:
  * Open the Terminal and type `python`
  * You should see the following:
  ![](https://www.applegazette.com/wp-content/uploads/2017/06/python-3-cli-2.png)
  * _I have no idea how to fix the formatting, the code is the exact same as in the Windows section._
  * If you do not see the prompt, Python is not installed. There are many resources available to install Python on Mac. Google is your friend.
* Linux:
  * TBCompleted

## 2. File/Foler Permissions

Another reason why the script may fail is due to not having the proper permissions for the folder the script is located in. The easiest way to check if you have proper permissions is to create a new text file in the directory the script is located in.

## 3. Unable to Download Media

---

This script uses [Youtube-DL](https://github.com/ytdl-org/youtube-dl) for the actual downloading of the media. 

The short version of how it works:

1. Youtube-DL tries to find an extractor based on the domain of the website. For example, there are extractors for Twitter, Instagram, and Youtube.
2. If an extractor is found, it then tries to find the direct link of the media in question (Video, GIF, Audio, Image) and downloads the media.
3. If an extractor is **NOT** found, it falls back to a generic extractor, which tires to look throughout the entire page for any information on the media. [Reference](https://github.com/ytdl-org/youtube-dl/blob/7009bb9f3182449ae8cc05cc28b768b63030a485/youtube_dl/extractor/common.py#L87)

* If no media information is found, it will throw out an error and you must find the direct link yourself.

* You can try right clicking the media in question and clicking "Copy Image/Video address". You can also use the Inspect Element tool (F12) to look through the HTML Markup of the webpage and find the direct link. Sometikmes is buried deep inside the code.

---

If the script throws a 404 not found error, you can try to access the link in question to determine if its a bug or a feature.

If you ARE able to access the link, then its a bug. Create an issue with the following information:

* Python version
* Dependency versions
* OS type and version
* URL that you tried to download
* Error message

If you are NOT able to access the link, its a feature.

# Credits / License

This scrpit was created in Visual Studio Code with Python 3.10.4

I only wish that you give me credit as the author if you decide to distribute my script.

If there is anything that can be improved, please let me know. While I took a basic python course in high school back in 2016-2017, most of my programming skills are self taught through ***lots*** of trial and error. This script took 6 months to get to where it is now.