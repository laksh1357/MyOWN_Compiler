"""
Unittest Suite for Compiler Exception Hierarchy & Error Formatting (errors.py).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from errors import (
    CompilerError,
    CompilerRuntimeError,
    LexerError,
    MiniLangError,
    ParserError,
    SemanticError,
    SudarshanError,
    TACError,
)


class TestErrorHierarchy(unittest.TestCase):

    def test_exception_inheritance_hierarchy(self):
        """Verifies that all phase exceptions inherit from SudarshanError & CompilerError."""
        self.assertTrue(issubclass(LexerError, SudarshanError))
        self.assertTrue(issubclass(ParserError, SudarshanError))
        self.assertTrue(issubclass(SemanticError, SudarshanError))
        self.assertTrue(issubclass(TACError, SudarshanError))
        self.assertTrue(issubclass(CompilerRuntimeError, SudarshanError))

        self.assertTrue(issubclass(SudarshanError, CompilerError))
        self.assertTrue(issubclass(SudarshanError, MiniLangError))

    def test_error_formatting_line_column(self):
        """Verifies error message formatting with line & column numbers."""
        err = LexerError("Unexpected character '$'", line=5, column=12)
        msg = str(err)
        self.assertIn("LexerError: Unexpected character '$' at line 5, column 12", msg)

    def test_error_formatting_with_source_context(self):
        """Verifies error message formatting with source code context snippet."""
        err = ParserError("Missing semicolon", line=3, column=10, source_context="int x = 5")
        msg = str(err)
        self.assertIn("ParserError: Missing semicolon at line 3, column 10", msg)
        self.assertIn("Context: int x = 5", msg)

    def test_polymorphic_exception_catching(self):
        """Verifies catching any compiler error polymorphically with CompilerError."""
        try:
            raise SemanticError("Undeclared variable 'x'", line=2)
        except CompilerError as e:
            self.assertEqual(e.line, 2)
            self.assertIn("Undeclared variable 'x'", str(e))


if __name__ == "__main__":
    unittest.main()
