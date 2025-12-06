"""Lexer module for TaskLang Compiler."""

import re
from typing import List, Optional
from .token import Token


class LexerError(Exception):
    """Exception raised when lexer encounters an error."""
    
    def __init__(self, message: str, line: int, column: int):
        """
        Initialize a LexerError.
        
        Args:
            message: Error message
            line: Line number where error occurred (1-indexed)
            column: Column number where error occurred (1-indexed)
        """
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"{message} at line {line}, column {column}")


class Lexer:
    """Lexical analyzer for TaskLang."""
    
    # Keyword mapping
    KEYWORDS = {
        'open': 'OPEN',
        'go': 'GO',
        'type': 'TYPE',
        'click': 'CLICK',
        'enter': 'ENTER',
        'wait': 'WAIT',
        'screenshot': 'SCREENSHOT',
        'close': 'CLOSE',
    }
    
    def __init__(self, source: str):
        """
        Initialize the lexer with source code.
        
        Args:
            source: The source code to tokenize
        """
        self.source = source
        self.tokens: List[Token] = []
        self.pos = 0
        self.line = 1
        self.column = 1
        self.start_pos = 0
        self.start_line = 1
        self.start_column = 1
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the source code and return a list of tokens.
        
        Returns:
            List of Token objects
            
        Raises:
            LexerError: If an invalid token or unterminated string is found
        """
        self.tokens = []
        self.pos = 0
        self.line = 1
        self.column = 1
        
        while self.pos < len(self.source):
            self.start_pos = self.pos
            self.start_line = self.line
            self.start_column = self.column
            
            # Skip whitespace (but track newlines)
            if self._match(r'\s'):
                if self.source[self.pos - 1] == '\n':
                    self.line += 1
                    self.column = 1
                continue
            
            # Skip comments (lines starting with #)
            if self._match(r'#.*'):
                # Skip until newline
                while self.pos < len(self.source) and self.source[self.pos] != '\n':
                    self.pos += 1
                continue
            
            # Match tokens in order of specificity
            
            # URL pattern (must come before identifier)
            if token := self._match_url():
                self.tokens.append(token)
                continue
            
            # String literals (double quoted)
            if token := self._match_string():
                self.tokens.append(token)
                continue
            
            # Numbers (integers)
            if token := self._match_number():
                self.tokens.append(token)
                continue
            
            # Keywords and identifiers
            if token := self._match_keyword_or_identifier():
                self.tokens.append(token)
                continue
            
            # If we get here, we have an unknown character
            raise LexerError(
                f"Unexpected character: {self.source[self.pos]!r}",
                self.line,
                self.column
            )
        
        return self.tokens
    
    def _match(self, pattern: str) -> bool:
        """
        Try to match a pattern at the current position.
        
        Args:
            pattern: Regular expression pattern
            
        Returns:
            True if pattern matched, False otherwise
        """
        regex = re.compile(pattern)
        match = regex.match(self.source, self.pos)
        if match:
            matched_text = match.group(0)
            self.pos += len(matched_text)
            self.column += len(matched_text)
            return True
        return False
    
    def _match_string(self) -> Optional[Token]:
        """
        Match a string literal (double quoted).
        
        Returns:
            Token if matched, None otherwise
            
        Raises:
            LexerError: If string is unterminated
        """
        if self.pos >= len(self.source) or self.source[self.pos] != '"':
            return None
        
        # Start of string
        self.pos += 1
        self.column += 1
        start_col = self.column
        
        # Find the end of the string
        while self.pos < len(self.source):
            if self.source[self.pos] == '"':
                # Found closing quote
                value = self.source[self.start_pos + 1:self.pos]
                self.pos += 1
                self.column += 1
                return Token('STRING', value, self.start_line, self.start_column)
            elif self.source[self.pos] == '\n':
                # String spans multiple lines - error
                raise LexerError(
                    "Unterminated string literal",
                    self.start_line,
                    self.start_column
                )
            else:
                self.pos += 1
                self.column += 1
        
        # Reached end of file without closing quote
        raise LexerError(
            "Unterminated string literal",
            self.start_line,
            self.start_column
        )
    
    def _match_number(self) -> Optional[Token]:
        """
        Match an integer number.
        
        Returns:
            Token if matched, None otherwise
        """
        if self.pos >= len(self.source) or not self.source[self.pos].isdigit():
            return None
        
        # Match one or more digits
        start_col = self.column
        value = ''
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            value += self.source[self.pos]
            self.pos += 1
            self.column += 1
        
        return Token('NUMBER', value, self.start_line, self.start_column)
    
    def _match_url(self) -> Optional[Token]:
        """
        Match a URL (http:// or https://).
        
        Returns:
            Token if matched, None otherwise
        """
        # Match http:// or https:// followed by URL characters
        pattern = r'https?://[^\s\n]+'
        regex = re.compile(pattern)
        match = regex.match(self.source, self.pos)
        if match:
            value = match.group(0)
            token = Token('URL', value, self.start_line, self.start_column)
            self.pos += len(value)
            self.column += len(value)
            return token
        return None
    
    def _match_keyword_or_identifier(self) -> Optional[Token]:
        """
        Match a keyword or identifier.
        
        Returns:
            Token if matched, None otherwise
        """
        # Match identifier: starts with letter or underscore, followed by letters, digits, underscores, dots
        pattern = r'[a-zA-Z_][a-zA-Z0-9_.]*'
        regex = re.compile(pattern)
        match = regex.match(self.source, self.pos)
        if match:
            value = match.group(0)
            # Check if it's a keyword
            token_type = self.KEYWORDS.get(value.lower(), 'IDENTIFIER')
            token = Token(token_type, value, self.start_line, self.start_column)
            self.pos += len(value)
            self.column += len(value)
            return token
        return None

