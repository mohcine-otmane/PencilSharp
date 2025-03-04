import customtkinter as ctk
from src.utils.theme import theme
from src.views.widgets.latex_viewer import LaTeXViewer

class LearningView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Create main content area
        self.content_area = ctk.CTkFrame(
            self,
            fg_color=theme.colors.surface
        )
        self.content_area.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Create tabs for different modes
        self.tab_frame = ctk.CTkFrame(
            self.content_area,
            fg_color="transparent"
        )
        self.tab_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        self.tabs = {}
        for mode in ["Learn", "Practice", "Quiz"]:
            self.tabs[mode] = ctk.CTkButton(
                self.tab_frame,
                text=mode,
                width=120,
                height=32,
                corner_radius=16,
                fg_color=theme.colors.primary if mode == "Learn" else "transparent",
                text_color="#ffffff" if mode == "Learn" else theme.colors.text,
                command=lambda m=mode: self._switch_mode(m)
            )
            self.tabs[mode].pack(side="left", padx=5)
        
        # Create LaTeX viewer
        self.latex_viewer = LaTeXViewer(self.content_area)
        self.latex_viewer.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Load sample content
        self.load_sample_content()
        
    def _switch_mode(self, mode):
        """Switch between learning modes"""
        for tab_mode, tab in self.tabs.items():
            if tab_mode == mode:
                tab.configure(
                    fg_color=theme.colors.primary,
                    text_color="#ffffff"
                )
            else:
                tab.configure(
                    fg_color="transparent",
                    text_color=theme.colors.text
                )
        
        # Load appropriate content for the mode
        if mode == "Learn":
            self.load_sample_content()
        elif mode == "Practice":
            self.load_practice_content()
        else:  # Quiz
            self.load_quiz_content()
            
    def load_sample_content(self):
        """Load sample mathematics content"""
        content = """
        <h1>Introduction to Numbers</h1>
        
        <div class="theorem">
            <h3>Definition</h3>
            <p>A number is a mathematical object used to count, measure, and label. The main types of numbers include:</p>
            <ul>
                <li>Natural Numbers (ℕ)</li>
                <li>Integers (ℤ)</li>
                <li>Rational Numbers (ℚ)</li>
                <li>Real Numbers (ℝ)</li>
            </ul>
        </div>
        
        <div class="example">
            <h3>Example: Quadratic Formula</h3>
            <p>The quadratic formula is used to solve quadratic equations of the form ax² + bx + c = 0:</p>
            $$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$
            <p>This formula gives us the x-coordinates of where a parabola crosses the x-axis.</p>
        </div>
        
        <div class="note">
            <h3>Properties of Real Numbers</h3>
            <p>For any real numbers a, b, and c:</p>
            <ul>
                <li>Commutative Property: $a + b = b + a$ and $a \\times b = b \\times a$</li>
                <li>Associative Property: $(a + b) + c = a + (b + c)$</li>
                <li>Distributive Property: $a(b + c) = ab + ac$</li>
            </ul>
        </div>
        
        <h2>Complex Numbers</h2>
        <p>A complex number is a number that can be expressed in the form:</p>
        $$z = a + bi$$
        <p>where $a$ and $b$ are real numbers, and $i$ is the imaginary unit with the property $i^2 = -1$.</p>
        """
        self.latex_viewer.load_content(content)
        
    def load_practice_content(self):
        """Load practice problems"""
        content = """
        <h1>Practice Problems</h1>
        
        <div class="example">
            <h3>Problem 1</h3>
            <p>Solve the quadratic equation:</p>
            $$x^2 - 5x + 6 = 0$$
            <div class="note">
                <p>Hint: Use the quadratic formula or factoring.</p>
            </div>
        </div>
        
        <div class="example">
            <h3>Problem 2</h3>
            <p>Simplify the following expression:</p>
            $$\\frac{x^2 - 4}{x - 2}$$
            <div class="note">
                <p>Hint: Factor the numerator.</p>
            </div>
        </div>
        """
        self.latex_viewer.load_content(content)
        
    def load_quiz_content(self):
        """Load quiz questions"""
        content = """
        <h1>Quiz: Numbers and Operations</h1>
        
        <div class="example">
            <h3>Question 1</h3>
            <p>What is the solution to the equation:</p>
            $$2x^2 + 7x + 3 = 0$$
            <ol>
                <li>$x = -3$ and $x = -\\frac{1}{2}$</li>
                <li>$x = 3$ and $x = \\frac{1}{2}$</li>
                <li>$x = -3$ and $x = \\frac{1}{2}$</li>
                <li>$x = 3$ and $x = -\\frac{1}{2}$</li>
            </ol>
        </div>
        
        <div class="example">
            <h3>Question 2</h3>
            <p>If $z = 3 + 4i$, what is $|z|$?</p>
            <ol>
                <li>$5$</li>
                <li>$7$</li>
                <li>$25$</li>
                <li>$\\sqrt{25}$</li>
            </ol>
        </div>
        """
        self.latex_viewer.load_content(content)