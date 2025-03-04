from dataclasses import dataclass
from typing import Dict, Any
import customtkinter as ctk

@dataclass
class ThemeColors:
    primary: str = "#58cc02"
    secondary: str = "#3c3c3c"
    background: str = "#1a1a1a"
    surface: str = "#2b2b2b"
    surface_variant: str = "#323232"
    text: str = "#ffffff"
    text_secondary: str = "#b3b3b3"
    error: str = "#ff4b4b"
    success: str = "#58cc02"
    warning: str = "#ffc800"
    info: str = "#4b8eff"

@dataclass
class ThemeSizing:
    padding_small: int = 5
    padding_medium: int = 10
    padding_large: int = 20
    padding_xlarge: int = 30
    border_radius_small: int = 8
    border_radius_medium: int = 12
    border_radius_large: int = 16
    border_radius_xlarge: int = 24
    button_height_small: int = 32
    button_height_medium: int = 40
    button_height_large: int = 48
    icon_size_small: int = 24
    icon_size_medium: int = 32
    icon_size_large: int = 48

@dataclass
class ThemeTypography:
    font_family: str = "Helvetica"
    header_large: tuple = ("Helvetica", 36, "bold")
    header_medium: tuple = ("Helvetica", 28, "bold")
    header_small: tuple = ("Helvetica", 24, "bold")
    body_large: tuple = ("Helvetica", 18)
    body_medium: tuple = ("Helvetica", 16)
    body_small: tuple = ("Helvetica", 14)
    caption: tuple = ("Helvetica", 12)

class ThemeManager:
    def __init__(self):
        self.colors = ThemeColors()
        self.sizing = ThemeSizing()
        self.typography = ThemeTypography()
        
    def get_button_style(self, style: str = "primary") -> Dict[str, Any]:
        """Get consistent button styling"""
        styles = {
            "primary": {
                "fg_color": self.colors.primary,
                "hover_color": self._adjust_brightness(self.colors.primary, 0.8),
                "text_color": self.colors.text,
                "font": self.typography.body_medium,
                "corner_radius": self.sizing.border_radius_medium,
                "height": self.sizing.button_height_medium,
            },
            "secondary": {
                "fg_color": self.colors.secondary,
                "hover_color": self._adjust_brightness(self.colors.secondary, 1.2),
                "text_color": self.colors.text,
                "font": self.typography.body_medium,
                "corner_radius": self.sizing.border_radius_medium,
                "height": self.sizing.button_height_medium,
            },
            "outline": {
                "fg_color": "transparent",
                "hover_color": self._adjust_brightness(self.colors.surface, 1.1),
                "text_color": self.colors.text,
                "font": self.typography.body_medium,
                "corner_radius": self.sizing.border_radius_medium,
                "height": self.sizing.button_height_medium,
                "border_width": 2,
                "border_color": self.colors.primary,
            }
        }
        return styles.get(style, styles["primary"])

    def get_card_style(self, style: str = "default") -> Dict[str, Any]:
        """Get consistent card styling"""
        styles = {
            "default": {
                "fg_color": self.colors.surface,
                "corner_radius": self.sizing.border_radius_large,
                "border_width": 2,
                "border_color": self._adjust_brightness(self.colors.surface, 1.2),
            },
            "elevated": {
                "fg_color": self.colors.surface,
                "corner_radius": self.sizing.border_radius_large,
                "border_width": 0,
            }
        }
        return styles.get(style, styles["default"])

    def get_input_style(self) -> Dict[str, Any]:
        """Get consistent input field styling"""
        return {
            "fg_color": self.colors.surface_variant,
            "border_color": self._adjust_brightness(self.colors.surface_variant, 1.2),
            "text_color": self.colors.text,
            "placeholder_text_color": self.colors.text_secondary,
            "font": self.typography.body_medium,
            "corner_radius": self.sizing.border_radius_medium,
        }

    @staticmethod
    def _adjust_brightness(hex_color: str, factor: float) -> str:
        """Adjust the brightness of a hex color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(min(int(c * factor), 255) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)

# Create a global theme instance
theme = ThemeManager()

class Theme:
    def __init__(self):
        # Color palette
        self.colors = {
            "background": "#1a1b1e",
            "surface": "#1e2124",
            "surface_variant": "#2a2b30",
            "primary": "#2196F3",
            "secondary": "#4CAF50",
            "text": "#ffffff",
            "text_secondary": "#8a8d93",
            "error": "#f44336",
            "success": "#4CAF50",
            "warning": "#ff9800"
        }
        
        # Font configurations
        self.fonts = {
            "heading": ("Helvetica", 24, "bold"),
            "subheading": ("Helvetica", 18, "bold"),
            "body": ("Helvetica", 14),
            "caption": ("Helvetica", 12)
        }
        
        # Spacing and sizing
        self.spacing = {
            "xs": 5,
            "sm": 10,
            "md": 20,
            "lg": 40,
            "xl": 60
        }
        
        # Border radius
        self.radius = {
            "sm": 8,
            "md": 15,
            "lg": 30
        }

# Create a singleton instance
theme = Theme()

def set_theme():
    """Configure the application theme"""
    # Set appearance mode to dark
    ctk.set_appearance_mode("dark")
    # Set default color theme to blue
    ctk.set_default_color_theme("blue")

theme = {
    "primary": "#2196F3",
    "primary_dark": "#1976D2",
    "background": "#1a1b1e",
    "surface": "#1e2124",
    "surface_dark": "#2a2b30",
    "text": "#ffffff",
    "text_secondary": "#8a8d93"
} 