import os
import customtkinter as ctk
from threading import Thread
from tkinter import filedialog

from downloader import download_video


class DownloaderUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ---------- App config ----------
        ctk.set_appearance_mode("Dark")   # Dark / Light / System
        ctk.set_default_color_theme("blue")

        self.title("yt-dlp")
        self.geometry("900x520")
        self.resizable(False, False)
        
        # Set icon
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "256.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # ---------- State ----------
        self.save_path = os.path.expanduser("~/Downloads")

        # ---------- Layout ----------
        self.create_main_panel()

    # ---------- Main Panel ----------
    def create_main_panel(self):
        self.main = ctk.CTkFrame(self, corner_radius=18)
        self.main.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(
            self.main,
            text="Download Audio from YouTube",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            self.main,
            text="Paste a link or song name and relax",
            font=ctk.CTkFont(size=14),
            text_color="#b084ff"
        ).pack(pady=(0, 25))

        # ---------- Card ----------
        self.card = ctk.CTkFrame(self.main, corner_radius=16)
        self.card.pack(padx=60, pady=10, fill="x")

        ctk.CTkLabel(
            self.card,
            text="YouTube URL or Search",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.url_entry = ctk.CTkEntry(self.card, height=40, corner_radius=10)
        self.url_entry.pack(fill="x", padx=20, pady=(0, 15))

        # ---------- Resolution ----------
        ctk.CTkLabel(
            self.card,
            text="Quality",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=20)

        self.resolution_var = ctk.StringVar(value="Best")

        self.resolution_menu = ctk.CTkOptionMenu(
            self.card,
            values=["Best", "1080p", "720p", "480p", "Audio only"],
            variable=self.resolution_var
        )
        self.resolution_menu.pack(anchor="w", padx=20, pady=(5, 15))

        # ---------- Save Path ----------
        path_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        path_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.path_label = ctk.CTkLabel(
            path_frame,
            text=f"Save to: {self.save_path}",
            anchor="w"
        )
        self.path_label.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            path_frame,
            text="Browse",
            width=90,
            command=self.choose_folder
        ).pack(side="right")

        # ---------- Download Button ----------
        self.download_btn = ctk.CTkButton(
            self.main,
            text="Download",
            height=50,
            width=200,
            corner_radius=25,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.start_download
        )
        self.download_btn.pack(pady=(25, 15))

        # ---------- Progress ----------
        self.progress_bar = ctk.CTkProgressBar(
            self.main,
            width=420,
            height=18,
            corner_radius=10
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(10, 5))

        self.progress_label = ctk.CTkLabel(
            self.main,
            text="",
            font=ctk.CTkFont(size=13)
        )
        self.progress_label.pack(pady=(5, 10))

    # ---------- Folder Picker ----------
    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_path = folder
            self.path_label.configure(text=f"Save to: {folder}")

    # ---------- Download Logic ----------
    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            self.set_progress("Please enter a valid URL")
            return

        self.download_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.set_progress("Starting download...")

        Thread(
            target=self.run_download,
            args=(url,),
            daemon=True
        ).start()

    def run_download(self, url):
        resolution = self.resolution_var.get()

        def on_progress(percent, speed):
            try:
                value = float(percent.strip('%')) / 100
            except ValueError:
                value = 0

            self.after(0, lambda: self.progress_bar.set(value))
            self.after(
                0,
                lambda: self.set_progress(f"{percent} • {speed}")
            )

        download_video(
            url,
            save_path=self.save_path,
            resolution=resolution,
            progress_callback=on_progress
        )

        self.after(0, self.on_download_complete)

    def on_download_complete(self):
        self.set_progress("Download complete")
        self.download_btn.configure(state="normal")

    def set_progress(self, text):
        self.progress_label.configure(text=text)


if __name__ == "__main__":
    app = DownloaderUI()
    app.mainloop()
