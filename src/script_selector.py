"""Interactive script selector and launcher for TaskLang Compiler."""

import sys
import os
from pathlib import Path
from typing import List, Optional
from .cli import TaskLangCLI


class ScriptSelector:
    """Interactive script selector for choosing and compiling TaskLang scripts."""
    
    def __init__(self, examples_dir: str = "examples"):
        """
        Initialize the script selector.
        
        Args:
            examples_dir: Directory containing .task script files
        """
        self.examples_dir = Path(examples_dir)
        self.scripts: List[Path] = []
        self._load_scripts()
    
    def _load_scripts(self):
        """Load all .task files from the examples directory."""
        if not self.examples_dir.exists():
            print(f"Warning: Examples directory '{self.examples_dir}' not found.")
            return
        
        self.scripts = sorted(self.examples_dir.glob("*.task"))
        
        if not self.scripts:
            print(f"No .task files found in '{self.examples_dir}'")
    
    def display_menu(self):
        """Display the script selection menu."""
        if not self.scripts:
            print("No scripts available.")
            return
        
        print("\n" + "="*60)
        print("TaskLang Script Selector")
        print("="*60)
        print("\nAvailable scripts:\n")
        
        for i, script in enumerate(self.scripts, 1):
            # Read first few lines for description
            try:
                with open(script, 'r', encoding='utf-8') as f:
                    preview = f.read(100).replace('\n', ' ').strip()
                    if len(preview) > 50:
                        preview = preview[:50] + "..."
            except:
                preview = "N/A"
            
            print(f"  {i}. {script.name}")
            print(f"     Preview: {preview}")
            print()
        
        print(f"  {len(self.scripts) + 1}. Exit")
        print("="*60)
    
    def select_script(self) -> Optional[Path]:
        """
        Prompt user to select a script.
        
        Returns:
            Selected script path or None if user chooses to exit
        """
        if not self.scripts:
            return None
        
        while True:
            try:
                choice = input(f"\nSelect a script (1-{len(self.scripts) + 1}): ").strip()
                
                if not choice:
                    continue
                
                choice_num = int(choice)
                
                if choice_num == len(self.scripts) + 1:
                    print("Exiting...")
                    return None
                
                if 1 <= choice_num <= len(self.scripts):
                    return self.scripts[choice_num - 1]
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(self.scripts) + 1}")
            
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\n\nExiting...")
                return None
    
    def compile_script(self, script_path: Path, output_dir: str = "output"):
        """
        Compile a selected script.
        
        Args:
            script_path: Path to the .task script file
            output_dir: Output directory for generated Python file
        """
        print(f"\nCompiling: {script_path.name}")
        print("-" * 60)
        
        # Create a mock CLI instance and run compilation
        # We'll simulate the CLI arguments
        original_argv = sys.argv
        try:
            sys.argv = ['tasklang', str(script_path), '--output', output_dir]
            cli = TaskLangCLI()
            cli.run()
        except SystemExit as e:
            # CLI uses sys.exit(0) on success, sys.exit(1) on error
            if e.code != 0:
                print(f"\n❌ Compilation failed with exit code {e.code}")
            else:
                print(f"\n✅ Compilation successful!")
        except Exception as e:
            print(f"\n❌ Error during compilation: {e}")
        finally:
            sys.argv = original_argv
    
    def run(self):
        """Run the interactive script selector."""
        while True:
            self.display_menu()
            selected_script = self.select_script()
            
            if selected_script is None:
                break
            
            self.compile_script(selected_script)
            
            # Ask if user wants to continue
            while True:
                continue_choice = input("\nCompile another script? (y/n): ").strip().lower()
                if continue_choice in ['y', 'yes']:
                    break
                elif continue_choice in ['n', 'no']:
                    return
                else:
                    print("Please enter 'y' or 'n'")


def main():
    """Main entry point for script selector."""
    selector = ScriptSelector()
    selector.run()


if __name__ == "__main__":
    main()

