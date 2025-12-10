# TaskLang Compiler - GUI Quick Start Guide

## 🖥️ Launch the GUI Application

Simply run:

```bash
python run_gui.py
```

This will open a graphical user interface where you can:

1. **Browse** for `.task` files
2. **Compile** TaskLang scripts to Python
3. **Run** the generated automation scripts
4. **View** compilation results (tokens, AST, semantic analysis)

## GUI Features

### File Selection
- Click **"Browse"** to select a `.task` file from your computer
- Or type the file path directly in the text field

### Compilation
- Click **"Compile"** to compile your selected script
- View real-time compilation results:
  - **Tokens Panel**: See all tokens generated from your script
  - **AST Panel**: View the Abstract Syntax Tree
  - **Semantic Analysis**: Check if compilation succeeded
  - **Generated Output**: See where your Python file was created

### Running Scripts
- After successful compilation, click **"Run"** to execute the automation
- The browser will open automatically and perform the automation
- Watch the status updates in the GUI

### Output Directory
- Change the output directory where Python files are generated
- Default is `output/` folder

## Step-by-Step Example

1. **Launch GUI:**
   ```bash
   python run_gui.py
   ```

2. **Select a script:**
   - Click "Browse"
   - Navigate to `examples/` folder
   - Select `demo.task` (or any other `.task` file)

3. **Compile:**
   - Click "Compile" button
   - Wait for compilation to complete
   - Check the panels for results

4. **Run:**
   - Click "Run" button
   - Watch the browser automation execute!

## Troubleshooting

### GUI doesn't open
- Make sure Python is installed: `python --version`
- Check if tkinter is available (usually comes with Python)

### Compilation fails
- Check the error message in the Semantic Analysis panel
- Make sure your `.task` file has valid syntax
- See `QUICK_REFERENCE.md` for syntax examples

### Script doesn't run
- Make sure browser drivers are installed (ChromeDriver, GeckoDriver, etc.)
- Check that the browser is installed on your system
- Look at error messages in the status panel

## Alternative Methods

If you prefer command line:

- **Compile directly:** `python -m src.main examples/demo.task`
- **Script selector:** `python run_scripts.py`

But the GUI is the easiest way to get started! 🚀

