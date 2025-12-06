# TaskLang Compiler

A production-ready compiler for TaskLang, a domain-specific language designed for browser automation and task scripting.

## Overview

TaskLang Compiler is a Python-based compiler that transforms TaskLang scripts (`.task` files) into executable Python automation code. It provides a simple, intuitive syntax for automating web browser interactions and system tasks.

## Features

- **Simple Syntax**: Clean, readable syntax for automation tasks
- **Browser Automation**: Built-in support for Chrome browser automation
- **Web Navigation**: Navigate to URLs and interact with web pages
- **Input Handling**: Type text and simulate keyboard input
- **Screenshot Capture**: Capture screenshots during automation
- **Wait Commands**: Control timing and synchronization
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
go https://google.com  
type "compiler project"  
enter  
wait 2  
screenshot test.png  
```

### Running the Example

```bash
python -m src.main examples/demo.task
```

This will:
1. Validate the file exists
2. Process the TaskLang script
3. Generate executable Python code (once implementation is complete)

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

🚧 **Under Development**: The project structure is set up, but lexer, parser, and execution logic are not yet implemented. This is the initial project setup phase.

## Contributing

Contributions are welcome! Please ensure that:
- Code follows PEP 8 style guidelines
- Tests are added for new features
- Documentation is updated accordingly

## License

[Add your license here]

## Author

[Add author information here]

