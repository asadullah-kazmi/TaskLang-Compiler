"""Token class for TaskLang Compiler."""


class Token:
    """Represents a token in the TaskLang source code."""
    
    def __init__(self, type: str, value: str, line: int, column: int):
        """
        Initialize a Token.
        
        Args:
            type: The token type (e.g., 'OPEN', 'STRING', 'IDENTIFIER')
            value: The token value (e.g., 'open', '"hello"', 'chrome')
            line: Line number where the token appears (1-indexed)
            column: Column number where the token starts (1-indexed)
        """
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self) -> str:
        """Return string representation of the token."""
        return f"TOKEN({self.type}, {self.value!r}, {self.line}, {self.column})"
    
    def __eq__(self, other) -> bool:
        """Check equality of two tokens."""
        if not isinstance(other, Token):
            return False
        return (self.type == other.type and 
                self.value == other.value and 
                self.line == other.line and 
                self.column == other.column)

