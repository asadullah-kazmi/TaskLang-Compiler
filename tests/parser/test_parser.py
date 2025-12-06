"""Unit tests for the TaskLang parser."""

import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser, ParserError
from src.parser.ast import (
    ProgramNode, OpenNode, GoNode, TypeNode, EnterNode,
    WaitNode, ScreenshotNode, CloseNode
)


class TestParser:
    """Test cases for the Parser class."""
    
    def test_valid_program_produces_program_node(self):
        """Test that a valid program produces a ProgramNode with correct child nodes."""
        source = """open chrome
go https://google.com
type "compiler project"
enter
wait 2
screenshot test.png"""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 6
        
        # Check statement types
        assert isinstance(ast.statements[0], OpenNode)
        assert isinstance(ast.statements[1], GoNode)
        assert isinstance(ast.statements[2], TypeNode)
        assert isinstance(ast.statements[3], EnterNode)
        assert isinstance(ast.statements[4], WaitNode)
        assert isinstance(ast.statements[5], ScreenshotNode)
        
        # Check values
        assert ast.statements[0].browser == 'chrome'
        assert ast.statements[1].url == 'https://google.com'
        assert ast.statements[2].text == 'compiler project'
        assert ast.statements[4].seconds == 2
        assert ast.statements[5].filename == 'test.png'
    
    def test_open_statement(self):
        """Test parsing of 'open' statement."""
        source = "open chrome"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], OpenNode)
        assert ast.statements[0].browser == 'chrome'
    
    def test_go_statement(self):
        """Test parsing of 'go' statement."""
        source = "go https://example.com"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], GoNode)
        assert ast.statements[0].url == 'https://example.com'
    
    def test_type_statement(self):
        """Test parsing of 'type' statement."""
        source = 'type "hello world"'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], TypeNode)
        assert ast.statements[0].text == 'hello world'
    
    def test_enter_statement(self):
        """Test parsing of 'enter' statement."""
        source = "enter"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], EnterNode)
    
    def test_wait_statement(self):
        """Test parsing of 'wait' statement."""
        source = "wait 5"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], WaitNode)
        assert ast.statements[0].seconds == 5
    
    def test_screenshot_statement(self):
        """Test parsing of 'screenshot' statement."""
        source = "screenshot output.png"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], ScreenshotNode)
        assert ast.statements[0].filename == 'output.png'
    
    def test_close_statement(self):
        """Test parsing of 'close' statement."""
        source = "close"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], CloseNode)
    
    def test_type_without_string_raises_error(self):
        """Test that TYPE without STRING causes syntax error."""
        source = "type"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        with pytest.raises(ParserError) as exc_info:
            parser.parse()
        
        assert "Expected string literal after 'type'" in str(exc_info.value)
        assert exc_info.value.line == 1
    
    def test_wait_without_number_raises_error(self):
        """Test that WAIT without NUMBER causes syntax error."""
        source = "wait"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        with pytest.raises(ParserError) as exc_info:
            parser.parse()
        
        assert "Expected number after 'wait'" in str(exc_info.value)
        assert exc_info.value.line == 1
    
    def test_open_without_identifier_raises_error(self):
        """Test that OPEN without IDENTIFIER causes syntax error."""
        source = "open"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        with pytest.raises(ParserError) as exc_info:
            parser.parse()
        
        assert "Expected browser identifier after 'open'" in str(exc_info.value)
        assert exc_info.value.line == 1
    
    def test_go_without_url_raises_error(self):
        """Test that GO without URL causes syntax error."""
        source = "go"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        with pytest.raises(ParserError) as exc_info:
            parser.parse()
        
        assert "Expected URL after 'go'" in str(exc_info.value)
        assert exc_info.value.line == 1
    
    def test_screenshot_without_identifier_raises_error(self):
        """Test that SCREENSHOT without IDENTIFIER causes syntax error."""
        source = "screenshot"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        with pytest.raises(ParserError) as exc_info:
            parser.parse()
        
        assert "Expected filename after 'screenshot'" in str(exc_info.value)
        assert exc_info.value.line == 1
    
    def test_empty_program(self):
        """Test parsing of empty program."""
        source = ""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 0
    
    def test_multiple_statements(self):
        """Test parsing of multiple statements."""
        source = """open chrome
go https://test.com
type "test"
enter"""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert len(ast.statements) == 4
        assert isinstance(ast.statements[0], OpenNode)
        assert isinstance(ast.statements[1], GoNode)
        assert isinstance(ast.statements[2], TypeNode)
        assert isinstance(ast.statements[3], EnterNode)
    
    def test_wrong_token_type_raises_error(self):
        """Test that wrong token type raises syntax error."""
        source = "open https://test.com"  # Should be IDENTIFIER, not URL
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        with pytest.raises(ParserError) as exc_info:
            parser.parse()
        
        assert "Expected browser identifier after 'open'" in str(exc_info.value)
        assert "but found URL" in str(exc_info.value)
    
    def test_wait_with_large_number(self):
        """Test parsing of wait with large number."""
        source = "wait 1000"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert ast.statements[0].seconds == 1000

