import customtkinter as ctk
import webbrowser

class AboutDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("About")
        self.geometry("420x360")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="YT-DLP GUI",
            font=ctk.CTkFont(size=22, weight="bold")
        ).grid(row=0, column=0, pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="Version 0.1.0"
        ).grid(row=1, column=0, pady=(0, 15))

        ctk.CTkLabel(
            self,
            text="A simple graphical interface for yt-dlp,\n"
                 "designed for non-technical users.",
            justify="center",
            wraplength=360
        ).grid(row=2, column=0, pady=10)

        ctk.CTkLabel(
            self,
            text="Disclaimer:\n"
                 "This application does NOT bypass DRM or paywalls.\n"
                 "Downloading copyrighted content may be illegal.\n"
                 "You are solely responsible for how you use this software.",
            justify="center",
            wraplength=360,
            text_color="gray"
        ).grid(row=3, column=0, pady=15)

        ctk.CTkLabel(
            self,
            text="Credits:\n• yt-dlp\n• FFmpeg",
            justify="center"
        ).grid(row=4, column=0, pady=10)

        ctk.CTkButton(
            self,
            text="GitHub Repository",
            command=lambda: webbrowser.open(
                "https://github.com/Kk200507/yt-dlp-gui"
            )
        ).grid(row=5, column=0, pady=(10, 5))

        ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy,
            fg_color="gray"
        ).grid(row=6, column=0, pady=(5, 20))