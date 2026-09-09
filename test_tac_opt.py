"""
Unit Test Suite for MiniLang TAC Optimizer (tac_opt.py).
Verifies Constant Folding, Constant Propagation, Dead Code Elimination, and zero division safety.
"""

from lexer import Lexer
from parser import Parser
from tac import TACGenerator, TACInstruction
from tac_opt import optimize_tac, compare_optimization


def test_constant_folding_arithmetic():
    source = "int x = 10 + 20 * 3 - 5;"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    raw_tac = TACGenerator().generate(ast)
    opt_tac = optimize_tac(raw_tac)

    # All constants fold to 65
    print_inst = opt_tac[-1]
    assert print_inst.op == "ASSIGN" and print_inst.arg1 == 65
    print("  ✓ Test 1 Passed: Constant folding for arithmetic operations")


def test_constant_folding_comparisons():
    source = "int c1 = 2 < 5;\nint c2 = 10 == 20;"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    raw_tac = TACGenerator().generate(ast)
    opt_tac = optimize_tac(raw_tac)

    const_vals = [inst.arg1 for inst in opt_tac if inst.op == "ASSIGN"]
    assert 1 in const_vals  # 2 < 5 is 1
    assert 0 in const_vals  # 10 == 20 is 0
    print("  ✓ Test 2 Passed: Constant folding for comparison operations")


def test_dead_code_elimination():
    insts = [
        TACInstruction("JUMP", None, None, "L1"),
        TACInstruction("CONST", 42, None, "t1"),
        TACInstruction("PRINT", "t1", None, None),
        TACInstruction("LABEL", None, None, "L1"),
    ]
    opt_insts = optimize_tac(insts)
    ops = [inst.op for inst in opt_insts]
    assert ops == ["JUMP", "LABEL"]
    print("  ✓ Test 3 Passed: Dead code elimination after unconditional GOTO")


def test_division_by_zero_safety():
    source = "int x = 10 / 0;"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    raw_tac = TACGenerator().generate(ast)
    # Optimizer must not crash on 10 / 0 and leave DIV instruction intact for runtime error
    opt_tac = optimize_tac(raw_tac)
    assert any(inst.op == "DIV" for inst in opt_tac)
    print("  ✓ Test 4 Passed: Division by zero safety in TAC Optimizer")


def run_all_tests():
    print("=== Running MiniLang TAC Optimizer Unit Test Suite ===")
    test_constant_folding_arithmetic()
    test_constant_folding_comparisons()
    test_dead_code_elimination()
    test_division_by_zero_safety()
    print("\n✅ All 4 TAC Optimizer Test Cases Passed Successfully!")


if __name__ == "__main__":
    run_all_tests()
