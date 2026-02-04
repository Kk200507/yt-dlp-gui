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
        # Slightly taller + resizable to prevent clipping on different DPI / font scaling
        self.geometry("900x580")
        self.minsize(820, 540)
        self.resizable(True, True)
        
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
        self.main.pack(expand=True, fill="both", padx=20, pady=15)

        ctk.CTkLabel(
            self.main,
            text="Download Video or Audio from YouTube",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self.main,
            text="Paste a link (or search) • pick quality • download",
            font=ctk.CTkFont(size=14),
            text_color="#b084ff"
        ).pack(pady=(0, 15))

        # ---------- Card ----------
        self.card = ctk.CTkFrame(self.main, corner_radius=16)
        self.card.pack(padx=60, pady=8, fill="x")

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
        self.download_btn.pack(pady=(16, 10))

        # ---------- Progress Area (hidden until download starts) ----------
        self.progress_area = ctk.CTkFrame(self.main, fg_color="transparent")
        # Note: do NOT pack this yet.

        self.progress_bar = ctk.CTkProgressBar(
            self.progress_area,
            width=420,
            height=18,
            corner_radius=10
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(6, 4))

        # Status updating text below the bar (details like %, speed, etc.)
        self.progress_label = ctk.CTkLabel(
            self.progress_area,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(pady=(0, 4))

        # Phase text (Downloading / Merging / Finished) below the detail text
        self.status_label = ctk.CTkLabel(
            self.progress_area,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#b084ff"
        )
        self.status_label.pack(pady=(0, 6))

    def show_progress_area(self):
        if not self.progress_area.winfo_ismapped():
            self.progress_area.pack(pady=(0, 8))

    def hide_progress_area(self):
        if self.progress_area.winfo_ismapped():
            self.progress_area.pack_forget()

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
        self.show_progress_area()
        self.progress_bar.set(0)
        self.status_label.configure(text="Initializing...")
        self.set_progress("")

        Thread(
            target=self.run_download,
            args=(url,),
            daemon=True
        ).start()

    def run_download(self, url):
        resolution = self.resolution_var.get()

        def on_progress(status_msg, percent, speed, info):
            # Update status label (main phase)
            self.after(0, lambda s=status_msg: self.status_label.configure(text=s))
            
            # Update progress bar
            if percent:
                try:
                    value = float(percent.strip('%')) / 100
                except ValueError:
                    value = 0
            else:
                value = self.progress_bar.get()  # Keep current value if no percent
            
            self.after(0, lambda v=value: self.progress_bar.set(v))
            
            # Build detailed progress text
            progress_parts = []
            if percent:
                progress_parts.append(percent)
            if speed:
                progress_parts.append(speed)
            if info:
                progress_parts.append(info)
            
            progress_text = " • ".join(progress_parts) if progress_parts else ""
            self.after(0, lambda t=progress_text: self.set_progress(t))

        try:
            download_video(
                url,
                save_path=self.save_path,
                resolution=resolution,
                progress_callback=on_progress
            )
            self.after(0, self.on_download_complete)
        except Exception as e:
            self.after(0, lambda: self.on_download_error(str(e)))

    def on_download_complete(self):
        self.status_label.configure(text="✓ Complete")
        self.set_progress("Download finished successfully!")
        self.progress_bar.set(1.0)
        self.download_btn.configure(state="normal")

    def on_download_error(self, error_msg):
        self.status_label.configure(text="✗ Error")
        self.set_progress(f"Error: {error_msg}")
        self.download_btn.configure(state="normal")

    def set_progress(self, text):
        self.progress_label.configure(text=text)


if __name__ == "__main__":
    app = DownloaderUI()
    app.mainloop()
