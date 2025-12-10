"""Python code generator for TaskLang Compiler."""

from pathlib import Path
from ..parser.ast import (
    ProgramNode, OpenNode, GoNode, TypeNode, EnterNode,
    WaitNode, ScreenshotNode, CloseNode, ClickNode
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
        self.lines.append("from selenium.webdriver.chrome.options import Options as ChromeOptions")
        self.lines.append("from selenium.webdriver.chrome.service import Service as ChromeService")
        self.lines.append("from selenium.webdriver.firefox.options import Options as FirefoxOptions")
        self.lines.append("from selenium.webdriver.edge.options import Options as EdgeOptions")
        self.lines.append("from selenium.webdriver.common.by import By")
        self.lines.append("from selenium.webdriver.common.keys import Keys")
        self.lines.append("from selenium.webdriver.support.ui import WebDriverWait")
        self.lines.append("from selenium.webdriver.support import expected_conditions as EC")
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
        elif isinstance(statement, ClickNode):
            self._generate_click(statement)
        elif isinstance(statement, EnterNode):
            self._generate_enter(statement)
        elif isinstance(statement, WaitNode):
            self._generate_wait(statement)
        elif isinstance(statement, ScreenshotNode):
            self._generate_screenshot(statement)
        elif isinstance(statement, CloseNode):
            self._generate_close(statement)
    
    def _generate_open(self, node: OpenNode):
        """Generate code for OpenNode: driver = webdriver.Browser() with anti-detection options"""
        browser = node.browser.lower()
        if browser == 'chrome':
            self.lines.append("# Configure Chrome options to avoid bot detection")
            self.lines.append("chrome_options = ChromeOptions()")
            self.lines.append("chrome_options.add_argument('--disable-blink-features=AutomationControlled')")
            self.lines.append("chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])")
            self.lines.append("chrome_options.add_experimental_option('useAutomationExtension', False)")
            self.lines.append("chrome_options.add_argument('--disable-dev-shm-usage')")
            self.lines.append("chrome_options.add_argument('--no-sandbox')")
            self.lines.append("chrome_options.add_argument('--disable-gpu')")
            self.lines.append("chrome_options.add_argument('--window-size=1920,1080')")
            self.lines.append("chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')")
            self.lines.append("driver = webdriver.Chrome(options=chrome_options)")
            self.lines.append("# Execute script to remove webdriver property")
            self.lines.append("driver.execute_script(\"Object.defineProperty(navigator, 'webdriver', {get: () => undefined})\")")
        elif browser == 'firefox':
            self.lines.append("# Configure Firefox options")
            self.lines.append("firefox_options = FirefoxOptions()")
            self.lines.append("firefox_options.set_preference('dom.webdriver.enabled', False)")
            self.lines.append("firefox_options.set_preference('useAutomationExtension', False)")
            self.lines.append("driver = webdriver.Firefox(options=firefox_options)")
        elif browser == 'edge':
            self.lines.append("# Configure Edge options")
            self.lines.append("edge_options = EdgeOptions()")
            self.lines.append("edge_options.add_argument('--disable-blink-features=AutomationControlled')")
            self.lines.append("edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])")
            self.lines.append("edge_options.add_experimental_option('useAutomationExtension', False)")
            self.lines.append("driver = webdriver.Edge(options=edge_options)")
        elif browser == 'safari':
            self.lines.append("driver = webdriver.Safari()")
        else:
            # Default to Chrome with anti-detection
            self.lines.append(f"# Unknown browser '{browser}', defaulting to Chrome")
            self.lines.append("chrome_options = ChromeOptions()")
            self.lines.append("chrome_options.add_argument('--disable-blink-features=AutomationControlled')")
            self.lines.append("chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])")
            self.lines.append("chrome_options.add_experimental_option('useAutomationExtension', False)")
            self.lines.append("driver = webdriver.Chrome(options=chrome_options)")
            self.lines.append("driver.execute_script(\"Object.defineProperty(navigator, 'webdriver', {get: () => undefined})\")")
        # Add safety delay after opening browser
        self.lines.append("time.sleep(2)")
    
    def _generate_go(self, node: GoNode):
        """Generate code for GoNode: driver.get("<url>")"""
        self.lines.append(f'driver.get("{node.url}")')
    
    def _get_element_selector(self, selector: str, selector_type: str) -> str:
        """
        Generate Selenium element selector code.
        
        Args:
            selector: The selector value
            selector_type: Type of selector ('id', 'name', 'xpath', 'css', 'tag')
            
        Returns:
            Python code string to find the element
        """
        if not selector or not selector_type:
            # Default to name="q" for backward compatibility
            return 'driver.find_element(By.NAME, "q")'
        
        selector_type = selector_type.lower()
        escaped_selector = selector.replace('"', '\\"')
        
        if selector_type == 'id':
            return f'driver.find_element(By.ID, "{escaped_selector}")'
        elif selector_type == 'name':
            return f'driver.find_element(By.NAME, "{escaped_selector}")'
        elif selector_type == 'xpath':
            return f'driver.find_element(By.XPATH, "{escaped_selector}")'
        elif selector_type == 'css':
            return f'driver.find_element(By.CSS_SELECTOR, "{escaped_selector}")'
        elif selector_type == 'tag':
            return f'driver.find_element(By.TAG_NAME, "{escaped_selector}")'
        else:
            # Default fallback
            return f'driver.find_element(By.NAME, "{escaped_selector}")'
    
    def _generate_type(self, node: TypeNode):
        """Generate code for TypeNode: driver.find_element(...).send_keys("<text>")"""
        # Escape quotes in the text
        escaped_text = node.text.replace('"', '\\"')
        element_code = self._get_element_selector(node.selector, node.selector_type)
        self.lines.append(f'{element_code}.send_keys("{escaped_text}")')
    
    def _generate_click(self, node: ClickNode):
        """Generate code for ClickNode: driver.find_element(...).click() with fallback for multiple selectors"""
        # Handle CSS selectors with multiple options (comma-separated)
        if node.selector_type == 'css' and ',' in node.selector:
            # Try multiple selectors
            selectors = [s.strip() for s in node.selector.split(',')]
            self.lines.append("# Try multiple CSS selectors")
            self.lines.append("element_found = False")
            
            # Build nested try-except structure
            for i, selector in enumerate(selectors):
                escaped_selector = selector.replace('"', '\\"').replace("'", "\\'")
                
                if i == 0:
                    # First try block
                    self.lines.append("try:")
                    self.lines.append(f"    element = driver.find_element(By.CSS_SELECTOR, \"{escaped_selector}\")")
                    self.lines.append(f"    element.click()")
                    self.lines.append(f"    element_found = True")
                else:
                    # Nested except-try blocks
                    # except should be at same level as previous try's content
                    except_indent = "    " * (i - 1) if i > 1 else ""
                    try_indent = "    " * i
                    self.lines.append(f"{except_indent}except Exception:")
                    self.lines.append(f"{try_indent}try:")
                    self.lines.append(f"{try_indent}    element = driver.find_element(By.CSS_SELECTOR, \"{escaped_selector}\")")
                    self.lines.append(f"{try_indent}    element.click()")
                    self.lines.append(f"{try_indent}    element_found = True")
            
            # Close the final nested except block
            if len(selectors) > 1:
                final_except_indent = "    " * (len(selectors) - 1)
                self.lines.append(f"{final_except_indent}except Exception:")
                self.lines.append(f"{final_except_indent}    pass")
            
            # Check if element was found - continue gracefully if not found
            self.lines.append("if not element_found:")
            selectors_repr = ', '.join([f'"{s}"' for s in selectors])
            self.lines.append(f"    selectors_list = [{selectors_repr}]")
            self.lines.append("    print(f\"Warning: Could not find element with any of the selectors: {selectors_list}\")")
            self.lines.append("    print(\"Continuing script execution...\")")
        else:
            # Single selector - wrap in try-except for graceful failure
            element_code = self._get_element_selector(node.selector, node.selector_type)
            self.lines.append("try:")
            self.lines.append(f"    {element_code}.click()")
            self.lines.append("except Exception as e:")
            if node.selector:
                # Use repr to properly escape the selector for display
                selector_repr = repr(node.selector)
                self.lines.append(f'    print("Warning: Could not find element with {node.selector_type} " + {selector_repr})')
            else:
                self.lines.append('    print("Warning: Could not find element with default selector")')
            self.lines.append('    print(f"Error: {e}")')
            self.lines.append("    print(\"Continuing script execution...\")")
    
    def _generate_enter(self, node: EnterNode):
        """Generate code for EnterNode: driver.find_element(...).send_keys(Keys.ENTER)"""
        element_code = self._get_element_selector(node.selector, node.selector_type)
        self.lines.append(f'{element_code}.send_keys(Keys.ENTER)')
    
    def _generate_wait(self, node: WaitNode):
        """Generate code for WaitNode: time.sleep(<seconds>)"""
        self.lines.append(f"time.sleep({node.seconds})")
    
    def _generate_screenshot(self, node: ScreenshotNode):
        """Generate code for ScreenshotNode: driver.save_screenshot("<filename>")"""
        self.lines.append(f'driver.save_screenshot("{node.filename}")')
    
    def _generate_close(self, node: CloseNode):
        """Generate code for CloseNode: driver.quit()"""
        self.lines.append("driver.quit()")

