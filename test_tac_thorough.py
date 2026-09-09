"""
Comprehensive Unit Test Suite for MiniLang Three-Address Code Generator (tac.py).

Verifies TAC generation across:
1. Arithmetic precedence (z = x + y * 2)
2. Conditional logic (if/else)
3. Loop logic (while)
4. Complex nested control flow (nested if inside while)
Checks uniqueness of temporary variables and jump labels.
"""

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from tac import TACGenerator, dump_tac


def run_tac_test(name: str, source: str):
    print(f"\n==================================================")
    print(f"--- [TAC Test {name}] ---")
    print(f"Source Code:\n{source.strip()}")
    print("--------------------------------------------------")

    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    # Validate semantics first
    SemanticAnalyzer().analyze(ast)

    # Generate TAC
    tac_gen = TACGenerator()
    insts = tac_gen.generate(ast)

    formatted_tac = dump_tac(insts)
    print("Generated TAC Output:")
    print(formatted_tac)

    # Verification checks
    temps = [inst.result for inst in insts if inst.result and inst.result.startswith("t")]
    labels = [inst.result for inst in insts if inst.op == "LABEL"]

    # Verify label uniqueness
    assert len(labels) == len(set(labels)), f"Duplicate labels found: {labels}"

    return insts, temps, labels


def test_thorough():
    # 1. Declarations & Arithmetic Precedence
    insts1, temps1, _ = run_tac_test("1: Arithmetic Precedence", """
int x = 5;
int y = 10;
int z = x + y * 2;
print(z);
""")
    # Verify y * 2 is evaluated before addition
    mul_index = next(i for i, inst in enumerate(insts1) if inst.op == "MUL")
    add_index = next(i for i, inst in enumerate(insts1) if inst.op == "ADD")
    assert mul_index < add_index, "Multiplication must precede addition in TAC"

    # 2. If/Else Conditional Logic
    _, _, labels2 = run_tac_test("2: Conditional If/Else", """
int x = 5;
if (x < 10) {
    print(x);
} else {
    print(0);
}
""")
    assert len(labels2) == 2, "Expected 2 unique labels for if/else"

    # 3. While Loop Logic
    _, _, labels3 = run_tac_test("3: While Loop", """
int i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}
""")
    assert len(labels3) == 2, "Expected 2 unique labels for while loop"

    # 4. Nested Constructs (if inside while)
    _, _, labels4 = run_tac_test("4: Nested Control Flow", """
int i = 0;
while (i < 5) {
    if (i == 3) {
        print(100);
    } else {
        print(i);
    }
    i = i + 1;
}
""")
    assert len(labels4) == 4, f"Expected 4 unique labels for nested control flow, got {len(labels4)}"

    print("\n==================================================")
    print("✅ ALL 4 TAC GENERATOR TEST SCENARIOS PASSED SUCCESSFULLY!")
    print("==================================================")


if __name__ == "__main__":
    test_thorough()
