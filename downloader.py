import os
from yt_dlp import YoutubeDL

def download_video(url: str, save_path: str = None, resolution: str = "Best", progress_callback=None):
    """
    Downloads a video using yt-dlp.
    progress_callback: function(status: str, percent: str, speed: str, info: str)
    """

    def progress_hook(d):
        status = d.get("status")
        filename = d.get("filename", "")
        postprocessor = d.get("postprocessor")
        
        # Determine what's being downloaded/processed
        if status == "downloading":
            percent = d.get("_percent_str", "").strip()
            speed = d.get("_speed_str", "").strip()
            
            # Try to determine if downloading video or audio
            if filename:
                if any(ext in filename.lower() for ext in [".f", "video", ".mp4", ".webm"]):
                    status_msg = "Downloading video"
                elif any(ext in filename.lower() for ext in ["audio", ".m4a", ".opus", ".mp3"]):
                    status_msg = "Downloading audio"
                else:
                    status_msg = "Downloading"
            else:
                status_msg = "Downloading"
            
            if progress_callback:
                progress_callback(status_msg, percent, speed, "")

        elif status == "downloaded":
            if progress_callback:
                progress_callback("Downloaded", "100%", "", "Preparing to merge...")

        elif status == "processing" or postprocessor:
            postprocessor_name = ""
            if postprocessor:
                postprocessor_name = str(postprocessor.get("_name", "")).lower()
            
            # Check if merging based on postprocessor name or assume merging if processing after download
            if postprocessor_name and ("merge" in postprocessor_name or "ffmpeg" in postprocessor_name):
                status_msg = "Merging"
                info = "Combining audio and video streams..."
            elif status == "processing":
                # If status is processing, it's likely merging (especially for video+audio formats)
                status_msg = "Merging"
                info = "Combining audio and video streams..."
            else:
                status_msg = "Processing"
                info = "Processing files..."
            
            if progress_callback:
                progress_callback(status_msg, "", "", info)

        elif status == "finished":
            if progress_callback:
                progress_callback("Finished", "100%", "", "Download complete!")

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
        "quiet": False,
        "no_warnings": False,
    }

    # Notify that we're fetching video info
    if progress_callback:
        progress_callback("Fetching info", "", "", "Getting video information...")

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])



if __name__ == "__main__":
    test_url = input("Enter video URL: ")
    download_video(test_url)
