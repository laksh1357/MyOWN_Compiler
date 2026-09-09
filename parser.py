"""
Parser Module for MiniLang Compiler.

Implements a recursive-descent parser adhering to the MiniLang BNF grammar,
constructing AST nodes from ast_nodes.py and raising ParserError from errors.py.
"""

from typing import List, Optional
from errors import ParserError
from lexer import Token, TokenType
from ast_nodes import (
    Program, VarDecl, Assignment, PrintStmt, IfStmt, WhileStmt,
    Block, BinaryExpr, UnaryExpr, IntegerLiteral, Variable, ASTNode
)


class Parser:
    """
    Recursive-descent parser for MiniLang source code tokens.
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0

    def _current_token(self) -> Token:
        """Returns the token at current position."""
        return self.tokens[self.position]

    def _peek_type(self) -> TokenType:
        """Returns the type of the current token."""
        return self.tokens[self.position].type

    def _match(self, *types: TokenType) -> bool:
        """Checks if current token matches any of the specified types."""
        return self._peek_type() in types

    def _consume(self, expected_type: TokenType) -> Token:
        """Consumes token if it matches expected_type; otherwise raises ParserError."""
        token = self._current_token()
        if token.type == expected_type:
            self.position += 1
            return token
        raise ParserError(
            f"Expected '{expected_type.value}', got '{token.value}'",
            token.line,
            token.column
        )

    def parse(self) -> Program:
        """
        Parses the entire token stream into a Program AST node.
        program -> statement* EOF
        """
        statements: List[ASTNode] = []
        while self._peek_type() != TokenType.EOF:
            statements.append(self._parse_statement())
        
        eof_token = self._current_token()
        return Program(statements, line=1, column=1)

    def _parse_statement(self) -> ASTNode:
        """
        statement -> varDecl | assign | printStmt | ifStmt | whileStmt | block
        """
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
            raise ParserError(
                f"Unexpected statement start token '{token.value}'",
                token.line,
                token.column
            )

    def _parse_var_decl(self) -> VarDecl:
        """
        varDecl -> 'int' ID '=' expr ';'
        """
        int_tok = self._consume(TokenType.INT)
        id_tok = self._consume(TokenType.ID)
        self._consume(TokenType.ASSIGN)
        expr_node = self._parse_expr()
        self._consume(TokenType.SEMICOLON)
        return VarDecl("int", id_tok.value, expr_node, line=int_tok.line, column=int_tok.column)

    def _parse_assign(self) -> Assignment:
        """
        assign -> ID '=' expr ';'
        """
        id_tok = self._consume(TokenType.ID)
        self._consume(TokenType.ASSIGN)
        expr_node = self._parse_expr()
        self._consume(TokenType.SEMICOLON)
        return Assignment(id_tok.value, expr_node, line=id_tok.line, column=id_tok.column)

    def _parse_print(self) -> PrintStmt:
        """
        printStmt -> 'print' '(' expr ')' ';'
        """
        print_tok = self._consume(TokenType.PRINT)
        self._consume(TokenType.LPAREN)
        expr_node = self._parse_expr()
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)
        return PrintStmt(expr_node, line=print_tok.line, column=print_tok.column)

    def _parse_if(self) -> IfStmt:
        """
        ifStmt -> 'if' '(' expr ')' block ('else' (ifStmt | block))?
        """
        if_tok = self._consume(TokenType.IF)
        self._consume(TokenType.LPAREN)
        condition = self._parse_expr()
        self._consume(TokenType.RPAREN)
        then_branch = self._parse_block()

        else_branch: Optional[ASTNode] = None
        if self._peek_type() == TokenType.ELSE:
            self._consume(TokenType.ELSE)
            if self._peek_type() == TokenType.IF:
                else_stmt = self._parse_if()
                else_branch = Block([else_stmt], line=else_stmt.line, column=else_stmt.column)
            else:
                else_branch = self._parse_block()

        return IfStmt(condition, then_branch, else_branch, line=if_tok.line, column=if_tok.column)

    def _parse_while(self) -> WhileStmt:
        """
        whileStmt -> 'while' '(' expr ')' block
        """
        while_tok = self._consume(TokenType.WHILE)
        self._consume(TokenType.LPAREN)
        condition = self._parse_expr()
        self._consume(TokenType.RPAREN)
        body = self._parse_block()
        return WhileStmt(condition, body, line=while_tok.line, column=while_tok.column)

    def _parse_block(self) -> Block:
        """
        block -> '{' statement* '}'
        """
        lbrace_tok = self._consume(TokenType.LBRACE)
        statements: List[ASTNode] = []
        while self._peek_type() != TokenType.RBRACE and self._peek_type() != TokenType.EOF:
            statements.append(self._parse_statement())
        self._consume(TokenType.RBRACE)
        return Block(statements, line=lbrace_tok.line, column=lbrace_tok.column)

    def _parse_expr(self) -> ASTNode:
        """
        expr -> comparison
        """
        return self._parse_comparison()

    def _parse_comparison(self) -> ASTNode:
        """
        comparison -> addExpr (('=='|'!='|'<'|'>'|'<='|'>=') addExpr)*
        """
        left = self._parse_add_expr()
        comp_ops = (
            TokenType.EQ, TokenType.NEQ, TokenType.LT,
            TokenType.GT, TokenType.LE, TokenType.GE
        )
        while self._peek_type() in comp_ops:
            op_tok = self._current_token()
            self.position += 1
            right = self._parse_add_expr()
            left = BinaryExpr(left, op_tok.value, right, line=op_tok.line, column=op_tok.column)
        return left

    def _parse_add_expr(self) -> ASTNode:
        """
        addExpr -> term (('+'|'-') term)*
        """
        left = self._parse_term()
        while self._peek_type() in (TokenType.PLUS, TokenType.MINUS):
            op_tok = self._current_token()
            self.position += 1
            right = self._parse_term()
            left = BinaryExpr(left, op_tok.value, right, line=op_tok.line, column=op_tok.column)
        return left

    def _parse_term(self) -> ASTNode:
        """
        term -> factor (('*'|'/') factor)*
        """
        left = self._parse_factor()
        while self._peek_type() in (TokenType.STAR, TokenType.SLASH):
            op_tok = self._current_token()
            self.position += 1
            right = self._parse_factor()
            left = BinaryExpr(left, op_tok.value, right, line=op_tok.line, column=op_tok.column)
        return left

    def _parse_factor(self) -> ASTNode:
        """
        factor -> NUMBER | ID | '(' expr ')' | '-' factor
        """
        token = self._current_token()

        if token.type == TokenType.NUMBER:
            self._consume(TokenType.NUMBER)
            return IntegerLiteral(token.value, line=token.line, column=token.column)

        elif token.type == TokenType.ID:
            self._consume(TokenType.ID)
            return Variable(token.value, line=token.line, column=token.column)

        elif token.type == TokenType.LPAREN:
            self._consume(TokenType.LPAREN)
            expr_node = self._parse_expr()
            self._consume(TokenType.RPAREN)
            return expr_node

        elif token.type == TokenType.MINUS:
            self._consume(TokenType.MINUS)
            operand = self._parse_factor()
            return UnaryExpr("-", operand, line=token.line, column=token.column)

        else:
            raise ParserError(
                f"Unexpected token '{token.value}' in expression factor",
                token.line,
                token.column
            )
