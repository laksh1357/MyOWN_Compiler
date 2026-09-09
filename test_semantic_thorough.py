"""
Comprehensive Unit Test Suite for MiniLang Semantic Analyzer (semantic.py & symbol_table.py).

Verifies 4 valid semantic test cases (simple decl, parent scope access, shadowing, nested initialization)
and 3 invalid semantic test cases (undeclared variable, duplicate declaration, scope leakage).
"""

from errors import SemanticError
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer


def run_valid_semantic_test(name: str, source: str):
    print(f"\n--- [Valid Semantic Test {name}] ---")
    print(f"Source Code:\n{source.strip()}")
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    analyzer = SemanticAnalyzer()
    symtab = analyzer.analyze(ast)
    print("  ✓ Semantic Validation Succeeded!")
    return symtab


def run_invalid_semantic_test(name: str, source: str, expected_substring: str):
    print(f"\n--- [Invalid Semantic Test {name}] ---")
    print(f"Source Code:\n{source.strip()}")
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    analyzer = SemanticAnalyzer()
    try:
        analyzer.analyze(ast)
        assert False, f"Test '{name}' failed: Expected SemanticError was not raised."
    except SemanticError as err:
        print(f"  ✓ Successfully caught expected error: {err}")
        assert err.line is not None and err.column is not None, "Error missing line/column info"
        assert expected_substring in err.message, f"Expected '{expected_substring}' in message, got '{err.message}'"


def test_thorough():
    print("==================================================")
    print("    MINILANG SEMANTIC ANALYSIS THOROUGH SUITE     ")
    print("==================================================")

    # 1. Valid: Declaration & print
    run_valid_semantic_test("1: Simple Declaration & Print", """
int x = 10;
print(x);
""")

    # 2. Valid: Outer variable visible in inner block
    run_valid_semantic_test("2: Parent Scope Access", """
int x = 10;
{
    int y = 20;
    print(x + y);
}
""")

    # 3. Valid: Shadowing outer variable in inner block
    run_valid_semantic_test("3: Inner Scope Shadowing", """
int x = 10;
{
    int x = 20;
    print(x);
}
""")

    # 4. Valid: Outer variable used to initialize inner variable
    run_valid_semantic_test("4: Parent Scope Access in Inner Initializer", """
int x = 10;
{
    int y = x + 5;
    print(y);
}
""")

    # 5. Invalid: Undeclared variable print(x)
    run_invalid_semantic_test("5: Undeclared Variable Access", "print(x);", "Undeclared variable 'x'")

    # 6. Invalid: Duplicate declaration in same scope
    run_invalid_semantic_test("6: Duplicate Declaration in Same Scope", """
int x = 10;
int x = 20;
""", "Variable 'x' is already declared in this scope")

    # 7. Invalid: Inner block variable accessed outside block
    run_invalid_semantic_test("7: Inner Scope Leakage Outside Block", """
{
    int x = 10;
}
print(x);
""", "Undeclared variable 'x'")

    print("\n==================================================")
    print("✅ ALL 7 SEMANTIC TEST SCENARIOS PASSED SUCCESSFULLY!")
    print("==================================================")


if __name__ == "__main__":
    test_thorough()
