import customtkinter as ctk
from src.utils.database import Database

class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login=None, on_signup=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Store callbacks
        self.on_login = on_login
        self.on_signup = on_signup
        
        # Initialize database
        self.db = Database()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create center frame
        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.grid(row=0, column=0)
        
        # Logo/Title
        title = ctk.CTkLabel(
            center_frame,
            text="✏️ PencilSharp",
            font=("Helvetica", 32, "bold"),
            text_color="#4B91F1"
        )
        title.pack(pady=(0, 30))
        
        # Login frame
        login_frame = ctk.CTkFrame(center_frame)
        login_frame.pack(padx=40, pady=40)
        
        # Error message
        self.error_label = ctk.CTkLabel(
            login_frame,
            text="",
            font=("Helvetica", 12),
            text_color="#FF4444"
        )
        self.error_label.pack(padx=20, pady=(20, 0))
        
        # Username
        username_label = ctk.CTkLabel(
            login_frame,
            text="Username",
            font=("Helvetica", 14)
        )
        username_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        self.username_entry = ctk.CTkEntry(
            login_frame,
            width=300,
            height=40,
            placeholder_text="Enter your username"
        )
        self.username_entry.pack(padx=20, pady=(0, 15))
        
        # Password
        password_label = ctk.CTkLabel(
            login_frame,
            text="Password",
            font=("Helvetica", 14)
        )
        password_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            login_frame,
            width=300,
            height=40,
            placeholder_text="Enter your password",
            show="•"
        )
        self.password_entry.pack(padx=20, pady=(0, 30))
        
        # Login button
        login_button = ctk.CTkButton(
            login_frame,
            text="Login",
            font=("Helvetica", 15, "bold"),
            width=300,
            height=45,
            command=self._handle_login
        )
        login_button.pack(padx=20, pady=(0, 20))
        
        # Signup link
        signup_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        signup_frame.pack(pady=(0, 20))
        
        signup_label = ctk.CTkLabel(
            signup_frame,
            text="Don't have an account?",
            font=("Helvetica", 12),
            text_color="gray70"
        )
        signup_label.pack(side="left")
        
        signup_button = ctk.CTkButton(
            signup_frame,
            text="Sign up",
            font=("Helvetica", 12),
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            command=self._handle_signup
        )
        signup_button.pack(side="left", padx=(5, 0))
    
    def _handle_login(self):
        if self.on_login:
            username = self.username_entry.get().strip()
            password = self.password_entry.get()
            
            # Basic validation
            if not username:
                self.error_label.configure(text="Please enter a username")
                return
            
            if not password:
                self.error_label.configure(text="Please enter a password")
                return
            
            # For now, accept any non-empty username/password
            # TODO: Add proper authentication
            self.on_login(username)
    
    def _handle_signup(self):
        if self.on_signup:
            self.on_signup() 