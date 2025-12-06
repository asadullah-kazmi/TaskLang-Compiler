"""Abstract Syntax Tree nodes for TaskLang Compiler."""


class ASTNode:
    """Base class for all AST nodes."""
    
    def __repr__(self) -> str:
        """Return string representation of the node."""
        return self.__class__.__name__


class ProgramNode(ASTNode):
    """Root node representing a complete program."""
    
    def __init__(self, statements):
        """
        Initialize a ProgramNode.
        
        Args:
            statements: List of statement nodes
        """
        self.statements = statements
    
    def __repr__(self) -> str:
        """Return string representation of the program."""
        if not self.statements:
            return "ProgramNode([])"
        
        lines = ["ProgramNode("]
        for i, stmt in enumerate(self.statements):
            prefix = "  ├─ " if i < len(self.statements) - 1 else "  └─ "
            stmt_repr = repr(stmt)
            # Indent child nodes
            stmt_lines = stmt_repr.split('\n')
            lines.append(prefix + stmt_lines[0])
            for line in stmt_lines[1:]:
                connector = "  │  " if i < len(self.statements) - 1 else "     "
                lines.append(connector + line)
        lines.append(")")
        return "\n".join(lines)


class OpenNode(ASTNode):
    """Node representing an 'open' statement."""
    
    def __init__(self, browser: str):
        """
        Initialize an OpenNode.
        
        Args:
            browser: Browser name (e.g., 'chrome')
        """
        self.browser = browser
    
    def __repr__(self) -> str:
        """Return string representation of the node."""
        return f"OpenNode(browser={self.browser!r})"


class GoNode(ASTNode):
    """Node representing a 'go' statement."""
    
    def __init__(self, url: str):
        """
        Initialize a GoNode.
        
        Args:
            url: URL to navigate to
        """
        self.url = url
    
    def __repr__(self) -> str:
        """Return string representation of the node."""
        return f"GoNode(url={self.url!r})"


class TypeNode(ASTNode):
    """Node representing a 'type' statement."""
    
    def __init__(self, text: str):
        """
        Initialize a TypeNode.
        
        Args:
            text: Text to type
        """
        self.text = text
    
    def __repr__(self) -> str:
        """Return string representation of the node."""
        return f"TypeNode(text={self.text!r})"


class EnterNode(ASTNode):
    """Node representing an 'enter' statement."""
    
    def __repr__(self) -> str:
        """Return string representation of the node."""
        return "EnterNode()"


class WaitNode(ASTNode):
    """Node representing a 'wait' statement."""
    
    def __init__(self, seconds: int):
        """
        Initialize a WaitNode.
        
        Args:
            seconds: Number of seconds to wait
        """
        self.seconds = seconds
    
    def __repr__(self) -> str:
        """Return string representation of the node."""
        return f"WaitNode(seconds={self.seconds})"


class ScreenshotNode(ASTNode):
    """Node representing a 'screenshot' statement."""
    
    def __init__(self, filename: str):
        """
        Initialize a ScreenshotNode.
        
        Args:
            filename: Filename for the screenshot
        """
        self.filename = filename
    
    def __repr__(self) -> str:
        """Return string representation of the node."""
        return f"ScreenshotNode(filename={self.filename!r})"


class CloseNode(ASTNode):
    """Node representing a 'close' statement."""
    
    def __repr__(self) -> str:
        """Return string representation of the node."""
        return "CloseNode()"

