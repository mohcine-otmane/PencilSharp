import customtkinter as ctk
from typing import Optional, Callable, Any, Dict
from src.utils.theme import theme

class BaseWidget(ctk.CTkFrame):
    def __init__(
        self,
        master: Any,
        width: int = 0,
        height: int = 0,
        corner_radius: Optional[int] = None,
        border_width: Optional[int] = None,
        bg_color: Optional[str] = None,
        fg_color: Optional[str] = None,
        border_color: Optional[str] = None,
        background_corner_colors: Optional[tuple] = None,
        overwrite_preferred_drawing_method: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            master=master,
            width=width,
            height=height,
            corner_radius=corner_radius,
            border_width=border_width,
            bg_color=bg_color,
            fg_color=fg_color or theme.colors.surface,
            border_color=border_color,
            background_corner_colors=background_corner_colors,
            overwrite_preferred_drawing_method=overwrite_preferred_drawing_method,
            **kwargs
        )
        
        # Initialize animation variables
        self._animation_running = False
        self._animation_id = None
        self._hover_animation_running = False
        self._hover_animation_id = None
        
        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def animate_opacity(
        self,
        start: float = 0.0,
        end: float = 1.0,
        duration: int = 250,
        callback: Optional[Callable] = None
    ):
        """Animate the widget's opacity"""
        if self._animation_running:
            self.after_cancel(self._animation_id)
        
        steps = 20
        step_time = duration // steps
        
        def _animate(step: int = 0):
            if step <= steps:
                progress = step / steps
                opacity = start + (end - start) * self._ease_in_out(progress)
                self.configure(fg_color=self._adjust_opacity(theme.colors.surface, opacity))
                self._animation_id = self.after(step_time, lambda: _animate(step + 1))
                self._animation_running = True
            else:
                self._animation_running = False
                if callback:
                    callback()
        
        _animate()

    def animate_hover(
        self,
        hover_in: bool,
        duration: int = 150
    ):
        """Animate hover effect"""
        if self._hover_animation_running:
            self.after_cancel(self._hover_animation_id)
        
        start_color = theme.colors.surface
        end_color = theme.colors.surface_variant if hover_in else theme.colors.surface
        steps = 10
        step_time = duration // steps
        
        def _animate(step: int = 0):
            if step <= steps:
                progress = step / steps
                color = self._interpolate_color(
                    start_color,
                    end_color,
                    self._ease_in_out(progress)
                )
                self.configure(fg_color=color)
                self._hover_animation_id = self.after(
                    step_time,
                    lambda: _animate(step + 1)
                )
                self._hover_animation_running = True
            else:
                self._hover_animation_running = False
        
        _animate()

    def _on_enter(self, event):
        """Handle mouse enter event"""
        self.animate_hover(True)

    def _on_leave(self, event):
        """Handle mouse leave event"""
        self.animate_hover(False)

    @staticmethod
    def _ease_in_out(t: float) -> float:
        """Cubic easing function"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2

    @staticmethod
    def _adjust_opacity(hex_color: str, opacity: float) -> str:
        """Adjust the opacity of a hex color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return '#{:02x}{:02x}{:02x}{:02x}'.format(*rgb, int(opacity * 255))

    @staticmethod
    def _interpolate_color(start_color: str, end_color: str, progress: float) -> str:
        """Interpolate between two colors"""
        start = tuple(int(start_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        end = tuple(int(end_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        current = tuple(
            int(start[i] + (end[i] - start[i]) * progress)
            for i in range(3)
        )
        return '#{:02x}{:02x}{:02x}'.format(*current)

class BaseButton(ctk.CTkButton):
    def __init__(
        self,
        master: Any,
        text: str = "",
        command: Optional[Callable] = None,
        style: str = "primary",
        **kwargs
    ):
        button_style = theme.get_button_style(style)
        button_style.update(kwargs)
        
        super().__init__(
            master=master,
            text=text,
            command=command,
            **button_style
        )
        
        self._hover_animation_running = False
        self._hover_animation_id = None
        self._original_color = button_style["fg_color"]
        self._hover_color = button_style["hover_color"]

    def animate_hover(
        self,
        hover_in: bool,
        duration: int = 150
    ):
        """Animate hover effect"""
        if self._hover_animation_running:
            self.after_cancel(self._hover_animation_id)
        
        start_color = self._hover_color if hover_in else self._original_color
        end_color = self._original_color if hover_in else self._hover_color
        steps = 10
        step_time = duration // steps
        
        def _animate(step: int = 0):
            if step <= steps:
                progress = step / steps
                color = self._interpolate_color(
                    start_color,
                    end_color,
                    self._ease_in_out(progress)
                )
                self.configure(fg_color=color)
                self._hover_animation_id = self.after(
                    step_time,
                    lambda: _animate(step + 1)
                )
                self._hover_animation_running = True
            else:
                self._hover_animation_running = False
        
        _animate()

    @staticmethod
    def _ease_in_out(t: float) -> float:
        """Cubic easing function"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2

    @staticmethod
    def _interpolate_color(start_color: str, end_color: str, progress: float) -> str:
        """Interpolate between two colors"""
        start = tuple(int(start_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        end = tuple(int(end_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        current = tuple(
            int(start[i] + (end[i] - start[i]) * progress)
            for i in range(3)
        )
        return '#{:02x}{:02x}{:02x}'.format(*current) 