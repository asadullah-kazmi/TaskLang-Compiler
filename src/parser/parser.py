"""Parser module for TaskLang Compiler."""

from typing import List, Optional
from .ast import (
    ProgramNode, OpenNode, GoNode, TypeNode, EnterNode,
    WaitNode, ScreenshotNode, CloseNode
)


class ParserError(Exception):
    """Exception raised when parser encounters a syntax error."""
    
    def __init__(self, message: str, line: int, column: int):
        """
        Initialize a ParserError.
        
        Args:
            message: Error message
            line: Line number where error occurred (1-indexed)
            column: Column number where error occurred (1-indexed)
        """
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Syntax error: {message} at line {line}, column {column}")


class Parser:
    """Recursive descent parser for TaskLang."""
    
    def __init__(self, tokens: List):
        """
        Initialize the parser with a list of tokens.
        
        Args:
            tokens: List of Token objects from the lexer
        """
        self.tokens = tokens
        self.pos = 0
    
    def parse(self) -> ProgramNode:
        """
        Parse the tokens and return an AST.
        
        Returns:
            ProgramNode representing the parsed program
            
        Raises:
            ParserError: If a syntax error is encountered
        """
        statements = []
        
        while not self._is_at_end():
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        return ProgramNode(statements)
    
    def parse_statement(self):
        """
        Parse a single statement.
        
        Returns:
            An AST node representing the statement
            
        Raises:
            ParserError: If a syntax error is encountered
        """
        if self._is_at_end():
            return None
        
        token = self._peek()
        
        if token.type == 'OPEN':
            return self._parse_open_stmt()
        elif token.type == 'GO':
            return self._parse_go_stmt()
        elif token.type == 'TYPE':
            return self._parse_type_stmt()
        elif token.type == 'ENTER':
            return self._parse_enter_stmt()
        elif token.type == 'WAIT':
            return self._parse_wait_stmt()
        elif token.type == 'SCREENSHOT':
            return self._parse_screenshot_stmt()
        elif token.type == 'CLOSE':
            return self._parse_close_stmt()
        else:
            raise ParserError(
                f"Unexpected token: {token.type}",
                token.line,
                token.column
            )
    
    def _parse_open_stmt(self) -> OpenNode:
        """Parse an 'open' statement: OPEN IDENTIFIER"""
        open_token = self._consume('OPEN', "Expected 'open' keyword")
        browser_token = self._consume('IDENTIFIER', "Expected browser identifier after 'open'")
        return OpenNode(browser_token.value)
    
    def _parse_go_stmt(self) -> GoNode:
        """Parse a 'go' statement: GO URL"""
        go_token = self._consume('GO', "Expected 'go' keyword")
        url_token = self._consume('URL', "Expected URL after 'go'")
        return GoNode(url_token.value)
    
    def _parse_type_stmt(self) -> TypeNode:
        """Parse a 'type' statement: TYPE STRING"""
        type_token = self._consume('TYPE', "Expected 'type' keyword")
        string_token = self._consume('STRING', "Expected string literal after 'type'")
        return TypeNode(string_token.value)
    
    def _parse_enter_stmt(self) -> EnterNode:
        """Parse an 'enter' statement: ENTER"""
        self._consume('ENTER', "Expected 'enter' keyword")
        return EnterNode()
    
    def _parse_wait_stmt(self) -> WaitNode:
        """Parse a 'wait' statement: WAIT NUMBER"""
        wait_token = self._consume('WAIT', "Expected 'wait' keyword")
        number_token = self._consume('NUMBER', "Expected number after 'wait'")
        try:
            seconds = int(number_token.value)
        except ValueError:
            raise ParserError(
                f"Invalid number: {number_token.value}",
                number_token.line,
                number_token.column
            )
        return WaitNode(seconds)
    
    def _parse_screenshot_stmt(self) -> ScreenshotNode:
        """Parse a 'screenshot' statement: SCREENSHOT IDENTIFIER"""
        screenshot_token = self._consume('SCREENSHOT', "Expected 'screenshot' keyword")
        filename_token = self._consume('IDENTIFIER', "Expected filename after 'screenshot'")
        return ScreenshotNode(filename_token.value)
    
    def _parse_close_stmt(self) -> CloseNode:
        """Parse a 'close' statement: CLOSE"""
        self._consume('CLOSE', "Expected 'close' keyword")
        return CloseNode()
    
    def _peek(self):
        """Return the current token without consuming it."""
        if self._is_at_end():
            return None
        return self.tokens[self.pos]
    
    def _advance(self):
        """Consume and return the current token."""
        if not self._is_at_end():
            self.pos += 1
        return self.tokens[self.pos - 1] if self.pos > 0 else None
    
    def _is_at_end(self) -> bool:
        """Check if we've consumed all tokens."""
        return self.pos >= len(self.tokens)
    
    def _consume(self, expected_type: str, error_message: str):
        """
        Consume a token of the expected type.
        
        Args:
            expected_type: The expected token type
            error_message: Error message if token doesn't match
            
        Returns:
            The consumed token
            
        Raises:
            ParserError: If the current token doesn't match the expected type
        """
        if self._is_at_end():
            # Use the last token's position for error reporting
            last_token = self.tokens[-1] if self.tokens else None
            if last_token:
                raise ParserError(
                    f"{error_message} (reached end of file)",
                    last_token.line,
                    last_token.column
                )
            else:
                raise ParserError(
                    f"{error_message} (no tokens available)",
                    1,
                    1
                )
        
        token = self._peek()
        if token.type != expected_type:
            raise ParserError(
                f"{error_message}, but found {token.type} ({token.value!r})",
                token.line,
                token.column
            )
        
        return self._advance()

