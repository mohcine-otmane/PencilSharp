# PencilSharp Learning Platform

A modern, interactive learning platform with support for mathematics, science, and other subjects.

## Features

- 📚 Interactive learning interface with dark theme
- ⚡ Real-time LaTeX rendering for mathematical content
- 🎯 Three learning modes: Learn, Practice, and Quiz
- 📱 Touch-friendly scrollable interface
- 🎨 Beautiful subject cards with animations
- 📝 Rich content formatting with theorems, examples, and notes
- 🌙 Dark mode optimized for comfortable reading

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PencilSharp.git
cd PencilSharp
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python pencilsharp_gui.py
```

## Project Structure

```
PencilSharp/
├── src/
│   ├── views/          # UI components and views
│   ├── controllers/    # Business logic
│   ├── models/         # Data models
│   ├── utils/          # Utility functions
│   └── assets/         # Static assets
├── config/             # Configuration files
├── tests/              # Test files
├── pencilsharp_gui.py  # Main application
└── requirements.txt    # Dependencies
```

## Features in Detail

### LaTeX Support
- Real-time rendering of mathematical equations
- Support for inline and display math
- Custom styling for dark theme
- MathJax integration

### Learning Modes
1. **Learn Mode**
   - Structured content presentation
   - Interactive examples
   - Theorem boxes and notes

2. **Practice Mode**
   - Problem sets with hints
   - Step-by-step solutions
   - Progress tracking

3. **Quiz Mode**
   - Multiple choice questions
   - Immediate feedback
   - Score tracking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 