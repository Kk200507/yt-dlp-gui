import customtkinter as ctk

class OverwriteDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_overwrite, on_skip, on_cancel):
        super().__init__(parent)
        self.on_overwrite = on_overwrite
        self.on_skip = on_skip
        self.on_cancel = on_cancel

        self.title("File Already Exists")
        self.geometry("400x180")
        self.resizable(False, False)
        
        # Center the dialog
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (180 // 2)
        self.geometry(f"+{x}+{y}")

        # Make modal
        self.transient(parent)
        self.grab_set()
        self.focus_force()

        # UI Elements
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)

        msg_label = ctk.CTkLabel(
            self,
            text="A file with the same name already exists\nfor this resolution and format.\n\nWhat would you like to do?",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        msg_label.pack(pady=(20, 20), padx=20)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        # Buttons
        # Use simple colors or default theme. 
        # User requested: Overwrite, Skip, Cancel.
        
        self.btn_overwrite = ctk.CTkButton(
            btn_frame, 
            text="Overwrite", 
            fg_color="#e63946", # Red-ish for destructive/force action? Or maybe standard blue? 
                               # "Green" for go? Usually Overwrite is a bit "warning".
                               # Let's stick to theme or a distinct color. 
                               # User didn't specify color, but "Standard desktop behavior".
            hover_color="#c92a37",
            width=100,
            command=self._overwrite
        )
        self.btn_overwrite.pack(side="left", padx=5, expand=True)

        self.btn_skip = ctk.CTkButton(
            btn_frame, 
            text="Skip", 
            fg_color="#e9c46a", # Yellow-ish? Or maybe just secondary color.
            text_color="black",
            hover_color="#d4b055",
            width=100,
            command=self._skip
        )
        self.btn_skip.pack(side="left", padx=5, expand=True)

        self.btn_cancel = ctk.CTkButton(
            btn_frame, 
            text="Cancel", 
            fg_color="transparent", 
            border_width=1, 
            text_color=("gray10", "gray90"),
            width=80,
            command=self._cancel
        )
        self.btn_cancel.pack(side="left", padx=5, expand=True)
        
        # Handle X button
        self.protocol("WM_DELETE_WINDOW", self._cancel)

    def _overwrite(self):
        self.destroy()
        if self.on_overwrite:
            self.on_overwrite()

    def _skip(self):
        self.destroy()
        if self.on_skip:
            self.on_skip()

    def _cancel(self):
        self.destroy()
        if self.on_cancel:
            self.on_cancel()
