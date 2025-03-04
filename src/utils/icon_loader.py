import os
import requests
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import customtkinter as ctk
from io import BytesIO
import base64

class IconLoader:
    ICON_URLS = {
        "math": "https://raw.githubusercontent.com/Templarian/MaterialDesign/master/svg/calculator-variant.svg",
        "science": "https://raw.githubusercontent.com/Templarian/MaterialDesign/master/svg/flask-round-bottom.svg",
        "language": "https://raw.githubusercontent.com/Templarian/MaterialDesign/master/svg/book-open-page-variant.svg",
        "social": "https://raw.githubusercontent.com/Templarian/MaterialDesign/master/svg/earth.svg",
        "computer": "https://raw.githubusercontent.com/Templarian/MaterialDesign/master/svg/laptop-account.svg",
        "foreign": "https://raw.githubusercontent.com/Templarian/MaterialDesign/master/svg/translate-variant.svg"
    }
    
    def __init__(self):
        self.icon_cache = {}
        self.icon_dir = os.path.join("src", "assets", "icons")
        os.makedirs(self.icon_dir, exist_ok=True)
        
    def save_custom_icon(self, image_data, icon_name):
        """Save a custom icon from image data"""
        local_path = os.path.join(self.icon_dir, f"{icon_name}.png")
        
        # Convert the image to RGBA mode to ensure transparency support
        image = Image.open(BytesIO(image_data))
        image = image.convert("RGBA")
        
        # Save the processed image
        image.save(local_path, "PNG")
        return local_path
        
    def get_custom_icon(self, icon_path, size=64):
        """Get a CTkImage from a custom icon file"""
        cache_key = (icon_path, size)
        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]
            
        try:
            # Load and process the image
            image = Image.open(icon_path)
            image = image.convert("RGBA")
            
            # Create a square canvas with the target size
            canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            
            # Calculate scaling while maintaining aspect ratio
            scale = min(size / image.width, size / image.height)
            new_size = (int(image.width * scale), int(image.height * scale))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Calculate position to center the image
            x = (size - new_size[0]) // 2
            y = (size - new_size[1]) // 2
            
            # Paste the image onto the canvas
            canvas.paste(image, (x, y), image)
            
            # Create CTkImage
            ctk_image = ctk.CTkImage(
                light_image=canvas,
                dark_image=canvas,
                size=(size, size)
            )
            
            # Cache the image
            self.icon_cache[cache_key] = ctk_image
            return ctk_image
            
        except Exception as e:
            print(f"Error loading custom icon: {e}")
            return None
        
    def download_icon(self, icon_type):
        """Download an SVG icon and save it locally"""
        if icon_type not in self.ICON_URLS:
            raise ValueError(f"Unknown icon type: {icon_type}")
            
        url = self.ICON_URLS[icon_type]
        local_path = os.path.join(self.icon_dir, f"{icon_type}.svg")
        
        # Download if not exists
        if not os.path.exists(local_path):
            response = requests.get(url)
            response.raise_for_status()
            
            # Clean up SVG content to ensure proper rendering
            svg_content = response.content.decode('utf-8')
            svg_content = svg_content.replace('fill="currentColor"', 'fill="#ffffff"')
            
            with open(local_path, "w", encoding='utf-8') as f:
                f.write(svg_content)
                
        return local_path
        
    def get_icon(self, icon_type, size=64, color="#ffffff"):
        """Get a CTkImage for the specified icon type"""
        cache_key = (icon_type, size, color)
        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]
            
        # Download or get local SVG
        svg_path = self.download_icon(icon_type)
        
        try:
            # Convert SVG to PNG using svglib
            drawing = svg2rlg(svg_path)
            
            # Scale the drawing while maintaining aspect ratio
            scale = size / max(drawing.width, drawing.height)
            drawing.width *= scale
            drawing.height *= scale
            
            # Center the drawing in a square canvas
            png_data = BytesIO()
            renderPM.drawToFile(drawing, png_data, fmt="PNG")
            
            # Load and process the image
            image = Image.open(png_data)
            
            # Create a square canvas with the target size
            canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            
            # Calculate position to center the image
            x = (size - image.width) // 2
            y = (size - image.height) // 2
            
            # Paste the image onto the canvas
            canvas.paste(image, (x, y), image)
            
            # Create CTkImage
            ctk_image = ctk.CTkImage(
                light_image=canvas,
                dark_image=canvas,
                size=(size, size)
            )
            
            # Cache the image
            self.icon_cache[cache_key] = ctk_image
            return ctk_image
            
        except Exception as e:
            print(f"Error loading icon {icon_type}: {e}")
            return None

# Create a global instance
icon_loader = IconLoader() 