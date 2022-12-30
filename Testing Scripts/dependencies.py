import os
import subprocess
import platform
import time
import sys

def clear():
    command = 'clear' # Unix
    if platform.system() == "Windows": command = 'cls' # Windows
    os.system(command)

clear()

print("Validating Dependency Requirements...\n")

try:
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
except subprocess.CalledProcessError:
    import requests

    os.chdir(os.path.dirname(__file__))
    url = "https://bootstrap.pypa.io/get-pip.py"
    response = requests.get(url, allow_redirects=True)

    print("pip, python's package manager, is not installed. I will attempt to download and install it for you. (3)\n\n")
    time.sleep(3)

    if not response.status_code == 200:
        command = 'clear' # Unix
        if platform.system() == "Windows": command = 'cls' # Windows
        os.system(command)

        print("I was unable to download pip. Please install pip manually (Google is your friend) or from " +
        "https://bootstrap.pypa.io/get-pip.py and execute the script. Exiting...")
        sys.exit()
    try:
        subprocess.check_call([os.system("./get-pip.py")])
        print("Pip should have installed without error. Please run this script again. If you keep seeing this message, you may want to try " +
        "adding your python installation to your PATH or read through the terminal and see if there are any errors. Exiting...")
        sys.exit()

    except:
        command = 'clear' # Unix
        if platform.system() == "Windows": command = 'cls' # Windows
        os.system(command)

        print("An unknown error has occured. Please file a bug report at " +
        "https://github.com/jose011974/Download-Compress-Media/wiki/Create-a-Bug-Report and be sure to include a copy of the terminal output.")

packages = ["python-magic", "Pillow", "youtube-dl"]

# Turns out the library needed for magic on Windows has been out of date since 2009. These are up to date and will work with Windows 10.
if platform.system() == "Windows":
    packages.append("python-magic-bin")

# Check if the packages are installed
for p in packages:
    if not p in installed_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", p])
        #Uh oh.
        except Exception as e:
            print(e)
    elif p in installed_packages:
        time.sleep(0.3)

clear()

print("Dependencies validated.")