"""
Centralized Error Handling Module for MiniLang Compiler.

Defines a clean hierarchy of compiler exceptions with line, column,
and optional source code context tracking across all pipeline phases.
"""

from typing import Optional


class MiniLangError(Exception):
    """Base class for all MiniLang compiler and interpreter errors."""

    def __init__(
        self,
        message: str,
        line: Optional[int] = None,
        column: Optional[int] = None,
        source_context: Optional[str] = None
    ):
        self.message = message
        self.line = line
        self.column = column
        self.source_context = source_context
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        error_name = self.__class__.__name__
        location_str = ""

        if self.line is not None and self.column is not None:
            location_str = f" at line {self.line}, column {self.column}"
        elif self.line is not None:
            location_str = f" at line {self.line}"

        base_msg = f"{error_name}: {self.message}{location_str}"

        if self.source_context:
            base_msg += f"\n  Context: {self.source_context.strip()}"

        return base_msg


class LexerError(MiniLangError):
    """Raised when an unrecognized character or malformed token is scanned."""
    pass


class ParserError(MiniLangError):
    """Raised when source tokens violate MiniLang syntax/grammar rules."""
    pass


class SemanticError(MiniLangError):
    """Raised on scope violations, undeclared variables, or type mismatches."""
    pass


class RuntimeError(MiniLangError):
    """Raised during TAC execution (e.g. division by zero, undefined access)."""
    pass
