"""Unit tests for the TaskLang semantic analyzer."""

import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer, SemanticError


class TestSemanticAnalyzer:
    """Test cases for the SemanticAnalyzer class."""
    
    def test_go_before_open_raises_error(self):
        """Test that 'go' before 'open' raises semantic error."""
        source = "go https://google.com"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        
        with pytest.raises(SemanticError) as exc_info:
            analyzer.analyze()
        
        assert "Cannot navigate to URL" in str(exc_info.value)
        assert "before opening a browser" in str(exc_info.value)
        assert exc_info.value.line == 1
    
    def test_negative_wait_raises_error(self):
        """Test that negative wait value raises semantic error."""
        source = "open chrome\nwait -5"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        
        with pytest.raises(SemanticError) as exc_info:
            analyzer.analyze()
        
        assert "Wait time must be greater than 0" in str(exc_info.value)
        assert exc_info.value.line == 2
    
    def test_zero_wait_raises_error(self):
        """Test that zero wait value raises semantic error."""
        source = "open chrome\nwait 0"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        
        with pytest.raises(SemanticError) as exc_info:
            analyzer.analyze()
        
        assert "Wait time must be greater than 0" in str(exc_info.value)
        assert exc_info.value.line == 2
    
    def test_valid_program_passes(self):
        """Test that a valid program passes semantic analysis."""
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
        
        analyzer = SemanticAnalyzer(ast)
        # Should not raise any exception
        analyzer.analyze()
    
    def test_type_before_go_raises_error(self):
        """Test that 'type' before 'go' raises semantic error."""
        source = "open chrome\ntype \"hello\""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        
        with pytest.raises(SemanticError) as exc_info:
            analyzer.analyze()
        
        assert "Cannot type text" in str(exc_info.value)
        assert "before loading a page" in str(exc_info.value)
        assert exc_info.value.line == 2
    
    def test_enter_before_go_raises_error(self):
        """Test that 'enter' before 'go' raises semantic error."""
        source = "open chrome\nenter"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        
        with pytest.raises(SemanticError) as exc_info:
            analyzer.analyze()
        
        assert "Cannot press Enter" in str(exc_info.value)
        assert "before loading a page" in str(exc_info.value)
        assert exc_info.value.line == 2
    
    def test_screenshot_before_open_raises_error(self):
        """Test that 'screenshot' before 'open' raises semantic error."""
        source = "screenshot test.png"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        
        with pytest.raises(SemanticError) as exc_info:
            analyzer.analyze()
        
        assert "Cannot take screenshot" in str(exc_info.value)
        assert "before opening a browser" in str(exc_info.value)
        assert exc_info.value.line == 1
    
    def test_close_before_open_raises_error(self):
        """Test that 'close' before 'open' raises semantic error."""
        source = "close"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        
        with pytest.raises(SemanticError) as exc_info:
            analyzer.analyze()
        
        assert "Cannot close browser" in str(exc_info.value)
        assert "before opening one" in str(exc_info.value)
        assert exc_info.value.line == 1
    
    def test_multiple_opens_allowed(self):
        """Test that multiple 'open' statements are allowed."""
        source = "open chrome\nopen firefox"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        # Should not raise any exception
        analyzer.analyze()
    
    def test_go_resets_page_loaded(self):
        """Test that opening a new browser resets page_loaded state."""
        source = """open chrome
go https://google.com
open firefox
type "test\""""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        
        # Should fail because type comes after a new open without a go
        with pytest.raises(SemanticError) as exc_info:
            analyzer.analyze()
        
        assert "Cannot type text" in str(exc_info.value)
        assert exc_info.value.line == 4
    
    def test_wait_with_positive_value_passes(self):
        """Test that wait with positive value passes."""
        source = "open chrome\nwait 1"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        # Should not raise any exception
        analyzer.analyze()
    
    def test_empty_program_passes(self):
        """Test that empty program passes semantic analysis."""
        source = ""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        # Should not raise any exception
        analyzer.analyze()
    
    def test_screenshot_after_open_passes(self):
        """Test that screenshot after open passes."""
        source = "open chrome\nscreenshot test.png"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        # Should not raise any exception
        analyzer.analyze()
    
    def test_close_after_open_passes(self):
        """Test that close after open passes."""
        source = "open chrome\nclose"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        # Should not raise any exception
        analyzer.analyze()

