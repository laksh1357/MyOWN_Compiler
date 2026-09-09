"""
Abstract Syntax Tree (AST) Nodes Module for MiniLang Compiler.

Defines AST nodes for all MiniLang constructs, preserving source location (line, column).
Includes a pretty-printer function dump_ast() for visual inspection during demonstrations.
"""

from typing import List, Optional


class ASTNode:
    """Base class for all Abstract Syntax Tree nodes."""

    def __init__(self, line: Optional[int] = None, column: Optional[int] = None):
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


# --- Root Node ---

class Program(ASTNode):
    """Root AST node representing an entire MiniLang program."""

    def __init__(self, statements: Optional[List[ASTNode]] = None, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(line, column)
        self.statements: List[ASTNode] = statements if statements is not None else []


# --- Expression Nodes ---

class IntegerLiteral(ASTNode):
    """AST node for integer literal values (e.g. 5, 42)."""

    def __init__(self, value: int, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(line, column)
        self.value = value


class Variable(ASTNode):
    """AST node for variable references (e.g. x, count)."""

    def __init__(self, name: str, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(line, column)
        self.name = name


class UnaryExpr(ASTNode):
    """AST node for unary expressions (e.g. -x)."""

    def __init__(self, operator: str, operand: ASTNode, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(line, column)
        self.operator = operator
        self.operand = operand


class BinaryExpr(ASTNode):
    """AST node for binary expressions (e.g. x + 1, a < b)."""

    def __init__(self, left: ASTNode, operator: str, right: ASTNode, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(line, column)
        self.left = left
        self.operator = operator
        self.right = right


# --- Statement Nodes ---

class VarDecl(ASTNode):
    """AST node for variable declarations (e.g. int x = 5;)."""

    def __init__(self, var_type: str, name: str, initializer: ASTNode, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(line, column)
        self.var_type = var_type
        self.name = name
        self.initializer = initializer


class Assignment(ASTNode):
    """AST node for variable assignments (e.g. x = y + 1;)."""

    def __init__(self, name: str, value: ASTNode, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(line, column)
        self.name = name
        self.value = value


class PrintStmt(ASTNode):
    """AST node for print statements (e.g. print(x);)."""

    def __init__(self, expression: ASTNode, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(line, column)
        self.expression = expression


class IfStmt(ASTNode):
    """AST node for conditional statements (if (cond) then_branch else else_branch)."""

    def __init__(self, condition: ASTNode, then_branch: ASTNode, else_branch: Optional[ASTNode] = None, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class WhileStmt(ASTNode):
    """AST node for loop statements (while (cond) body)."""

    def __init__(self, condition: ASTNode, body: ASTNode, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(line, column)
        self.condition = condition
        self.body = body


class Block(ASTNode):
    """AST node for block statements ({ statement* })."""

    def __init__(self, statements: Optional[List[ASTNode]] = None, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(line, column)
        self.statements: List[ASTNode] = statements if statements is not None else []


# --- AST Pretty Printer ---

def dump_ast(node: ASTNode, indent: int = 0) -> str:
    """
    Recursively formats an AST node hierarchy into a clean, human-readable string.
    Suitable for lab demonstrations and CLI --ast flag output.
    """
    prefix = "  " * indent

    if isinstance(node, Program):
        res = f"{prefix}Program:\n"
        for stmt in node.statements:
            res += dump_ast(stmt, indent + 1)
        return res

    elif isinstance(node, VarDecl):
        res = f"{prefix}VarDecl ({node.var_type} {node.name}):\n"
        res += dump_ast(node.initializer, indent + 1)
        return res

    elif isinstance(node, Assignment):
        res = f"{prefix}Assignment ({node.name} =):\n"
        res += dump_ast(node.value, indent + 1)
        return res

    elif isinstance(node, PrintStmt):
        res = f"{prefix}PrintStmt:\n"
        res += dump_ast(node.expression, indent + 1)
        return res

    elif isinstance(node, IfStmt):
        res = f"{prefix}IfStmt:\n"
        res += f"{prefix}  Condition:\n" + dump_ast(node.condition, indent + 2)
        res += f"{prefix}  Then:\n" + dump_ast(node.then_branch, indent + 2)
        if node.else_branch:
            res += f"{prefix}  Else:\n" + dump_ast(node.else_branch, indent + 2)
        return res

    elif isinstance(node, WhileStmt):
        res = f"{prefix}WhileStmt:\n"
        res += f"{prefix}  Condition:\n" + dump_ast(node.condition, indent + 2)
        res += f"{prefix}  Body:\n" + dump_ast(node.body, indent + 2)
        return res

    elif isinstance(node, Block):
        res = f"{prefix}Block:\n"
        for stmt in node.statements:
            res += dump_ast(stmt, indent + 1)
        return res

    elif isinstance(node, BinaryExpr):
        res = f"{prefix}BinaryExpr ('{node.operator}'):\n"
        res += dump_ast(node.left, indent + 1)
        res += dump_ast(node.right, indent + 1)
        return res

    elif isinstance(node, UnaryExpr):
        res = f"{prefix}UnaryExpr ('{node.operator}'):\n"
        res += dump_ast(node.operand, indent + 1)
        return res

    elif isinstance(node, IntegerLiteral):
        return f"{prefix}IntegerLiteral({node.value})\n"

    elif isinstance(node, Variable):
        return f"{prefix}Variable({node.name})\n"

    else:
        return f"{prefix}{node.__class__.__name__}\n"
