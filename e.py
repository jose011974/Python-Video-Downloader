import subprocess
import platform
import os
import time
import sys
import requests

os.chdir(os.path.dirname(__file__))

command = 'clear' # Unix
if platform.system() == "Windows": command = 'cls' # Windows
os.system(command)

os.chdir(os.path.dirname(__file__))
url = "https://bootstrap.pypa.io/get-pip.py"
response = requests.get(url, allow_redirects=True)

with open("./get-pip.py", "wb") as f:
    f.write(response.content)

print("pip, python's package manager, is not installed. I will attempt to download and install it for you.\n\n")

time.sleep(3)

if not response.status_code == 200:
    command = 'clear' # Unix
    if platform.system() == "Windows": command = 'cls' # Windows
    os.system(command)

    print("Unable to download pip. Please install pip manually or from https://bootstrap.pypa.io/get-pip.py and execute the script. Aborting.")
    sys.exit()
try:
    subprocess.check_call([os.system("get-pip.py")])
    print("\n\nIf you see this, that means that pip installed with no issue. The script will continue to run after 5 seconds...")

except:

    print("\n\nPip exited with an error. For the most part, you can google the error and find an appropriate solution. If you are unable to find a solution, " +
    "please go to [placeholder for URL]")