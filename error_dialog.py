import customtkinter as ctk

class ErrorDialog(ctk.CTkToplevel):
    def __init__(self, parent, title: str, description: str, raw_error: str = None):
        super().__init__(parent)
        
        self.title(title or "Error")
        self.geometry("480x280")
        self.resizable(False, False)
        
        # Center the dialog on the parent window if possible
        self.transient(parent)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Expands if details are shown
        
        # --- Icon/Title Header ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        # Simple error symbol (Optional: use an image if available, but text is safer/portable)
        icon_label = ctk.CTkLabel(
            header_frame, 
            text="⚠️", 
            font=ctk.CTkFont(size=32),
            text_color="#ff5555" # Red-ish
        )
        icon_label.pack(side="left", padx=(0, 15))
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text=title, 
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        title_label.pack(side="left", fill="x", expand=True)

        # --- Message Body ---
        message_label = ctk.CTkLabel(
            self, 
            text=description, 
            font=ctk.CTkFont(size=14),
            wraplength=440,
            justify="left",
            anchor="w"
        )
        message_label.grid(row=1, column=0, padx=25, pady=(0, 20), sticky="w")
        
        # --- Details Section (initially hidden if raw_error provided) ---
        self.raw_error = raw_error
        self.details_frame = None
        
        # Button Row
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=20)
        
        # OK Button (Right)
        ok_btn = ctk.CTkButton(
            button_frame, 
            text="OK", 
            width=100, 
            command=self.destroy
        )
        ok_btn.pack(side="right")
        
        # Details Button (Left) - Only if raw_error exists
        if raw_error:
            self.details_btn = ctk.CTkButton(
                button_frame,
                text="Show Details ▼",
                width=120,
                fg_color="transparent",
                border_width=1,
                text_color=("gray10", "gray90"), # Adapted for light/dark
                command=self.toggle_details
            )
            self.details_btn.pack(side="left")

    def toggle_details(self):
        if self.details_frame is None:
            # Create and show details
            self.geometry("480x450") # Expand window
            
            self.details_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.details_frame.grid(row=2, column=0, padx=20, pady=(0, 5), sticky="nsew")
            
            textbox = ctk.CTkTextbox(self.details_frame, height=120, corner_radius=8)
            textbox.pack(fill="both", expand=True)
            textbox.insert("0.0", self.raw_error)
            textbox.configure(state="disabled") # Read-only
            
            self.details_btn.configure(text="Hide Details ▲")
        else:
            # Hide details
            self.details_frame.destroy()
            self.details_frame = None
            self.geometry("480x280") # Shrink window
            self.details_btn.configure(text="Show Details ▼")
