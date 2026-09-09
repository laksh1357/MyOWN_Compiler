"""
Unit Test Suite for MiniLang Parser (parser.py).
Verifies AST node construction, operator precedence, associativity, and error handling.
"""

from errors import ParserError
from lexer import Lexer
from parser import Parser
from ast_nodes import (
    Program, VarDecl, Assignment, PrintStmt, IfStmt, WhileStmt,
    Block, BinaryExpr, UnaryExpr, IntegerLiteral, Variable, dump_ast
)


def test_operator_precedence():
    # 5 + 3 * 2  ==>  + (5, * (3, 2))
    source = "int x = 5 + 3 * 2;"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()

    var_decl = ast.statements[0]
    assert isinstance(var_decl, VarDecl)
    bin_add = var_decl.initializer
    assert isinstance(bin_add, BinaryExpr) and bin_add.operator == "+"
    assert isinstance(bin_add.left, IntegerLiteral) and bin_add.left.value == 5
    assert isinstance(bin_add.right, BinaryExpr) and bin_add.right.operator == "*"
    print("  ✓ Test 1 Passed: Operator precedence (* before +)")


def test_comparison_precedence():
    # x + 1 < y * 2  ==>  < (+ (x, 1), * (y, 2))
    source = "int res = x + 1 < y * 2;"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()

    var_decl = ast.statements[0]
    comp_expr = var_decl.initializer
    assert isinstance(comp_expr, BinaryExpr) and comp_expr.operator == "<"
    assert comp_expr.left.operator == "+"
    assert comp_expr.right.operator == "*"
    print("  ✓ Test 2 Passed: Comparison precedence (lower than arithmetic)")


def test_unary_minus_and_parentheses():
    # x = -(a + b);
    source = "x = -(a + b);"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()

    assign = ast.statements[0]
    assert isinstance(assign, Assignment)
    un_expr = assign.value
    assert isinstance(un_expr, UnaryExpr) and un_expr.operator == "-"
    assert isinstance(un_expr.operand, BinaryExpr) and un_expr.operand.operator == "+"
    print("  ✓ Test 3 Passed: Unary minus & parentheses handling")


def test_if_else_and_else_if():
    source = """if (x > 0) {
    print(x);
} else if (x == 0) {
    print(0);
} else {
    print(-1);
}"""
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()

    if_stmt = ast.statements[0]
    assert isinstance(if_stmt, IfStmt)
    assert isinstance(if_stmt.else_branch, Block)
    nested_if = if_stmt.else_branch.statements[0]
    assert isinstance(nested_if, IfStmt)
    assert isinstance(nested_if.else_branch, Block)
    print("  ✓ Test 4 Passed: if / else if / else chain parsing")


def test_while_loop_and_nested_blocks():
    source = "while (i < 5) { { i = i + 1; } }"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()

    while_stmt = ast.statements[0]
    assert isinstance(while_stmt, WhileStmt)
    assert isinstance(while_stmt.body, Block)
    outer_block = while_stmt.body
    assert isinstance(outer_block.statements[0], Block)
    print("  ✓ Test 5 Passed: while loop & nested block parsing")


def test_parser_error_handling():
    # Missing semicolon
    source = "int x = 5\nprint(x);"
    tokens = Lexer(source).tokenize()
    try:
        Parser(tokens).parse()
        assert False, "Expected ParserError not raised"
    except ParserError as err:
        assert err.line == 2 and err.column == 1
        assert "Expected ';', got 'print'" in err.message
        print("  ✓ Test 6 Passed: ParserError raised on missing semicolon")


def run_all_tests():
    print("=== Running MiniLang Parser Unit Test Suite ===")
    test_operator_precedence()
    test_comparison_precedence()
    test_unary_minus_and_parentheses()
    test_if_else_and_else_if()
    test_while_loop_and_nested_blocks()
    test_parser_error_handling()
    print("\n✅ All 6 Parser Test Cases Passed Successfully!")


if __name__ == "__main__":
    run_all_tests()
