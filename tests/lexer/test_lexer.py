"""Unit tests for the TaskLang lexer."""

import pytest
from src.lexer.lexer import Lexer, LexerError
from src.lexer.token import Token


class TestLexer:
    """Test cases for the Lexer class."""
    
    def test_single_command_open_chrome(self):
        """Test tokenization of 'open chrome' command."""
        source = "open chrome"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        assert len(tokens) == 2
        assert tokens[0] == Token('OPEN', 'open', 1, 1)
        assert tokens[1] == Token('IDENTIFIER', 'chrome', 1, 6)
    
    def test_full_example_program(self):
        """Test tokenization of the full example program."""
        source = """open chrome
go https://google.com
type "compiler project"
enter
wait 2
screenshot test.png"""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Verify token count and types
        expected_tokens = [
            ('OPEN', 'open', 1, 1),
            ('IDENTIFIER', 'chrome', 1, 6),
            ('GO', 'go', 2, 1),
            ('URL', 'https://google.com', 2, 4),
            ('TYPE', 'type', 3, 1),
            ('STRING', 'compiler project', 3, 6),
            ('ENTER', 'enter', 4, 1),
            ('WAIT', 'wait', 5, 1),
            ('NUMBER', '2', 5, 6),
            ('SCREENSHOT', 'screenshot', 6, 1),
            ('IDENTIFIER', 'test.png', 6, 12),
        ]
        
        assert len(tokens) == len(expected_tokens)
        for i, (token_type, value, line, column) in enumerate(expected_tokens):
            assert tokens[i].type == token_type
            assert tokens[i].value == value
            assert tokens[i].line == line
            assert tokens[i].column == column
    
    def test_comments_are_ignored(self):
        """Test that comments (lines starting with #) are ignored."""
        source = """open chrome
# This is a comment
go https://google.com
# Another comment
type "hello"
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Should not have any COMMENT tokens, and comments should be skipped
        token_types = [token.type for token in tokens]
        assert 'COMMENT' not in token_types
        
        # Verify actual tokens
        assert tokens[0].type == 'OPEN'
        assert tokens[1].type == 'IDENTIFIER'
        assert tokens[2].type == 'GO'
        assert tokens[3].type == 'URL'
        assert tokens[4].type == 'TYPE'
        assert tokens[5].type == 'STRING'
    
    def test_whitespace_is_skipped(self):
        """Test that whitespace and tabs are skipped."""
        source = "open    chrome\t\t\nwait  2"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Should only have tokens, no whitespace tokens
        assert len(tokens) == 4
        assert tokens[0].type == 'OPEN'
        assert tokens[1].type == 'IDENTIFIER'
        assert tokens[2].type == 'WAIT'
        assert tokens[3].type == 'NUMBER'
    
    def test_string_literal(self):
        """Test string literal tokenization."""
        source = 'type "hello world"'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        assert len(tokens) == 2
        assert tokens[0].type == 'TYPE'
        assert tokens[1].type == 'STRING'
        assert tokens[1].value == 'hello world'
    
    def test_number_token(self):
        """Test number tokenization."""
        source = "wait 123"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        assert len(tokens) == 2
        assert tokens[0].type == 'WAIT'
        assert tokens[1].type == 'NUMBER'
        assert tokens[1].value == '123'
    
    def test_url_token(self):
        """Test URL tokenization."""
        source = "go http://example.com"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        assert len(tokens) == 2
        assert tokens[0].type == 'GO'
        assert tokens[1].type == 'URL'
        assert tokens[1].value == 'http://example.com'
        
        source2 = "go https://test.org/path"
        lexer2 = Lexer(source2)
        tokens2 = lexer2.tokenize()
        
        assert tokens2[1].type == 'URL'
        assert tokens2[1].value == 'https://test.org/path'
    
    def test_all_keywords(self):
        """Test that all keywords are recognized."""
        keywords = ['open', 'go', 'type', 'click', 'enter', 'wait', 'screenshot', 'close']
        
        for keyword in keywords:
            source = keyword
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            assert len(tokens) == 1
            assert tokens[0].type == keyword.upper()
            assert tokens[0].value == keyword
    
    def test_keywords_case_insensitive(self):
        """Test that keywords are case-insensitive."""
        source = "OPEN Chrome"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        assert tokens[0].type == 'OPEN'
        assert tokens[0].value == 'OPEN'
    
    def test_identifier_with_dots(self):
        """Test identifiers with dots (like filenames)."""
        source = "screenshot test.png"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        assert tokens[1].type == 'IDENTIFIER'
        assert tokens[1].value == 'test.png'
    
    def test_unterminated_string_raises_error(self):
        """Test that unterminated string raises LexerError."""
        source = 'type "unterminated string'
        lexer = Lexer(source)
        
        with pytest.raises(LexerError) as exc_info:
            lexer.tokenize()
        
        assert "Unterminated string literal" in str(exc_info.value)
        assert exc_info.value.line == 1
        assert exc_info.value.column == 6
    
    def test_invalid_symbol_raises_error(self):
        """Test that invalid symbols raise LexerError."""
        source = "open chrome @invalid"
        lexer = Lexer(source)
        
        with pytest.raises(LexerError) as exc_info:
            lexer.tokenize()
        
        assert "Unexpected character" in str(exc_info.value)
        assert '@' in str(exc_info.value)
    
    def test_empty_source(self):
        """Test tokenization of empty source."""
        source = ""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        assert len(tokens) == 0
    
    def test_only_whitespace(self):
        """Test tokenization of source with only whitespace."""
        source = "   \n\t  \n  "
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        assert len(tokens) == 0
    
    def test_only_comments(self):
        """Test tokenization of source with only comments."""
        source = "# This is a comment\n# Another comment"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        assert len(tokens) == 0
    
    def test_multiline_string_error(self):
        """Test that strings spanning multiple lines raise error."""
        source = 'type "line1\nline2"'
        lexer = Lexer(source)
        
        with pytest.raises(LexerError) as exc_info:
            lexer.tokenize()
        
        assert "Unterminated string literal" in str(exc_info.value)

