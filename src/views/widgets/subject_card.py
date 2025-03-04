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
        # Set fixed dimensions for more compact card size
        kwargs.update({
            "width": 280,  # Reduced width
            "height": 320  # Reduced height
        })
        
        super().__init__(
            master,
            **theme.get_card_style("elevated"),
            **kwargs
        )

        # Store original position for animations
        self._original_pos = None
        self._is_dragging = False
        self._drag_start = None
        self._animation_running = False
        
        # Create content frame with padding
        self.content_frame = BaseWidget(
            self,
            fg_color="transparent"
        )
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Icon with proportional size
        self.icon_label = self._create_label(
            self.content_frame,
            text=data["icon"],
            font=("Helvetica", 48),  # Reduced size
            text_color=data["color"]
        )
        self.icon_label.pack(pady=(0, 10))  # Reduced padding
        
        # Subject name with adjusted font
        self.subject_label = self._create_label(
            self.content_frame,
            text=subject,
            font=("Helvetica", 24, "bold"),  # Adjusted size
            text_color=data["color"]
        )
        self.subject_label.pack(pady=(0, 10))  # Reduced padding
        
        # Unit count with medium font
        unit_count = len(data["units"])
        self.units_label = self._create_label(
            self.content_frame,
            text=f"{unit_count} Units",
            font=("Helvetica", 16),  # Adjusted size
            text_color=theme.colors.text
        )
        self.units_label.pack(pady=(0, 15))  # Reduced padding
        
        # Progress bar (if any progress exists)
        if "progress" in data:
            self.progress_frame = BaseWidget(
                self.content_frame,
                fg_color="transparent",
                height=4,
                width=180  # Reduced width
            )
            self.progress_frame.pack(pady=(0, 15))  # Reduced padding
            
            progress = data.get("progress", 0)
            self.progress_bar = BaseWidget(
                self.progress_frame,
                fg_color=data["color"],
                corner_radius=2,
                height=4,
                width=int(180 * (progress / 100))  # Adjusted width
            )
            self.progress_bar.place(relx=0.5, rely=0.5, anchor="center")
        
        # Start button with hover effect
        self.start_button = BaseButton(
            self.content_frame,
            text="Start Learning",
            command=command,
            style="primary",
            fg_color=data["color"],
            width=180,  # Reduced width
            height=40   # Reduced height
        )
        self.start_button.pack(pady=(0, 0))
        
        # Shadow effect for depth
        self._shadow_intensity = 0
        self.update_shadow()
        
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

    def update_shadow(self):
        """Update the shadow effect based on drag state"""
        target_intensity = 20 if self._is_dragging else 0
        current = self._shadow_intensity
        
        if current != target_intensity:
            def animate_shadow(step=0):
                if step < 10:
                    progress = self._ease_in_out(step / 10)
                    intensity = current + (target_intensity - current) * progress
                    self.configure(border_width=1)
                    self.configure(border_color=self._adjust_opacity(theme.colors.text, intensity / 100))
                    self.after(20, lambda: animate_shadow(step + 1))
                else:
                    self._shadow_intensity = target_intensity
            
            animate_shadow()

    def _on_press(self, event):
        """Handle mouse press"""
        if self._animation_running:
            return
            
        # Store initial position
        self._drag_start = (event.x_root, event.y_root)
        self._original_pos = self.winfo_x(), self.winfo_y()
        
        # Visual feedback
        self.lift()  # Bring to front
        self._is_dragging = True
        self.update_shadow()

    def _on_drag(self, event):
        """Handle mouse drag"""
        if not self._is_dragging or not self._drag_start or not self._original_pos:
            return
            
        # Calculate movement with smoothing
        dx = event.x_root - self._drag_start[0]
        dy = event.y_root - self._drag_start[1]
        
        # Apply smooth movement
        self.place(
            x=self._original_pos[0] + dx,
            y=self._original_pos[1] + dy
        )

    def _on_release(self, event):
        """Handle mouse release"""
        if not self._is_dragging:
            return
            
        self._is_dragging = False
        self.update_shadow()
        
        if self._original_pos:
            self._animate_return()
        
        # Reset drag state
        self._drag_start = None
        self._original_pos = None

    def _animate_return(self, duration=300):
        """Animate the card returning to its original position"""
        if self._animation_running or not hasattr(self, '_original_grid_info'):
            return
            
        self._animation_running = True
        start_time = self.after_idle(lambda: None)  # Get current time
        
        current_x = self.winfo_x()
        current_y = self.winfo_y()
        target_x = self._original_grid_info.get('x', 0)
        target_y = self._original_grid_info.get('y', 0)
        
        def _animate_step(elapsed):
            if elapsed >= duration:
                # Final position
                self.place_forget()
                self.grid(**self._original_grid_info)
                self._animation_running = False
                return
                
            # Calculate progress with easing
            progress = self._ease_in_out(elapsed / duration)
            
            # Calculate new position
            new_x = current_x + (target_x - current_x) * progress
            new_y = current_y + (target_y - current_y) * progress
            
            # Update position
            self.place(x=new_x, y=new_y)
            
            # Schedule next frame
            self.after(16, lambda: _animate_step(elapsed + 16))  # ~60fps
        
        _animate_step(0)

    def _store_grid_info(self, event):
        """Store grid information when the widget is mapped"""
        self._original_grid_info = self.grid_info() 