from typing import Dict, Callable, Any
import customtkinter as ctk
from PIL import Image, ImageTk
import colorsys
from .icon_widget import IconWidget
from src.utils.theme import theme
from src.utils.icon_loader import icon_loader
from src.views.widgets.base_widget import BaseWidget
import os

class SubjectCard(BaseWidget):
    # Map subjects to their icon files
    ICON_MAP = {
        "Mathematics": "math_icon.png",
        "Biology": "biology_icon.png",
        "Chemistry": "chemestry_icon.png",
        # Default icons for other subjects will use math_icon.png
    }

    def __init__(
        self,
        master,
        subject,
        data,
        command=None,
        **kwargs
    ):
        super().__init__(
            master,
            width=280,
            height=180,
            corner_radius=15,
            fg_color=theme.colors.card_bg,
            **kwargs
        )
        
        self.subject = subject
        self.data = data
        self.command = command
        
        # Create content frame with padding
        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content.pack(expand=True, fill="both", padx=20, pady=15)
        
        # Icon container for better centering and hover effects
        self.icon_container = ctk.CTkFrame(
            self.content,
            fg_color="transparent",
            width=90,
            height=90
        )
        self.icon_container.pack(pady=(0, 10))
        self.icon_container.pack_propagate(False)
        
        # Load the appropriate icon for this subject
        icon_size = 64  # Base size for the icon
        icon_file = self.ICON_MAP.get(subject, "math_icon.png")  # Default to math icon if subject not found
        
        self.icon = ctk.CTkLabel(
            self.icon_container,
            text="",
            image=icon_loader.get_custom_icon(icon_file, size=icon_size),
            width=icon_size,
            height=icon_size
        )
        self.icon.place(relx=0.5, rely=0.5, anchor="center")
        
        # Subject name with larger font
        self.name_label = ctk.CTkLabel(
            self.content,
            text=subject,
            font=theme.typography.h3
        )
        self.name_label.pack(pady=(0, 5))
        
        # Unit count
        unit_count = len(data.get("units", []))
        self.unit_label = ctk.CTkLabel(
            self.content,
            text=f"{unit_count} Units",
            font=theme.typography.body2,
            text_color=theme.colors.text_secondary
        )
        self.unit_label.pack(pady=(0, 10))
        
        # Progress bar (if progress data available)
        if "progress" in data:
            progress = data["progress"]
            self.progress_bar = ctk.CTkProgressBar(
                self.content,
                width=200,
                height=6,
                corner_radius=3
            )
            self.progress_bar.set(progress)
            self.progress_bar.pack(pady=(0, 10))
        
        # Start button
        self.start_button = ctk.CTkButton(
            self.content,
            text="Start Learning",
            width=160,
            height=32,
            corner_radius=16,
            font=theme.typography.button,
            command=self._handle_click
        )
        self.start_button.pack()
        
        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _handle_click(self):
        if self.command:
            self.command(self.subject)
            
    def _on_enter(self, event):
        """Handle hover enter - scale up icon with smooth animation"""
        self.icon.configure(width=74, height=74)  # Scale up by ~15%
        
    def _on_leave(self, event):
        """Handle hover leave - return to normal scale with smooth animation"""
        self.icon.configure(width=64, height=64)

    def _create_gradient(self, base_color):
        """Create a darker gradient version of the base color"""
        # Convert hex to HSV
        base_color = base_color.lstrip('#')
        rgb = tuple(int(base_color[i:i+2], 16) for i in (0, 2, 4))
        hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        
        # Create darker version
        darker_hsv = (hsv[0], hsv[1], hsv[2] * 0.7)
        darker_rgb = colorsys.hsv_to_rgb(*darker_hsv)
        darker_hex = '#{:02x}{:02x}{:02x}'.format(
            int(darker_rgb[0] * 255),
            int(darker_rgb[1] * 255),
            int(darker_rgb[2] * 255)
        )
        
        return [base_color, darker_hex]
    
    def _adjust_color(self, color, factor):
        """Adjust color brightness"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(min(int(c * factor), 255) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)
    
    def _lighten_color(self, color, factor=1.3):
        """Create lighter version of a color"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(min(int(c * factor), 255) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)
    
    def _on_press(self, event):
        self.original_pos = (self.winfo_x(), self.winfo_y())
        
    def _on_drag(self, event):
        if self.original_pos:
            x = self.winfo_x() + (event.x_root - self._last_click_x)
            y = self.winfo_y() + (event.y_root - self._last_click_y)
            self.place(x=x, y=y)
            
    def _on_release(self, event):
        if self.original_pos:
            current_pos = (self.winfo_x(), self.winfo_y())
            if current_pos != self.original_pos:
                # Animate back to original position
                self.place(x=self.original_pos[0], y=self.original_pos[1])
            self.original_pos = None 