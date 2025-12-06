"""Python code generator for TaskLang Compiler."""

from pathlib import Path
from ..parser.ast import (
    ProgramNode, OpenNode, GoNode, TypeNode, EnterNode,
    WaitNode, ScreenshotNode, CloseNode
)


class PythonCodeGenerator:
    """Generates Python Selenium automation code from TaskLang AST."""
    
    def __init__(self, ast: ProgramNode):
        """
        Initialize the Python code generator with an AST.
        
        Args:
            ast: The ProgramNode root of the AST to generate code from
        """
        self.ast = ast
        self.lines = []
    
    def generate(self, output_path: str) -> str:
        """
        Generate Python code and write it to the output file.
        
        Args:
            output_path: Path to the output Python file
            
        Returns:
            The generated Python code as a string
        """
        self.lines = []
        
        # Add imports
        self._add_imports()
        self.lines.append("")
        
        # Generate code for each statement
        for statement in self.ast.statements:
            self._generate_statement(statement)
        
        # Join all lines
        code = "\n".join(self.lines)
        
        # Ensure output directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        return code
    
    def _add_imports(self):
        """Add required imports at the top of the file."""
        self.lines.append("from selenium import webdriver")
        self.lines.append("from selenium.webdriver.common.keys import Keys")
        self.lines.append("import time")
    
    def _generate_statement(self, statement):
        """
        Generate Python code for a single statement.
        
        Args:
            statement: An AST node representing a statement
        """
        if isinstance(statement, OpenNode):
            self._generate_open(statement)
        elif isinstance(statement, GoNode):
            self._generate_go(statement)
        elif isinstance(statement, TypeNode):
            self._generate_type(statement)
        elif isinstance(statement, EnterNode):
            self._generate_enter(statement)
        elif isinstance(statement, WaitNode):
            self._generate_wait(statement)
        elif isinstance(statement, ScreenshotNode):
            self._generate_screenshot(statement)
        elif isinstance(statement, CloseNode):
            self._generate_close(statement)
    
    def _generate_open(self, node: OpenNode):
        """Generate code for OpenNode: driver = webdriver.Chrome()"""
        self.lines.append("driver = webdriver.Chrome()")
        # Add safety delay after opening browser
        self.lines.append("time.sleep(2)")
    
    def _generate_go(self, node: GoNode):
        """Generate code for GoNode: driver.get("<url>")"""
        self.lines.append(f'driver.get("{node.url}")')
    
    def _generate_type(self, node: TypeNode):
        """Generate code for TypeNode: driver.find_element("name", "q").send_keys("<text>")"""
        # Escape quotes in the text
        escaped_text = node.text.replace('"', '\\"')
        self.lines.append(f'driver.find_element("name", "q").send_keys("{escaped_text}")')
    
    def _generate_enter(self, node: EnterNode):
        """Generate code for EnterNode: driver.find_element("name", "q").send_keys(Keys.ENTER)"""
        self.lines.append('driver.find_element("name", "q").send_keys(Keys.ENTER)')
    
    def _generate_wait(self, node: WaitNode):
        """Generate code for WaitNode: time.sleep(<seconds>)"""
        self.lines.append(f"time.sleep({node.seconds})")
    
    def _generate_screenshot(self, node: ScreenshotNode):
        """Generate code for ScreenshotNode: driver.save_screenshot("<filename>")"""
        self.lines.append(f'driver.save_screenshot("{node.filename}")')
    
    def _generate_close(self, node: CloseNode):
        """Generate code for CloseNode: driver.quit()"""
        self.lines.append("driver.quit()")

