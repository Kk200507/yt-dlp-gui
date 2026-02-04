import tkinter as tk
from threading import Thread
from downloader import download_video


class DownloaderUI:
    def __init__(self, root):
        self.root = root
        self.root.title("yt-dlp GUI")

        tk.Label(root, text="Video URL").pack(pady=5)

        self.url_entry = tk.Entry(root, width=55)
        self.url_entry.pack(pady=5)

        self.status_label = tk.Label(root, text="Idle")
        self.status_label.pack(pady=5)

        download_btn = tk.Button(
            root,
            text="Download",
            command=self.start_download
        )
        download_btn.pack(pady=10)

    def start_download(self):
        url = self.url_entry.get()
        self.set_status("Downloading...")

        # ✅ start background thread
        thread = Thread(
            target=self.run_download,
            args=(url,),
            daemon=True
        )
        thread.start()

    def run_download(self, url):
        # This runs in a worker thread
        download_video(url)

        # Schedule UI update safely
        self.root.after(0, lambda: self.set_status("Done"))

    def set_status(self, text):
        self.status_label.config(text=text)
