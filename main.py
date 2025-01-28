# Step 1: Install yt-dlp and ffmpeg in Colab
!pip install yt-dlp
!apt update && apt install -y ffmpeg

import yt_dlp
import time
import os

# Step 2: (Optional) Mount Google Drive if you want to save files there
from google.colab import drive
drive.mount('/content/drive')

# Define the download directory
DOWNLOAD_DIR = "/content/drive/MyDrive/yt_downloads"  # Save files to Google Drive
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Function to print progress and slow down the requests between downloads
def hook(d):
    if d['status'] == 'finished':
        print(f"\nDownload complete: {d['filename']}")
        print(f"Elapsed time: {d['elapsed']} seconds")
        # Adding a delay after each download
        time.sleep(5)  # Adjust the delay as needed (in seconds)

# Function to download videos from a playlist in 720p and MP4 format
def download_video_from_playlist(playlist_url):
    # Define the download options for yt-dlp
    ydl_opts = {
        'format': 'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]',  # Download MP4 video
        'merge_output_format': 'mp4',  # Ensure the final output is in MP4
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),  # Specify output location with video title
        'noplaylist': False,  # Download all videos from a playlist
        'quiet': False,  # Show verbose output
        'progress_hooks': [hook],  # Track progress during the download
        'postprocessors': [{  # Use FFmpeg to clean up
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # Convert everything to MP4
        }]
    }

    # Use yt-dlp to download the playlist
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Starting download for playlist: {playlist_url}")
            ydl.download([playlist_url])  # Start downloading the playlist
    except Exception as e:
        print(f"Failed to download playlist {playlist_url}: {e}")

# Main function to start the download process
def start_download(playlist_url):
    download_video_from_playlist(playlist_url)

# Step 3: Enter the playlist URL to download
if __name__ == "__main__":
    playlist_url = "https://youtube.com/playlist?list=PL9Zg64loGCGBN9D-dev7aJIwmO19xgFpa&si=MOW8LgCOH2zo7lj9"  # Replace with your playlist URL
    start_download(playlist_url)
