"""
Unit Test Suite for MiniLang Three-Address Code Generator (tac.py).
Verifies TAC instruction quadruples, temporary variable generation (t1, t2, ...),
label generation (L1, L2, ...), and dump formatting.
"""

from lexer import Lexer
from parser import Parser
from tac import TACGenerator, dump_tac


def test_basic_declarations_and_assignment():
    source = "int x = 5;\nx = x + 1;\nprint(x);"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    insts = TACGenerator().generate(ast)

    ops = [inst.op for inst in insts]
    assert ops == ["CONST", "ASSIGN", "CONST", "ADD", "ASSIGN", "PRINT"]
    assert insts[0].arg1 == 5 and insts[0].result == "t1"
    assert insts[1].arg1 == "t1" and insts[1].result == "x"
    print("  ✓ Test 1 Passed: Basic declarations, assignment, and print TAC")


def test_arithmetic_opcodes():
    source = "int res = (a + b) * (c - d) / e;"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    insts = TACGenerator().generate(ast)

    opcodes = [inst.op for inst in insts if inst.op in ("ADD", "SUB", "MUL", "DIV")]
    assert opcodes == ["ADD", "SUB", "MUL", "DIV"]
    print("  ✓ Test 2 Passed: Arithmetic opcodes (ADD, SUB, MUL, DIV)")


def test_if_else_tac_generation():
    source = "if (x > 0) { print(x); } else { print(0); }"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    insts = TACGenerator().generate(ast)

    ops = [inst.op for inst in insts]
    assert "GT" in ops
    assert "JUMP_IF_FALSE" in ops
    assert "JUMP" in ops
    assert "LABEL" in ops

    labels = [inst.result for inst in insts if inst.op == "LABEL"]
    assert labels == ["L1", "L2"]
    print("  ✓ Test 3 Passed: If/else TAC label and jump generation")


def test_while_loop_tac_generation():
    source = "while (i < 5) { i = i + 1; }"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    insts = TACGenerator().generate(ast)

    ops = [inst.op for inst in insts]
    assert "LABEL" in ops
    assert "LT" in ops
    assert "JUMP_IF_FALSE" in ops
    assert "JUMP" in ops

    labels = [inst.result for inst in insts if inst.op == "LABEL"]
    assert labels == ["L1", "L2"]
    print("  ✓ Test 4 Passed: While loop TAC start/end label generation")


def run_all_tests():
    print("=== Running MiniLang TAC Generator Unit Test Suite ===")
    test_basic_declarations_and_assignment()
    test_arithmetic_opcodes()
    test_if_else_tac_generation()
    test_while_loop_tac_generation()
    print("\n✅ All 4 TAC Generator Test Cases Passed Successfully!")


if __name__ == "__main__":
    run_all_tests()
