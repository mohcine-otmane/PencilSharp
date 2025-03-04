import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})
from sympy import preview
import io
from PIL import Image, ImageTk
import os
import tempfile
from pathlib import Path
from tkhtmlview import HTMLScrolledText
import tkinter as tk
import sys
sys.path.append("C:\\PyQt6")

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QWindow

class TransitionManager:
    def __init__(self, parent):
        self.parent = parent
        self.overlay = None
        self.fade_steps = 20  # Increased steps for smoother transition
        self.fade_delay = 10  # Decreased delay for faster overall transition
        self.fade_color = "#1a1a1a"  # Darker gray instead of pure black for softer transition

    def _ease_in_out(self, t):
        # Cubic easing function for smoother acceleration and deceleration
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2

    def create_overlay(self):
        # Create a Toplevel window for the overlay
        self.overlay = tk.Toplevel(self.parent)
        self.overlay.overrideredirect(True)  # Remove window decorations
        
        # Make it cover the parent window exactly
        x = self.parent.winfo_rootx()
        y = self.parent.winfo_rooty()
        w = self.parent.winfo_width()
        h = self.parent.winfo_height()
        self.overlay.geometry(f"{w}x{h}+{x}+{y}")
        
        # Create a frame inside the Toplevel with the fade color
        frame = tk.Frame(self.overlay, bg=self.fade_color)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Set initial transparency
        self.overlay.attributes('-alpha', 0.0)
        
        # Keep the overlay on top
        self.overlay.lift()
        self.overlay.attributes('-topmost', True)
        
        # Bind to parent's Configure event to keep overlay aligned
        self.parent.bind('<Configure>', self._update_overlay_position)
        
        return self.overlay

    def _update_overlay_position(self, event=None):
        if self.overlay:
            x = self.parent.winfo_rootx()
            y = self.parent.winfo_rooty()
            w = self.parent.winfo_width()
            h = self.parent.winfo_height()
            self.overlay.geometry(f"{w}x{h}+{x}+{y}")

    def fade_out(self, callback=None):
        def _fade_out(step=0):
            if step <= self.fade_steps:
                progress = step / self.fade_steps
                opacity = self._ease_in_out(progress)
                if self.overlay:
                    self.overlay.attributes('-alpha', opacity)
                    self._update_overlay_position()
                self.parent.after(self.fade_delay, lambda: _fade_out(step + 1))
            else:
                if callback:
                    self.parent.after(50, callback)  # Small pause at full opacity

        if not self.overlay:
            self.create_overlay()
        _fade_out()

    def fade_in(self, callback=None):
        def _fade_in(step=0):
            if step <= self.fade_steps:
                progress = step / self.fade_steps
                opacity = 1.0 - self._ease_in_out(progress)
                if self.overlay:
                    self.overlay.attributes('-alpha', opacity)
                    self._update_overlay_position()
                self.parent.after(self.fade_delay, lambda: _fade_in(step + 1))
            else:
                if self.overlay:
                    self.overlay.destroy()
                    self.overlay = None
                if callback:
                    callback()

        _fade_in()

class HeaderBar(ctk.CTkFrame):
    def __init__(self, parent, xp, points, streak):
        super().__init__(parent, height=40)  # Reduced height
        self.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.grid_columnconfigure(1, weight=1)  # Middle space expands

        # Logo and title
        title = ctk.CTkLabel(
            self,
            text="PencilSharp Learning",
            font=("Helvetica", 20, "bold"),  # Slightly smaller font
            text_color="#58cc02"
        )
        title.grid(row=0, column=0, padx=10)

        # Stats frame in header
        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=0, column=2, padx=10)

        # Stats in horizontal layout
        stats = [
            (f"🏆 {xp} XP", "xp"),
            (f"💎 {points}", "points"),
            (f"🔥 {streak}", "streak")
        ]

        for i, (text, _) in enumerate(stats):
            label = ctk.CTkLabel(
                stats_frame,
                text=text,
                font=("Helvetica", 12)  # Smaller font
            )
            label.grid(row=0, column=i, padx=5)

class TouchScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Bind mouse/touch events
        self.bind("<Button-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)
        
        # Initialize drag state
        self._drag_start = None
        self._scroll_start = None
        
    def _on_press(self, event):
        # Store initial position
        self._drag_start = (event.x, event.y)
        self._scroll_start = (self._parent_canvas.canvasx(0),
                            self._parent_canvas.canvasy(0))
    
    def _on_drag(self, event):
        if self._drag_start:
            # Calculate movement
            dx = event.x - self._drag_start[0]
            dy = event.y - self._drag_start[1]
            
            # Apply scrolling
            self._parent_canvas.canvasx(self._scroll_start[0] - dx)
            self._parent_canvas.yview_moveto(
                (self._scroll_start[1] - dy) / self._parent_canvas.winfo_height()
            )
    
    def _on_release(self, event):
        # Reset drag state
        self._drag_start = None
        self._scroll_start = None

class DraggableCard(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Bind mouse/touch events
        self.bind("<Button-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)
        
        # Initialize drag state
        self._drag_start = None
        self._original_pos = None
        self._is_dragging = False
        
    def _on_press(self, event):
        # Store initial position
        self._drag_start = (event.x_root, event.y_root)
        self._original_pos = self.winfo_x(), self.winfo_y()
        
        # Lift the card above other widgets
        self.lift()
        
        # Add dragging visual effect
        self.configure(border_width=2, border_color="#58cc02")
    
    def _on_drag(self, event):
        if self._drag_start:
            # Calculate movement
            dx = event.x_root - self._drag_start[0]
            dy = event.y_root - self._drag_start[1]
            
            # Update position
            self.place(x=self._original_pos[0] + dx,
                      y=self._original_pos[1] + dy)
            
            self._is_dragging = True
    
    def _on_release(self, event):
        if self._is_dragging:
            # Animate back to original position
            self._animate_return()
        
        # Reset drag state
        self._drag_start = None
        self._original_pos = None
        self._is_dragging = False
        
        # Remove dragging visual effect
        self.configure(border_width=2, border_color="#3b3b3b")
    
    def _animate_return(self, steps=10):
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
                self.place(x=current_x + dx * (step + 1),
                         y=current_y + dy * (step + 1))
                self.after(20, lambda: _step(step + 1))
            else:
                # Restore original grid position
                self.place_forget()
                self.grid(**self._original_grid_info)
        
        _step(0)

class SubjectCard(DraggableCard):
    def __init__(self, parent, subject, data, command):
        super().__init__(
            parent,
            fg_color="#2b2b2b",
            corner_radius=15,
            border_width=2,
            border_color="#3b3b3b"
        )
        
        # Store grid info for animation
        self._original_grid_info = None
        self.bind("<Map>", self._store_grid_info)
        
        # Create content frame with padding
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Center content vertically
        content_frame.grid_rowconfigure((0, 5), weight=1)  # Add weight to top and bottom rows
        
        # Icon with increased size
        icon_label = ctk.CTkLabel(
            content_frame,
            text=data["icon"],
            font=("Helvetica", 84),  # Increased font size
            text_color=data["color"]  # Use subject color for icon
        )
        icon_label.pack(pady=(0, 15))
        
        # Subject name with larger font
        subject_label = ctk.CTkLabel(
            content_frame,
            text=subject,
            font=("Helvetica", 28, "bold"),  # Increased font size
            text_color=data["color"]
        )
        subject_label.pack(pady=(0, 20))
        
        # Unit count with medium font
        unit_count = len(data["units"])
        units_label = ctk.CTkLabel(
            content_frame,
            text=f"{unit_count} Units",
            font=("Helvetica", 18),  # Increased font size
            text_color="#ffffff"
        )
        units_label.pack(pady=(0, 25))
        
        # Larger start button with hover effect
        self.start_button = ctk.CTkButton(
            content_frame,
            text="Start Learning",
            font=("Helvetica", 20),
            fg_color=data["color"],
            hover_color=self._adjust_color_brightness(data["color"], 0.8),  # Darker on hover
            command=command,
            width=240,  # Increased width
            height=50,  # Increased height
            corner_radius=25  # Rounded corners
        )
        self.start_button.pack(pady=(0, 0))
        
        # Store color for hover effect
        self._normal_color = "#2b2b2b"
        self._hover_color = "#323232"
    
    def _adjust_color_brightness(self, hex_color, factor):
        """Adjust the brightness of a hex color"""
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Adjust brightness
        new_rgb = tuple(min(int(c * factor), 255) for c in rgb)
        
        # Convert back to hex
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)
    
    def _on_hover(self, event):
        """Handle mouse hover"""
        self.configure(fg_color=self._hover_color)
    
    def _on_leave(self, event):
        """Handle mouse leave"""
        self.configure(fg_color=self._normal_color)
    
    def _store_grid_info(self, event):
        """Store grid information when the widget is mapped"""
        self._original_grid_info = self.grid_info()

class NavigationBar(ctk.CTkFrame):
    def __init__(self, parent, back_text, back_command, title_text, title_color=None):
        super().__init__(parent, fg_color="#1e1e1e", height=60)  # Darker background, taller height
        self.pack(fill='x', padx=0, pady=0)  # Remove padding to span full width
        
        # Create inner frame for content with padding
        inner_frame = ctk.CTkFrame(self, fg_color="transparent")
        inner_frame.pack(fill='x', padx=20, pady=10)
        
        # Configure grid weights
        inner_frame.grid_columnconfigure(1, weight=1)  # Title expands
        
        # Back button with improved styling
        back_button = ctk.CTkButton(
            inner_frame,
            text=f"← {back_text}",
            font=("Helvetica", 16),
            fg_color="#2d2d2d",  # Slightly lighter than background
            hover_color="#3d3d3d",  # Lighter on hover
            corner_radius=10,
            width=150,  # Fixed width
            height=35,  # Fixed height
            command=back_command
        )
        back_button.grid(row=0, column=0, padx=(0, 20))
        
        # Title with larger font
        header_label = ctk.CTkLabel(
            inner_frame,
            text=title_text,
            font=("Helvetica", 28, "bold"),
            text_color=title_color if title_color else "white"
        )
        header_label.grid(row=0, column=1, sticky="w")

class UnitSection(ctk.CTkFrame):
    def __init__(self, parent, unit, index, color, topic_callback):
        super().__init__(parent, fg_color="#2b2b2b", corner_radius=10)
        self.pack(fill='x', padx=20, pady=10)
        
        # Make the entire section draggable
        self.bind("<Button-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)
        
        # Initialize drag state
        self._drag_start = None
        self._scroll_start = None
        
        # Unit header with progress
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill='x', padx=15, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)  # Make middle space expand

        # Unit icon and label in one frame
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")

        unit_icon = ctk.CTkLabel(
            title_frame,
            text="📚",  # Unit icon
            font=("Helvetica", 24)
        )
        unit_icon.pack(side='left', padx=(0, 10))

        unit_label = ctk.CTkLabel(
            title_frame,
            text=f"Unit {index + 1}: {unit['name']}",
            font=("Helvetica", 20, "bold"),
            text_color=color
        )
        unit_label.pack(side='left')

        # Progress section
        progress_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        progress_frame.grid(row=0, column=2, sticky="e", padx=(10, 0))

        progress = ctk.CTkProgressBar(progress_frame, width=120)
        progress.pack(side='left', padx=10)
        progress.set(0)  # Set initial progress

        progress_text = ctk.CTkLabel(
            progress_frame,
            text="0%",
            font=("Helvetica", 14)
        )
        progress_text.pack(side='left')

        # Topics container with grid layout
        topics_frame = ctk.CTkFrame(self, fg_color="transparent")
        topics_frame.pack(fill='x', padx=15, pady=10)
        
        # Configure grid for topics (2 columns)
        topics_frame.grid_columnconfigure((0, 1), weight=1)

        # Create topic buttons in a grid
        for i, topic in enumerate(unit["topics"]):
            is_locked = index > 0 or i > 0  # Lock all topics except the first one in first unit
            row = i // 2  # Integer division for row number
            col = i % 2   # Remainder for column number
            self._create_topic_button(topics_frame, topic, row, col, is_locked, color, topic_callback)

    def _create_topic_button(self, parent, topic, row, col, locked, color, callback):
        # Create frame to hold icon and text
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)

        button = ctk.CTkButton(
            button_frame,
            text=f"{'🔒' if locked else '📖'} {topic}",
            font=("Helvetica", 16),
            fg_color="#3b3b3b" if locked else color,
            hover_color="#4b4b4b" if locked else self._adjust_color_brightness(color, 0.8),
            state="disabled" if locked else "normal",
            command=lambda: callback(topic) if not locked else None,
            height=40,  # Fixed height
            corner_radius=8
        )
        button.pack(fill='x', padx=5, pady=2)
    
    def _adjust_color_brightness(self, hex_color, factor):
        """Adjust the brightness of a hex color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(min(int(c * factor), 255) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)
    
    def _on_press(self, event):
        # Store initial position
        self._drag_start = event.y
        self._scroll_start = self.winfo_y()
        
        # Visual feedback
        self.configure(border_width=2, border_color="#58cc02")
    
    def _on_drag(self, event):
        if self._drag_start is not None:
            # Calculate movement
            dy = event.y - self._drag_start
            
            # Update position
            if self.winfo_parent():
                parent = self.nametowidget(self.winfo_parent())
                if isinstance(parent, (ctk.CTkScrollableFrame, TouchScrollableFrame)):
                    parent._parent_canvas.yview_scroll(-dy, "units")
    
    def _on_release(self, event):
        # Reset drag state
        self._drag_start = None
        self._scroll_start = None
        
        # Remove visual feedback
        self.configure(border_width=0)

class SidebarWidget(ctk.CTkFrame):
    def __init__(self, parent, league_data, progress_data):
        super().__init__(parent)
        # Remove pack() since we're using grid in the main window
        
        # Create a more compact layout using grid
        self.grid_columnconfigure(0, weight=1)
        
        # Profile section - Row 0
        profile_label = ctk.CTkLabel(
            self,
            text="Your Progress",
            font=("Helvetica", 18, "bold")  # Slightly smaller
        )
        profile_label.grid(row=0, column=0, pady=(5, 2), sticky="w", padx=5)

        # League section - Row 1
        league_frame = ctk.CTkFrame(self)
        league_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=2)
        league_frame.grid_columnconfigure(0, weight=1)

        # League info in horizontal layout
        league_label = ctk.CTkLabel(
            league_frame,
            text=f"{league_data['league']} League",
            font=("Helvetica", 14, "bold")  # Smaller font
        )
        league_label.grid(row=0, column=0, sticky="w", padx=5)

        rank_label = ctk.CTkLabel(
            league_frame,
            text=f"#{league_data['rank']}",
            font=("Helvetica", 12)  # Smaller font
        )
        rank_label.grid(row=0, column=1, sticky="e", padx=5)

        xp_label = ctk.CTkLabel(
            league_frame,
            text=f"{league_data['xp']} XP this week",
            font=("Helvetica", 11)  # Smaller font
        )
        xp_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=(0, 2))

        # Progress section - Row 2
        progress_frame = ctk.CTkFrame(self)
        progress_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=2)
        progress_frame.grid_columnconfigure(0, weight=1)

        progress_label = ctk.CTkLabel(
            progress_frame,
            text="Daily Goals",
            font=("Helvetica", 14, "bold")
        )
        progress_label.grid(row=0, column=0, sticky="w", padx=5, pady=(2, 0))

        progress = ctk.CTkProgressBar(progress_frame, width=150)  # Slightly narrower
        progress.grid(row=1, column=0, sticky="ew", padx=5, pady=2)
        progress.set(progress_data['progress'] / progress_data['goal'])

        quest_label = ctk.CTkLabel(
            progress_frame,
            text=f"{progress_data['progress']}/{progress_data['goal']} lessons",
            font=("Helvetica", 11)  # Smaller font
        )
        quest_label.grid(row=2, column=0, sticky="w", padx=5, pady=(0, 2))

        # Achievements section - Row 3
        achievements_frame = ctk.CTkFrame(self)
        achievements_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=2)
        achievements_frame.grid_columnconfigure(0, weight=1)

        achievement_label = ctk.CTkLabel(
            achievements_frame,
            text="Recent Achievements",
            font=("Helvetica", 14, "bold")
        )
        achievement_label.grid(row=0, column=0, sticky="w", padx=5, pady=(2, 1))

        achievements = [
            "🌟 First Lesson Completed",
            "📚 5 Topics Mastered",
            "🎯 Perfect Quiz Score"
        ]

        for i, achievement in enumerate(achievements):
            achievement_item = ctk.CTkLabel(
                achievements_frame,
                text=achievement,
                font=("Helvetica", 11)  # Smaller font
            )
            achievement_item.grid(row=i+1, column=0, sticky="w", padx=5, pady=1)

class LatexLabel(ctk.CTkLabel):
    def __init__(self, parent, latex_text, **kwargs):
        # Convert LaTeX to unicode math symbols where possible
        text = self._convert_to_unicode(latex_text)
        super().__init__(parent, text=text, font=("Helvetica", 14), **kwargs)
    
    def _convert_to_unicode(self, latex):
        # Basic LaTeX to Unicode conversions
        replacements = {
            "\\alpha": "α", "\\beta": "β", "\\gamma": "γ",
            "\\pm": "±", "\\times": "×", "\\div": "÷",
            "\\leq": "≤", "\\geq": "≥", "\\neq": "≠",
            "\\approx": "≈", "\\sqrt": "√", "\\infty": "∞",
            "^2": "²", "^3": "³", "^n": "ⁿ",
            "_1": "₁", "_2": "₂", "_3": "₃",
            "\\rightarrow": "→", "\\leftarrow": "←",
            "\\sum": "Σ", "\\prod": "∏",
            "\\frac": "/",  # Simplified fraction representation
        }
        
        result = latex
        
        # Remove $ signs
        result = result.replace("$", "")
        
        # Handle fractions specially
        if "\\frac" in result:
            # Extract numerator and denominator
            parts = result.split("\\frac{")
            for i in range(1, len(parts)):
                try:
                    num_end = parts[i].find("}")
                    numerator = parts[i][:num_end]
                    denom_start = parts[i].find("{", num_end)
                    denom_end = parts[i].find("}", denom_start)
                    denominator = parts[i][denom_start+1:denom_end]
                    rest = parts[i][denom_end+1:]
                    parts[i] = f"({numerator}/{denominator}){rest}"
                except:
                    continue
            result = "".join(parts)
        
        # Apply other replacements
        for tex, unicode in replacements.items():
            result = result.replace(tex, unicode)
        
        # Remove remaining curly braces
        result = result.replace("{", "").replace("}", "")
        
        return result

class MathText(ctk.CTkTextbox):
    def __init__(self, parent, height=30, **kwargs):
        super().__init__(parent, height=height, **kwargs)
        self.configure(state="disabled")
    
    def set_text(self, text):
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.insert("1.0", text)
        self.configure(state="disabled")

class LessonContent(ctk.CTkFrame):
    def __init__(self, master, topic, **kwargs):
        super().__init__(master, **kwargs)
        self.topic = topic
        self.temp_files = []  # Initialize temp_files list
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        self.learn_tab = self.tabview.add("Learn")
        self.practice_tab = self.tabview.add("Practice")
        self.quiz_tab = self.tabview.add("Quiz")
        
        # Create content for each tab
        self._create_learn_tab()
        self._create_practice_tab()
        self._create_quiz_tab()
        
    def _create_learn_tab(self):
        # Create a container frame
        container = ctk.CTkFrame(self.learn_tab)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create a button to open content in browser
        open_button = ctk.CTkButton(
            container,
            text="Open Content in Browser",
            command=lambda: self._open_content_in_browser("learn")
        )
        open_button.pack(pady=10)
        
        # Create HTML content with MathJax
        html_content = r"""
        <!DOCTYPE html>
        <html>
        <head>
            <script type="text/javascript" async
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
            </script>
            <style>
                body {
                    background-color: #2b2b2b;
                    color: #ffffff;
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                .content {
                    max-width: 800px;
                    margin: 0 auto;
                }
                h1 { color: #58cc02; }
                .equation { margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="content">
                <h1>Quadratic Equations</h1>
                
                <p>The standard form of a quadratic equation is:</p>
                <div class="equation">\[ax^2 + bx + c = 0\] where \(a \neq 0\)</div>
                
                <p>The quadratic formula for finding roots is:</p>
                <div class="equation">\[x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}\]</div>
                
                <h2>Properties:</h2>
                <ul>
                    <li>If \(b^2 - 4ac > 0\), there are two distinct real roots</li>
                    <li>If \(b^2 - 4ac = 0\), there is one repeated real root</li>
                    <li>If \(b^2 - 4ac < 0\), there are two complex conjugate roots</li>
                </ul>
                
                <h2>Example:</h2>
                <p>Solve: \(x^2 - 5x + 6 = 0\)</p>
                <p>Using the quadratic formula with \(a=1\), \(b=-5\), and \(c=6\):</p>
                <div class="equation">\[x = \frac{5 \pm \sqrt{25 - 24}}{2} = \frac{5 \pm 1}{2}\]</div>
                <p>Therefore, \(x = 3\) or \(x = 2\)</p>
            </div>
        </body>
        </html>
        """
        
        # Create temporary file for HTML content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_content)
            self.temp_files.append(f.name)
        
        # Create a preview textbox
        preview = ctk.CTkTextbox(container, wrap="word")
        preview.pack(fill="both", expand=True, padx=10, pady=10)
        preview.insert("1.0", "Click the button above to view the full content with properly rendered equations.")
        preview.configure(state="disabled")
        
    def _create_practice_tab(self):
        # Create a container frame
        container = ctk.CTkFrame(self.practice_tab)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create a button to open content in browser
        open_button = ctk.CTkButton(
            container,
            text="Open Content in Browser",
            command=lambda: self._open_content_in_browser("practice")
        )
        open_button.pack(pady=10)
        
        # Create HTML content with MathJax
        html_content = r"""
        <!DOCTYPE html>
        <html>
        <head>
            <script type="text/javascript" async
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
            </script>
            <style>
                body {
                    background-color: #2b2b2b;
                    color: #ffffff;
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                .content {
                    max-width: 800px;
                    margin: 0 auto;
                }
                h1 { color: #58cc02; }
                .equation { margin: 20px 0; }
                .options {
                    margin: 20px 0;
                    padding: 20px;
                    background-color: #3b3b3b;
                    border-radius: 10px;
                }
            </style>
        </head>
        <body>
            <div class="content">
                <h1>Practice Problems</h1>
                
                <p>Solve the quadratic equation:</p>
                <div class="equation">\[2x^2 - 7x + 3 = 0\]</div>
                
                <div class="options">
                    <h3>Choose the correct answer:</h3>
                    <ol>
                        <li>\[x = \frac{7 \pm \sqrt{49 - 24}}{4}\]</li>
                        <li>\[x = \frac{7 \pm \sqrt{49 - 12}}{4}\]</li>
                        <li>\[x = \frac{7 \pm \sqrt{49 - 48}}{4}\]</li>
                    </ol>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create temporary file for HTML content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_content)
            self.temp_files.append(f.name)
        
        # Create a preview textbox
        preview = ctk.CTkTextbox(container, wrap="word")
        preview.pack(fill="both", expand=True, padx=10, pady=10)
        preview.insert("1.0", "Click the button above to view the full content with properly rendered equations.")
        preview.configure(state="disabled")
        
    def _create_quiz_tab(self):
        # Create a container frame
        container = ctk.CTkFrame(self.quiz_tab)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create a button to open content in browser
        open_button = ctk.CTkButton(
            container,
            text="Open Content in Browser",
            command=lambda: self._open_content_in_browser("quiz")
        )
        open_button.pack(pady=10)
        
        # Create HTML content with MathJax
        html_content = r"""
        <!DOCTYPE html>
        <html>
        <head>
            <script type="text/javascript" async
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
            </script>
            <style>
                body {
                    background-color: #2b2b2b;
                    color: #ffffff;
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                .content {
                    max-width: 800px;
                    margin: 0 auto;
                }
                h1 { color: #58cc02; }
                .equation { margin: 20px 0; }
                .options {
                    margin: 20px 0;
                    padding: 20px;
                    background-color: #3b3b3b;
                    border-radius: 10px;
                }
            </style>
        </head>
        <body>
            <div class="content">
                <h1>Quiz</h1>
                
                <h2>1. What is the discriminant of a quadratic equation?</h2>
                
                <div class="options">
                    <h3>Select the correct formula:</h3>
                    <ol>
                        <li>\[b^2 - 4ac\]</li>
                        <li>\[b^2 + 4ac\]</li>
                        <li>\[-b \pm \sqrt{b^2 - 4ac}\]</li>
                    </ol>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create temporary file for HTML content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_content)
            self.temp_files.append(f.name)
        
        # Create a preview textbox
        preview = ctk.CTkTextbox(container, wrap="word")
        preview.pack(fill="both", expand=True, padx=10, pady=10)
        preview.insert("1.0", "Click the button above to view the full content with properly rendered equations.")
        preview.configure(state="disabled")
    
    def _open_content_in_browser(self, tab_name):
        import webbrowser
        # Open the corresponding HTML file in the default web browser
        index = {"learn": 0, "practice": 1, "quiz": 2}[tab_name]
        webbrowser.open(self.temp_files[index])
    
    def __del__(self):
        # Clean up temporary files
        for temp_file in self.temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass 