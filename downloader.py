import os
import shutil
from yt_dlp import YoutubeDL
from history import save_history_entry

def get_available_qualities(url: str):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # save_history_entry(info)

    formats = info.get("formats", [])
    heights = set()
    has_audio = False

    for f in formats:
        if f.get("vcodec") != "none" and f.get("height"):
            heights.add(f["height"])
        if f.get("acodec") != "none":
            has_audio = True

    qualities_set = set()
    standard_heights = [144, 240, 360, 480, 720, 1080, 1440, 2160, 4320]
    
    for h in heights:
        # Snap to nearest standard, but prefer snapping up to ensure quality
        # Actually, best approach: Use buckets.
        # If h is close to a standard, map it.
        # If h > max standard, map to "Original" or nearest.
        
        # Simple approach: Find closest standard height
        closest = min(standard_heights, key=lambda x: abs(x - h))
        qualities_set.add(closest)

    qualities = sorted(list(qualities_set), reverse=True)
    result = [f"{h}p" for h in qualities]

    if has_audio:
        result.append("Audio only")

    if not result:
        result.append("Best")

    return result


def check_ffmpeg():
    """Check if ffmpeg is available in the system PATH."""
    return shutil.which("ffmpeg") is not None


def download_video(
    url: str,
    save_path: str = None,
    resolution: str = "Best",
    container: str = "auto",   # "auto" | "mp4"
    progress_callback=None
):

    """
    progress_callback: function(status: str, percent: str, speed: str, total: str, eta: str, info: str)
    """

    class InterceptLogger:
        def debug(self, msg):
            if "already been downloaded" in msg:
                 if progress_callback:
                     progress_callback("Finished", "100%", "", "", "", "File already exists - skipped download")
            pass
        def warning(self, msg):
            pass
        def error(self, msg):
            pass
        def info(self, msg):
            pass

    def progress_hook(d):
        status = d.get("status")
        filename = d.get("filename", "")
        postprocessor = d.get("postprocessor")
        
        # Determine what's being downloaded/processed
        if status == "downloading":
            percent = d.get("_percent_str", "").strip()
            speed = d.get("_speed_str", "").strip()
            total = d.get("_total_bytes_str") or d.get("_total_bytes_estimate_str", "")
            total = total.strip()
            eta = d.get("_eta_str", "").strip()
            
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
                progress_callback(status_msg, percent, speed, total, eta, "")

        elif status == "downloaded":
            if progress_callback:
                progress_callback("Downloaded", "100%", "", "", "", "Preparing to merge...")

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
                progress_callback(status_msg, "", "", "", "", info)

        elif status == "finished":
            if progress_callback:
                progress_callback("Finished", "100%", "", "", "", "Download complete!")

    # Format selection based on resolution
    format_selector = "best"

    if resolution == "Audio only":
        format_selector = "bestaudio/best"

    elif resolution.endswith("p"):
        height = resolution.replace("p", "")
        format_selector = f"bestvideo[height<={height}]+bestaudio/best"

    # Container preference (MP4)

    if container == "mp4":
        if resolution == "Audio only":
            format_selector = "bestaudio[ext=m4a]/bestaudio"
        elif resolution.endswith("p"):
            height = resolution.replace("p", "")
            format_selector = f"bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        else:
            # Resolution is "Best" or unknown
            format_selector = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    
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
    "logger": InterceptLogger(),
    "merge_output_format": "mp4" if container == "mp4" else None,
}


    # Note: yt-dlp will automatically detect and use ffmpeg if available
    # We don't need to check manually - yt-dlp will handle it gracefully

    # Notify that we're fetching video info
    if progress_callback:
        progress_callback("Fetching info", "", "", "", "", "Getting video information...")

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    save_history_entry(info)


if __name__ == "__main__":
    test_url = input("Enter video URL: ")
    download_video(test_url)
