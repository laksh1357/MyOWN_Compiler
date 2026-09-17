"""
Unittest Suite for AST Graphviz Visualization & Fallback Behavior (ast_nodes.py).
"""

import io
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from ast_nodes import BinaryExpr, IntegerLiteral, Program, VarDecl, export_ast_dot, render_ast_graph
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from tac import TACGenerator
from tac_opt import optimize_tac


class TestASTVisualization(unittest.TestCase):

    def test_export_ast_dot(self):
        """Verifies that export_ast_dot constructs valid Graphviz DOT syntax."""
        ast = Program([
            VarDecl("int", "x", BinaryExpr(IntegerLiteral(5), "+", IntegerLiteral(10)))
        ])
        dot_str = export_ast_dot(ast)

        self.assertIn("digraph AST {", dot_str)
        self.assertIn("VarDecl(int x)", dot_str)
        self.assertIn("BinaryExpr('+\')", dot_str)
        self.assertIn("IntegerLiteral(5)", dot_str)
        self.assertIn("IntegerLiteral(10)", dot_str)
        self.assertIn("}", dot_str)

    def test_render_ast_graph_missing_graphviz_fallback(self):
        """
        Verifies that render_ast_graph gracefully falls back and prints a warning
        when graphviz library or dot binary is unavailable, without raising exceptions.
        """
        ast = Program([VarDecl("int", "a", IntegerLiteral(42))])

        with patch("shutil.which", return_value=None):
            with patch("sys.modules", {**sys.modules, "graphviz": None}):
                captured_stdout = io.StringIO()
                with patch("sys.stdout", captured_stdout):
                    result = render_ast_graph(ast, "test_output")

                self.assertFalse(result)
                output = captured_stdout.getvalue()
                self.assertIn("Graphviz not installed. Skipping AST image generation.", output)

    def test_pipeline_continues_when_graphviz_fails(self):
        """
        Integration test: Verifies that full compilation and VM execution succeed
        even if AST visualization fails or is skipped.
        """
        source = "int x = 100;\nprint(x * 2);"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()

        # Simulate graphviz failure
        with patch("ast_nodes.render_ast_graph", return_value=False):
            symtab = SemanticAnalyzer().analyze(ast)
            raw_tac = TACGenerator().generate(ast)
            opt_tac = optimize_tac(raw_tac)
            output = Interpreter(opt_tac).run()

        self.assertEqual(output, [200])


    def test_render_ast_graph_uses_output_directory(self):
        """Verifies that render_ast_graph routes output files to a dedicated directory."""
        from pathlib import Path
        ast = Program([VarDecl("int", "x", IntegerLiteral(10))])

        with patch("shutil.which", return_value=None):
            with patch("sys.modules", {**sys.modules, "graphviz": None}):
                with patch.object(Path, "mkdir") as mock_mkdir:
                    render_ast_graph(ast, "my_ast")
                    mock_mkdir.assert_called()


if __name__ == "__main__":
    unittest.main()

