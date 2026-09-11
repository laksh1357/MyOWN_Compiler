"""
Semantic Analyzer Module for Sudarshan Compiler.

Performs static semantics validation on the AST including:
- Declaration before use validation
- Duplicate declaration checking in the same scope
- Scope entry/exit management for nested blocks
- Shadowing support
- Type validation for arithmetic and comparison expressions
Raises SemanticError from errors.py with line and column tracking.
"""

from errors import SemanticError
from symbol_table import SymbolTable
from ast_nodes import (
    ASTNode, Program, VarDecl, Assignment, PrintStmt, IfStmt,
    WhileStmt, Block, BinaryExpr, UnaryExpr, IntegerLiteral, Variable
)


class SemanticAnalyzer:
    """
    AST Visitor that performs type checking, symbol resolution,
    and lexical scope verification.
    """

    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, program: Program) -> SymbolTable:
        """Analyzes the given AST Program root node and returns the symbol table."""
        self._visit(program)
        return self.symbol_table

    def _visit(self, node: ASTNode) -> str:
        """
        Dispatches node visit to appropriate handler based on node class name.
        Returns the type name of the evaluated expression (e.g. "int").
        """
        method_name = f"_visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node: ASTNode):
        raise NotImplementedError(f"No visitor method defined for AST node '{type(node).__name__}'")

    def _visit_Program(self, node: Program) -> str:
        for stmt in node.statements:
            self._visit(stmt)
        return "void"

    def _visit_VarDecl(self, node: VarDecl) -> str:
        # Evaluate initializer expression first
        expr_type = self._visit(node.initializer)
        if expr_type != "int":
            raise SemanticError(
                f"Cannot initialize variable '{node.name}' of type '{node.var_type}' with expression of type '{expr_type}'.",
                node.line,
                node.column
            )

        # Check for duplicate declaration in the current active scope
        if self.symbol_table.lookup_current_scope(node.name) is not None:
            raise SemanticError(
                f"Variable '{node.name}' is already declared in this scope.",
                node.line,
                node.column
            )

        # Register variable in current scope
        self.symbol_table.declare(
            name=node.name,
            type_name=node.var_type,
            line=node.line,
            column=node.column
        )
        return "void"

    def _visit_Assignment(self, node: Assignment) -> str:
        # Check variable is declared
        sym = self.symbol_table.lookup(node.name)
        if sym is None:
            raise SemanticError(
                f"Cannot assign to undeclared variable '{node.name}'.",
                node.line,
                node.column
            )

        expr_type = self._visit(node.value)
        if expr_type != sym.type_name:
            raise SemanticError(
                f"Cannot assign expression of type '{expr_type}' to variable '{node.name}' of type '{sym.type_name}'.",
                node.line,
                node.column
            )
        return "void"

    def _visit_PrintStmt(self, node: PrintStmt) -> str:
        expr_type = self._visit(node.expression)
        if expr_type != "int":
            raise SemanticError(
                f"Print statement requires integer expression, got '{expr_type}'.",
                node.line,
                node.column
            )
        return "void"

    def _visit_IfStmt(self, node: IfStmt) -> str:
        cond_type = self._visit(node.condition)
        if cond_type != "int":
            raise SemanticError(
                f"If condition must evaluate to integer/boolean expression, got '{cond_type}'.",
                node.line,
                node.column
            )
        self._visit(node.then_branch)
        if node.else_branch:
            self._visit(node.else_branch)
        return "void"

    def _visit_WhileStmt(self, node: WhileStmt) -> str:
        cond_type = self._visit(node.condition)
        if cond_type != "int":
            raise SemanticError(
                f"While condition must evaluate to integer/boolean expression, got '{cond_type}'.",
                node.line,
                node.column
            )
        self._visit(node.body)
        return "void"

    def _visit_Block(self, node: Block) -> str:
        # Enter nested scope on block start
        self.symbol_table.enter_scope()
        for stmt in node.statements:
            self._visit(stmt)
        # Exit scope on block end
        self.symbol_table.exit_scope()
        return "void"

    def _visit_BinaryExpr(self, node: BinaryExpr) -> str:
        left_type = self._visit(node.left)
        right_type = self._visit(node.right)

        if left_type != "int" or right_type != "int":
            raise SemanticError(
                f"Binary operator '{node.operator}' requires integer operands, got '{left_type}' and '{right_type}'.",
                node.line,
                node.column
            )

        # In MiniLang, both arithmetic (+, -, *, /) and comparison (==, !=, <, >, <=, >=) return int (0 or 1 for bool)
        return "int"

    def _visit_UnaryExpr(self, node: UnaryExpr) -> str:
        operand_type = self._visit(node.operand)
        if operand_type != "int":
            raise SemanticError(
                f"Unary operator '{node.operator}' requires integer operand, got '{operand_type}'.",
                node.line,
                node.column
            )
        return "int"

    def _visit_IntegerLiteral(self, node: IntegerLiteral) -> str:
        return "int"

    def _visit_Variable(self, node: Variable) -> str:
        sym = self.symbol_table.lookup(node.name)
        if sym is None:
            raise SemanticError(
                f"Undeclared variable '{node.name}'.",
                node.line,
                node.column
            )
        return sym.type_name
