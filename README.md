# Youtube-to-mp3

This is a simple python script created with the GPT-3 chatbot, even this README file was created by it, the code had some bugs and didn't do everything I asked for so some of the code is mine. It downloads a youtube video and converts it to mp3. It also displays a fixed-length progress bar with a percentage indicator and shows the total time taken to download the youtube video.

## Updates
Using [yt-dlp](https://github.com/yt-dlp/yt-dlp) now, that is a youtube-dl fork based on the now inactive youtube-dlc.

## Requirements

* Python 3.x

* Install requirements:
    `pip install -r requirements.txt`

* Also install **ffmpeg**:

    For Debian-based Linux distributions:
    ```
    sudo apt update
    sudo apt install ffmpeg
    ```

    For Red Hat-based Linux distributions:
    ```
    sudo yum install ffmpeg
    ```

    For macOS (using Homebrew):
    ```
    brew install ffmpeg
    ```

* In case there is any error related to cryptography, update it with: `python3 -m pip install -U cryptography`

## Usage:

`$ python youtube_to_mp3.py [youtube_video_url]`

The script will download the youtube video as an mp3 file in the highest possible quality and save it 
in the Downloads folder located in this same directory. It will also display a progress bar with a percentage indicator as the download is in progress. When the download is complete, it will display the total time taken to download the youtube video.

## TODO:

- [ ] Accept both `[youtube_video_url]` or `[youtube_video_ID]`
- [ ] Download 1 or more file from list in external file
- [ ] Select audio quality
- [ ] Add lyrics?