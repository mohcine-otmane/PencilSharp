import customtkinter as ctk
from PIL import Image
import os

class HeaderBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, height=60, fg_color="#1e2124", **kwargs)
        
        # Make the frame maintain its height
        self.pack_propagate(False)
        
        # Left section with logo and brand
        left_section = ctk.CTkFrame(self, fg_color="transparent")
        left_section.pack(side="left", padx=(20, 40))
        
        # Logo (you should replace this with your actual logo)
        logo_label = ctk.CTkLabel(
            left_section,
            text="E",  # Replace with actual logo image
            font=("Helvetica", 24, "bold"),
            text_color="#ffffff",
            width=40,
            height=40
        )
        logo_label.pack(side="left", padx=(0, 10))
        
        brand_label = ctk.CTkLabel(
            left_section,
            text="Ecourze",
            font=("Helvetica", 20, "bold"),
            text_color="#ffffff"
        )
        brand_label.pack(side="left")
        
        # Center section with navigation items
        nav_items = ["Dashboard", "Explore", "My Course", "Wallet", "Settings"]
        
        for item in nav_items:
            btn = ctk.CTkButton(
                self,
                text=item,
                font=("Helvetica", 14),
                fg_color="transparent",
                text_color="#ffffff" if item == "Dashboard" else "#8a8d93",
                hover_color="#2a2b30",
                width=100,
                height=40
            )
            btn.pack(side="left", padx=5)
        
        # Right section with notifications and profile
        right_section = ctk.CTkFrame(self, fg_color="transparent")
        right_section.pack(side="right", padx=20)
        
        # Notification button
        notif_btn = ctk.CTkButton(
            right_section,
            text="🔔",  # Replace with actual icon
            font=("Helvetica", 16),
            fg_color="transparent",
            hover_color="#2a2b30",
            width=40,
            height=40
        )
        notif_btn.pack(side="left", padx=10)
        
        # Search button
        search_btn = ctk.CTkButton(
            right_section,
            text="🔍",  # Replace with actual icon
            font=("Helvetica", 16),
            fg_color="transparent",
            hover_color="#2a2b30",
            width=40,
            height=40
        )
        search_btn.pack(side="left", padx=10)
        
        # Profile section
        profile_frame = ctk.CTkFrame(right_section, fg_color="transparent")
        profile_frame.pack(side="left", padx=10)
        
        # Profile image (circular frame)
        profile_img = ctk.CTkFrame(
            profile_frame,
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#2a2b30"
        )
        profile_img.pack(side="left")
        profile_img.pack_propagate(False)
        
        # Profile name
        profile_name = ctk.CTkLabel(
            profile_frame,
            text="James Smith",
            font=("Helvetica", 14),
            text_color="#ffffff"
        )
        profile_name.pack(side="left", padx=10) 