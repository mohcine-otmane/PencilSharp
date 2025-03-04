import customtkinter as ctk
from typing import Dict, Any
from src.utils.observer import Observer
from src.controllers.app_controller import AppController
from src.views.widgets import (
    HeaderBar,
    SubjectCard,
    NavigationBar,
    UnitSection,
    SidebarWidget,
    LessonContent,
    TransitionManager,
    TouchScrollableFrame
)

class MainWindow(ctk.CTk, Observer):
    def __init__(self, controller: AppController):
        super().__init__()
        
        # Set up window
        self.title("PencilSharp Learning")
        self.geometry("1400x800")
        
        # Store controller reference
        self.controller = controller
        self.controller.add_observer(self)
        
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize transition manager
        self.transition_manager = TransitionManager(self)
        
        # Create main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)
        
        # Configure main container grid
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        
        # Create header
        self.header = HeaderBar(
            self.main_container,
            xp=self.controller.user_progress.xp,
            points=self.controller.user_progress.points,
            streak=self.controller.user_progress.streak
        )
        
        # Create content area
        self.content_area = ctk.CTkFrame(self.main_container)
        self.content_area.grid(row=1, column=0, sticky="nsew")
        
        # Create sidebar
        self.sidebar = SidebarWidget(
            self.main_container,
            league_data={
                "league": "Diamond",
                "rank": 42,
                "xp": self.controller.user_progress.xp
            },
            progress_data={
                "progress": self.controller.user_progress.lessons_completed_today,
                "goal": self.controller.user_progress.daily_goal
            }
        )
        self.sidebar.grid(row=1, column=1, sticky="nsew", padx=(0, 20), pady=20)
        
        # Show initial subjects page
        self.show_subjects_page()

    def update(self, event_type: str, data: Any):
        """Handle updates from the controller"""
        handlers = {
            "subject_changed": self.handle_subject_changed,
            "unit_changed": self.handle_unit_changed,
            "topic_changed": self.handle_topic_changed,
            "progress_updated": self.handle_progress_updated
        }
        
        if event_type in handlers:
            handlers[event_type](data)

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

            # Create main container with padding
            main_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            main_container.pack(fill="both", expand=True)
            
            # Subject selection header
            header_label = ctk.CTkLabel(
                main_container,
                text="Choose Your Subject",
                font=("Helvetica", 36, "bold")
            )
            header_label.pack(pady=(0, 20))  # Reduced padding

            # Create scrollable frame for the grid
            scroll_container = TouchScrollableFrame(
                main_container,
                fg_color="transparent"
            )
            scroll_container.pack(fill="both", expand=True)

            # Create grid frame for subject cards
            grid_frame = ctk.CTkFrame(scroll_container, fg_color="transparent")
            grid_frame.pack(fill="both", expand=True, padx=10)  # Reduced padding

            # Calculate number of columns based on window width
            window_width = self.winfo_width()
            card_width = 280  # Match the new card width
            spacing = 20     # Reduced spacing between cards
            num_columns = max(2, min(4, (window_width - 100) // (card_width + spacing)))

            # Configure grid columns
            for i in range(num_columns):
                grid_frame.grid_columnconfigure(i, weight=1, uniform="column")

            # Create subject cards in a grid
            for i, (subject_name, subject) in enumerate(self.controller.subjects.items()):
                row = i // num_columns
                col = i % num_columns
                
                card = SubjectCard(
                    grid_frame,
                    subject=subject_name,
                    data={
                        "icon": subject.icon,
                        "color": subject.color,
                        "units": subject.units,
                        "progress": subject.progress
                    },
                    command=lambda s=subject_name: self.controller.select_subject(s)
                )
                card.grid(
                    row=row,
                    column=col,
                    padx=spacing//2,
                    pady=spacing//2,
                    sticky="nsew"
                )
                
                # Configure row weight for equal spacing
                grid_frame.grid_rowconfigure(row, weight=1, pad=spacing//2)
            
            # Add bottom padding for last row
            grid_frame.grid_rowconfigure(row + 1, weight=1, pad=spacing//2)
            
            # Bind window resize event to update layout
            def on_resize(event):
                # Recalculate number of columns
                new_width = event.width
                new_num_columns = max(2, min(4, (new_width - 100) // (card_width + spacing)))
                
                # Only update if number of columns changed
                if new_num_columns != num_columns:
                    self.after(100, self.show_subjects_page)  # Debounced refresh
            
            self.bind("<Configure>", on_resize)
            
            # Start fade-in transition
            self.transition_manager.fade_in()

        # Start fade-out transition
        self.transition_manager.fade_out(callback=create_content)

    def handle_subject_changed(self, subject_name: str):
        """Handle subject selection"""
        subject = self.controller.get_current_subject()
        if subject:
            def create_content():
                self.clear_main_frame()

                # Navigation bar
                nav = NavigationBar(
                    self.main_frame,
                    back_text="Back to Subjects",
                    back_command=self.show_subjects_page,
                    title_text=f"{subject.icon} {subject.name}",
                    title_color=subject.color
                )

                # Create main content container
                content_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
                content_container.pack(fill="both", expand=True, padx=30, pady=20)
                
                # Create left sidebar for unit navigation
                unit_nav = self.create_unit_navigation(content_container, subject)
                
                # Create main content area
                main_content = ctk.CTkFrame(content_container)
                main_content.pack(side="left", fill="both", expand=True)

                # Create scrollable frame for units
                scroll_frame = TouchScrollableFrame(main_content, fg_color="transparent")
                scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

                # Create units
                for i, unit in enumerate(subject.units):
                    UnitSection(
                        scroll_frame,
                        unit={"name": unit.name, "topics": [t.name for t in unit.topics]},
                        index=i,
                        color=subject.color,
                        topic_callback=self.controller.select_topic
                    )
                
                # Start fade-in transition
                self.transition_manager.fade_in()

            # Start fade-out transition
            self.transition_manager.fade_out(callback=create_content)

    def create_unit_navigation(self, parent: ctk.CTkFrame, subject):
        """Create the unit navigation sidebar"""
        unit_nav = ctk.CTkFrame(parent, fg_color="#1e1e1e", width=250)
        unit_nav.pack(side="left", fill="y", padx=(0, 20))
        unit_nav.pack_propagate(False)
        
        # Unit navigation header
        unit_nav_header = ctk.CTkLabel(
            unit_nav,
            text="Units",
            font=("Helvetica", 24, "bold"),
            text_color=subject.color
        )
        unit_nav_header.pack(pady=(20, 10), padx=15)
        
        # Create scrollable frame for unit buttons
        unit_scroll = TouchScrollableFrame(unit_nav, fg_color="transparent")
        unit_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create unit buttons
        for i, unit in enumerate(subject.units):
            unit_button = ctk.CTkButton(
                unit_scroll,
                text=f"Unit {i + 1}: {unit.name}",
                font=("Helvetica", 14),
                fg_color="#2d2d2d",
                hover_color="#3d3d3d",
                anchor="w",
                height=40,
                corner_radius=8,
                command=lambda idx=i: self.controller.select_unit(idx)
            )
            unit_button.pack(fill="x", pady=5)
        
        return unit_nav

    def handle_unit_changed(self, unit_index: int):
        """Handle unit selection"""
        pass  # Units are already visible in the subject view

    def handle_topic_changed(self, topic_name: str):
        """Handle topic selection"""
        subject = self.controller.get_current_subject()
        if subject:
            def create_content():
                self.clear_main_frame()

                # Navigation bar
                nav = NavigationBar(
                    self.main_frame,
                    back_text=f"Back to {subject.name}",
                    back_command=lambda: self.controller.select_subject(subject.name),
                    title_text=f"Learning: {topic_name}"
                )
                nav.pack(fill="x", padx=5, pady=5)

                # Create scrollable lesson content
                content_scroll = TouchScrollableFrame(self.main_frame)
                content_scroll.pack(fill="both", expand=True, padx=5, pady=5)

                # Create lesson content
                lesson = LessonContent(content_scroll, topic=topic_name)
                lesson.pack(fill="both", expand=True)
                
                # Start fade-in transition
                self.transition_manager.fade_in()

            # Start fade-out transition
            self.transition_manager.fade_out(callback=create_content)

    def handle_progress_updated(self, user_progress):
        """Handle progress updates"""
        # Update header stats
        self.header.update_stats(
            user_progress.xp,
            user_progress.points,
            user_progress.streak
        )
        
        # Update sidebar progress
        self.sidebar.update_progress(
            league_data={
                "league": "Diamond",
                "rank": 42,
                "xp": user_progress.xp
            },
            progress_data={
                "progress": user_progress.lessons_completed_today,
                "goal": user_progress.daily_goal
            }
        ) 