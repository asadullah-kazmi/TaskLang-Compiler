# TaskLang Compiler - File Structure & Commands Guide

## 📁 Project Structure

```
tasklang-compiler/
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Entry point
│   ├── cli.py                   # Command-line interface
│   │
│   ├── lexer/                   # Lexical analysis
│   │   ├── __init__.py
│   │   ├── token.py            # Token class definition
│   │   └── lexer.py            # Lexer implementation
│   │
│   ├── parser/                  # Syntax parsing
│   │   ├── __init__.py
│   │   ├── ast.py              # AST node classes
│   │   └── parser.py           # Recursive descent parser
│   │
│   ├── semantic/                # Semantic analysis
│   │   ├── __init__.py
│   │   └── analyzer.py         # Semantic analyzer
│   │
│   ├── codegen/                 # Code generation
│   │   ├── __init__.py
│   │   └── python_gen.py       # Python code generator
│   │
│   ├── ir/                      # Intermediate representation (future)
│   │   └── __init__.py
│   │
│   └── runtime/                  # Runtime (future)
│       └── __init__.py
│
├── tests/                       # Test suite
│   ├── lexer/
│   │   └── test_lexer.py       # Lexer unit tests
│   ├── parser/
│   │   └── test_parser.py     # Parser unit tests
│   ├── semantic/
│   │   └── test_semantic.py   # Semantic analyzer tests
│   └── integration/            # Integration tests (future)
│
├── examples/                    # Example TaskLang scripts
│   └── demo.task               # Demo automation script
│
├── output/                      # Generated Python files
│   ├── demo.py                 # Generated from demo.task
│   └── test_full.py            # Generated test file
│
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Git ignore rules
```

---

## 🚀 Commands by File Name

### **Main Entry Point**

#### `src/main.py`
**Purpose**: Entry point for the compiler

**Command to run compiler:**
```bash
python -m src.main examples/demo.task
```

**Command with custom output:**
```bash
python -m src.main examples/demo.task --output my_output
python -m src.main examples/demo.task -o my_output
```

**Command to show help:**
```bash
python -m src.main --help
```

---

### **CLI Module**

#### `src/cli.py`
**Purpose**: Command-line interface orchestrator

**Direct import (for testing):**
```python
from src.cli import TaskLangCLI
cli = TaskLangCLI()
cli.run()
```

---

### **Lexer Module**

#### `src/lexer/token.py`
**Purpose**: Token class definition

**Test command:**
```bash
python -m pytest tests/lexer/test_lexer.py -v
```

#### `src/lexer/lexer.py`
**Purpose**: Lexical analyzer implementation

**Test command:**
```bash
python -m pytest tests/lexer/test_lexer.py::TestLexer -v
```

**Direct usage:**
```python
from src.lexer.lexer import Lexer
lexer = Lexer(source_code)
tokens = lexer.tokenize()
```

---

### **Parser Module**

#### `src/parser/ast.py`
**Purpose**: Abstract Syntax Tree node classes

**Test command:**
```bash
python -m pytest tests/parser/test_parser.py -v
```

#### `src/parser/parser.py`
**Purpose**: Recursive descent parser

**Test command:**
```bash
python -m pytest tests/parser/test_parser.py::TestParser -v
```

**Direct usage:**
```python
from src.parser.parser import Parser
parser = Parser(tokens)
ast = parser.parse()
```

---

### **Semantic Analyzer Module**

#### `src/semantic/analyzer.py`
**Purpose**: Semantic analysis and validation

**Test command:**
```bash
python -m pytest tests/semantic/test_semantic.py -v
```

**Direct usage:**
```python
from src.semantic.analyzer import SemanticAnalyzer
analyzer = SemanticAnalyzer(ast)
analyzer.analyze()
```

---

### **Code Generator Module**

#### `src/codegen/python_gen.py`
**Purpose**: Python Selenium code generation

**Direct usage:**
```python
from src.codegen.python_gen import PythonCodeGenerator
generator = PythonCodeGenerator(ast)
generator.generate("output/demo.py")
```

---

### **Example Files**

#### `examples/demo.task`
**Purpose**: Sample TaskLang script

**Compile command:**
```bash
python -m src.main examples/demo.task
```

**View file:**
```bash
cat examples/demo.task        # Linux/Mac
type examples\demo.task     # Windows
Get-Content examples\demo.task  # PowerShell
```

---

### **Generated Output Files**

#### `output/demo.py`
**Purpose**: Generated Python automation script

**Run generated script:**
```bash
python output/demo.py
```

**View generated file:**
```bash
cat output/demo.py           # Linux/Mac
type output\demo.py          # Windows
Get-Content output\demo.py   # PowerShell
```

---

## 🧪 Testing Commands

### Run all tests:
```bash
python -m pytest tests/ -v
```

### Run specific test file:
```bash
python -m pytest tests/lexer/test_lexer.py -v
python -m pytest tests/parser/test_parser.py -v
python -m pytest tests/semantic/test_semantic.py -v
```

### Run specific test class:
```bash
python -m pytest tests/lexer/test_lexer.py::TestLexer -v
```

### Run with coverage:
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

---

## 📦 Installation Commands

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Install specific package:
```bash
pip install selenium
pip install pytest
```

---

## 🔍 File Inspection Commands

### View Python file:
```bash
# Windows PowerShell
Get-Content src/main.py
Get-Content src/cli.py

# Windows CMD
type src\main.py
type src\cli.py

# Linux/Mac
cat src/main.py
cat src/cli.py
```

### Count lines in file:
```bash
# PowerShell
(Get-Content src/main.py).Count

# Linux/Mac
wc -l src/main.py
```

### Search in files:
```bash
# PowerShell
Select-String -Path "src/**/*.py" -Pattern "class"

# Linux/Mac
grep -r "class" src/
```

---

## 🗑️ Cleanup Commands

### Remove generated files:
```bash
# Windows PowerShell
Remove-Item output/*.py

# Linux/Mac
rm output/*.py
```

### Remove Python cache:
```bash
# Windows PowerShell
Get-ChildItem -Path . -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force

# Linux/Mac
find . -type d -name "__pycache__" -exec rm -r {} +
find . -name "*.pyc" -delete
```

---

## 📊 Compilation Pipeline Commands

### Full compilation workflow:
```bash
# Step 1: Compile .task file
python -m src.main examples/demo.task

# Step 2: Run generated Python script
python output/demo.py
```

### Compile with verbose output (already included):
```bash
python -m src.main examples/demo.task
# Output shows:
# - Tokens
# - AST
# - Semantic analysis result
# - Generated file location
```

---

## 🔧 Development Commands

### Check Python syntax:
```bash
python -m py_compile src/main.py
python -m py_compile src/cli.py
```

### Lint code (if pylint/flake8 installed):
```bash
pylint src/
flake8 src/
```

### Format code (if black installed):
```bash
black src/
```

---

## 📝 Quick Reference

| File | Purpose | Command |
|------|---------|---------|
| `src/main.py` | Entry point | `python -m src.main <file.task>` |
| `src/cli.py` | CLI orchestrator | Imported by main.py |
| `src/lexer/lexer.py` | Tokenizer | Used internally |
| `src/parser/parser.py` | Parser | Used internally |
| `src/semantic/analyzer.py` | Validator | Used internally |
| `src/codegen/python_gen.py` | Code generator | Used internally |
| `examples/demo.task` | Example script | `python -m src.main examples/demo.task` |
| `output/demo.py` | Generated code | `python output/demo.py` |

---

## 🎯 Common Workflows

### 1. Create and compile new TaskLang file:
```bash
# Create file
echo 'open chrome' > my_script.task
echo 'go https://example.com' >> my_script.task

# Compile
python -m src.main my_script.task

# Run
python output/my_script.py
```

### 2. Test compilation without running:
```bash
python -m src.main examples/demo.task
# Check output/demo.py was created
```

### 3. Run all tests:
```bash
python -m pytest tests/ -v
```

---

## 📚 File Dependencies

```
src/main.py
  └── src/cli.py
      ├── src/lexer/lexer.py
      │   └── src/lexer/token.py
      ├── src/parser/parser.py
      │   └── src/parser/ast.py
      ├── src/semantic/analyzer.py
      │   └── src/parser/ast.py
      └── src/codegen/python_gen.py
          └── src/parser/ast.py
```

---

## 🔗 Related Files

- **Configuration**: `requirements.txt`, `.gitignore`
- **Documentation**: `README.md`, `FILE_STRUCTURE.md` (this file)
- **Examples**: `examples/demo.task`
- **Output**: `output/*.py` (generated files)

