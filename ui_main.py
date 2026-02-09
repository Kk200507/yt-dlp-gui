import os
import customtkinter as ctk
from threading import Thread
from tkinter import filedialog
from downloader import download_video, get_available_qualities
from about_dialog import AboutDialog
from history_dialog import HistoryDialog
from error_dialog import ErrorDialog
from error_handling import get_user_friendly_error

# MAIN UI WINDOW
class DownloaderUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ---------- App config ----------
        ctk.set_appearance_mode("Dark")   # Dark / Light / System
        ctk.set_default_color_theme("blue")

        self.title("yt-dlp GUI")
        # Slightly taller + resizable to prevent clipping on different DPI / font scaling
        self.geometry("900x580")
        self.minsize(820, 540)
        self.resizable(True, True)

        # Configure connection to grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Set icon
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "256.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # ---------- State ----------
        self.save_path = os.path.expanduser("~/Downloads")
        self._probe_seq = 0
        self._is_downloading = False
        self._app_status = "Idle"  # Idle / Probing / Downloading / Finished

        # ---------- Layout ----------
        self.create_sidebar()
        self.create_home_frame()
        self.set_app_status("Idle")

    # ---------- Status + UI enable/disable ----------
    def set_app_status(self, status: str):
        """Global UI status: Idle / Probing / Downloading / Finished."""
        self._app_status = status
        if hasattr(self, "app_status_label"):
            self.app_status_label.configure(text=f"Status: {status}")

    def _set_controls_enabled(self, *, url: bool, quality: bool, browse: bool, download: bool):
        self.url_entry.configure(state="normal" if url else "disabled")
        self.resolution_menu.configure(state="normal" if quality else "disabled")
        self.browse_btn.configure(state="normal" if browse else "disabled")
        self.download_btn.configure(state="normal" if download else "disabled")

    def _set_busy(self, mode: str, busy: bool):
        """
        mode: 'probing' or 'downloading'
        """
        if mode == "probing":
            if busy:
                self.set_app_status("Probing")
                # Allow URL editing so the user can fix/paste; lock the rest.
                self._set_controls_enabled(url=True, quality=False, browse=False, download=False)
            else:
                # If a download is running, don't override its locked state/status.
                if not self._is_downloading:
                    self.set_app_status("Idle")
                    # Quality/download enabling is handled by update_quality_menu().
                    self._set_controls_enabled(url=True, quality=True, browse=True, download=True)
        elif mode == "downloading":
            if busy:
                self._is_downloading = True
                self.set_app_status("Downloading")
                self._set_controls_enabled(url=False, quality=False, browse=False, download=False)
            else:
                self._is_downloading = False
                # Keep status as Finished/Error; caller decides next status.
                self._set_controls_enabled(url=True, quality=True, browse=True, download=True)
        else:
            raise ValueError(f"Unknown busy mode: {mode}")
    def open_history(self):
        HistoryDialog(self)

    def fetch_qualities(self):
        url = self.url_entry.get().strip()
        if not url:
            self.set_app_status("Idle")
            return

        self._probe_seq += 1
        probe_seq = self._probe_seq

        self._set_busy("probing", True)
        self.resolution_menu.set("Checking formats...")

        Thread(
            target=self._qualities_worker,
            args=(url, probe_seq),
            daemon=True
        ).start()


    def _qualities_worker(self, url, probe_seq: int):
        try:
            qualities = get_available_qualities(url)
        except Exception:
            qualities = ["Best"]

        self.after(0, lambda: self.update_quality_menu(qualities, url, probe_seq))


    def update_quality_menu(self, qualities, url: str, probe_seq: int):
        # Ignore stale probe results if the user changed the URL while probing.
        if probe_seq != self._probe_seq or url != self.url_entry.get().strip():
            return

        self.resolution_menu.configure(values=qualities, state="normal")
        self.resolution_var.set(qualities[0])
        #Qualities are ready → enable download
        self.download_btn.configure(state="normal")
        self.browse_btn.configure(state="normal")
        self._set_busy("probing", False)

    # ---------- Sidebar ----------
    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="YT-DLP GUI", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_home = ctk.CTkButton(
            self.sidebar_frame, 
            text="Home",
            command=self.sidebar_home_event
        )
        self.sidebar_button_home.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_history = ctk.CTkButton(
            self.sidebar_frame,
            text="History",
            command=self.open_history
        )
        self.sidebar_button_history.grid(row=2, column=0, padx=20, pady=10)


        self.sidebar_button_about = ctk.CTkButton(
            self.sidebar_frame, 
            text="About",
            command=self.open_about_dialog
        )
        self.sidebar_button_about.grid(row=3, column=0, padx=20, pady=10)

        # Appearance Mode
        self.appearance_mode_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Appearance Mode:", 
            anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["System", "Light", "Dark"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))
        
        # Select default
        self.appearance_mode_optionemenu.set("Dark")

    def sidebar_home_event(self):
        # Already on home, maybe reset? For now just pass
        pass

    def open_about_dialog(self):
        AboutDialog(self)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    # ---------- Main Panel (Home) ----------
    def create_home_frame(self):
        self.home_frame = ctk.CTkFrame(self, corner_radius=18, fg_color="transparent")
        self.home_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # We need a container for the 'main' content inside home_frame because
        # the original code packed everything into self.main
        self.main = ctk.CTkFrame(self.home_frame, corner_radius=18)
        self.main.pack(expand=True, fill="both")

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

        self.url_var = ctk.StringVar()

        self.url_entry = ctk.CTkEntry(
            self.card,
            height=40,
            corner_radius=10,
            textvariable=self.url_var
        )
        self.url_var.trace_add("write", self._on_url_change)

        self.url_entry.pack(fill="x", padx=20, pady=(0, 15))
        self.url_entry.bind("<FocusOut>", lambda e: self.fetch_qualities())

        # ---------- Resolution ----------
        ctk.CTkLabel(
            self.card,
            text="Quality",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=20)

        self.resolution_var = ctk.StringVar(value="Best")

        self.resolution_menu = ctk.CTkOptionMenu(
            self.card,
            values=["Paste URL first"],
            variable=self.resolution_var
        )
        self.resolution_menu.configure(state="disabled")
        self.resolution_menu.pack(anchor="w", padx=20, pady=(5, 15))

        ctk.CTkLabel(
            self.card,
            text="Output Format",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=20)

        self.container_var = ctk.StringVar(value="Auto")

        self.container_menu = ctk.CTkOptionMenu(
            self.card,
            values=["Auto", "MP4"],
            variable=self.container_var
        )
        self.container_menu.pack(anchor="w", padx=20, pady=(5, 15))

        # ---------- Save Path ----------
        path_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        path_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.path_label = ctk.CTkLabel(
            path_frame,
            text=f"Save to: {self.save_path}",
            anchor="w"
        )
        self.path_label.pack(side="left", fill="x", expand=True)

        self.browse_btn = ctk.CTkButton(
            path_frame,
            text="Browse",
            width=90,
            command=self.choose_folder
        )
        self.browse_btn.pack(side="right")

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
        self.download_btn.configure(state="disabled")

        # ---------- Global Status (always visible) ----------
        self.app_status_label = ctk.CTkLabel(
            self.main,
            text="Status: Idle",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#b084ff"
        )
        self.app_status_label.pack(pady=(0, 8))

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
    def _on_url_change(self, *args):
        # New input resets global status unless we're actively downloading.
        if not self._is_downloading:
            self.set_app_status("Idle")
        self.download_btn.configure(state="disabled")
        url = self.url_var.get().strip()

        # Avoid hammering yt-dlp on every keystroke
        if len(url) < 10:
            return

        # Debounce: cancel previous scheduled call
        if hasattr(self, "_format_job"):
            self.after_cancel(self._format_job)

        # Schedule format check after user pauses typing/pasting
        self._format_job = self.after(600, self.fetch_qualities)

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
        self._set_busy("downloading", True)

        url = self.url_entry.get().strip()
        if not url:
            self.set_progress("Please enter a valid URL")
            self._set_busy("downloading", False)
            self.set_app_status("Idle")
            return

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
        container = self.container_var.get().lower()

        def on_progress(status_msg, percent, speed, total, eta, info):
            # Update status label (main phase)
            self.after(0, lambda s=status_msg: self.status_label.configure(text=s))
            
            if status_msg == "Finished":
                self.after(0, lambda: self.set_app_status("Finished"))
            
            # Update progress bar
            if percent:
                try:
                    # Remove ANSI codes or extra chars if necessary, mostly yt-dlp percent is cleanish
                    clean_percent = percent.replace('%', '').strip()
                    value = float(clean_percent) / 100
                except ValueError:
                    value = 0
            else:
                value = self.progress_bar.get()
            
            self.after(0, lambda v=value: self.progress_bar.set(v))
            
            # Build detailed progress text
            # Goal: "86.9% of 117.77MiB at 7.32MiB/s ETA 00:02"
            parts = []
            
            if percent:
                if total:
                    parts.append(f"{percent} of {total}")
                else:
                    parts.append(percent)
            
            if speed:
                parts.append(f"at {speed}")
            
            if eta:
                parts.append(f"ETA {eta}")
            
            if info:
                # If we have info (like "Combining..."), it might be the only thing or separate
                if parts:
                    parts.append(f"• {info}")
                else:
                    parts.append(info)
            
            progress_text = " ".join(parts) if parts else ""
            self.after(0, lambda t=progress_text: self.set_progress(t))

        try:
            download_video(
                url,
                save_path=self.save_path,
                resolution=resolution,
                container=container,
                progress_callback=on_progress
            )
            self.after(0, self.on_download_complete)
        except Exception as e:
            error_msg = str(e)
            # Provide helpful message for ffmpeg errors
            self.after(0, lambda msg=error_msg: self.on_download_error(msg))

    def on_download_complete(self):
        # If we already marked it as Finished (e.g. via "already downloaded" logger), don't overwrite the message
        if self._app_status == "Finished":
             self._set_busy("downloading", False)
             return

        self.status_label.configure(text="✓ Complete")
        self.set_app_status("Finished")
        self.set_progress("Download finished successfully!")
        self.progress_bar.set(1.0)
        self._set_busy("downloading", False)

    def on_download_error(self, error_msg):
        self.status_label.configure(text="✗ Error")
        
        # Determine friendly message
        title, friendly_desc = get_user_friendly_error(error_msg)
        
        # Update inline progress validation - keep it short, dialog has full details
        self.set_progress(f"Failed: {title}")
        
        self._set_busy("downloading", False)
        self.set_app_status("Idle")
        
        # Show the polished dialog
        ErrorDialog(self, title=title, description=friendly_desc, raw_error=error_msg)

    def set_progress(self, text):
        self.progress_label.configure(text=text)


if __name__ == "__main__":
    app = DownloaderUI()
    app.mainloop()
