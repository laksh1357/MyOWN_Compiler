"""
Comprehensive Unit Test Suite for MiniLang Parser (parser.py).

Covers 15 test scenarios: 11 valid construct tests displaying pretty-printed ASTs,
and 4 invalid construct tests verifying ParserError line and column reporting.
"""

from errors import ParserError
from lexer import Lexer
from parser import Parser
from ast_nodes import dump_ast, Program, VarDecl, Assignment, PrintStmt, IfStmt, WhileStmt, BinaryExpr, UnaryExpr, IntegerLiteral, Variable


def run_valid_test(name: str, source: str):
    print(f"\n--- [Valid Test {name}] ---")
    print(f"Source Code:\n{source}")
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    print("Parsed AST Output:")
    print(dump_ast(ast))
    return ast


def run_invalid_test(name: str, source: str, expected_msg_substring: str):
    print(f"\n--- [Invalid Test {name}] ---")
    print(f"Source Code: {repr(source)}")
    tokens = Lexer(source).tokenize()
    try:
        Parser(tokens).parse()
        assert False, f"Test '{name}' failed: Expected ParserError was not raised."
    except ParserError as err:
        print(f"  ✓ Successfully caught expected error: {err}")
        assert err.line is not None and err.column is not None, "Error missing line/column info"
        assert expected_msg_substring in err.message, f"Expected '{expected_msg_substring}' in message, got '{err.message}'"


def test_thorough():
    print("==================================================")
    print("      MINILANG PARSER THOROUGH TEST SUITE         ")
    print("==================================================")

    # 1. Variable declaration
    run_valid_test("1: Variable Declaration", "int x = 5;")

    # 2. Assignment
    run_valid_test("2: Variable Assignment", "x = x + 1;")

    # 3. Print statement
    run_valid_test("3: Print Statement", "print(x);")

    # 4. Arithmetic Precedence (2 + 3 * 4)
    ast4 = run_valid_test("4: Arithmetic Precedence", "int x = 2 + 3 * 4;")
    init4 = ast4.statements[0].initializer
    assert init4.operator == "+" and init4.right.operator == "*"

    # 5. Parentheses ((2 + 3) * 4)
    ast5 = run_valid_test("5: Parentheses Precedence Override", "int x = (2 + 3) * 4;")
    init5 = ast5.statements[0].initializer
    assert init5.operator == "*" and init5.left.operator == "+"

    # 6. Unary minus
    ast6 = run_valid_test("6: Unary Minus", "int x = -5;")
    init6 = ast6.statements[0].initializer
    assert isinstance(init6, UnaryExpr) and init6.operator == "-"

    # 7. Comparisons (x <= 10)
    run_valid_test("7: Comparison Operator", "int c = x <= 10;")

    # 8. if/else
    run_valid_test("8: If/Else Conditional", "if (x > 0) { print(x); } else { print(0); }")

    # 9. while loop
    run_valid_test("9: While Loop", "while (x < 10) { x = x + 1; }")

    # 10. Nested blocks
    run_valid_test("10: Nested Blocks", "{\n  {\n    int inner = 1;\n  }\n}")

    # 11. else-if chain
    run_valid_test("11: Else-If Chain", "if (x > 0) { print(1); } else if (x < 0) { print(-1); } else { print(0); }")

    # 12. Missing semicolon
    run_invalid_test("12: Missing Semicolon", "int x = 5\nprint(x);", "Expected ';'")

    # 13. Missing closing parenthesis
    run_invalid_test("13: Missing Closing Parenthesis", "print(x;", "Expected ')'")

    # 14. Missing closing brace
    run_invalid_test("14: Missing Closing Brace", "while (x > 0) { print(x);", "Expected '}'")

    # 15. Invalid statement (expression without statement wrapper)
    run_invalid_test("15: Invalid Statement Start", "5 + 5;", "Unexpected statement start token '5'")

    print("\n==================================================")
    print("✅ ALL 15 PARSER TEST SCENARIOS PASSED SUCCESSFULLY!")
    print("==================================================")


if __name__ == "__main__":
    test_thorough()
