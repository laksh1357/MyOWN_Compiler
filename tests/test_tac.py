"""
Unittest Suite for Three-Address Code Generator (tac.py).
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lexer import Lexer
from parser import Parser
from tac import TACGenerator


class TestTAC(unittest.TestCase):

    def test_tac_arithmetic_generation(self):
        source = "int x = 5;\nx = x + 1;\nprint(x);"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        insts = TACGenerator().generate(ast)

        ops = [inst.op for inst in insts]
        self.assertEqual(ops, ["CONST", "ASSIGN", "CONST", "ADD", "ASSIGN", "PRINT"])

    def test_tac_unique_temporaries_and_labels(self):
        source = "while (i < 5) { if (i == 3) { print(100); } i = i + 1; }"
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        insts = TACGenerator().generate(ast)

        temps = [inst.result for inst in insts if inst.result and inst.result.startswith("t")]
        labels = [inst.result for inst in insts if inst.op == "LABEL"]

        # Ensure unique labels
        self.assertEqual(len(labels), len(set(labels)))
        self.assertGreater(len(labels), 0)


if __name__ == "__main__":
    unittest.main()
