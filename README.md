# Important Notes!

It is imperative that you understand that I am **NOT** responsible for any data loss that **will** occur if you do not take into account the quirks of this script.

Please read this Readme in its **ENTIRETY**

For example:

- This script will look inside of ALL sub-directories from the script path. So it is recommended to run this script inside its own folder, and leave the output folder empty once you are finished using the program.
- This script does not have a check for reading of "SPOILER" as a prefix to the file when doing a spoil command.
	- The same applies for "non-spoling".

------------

# Introduction - Python Video Downloader

This python script is designed to do the following:

- Download media from the internet, whether it be one URI or multiple URI.
- Attempt to compress media, whether it be one file or multiple. It tries to compress files under 8 MB because Discord needs more money I guess.
- A basic ffmpeg parameter is used, as if a file cannot be compressed under 8 MB, the next option will be to segment the file.
- Append "SPOILER" to files for sharing pictures of your sweet ride to your Discord peeps.
- Remove "Spoiler" to files for whatever reason.

------------

# Prerequisites

You are going to need the following:

- Python 3.10 or 3.11
	- I have not tested on Python 3.9 or below. It will **NOT** work with any version of Python 2.
- Python PIP Manager
	- This allows you to install Python packages hosted on pypi
- ffmpeg
	- I have been using version 2022-07-06 on Windows, any version should work however.
	- On Windows, place ffmpeg.exe in C:\ffmpeg
	- On Linux, make sure it is accessible via your terminal. Type `ffmpeg -version` and you should get something in return. Check the troubleshooting section for more information

The script will automatically grab the required libraries. In the event this does not occur, here are the libraries used in this script:

- blessed - Used for terminal colors and cursor placement
- magic - Used for file type detection. This is referenced as `python-magic` at pypi.org
- numpy - Used for number operations
- PIL - Python Imaging Library - Used for manipulating images.
- psutil - Used for processes and system utilities (used to terminate ffmpeg processes in the event they are frozen)
- requests - Used to create HTTP requests
- validators - Used to validate data types (emails, links, etc.)
- youtube_dl - Used to download media from various websites using extractors. [Learn More](https://github.com/ytdl-org/youtube-dl "Learn More")
------------

# Usage

**Use at your own risk!**

Video Tutorial: TBD

------------

# Text Tutorial

### Step 1 - Download Prerequisites

- Download the prerequisites listed above:
	- [Python](https://www.python.org/downloads/ "Python")
		- **Linux:**
			- Most Linux distributions include python by default. You can install python via your package manager or terminal. Google is your friend for any distributions not listed here.
			- Ubuntu/Debian/KDE Neon: `sudo apt install python3`
			- Fedora: `sudo dnf install python3`
			- Arch: `sudo pacman -Sy python-pip` (installs both python and pip)
			- openSUSE: [Click here for the latest builds](https://software.opensuse.org/package/python3 "Click here for the latest builds")
	- [PIP](https://bootstrap.pypa.io/get-pip.py "PIP")
		- **Windows 10/11:**
			- You can install pip via the python installer or through the script linked [here](https://bootstrap.pypa.io/get-pip.py "here")
		- **Linux:**
			- You can install pip using the script linked [here](https://bootstrap.pypa.io/get-pip.py "here"), via your package manager, or via the terminal. Google is your friend for any distributions not listed here.
			- Ubuntu/Debian/KDE Neon: `sudo apt install python3-pip`
			- Fedora: `sudo dnf install python3-pip`
			- Arch: `pacman -S python-pip`
			- openSUSE: [Click here for the latest build](https://software.opensuse.org/package/python-pip "Click here for the latest build")
		
	- [ffmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z "ffmpeg")
		- **Windows 10/11:**
			- Extract the .7z file (using 7-zip or Winrar) and place ffmpeg.exe at `C:\ffmpeg`
		- **Linux:**
			 - You can install ffmpeg via your package manager, the link above, or via the terminal. Google is your friend here.
			 - Ubuntu/Debian/KDE Neon: `sudo apt install ffmpeg`
			- Fedora: `sudo dnf install ffmpeg`
			- Arch: `pacman -S ffmpeg`
			- openSUSE: [Click here for the latest build](https://software.opensuse.org/package/ffmpeg "Click here for the latest build")

### Step 2 - Install Prerequisites - WINDOWS 10/11 ONLY!

*Linux users go to step 3*

	1.  Download Python using the link above, then install using the defaults, with the checkbox labeled "Add Python to PATH" checked. You do not need administrator permissions to install Python or set up the PATH environment variables.

![Python Installation Parameters](https://i.imgur.com/P58jdP6.png "Python Installation Parameters")

	2. Once Python is installed, download ffmpeg and create a folder on your C:\ directory called 'ffmpeg'
	
	Using a program such as 7-Zip or Winrar, extract ffmpeg.exe to 'C:\ffmpeg\' You only need ffmpeg.exe for the script to function.
	
	The full path should be 'C:\ffmpeg\ffmpeg.exe

	3. Download the Microsoft Visual C++ 2010 Service Pack 1 RP (x86) using the link above and install it normally.

### Step 3 - Obtain Python Video Downloader

- Once you have completed Steps 1 & 2, you may now download the script. [Click here](https://github.com/jose011974/Python-Video-Downloader/releases "Click here") to download the latest release.

### Step 4 - Run Python Video Downloader

1. Create a folder with any name you desire. For this example, the folder will be called `Python Video Downloader`. I suggest creating the folder on your desktop for easy access.
2. Place the script inside the folder (`Python Video Downloader`)
3. Run the script

**Windows 10/11 Instructions**:
- Assuming the defaults were selected, double click `Python Video Downloader.py` to launch the script. If you have extensions disabled, you may only see `Python Video Downloader.py`

**Linux Instructions**:
- In order to allow the script to be executed with a double click gesture, you must right click and allow the script to be executed. This WILL differ depending on your file manager.

	- You can set this execution flag via the terminal with the following: `sudo chmod +x ./'Python Video Downloader.py'`
	- You can also run the script via the terminal with the following: `python3 ./'Python Video Downloader.py'`

**The following will be checked once the script launches:**
	- pip installation
	- The presence of required packages
	- The presence of ffmpeg

Assuming everything was installed and works correctly, congration! You are now a proud operator of Python Video Downloader!

If you have any issues, please go to the troubleshooting[link goes here] section.

### Using Python Video Downloader

The main menu and the available options are shown below:

[![Python Video Downloader Main Menu](https://i.imgur.com/GXBKfKi.png "Python Video Downloader Main Menu")](https://i.imgur.com/GXBKfKi.png "Python Video Downloader Main Menu")

- **Option 1: Compress a single file**
	- This option will prompt for the full path of the file name, or if the file is in the same directory as the script, you can just type the file name and the extension.
	- Example: `C:\yourmotherisaspy\spy.mp4` | `spy.mp4`
- **Option 2: Compress multiple files in a folder**
	- WARNING: THIS WILL SCAN *ALL* SUB DIRECTORES! IT IS RECOMMENDED TO PLACE THE IMAGES YOU WISH TO COMPRESS INTO A STANDALONE FOLDER.
- **Option 3: Download and compress a media file from the internet**
	- This option will create a folder called `output` in the running directory and place the file inside `output`
- **Option 4: Download and compress multiple files from the internet**
	- This option uses a text file called `URL.txt` at the script directory to grab multiple URI.
	- This option will create a folder called `output` in the running directory and place the files inside `output`
- **Option 5: Appends `SPOILER_` to the prefix of the file name in order to send media behind a spoiler tag on Discord**.
	- WARNING: THIS WILL SCAN *ALL* SUB DIRECTORES! IT IS RECOMMENDED TO PLACE THE IMAGES YOU WISH TO COMPRESS INTO A STANDALONE FOLDER.
- **Option 6: Removes the `SPOILER_` tag from the prefix of a file name.**
	- WARNING: THIS WILL SCAN *ALL* SUB DIRECTORES! IT IS RECOMMENDED TO PLACE THE IMAGES YOU WISH TO COMPRESS INTO A STANDALONE FOLDER.
- **Option 7: Any URLs that were not able to be downloaded will be placed in a text file called `Unsupported URLs.txt` .** This option will automatically go through all URLs in the text file and open them in your web browser so you can download them manually.
- **Option 8: Open the GitHub page of this script**
- **Option 9: Exit the script.**

### Extra Notes:
- Only files above 8 MB will be compressed. This is because Discord wants money apparently.
- Only `jpg/jpeg, png, gif, mp4, and webm` files have been tested. In order to maintain compatabilty with all devices out there, the output file will be an `.mp4` file. The original file will not be deleted and instead have `old_` appended to the prefix of the file name.

### More information on how the Downloading and Compressing features work

`Python Video Downloader` uses youtube-dl for downloading media from the internet.
- In summary, youtube-dl will try to use an extractor to grab the media url and download it with the highest quality possible.
- If an extractor is not available, then a generic extractor is used and results will vary if the generic extractor is used.
	- This may result in a URL not being accessable and the script throwing an error message.


------------

`Python Video Downloader` uses ffmpeg to compress media.

- Here is the parameter used in `Python Video Downloader`: `-c:v libx264 -crf 23 -pix_fmt yuv420p`
	- This creates an H.264 MP4 file with moderate quality that is compatible with many devices.

In the future, an option will be implimented that can cut a media file into 10 second clips and stitch them back into one video.
