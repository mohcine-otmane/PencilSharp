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

class PencilSharpGUI:
    def __init__(self):
        # Initialize PyQt6 application
        self.qt_app = QApplication(sys.argv)
        
        # Initialize main window
        self.window = ctk.CTk()
        self.window.title("PencilSharp Learning")
        self.window.geometry("1400x800")  # Increased width
        
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize transition manager
        self.transition_manager = TransitionManager(self.window)
        
        # Initialize state
        self.current_page = None
        self.current_subject = None
        self.current_unit = None
        self.current_topic = None
        
        # Create main container
        self.main_container = ctk.CTkFrame(self.window)
        self.main_container.pack(fill="both", expand=True)
        
        # Configure main container grid
        self.main_container.grid_columnconfigure(0, weight=1)  # Content area expands
        self.main_container.grid_rowconfigure(1, weight=1)  # Content area expands vertically
        
        # Create header
        self.header = HeaderBar(self.main_container, xp=1000, points=500, streak=5)
        
        # Create content area
        self.content_area = ctk.CTkFrame(self.main_container)
        self.content_area.grid(row=1, column=0, sticky="nsew")
        
        # Create sidebar
        self.sidebar = SidebarWidget(
            self.main_container,
            league_data={"league": "Diamond", "rank": 42, "xp": 2500},
            progress_data={"progress": 3, "goal": 5}
        )
        self.sidebar.grid(row=1, column=1, sticky="nsew", padx=(0, 20), pady=20)
        
        # Show initial page
        self.show_subjects_page()
        
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

    def show_subjects_page(self):
        """Show the subject selection screen with transition"""
        def create_content():
            self.clear_main_frame()

            # Create centered container for content
            content_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            content_container.place(relx=0.5, rely=0.5, anchor="center")
            
            # Subject selection header
            header_label = ctk.CTkLabel(
                content_container,
                text="Choose Your Subject",
                font=("Helvetica", 36, "bold")  # Increased font size
            )
            header_label.pack(pady=(0, 40))  # Increased padding below header

            # Create grid frame for subject cards
            grid_frame = ctk.CTkFrame(content_container, fg_color="transparent")
            grid_frame.pack(fill="both", expand=True)

            # Configure grid for equal spacing
            for i in range(3):
                grid_frame.grid_columnconfigure(i, weight=1, uniform="column")
            grid_frame.grid_rowconfigure(0, weight=1)

            # Create subject cards
            for i, (subject, data) in enumerate(SUBJECTS.items()):
                card = SubjectCard(
                    grid_frame,
                    subject=subject,
                    data=data,
                    command=lambda s=subject: self.show_subject_content(s)
                )
                card.grid(row=0, column=i, padx=30, pady=20, sticky="nsew")  # Increased padding
            
            # Start fade-in transition
            self.transition_manager.fade_in()

        # Start fade-out transition
        self.transition_manager.fade_out(callback=create_content)

    def show_subject_content(self, subject):
        """Show the content for a specific subject with transition"""
        def create_content():
            self.clear_main_frame()
            self.current_subject = subject
            subject_data = SUBJECTS[subject]

            # Navigation bar
            nav = NavigationBar(
                self.main_frame,
                back_text="Back to Subjects",
                back_command=self.show_subjects_page,
                title_text=f"{subject_data['icon']} {subject}",
                title_color=subject_data["color"]
            )

            # Create main content container
            content_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            content_container.pack(fill="both", expand=True, padx=30, pady=20)
            
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
            main_content = ctk.CTkFrame(content_container)
            main_content.pack(side="left", fill="both", expand=True)

            # Create scrollable frame for units with touch support
            scroll_frame = TouchScrollableFrame(main_content, fg_color="transparent")
            scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

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
            self.clear_main_frame()
            self.current_topic = topic

            # Navigation bar
            nav = NavigationBar(
                self.main_frame,
                back_text=f"Back to {self.current_subject}",
                back_command=lambda: self.show_subject_content(self.current_subject),
                title_text=f"Learning: {topic}"
            )
            nav.pack(fill="x", padx=5, pady=5)

            # Create scrollable lesson content with touch support
            content_scroll = TouchScrollableFrame(self.main_frame)
            content_scroll.pack(fill="both", expand=True, padx=5, pady=5)

            # Create lesson content
            lesson = LessonContent(content_scroll, topic=topic)
            lesson.pack(fill="both", expand=True)
            
            # Start fade-in transition
            self.transition_manager.fade_in()

        # Start fade-out transition
        self.transition_manager.fade_out(callback=create_content)

if __name__ == "__main__":
    app = PencilSharpGUI()
    app.run() 