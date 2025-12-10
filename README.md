# TaskLang Compiler

A production-ready compiler for TaskLang, a domain-specific language designed for browser automation and task scripting.

## Overview

TaskLang Compiler is a Python-based compiler that transforms TaskLang scripts (`.task` files) into executable Python automation code. It provides a simple, intuitive syntax for automating web browser interactions and system tasks.

## Features

- **Simple Syntax**: Clean, readable syntax for automation tasks
- **Multi-Browser Support**: Support for Chrome, Firefox, Edge, and Safari
- **Dynamic Element Selection**: Select elements by ID, name, XPath, CSS selector, or tag name
- **Web Navigation**: Navigate to URLs and interact with web pages
- **Input Handling**: Type text and simulate keyboard input
- **Click Support**: Click on any element using various selectors
- **Screenshot Capture**: Capture screenshots during automation
- **Wait Commands**: Control timing and synchronization
- **Script Selector**: Interactive script selector for easy script management
- **Modular Architecture**: Well-structured codebase with separate modules for lexing, parsing, semantic analysis, IR generation, and code generation

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository** (or navigate to the project directory):

   ```bash
   cd tasklang-compiler
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Compiler

### Basic Usage

Run the compiler with a `.task` file:

```bash
python -m src.main <filename.task>
```

### Example

Compile the demo script:

```bash
python -m src.main examples/demo.task
```

## Example Usage

### Sample TaskLang Script

Create a file `examples/demo.task`:

```
open chrome
go https://google.com/
type "compiler project" in name "q"
enter in name "q"
wait 2
screenshot test.png
close
```

### Running the Example

**Option 1: Use the GUI Application (Recommended)** 🖥️

```bash
python run_gui.py
```

**Option 2: Compile a specific script**

```bash
python -m src.main examples/demo.task
```

**Option 3: Use the interactive script selector**

```bash
python run_scripts.py
```

This will:

1. Display all available scripts in the `examples/` directory
2. Let you select a script interactively
3. Compile the selected script to Python
4. Generate executable Python code in the `output/` directory

### TaskLang Syntax

**Browser Commands:**

- `open chrome` - Open Chrome browser (also supports: firefox, edge, safari)
- `go <url>` - Navigate to a URL
- `close` - Close the browser

**Element Interaction:**

- `type "text" [in selector_type "value"]` - Type text into an element
- `click [selector_type "value"]` - Click an element
- `enter [in selector_type "value"]` - Press Enter in an element

**Selector Types:**

- `id "value"` - Select by element ID
- `name "value"` - Select by name attribute
- `css "selector"` - Select by CSS selector
- `xpath "//path"` - Select by XPath
- `tag "tagname"` - Select by tag name

**Other Commands:**

- `wait <seconds>` - Wait for specified seconds
- `screenshot <filename>` - Take a screenshot

### Example Scripts

The `examples/` directory contains several example scripts:

- `demo.task` - Basic Google search example
- `google_search.task` - Google search with selectors
- `github_search.task` - GitHub search example
- `wikipedia.task` - Wikipedia search example
- `youtube_search.task` - YouTube search example
- `simple_navigation.task` - Simple page navigation

## Project Structure

```
tasklang-compiler/
├── src/                    # Source code
│   ├── lexer/             # Lexical analysis
│   ├── parser/            # Syntax parsing
│   ├── semantic/          # Semantic analysis
│   ├── ir/                # Intermediate representation
│   ├── codegen/           # Code generation
│   ├── runtime/           # Runtime execution
│   └── main.py            # Entry point
├── tests/                 # Test suite
│   ├── lexer/            # Lexer tests
│   ├── parser/           # Parser tests
│   └── integration/      # Integration tests
├── examples/             # Example TaskLang scripts
│   └── demo.task         # Demo script
├── output/               # Generated output files
│   └── demo.py           # Generated Python code
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .gitignore           # Git ignore rules
```

## Dependencies

- **selenium**: Browser automation framework
- **pyautogui**: GUI automation library
- **lark**: Parsing toolkit for building parsers
- **rich**: Rich text and beautiful formatting in the terminal
- **pytest**: Testing framework

## Development Status

✅ **Fully Functional**: The compiler is complete and ready to use! All core features are implemented and tested.

## Contributing

Contributions are welcome! Please ensure that:

- Code follows PEP 8 style guidelines
- Tests are added for new features
- Documentation is updated accordingly

## License

[Add your license here]

## Author

[Add author information here]
