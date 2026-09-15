"""
Unittest Suite for Semantic Analyzer (semantic.py) and Symbol Table (symbol_table.py).
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from errors import SemanticError


class TestSemantic(unittest.TestCase):

    def test_valid_semantic_program(self):
        source = "int x = 10;\n{ int y = 20;\n print(x + y); }"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        analyzer = SemanticAnalyzer()
        symtab = analyzer.analyze(ast)

        self.assertIsNotNone(symtab.lookup("x"))

    def test_undeclared_variable_raises_semantic_error(self):
        source = "print(x);"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        with self.assertRaises(SemanticError) as cm:
            SemanticAnalyzer().analyze(ast)

        err = cm.exception
        self.assertEqual(err.line, 1)
        self.assertEqual(err.column, 7)
        self.assertIn("Undeclared variable 'x'", err.message)

    def test_duplicate_declaration_raises_semantic_error(self):
        source = "int x = 10;\nint x = 20;"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        with self.assertRaises(SemanticError) as cm:
            SemanticAnalyzer().analyze(ast)

        err = cm.exception
        self.assertEqual(err.line, 2)
        self.assertEqual(err.column, 1)
        self.assertIn("Variable 'x' is already declared in this scope", err.message)

    def test_variable_shadowing_allowed(self):
        source = "int x = 10;\n{\n  int x = 20;\n  print(x);\n}"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        analyzer = SemanticAnalyzer()
        # Should not raise exception
        analyzer.analyze(ast)

    def test_block_scope_isolation(self):
        source = "{\n  int x = 10;\n}\nprint(x);"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        with self.assertRaises(SemanticError) as cm:
            SemanticAnalyzer().analyze(ast)

        err = cm.exception
        self.assertEqual(err.line, 4)
        self.assertIn("Undeclared variable 'x'", err.message)


if __name__ == "__main__":
    unittest.main()
