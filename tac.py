"""
Three-Address Code (TAC) Generator Module for Sudarshan Compiler.

Translates Sudarshan AST nodes into a linear sequence of 3-Address Code quadruples
with temporary variable (t1, t2, ...) and jump label (L1, L2, ...) generation.
Integrates lexical scope variable mangling for accurate variable shadowing.
"""

from typing import Any, List, Optional
from symbol_table import SymbolTable
from ast_nodes import (
    ASTNode, Program, VarDecl, Assignment, PrintStmt, IfStmt,
    WhileStmt, Block, BinaryExpr, UnaryExpr, IntegerLiteral, Variable
)


class TACInstruction:
    """Represents a single Three-Address Code quadruple (op, arg1, arg2, result)."""

    def __init__(self, op: str, arg1: Any = None, arg2: Any = None, result: Any = None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __repr__(self) -> str:
        if self.op == "LABEL":
            return f"{self.result}:"
        elif self.op == "JUMP":
            return f"GOTO {self.result}"
        elif self.op == "JUMP_IF_FALSE":
            return f"IF_FALSE {self.arg1} GOTO {self.result}"
        elif self.op == "PRINT":
            return f"PRINT {self.arg1}"
        elif self.op == "CONST":
            return f"{self.result} = {self.arg1}"
        elif self.op == "ASSIGN":
            return f"{self.result} = {self.arg1}"
        elif self.op in ("ADD", "SUB", "MUL", "DIV", "EQ", "NE", "LT", "GT", "LE", "GE"):
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        elif self.op == "NEG":
            return f"{self.result} = -{self.arg1}"
        else:
            return f"{self.op} {self.arg1}, {self.arg2}, {self.result}"


# Map AST binary operators to TAC opcodes
OPCODE_MAP = {
    "+": "ADD",
    "-": "SUB",
    "*": "MUL",
    "/": "DIV",
    "==": "EQ",
    "!=": "NE",
    "<": "LT",
    ">": "GT",
    "<=": "LE",
    ">=": "GE",
}


class TACGenerator:
    """
    AST Visitor that translates MiniLang AST nodes into linear TAC instructions.
    Uses SymbolTable to handle scope-based variable name mangling for shadowing.
    """

    def __init__(self):
        self.instructions: List[TACInstruction] = []
        self.temp_counter = 1
        self.label_counter = 1
        self.symbol_table = SymbolTable()

    def new_temp(self) -> str:
        """Allocates a unique temporary variable name (t1, t2, ...)."""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def new_label(self) -> str:
        """Allocates a unique label name (L1, L2, ...)."""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def _get_var_tac_name(self, name: str) -> str:
        """Returns the scope-mangled variable name for TAC execution (e.g. x vs x_s1)."""
        sym = self.symbol_table.lookup(name)
        if sym and sym.scope_level > 0:
            return f"{name}_s{sym.scope_level}"
        return name

    def generate(self, program: Program) -> List[TACInstruction]:
        """Translates the AST Program root node into a list of TAC instructions."""
        self._visit(program)
        return self.instructions

    def _visit(self, node: ASTNode) -> Any:
        method_name = f"_visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node: ASTNode):
        raise NotImplementedError(f"No TAC generator defined for AST node '{type(node).__name__}'")

    def _visit_Program(self, node: Program):
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_VarDecl(self, node: VarDecl):
        expr_res = self._visit(node.initializer)
        try:
            sym = self.symbol_table.declare(node.name, node.var_type, node.line, node.column)
            tac_name = f"{node.name}_s{sym.scope_level}" if sym.scope_level > 0 else node.name
        except ValueError:
            tac_name = self._get_var_tac_name(node.name)

        self.instructions.append(TACInstruction("ASSIGN", expr_res, None, tac_name))

    def _visit_Assignment(self, node: Assignment):
        expr_res = self._visit(node.value)
        tac_name = self._get_var_tac_name(node.name)
        self.instructions.append(TACInstruction("ASSIGN", expr_res, None, tac_name))

    def _visit_PrintStmt(self, node: PrintStmt):
        expr_res = self._visit(node.expression)
        self.instructions.append(TACInstruction("PRINT", expr_res, None, None))

    def _visit_IfStmt(self, node: IfStmt):
        else_label = self.new_label()
        end_label = self.new_label()

        cond_res = self._visit(node.condition)
        if node.else_branch:
            self.instructions.append(TACInstruction("JUMP_IF_FALSE", cond_res, None, else_label))
            self._visit(node.then_branch)
            self.instructions.append(TACInstruction("JUMP", None, None, end_label))
            self.instructions.append(TACInstruction("LABEL", None, None, else_label))
            self._visit(node.else_branch)
            self.instructions.append(TACInstruction("LABEL", None, None, end_label))
        else:
            self.instructions.append(TACInstruction("JUMP_IF_FALSE", cond_res, None, end_label))
            self._visit(node.then_branch)
            self.instructions.append(TACInstruction("LABEL", None, None, end_label))

    def _visit_WhileStmt(self, node: WhileStmt):
        start_label = self.new_label()
        end_label = self.new_label()

        self.instructions.append(TACInstruction("LABEL", None, None, start_label))
        cond_res = self._visit(node.condition)
        self.instructions.append(TACInstruction("JUMP_IF_FALSE", cond_res, None, end_label))
        self._visit(node.body)
        self.instructions.append(TACInstruction("JUMP", None, None, start_label))
        self.instructions.append(TACInstruction("LABEL", None, None, end_label))

    def _visit_Block(self, node: Block):
        self.symbol_table.enter_scope()
        for stmt in node.statements:
            self._visit(stmt)
        self.symbol_table.exit_scope()

    def _visit_BinaryExpr(self, node: BinaryExpr) -> str:
        left_res = self._visit(node.left)
        right_res = self._visit(node.right)
        temp = self.new_temp()
        opcode = OPCODE_MAP.get(node.operator, node.operator)
        self.instructions.append(TACInstruction(opcode, left_res, right_res, temp))
        return temp

    def _visit_UnaryExpr(self, node: UnaryExpr) -> str:
        operand_res = self._visit(node.operand)
        temp = self.new_temp()
        self.instructions.append(TACInstruction("NEG", operand_res, None, temp))
        return temp

    def _visit_IntegerLiteral(self, node: IntegerLiteral) -> Any:
        temp = self.new_temp()
        self.instructions.append(TACInstruction("CONST", node.value, None, temp))
        return temp

    def _visit_Variable(self, node: Variable) -> str:
        return self._get_var_tac_name(node.name)


def dump_tac(instructions: List[TACInstruction]) -> str:
    """Formats TAC instructions into a clean string for lab demonstration output."""
    lines = []
    for idx, inst in enumerate(instructions, start=1):
        if inst.op == "LABEL":
            lines.append(f"{idx:3d}: {inst.result}:")
        else:
            lines.append(f"{idx:3d}:   {inst}")
    return "\n".join(lines)
