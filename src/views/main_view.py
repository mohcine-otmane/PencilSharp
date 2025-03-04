import customtkinter as ctk
from src.widgets import NavigationBar, TouchScrollableFrame, SubjectCard, TransitionManager
from src.utils.subjects_data import SUBJECTS
from src.views.learning_view import LearningView

class MainView(ctk.CTkFrame):
    def __init__(self, master, username="User", on_logout=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Row 1 should expand
        
        # Create navigation bar
        self.nav_bar = NavigationBar(
            self,
            username=username,
            on_logout=on_logout,
            fg_color=("gray85", "gray20")
        )
        self.nav_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        
        # Create scrollable content frame
        self.content = TouchScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # Create subject cards grid
        self.subjects_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.subjects_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid columns for subject cards
        self.subjects_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="column")
        
        # Add subject cards
        for i, (subject, data) in enumerate(SUBJECTS.items()):
            row = i // 3
            col = i % 3
            
            # Skip Computer Science as it has a different data structure
            if subject == "Computer Science":
                continue
                
            card = SubjectCard(
                self.subjects_frame,
                subject=subject,
                data=data,
                command=lambda s=subject: self.show_subject_content(s),
                fg_color=("gray80", "gray20"),
                width=350,
                height=200
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Show subjects page
        self.show_subjects_page()
    
    def show_subjects_page(self):
        # Clear previous content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Create header section
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(40, 30))
        
        # Page title and greeting
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        
        title = ctk.CTkLabel(
            title_frame,
            text="Featured Subjects",
            font=("Helvetica", 32, "bold"),
            text_color="#ffffff"
        )
        title.pack(anchor="w")
        
        greeting = ctk.CTkLabel(
            title_frame,
            text="Welcome back! Ready to learn?",
            font=("Helvetica", 16),
            text_color="#8a8d93"
        )
        greeting.pack(anchor="w")
        
        # Create scrollable container for the grid
        scroll_container = TouchScrollableFrame(
            self.content,
            fg_color="transparent",
            height=600
        )
        scroll_container.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Create grid for subject cards
        grid = ctk.CTkFrame(scroll_container, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        
        # Configure grid columns with equal weight
        grid.grid_columnconfigure((0, 1, 2), weight=1, uniform="column")
        
        # Create subject cards
        for i, (subject, data) in enumerate(SUBJECTS.items()):
            row = i // 3
            col = i % 3
            
            card = SubjectCard(
                grid,
                subject=subject,
                data=data,
                command=lambda s=subject: self.show_subject_content(s)
            )
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
    
    def show_subject_content(self, subject):
        def create_content():
            # Clear previous content
            for widget in self.content.winfo_children():
                widget.destroy()
            
            subject_data = SUBJECTS[subject]
            
            # Create two-column layout
            content_container = ctk.CTkFrame(self.content, fg_color="transparent")
            content_container.pack(fill="both", expand=True, padx=40, pady=20)
            content_container.grid_columnconfigure(1, weight=1)
            
            # Left sidebar for units
            unit_sidebar = ctk.CTkFrame(content_container, fg_color="#1e2124", width=300)
            unit_sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
            unit_sidebar.grid_propagate(False)
            
            # Back button
            back_btn = ctk.CTkButton(
                unit_sidebar,
                text="← Back",
                command=self.show_subjects_page,
                fg_color="transparent",
                text_color="#ffffff",
                hover_color="#2a2b30",
                anchor="w"
            )
            back_btn.pack(fill="x", padx=20, pady=(20, 10))
            
            # Subject title
            title = ctk.CTkLabel(
                unit_sidebar,
                text=subject,
                font=("Helvetica", 24, "bold"),
                text_color="#ffffff"
            )
            title.pack(padx=20, pady=10)
            
            # Units list
            units_frame = TouchScrollableFrame(unit_sidebar, fg_color="transparent")
            units_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            for i, unit in enumerate(subject_data["units"]):
                unit_btn = ctk.CTkButton(
                    units_frame,
                    text=f"Unit {i+1}: {unit['name']}",
                    font=("Helvetica", 14),
                    fg_color="#2a2b30",
                    text_color="#ffffff",
                    hover_color="#3d3d3d",
                    height=40,
                    anchor="w"
                )
                unit_btn.pack(fill="x", pady=5)
            
            # Main content area
            main_content = ctk.CTkFrame(content_container, fg_color="#1e2124")
            main_content.grid(row=0, column=1, sticky="nsew")
            
            # Create learning view
            learning_view = LearningView(main_content)
            learning_view.pack(fill="both", expand=True, padx=20, pady=20)
            
            self.transition_manager.fade_in()
        
        self.transition_manager.fade_out(callback=create_content) 