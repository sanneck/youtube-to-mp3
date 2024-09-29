import yt_dlp
import time
import os
import sys
import re

# Get current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
download_folder = os.path.join(current_dir, 'Downloads')

# Create Downloads folder if it doesn't exist
try:
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
except OSError as e:
    print(f"Error creating Downloads directory: {e}")
    sys.exit(1)

os.chdir(current_dir)

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
        # Remove escape sequences using regex
        progress = re.sub(r'\x1b[^m]*m', '', progress)
        progress = progress.split('%')[0].strip()  # Remove '%' symbol and leading/trailing spaces
        progress = float(progress)  # Convert the cleaned string to a float

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

# Function to handle playlists
def download_playlist(playlist_url):
    # Create a temporary directory to fetch playlist metadata
    temp_opts = {
        'quiet': True,
        'extract_flat': True,  # Extract metadata only, don't download
    }

    # Extract playlist metadata to get the playlist title
    with yt_dlp.YoutubeDL(temp_opts) as temp_ydl:
        playlist_info = temp_ydl.extract_info(playlist_url, download=False)
        playlist_title = playlist_info.get('title', 'Playlist')

    # Remove any invalid characters for folder names
    playlist_title = re.sub(r'[<>:"/\\|?*]', '', playlist_title)

    # Create a folder for the playlist in the Downloads folder
    playlist_folder = os.path.join(download_folder, playlist_title)
    try:
        if not os.path.exists(playlist_folder):
            os.makedirs(playlist_folder)
    except OSError as e:
        print(f"Failed to create directory {playlist_folder}: {e}")
        sys.exit(1)

    # Set download options for the playlist
    ydl_opts_playlist = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(playlist_folder, '%(playlist_index)s - %(title)s.%(ext)s'),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
        "logger": MyLogger(),
        "progress_hooks": [],
        "noplaylist": False  # Ensure the entire playlist is downloaded
    }

    # Download the playlist
    with CustomYoutubeDL(ydl_opts_playlist) as ydl:
        ydl.download([playlist_url])

# Function to handle single videos
def download_video(video_url):
    ydl_opts_video = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(download_folder, '%(title)s.%(ext)s'),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
        "logger": MyLogger(),
        "progress_hooks": [],
    }

    # Download the video
    with CustomYoutubeDL(ydl_opts_video) as ydl:
        ydl.download([video_url])

# Record the start time
start = time.time()

# Get the youtube video or playlist URL from the command-line arguments
if len(sys.argv) != 2:
    print("Usage: python youtube_to_mp3.py '[youtube_video_or_playlist_url]'")
    sys.exit(1)

video_url = sys.argv[1]

print("\nDownloading..\n")

# Check if the URL is a playlist (check for 'list=' in the URL)
if 'list=' in video_url:
    download_playlist(video_url)
else:
    download_video(video_url)

# Record the end time and calculate the total time taken
end = time.time()
total_time = end - start

# Display the total time taken
print("\nTotal time taken: {} seconds".format(round(total_time, 1)))
