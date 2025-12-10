"""Semantic analyzer for TaskLang Compiler."""

from ..parser.ast import (
    ProgramNode, OpenNode, GoNode, TypeNode, EnterNode,
    WaitNode, ScreenshotNode, CloseNode, ClickNode
)


class SemanticError(Exception):
    """Exception raised when semantic analysis encounters an error."""
    
    def __init__(self, message: str, line: int = None):
        """
        Initialize a SemanticError.
        
        Args:
            message: Error message
            line: Line number where error occurred (1-indexed, optional)
        """
        self.message = message
        self.line = line
        if line is not None:
            super().__init__(f"Semantic error: {message} at line {line}")
        else:
            super().__init__(f"Semantic error: {message}")


class SemanticAnalyzer:
    """Semantic analyzer for TaskLang programs."""
    
    def __init__(self, ast: ProgramNode):
        """
        Initialize the semantic analyzer with an AST.
        
        Args:
            ast: The ProgramNode root of the AST to analyze
        """
        self.ast = ast
        self.browser_opened = False
        self.page_loaded = False
        self.statement_index = 0
    
    def analyze(self):
        """
        Perform semantic analysis on the AST.
        
        Raises:
            SemanticError: If any semantic rule is violated
            
        Returns:
            None on success
        """
        self.browser_opened = False
        self.page_loaded = False
        self.statement_index = 0
        
        for statement in self.ast.statements:
            self._analyze_statement(statement)
            self.statement_index += 1
    
    def _analyze_statement(self, statement):
        """
        Analyze a single statement.
        
        Args:
            statement: An AST node representing a statement
            
        Raises:
            SemanticError: If semantic rules are violated
        """
        line_number = self.statement_index + 1
        
        if isinstance(statement, OpenNode):
            self._analyze_open(statement, line_number)
        elif isinstance(statement, GoNode):
            self._analyze_go(statement, line_number)
        elif isinstance(statement, TypeNode):
            self._analyze_type(statement, line_number)
        elif isinstance(statement, ClickNode):
            self._analyze_click(statement, line_number)
        elif isinstance(statement, EnterNode):
            self._analyze_enter(statement, line_number)
        elif isinstance(statement, WaitNode):
            self._analyze_wait(statement, line_number)
        elif isinstance(statement, ScreenshotNode):
            self._analyze_screenshot(statement, line_number)
        elif isinstance(statement, CloseNode):
            self._analyze_close(statement, line_number)
    
    def _analyze_open(self, node: OpenNode, line_number: int):
        """Analyze an OpenNode statement."""
        self.browser_opened = True
        # Reset page_loaded when browser is opened
        self.page_loaded = False
    
    def _analyze_go(self, node: GoNode, line_number: int):
        """Analyze a GoNode statement."""
        if not self.browser_opened:
            raise SemanticError(
                f"Cannot navigate to URL '{node.url}' before opening a browser. "
                "You must use 'open' command first.",
                line_number
            )
        self.page_loaded = True
    
    def _analyze_type(self, node: TypeNode, line_number: int):
        """Analyze a TypeNode statement."""
        if not self.page_loaded:
            raise SemanticError(
                f"Cannot type text '{node.text}' before loading a page. "
                "You must use 'go' command to navigate to a URL first.",
                line_number
            )
    
    def _analyze_click(self, node: ClickNode, line_number: int):
        """Analyze a ClickNode statement."""
        if not self.page_loaded:
            raise SemanticError(
                "Cannot click element before loading a page. "
                "You must use 'go' command to navigate to a URL first.",
                line_number
            )
    
    def _analyze_enter(self, node: EnterNode, line_number: int):
        """Analyze an EnterNode statement."""
        if not self.page_loaded:
            raise SemanticError(
                "Cannot press Enter before loading a page. "
                "You must use 'go' command to navigate to a URL first.",
                line_number
            )
    
    def _analyze_wait(self, node: WaitNode, line_number: int):
        """Analyze a WaitNode statement."""
        if node.seconds <= 0:
            raise SemanticError(
                f"Wait time must be greater than 0, but got {node.seconds}. "
                "Please specify a positive number of seconds.",
                line_number
            )
    
    def _analyze_screenshot(self, node: ScreenshotNode, line_number: int):
        """Analyze a ScreenshotNode statement."""
        if not self.browser_opened:
            raise SemanticError(
                f"Cannot take screenshot '{node.filename}' before opening a browser. "
                "You must use 'open' command first.",
                line_number
            )
    
    def _analyze_close(self, node: CloseNode, line_number: int):
        """Analyze a CloseNode statement."""
        if not self.browser_opened:
            raise SemanticError(
                "Cannot close browser before opening one. "
                "You must use 'open' command first.",
                line_number
            )

