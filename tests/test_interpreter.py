"""
Unittest Suite for Interpreter (interpreter.py) and End-to-End Pipeline Integration.
"""

import builtins
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from errors import CompilerRuntimeError
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from tac import TACGenerator
from tac_opt import optimize_tac


class TestInterpreter(unittest.TestCase):

    def test_custom_runtime_error_distinct_from_python_builtin(self):
        """Regression test: Ensures CompilerRuntimeError does not shadow builtins.RuntimeError."""
        self.assertIsNot(CompilerRuntimeError, builtins.RuntimeError)
        self.assertTrue(issubclass(CompilerRuntimeError, Exception))
        self.assertFalse(issubclass(builtins.RuntimeError, CompilerRuntimeError))

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

        with self.assertRaises(CompilerRuntimeError) as cm:
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


    def test_relational_and_unary_tac_execution(self):
        """Tests TAC execution for unary negation and comparison operators (<, >, <=, >=, ==, !=)."""
        source = """
int a = -10;
int b = 20;
print(-a);
if (a < b) { print(1); } else { print(0); }
if (a > b) { print(1); } else { print(0); }
if (a <= -10) { print(1); } else { print(0); }
if (b >= 20) { print(1); } else { print(0); }
if (a != b) { print(1); } else { print(0); }
if (a == b) { print(1); } else { print(0); }
"""
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        insts = TACGenerator().generate(ast)
        vm = Interpreter(insts)
        output = vm.run()

        self.assertEqual(output, [10, 1, 0, 1, 1, 1, 0])

    def test_undefined_variable_access_raises_runtime_error(self):
        """Tests that accessing an uninitialized variable in VM raises CompilerRuntimeError."""
        from tac import TACInstruction
        insts = [TACInstruction("PRINT", "uninitialized_var", None, None)]
        vm = Interpreter(insts)
        with self.assertRaises(CompilerRuntimeError) as cm:
            vm.run()
        self.assertIn("Undefined variable", cm.exception.message)

    def test_undefined_jump_target_raises_runtime_error(self):
        """Tests that jumping to an undefined label raises CompilerRuntimeError."""
        from tac import TACInstruction
        insts = [TACInstruction("JUMP", None, None, "L999")]
        vm = Interpreter(insts)
        with self.assertRaises(CompilerRuntimeError) as cm:
            vm.run()
        self.assertIn("Undefined jump label target", cm.exception.message)

    def test_invalid_opcode_raises_runtime_error(self):
        """Tests that executing an unknown opcode raises CompilerRuntimeError."""
        from tac import TACInstruction
        insts = [TACInstruction("UNKNOWN_OP", 1, 2, "t1")]
        vm = Interpreter(insts)
        with self.assertRaises(CompilerRuntimeError) as cm:
            vm.run()
        self.assertIn("Invalid instruction", cm.exception.message)


if __name__ == "__main__":
    unittest.main()

