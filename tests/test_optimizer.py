"""
Unittest Suite for TAC Optimizer (tac_opt.py).
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

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

    def test_algebraic_identity_simplification(self):
        """Tests algebraic identity simplifications (x+0, x-0, x*1, x/1, x*0, x-x, x==x)."""
        insts = [
            TACInstruction("ADD", "x", 0, "t1"),        # t1 = x + 0 -> ASSIGN x t1
            TACInstruction("ADD", 0, "y", "t2"),        # t2 = 0 + y -> ASSIGN y t2
            TACInstruction("SUB", "z", 0, "t3"),        # t3 = z - 0 -> ASSIGN z t3
            TACInstruction("MUL", "a", 1, "t4"),        # t4 = a * 1 -> ASSIGN a t4
            TACInstruction("MUL", 1, "b", "t5"),        # t5 = 1 * b -> ASSIGN b t5
            TACInstruction("DIV", "c", 1, "t6"),        # t6 = c / 1 -> ASSIGN c t6
            TACInstruction("MUL", "d", 0, "t7"),        # t7 = d * 0 -> CONST 0 t7
            TACInstruction("SUB", "e", "e", "t8"),      # t8 = e - e -> CONST 0 t8
            TACInstruction("EQ", "f", "f", "t9"),       # t9 = f == f -> CONST 1 t9
        ]
        opt = optimize_tac(insts)

        # Check t1 -> ASSIGN x
        t1_inst = [i for i in opt if i.result == "t1"][0]
        self.assertEqual(t1_inst.op, "ASSIGN")
        self.assertEqual(t1_inst.arg1, "x")

        # Check t2 -> ASSIGN y
        t2_inst = [i for i in opt if i.result == "t2"][0]
        self.assertEqual(t2_inst.op, "ASSIGN")
        self.assertEqual(t2_inst.arg1, "y")

        # Check t3 -> ASSIGN z
        t3_inst = [i for i in opt if i.result == "t3"][0]
        self.assertEqual(t3_inst.op, "ASSIGN")
        self.assertEqual(t3_inst.arg1, "z")

        # Check t4 -> ASSIGN a
        t4_inst = [i for i in opt if i.result == "t4"][0]
        self.assertEqual(t4_inst.op, "ASSIGN")
        self.assertEqual(t4_inst.arg1, "a")

        # Check t5 -> ASSIGN b
        t5_inst = [i for i in opt if i.result == "t5"][0]
        self.assertEqual(t5_inst.op, "ASSIGN")
        self.assertEqual(t5_inst.arg1, "b")

        # Check t6 -> ASSIGN c
        t6_inst = [i for i in opt if i.result == "t6"][0]
        self.assertEqual(t6_inst.op, "ASSIGN")
        self.assertEqual(t6_inst.arg1, "c")

        # Check t7 -> CONST 0
        t7_inst = [i for i in opt if i.result == "t7"][0]
        self.assertEqual(t7_inst.op, "CONST")
        self.assertEqual(t7_inst.arg1, 0)

        # Check t8 -> CONST 0
        t8_inst = [i for i in opt if i.result == "t8"][0]
        self.assertEqual(t8_inst.op, "CONST")
        self.assertEqual(t8_inst.arg1, 0)

        # Check t9 -> CONST 1
        t9_inst = [i for i in opt if i.result == "t9"][0]
        self.assertEqual(t9_inst.op, "CONST")
        self.assertEqual(t9_inst.arg1, 1)


if __name__ == "__main__":
    unittest.main()

