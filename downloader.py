import os
from yt_dlp import YoutubeDL

def download_video(url: str, save_path: str = None, resolution: str = "Best", progress_callback=None):
    """
    Downloads a video using yt-dlp.
    progress_callback: function(percent: str, speed: str)
    """

    def progress_hook(d):
        status = d.get("status")

        if status == "downloading":
            percent = d.get("_percent_str", "").strip()
            speed = d.get("_speed_str", "").strip()

            if progress_callback:
                progress_callback(percent, speed)

        elif status == "finished":
            if progress_callback:
                progress_callback("100%", "Finishing...")

    # Format selection based on resolution
    format_selector = "best"
    if resolution == "Audio only":
        format_selector = "bestaudio/best"
    elif resolution == "1080p":
        format_selector = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
    elif resolution == "720p":
        format_selector = "bestvideo[height<=720]+bestaudio/best[height<=720]"
    elif resolution == "480p":
        format_selector = "bestvideo[height<=480]+bestaudio/best[height<=480]"
    
    # Output template
    if save_path:
        outtmpl = os.path.join(save_path, "%(title)s.%(ext)s")
    else:
        outtmpl = "%(title)s.%(ext)s"

    ydl_opts = {
        "format": format_selector,
        "outtmpl": outtmpl,
        "progress_hooks": [progress_hook],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])



if __name__ == "__main__":
    test_url = input("Enter video URL: ")
    download_video(test_url)
