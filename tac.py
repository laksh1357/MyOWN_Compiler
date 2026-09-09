"""
Intermediate Code Generator (Three-Address Code - TAC) for MiniLang.
Translates AST nodes into linear 3-Address Code quadruples.
"""

from ast_nodes import (
    ASTNode, ProgramNode, VarDeclNode, AssignNode, PrintNode, IfNode,
    WhileNode, BlockNode, BinaryOpNode, UnaryOpNode, NumNode, VarNode
)


class TACInstruction:
    def __init__(self, op: str, arg1: str | int | float | None = None, arg2: str | int | float | None = None, result: str | None = None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __repr__(self):
        if self.op == "LABEL":
            return f"{self.result}:"
        elif self.op == "JUMP":
            return f"GOTO {self.result}"
        elif self.op == "JUMP_IF_FALSE":
            return f"IF_FALSE {self.arg1} GOTO {self.result}"
        elif self.op == "PRINT":
            return f"PRINT {self.arg1}"
        elif self.op == "ASSIGN":
            return f"{self.result} = {self.arg1}"
        elif self.op in ("+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="):
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        elif self.op == "NEG":
            return f"{self.result} = -{self.arg1}"
        else:
            return f"{self.op} {self.arg1}, {self.arg2}, {self.result}"


class TACGenerator:
    def __init__(self):
        self.instructions: list[TACInstruction] = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self) -> str:
        t = f"t{self.temp_count}"
        self.temp_count += 1
        return t

    def new_label(self) -> str:
        lbl = f"L{self.label_count}"
        self.label_count += 1
        return lbl

    def generate(self, node: ASTNode) -> list[TACInstruction]:
        self._visit(node)
        return self.instructions

    def _visit(self, node: ASTNode) -> str | None:
        method_name = f"_visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node: ASTNode):
        raise NotImplementedError(f"No TAC visitor defined for {type(node).__name__}")

    def _visit_ProgramNode(self, node: ProgramNode):
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_VarDeclNode(self, node: VarDeclNode):
        expr_res = self._visit(node.expr)
        self.instructions.append(TACInstruction("ASSIGN", expr_res, None, node.name))
        return node.name

    def _visit_AssignNode(self, node: AssignNode):
        expr_res = self._visit(node.expr)
        self.instructions.append(TACInstruction("ASSIGN", expr_res, None, node.name))
        return node.name

    def _visit_PrintNode(self, node: PrintNode):
        expr_res = self._visit(node.expr)
        self.instructions.append(TACInstruction("PRINT", expr_res, None, None))

    def _visit_IfNode(self, node: IfNode):
        else_label = self.new_label()
        end_label = self.new_label()

        cond_res = self._visit(node.condition)
        if node.else_block:
            self.instructions.append(TACInstruction("JUMP_IF_FALSE", cond_res, None, else_label))
            self._visit(node.then_block)
            self.instructions.append(TACInstruction("JUMP", None, None, end_label))
            self.instructions.append(TACInstruction("LABEL", None, None, else_label))
            self._visit(node.else_block)
            self.instructions.append(TACInstruction("LABEL", None, None, end_label))
        else:
            self.instructions.append(TACInstruction("JUMP_IF_FALSE", cond_res, None, end_label))
            self._visit(node.then_block)
            self.instructions.append(TACInstruction("LABEL", None, None, end_label))

    def _visit_WhileNode(self, node: WhileNode):
        start_label = self.new_label()
        end_label = self.new_label()

        self.instructions.append(TACInstruction("LABEL", None, None, start_label))
        cond_res = self._visit(node.condition)
        self.instructions.append(TACInstruction("JUMP_IF_FALSE", cond_res, None, end_label))
        self._visit(node.body)
        self.instructions.append(TACInstruction("JUMP", None, None, start_label))
        self.instructions.append(TACInstruction("LABEL", None, None, end_label))

    def _visit_BlockNode(self, node: BlockNode):
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_BinaryOpNode(self, node: BinaryOpNode) -> str:
        left_res = self._visit(node.left)
        right_res = self._visit(node.right)
        temp = self.new_temp()
        self.instructions.append(TACInstruction(node.op, left_res, right_res, temp))
        return temp

    def _visit_UnaryOpNode(self, node: UnaryOpNode) -> str:
        operand_res = self._visit(node.operand)
        temp = self.new_temp()
        op_code = "NEG" if node.op == "-" else node.op
        self.instructions.append(TACInstruction(op_code, operand_res, None, temp))
        return temp

    def _visit_NumNode(self, node: NumNode) -> str | int | float:
        return node.value

    def _visit_VarNode(self, node: VarNode) -> str:
        return node.name


def dump_tac(instructions: list[TACInstruction]) -> str:
    lines = []
    for idx, inst in enumerate(instructions, start=1):
        if inst.op == "LABEL":
            lines.append(f"{idx:3d}: {inst.result}:")
        else:
            lines.append(f"{idx:3d}:   {inst}")
    return "\n".join(lines)
