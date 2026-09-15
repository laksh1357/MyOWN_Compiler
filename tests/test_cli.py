"""
Unittest Suite for Main CLI Driver & Flags (src/main.py).
"""

import io
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from main import main


class TestCLIDriver(unittest.TestCase):

    def setUp(self):
        self.examples_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../examples"))
        self.valid_file = os.path.join(self.examples_dir, "valid.mini")
        self.syntax_err_file = os.path.join(self.examples_dir, "error_syntax.mini")
        self.semantic_err_file = os.path.join(self.examples_dir, "error_semantic.mini")
        self.runtime_err_file = os.path.join(self.examples_dir, "error_runtime.mini")

    def test_cli_normal_execution(self):
        """Verifies CLI default execution on valid source file."""
        test_args = ["main.py", self.valid_file]
        with patch.object(sys, "argv", test_args):
            captured_stdout = io.StringIO()
            with patch("sys.stdout", captured_stdout):
                main()
            output = captured_stdout.getvalue()
            self.assertIn("PHASE 5: VIRTUAL MACHINE EXECUTION", output)
            self.assertIn("15", output)
            self.assertIn("115", output)

    def test_cli_all_flags(self):
        """Verifies CLI --all flag displays output for all pipeline phases."""
        test_args = ["main.py", self.valid_file, "--all"]
        with patch.object(sys, "argv", test_args):
            captured_stdout = io.StringIO()
            with patch("sys.stdout", captured_stdout):
                main()
            output = captured_stdout.getvalue()
            self.assertIn("PHASE 1: LEXICAL ANALYSIS", output)
            self.assertIn("PHASE 2: SYNTAX ANALYSIS", output)
            self.assertIn("PHASE 3: SEMANTIC ANALYSIS", output)
            self.assertIn("PHASE 4: THREE-ADDRESS CODE", output)
            self.assertIn("PHASE 4b: THREE-ADDRESS CODE (OPTIMIZED)", output)
            self.assertIn("PHASE 5: VIRTUAL MACHINE EXECUTION", output)

    def test_cli_explain_flag(self):
        """Verifies CLI --explain flag displays pipeline educational walk-through."""
        test_args = ["main.py", self.valid_file, "--explain"]
        with patch.object(sys, "argv", test_args):
            captured_stdout = io.StringIO()
            with patch("sys.stdout", captured_stdout):
                main()
            output = captured_stdout.getvalue()
            self.assertIn("SUDARSHAN COMPILER PIPELINE EXPLANATION", output)

    def test_cli_syntax_error_handling(self):
        """Verifies CLI handles syntax error with system exit 1 and clean stderr message."""
        test_args = ["main.py", self.syntax_err_file]
        with patch.object(sys, "argv", test_args):
            captured_stderr = io.StringIO()
            with patch("sys.stderr", captured_stderr):
                with self.assertRaises(SystemExit) as cm:
                    main()
                self.assertEqual(cm.exception.code, 1)
            err_msg = captured_stderr.getvalue()
            self.assertIn("SYNTAX ERROR", err_msg)

    def test_cli_semantic_error_handling(self):
        """Verifies CLI handles semantic error with system exit 1 and clean stderr message."""
        test_args = ["main.py", self.semantic_err_file]
        with patch.object(sys, "argv", test_args):
            captured_stderr = io.StringIO()
            with patch("sys.stderr", captured_stderr):
                with self.assertRaises(SystemExit) as cm:
                    main()
                self.assertEqual(cm.exception.code, 1)
            err_msg = captured_stderr.getvalue()
            self.assertIn("SEMANTIC ERROR", err_msg)

    def test_cli_runtime_error_handling(self):
        """Verifies CLI handles VM runtime error with system exit 1 and clean stderr message."""
        test_args = ["main.py", self.runtime_err_file]
        with patch.object(sys, "argv", test_args):
            captured_stderr = io.StringIO()
            with patch("sys.stderr", captured_stderr):
                with self.assertRaises(SystemExit) as cm:
                    main()
                self.assertEqual(cm.exception.code, 1)
            err_msg = captured_stderr.getvalue()
            self.assertIn("RUNTIME ERROR", err_msg)

    def test_cli_missing_file_handling(self):
        """Verifies CLI handles missing file with system exit 1."""
        test_args = ["main.py", "non_existent_file.mini"]
        with patch.object(sys, "argv", test_args):
            captured_stderr = io.StringIO()
            with patch("sys.stderr", captured_stderr):
                with self.assertRaises(SystemExit) as cm:
                    main()
                self.assertEqual(cm.exception.code, 1)
            err_msg = captured_stderr.getvalue()
            self.assertIn("not found", err_msg)

    def test_cli_viz_fallback_handling(self):
        """Verifies CLI --viz flag graceful fallback when graphviz is missing."""
        test_args = ["main.py", self.valid_file, "--viz"]
        with patch.object(sys, "argv", test_args):
            captured_stdout = io.StringIO()
            with patch("sys.stdout", captured_stdout):
                with patch("shutil.which", return_value=None):
                    with patch("sys.modules", {**sys.modules, "graphviz": None}):
                        main()
            output = captured_stdout.getvalue()
            self.assertIn("Graphviz not installed. Skipping AST image generation.", output)


if __name__ == "__main__":
    unittest.main()
