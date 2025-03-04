import customtkinter as ctk
import re
from src.utils.database import Database

class SignupView(ctk.CTkFrame):
    def __init__(self, master, on_signup=None, on_login=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Store callbacks
        self.on_signup = on_signup
        self.on_login = on_login
        
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
        
        # Signup frame
        signup_frame = ctk.CTkFrame(center_frame)
        signup_frame.pack(padx=40, pady=40)
        
        # Username
        username_label = ctk.CTkLabel(
            signup_frame,
            text="Username",
            font=("Helvetica", 14)
        )
        username_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        self.username_entry = ctk.CTkEntry(
            signup_frame,
            width=300,
            height=40,
            placeholder_text="Choose a username"
        )
        self.username_entry.pack(padx=20, pady=(0, 15))
        
        # Password
        password_label = ctk.CTkLabel(
            signup_frame,
            text="Password",
            font=("Helvetica", 14)
        )
        password_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            signup_frame,
            width=300,
            height=40,
            placeholder_text="Choose a password",
            show="•"
        )
        self.password_entry.pack(padx=20, pady=(0, 15))
        
        # Confirm Password
        confirm_label = ctk.CTkLabel(
            signup_frame,
            text="Confirm Password",
            font=("Helvetica", 14)
        )
        confirm_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.confirm_entry = ctk.CTkEntry(
            signup_frame,
            width=300,
            height=40,
            placeholder_text="Confirm your password",
            show="•"
        )
        self.confirm_entry.pack(padx=20, pady=(0, 30))
        
        # Signup button
        signup_button = ctk.CTkButton(
            signup_frame,
            text="Sign Up",
            font=("Helvetica", 15, "bold"),
            width=300,
            height=45,
            command=self._handle_signup
        )
        signup_button.pack(padx=20, pady=(0, 20))
        
        # Login link
        login_frame = ctk.CTkFrame(signup_frame, fg_color="transparent")
        login_frame.pack(pady=(0, 20))
        
        login_label = ctk.CTkLabel(
            login_frame,
            text="Already have an account?",
            font=("Helvetica", 12),
            text_color="gray70"
        )
        login_label.pack(side="left")
        
        login_button = ctk.CTkButton(
            login_frame,
            text="Login",
            font=("Helvetica", 12),
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            command=self._handle_login
        )
        login_button.pack(side="left", padx=(5, 0))
    
    def _handle_signup(self):
        if self.on_signup:
            username = self.username_entry.get()
            password = self.password_entry.get()
            confirm = self.confirm_entry.get()
            
            # Basic validation
            if username and password and password == confirm:
                self.on_signup(username)
    
    def _handle_login(self):
        if self.on_login:
            self.on_login()

    def _validate_form(self) -> tuple[bool, str]:
        """Validate form inputs"""
        name = self.username_entry.get().strip()
        email = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_entry.get()
        
        # Check if all fields are filled
        if not all([name, email, password, confirm_password]):
            return False, "All fields are required"
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        # Check if email already exists
        db = Database()
        if db.user_exists(email):
            return False, "Email already exists"
        
        # Validate password length
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        # Check if passwords match
        if password != confirm_password:
            return False, "Passwords do not match"
        
        return True, ""
    
    def _handle_signup(self):
        """Handle signup button click"""
        # Clear previous error
        self.error_label.configure(text="")
        
        # Validate form
        valid, error = self._validate_form()
        if not valid:
            self.error_label.configure(text=error)
            return
        
        # Create user
        success, message = self.db.create_user(
            email=self.username_entry.get().strip(),
            password=self.password_entry.get(),
            name=self.username_entry.get().strip()
        )
        
        if success:
            if self.on_signup:
                self.on_signup(self.username_entry.get())
        else:
            self.error_label.configure(text=message) 