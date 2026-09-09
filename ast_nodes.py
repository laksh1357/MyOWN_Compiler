"""
Abstract Syntax Tree (AST) node definitions for MiniLang.
"""

class ASTNode:
    """Base class for all AST nodes."""
    def dump(self, indent: int = 0) -> str:
        raise NotImplementedError


class ProgramNode(ASTNode):
    def __init__(self, statements: list[ASTNode]):
        self.statements = statements

    def dump(self, indent: int = 0) -> str:
        prefix = "  " * indent
        res = f"{prefix}ProgramNode:\n"
        for stmt in self.statements:
            res += stmt.dump(indent + 1)
        return res


class VarDeclNode(ASTNode):
    def __init__(self, var_type: str, name: str, expr: ASTNode, line: int, column: int):
        self.var_type = var_type
        self.name = name
        self.expr = expr
        self.line = line
        self.column = column

    def dump(self, indent: int = 0) -> str:
        prefix = "  " * indent
        res = f"{prefix}VarDeclNode ({self.var_type} {self.name}):\n"
        res += self.expr.dump(indent + 1)
        return res


class AssignNode(ASTNode):
    def __init__(self, name: str, expr: ASTNode, line: int, column: int):
        self.name = name
        self.expr = expr
        self.line = line
        self.column = column

    def dump(self, indent: int = 0) -> str:
        prefix = "  " * indent
        res = f"{prefix}AssignNode ({self.name} =):\n"
        res += self.expr.dump(indent + 1)
        return res


class PrintNode(ASTNode):
    def __init__(self, expr: ASTNode, line: int, column: int):
        self.expr = expr
        self.line = line
        self.column = column

    def dump(self, indent: int = 0) -> str:
        prefix = "  " * indent
        res = f"{prefix}PrintNode:\n"
        res += self.expr.dump(indent + 1)
        return res


class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, then_block: ASTNode, else_block: ASTNode | None, line: int, column: int):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block
        self.line = line
        self.column = column

    def dump(self, indent: int = 0) -> str:
        prefix = "  " * indent
        res = f"{prefix}IfNode:\n"
        res += f"{prefix}  Condition:\n" + self.condition.dump(indent + 2)
        res += f"{prefix}  Then:\n" + self.then_block.dump(indent + 2)
        if self.else_block:
            res += f"{prefix}  Else:\n" + self.else_block.dump(indent + 2)
        return res


class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode, body: ASTNode, line: int, column: int):
        self.condition = condition
        self.body = body
        self.line = line
        self.column = column

    def dump(self, indent: int = 0) -> str:
        prefix = "  " * indent
        res = f"{prefix}WhileNode:\n"
        res += f"{prefix}  Condition:\n" + self.condition.dump(indent + 2)
        res += f"{prefix}  Body:\n" + self.body.dump(indent + 2)
        return res


class BlockNode(ASTNode):
    def __init__(self, statements: list[ASTNode], line: int, column: int):
        self.statements = statements
        self.line = line
        self.column = column

    def dump(self, indent: int = 0) -> str:
        prefix = "  " * indent
        res = f"{prefix}BlockNode:\n"
        for stmt in self.statements:
            res += stmt.dump(indent + 1)
        return res


class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode, line: int, column: int):
        self.left = left
        self.op = op
        self.right = right
        self.line = line
        self.column = column

    def dump(self, indent: int = 0) -> str:
        prefix = "  " * indent
        res = f"{prefix}BinaryOpNode ('{self.op}'):\n"
        res += self.left.dump(indent + 1)
        res += self.right.dump(indent + 1)
        return res


class UnaryOpNode(ASTNode):
    def __init__(self, op: str, operand: ASTNode, line: int, column: int):
        self.op = op
        self.operand = operand
        self.line = line
        self.column = column

    def dump(self, indent: int = 0) -> str:
        prefix = "  " * indent
        res = f"{prefix}UnaryOpNode ('{self.op}'):\n"
        res += self.operand.dump(indent + 1)
        return res


class NumNode(ASTNode):
    def __init__(self, value: int | float, line: int, column: int):
        self.value = value
        self.line = line
        self.column = column

    def dump(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}NumNode({self.value})\n"


class VarNode(ASTNode):
    def __init__(self, name: str, line: int, column: int):
        self.name = name
        self.line = line
        self.column = column

    def dump(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}VarNode({self.name})\n"
