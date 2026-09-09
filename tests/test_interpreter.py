"""
Unittest Suite for Interpreter (interpreter.py) and End-to-End Pipeline Integration.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from tac import TACGenerator
from tac_opt import optimize_tac
from interpreter import Interpreter
from errors import RuntimeError


class TestInterpreter(unittest.TestCase):

    def test_execution_valid_program(self):
        source = "int sum = 0;\nint i = 1;\nwhile (i <= 5) {\n sum = sum + i;\n i = i + 1;\n}\nprint(sum);"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        insts = TACGenerator().generate(ast)
        vm = Interpreter(insts)
        output = vm.run()

        self.assertEqual(output, [15])

    def test_division_by_zero_raises_runtime_error(self):
        source = "int x = 42;\nint y = 0;\nprint(x / y);"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        insts = TACGenerator().generate(ast)
        vm = Interpreter(insts)

        with self.assertRaises(RuntimeError) as cm:
            vm.run()

        err = cm.exception
        self.assertIn("Division by zero", err.message)

    def test_end_to_end_pipeline_equivalence(self):
        """
        Complete end-to-end integration test:
        source -> lexer -> parser -> semantic -> TAC -> optimizer -> interpreter
        Verifies raw TAC execution output matches optimized TAC execution output.
        """
        source = """
int x = 10;
{
    int y = 20;
    print(x + y);
}
{
    int x = 200;
    print(x);
}
print(x);
"""
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        symtab = SemanticAnalyzer().analyze(ast)
        self.assertIsNotNone(symtab)

        raw_tac = TACGenerator().generate(ast)
        opt_tac = optimize_tac(raw_tac)

        raw_output = Interpreter(raw_tac).run()
        opt_output = Interpreter(opt_tac).run()

        # Both raw TAC and optimized TAC must produce identical observable outputs
        self.assertEqual(raw_output, [30, 200, 10])
        self.assertEqual(opt_output, [30, 200, 10])


if __name__ == "__main__":
    unittest.main()
