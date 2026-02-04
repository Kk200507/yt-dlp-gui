from yt_dlp import YoutubeDL


def download_video(url: str):
    """
    Downloads a video from the given URL using yt-dlp.
    This is engine code — no UI, no Tkinter.
    """

    def progress_hook(d):
        status = d.get("status")

        if status == "downloading":
            percent = d.get("_percent_str", "").strip()
            speed = d.get("_speed_str", "").strip()
            print(f"Downloading: {percent} at {speed}")

        elif status == "finished":
            print("Download finished, post-processing...")

    ydl_opts = {
        "format": "best",
        "outtmpl": "%(title)s.%(ext)s",
        "progress_hooks": [progress_hook],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    test_url = input("Enter video URL: ")
    download_video(test_url)
