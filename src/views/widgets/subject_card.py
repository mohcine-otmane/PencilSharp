from typing import Dict, Callable, Any
from src.views.widgets.base_widget import BaseWidget, BaseButton
from src.utils.theme import theme

class SubjectCard(BaseWidget):
    def __init__(
        self,
        master: Any,
        subject: str,
        data: Dict,
        command: Callable,
        **kwargs
    ):
        super().__init__(
            master,
            **theme.get_card_style("elevated"),
            **kwargs
        )

        # Store original position for animations
        self._original_pos = None
        self._is_dragging = False
        
        # Create content frame with padding
        self.content_frame = BaseWidget(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(
            expand=True,
            fill="both",
            padx=theme.sizing.padding_xlarge,
            pady=theme.sizing.padding_xlarge
        )
        
        # Center content vertically
        self.content_frame.grid_rowconfigure((0, 5), weight=1)
        
        # Icon with increased size
        self.icon_label = self._create_label(
            self.content_frame,
            text=data["icon"],
            font=("Helvetica", theme.sizing.icon_size_large * 2),
            text_color=data["color"]
        )
        self.icon_label.pack(pady=(0, theme.sizing.padding_large))
        
        # Subject name with larger font
        self.subject_label = self._create_label(
            self.content_frame,
            text=subject,
            font=theme.typography.header_medium,
            text_color=data["color"]
        )
        self.subject_label.pack(pady=(0, theme.sizing.padding_large))
        
        # Unit count with medium font
        unit_count = len(data["units"])
        self.units_label = self._create_label(
            self.content_frame,
            text=f"{unit_count} Units",
            font=theme.typography.body_large,
            text_color=theme.colors.text
        )
        self.units_label.pack(pady=(0, theme.sizing.padding_xlarge))
        
        # Progress bar (if any progress exists)
        if "progress" in data:
            self.progress_frame = BaseWidget(
                self.content_frame,
                fg_color="transparent",
                height=4
            )
            self.progress_frame.pack(fill="x", pady=(0, theme.sizing.padding_large))
            
            progress = data.get("progress", 0)
            self.progress_bar = BaseWidget(
                self.progress_frame,
                fg_color=data["color"],
                corner_radius=2,
                width=int(200 * (progress / 100))
            )
            self.progress_bar.place(relx=0.5, rely=0.5, anchor="center")
        
        # Start button with hover effect
        self.start_button = BaseButton(
            self.content_frame,
            text="Start Learning",
            command=command,
            style="primary",
            fg_color=data["color"],
            width=240,
            height=50
        )
        self.start_button.pack(pady=(0, 0))
        
        # Bind mouse events for drag functionality
        self.bind("<Button-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _create_label(self, parent, **kwargs):
        """Create a themed label"""
        return ctk.CTkLabel(
            parent,
            font=kwargs.pop("font", theme.typography.body_medium),
            text_color=kwargs.pop("text_color", theme.colors.text),
            **kwargs
        )

    def _on_press(self, event):
        """Handle mouse press"""
        # Store initial position
        self._drag_start = (event.x_root, event.y_root)
        self._original_pos = self.winfo_x(), self.winfo_y()
        
        # Visual feedback
        self.configure(border_width=2, border_color=theme.colors.primary)
        
        # Lift above other widgets
        self.lift()

    def _on_drag(self, event):
        """Handle mouse drag"""
        if self._drag_start and self._original_pos:
            # Calculate movement
            dx = event.x_root - self._drag_start[0]
            dy = event.y_root - self._drag_start[1]
            
            # Update position with smooth animation
            self.place(
                x=self._original_pos[0] + dx,
                y=self._original_pos[1] + dy
            )
            
            self._is_dragging = True

    def _on_release(self, event):
        """Handle mouse release"""
        if self._is_dragging:
            # Animate back to original position
            self._animate_return()
        
        # Reset drag state
        self._drag_start = None
        self._original_pos = None
        self._is_dragging = False
        
        # Remove visual feedback
        self.configure(border_width=0)

    def _animate_return(self, steps=15):
        """Animate the card returning to its original position"""
        if not hasattr(self, '_original_grid_info'):
            return
        
        current_x = self.winfo_x()
        current_y = self.winfo_y()
        target_x = self._original_pos[0]
        target_y = self._original_pos[1]
        
        dx = (target_x - current_x) / steps
        dy = (target_y - current_y) / steps
        
        def _step(step):
            if step < steps:
                progress = self._ease_in_out(step / steps)
                self.place(
                    x=current_x + dx * (step + 1),
                    y=current_y + dy * (step + 1)
                )
                self.after(20, lambda: _step(step + 1))
            else:
                # Restore original grid position
                self.place_forget()
                self.grid(**self._original_grid_info)
        
        _step(0)

    def _store_grid_info(self, event):
        """Store grid information when the widget is mapped"""
        self._original_grid_info = self.grid_info() 