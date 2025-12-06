"""Main window for TaskLang Compiler GUI."""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from pathlib import Path
import subprocess
import threading
from ..lexer.lexer import Lexer, LexerError
from ..parser.parser import Parser, ParserError
from ..semantic.analyzer import SemanticAnalyzer, SemanticError
from ..codegen.python_gen import PythonCodeGenerator


class MainWindow:
    """Main application window for TaskLang Compiler."""
    
    def __init__(self, root: tk.Tk = None):
        """
        Initialize the main window.
        
        Args:
            root: Tkinter root window. If None, creates a new one.
        """
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root
        
        # Store selected file path
        self.selected_file_path = None
        
        # Store output directory (default: output/)
        self.output_directory = Path("output")
        
        # Store generated Python script path
        self.generated_script_path = None
        
        self._setup_window()
        self._create_layout()
    
    def _setup_window(self):
        """Configure the main window properties."""
        self.root.title("TaskLang Compiler")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Center the window on screen
        self._center_window()
    
    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_layout(self):
        """Create the main layout structure."""
        # Main container frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Create file selection section
        self._create_file_selection()
        
        # Create output panels section
        self._create_output_panels()
    
    def _create_file_selection(self):
        """Create the file selection widgets."""
        # File selection frame with padding
        file_frame = ttk.LabelFrame(self.main_frame, text="File Selection", padding="10")
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # File selection row
        file_label = ttk.Label(
            file_frame,
            text="TaskLang File:",
            font=("Arial", 10, "bold")
        )
        file_label.grid(row=0, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        
        # Entry field for file path
        self.file_entry = ttk.Entry(
            file_frame,
            width=50,
            font=("Arial", 9)
        )
        self.file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        # Browse button
        browse_button = ttk.Button(
            file_frame,
            text="Browse",
            command=self._browse_file,
            width=12
        )
        browse_button.grid(row=0, column=2, pady=5, padx=(0, 10))
        
        # Compile button
        self.compile_button = ttk.Button(
            file_frame,
            text="Compile",
            command=self._compile_clicked,
            width=12
        )
        self.compile_button.grid(row=0, column=3, pady=5, padx=(0, 10))
        
        # Run button
        self.run_button = ttk.Button(
            file_frame,
            text="Run",
            command=self._run_script,
            width=12,
            state=tk.DISABLED
        )
        self.run_button.grid(row=0, column=4, pady=5)
        
        # Output directory selection row
        output_label = ttk.Label(
            file_frame,
            text="Output Directory:",
            font=("Arial", 10, "bold")
        )
        output_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        
        # Entry field for output directory
        self.output_entry = ttk.Entry(
            file_frame,
            width=50,
            font=("Arial", 9)
        )
        self.output_entry.insert(0, str(self.output_directory))
        self.output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        # Browse output directory button
        browse_output_button = ttk.Button(
            file_frame,
            text="Browse Output",
            command=self._browse_output_directory,
            width=12
        )
        browse_output_button.grid(row=1, column=2, pady=5, padx=(0, 10))
    
    def _create_output_panels(self):
        """Create output panels for displaying compilation results."""
        # Container frame for output panels
        output_container = ttk.Frame(self.main_frame)
        output_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        output_container.columnconfigure(0, weight=1)
        output_container.columnconfigure(1, weight=1)
        output_container.rowconfigure(0, weight=1)
        output_container.rowconfigure(1, weight=1)
        
        # Tokens Panel (top-left)
        self._create_tokens_panel(output_container)
        
        # AST Panel (top-right)
        self._create_ast_panel(output_container)
        
        # Semantic Analysis Result (bottom-left)
        self._create_semantic_panel(output_container)
        
        # Generated Python Script Path (bottom-right)
        self._create_output_path_panel(output_container)
    
    def _create_tokens_panel(self, parent):
        """Create the Tokens display panel."""
        # Frame for tokens panel with padding
        tokens_frame = ttk.LabelFrame(parent, text="Tokens", padding="8")
        tokens_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5), pady=(0, 5))
        tokens_frame.columnconfigure(0, weight=1)
        tokens_frame.rowconfigure(1, weight=1)
        
        # Label
        tokens_label = ttk.Label(
            tokens_frame,
            text="Tokenized Output:",
            font=("Arial", 9, "bold")
        )
        tokens_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        
        # ScrolledText widget for tokens (already scrollable)
        self.tokens_text = scrolledtext.ScrolledText(
            tokens_frame,
            width=40,
            height=15,
            wrap=tk.NONE,  # No wrapping for better readability of tokens
            font=("Consolas", 9),
            state=tk.DISABLED,
            bg="#f8f8f8",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        self.tokens_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def _create_ast_panel(self, parent):
        """Create the AST display panel."""
        # Frame for AST panel with padding
        ast_frame = ttk.LabelFrame(parent, text="AST", padding="8")
        ast_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0), pady=(0, 5))
        ast_frame.columnconfigure(0, weight=1)
        ast_frame.rowconfigure(1, weight=1)
        
        # Label
        ast_label = ttk.Label(
            ast_frame,
            text="Abstract Syntax Tree:",
            font=("Arial", 9, "bold")
        )
        ast_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        
        # ScrolledText widget for AST (already scrollable)
        self.ast_text = scrolledtext.ScrolledText(
            ast_frame,
            width=40,
            height=15,
            wrap=tk.NONE,  # No wrapping for better tree structure readability
            font=("Consolas", 9),
            state=tk.DISABLED,
            bg="#f8f8f8",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        self.ast_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def _create_semantic_panel(self, parent):
        """Create the Semantic Analysis Result panel."""
        # Frame for semantic panel with padding
        semantic_frame = ttk.LabelFrame(parent, text="Semantic Analysis", padding="8")
        semantic_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5), pady=(5, 0))
        semantic_frame.columnconfigure(0, weight=1)
        
        # Label
        semantic_label = ttk.Label(
            semantic_frame,
            text="Status:",
            font=("Arial", 9, "bold")
        )
        semantic_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        
        # Result label with word wrapping
        self.semantic_result_label = ttk.Label(
            semantic_frame,
            text="Not analyzed yet",
            font=("Arial", 9),
            foreground="gray",
            wraplength=400
        )
        self.semantic_result_label.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
    
    def _create_output_path_panel(self, parent):
        """Create the Generated Python Script Path panel."""
        # Frame for output path panel with padding
        output_path_frame = ttk.LabelFrame(parent, text="Generated Output", padding="8")
        output_path_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0), pady=(5, 0))
        output_path_frame.columnconfigure(0, weight=1)
        
        # Label
        output_path_label = ttk.Label(
            output_path_frame,
            text="Python Script Path:",
            font=("Arial", 9, "bold")
        )
        output_path_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        
        # Result label with word wrapping
        self.output_path_label = ttk.Label(
            output_path_frame,
            text="No file generated yet",
            font=("Arial", 9),
            foreground="gray",
            wraplength=400
        )
        self.output_path_label.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
    
    def _browse_file(self):
        """
        Open file dialog to select a .task file.
        Updates the Entry field and stores the selected path.
        """
        file_path = filedialog.askopenfilename(
            title="Select TaskLang File",
            filetypes=[("TaskLang files", "*.task"), ("All files", "*.*")],
            initialdir=Path.cwd()
        )
        
        if file_path:
            self.selected_file_path = file_path
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
    
    def _browse_output_directory(self):
        """
        Open directory dialog to select output directory.
        Updates the Entry field and stores the selected path.
        """
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=str(self.output_directory)
        )
        
        if directory:
            self.output_directory = Path(directory)
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, str(self.output_directory))
    
    def _compile_clicked(self):
        """
        Handle Compile button click event.
        Executes the compiler pipeline: lexer → parser → semantic analysis.
        """
        # Clear previous results
        self._clear_output_panels()
        
        # Check if a file is selected
        if not self.selected_file_path:
            self._show_error("Please select a TaskLang file first.")
            return
        
        # Validate file exists
        file_path = Path(self.selected_file_path)
        if not file_path.exists():
            self._show_error(f"File not found: {self.selected_file_path}")
            return
        
        # Read the file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception as e:
            self._show_error(f"Failed to read file: {e}")
            return
        
        # Step 1: Lexical Analysis
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            # Display tokens in Tokens Panel
            self._display_tokens(tokens)
            
        except LexerError as e:
            self._show_error(f"Lexer Error: {e}")
            return
        except Exception as e:
            self._show_error(f"Unexpected error during lexing: {e}")
            return
        
        # Step 2: Parsing
        try:
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Display AST in AST Panel
            self._display_ast(ast)
            
        except ParserError as e:
            self._show_error(f"Parser Error: {e}")
            return
        except Exception as e:
            self._show_error(f"Unexpected error during parsing: {e}")
            return
        
        # Step 3: Semantic Analysis
        try:
            analyzer = SemanticAnalyzer(ast)
            analyzer.analyze()
            
            # Display success message
            self._show_semantic_success("✅ Semantic Analysis Passed")
            
        except SemanticError as e:
            self._show_error(f"Semantic Error: {e}")
            return
        except Exception as e:
            self._show_error(f"Unexpected error during semantic analysis: {e}")
            return
        
        # Step 4: Python Code Generation
        try:
            # Get output directory from entry field
            output_dir_str = self.output_entry.get().strip()
            if output_dir_str:
                self.output_directory = Path(output_dir_str)
            else:
                self.output_directory = Path("output")
            
            # Ensure output directory exists
            self.output_directory.mkdir(parents=True, exist_ok=True)
            
            # Determine output filename
            input_filename = file_path.stem  # Get filename without extension
            
            # Construct output file path
            output_file = self.output_directory / f"{input_filename}.py"
            
            # Generate Python code
            generator = PythonCodeGenerator(ast)
            generator.generate(str(output_file))
            
            # Store generated script path
            self.generated_script_path = output_file
            
            # Display success message with file path
            self._show_output_success(f"✅ Python automation script generated at {output_file}")
            
            # Enable Run button
            self.run_button.config(state=tk.NORMAL)
            
        except Exception as e:
            self._show_error(f"Failed to generate Python code: {e}")
            self.run_button.config(state=tk.DISABLED)
            return
    
    def _clear_output_panels(self):
        """Clear all output panels."""
        # Clear tokens panel
        self.tokens_text.config(state=tk.NORMAL)
        self.tokens_text.delete(1.0, tk.END)
        self.tokens_text.config(state=tk.DISABLED)
        
        # Clear AST panel
        self.ast_text.config(state=tk.NORMAL)
        self.ast_text.delete(1.0, tk.END)
        self.ast_text.config(state=tk.DISABLED)
        
        # Reset semantic analysis label
        self.semantic_result_label.config(text="Not analyzed yet", foreground="gray")
        
        # Reset output path label
        self.output_path_label.config(text="No file generated yet", foreground="gray")
        
        # Disable Run button
        self.run_button.config(state=tk.DISABLED)
        self.generated_script_path = None
    
    def _display_tokens(self, tokens):
        """
        Display tokens in the Tokens Panel.
        
        Args:
            tokens: List of Token objects
        """
        self.tokens_text.config(state=tk.NORMAL)
        self.tokens_text.delete(1.0, tk.END)
        
        if not tokens:
            self.tokens_text.insert(tk.END, "No tokens found.")
        else:
            for token in tokens:
                self.tokens_text.insert(tk.END, f"{token}\n")
        
        self.tokens_text.config(state=tk.DISABLED)
    
    def _display_ast(self, ast):
        """
        Display AST in the AST Panel.
        
        Args:
            ast: ProgramNode object
        """
        self.ast_text.config(state=tk.NORMAL)
        self.ast_text.delete(1.0, tk.END)
        
        # Convert AST to string representation
        ast_str = str(ast)
        self.ast_text.insert(tk.END, ast_str)
        
        self.ast_text.config(state=tk.DISABLED)
    
    def _show_semantic_success(self, message):
        """
        Display success message in Semantic Analysis Label.
        
        Args:
            message: Success message string
        """
        # Ensure message starts with ✅ if not already present
        if not message.startswith("✅"):
            message = f"✅ {message}"
        self.semantic_result_label.config(text=message, foreground="green")
    
    def _show_error(self, error_message):
        """
        Display error message in Semantic Analysis Label.
        
        Args:
            error_message: Error message string
        """
        # Ensure message starts with ❌ if not already present
        if not error_message.startswith("❌") and not error_message.startswith("✅"):
            error_message = f"❌ {error_message}"
        self.semantic_result_label.config(text=error_message, foreground="red")
        # Also clear output path on error
        self.output_path_label.config(text="No file generated yet", foreground="gray")
    
    def _show_output_success(self, message):
        """
        Display success message in Generated Output Label.
        
        Args:
            message: Success message string with file path
        """
        self.output_path_label.config(text=message, foreground="green")
    
    def _run_script(self):
        """
        Execute the generated Python automation script.
        Runs in a separate thread to keep GUI responsive.
        """
        if not self.generated_script_path or not self.generated_script_path.exists():
            self._show_error("No generated script found. Please compile first.")
            return
        
        # Disable Run button during execution
        self.run_button.config(state=tk.DISABLED, text="Running...")
        
        # Update status
        self._show_semantic_success("🚀 Running automation script...")
        
        # Run script in a separate thread to keep GUI responsive
        def execute_script():
            try:
                # Execute the Python script
                result = subprocess.run(
                    ["python", str(self.generated_script_path)],
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                
                # Update GUI in main thread
                self.root.after(0, lambda: self._script_finished(result))
                
            except subprocess.TimeoutExpired:
                self.root.after(0, lambda: self._show_error("❌ Script execution timed out (5 minutes)"))
                self.root.after(0, lambda: self.run_button.config(state=tk.NORMAL, text="Run"))
            except Exception as e:
                self.root.after(0, lambda: self._show_error(f"❌ Failed to run script: {e}"))
                self.root.after(0, lambda: self.run_button.config(state=tk.NORMAL, text="Run"))
        
        # Start execution in background thread
        thread = threading.Thread(target=execute_script, daemon=True)
        thread.start()
    
    def _script_finished(self, result):
        """
        Handle script execution completion.
        
        Args:
            result: subprocess.CompletedProcess result
        """
        # Re-enable Run button
        self.run_button.config(state=tk.NORMAL, text="Run")
        
        if result.returncode == 0:
            self._show_semantic_success("✅ Script executed successfully!")
        else:
            error_msg = result.stderr if result.stderr else "Script execution failed"
            self._show_error(f"❌ Script execution failed: {error_msg}")
    
    def run(self):
        """Start the GUI event loop."""
        self.root.mainloop()


def main():
    """Entry point for running the GUI standalone."""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()

