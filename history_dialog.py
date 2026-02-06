import customtkinter as ctk
from history import load_history

class HistoryDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Download History")
        self.geometry("600x400")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        history = load_history()

        container = ctk.CTkScrollableFrame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        if not history:
            ctk.CTkLabel(
                container,
                text="No downloads yet."
            ).pack(pady=20)
            return

        for item in history:
            self._add_item(container, item)

    def _add_item(self, parent, item):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=5)

        title = item.get("title", "Unknown title")
        resolution = item.get("resolution") or "—"
        url = item.get("url", "")

        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(weight="bold"),
            wraplength=520,
            justify="left"
        ).pack(anchor="w", padx=10, pady=(6, 0))

        ctk.CTkLabel(
            frame,
            text=f"Resolution: {resolution}",
            text_color="gray"
        ).pack(anchor="w", padx=10)

        ctk.CTkLabel(
            frame,
            text=url,
            text_color="gray",
            wraplength=520
        ).pack(anchor="w", padx=10, pady=(0, 6))
