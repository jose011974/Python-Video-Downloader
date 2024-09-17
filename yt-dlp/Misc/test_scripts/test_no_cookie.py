import platform
import yt_dlp
import os

def clear():
    command = 'clear' # Unix
    if platform.system() == "Windows": command = 'cls' # Windows
    os.system(command)

# Logger for yt-dlp
class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def downloadStatus(d):
    if d['status'] == 'finished': # Download status complete
        
        #downFileList.append(d['filename'])

        print("\nDownloading complete.\n")

if platform.system() == "Linux":
    cookie = ('firefox', None, None, None)

    # AppData\Roaming\Mozilla\Firefox\Profiles\ - Windows
    # /home/blunt/.mozilla/firefox/             - Linux

# Parameters for yt-dlp.
# See https://github.com/yt-dlp/yt-dlp/blob/5ab3534d44231f7711398bc3cfc520e2efd09f50/yt_dlp/YoutubeDL.py#L159
ydl_opts = {
    'outtmpl': f'%(id)s.%(ext)s',
    'restrictfilenames': True,
    'no_color': True,
    'logger': MyLogger(),
    'progress_hooks': [downloadStatus],
    'cookiesfrombrowser': cookie
}

clear()

uri = 'https://twitter.com/i/status/1754205509895233573'

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([uri])

