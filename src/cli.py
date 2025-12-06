"""Command-line interface for TaskLang Compiler."""

import sys
import argparse
from pathlib import Path
from .lexer.lexer import Lexer, LexerError
from .parser.parser import Parser, ParserError
from .semantic.analyzer import SemanticAnalyzer, SemanticError
from .codegen.python_gen import PythonCodeGenerator


class TaskLangCLI:
    """Command-line interface for TaskLang Compiler."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create and configure the argument parser.
        
        Returns:
            Configured ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            description='TaskLang Compiler - Compile .task files to Python Selenium automation scripts',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        parser.add_argument(
            'input_file',
            type=str,
            help='Input .task file to compile'
        )
        
        parser.add_argument(
            '--output', '-o',
            type=str,
            default='output',
            help='Output directory for generated Python file (default: output/)'
        )
        
        return parser
    
    def run(self):
        """
        Execute the full compilation pipeline.
        
        This method orchestrates:
        1. Reading the input file
        2. Tokenization (Lexer)
        3. Parsing (Parser)
        4. Semantic analysis (SemanticAnalyzer)
        5. Code generation (PythonCodeGenerator)
        """
        args = self.parser.parse_args()
        
        # Validate and process input file
        input_file = Path(args.input_file)
        
        # Validate file extension
        if not input_file.suffix == '.task':
            print(f"Error: File must have .task extension: {input_file}", file=sys.stderr)
            sys.exit(1)
        
        # Check if file exists
        if not input_file.exists():
            print(f"Error: File not found: {input_file}", file=sys.stderr)
            sys.exit(1)
        
        # Read the file content
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception as e:
            print(f"Error: Failed to read file {input_file}: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Step 1: Tokenize using Lexer
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            # Print all tokens
            print("Tokens:")
            for token in tokens:
                print(token)
            print()
                
        except LexerError as e:
            print(f"Lexer Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: Unexpected error during lexing: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Step 2: Parse tokens to AST using Parser
        try:
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Print AST
            print("AST:")
            print(ast)
            print()
            
        except ParserError as e:
            print(f"Parser Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: Unexpected error during parsing: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Step 3: Perform semantic analysis using SemanticAnalyzer
        try:
            analyzer = SemanticAnalyzer(ast)
            analyzer.analyze()
            print("✅ Semantic Analysis Passed")
            print()
            
        except SemanticError as e:
            print(f"Semantic Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: Unexpected error during semantic analysis: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Step 4: Generate Python Selenium code using PythonCodeGenerator
        try:
            # Determine output filename
            input_filename = input_file.stem  # Get filename without extension
            output_dir = Path(args.output)
            
            # Ensure output directory exists
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Construct output file path
            output_file = output_dir / f"{input_filename}.py"
            
            # Generate code
            generator = PythonCodeGenerator(ast)
            generator.generate(str(output_file))
            
            print(f"✅ Python automation script generated at {output_file}")
            
        except Exception as e:
            print(f"Error: Failed to generate Python code: {e}", file=sys.stderr)
            sys.exit(1)

