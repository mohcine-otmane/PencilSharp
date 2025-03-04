from typing import Optional, Callable, Any
import customtkinter as ctk
from src.views.widgets.base_widget import BaseWidget, BaseButton
from src.utils.theme import theme

class NavigationBar(BaseWidget):
    def __init__(
        self,
        master: Any,
        back_text: str,
        back_command: Callable,
        title_text: str,
        title_color: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=theme.colors.background,
            height=60,
            **kwargs
        )
        self.pack(fill='x', padx=0, pady=0)
        
        # Create inner frame for content with padding
        self.inner_frame = BaseWidget(
            self,
            fg_color="transparent"
        )
        self.inner_frame.pack(fill='x', padx=20, pady=10)
        
        # Configure grid weights
        self.inner_frame.grid_columnconfigure(1, weight=1)
        
        # Back button with improved styling
        self.back_button = BaseButton(
            self.inner_frame,
            text=f"← {back_text}",
            command=back_command,
            style="secondary"
        )
        self.back_button.grid(row=0, column=0, padx=(0, 20))
        
        # Title with larger font and optional color
        self.title_label = ctk.CTkLabel(
            self.inner_frame,
            text=title_text,
            font=theme.typography.header_medium,
            text_color=title_color or theme.colors.text
        )
        self.title_label.grid(row=0, column=1, sticky="w")
        
        # Add shadow effect
        self.shadow = BaseWidget(
            self,
            height=2,
            fg_color="transparent"
        )
        self.shadow.pack(fill='x', side="bottom")
        
        # Create gradient shadow effect
        for i in range(3):
            opacity = 0.1 - (i * 0.03)
            line = BaseWidget(
                self.shadow,
                height=1,
                fg_color=self._adjust_opacity(theme.colors.text, opacity)
            )
            line.pack(fill='x')
        
        # Add hover effect to back button
        self.back_button.bind("<Enter>", self._on_back_hover_enter)
        self.back_button.bind("<Leave>", self._on_back_hover_leave)
        
        # Initialize animation variables
        self._title_animation_running = False
        self._title_animation_id = None
        
        # Add entrance animation
        self.animate_entrance()

    def animate_entrance(self):
        """Animate the navigation bar entrance"""
        # Start with transparent background
        self.configure(fg_color="transparent")
        
        # Animate background color
        def animate_bg():
            steps = 20
            duration = 300
            step_time = duration // steps
            
            def _animate_bg(step=0):
                if step <= steps:
                    progress = step / steps
                    opacity = self._ease_in_out(progress)
                    self.configure(
                        fg_color=self._adjust_opacity(
                            theme.colors.background,
                            opacity
                        )
                    )
                    self.after(step_time, lambda: _animate_bg(step + 1))
            
            _animate_bg()
        
        # Animate title entrance
        def animate_title():
            original_x = self.title_label.winfo_x()
            self.title_label.place(x=original_x - 20)
            
            steps = 20
            duration = 300
            step_time = duration // steps
            
            def _animate_title(step=0):
                if step <= steps:
                    progress = step / steps
                    ease = self._ease_in_out(progress)
                    x = original_x - (20 * (1 - ease))
                    opacity = ease
                    self.title_label.place(x=x)
                    self.title_label.configure(
                        text_color=self._adjust_opacity(
                            theme.colors.text,
                            opacity
                        )
                    )
                    if step < steps:
                        self.after(step_time, lambda: _animate_title(step + 1))
                    else:
                        self.title_label.grid(row=0, column=1, sticky="w")
            
            _animate_title()
        
        # Start animations
        self.after(100, animate_bg)
        self.after(200, animate_title)

    def _on_back_hover_enter(self, event):
        """Handle back button hover enter"""
        self.back_button.configure(
            text=f"← {self.back_button.cget('text').replace('← ', '')}",
            font=("Helvetica", 16, "bold")
        )

    def _on_back_hover_leave(self, event):
        """Handle back button hover leave"""
        self.back_button.configure(
            font=("Helvetica", 16)
        )

    def _ease_in_out(self, t):
        """Ease-in-out function"""
        return 0.5 * (1 - math.cos(math.pi * t))

    def _adjust_opacity(self, color, opacity):
        """Adjust the opacity of a color"""
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        return '#{:02X}{:02X}{:02X}'.format(
            int(r * opacity),
            int(g * opacity),
            int(b * opacity)
        ) 