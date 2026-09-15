"""
Unittest Suite for Lexical Analyzer (lexer.py).
"""

import unittest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from lexer import Lexer, TokenType
from errors import LexerError


class TestLexer(unittest.TestCase):

    def test_valid_tokens(self):
        source = "int count = 100;"
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        self.assertEqual(len(tokens), 6)
        self.assertEqual(tokens[0].type, TokenType.INT)
        self.assertEqual(tokens[1].type, TokenType.ID)
        self.assertEqual(tokens[1].value, "count")
        self.assertEqual(tokens[2].type, TokenType.ASSIGN)
        self.assertEqual(tokens[3].type, TokenType.NUMBER)
        self.assertEqual(tokens[3].value, 100)
        self.assertEqual(tokens[4].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[5].type, TokenType.EOF)

    def test_operators_and_punctuation(self):
        source = "+ - * / == != < > <= >= ( ) { } ;"
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        expected_types = [
            TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH,
            TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.GT,
            TokenType.LE, TokenType.GE, TokenType.LPAREN, TokenType.RPAREN,
            TokenType.LBRACE, TokenType.RBRACE, TokenType.SEMICOLON, TokenType.EOF
        ]
        actual_types = [t.type for t in tokens]
        self.assertEqual(actual_types, expected_types)

    def test_comments_and_whitespace(self):
        source = "// This is a comment\nint x = 5; // inline comment"
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        self.assertEqual(tokens[0].type, TokenType.INT)
        self.assertEqual(tokens[1].value, "x")
        self.assertEqual(tokens[3].value, 5)

    def test_invalid_character_raises_lexer_error(self):
        source = "int x = @ 5;"
        lexer = Lexer(source)
        with self.assertRaises(LexerError) as cm:
            lexer.tokenize()

        err = cm.exception
        self.assertEqual(err.line, 1)
        self.assertEqual(err.column, 9)
        self.assertIn("Unexpected character '@'", err.message)


if __name__ == "__main__":
    unittest.main()
