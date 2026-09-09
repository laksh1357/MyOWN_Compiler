"""
Parser for MiniLang.
Constructs an Abstract Syntax Tree (AST) from a token stream using recursive descent parsing.
"""

from lexer import Token, TokenType
from ast_nodes import (
    ProgramNode, VarDeclNode, AssignNode, PrintNode, IfNode,
    WhileNode, BlockNode, BinaryOpNode, UnaryOpNode, NumNode, VarNode, ASTNode
)


class SyntaxError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Syntax Error [Line {line}, Column {column}]: {message}")
        self.line = line
        self.column = column


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    def _current_token(self) -> Token:
        return self.tokens[self.position]

    def _peek_type(self) -> TokenType:
        return self.tokens[self.position].type

    def _consume(self, expected_type: TokenType) -> Token:
        token = self._current_token()
        if token.type == expected_type:
            self.position += 1
            return token
        raise SyntaxError(
            f"Expected token '{expected_type.value}', got '{token.value}'",
            token.line,
            token.column
        )

    def parse(self) -> ProgramNode:
        statements = []
        while self._peek_type() != TokenType.EOF:
            statements.append(self._parse_statement())
        return ProgramNode(statements)

    def _parse_statement(self) -> ASTNode:
        token_type = self._peek_type()
        if token_type == TokenType.INT:
            return self._parse_var_decl()
        elif token_type == TokenType.ID:
            return self._parse_assign()
        elif token_type == TokenType.PRINT:
            return self._parse_print()
        elif token_type == TokenType.IF:
            return self._parse_if()
        elif token_type == TokenType.WHILE:
            return self._parse_while()
        elif token_type == TokenType.LBRACE:
            return self._parse_block()
        else:
            token = self._current_token()
            raise SyntaxError(f"Unexpected token '{token.value}'", token.line, token.column)

    def _parse_var_decl(self) -> VarDeclNode:
        int_token = self._consume(TokenType.INT)
        id_token = self._consume(TokenType.ID)
        self._consume(TokenType.ASSIGN)
        expr = self._parse_expr()
        self._consume(TokenType.SEMICOLON)
        return VarDeclNode("int", id_token.value, expr, int_token.line, int_token.column)

    def _parse_assign(self) -> AssignNode:
        id_token = self._consume(TokenType.ID)
        self._consume(TokenType.ASSIGN)
        expr = self._parse_expr()
        self._consume(TokenType.SEMICOLON)
        return AssignNode(id_token.value, expr, id_token.line, id_token.column)

    def _parse_print(self) -> PrintNode:
        print_token = self._consume(TokenType.PRINT)
        self._consume(TokenType.LPAREN)
        expr = self._parse_expr()
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)
        return PrintNode(expr, print_token.line, print_token.column)

    def _parse_if(self) -> IfNode:
        if_token = self._consume(TokenType.IF)
        self._consume(TokenType.LPAREN)
        condition = self._parse_expr()
        self._consume(TokenType.RPAREN)
        then_block = self._parse_block()

        else_block = None
        if self._peek_type() == TokenType.ELSE:
            self._consume(TokenType.ELSE)
            if self._peek_type() == TokenType.IF:
                else_stmt = self._parse_if()
                else_block = BlockNode([else_stmt], else_stmt.line, else_stmt.column)
            else:
                else_block = self._parse_block()

        return IfNode(condition, then_block, else_block, if_token.line, if_token.column)

    def _parse_while(self) -> WhileNode:
        while_token = self._consume(TokenType.WHILE)
        self._consume(TokenType.LPAREN)
        condition = self._parse_expr()
        self._consume(TokenType.RPAREN)
        body = self._parse_block()
        return WhileNode(condition, body, while_token.line, while_token.column)

    def _parse_block(self) -> BlockNode:
        lbrace_token = self._consume(TokenType.LBRACE)
        statements = []
        while self._peek_type() != TokenType.RBRACE and self._peek_type() != TokenType.EOF:
            statements.append(self._parse_statement())
        self._consume(TokenType.RBRACE)
        return BlockNode(statements, lbrace_token.line, lbrace_token.column)

    def _parse_expr(self) -> ASTNode:
        return self._parse_comparison()

    def _parse_comparison(self) -> ASTNode:
        left = self._parse_add_expr()
        comp_ops = (TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE)
        while self._peek_type() in comp_ops:
            op_token = self._current_token()
            self.position += 1
            right = self._parse_add_expr()
            left = BinaryOpNode(left, op_token.value, right, op_token.line, op_token.column)
        return left

    def _parse_add_expr(self) -> ASTNode:
        left = self._parse_term()
        while self._peek_type() in (TokenType.PLUS, TokenType.MINUS):
            op_token = self._current_token()
            self.position += 1
            right = self._parse_term()
            left = BinaryOpNode(left, op_token.value, right, op_token.line, op_token.column)
        return left

    def _parse_term(self) -> ASTNode:
        left = self._parse_factor()
        while self._peek_type() in (TokenType.STAR, TokenType.SLASH):
            op_token = self._current_token()
            self.position += 1
            right = self._parse_factor()
            left = BinaryOpNode(left, op_token.value, right, op_token.line, op_token.column)
        return left

    def _parse_factor(self) -> ASTNode:
        token = self._current_token()
        if token.type == TokenType.NUMBER:
            self._consume(TokenType.NUMBER)
            return NumNode(token.value, token.line, token.column)
        elif token.type == TokenType.ID:
            self._consume(TokenType.ID)
            return VarNode(token.value, token.line, token.column)
        elif token.type == TokenType.LPAREN:
            self._consume(TokenType.LPAREN)
            expr = self._parse_expr()
            self._consume(TokenType.RPAREN)
            return expr
        elif token.type == TokenType.MINUS:
            self._consume(TokenType.MINUS)
            operand = self._parse_factor()
            return UnaryOpNode("-", operand, token.line, token.column)
        else:
            raise SyntaxError(f"Unexpected factor '{token.value}'", token.line, token.column)
