"""
Unit Test Suite for MiniLang AST Nodes (ast_nodes.py).
Verifies node construction, property retention, line/column tracking, and dump_ast output.
"""

from ast_nodes import (
    Program, VarDecl, Assignment, PrintStmt, IfStmt, WhileStmt,
    Block, BinaryExpr, UnaryExpr, IntegerLiteral, Variable, dump_ast
)


def test_ast_node_properties():
    lit = IntegerLiteral(42, line=3, column=10)
    assert lit.value == 42
    assert lit.line == 3
    assert lit.column == 10

    var = Variable("count", line=1, column=5)
    assert var.name == "count"
    assert var.line == 1 and var.column == 5

    bin_op = BinaryExpr(Variable("x"), "+", IntegerLiteral(1))
    assert bin_op.operator == "+"
    assert isinstance(bin_op.left, Variable)
    assert isinstance(bin_op.right, IntegerLiteral)

    un_op = UnaryExpr("-", Variable("a"))
    assert un_op.operator == "-"
    assert isinstance(un_op.operand, Variable)

    print("  ✓ Test 1 Passed: Expressions Node Construction & Properties")


def test_ast_statements():
    var_decl = VarDecl("int", "a", IntegerLiteral(10))
    assign = Assignment("a", BinaryExpr(Variable("a"), "+", IntegerLiteral(1)))
    print_stmt = PrintStmt(Variable("a"))
    block = Block([var_decl, assign, print_stmt])

    if_stmt = IfStmt(
        condition=BinaryExpr(Variable("a"), ">", IntegerLiteral(0)),
        then_branch=block,
        else_branch=Block([PrintStmt(IntegerLiteral(0))])
    )

    while_stmt = WhileStmt(
        condition=BinaryExpr(Variable("a"), "<", IntegerLiteral(100)),
        body=block
    )

    program = Program([if_stmt, while_stmt])
    assert len(program.statements) == 2
    print("  ✓ Test 2 Passed: Statements Node Construction")


def test_dump_ast_formatting():
    ast = Program([
        VarDecl("int", "sum", IntegerLiteral(0)),
        WhileStmt(
            condition=BinaryExpr(Variable("i"), "<=", IntegerLiteral(5)),
            body=Block([
                Assignment("sum", BinaryExpr(Variable("sum"), "+", Variable("i")))
            ])
        ),
        PrintStmt(Variable("sum"))
    ])

    dumped_text = dump_ast(ast)
    assert "Program:" in dumped_text
    assert "VarDecl (int sum):" in dumped_text
    assert "WhileStmt:" in dumped_text
    assert "BinaryExpr ('<='):" in dumped_text
    assert "PrintStmt:" in dumped_text
    print("  ✓ Test 3 Passed: dump_ast Pretty Printing")


def run_all_tests():
    print("=== Running MiniLang AST Nodes Unit Test Suite ===")
    test_ast_node_properties()
    test_ast_statements()
    test_dump_ast_formatting()
    print("\n✅ All 3 AST Test Cases Passed Successfully!")


if __name__ == "__main__":
    run_all_tests()
