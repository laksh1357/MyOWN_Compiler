"""
Lexer Module for Sudarshan Compiler.

Converts Sudarshan source code into a stream of tokens, tracking line and column numbers.
Raises LexerError from errors.py for unrecognized characters.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, List

from errors import LexerError


class TokenType(Enum):
    # Keywords
    INT = "int"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    PRINT = "print"

    # Identifiers & Literals
    ID = "ID"
    NUMBER = "NUMBER"

    # Operators
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    ASSIGN = "="
    EQ = "=="
    NEQ = "!="
    LT = "<"
    GT = ">"
    LE = "<="
    GE = ">="

    # Punctuation
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    SEMICOLON = ";"

    # End of File
    EOF = "EOF"


KEYWORDS = {
    "int": TokenType.INT,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "print": TokenType.PRINT,
}


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {repr(self.value)}, L{self.line}:C{self.column})"


class Lexer:
    """Scans Sudarshan source code into a list of Token objects."""

    def __init__(self, source_code: str):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.length = len(source_code)

    def _peek(self) -> str:
        """Returns the current character without advancing."""
        if self.position >= self.length:
            return ""
        return self.source[self.position]

    def _peek_next(self) -> str:
        """Returns the next character without advancing."""
        if self.position + 1 >= self.length:
            return ""
        return self.source[self.position + 1]

    def _get_char(self) -> str:
        """Consumes and returns the current character, updating line and column numbers."""
        if self.position >= self.length:
            return ""
        ch = self.source[self.position]
        self.position += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def tokenize(self) -> List[Token]:
        """Scans the entire source code and returns a list of tokens ending with EOF."""
        tokens: List[Token] = []

        while self.position < self.length:
            ch = self._peek()

            # Ignore whitespace (spaces, tabs, newlines)
            if ch.isspace():
                self._get_char()
                continue

            # Ignore single-line comments (// ...)
            if ch == "/" and self._peek_next() == "/":
                while self._peek() != "" and self._peek() != "\n":
                    self._get_char()
                continue

            start_line = self.line
            start_col = self.column

            # Identifiers and Keywords
            if ch.isalpha() or ch == "_":
                ident = ""
                while self._peek().isalnum() or self._peek() == "_":
                    ident += self._get_char()
                token_type = KEYWORDS.get(ident, TokenType.ID)
                tokens.append(Token(token_type, ident, start_line, start_col))
                continue

            # Integer Literals
            if ch.isdigit():
                num_str = ""
                while self._peek().isdigit():
                    num_str += self._get_char()
                tokens.append(Token(TokenType.NUMBER, int(num_str), start_line, start_col))
                continue

            # Two-character operators vs Single-character operators (=, ==, !, !=, <, <=, >, >=)
            if ch in ("=", "!", "<", ">"):
                c1 = self._get_char()
                if self._peek() == "=":
                    self._get_char()
                    op_str = c1 + "="
                    op_type = {
                        "==": TokenType.EQ,
                        "!=": TokenType.NEQ,
                        "<=": TokenType.LE,
                        ">=": TokenType.GE,
                    }[op_str]
                    tokens.append(Token(op_type, op_str, start_line, start_col))
                elif c1 == "!":
                    raise LexerError("Unexpected character '!' (did you mean '!='?)", start_line, start_col)
                else:
                    op_type = {
                        "=": TokenType.ASSIGN,
                        "<": TokenType.LT,
                        ">": TokenType.GT,
                    }[c1]
                    tokens.append(Token(op_type, c1, start_line, start_col))
                continue

            # Single-character operators and punctuation
            if ch in "+-*/(){};":
                c = self._get_char()
                op_type = {
                    "+": TokenType.PLUS,
                    "-": TokenType.MINUS,
                    "*": TokenType.STAR,
                    "/": TokenType.SLASH,
                    "(": TokenType.LPAREN,
                    ")": TokenType.RPAREN,
                    "{": TokenType.LBRACE,
                    "}": TokenType.RBRACE,
                    ";": TokenType.SEMICOLON,
                }[c]
                tokens.append(Token(op_type, c, start_line, start_col))
                continue

            # Unexpected / Unknown character
            raise LexerError(f"Unexpected character '{ch}'", start_line, start_col)

        tokens.append(Token(TokenType.EOF, "EOF", self.line, self.column))
        return tokens
