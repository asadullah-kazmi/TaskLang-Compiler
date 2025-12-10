# How to Run TaskLang Compiler

## Quick Start Guide

### Step 1: Install Dependencies

First, make sure you have Python 3.8+ installed. Then install the required packages:

```bash
pip install -r requirements.txt
```

**Note:** You'll also need to have the browser drivers installed:

- **Chrome**: Install [ChromeDriver](https://chromedriver.chromium.org/)
- **Firefox**: Install [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
- **Edge**: EdgeDriver comes with Edge browser

### Step 2: Run the Compiler

You have **two ways** to compile TaskLang scripts:

#### Option A: Compile a Specific Script

Compile any `.task` file directly:

```bash
python -m src.main examples/demo.task
```

This will:

1. Parse the TaskLang script
2. Generate Python code in the `output/` directory
3. Create `output/demo.py` (or corresponding filename)

#### Option B: Use Interactive Script Selector

Launch the interactive script selector to browse and compile scripts:

```bash
python run_scripts.py
```

This will:

1. Show all available scripts in the `examples/` directory
2. Let you select a script by number
3. Compile the selected script
4. Ask if you want to compile another script

### Step 3: Run the Generated Python Script

After compilation, you can run the generated Python script:

```bash
python output/demo.py
```

This will execute the browser automation script.

## Examples

### Example 1: Use GUI Application (Easiest)

```bash
# Launch GUI
python run_gui.py

# In the GUI:
# 1. Click "Browse" to select a .task file
# 2. Click "Compile" to compile the script
# 3. Click "Run" to execute the generated Python script
# 4. Watch the browser automation happen!
```

### Example 2: Compile and Run Demo Script (Command Line)

```bash
# Compile
python -m src.main examples/demo.task

# Run the generated script
python output/demo.py
```

### Example 3: Use Script Selector (Command Line)

```bash
# Launch selector
python run_scripts.py

# Select script number (e.g., 1 for demo.task)
# Compile
# Run the generated script
python output/demo.py
```

### Example 3: Compile All Example Scripts

```bash
# Compile each script
python -m src.main examples/demo.task
python -m src.main examples/google_search.task
python -m src.main examples/github_search.task
python -m src.main examples/wikipedia.task
python -m src.main examples/youtube_search.task
python -m src.main examples/simple_navigation.task
```

## Available Example Scripts

1. **demo.task** - Basic Google search example
2. **google_search.task** - Google search with selectors
3. **github_search.task** - GitHub search example
4. **wikipedia.task** - Wikipedia search example
5. **youtube_search.task** - YouTube search example
6. **simple_navigation.task** - Simple page navigation

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'selenium'"

**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: "ChromeDriver not found"

**Solution:**

- Download ChromeDriver from https://chromedriver.chromium.org/
- Add it to your PATH or place it in the project directory

### Issue: "File not found"

**Solution:** Make sure you're running commands from the project root directory

### Issue: Browser doesn't open

**Solution:**

- Make sure the browser is installed
- Check that the browser driver is properly installed
- Verify the browser name in your script (chrome, firefox, edge, safari)

## Project Structure

```
tasklang-compiler/
├── examples/          # TaskLang script files (.task)
├── output/           # Generated Python files (.py)
├── src/              # Compiler source code
├── run_scripts.py    # Interactive script selector
└── requirements.txt  # Python dependencies
```

## Next Steps

- Create your own `.task` scripts in the `examples/` directory
- Compile them using `python -m src.main your_script.task`
- Run the generated Python files
- Check `QUICK_REFERENCE.md` for syntax examples
