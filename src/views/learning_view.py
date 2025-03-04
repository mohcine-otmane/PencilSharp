import customtkinter as ctk
from tkinterweb import HtmlFrame

class LearningView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Create tabs for different learning modes
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True)
        
        # Add tabs
        self.tab_view.add("Learn")
        self.tab_view.add("Practice")
        self.tab_view.add("Quiz")
        
        # Learn tab content
        learn_frame = ctk.CTkFrame(self.tab_view.tab("Learn"), fg_color="transparent")
        learn_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        learn_label = ctk.CTkLabel(
            learn_frame,
            text="Learning content will appear here",
            font=("Helvetica", 16)
        )
        learn_label.pack(pady=20)
        
        # Practice tab content
        practice_frame = ctk.CTkFrame(self.tab_view.tab("Practice"), fg_color="transparent")
        practice_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        practice_label = ctk.CTkLabel(
            practice_frame,
            text="Practice problems will appear here",
            font=("Helvetica", 16)
        )
        practice_label.pack(pady=20)
        
        # Quiz tab content
        quiz_frame = ctk.CTkFrame(self.tab_view.tab("Quiz"), fg_color="transparent")
        quiz_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        quiz_label = ctk.CTkLabel(
            quiz_frame,
            text="Quiz questions will appear here",
            font=("Helvetica", 16)
        )
        quiz_label.pack(pady=20)
        
        # Content viewer with LaTeX support
        self.content_frame = ctk.CTkFrame(self, fg_color="#2a2b30")
        self.content_frame.pack(fill="both", expand=True)
        
        self.html_viewer = HtmlFrame(self.content_frame)
        self.html_viewer.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Load MathJax for LaTeX rendering
        self.load_mathjax()
        
        # Show initial content
        self.show_sample_content()
    
    def load_mathjax(self):
        """Load MathJax configuration for LaTeX rendering"""
        mathjax_config = """
        <script>
        MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
            }
        };
        </script>
        <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        """
        self.html_viewer.add_html(mathjax_config)
    
    def show_sample_content(self):
        """Show sample learning content with LaTeX"""
        content = """
        <div style="font-family: Arial, sans-serif; color: #ffffff; line-height: 1.6;">
            <h1>Introduction to Quadratic Equations</h1>
            
            <p>A quadratic equation is a polynomial equation of degree 2. The standard form is:</p>
            
            <p style="text-align: center; font-size: 1.2em;">
                $$ax^2 + bx + c = 0$$
            </p>
            
            <p>where:</p>
            <ul>
                <li>$a \\neq 0$ (if $a = 0$ it becomes a linear equation)</li>
                <li>$b$ and $c$ can be any real number</li>
            </ul>
            
            <h2>The Quadratic Formula</h2>
            
            <p>The solutions to a quadratic equation can be found using the quadratic formula:</p>
            
            <p style="text-align: center; font-size: 1.2em;">
                $$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$
            </p>
            
            <p>The term under the square root ($b^2 - 4ac$) is called the discriminant.</p>
        </div>
        """
        self.html_viewer.load_html(content)
    
    def show_practice_content(self):
        """Show practice problems with LaTeX"""
        content = """
        <div style="font-family: Arial, sans-serif; color: #ffffff; line-height: 1.6;">
            <h1>Practice Problems</h1>
            
            <p>Solve the following quadratic equations:</p>
            
            <ol>
                <li>
                    $$x^2 + 5x + 6 = 0$$
                    <button onclick="showSolution(1)">Show Solution</button>
                    <div id="solution1" style="display: none;">
                        Solution: $x = -2$ or $x = -3$
                    </div>
                </li>
                
                <li>
                    $$2x^2 - 7x + 3 = 0$$
                    <button onclick="showSolution(2)">Show Solution</button>
                    <div id="solution2" style="display: none;">
                        Solution: $x = 3$ or $x = \\frac{1}{2}$
                    </div>
                </li>
            </ol>
        </div>
        
        <script>
        function showSolution(n) {
            document.getElementById('solution' + n).style.display = 'block';
        }
        </script>
        """
        self.html_viewer.load_html(content)
    
    def show_quiz_content(self):
        """Show quiz questions with LaTeX"""
        content = """
        <div style="font-family: Arial, sans-serif; color: #ffffff; line-height: 1.6;">
            <h1>Quiz: Quadratic Equations</h1>
            
            <form id="quiz">
                <p>1. What is the discriminant of the equation $x^2 + 4x + 4 = 0$?</p>
                <input type="radio" name="q1" value="a"> $b^2 - 4ac = 16 - 16 = 0$<br>
                <input type="radio" name="q1" value="b"> $b^2 - 4ac = 16 - 8 = 8$<br>
                <input type="radio" name="q1" value="c"> $b^2 - 4ac = 8 - 16 = -8$<br>
                
                <p>2. For what value of $k$ will the equation $x^2 + kx + 4 = 0$ have equal roots?</p>
                <input type="radio" name="q2" value="a"> $k = \\pm 4$<br>
                <input type="radio" name="q2" value="b"> $k = \\pm 2$<br>
                <input type="radio" name="q2" value="c"> $k = 4$<br>
                
                <button type="button" onclick="checkAnswers()">Submit</button>
            </form>
        </div>
        
        <script>
        function checkAnswers() {
            alert('Quiz submitted! Your answers have been recorded.');
        }
        </script>
        """
        self.html_viewer.load_html(content)