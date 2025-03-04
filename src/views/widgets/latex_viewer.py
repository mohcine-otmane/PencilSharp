import customtkinter as ctk
import tkinterweb
from src.utils.theme import theme
import os

class LaTeXViewer(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Create HTML viewer widget
        self.html_viewer = tkinterweb.HtmlFrame(self, messages_enabled=False)
        self.html_viewer.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Load MathJax configuration
        self.mathjax_config = """
        <script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
        </script>
        <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [['$','$'], ['\\\\(','\\\\)']],
                displayMath: [['$$','$$'], ['\\\\[','\\\\]']],
                processEscapes: true
            },
            "HTML-CSS": { 
                availableFonts: ["TeX"],
                scale: 130
            }
        });
        </script>
        """
        
        # Base HTML template
        self.html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            {mathjax}
            <style>
                body {{
                    background-color: #1a1b1e;
                    color: #ffffff;
                    font-family: system-ui, -apple-system, sans-serif;
                    line-height: 1.6;
                    padding: 20px;
                    font-size: 16px;
                }}
                .MathJax {{
                    color: #ffffff !important;
                }}
                .content {{
                    max-width: 800px;
                    margin: 0 auto;
                }}
                h1, h2, h3 {{
                    color: #8a8d93;
                    margin-top: 1.5em;
                    margin-bottom: 0.5em;
                }}
                .example {{
                    background-color: #2a2b2e;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 15px 0;
                }}
                .theorem {{
                    border-left: 4px solid #6366f1;
                    padding-left: 15px;
                    margin: 15px 0;
                }}
                .note {{
                    background-color: #2d3748;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 15px 0;
                }}
                p {{
                    margin: 1em 0;
                }}
                ul, ol {{
                    margin: 1em 0;
                    padding-left: 2em;
                }}
                li {{
                    margin: 0.5em 0;
                }}
            </style>
        </head>
        <body>
            <div class="content">
                {content}
            </div>
        </body>
        </html>
        """
        
    def load_content(self, content):
        """Load LaTeX content into the viewer"""
        try:
            # Format the content with the template
            html_content = self.html_template.format(
                mathjax=self.mathjax_config,
                content=content
            )
            
            # Load the content into the viewer
            self.html_viewer.load_html(html_content)
        except Exception as e:
            print(f"Error loading content: {e}")
            self.html_viewer.load_html(f"<p>Error loading content: {str(e)}</p>")
            
    def load_file(self, file_path):
        """Load content from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.load_content(content)
        except Exception as e:
            print(f"Error loading file: {e}")
            self.load_content(f"<p>Error loading content: {str(e)}</p>")
            
    def clear(self):
        """Clear the viewer content"""
        self.load_content("") 