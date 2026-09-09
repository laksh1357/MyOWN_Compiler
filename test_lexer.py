"""
Unit Test Suite for MiniLang Lexer (lexer.py).
Verifies token types, values, line numbers, and column numbers across all required constructs.
"""

import sys
from errors import LexerError
from lexer import Lexer, TokenType


def test_variable_declaration():
    source = "int count = 100;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert len(tokens) == 6
    assert tokens[0].type == TokenType.INT and tokens[0].value == "int" and tokens[0].line == 1 and tokens[0].column == 1
    assert tokens[1].type == TokenType.ID and tokens[1].value == "count" and tokens[1].line == 1 and tokens[1].column == 5
    assert tokens[2].type == TokenType.ASSIGN and tokens[2].value == "=" and tokens[2].line == 1 and tokens[2].column == 11
    assert tokens[3].type == TokenType.NUMBER and tokens[3].value == 100 and tokens[3].line == 1 and tokens[3].column == 13
    assert tokens[4].type == TokenType.SEMICOLON and tokens[4].value == ";" and tokens[4].line == 1 and tokens[4].column == 16
    assert tokens[5].type == TokenType.EOF
    print("  ✓ Test 1 Passed: Variable declaration")


def test_assignment_and_unary_minus():
    source = "x = -5;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.ID and tokens[0].value == "x"
    assert tokens[1].type == TokenType.ASSIGN and tokens[1].value == "="
    assert tokens[2].type == TokenType.MINUS and tokens[2].value == "-"
    assert tokens[3].type == TokenType.NUMBER and tokens[3].value == 5
    assert tokens[4].type == TokenType.SEMICOLON
    print("  ✓ Test 2 Passed: Assignment & Unary minus tokenization")


def test_arithmetic_expressions():
    source = "total = a + b * 2 / 4 - 10;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    ops = [t.value for t in tokens if t.type in (TokenType.PLUS, TokenType.STAR, TokenType.SLASH, TokenType.MINUS)]
    assert ops == ["+", "*", "/", "-"]
    print("  ✓ Test 3 Passed: Arithmetic expressions (+, -, *, /)")


def test_comparisons():
    source = "a == b != c < d > e <= f >= g"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    comp_types = [t.type for t in tokens if t.type != TokenType.ID and t.type != TokenType.EOF]
    expected = [
        TokenType.EQ, TokenType.NEQ, TokenType.LT,
        TokenType.GT, TokenType.LE, TokenType.GE
    ]
    assert comp_types == expected
    print("  ✓ Test 4 Passed: Comparison operators (==, !=, <, >, <=, >=)")


def test_if_else_and_while():
    source = """if (x <= 10) {
    while (x > 0) {
        x = x - 1;
    }
} else {
    print(x);
}"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    types = [t.type for t in tokens]
    assert TokenType.IF in types
    assert TokenType.WHILE in types
    assert TokenType.ELSE in types
    assert TokenType.PRINT in types
    print("  ✓ Test 5 Passed: Control flow (if/else, while, print)")


def test_nested_blocks():
    source = "{\n  {\n    int a = 1;\n  }\n}"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.LBRACE and tokens[0].line == 1
    assert tokens[1].type == TokenType.LBRACE and tokens[1].line == 2
    assert tokens[7].type == TokenType.RBRACE and tokens[7].line == 4
    assert tokens[8].type == TokenType.RBRACE and tokens[8].line == 5
    print("  ✓ Test 6 Passed: Nested blocks with accurate line numbers")


def test_invalid_characters():
    source = "int x = 5 @ 10;"
    lexer = Lexer(source)
    try:
        lexer.tokenize()
        assert False, "Expected LexerError was not raised."
    except LexerError as err:
        assert err.line == 1 and err.column == 11
        assert "Unexpected character '@'" in err.message
        print("  ✓ Test 7 Passed: Invalid character (@) raises LexerError with correct line/column")


def run_all_tests():
    print("=== Running MiniLang Lexer Unit Test Suite ===")
    test_variable_declaration()
    test_assignment_and_unary_minus()
    test_arithmetic_expressions()
    test_comparisons()
    test_if_else_and_while()
    test_nested_blocks()
    test_invalid_characters()
    print("\n✅ All 7 Lexer Test Cases Passed Successfully!")


if __name__ == "__main__":
    run_all_tests()
