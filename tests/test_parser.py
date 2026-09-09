"""
Unittest Suite for Syntax Analyzer / Parser (parser.py).
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lexer import Lexer
from parser import Parser
from ast_nodes import (
    Program, VarDecl, Assignment, PrintStmt, IfStmt, WhileStmt,
    Block, BinaryExpr, UnaryExpr, IntegerLiteral, Variable
)
from errors import ParserError


class TestParser(unittest.TestCase):

    def test_operator_precedence(self):
        # int x = 2 + 3 * 4;  =>  + (2, * (3, 4))
        source = "int x = 2 + 3 * 4;"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()

        self.assertIsInstance(ast, Program)
        var_decl = ast.statements[0]
        self.assertIsInstance(var_decl, VarDecl)

        bin_add = var_decl.initializer
        self.assertIsInstance(bin_add, BinaryExpr)
        self.assertEqual(bin_add.operator, "+")
        self.assertIsInstance(bin_add.right, BinaryExpr)
        self.assertEqual(bin_add.right.operator, "*")

    def test_parentheses(self):
        # int x = (2 + 3) * 4;  =>  * (+ (2, 3), 4)
        source = "int x = (2 + 3) * 4;"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()

        var_decl = ast.statements[0]
        bin_mul = var_decl.initializer
        self.assertIsInstance(bin_mul, BinaryExpr)
        self.assertEqual(bin_mul.operator, "*")
        self.assertIsInstance(bin_mul.left, BinaryExpr)
        self.assertEqual(bin_mul.left.operator, "+")

    def test_unary_minus(self):
        source = "int x = -5;"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()

        var_decl = ast.statements[0]
        un_expr = var_decl.initializer
        self.assertIsInstance(un_expr, UnaryExpr)
        self.assertEqual(un_expr.operator, "-")
        self.assertIsInstance(un_expr.operand, IntegerLiteral)
        self.assertEqual(un_expr.operand.value, 5)

    def test_if_else_and_while(self):
        source = "if (x > 0) { print(x); } else { print(0); }"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()

        if_stmt = ast.statements[0]
        self.assertIsInstance(if_stmt, IfStmt)
        self.assertIsInstance(if_stmt.then_branch, Block)
        self.assertIsInstance(if_stmt.else_branch, Block)

    def test_missing_semicolon_raises_parser_error(self):
        source = "int x = 5\nprint(x);"
        tokens = Lexer(source).tokenize()
        with self.assertRaises(ParserError) as cm:
            Parser(tokens).parse()

        err = cm.exception
        self.assertEqual(err.line, 2)
        self.assertEqual(err.column, 1)
        self.assertIn("Expected ';'", err.message)


if __name__ == "__main__":
    unittest.main()
