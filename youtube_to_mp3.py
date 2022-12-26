import yt_dlp
import time
import os
import sys

# Get current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
download_folder = current_dir + '/Downloads/'

try:
        
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
except OSError:
    pass

os.chdir(os.path.dirname(download_folder))

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class ProgressBar(object):
    def __init__(self, total_length, filled_char="=", empty_char=" "):
        self.total_length = total_length
        self.filled_char = filled_char
        self.empty_char = empty_char
        self.reset()

    def reset(self):
        self.filled_length = 0

    def update(self, progress):
        progress = float(progress.split('%')[0])
        num_filled = int(progress)
        num_empty = self.total_length - num_filled

        if num_filled < self.filled_length:
            self.reset()

        self.filled_length = num_filled
        filled_str = self.filled_char * self.filled_length
        empty_str = self.empty_char * num_empty
        print("\r[{}{}] {}%".format(filled_str, empty_str, progress), end="")

# Define a custom class that extends the base YoutubeDL class and adds a progress bar
class CustomYoutubeDL(yt_dlp.YoutubeDL):
    def __init__(self, *args, **kwargs):
        super(CustomYoutubeDL, self).__init__(*args, **kwargs)
        self.progress_bar = ProgressBar(100)
        self.add_progress_hook(self.on_progress_hook)

    def on_progress_hook(self, d):
        if d["status"] == "downloading":
            self.progress_bar.update(d["_percent_str"])

# Define the youtube-dl options
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "%(title)s.%(ext)s",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            #"preferredquality": "320",
        }
    ],
    "logger": MyLogger(),
    "progress_hooks": [],
}

# Record the start time
start = time.time()

# Get the youtube video URL from the command-line arguments
if len(sys.argv) != 2:
    print("Usage: python youtube_to_mp3.py [youtube_video_url]")
    sys.exit(1)

video_url = sys.argv[1]

print("\nDownloading..\n")
# Download the youtube video as an mp3
with CustomYoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

# Record the end time and calculate the total time taken
end = time.time()
total_time = end - start

# Display the total time taken
print("\nTotal time taken: {} seconds".format(round(total_time, 1)))
