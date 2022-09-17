I have no idea how to use Github. Please forgive me.

# Download-Compress-Media

This script can do the following:

* Download media from the internet using Youtube-DL as the backend.
* Compress media if it's file size is larger than 8 MB; This will allow you to send the media through Discord if you or the server do not have Nitro/Boosts.
* Append "SPOILER" to file names in order to send them through Discord

# Pre-reqs

You will need [Python 3+](https://www.python.org/downloads/). This script is INCOMPATABLE with ANY version of Python 2.

This script uses Youtube-DL to download the files. For Windows systems you need [Microsoft Visual C++ 2010 Service Pack 1 Redistributable Package (x86)](https://download.microsoft.com/download/1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x86.exe).

I have tested the script using KDE Neon 5.25 (Ubuntu 20.04 LTS) with Python 3.10.6. I have yet to try it on Windows, however it should work regardless. Mac is untested as I do not have one and will never own one. If anyone would like to help me test it on a Mac, please let me know via an issue.

The script will automatically download the required python libraries and update them if required at every startup.

Just in case something doesnt work, here are all of the libraries used in the script:

**Python-Included Libraries:**

*You shouldn't need to download these unless you installed Python wrong or something. These are already included with Python*

* os
* platform
* random
* requests
* shutil
* time
* subprocess
* sys

*These you will have to download from PyPI*

**3rd-Party Libraries:**

* Colorama
* magic
* pathlib
* PIL
* psutil
* validators
* youtube_dl

# Usage

Using the script is simple, open it either in a terminal (Linux / Mac) or double click (Windows) and the script will run.

If the script does not run, please check the Troubleshooting section below.

If no errors occur, then you will be presented with a menu consisting of the following choices:

 * 1. Single File     - Compress one file
 * 2. Multiple Files - Compress multiple files
 * 3. Single URL     - Download and compress one file
 * 4. Multiple URLs  - Download and compress
 * 5. Spoil media    - Make media "spoiled" to send on Discord
 * 6. Help           - Opens this page
 * 7. Exit           - I don't need to tell you what this does.

The choices should be self explanitory. I have tried to make the process simple and efficient. 

# Downloading

The process for downloading files is simple.

1. Select single URL or multiple URL

2a. Single URL: Paste in the URL in question and press enter. The program will attempt to download the file and save it in the same directory as the script.

2b. Multiple URLs: Create a text file called URL.txt in the same directory as the script and paste every URL on a new line. You may space out the URLs if it makes you feel better. Then the script will attempt to go through each URL and download the files.

In either case, if the file is larger than 8 MB (8,192 KB), the script will ask if you want to compress it. Multiple URLs will ask for compression when downloading is complete.

# Compression Method

The first version of this script used MoviePy to compress media files. After spending 2-3 months and having a finished product, I read that MoviePy should NOT be used that way and instead should have used FFMPEG.

So this script uses FFMPEG. It uses the input file for figuring out defaults.

For GIF files, the script re-encodes them to WEBM as FFMPEG creates LARGE size GIF files due to how the format works. While websites that can compress GIFs do exist, I have not found one that has an API I can use to upload and download the finished file.

For PNG files, the script always spat an error about an alpha channel and there seems to be no way to remove it. So I instead re-encode the PNG to JPG. If you have a solution to the error in question, please let me know through an issue.

# Spoiling Media

There are times where you don't want the person in question to see the file you have sent right away on Discrd. Maybe its a picture of your sweet ride. This is where Spoiling comes in. The script will append "SPOILDER" to the prefix and allow you to send files automatically spoiled.

# Errors

I have a basic error handing system in place. There are 4 error messages in place and more will be added as problems arise.

The errors are pretty self explaintory. If you think an error should not have occured, please create an issue with:

* Python version
* Dependency versions
* OS type and version
* URL that you tried to download
* Error message

# Credits / License

This scrpit was created in Visual Studio Code with Python 3.10.6

I only wish that you give me credit as the author if you decide to distribute my script.

If there is anything that can be improved, please let me know. While I took a basic python course in high school back in 2016-2017, most of my programming skills are self taught through lots of trial and error. This script took 6 months of trial and error to get to where it is now.
