import customtkinter as ctk
from subjects_data import SUBJECTS
from widgets import (
    HeaderBar,
    SubjectCard,
    NavigationBar,
    UnitSection,
    SidebarWidget,
    LessonContent,
    TransitionManager,
    TouchScrollableFrame
)
from PyQt6.QtWidgets import QApplication
import sys
from src.views.learning_view import LearningView
from src.utils.theme import theme

class PencilSharpGUI:
    def __init__(self):
        # Initialize PyQt6 application
        self.qt_app = QApplication(sys.argv)
        
        # Initialize main window
        self.window = ctk.CTk()
        self.window.title("PencilSharp Learning")
        self.window.geometry("1400x800")
        
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main container with dark theme
        self.main_container = ctk.CTkFrame(self.window, fg_color="#1a1b1e")
        self.main_container.pack(fill="both", expand=True)
        
        # Create left sidebar
        self.sidebar = ctk.CTkFrame(self.main_container, fg_color="#15161a", width=250)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        
        # Add logo/brand at top of sidebar
        brand = ctk.CTkLabel(
            self.sidebar,
            text="✏️ PencilSharp",
            font=("Helvetica", 24, "bold"),
            text_color="#ffffff"
        )
        brand.pack(pady=(30, 40), padx=20)
        
        # Add navigation menu
        self._create_nav_menu()
        
        # Create main content area
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="#1a1b1e")
        self.content_area.pack(side="left", fill="both", expand=True)
        
        # Initialize transition manager
        self.transition_manager = TransitionManager(self.window)
        
        # Initialize state
        self.current_page = None
        self.current_subject = None
        self.current_unit = None
        self.current_topic = None
        
        # Show initial page
        self.show_subjects_page()
        
    def _create_nav_menu(self):
        """Create navigation menu in sidebar"""
        menu_items = [
            ("📚 Library", self.show_subjects_page),
            ("🎯 Progress", None),
            ("⭐ Favorites", None),
            ("🔍 Browse", None),
        ]
        
        for text, command in menu_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                font=("Helvetica", 16),
                fg_color="transparent",
                text_color="#ffffff",
                hover_color="#2a2b30",
                anchor="w",
                height=45,
                command=command
            )
            btn.pack(fill="x", padx=10, pady=2)
    
    def show_subjects_page(self):
        """Show the subject selection screen with transition"""
        def create_content():
            # Clear ALL previous content first
            for widget in self.content_area.winfo_children():
                widget.destroy()
            
            # Create header section
            header = ctk.CTkFrame(self.content_area, fg_color="transparent")
            header.pack(fill="x", padx=40, pady=(40, 30))
            
            # Page title
            title = ctk.CTkLabel(
                header,
                text="Featured Subjects",
                font=("Helvetica", 32, "bold"),
                text_color="#ffffff"
            )
            title.pack(side="left")
            
            # Create scrollable content area
            content_scroll = TouchScrollableFrame(
                self.content_area,
                fg_color="transparent"
            )
            content_scroll.pack(fill="both", expand=True, padx=40)
            
            # Create grid for subject cards
            grid = ctk.CTkFrame(content_scroll, fg_color="transparent")
            grid.pack(fill="both", expand=True)
            
            # Configure grid columns
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
            
            # Start fade-in transition
            self.transition_manager.fade_in()
        
        # Start fade-out transition
        self.transition_manager.fade_out(callback=create_content)

    def run(self):
        self.window.mainloop()
        # Clean up PyQt6 application
        self.qt_app.quit()

    def clear_main_frame(self):
        """Clear the main frame for new content"""
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()
        self.main_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def show_subject_content(self, subject):
        """Show the content for a specific subject with transition"""
        def create_content():
            # Clear ALL previous content first
            for widget in self.content_area.winfo_children():
                widget.destroy()
            
            self.current_subject = subject
            subject_data = SUBJECTS[subject]

            # Navigation bar
            nav_container = ctk.CTkFrame(self.content_area, fg_color="transparent")
            nav_container.pack(fill="x", padx=40, pady=(40, 30))
            
            # Back button and title in navigation
            back_btn = ctk.CTkButton(
                nav_container,
                text="← Back to Subjects",
                command=self.show_subjects_page,
                fg_color="transparent",
                text_color="#ffffff",
                hover_color="#2a2b30",
                anchor="w",
                width=150
            )
            back_btn.pack(side="left")
            
            # Subject title
            title = ctk.CTkLabel(
                nav_container,
                text=f"{subject_data['icon']} {subject}",
                font=("Helvetica", 32, "bold"),
                text_color=subject_data["color"]
            )
            title.pack(side="left", padx=20)

            # Create main content container
            content_container = ctk.CTkFrame(self.content_area, fg_color="transparent")
            content_container.pack(fill="both", expand=True, padx=40, pady=20)
            
            # Create left sidebar for unit navigation
            unit_nav = ctk.CTkFrame(content_container, fg_color="#1e1e1e", width=250)
            unit_nav.pack(side="left", fill="y", padx=(0, 20))
            unit_nav.pack_propagate(False)  # Prevent frame from shrinking
            
            # Unit navigation header
            unit_nav_header = ctk.CTkLabel(
                unit_nav,
                text="Units",
                font=("Helvetica", 24, "bold"),
                text_color=subject_data["color"]
            )
            unit_nav_header.pack(pady=(20, 10), padx=15)
            
            # Create scrollable frame for unit buttons with touch support
            unit_scroll = TouchScrollableFrame(unit_nav, fg_color="transparent")
            unit_scroll.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create unit buttons
            for i, unit in enumerate(subject_data["units"]):
                unit_button = ctk.CTkButton(
                    unit_scroll,
                    text=f"Unit {i + 1}: {unit['name']}",
                    font=("Helvetica", 14),
                    fg_color="#2d2d2d",
                    hover_color="#3d3d3d",
                    anchor="w",
                    height=40,
                    corner_radius=8
                )
                unit_button.pack(fill="x", pady=5)

            # Create main content area
            main_content = ctk.CTkFrame(content_container, fg_color="#1e1e1e")
            main_content.pack(side="left", fill="both", expand=True)

            # Create scrollable frame for units with touch support
            scroll_frame = TouchScrollableFrame(main_content, fg_color="transparent")
            scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Create units
            for i, unit in enumerate(subject_data["units"]):
                UnitSection(
                    scroll_frame,
                    unit=unit,
                    index=i,
                    color=subject_data["color"],
                    topic_callback=self.start_lesson
                )
            
            # Start fade-in transition
            self.transition_manager.fade_in()

        # Start fade-out transition
        self.transition_manager.fade_out(callback=create_content)

    def start_lesson(self, topic):
        """Show lesson content in the main frame with transition"""
        def create_content():
            # Clear ALL previous content first
            for widget in self.content_area.winfo_children():
                widget.destroy()
            
            self.current_topic = topic

            # Navigation bar
            nav_container = ctk.CTkFrame(self.content_area, fg_color="transparent")
            nav_container.pack(fill="x", padx=40, pady=(40, 30))
            
            # Back button and title in navigation
            back_btn = ctk.CTkButton(
                nav_container,
                text=f"← Back to {self.current_subject}",
                command=lambda: self.show_subject_content(self.current_subject),
                fg_color="transparent",
                text_color="#ffffff",
                hover_color="#2a2b30",
                anchor="w",
                width=200
            )
            back_btn.pack(side="left")
            
            # Lesson title
            title = ctk.CTkLabel(
                nav_container,
                text=f"Learning: {topic}",
                font=("Helvetica", 32, "bold"),
                text_color="#ffffff"
            )
            title.pack(side="left", padx=20)

            # Create main content container
            content_container = ctk.CTkFrame(self.content_area, fg_color="#1e1e1e")
            content_container.pack(fill="both", expand=True, padx=40, pady=20)
            
            # Create tabs for different learning modes
            tabs = ctk.CTkFrame(content_container, fg_color="transparent")
            tabs.pack(fill="x", padx=20, pady=(20, 0))
            
            tab_items = [
                ("Learn", True),
                ("Practice", False),
                ("Quiz", False)
            ]
            
            for text, is_active in tab_items:
                tab = ctk.CTkButton(
                    tabs,
                    text=text,
                    fg_color="#2d2d2d" if is_active else "transparent",
                    hover_color="#3d3d3d",
                    text_color="#ffffff",
                    height=35,
                    corner_radius=8,
                    width=100
                )
                tab.pack(side="left", padx=(0, 10))
            
            # Create content area for lesson
            lesson_content = ctk.CTkFrame(content_container, fg_color="transparent")
            lesson_content.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Create LaTeX viewer
            latex_viewer = LearningView(lesson_content)
            latex_viewer.pack(expand=True, fill="both")
            
            # Start fade-in transition
            self.transition_manager.fade_in()

        # Start fade-out transition
        self.transition_manager.fade_out(callback=create_content)

if __name__ == "__main__":
    app = PencilSharpGUI()
    app.run() 