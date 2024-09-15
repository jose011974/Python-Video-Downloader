# UPDATE: Discord no longer offers 25 MB uploads because they are fucking dumb and are ruining their own service.

# THIS DOCUMENTATION IS OUT OF DATE. IT APPLIES TO VERSIONS BELOW 1.05. New documentation coming soon!

# Important Notes!

It is imperative that you understand that I am **NOT** responsible for any data loss that **will** occur if you do not take into account the quirks of this script.

Please read this Readme in its **ENTIRETY**

For example:

- This script will look inside of ALL sub-directories from the script path. 
	- For example, if the script is in the folder path "C:\Users\John McAfee\Desktop\SecretPlans\" and there are 2 folders called "Pentagon" and "Swiffer" that contain images/videos, they will ALL be moved to a new folder called "output" and be manipulated.
	- Options 1,2,5,6 use the user-defined directory to create an output folder; options 3,4 use the script folder to create an output directory.
- This script does not check if the "SPOILER_" tag is present or not.
- Compression may not actually lower file size. The output file may end up looking worse than the source file. I am looking for a fix.

I hope to fix these issues in the future. For now, I suggest placing the script in its own folder and if you want the best compression possible, use another program like [Handbrake](https://handbrake.fr/).
	
*This readme is a work in progress, create an issue if you are experiencing problems.*

------------

# Introduction - Python Video Downloader

This python script is designed to do the following:

- Download media from the internet using one or multiple URL's
- Compress single or multiple media; the minimum threshold being 25 MB as that is what Discord has set their free limit to.
	- A basic ffmpeg parameter is used, as if a file cannot be compressed under 25 MB, the next option will be to segment the file. (segmentation is not implimented yet)
- Append "SPOILER_" to file names for sharing pictures of your sweet ride to your Discord peeps.
- Remove "SPOILER_" from file names for whatever reason.

# Prerequisites

You are going to need the following:

- Python 3.7+
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
- yt-dlp - Used to download media from various websites using extractors. [Learn More](https://github.com/yt-dlp/yt-dlp "Learn More")

---

# Video Tutorial

Video Tutorial: TBD

------------

# Text Tutorial

### Step 1 - Download Prerequisites

- Download the prerequisites listed above:
	- [Python](https://www.python.org/downloads/ "Python")
		- **Windows**
			1. Download Python 3.11.0 | [32-Bit](https://www.python.org/ftp/python/3.11.0/python-3.11.0.exe) | [64-Bit](https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe) |
			2. Open the Python Installer
				**2a. With the installer opened, check the box labeled "Add python.exe to PATH" and select "Customize installation"** 
				
				![enter image description here](https://raw.githubusercontent.com/jose011974/Python-Video-Downloader/main/Readme%20Assets/Step%201.png)
				
				**2b. In the next step, check the boxes labeled "pip", "py launcher", and "for all users" (if possible)**
				
				![enter image description here](https://github.com/jose011974/Python-Video-Downloader/blob/main/Readme%20Assets/Step%202.png?raw=true)
				
				**2c. In the next step, check the boxes that have in a circle next to them as shown in the image below. Make sure that the "Customize install location" box has the following path: "C:\Python311\"** 
				
				![enter image description here](https://github.com/jose011974/Python-Video-Downloader/blob/main/Readme%20Assets/Step%203.png?raw=true)
				
				**2d. Python should install with no issues. If you do encounter any issues, please use Google to find a solution or create an issue if you are unable to find a solution.**
				
				**2e. Once Python is installed, press the "Windows" key + "R" to open the run dialog box as shown below:**
				
				![enter image description here](https://github.com/jose011974/Python-Video-Downloader/blob/main/Readme%20Assets/Step%204.png?raw=true)
				**Type "cmd" as shown in the image above and press enter or the "OK" button.**

				2f. You should see a black box appear with white text. Click inside the black box and type "python" and press your enter key on your keyboard. You should see the following text above the red line shown below: 
				
				![enter image description here](https://github.com/jose011974/Python-Video-Downloader/blob/main/Readme%20Assets/Step%205.png?raw=true)
				
				**If you see the text "Python 3.11.0", you have successfully installed python! Otherwise, see the troubleshooting section for more information.**

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
			- **NOTE:** You MAY need to add an entry to your PATH environment variable. [Click Here](https://github.com/jose011974/Python-Video-Downloader/wiki/Adding-an-entry-to-your-PATH-environment-variable-on-Linux) for more information.
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

### Step 3 - Obtain Python Video Downloader

- Once you have completed Steps 1 & 2, you may now download the script. [Click here](https://github.com/jose011974/Python-Video-Downloader/releases "Click here") to download the latest public release.

### Step 4 - Run Python Video Downloader

1. Create a folder with any name you desire. For this example, the folder will be called `Python Video Downloader`. I suggest creating the folder on your desktop for easy access.
2. Place the script inside the folder (`Python Video Downloader`)
3. Run the script

**Windows 10/11 Instructions**:
- Assuming the defaults were selected, double click `Python Video Downloader.py` to launch the script. If you have extensions disabled, you may only see `Python Video Downloader`

If you have any issues launching the script, see Troubleshooting.

**Linux Instructions**:
- In order to allow the script to be executed with a double click gesture, you must right click and allow the script to be executed. This WILL differ depending on your file manager.

	- You can set this execution flag via the terminal with the following: `sudo chmod +x ./'Python Video Downloader.py'`
	- You can also run the script via the terminal with the following: `python3 ./'Python Video Downloader.py'`

Note: If you installed python in a custom directory on Linux, you may need to change the shebang line to match your installation. 

**The following will be checked once the script launches:**

	- pip installation
	- The presence of required packages
	- The presence of ffmpeg
 	- The presense of Firefox Profile folder in cookies.txt

Assuming everything was installed and works correctly, congration! You are now a proud operator of Python Video Downloader!

### HOWEVER

The script will prompt you to open a file called cookies.txt, and replace "PROFILE NAME GOES HERE" with the name of your Firefox Profile folder.

A Firefox Profile folder is essentially where all of your settings, bookmarks, history, cookies, etc. are stored for the Firefox Browser on your system.

For more information, please [click here.](https://github.com/jose011974/Python-Video-Downloader/wiki/How-to-use-cookies.txt)

If you have any issues, please go to the [troubleshooting](https://github.com/jose011974/Python-Video-Downloader/blob/main/README.md#troubleshooting "troubleshooting") section.

### Using Python Video Downloader

The main menu and the available options are shown below (current options may not be reflective in the screenshot below):

![Python Video Downloader Main Menu](https://i.imgur.com/GXBKfKi.png "Python Video Downloader Main Menu")

- **Option 1: Compress a single file**
	- This option will prompt for the full path of the file name, or if the file is in the same directory as the script, you can just type the file name and the extension.
	- Example: `C:\yourmotherisaspy\spy.mp4` | `spy.mp4`
- **Option 2: Compress multiple files in a folder**
	*- WARNING: THIS WILL SCAN *ALL* SUB DIRECTORES! IT IS RECOMMENDED TO PLACE THE IMAGES YOU WISH TO COMPRESS INTO A STANDALONE FOLDER.*
- **Option 3: Download and compress a media file from the internet**
	- This option will create a folder called `output` in the running directory and place the file inside `output`
- **Option 4: Download and compress multiple files from the internet**
	- This option uses a text file called `URL.txt` at the script directory to grab multiple URL's.
	- This option will create a folder called `output` in the running directory and place the files inside `output`
- **Option 5: Appends `SPOILER_` to the prefix of the file name in order to send media behind a spoiler tag on Discord**.
	- *WARNING: THIS WILL SCAN *ALL* SUB DIRECTORES! IT IS RECOMMENDED TO PLACE THE IMAGES YOU WISH TO COMPRESS INTO A STANDALONE FOLDER.*
- **Option 6: Removes the `SPOILER_` tag from the prefix of a file name.**
	- *WARNING: THIS WILL SCAN *ALL* SUB DIRECTORES! IT IS RECOMMENDED TO PLACE THE IMAGES YOU WISH TO COMPRESS INTO A STANDALONE FOLDER.*
- **Option 7: Any URLs that were not able to be downloaded will be placed in a text file called `Unsupported URLs.txt` .** This option will automatically go through all URLs in the text file and open them in your web browser so you can download them manually.
- **Option 8: Open the GitHub page of this script**
- **Option 9: Exit the script.**
- Option 0: Update dependencies

### Extra Notes:
- Only files above 25 MB will be compressed. This is because Discord wants money apparently.
- Only `jpg/jpeg, png, gif, mp4, and webm` files have been tested. In order to maintain compatabilty with all devices out there, the output file will be an `.mp4` file. The original file will not be deleted and instead have `old_` appended to the prefix of the file name. (Applies to compressing media)

### More information on how the Downloading and Compressing features work

`Python Video Downloader` uses yt-dlp for downloading media from the internet.
- In summary, yt-dlp will try to use an extractor to grab the media url and download it with the highest quality possible.
- If an extractor is not available, then a generic extractor is used and results will vary if the generic extractor is used.
	- This may result in a URL not being accessable and the script throwing an error message.


------------

`Python Video Downloader` uses ffmpeg to compress media.

- Here is the parameter used in `Python Video Downloader`: `-c:v libx264 -crf 23 -pix_fmt yuv420p`
	- This creates an H.264 MP4 file with moderate quality that is compatible with many devices.

This parameter is broken in that the output file can be larger than the source file. If you are trying to get the smallest file possible, I suggest using [Handbrake](https://handbrake.fr/).

# Troubleshooting

* **When you double click the script, nothing happens or you see a black box that disappears quickly:**
	* 1. Press Win + R to open the Run Dialog Box, then type "cmd" (without the quotes) and press Enter or OK.
	* 2. A black box with white text should appear. Drag the script onto the window and press enter. You should get an error message on why the script isn't opening.
	
	* Python Execution Error:
	![enter image description here](https://github.com/jose011974/Python-Video-Downloader/blob/main/Readme%20Assets/Python%20Execution%20Error.png?raw=true)
	* To fix this:
		1. Press your Windows Key and type "Apps and Features". Press enter.
		2. A window should open, and near the top, click on "App execution aliases"
		![enter image description here](https://github.com/jose011974/Python-Video-Downloader/blob/main/Readme%20Assets/Python%20Execution%20Error1.png?raw=true)
		3. Find "python.exe" and "python3.exe" near the bottom of the list. Turn the switches off and try running the script again.

# Credits

This script was created in thanks to:

- Twitter not adding a download button to tweets
- Discord not allowing regular members to upload files larger than 25 MB without paying:
	- $3 a month or $30 a year for a 50 MB cap 
	- $10 a month or $100 a year for a 500 MB cap

This script has been in the works since July of 2022.
- First version used MoviePy and had basic error checking.
- Second version used ffmpeg instead and had improved handling of errors
- Third version (current) still uses ffmpeg but now incorporates the Blessed library for visual effects and vastly improves on everything from compression to error handling.

This script was created with:
- Visual Studio Code
- Windows Subsystems for Linux
- VirtualBox - Used for testing on clean installs of Windows & Ubuntu/KDE Neon/Mint
- Sublime Text 4
- Lots of late nights, frustration filled days, drinking caffinated beverages, and pain.

You are not allowed to monetize anything from this repository.
