import customtkinter as ctk
import math

class IconWidget(ctk.CTkCanvas):
    def __init__(
        self,
        master,
        size=120,
        color="#ffffff",
        hover_color=None,
        icon_type="math",
        **kwargs
    ):
        super().__init__(
            master,
            width=size,
            height=size,
            bg=master._fg_color,
            highlightthickness=0,
            **kwargs
        )

        self.size = size
        self.color = color
        self.hover_color = hover_color or color
        self.icon_type = icon_type
        self.animation_id = None
        self.current_scale = 1.0
        self.target_scale = 1.0
        
        # Draw initial icon
        self.draw_icon()
        
        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def draw_icon(self):
        """Draw the icon based on type"""
        self.delete("all")  # Clear canvas
        
        # Calculate center and working area
        cx = self.size / 2
        cy = self.size / 2
        padding = self.size * 0.2
        radius = (self.size - 2 * padding) / 2
        
        if self.icon_type == "math":
            # Draw math icon (calculator/grid style)
            self._draw_math_icon(cx, cy, radius)
        elif self.icon_type == "science":
            # Draw science icon (microscope style)
            self._draw_science_icon(cx, cy, radius)
        elif self.icon_type == "language":
            # Draw language icon (books style)
            self._draw_language_icon(cx, cy, radius)
        elif self.icon_type == "social":
            # Draw social studies icon (globe style)
            self._draw_social_icon(cx, cy, radius)
        elif self.icon_type == "computer":
            # Draw computer science icon (laptop/code style)
            self._draw_computer_icon(cx, cy, radius)
        elif self.icon_type == "foreign":
            # Draw foreign language icon (speech bubbles)
            self._draw_foreign_icon(cx, cy, radius)

    def _draw_math_icon(self, cx, cy, radius):
        """Draw animated math icon"""
        # Draw calculator body
        calc_width = radius * 2
        calc_height = radius * 2.2
        self.create_rectangle(
            cx - radius, cy - radius,
            cx + radius, cy + radius * 1.2,
            fill=self.color,
            width=0,
            radius=10
        )
        
        # Draw calculator screen
        screen_padding = radius * 0.2
        self.create_rectangle(
            cx - radius + screen_padding,
            cy - radius + screen_padding,
            cx + radius - screen_padding,
            cy - radius/2,
            fill="#1a1b1e",
            width=0,
            radius=5
        )
        
        # Draw calculator buttons
        button_rows = 4
        button_cols = 4
        button_padding = radius * 0.15
        button_area_width = calc_width - screen_padding * 2
        button_area_height = calc_height - (cy - radius/2 + screen_padding) - screen_padding
        button_size = min(
            (button_area_width - button_padding * (button_cols - 1)) / button_cols,
            (button_area_height - button_padding * (button_rows - 1)) / button_rows
        )
        
        for row in range(button_rows):
            for col in range(button_cols):
                x = cx - radius + screen_padding + col * (button_size + button_padding)
                y = cy - radius/2 + screen_padding + row * (button_size + button_padding) + button_padding * 2
                
                self.create_rectangle(
                    x, y,
                    x + button_size, y + button_size,
                    fill="#1a1b1e",
                    width=0,
                    radius=5
                )

    def _draw_science_icon(self, cx, cy, radius):
        """Draw animated science icon"""
        # Draw flask
        flask_width = radius * 1.2
        flask_neck_width = radius * 0.4
        flask_neck_height = radius * 0.8
        
        # Flask neck
        self.create_rectangle(
            cx - flask_neck_width/2,
            cy - radius,
            cx + flask_neck_width/2,
            cy - radius + flask_neck_height,
            fill=self.color,
            width=0
        )
        
        # Flask body (triangle with rounded corners)
        points = [
            cx - flask_width, cy + radius,  # Bottom left
            cx + flask_width, cy + radius,  # Bottom right
            cx + flask_neck_width/2, cy - radius + flask_neck_height,  # Top right
            cx - flask_neck_width/2, cy - radius + flask_neck_height,  # Top left
        ]
        self.create_polygon(points, fill=self.color, width=0, smooth=True)
        
        # Bubbles
        bubble_positions = [
            (cx - radius * 0.4, cy + radius * 0.3, radius * 0.2),
            (cx + radius * 0.2, cy + radius * 0.1, radius * 0.15),
            (cx - radius * 0.1, cy - radius * 0.2, radius * 0.1),
        ]
        
        for x, y, size in bubble_positions:
            self.create_oval(
                x - size, y - size,
                x + size, y + size,
                fill="#1a1b1e",
                width=0
            )

    def _draw_language_icon(self, cx, cy, radius):
        """Draw animated language icon"""
        # Draw open book
        book_width = radius * 2
        book_height = radius * 1.6
        page_curve = radius * 0.2
        
        # Left page
        points_left = [
            cx - book_width/2, cy - book_height/2,  # Top left
            cx, cy - book_height/2,  # Top right
            cx, cy + book_height/2,  # Bottom right
            cx - book_width/2, cy + book_height/2,  # Bottom left
        ]
        self.create_polygon(points_left, fill=self.color, width=0, smooth=True)
        
        # Right page
        points_right = [
            cx, cy - book_height/2,  # Top left
            cx + book_width/2, cy - book_height/2,  # Top right
            cx + book_width/2, cy + book_height/2,  # Bottom right
            cx, cy + book_height/2,  # Bottom left
        ]
        self.create_polygon(points_right, fill=self.color, width=0, smooth=True)
        
        # Add text lines
        line_spacing = radius * 0.25
        line_margin = radius * 0.3
        for i in range(4):
            # Left page lines
            line_width = radius * (0.8 - i * 0.1)
            self.create_line(
                cx - book_width/2 + line_margin,
                cy - book_height/4 + i * line_spacing,
                cx - line_margin - radius * 0.1,
                cy - book_height/4 + i * line_spacing,
                fill="#1a1b1e",
                width=2
            )
            
            # Right page lines
            self.create_line(
                cx + line_margin,
                cy - book_height/4 + i * line_spacing,
                cx + book_width/2 - line_margin,
                cy - book_height/4 + i * line_spacing,
                fill="#1a1b1e",
                width=2
            )

    def _draw_social_icon(self, cx, cy, radius):
        """Draw animated globe icon"""
        # Draw main globe circle
        self.create_oval(
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius,
            fill=self.color,
            width=0
        )
        
        # Draw latitude lines
        lat_count = 5
        for i in range(lat_count):
            y_offset = radius * (i - lat_count/2) * 0.3
            # Create curved line effect
            curve_factor = math.cos(math.pi * (y_offset/radius))
            line_width = radius * 2 * curve_factor
            x_offset = radius * (1 - curve_factor)
            
            self.create_line(
                cx - line_width/2, cy + y_offset,
                cx + line_width/2, cy + y_offset,
                fill="#1a1b1e",
                width=2
            )
        
        # Draw longitude curves
        for i in range(3):
            angle_offset = i * 45 - 45
            self.create_arc(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                start=angle_offset,
                extent=180,
                style="arc",
                outline="#1a1b1e",
                width=2
            )

    def _draw_computer_icon(self, cx, cy, radius):
        """Draw animated computer icon"""
        # Draw monitor
        monitor_width = radius * 2
        monitor_height = radius * 1.4
        bezel = radius * 0.1
        
        # Monitor body
        self.create_rectangle(
            cx - monitor_width/2,
            cy - radius,
            cx + monitor_width/2,
            cy + monitor_height - radius,
            fill=self.color,
            width=0,
            radius=10
        )
        
        # Screen
        self.create_rectangle(
            cx - monitor_width/2 + bezel,
            cy - radius + bezel,
            cx + monitor_width/2 - bezel,
            cy + monitor_height - radius - bezel,
            fill="#1a1b1e",
            width=0,
            radius=5
        )
        
        # Stand base
        base_width = radius * 0.8
        base_height = radius * 0.2
        self.create_rectangle(
            cx - base_width/2,
            cy + monitor_height - radius,
            cx + base_width/2,
            cy + monitor_height - radius + base_height,
            fill=self.color,
            width=0,
            radius=5
        )
        
        # Code lines
        line_spacing = radius * 0.25
        for i in range(4):
            line_length = radius * (1.4 - i * 0.2)
            indent = radius * 0.2 * (i % 2)  # Alternate line indentation
            self.create_line(
                cx - monitor_width/2 + bezel * 2 + indent,
                cy - radius/2 + i * line_spacing,
                cx - monitor_width/2 + bezel * 2 + line_length,
                cy - radius/2 + i * line_spacing,
                fill=self.color,
                width=2
            )

    def _draw_foreign_icon(self, cx, cy, radius):
        """Draw animated speech bubbles icon"""
        # Draw main chat bubble
        bubble_points = [
            cx - radius, cy - radius * 0.7,  # Top left
            cx + radius * 0.7, cy - radius * 0.7,  # Top right
            cx + radius * 0.7, cy + radius * 0.2,  # Bottom right
            cx - radius * 0.3, cy + radius * 0.2,  # Bottom middle
            cx - radius * 0.5, cy + radius * 0.7,  # Tail tip
            cx - radius * 0.7, cy + radius * 0.2,  # Bottom left after tail
            cx - radius, cy + radius * 0.2,  # Bottom left
        ]
        self.create_polygon(bubble_points, fill=self.color, width=0, smooth=True)
        
        # Draw second bubble (smaller, overlapping)
        bubble2_points = [
            cx - radius * 0.4, cy - radius * 0.3,  # Top left
            cx + radius, cy - radius * 0.3,  # Top right
            cx + radius, cy + radius * 0.6,  # Bottom right
            cx + radius * 0.3, cy + radius * 0.6,  # Bottom middle
            cx + radius * 0.1, cy + radius,  # Tail tip
            cx, cy + radius * 0.6,  # After tail
            cx - radius * 0.4, cy + radius * 0.6,  # Bottom left
        ]
        self.create_polygon(bubble2_points, fill=self.color, width=0, smooth=True)
        
        # Add conversation dots
        dot_positions = [
            (cx - radius * 0.6, cy - radius * 0.2),
            (cx - radius * 0.3, cy - radius * 0.2),
            (cx, cy - radius * 0.2),
            (cx + radius * 0.3, cy + radius * 0.2),
            (cx + radius * 0.6, cy + radius * 0.2),
        ]
        
        for x, y in dot_positions:
            self.create_oval(
                x - radius * 0.08,
                y - radius * 0.08,
                x + radius * 0.08,
                y + radius * 0.08,
                fill="#1a1b1e",
                width=0
            )

    def _animate(self):
        """Animate the icon scale"""
        if abs(self.current_scale - self.target_scale) > 0.01:
            # Calculate new scale
            self.current_scale += (self.target_scale - self.current_scale) * 0.2
            
            # Apply scale transformation
            self.scale("all", self.size/2, self.size/2, 
                      self.current_scale/self._last_scale, 
                      self.current_scale/self._last_scale)
            
            self._last_scale = self.current_scale
            
            # Continue animation
            self.animation_id = self.after(16, self._animate)
        else:
            self.animation_id = None

    def _on_enter(self, event):
        """Handle mouse enter"""
        self.target_scale = 1.1
        self._last_scale = self.current_scale
        if not self.animation_id:
            self._animate()
        self.itemconfig("all", fill=self.hover_color)

    def _on_leave(self, event):
        """Handle mouse leave"""
        self.target_scale = 1.0
        self._last_scale = self.current_scale
        if not self.animation_id:
            self._animate()
        self.itemconfig("all", fill=self.color) 