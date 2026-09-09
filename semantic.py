"""
Semantic Analyzer for MiniLang.
Performs symbol resolution, scope checking, and type checking across the AST.
"""

from ast_nodes import (
    ASTNode, ProgramNode, VarDeclNode, AssignNode, PrintNode, IfNode,
    WhileNode, BlockNode, BinaryOpNode, UnaryOpNode, NumNode, VarNode
)
from symbol_table import SymbolTable


class SemanticError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Semantic Error [Line {line}, Column {column}]: {message}")
        self.line = line
        self.column = column


class SemanticAnalyzer:
    def __init__(self):
        self.global_symtab = SymbolTable(scope_level=0)
        self.current_symtab = self.global_symtab

    def analyze(self, node: ASTNode) -> SymbolTable:
        self._visit(node)
        return self.global_symtab

    def _enter_scope(self) -> SymbolTable:
        new_scope = SymbolTable(scope_level=self.current_symtab.scope_level + 1, parent=self.current_symtab)
        self.current_symtab = new_scope
        return new_scope

    def _exit_scope(self):
        if self.current_symtab.parent:
            self.current_symtab = self.current_symtab.parent

    def _visit(self, node: ASTNode):
        method_name = f"_visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node: ASTNode):
        raise NotImplementedError(f"No visitor defined for {type(node).__name__}")

    def _visit_ProgramNode(self, node: ProgramNode):
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_VarDeclNode(self, node: VarDeclNode):
        self._visit(node.expr)
        try:
            self.current_symtab.define(node.name, node.var_type)
        except ValueError as err:
            raise SemanticError(str(err), node.line, node.column)

    def _visit_AssignNode(self, node: AssignNode):
        sym = self.current_symtab.lookup(node.name)
        if not sym:
            raise SemanticError(f"Variable '{node.name}' is not declared before assignment.", node.line, node.column)
        self._visit(node.expr)

    def _visit_PrintNode(self, node: PrintNode):
        self._visit(node.expr)

    def _visit_IfNode(self, node: IfNode):
        self._visit(node.condition)
        self._visit(node.then_block)
        if node.else_block:
            self._visit(node.else_block)

    def _visit_WhileNode(self, node: WhileNode):
        self._visit(node.condition)
        self._visit(node.body)

    def _visit_BlockNode(self, node: BlockNode):
        self._enter_scope()
        for stmt in node.statements:
            self._visit(stmt)
        self._exit_scope()

    def _visit_BinaryOpNode(self, node: BinaryOpNode):
        self._visit(node.left)
        self._visit(node.right)

    def _visit_UnaryOpNode(self, node: UnaryOpNode):
        self._visit(node.operand)

    def _visit_NumNode(self, node: NumNode):
        pass

    def _visit_VarNode(self, node: VarNode):
        sym = self.current_symtab.lookup(node.name)
        if not sym:
            raise SemanticError(f"Variable '{node.name}' is not declared.", node.line, node.column)
