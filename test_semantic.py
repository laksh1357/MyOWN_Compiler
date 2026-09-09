"""
Unit Test Suite for MiniLang Semantic Analyzer (semantic.py).
Verifies declaration validation, scope isolation, shadowing, and error reporting.
"""

from errors import SemanticError
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer


def test_valid_program_semantic():
    source = """
int sum = 0;
int i = 1;
while (i <= 5) {
    sum = sum + i;
    i = i + 1;
}
print(sum);
"""
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    analyzer = SemanticAnalyzer()
    symtab = analyzer.analyze(ast)

    assert symtab.lookup("sum") is not None
    assert symtab.lookup("i") is not None
    print("  ✓ Test 1 Passed: Valid program semantic validation")


def test_undeclared_variable_error():
    source = "int x = 5;\ny = x + 1;"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    try:
        SemanticAnalyzer().analyze(ast)
        assert False, "Expected SemanticError for undeclared variable 'y'"
    except SemanticError as err:
        assert err.line == 2 and err.column == 1
        assert "Cannot assign to undeclared variable 'y'" in err.message
        print("  ✓ Test 2 Passed: Undeclared variable error caught")


def test_duplicate_declaration_error():
    source = "int x = 5;\nint x = 10;"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    try:
        SemanticAnalyzer().analyze(ast)
        assert False, "Expected SemanticError for duplicate variable 'x'"
    except SemanticError as err:
        assert err.line == 2 and err.column == 1
        assert "Variable 'x' is already declared in this scope" in err.message
        print("  ✓ Test 3 Passed: Duplicate declaration in same scope caught")


def test_scope_isolation_error():
    source = """
if (1 > 0) {
    int secret = 42;
}
print(secret);
"""
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    try:
        SemanticAnalyzer().analyze(ast)
        assert False, "Expected SemanticError accessing block-isolated variable 'secret'"
    except SemanticError as err:
        assert err.line == 5 and err.column == 7
        assert "Undeclared variable 'secret'" in err.message
        print("  ✓ Test 4 Passed: Scope isolation error caught")


def test_variable_shadowing_valid():
    source = """
int x = 10;
{
    int x = 20;
    print(x);
}
print(x);
"""
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    print("  ✓ Test 5 Passed: Variable shadowing in nested scope allowed")


def run_all_tests():
    print("=== Running MiniLang Semantic Analyzer Unit Test Suite ===")
    test_valid_program_semantic()
    test_undeclared_variable_error()
    test_duplicate_declaration_error()
    test_scope_isolation_error()
    test_variable_shadowing_valid()
    print("\n✅ All 5 Semantic Analyzer Test Cases Passed Successfully!")


if __name__ == "__main__":
    run_all_tests()
