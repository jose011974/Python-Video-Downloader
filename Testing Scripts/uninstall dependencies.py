import subprocess
import sys

packages = ["blessed", "numpy", "python-magic", "Pillow", "psutil", "requests", "validators", "youtube-dl"]

for p in packages:
    subprocess.run([sys.executable, "-m", "pip", "uninstall", p, '-y'])