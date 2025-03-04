import customtkinter as ctk
from PIL import Image
import os

class TransitionManager:
    def __init__(self, master):
        self.master = master
        self.overlay = None
        self.callback = None
        self.fade_step = 0.1
        self.fade_delay = 10  # milliseconds
    
    def fade_out(self, callback=None):
        """Start fade out transition"""
        self.callback = callback
        
        # Create overlay
        self.overlay = ctk.CTkFrame(
            self.master,
            fg_color="#000000",
            bg_color="#000000"
        )
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Start with transparent overlay
        self.overlay.configure(fg_color=f"#000000")
        self.overlay._fg_color = (0, 0, 0, 0)
        
        # Start fade out animation
        self._fade_out_step(0)
    
    def fade_in(self):
        """Start fade in transition"""
        if self.overlay:
            # Start fade in animation
            self._fade_in_step(1)
    
    def _fade_out_step(self, alpha):
        """Perform one step of fade out animation"""
        if alpha < 1:
            # Update overlay opacity
            self.overlay._fg_color = (0, 0, 0, alpha)
            self.overlay.configure(fg_color=f"#000000")
            
            # Schedule next step
            self.master.after(
                self.fade_delay,
                lambda: self._fade_out_step(alpha + self.fade_step)
            )
        else:
            # Fade out complete, call callback
            if self.callback:
                self.callback()
    
    def _fade_in_step(self, alpha):
        """Perform one step of fade in animation"""
        if alpha > 0:
            # Update overlay opacity
            self.overlay._fg_color = (0, 0, 0, alpha)
            self.overlay.configure(fg_color=f"#000000")
            
            # Schedule next step
            self.master.after(
                self.fade_delay,
                lambda: self._fade_in_step(alpha - self.fade_step)
            )
        else:
            # Fade in complete, remove overlay
            self.overlay.destroy()
            self.overlay = None

class TouchScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Enable mouse wheel scrolling
        self.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        self._parent_canvas.yview_scroll(-1 * int(event.delta/120), "units")

class SubjectCard(ctk.CTkFrame):
    def __init__(self, master, subject, data, command=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Store data
        self.subject = subject
        self.data = data
        self.command = command
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Create content frame
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.content.grid_columnconfigure(0, weight=1)
        
        # Subject name
        self.title = ctk.CTkLabel(
            self.content,
            text=subject,
            font=("Helvetica", 24, "bold"),
            anchor="w"
        )
        self.title.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Units count
        self.units = ctk.CTkLabel(
            self.content,
            text=f"{data['units']} Units",
            font=("Helvetica", 16),
            text_color="gray75",
            anchor="w"
        )
        self.units.grid(row=1, column=0, sticky="w", pady=(0, 15))
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(
            self.content,
            height=8,
            corner_radius=4
        )
        self.progress.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.progress.set(data['progress'] / 100)
        
        # Progress text
        self.progress_text = ctk.CTkLabel(
            self.content,
            text=f"{data['progress']}% Complete",
            font=("Helvetica", 14),
            text_color="gray75",
            anchor="w"
        )
        self.progress_text.grid(row=3, column=0, sticky="w", pady=(0, 15))
        
        # Continue button
        self.button = ctk.CTkButton(
            self.content,
            text="Continue Learning",
            font=("Helvetica", 16),
            height=45,
            command=self._handle_click
        )
        self.button.grid(row=4, column=0, sticky="ew")
        
        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _handle_click(self):
        if self.command:
            self.command()
    
    def _on_enter(self, event):
        self.configure(fg_color=("gray85", "gray25"))
    
    def _on_leave(self, event):
        self.configure(fg_color=("gray80", "gray20"))

class NavigationBar(ctk.CTkFrame):
    def __init__(self, master, username, on_logout, **kwargs):
        super().__init__(master, height=60, **kwargs)
        self.pack_propagate(False)
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        
        # Logo
        self.logo_label = ctk.CTkLabel(
            self,
            text="✏️ PencilSharp",
            font=("Helvetica", 20, "bold"),
            text_color="#4B91F1"
        )
        self.logo_label.grid(row=0, column=0, padx=(20, 40), pady=10)
        
        # Spacer
        self.grid_columnconfigure(1, weight=1)
        
        # User profile frame
        self.profile_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.profile_frame.grid(row=0, column=2, padx=20, pady=10)
        
        # Try to load avatar image
        avatar_path = os.path.join("src", "assets", "default_avatar.png")
        try:
            avatar_image = Image.open(avatar_path)
            avatar_photo = ctk.CTkImage(avatar_image, size=(40, 40))
        except:
            # If image loading fails, show initials instead
            self.avatar_label = ctk.CTkLabel(
                self.profile_frame,
                text=username[0].upper(),
                font=("Helvetica", 16, "bold"),
                width=40,
                height=40,
                fg_color="#4B91F1",
                corner_radius=20
            )
        else:
            self.avatar_label = ctk.CTkLabel(
                self.profile_frame,
                text="",
                image=avatar_photo
            )
        self.avatar_label.pack(side="left", padx=(0, 10))
        
        # Username label
        self.username_label = ctk.CTkLabel(
            self.profile_frame,
            text=username,
            font=("Helvetica", 14)
        )
        self.username_label.pack(side="left", padx=(0, 15))
        
        # Logout button
        self.logout_button = ctk.CTkButton(
            self.profile_frame,
            text="Logout",
            font=("Helvetica", 12),
            width=80,
            height=30,
            command=on_logout
        )
        self.logout_button.pack(side="left") 