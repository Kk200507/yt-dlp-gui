import customtkinter as ctk
from history import load_history, clear_history

class HistoryDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Download History")
        self.geometry("600x500")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        # Header with title and Clear button
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header_frame,
            text="Download History",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")

        self.clear_btn = ctk.CTkButton(
            header_frame,
            text="Clear History",
            fg_color="#cf3a3a",
            hover_color="#a82323",
            width=100,
            command=self.on_clear_history
        )
        self.clear_btn.pack(side="right")

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.load_items()

    def load_items(self):
        # Clear existing widgets in scroll_frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        history = load_history()

        if not history:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No downloads yet.",
                text_color="gray"
            ).pack(pady=40)
            self.clear_btn.configure(state="disabled")
            return
        
        self.clear_btn.configure(state="normal")

        for item in history:
            self._add_item(item)

    def _add_item(self, item):
        frame = ctk.CTkFrame(self.scroll_frame, fg_color=("gray85", "gray20"))
        frame.pack(fill="x", pady=5)

        title = item.get("title", "Unknown title")
        
        # Determine best resolution string
        if item.get("height"):
            resolution = f"{item['height']}p"
        else:
            resolution = item.get("resolution") or "—"
            
        url = item.get("url", "")

        # date = item.get("timestamp", "")[:10]

        # Title
        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=520,
            justify="left",
            anchor="w"
        ).pack(fill="x", padx=10, pady=(8, 2))

        # Details row
        details_frame = ctk.CTkFrame(frame, fg_color="transparent")
        details_frame.pack(fill="x", padx=10, pady=(0, 8))

        ctk.CTkLabel(
            details_frame,
            text=f"Resolution: {resolution}",
            font=ctk.CTkFont(size=12),
            text_color="gray70"
        ).pack(side="left")

        ctk.CTkLabel(
            details_frame,
            text=url,
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        ).pack(side="right")

    def on_clear_history(self):
        clear_history()
        self.load_items()

