import customtkinter as ctk
from src.widgets import SubjectCard, TouchScrollableFrame, NavigationBar
from src.views.login_view import LoginView
from src.views.signup_view import SignupView
from src.views.main_view import MainView

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("PencilSharp Learning")
        self.geometry("1200x800")
        
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create container for views
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        
        # Store current username
        self.current_user = None
        
        # Show login view
        self.show_login()
    
    def show_login(self):
        # Clear container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Reset current user
        self.current_user = None
        
        # Show login view
        login_view = LoginView(
            self.container,
            on_login=self.handle_login,
            on_signup=self.show_signup
        )
        login_view.pack(fill="both", expand=True)
    
    def show_signup(self):
        # Clear container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Show signup view
        signup_view = SignupView(
            self.container,
            on_signup=self.handle_signup,
            on_login=self.show_login
        )
        signup_view.pack(fill="both", expand=True)
    
    def handle_login(self, username):
        # Store username and show main view
        self.current_user = username
        self.show_main()
    
    def handle_signup(self, username):
        # Store username and show main view
        self.current_user = username
        self.show_main()
    
    def show_main(self):
        # Clear container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Show main view with username and logout handler
        main_view = MainView(
            self.container,
            username=self.current_user,
            on_logout=self.show_login
        )
        main_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop() 