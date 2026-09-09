"""
Unittest Suite for TAC Optimizer (tac_opt.py).
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lexer import Lexer
from parser import Parser
from tac import TACGenerator, TACInstruction
from tac_opt import optimize_tac


class TestOptimizer(unittest.TestCase):

    def test_constant_folding(self):
        source = "int x = 2 + 3 * 4;"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        raw_tac = TACGenerator().generate(ast)
        opt_tac = optimize_tac(raw_tac)

        print_inst = opt_tac[-1]
        self.assertEqual(print_inst.op, "ASSIGN")
        self.assertEqual(print_inst.arg1, 14)

    def test_dead_code_elimination(self):
        insts = [
            TACInstruction("JUMP", None, None, "L1"),
            TACInstruction("CONST", 42, None, "t1"),
            TACInstruction("PRINT", "t1", None, None),
            TACInstruction("LABEL", None, None, "L1"),
        ]
        opt_insts = optimize_tac(insts)
        ops = [inst.op for inst in opt_insts]
        self.assertEqual(ops, ["JUMP", "LABEL"])

    def test_safe_division_by_zero_not_folded(self):
        source = "int x = 10 / 0;"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        raw_tac = TACGenerator().generate(ast)
        opt_tac = optimize_tac(raw_tac)

        has_div = any(inst.op == "DIV" for inst in opt_tac)
        self.assertTrue(has_div, "Division by zero should not be folded at compile time")


if __name__ == "__main__":
    unittest.main()
