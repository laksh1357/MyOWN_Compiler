"""
Lexer for MiniLang.
Handles tokenization of source code, tracking line and column numbers,
and detecting lexical errors.
"""

from enum import Enum

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


class Token:
    def __init__(self, type_: TokenType, value: object, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, L{self.line}:C{self.column})"


class LexicalError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Lexical Error [Line {line}, Column {column}]: {message}")
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.length = len(source_code)

    def _peek(self) -> str:
        if self.position >= self.length:
            return ""
        return self.source[self.position]

    def _get_char(self) -> str:
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

    def tokenize(self) -> list[Token]:
        tokens = []
        while self.position < self.length:
            ch = self._peek()

            # Whitespace
            if ch.isspace():
                self._get_char()
                continue

            # Comments (// ...)
            if ch == "/" and self.position + 1 < self.length and self.source[self.position + 1] == "/":
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

            # Numbers (Integers / Floats)
            if ch.isdigit():
                num_str = ""
                is_float = False
                while self._peek().isdigit() or (self._peek() == "." and not is_float):
                    c = self._get_char()
                    if c == ".":
                        is_float = True
                    num_str += c
                val = float(num_str) if is_float else int(num_str)
                tokens.append(Token(TokenType.NUMBER, val, start_line, start_col))
                continue

            # Two-character operators
            if ch in ("=", "!", "<", ">"):
                c1 = self._get_char()
                c2 = self._peek()
                if c2 == "=":
                    self._get_char()
                    op_str = c1 + c2
                    op_type = {
                        "==": TokenType.EQ,
                        "!=": TokenType.NEQ,
                        "<=": TokenType.LE,
                        ">=": TokenType.GE,
                    }[op_str]
                    tokens.append(Token(op_type, op_str, start_line, start_col))
                elif c1 == "!":
                    raise LexicalError("Unexpected character '!' (did you mean '!='?)", start_line, start_col)
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

            # Unknown character
            raise LexicalError(f"Unexpected character '{ch}'", start_line, start_col)

        tokens.append(Token(TokenType.EOF, "EOF", self.line, self.column))
        return tokens
