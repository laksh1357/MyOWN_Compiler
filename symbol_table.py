"""
Symbol Table management for MiniLang.
Supports lexical scoping via nested scope pointers.
"""

class Symbol:
    def __init__(self, name: str, type_name: str, scope_level: int):
        self.name = name
        self.type_name = type_name
        self.scope_level = scope_level

    def __repr__(self):
        return f"Symbol(name='{self.name}', type='{self.type_name}', scope={self.scope_level})"


class SymbolTable:
    def __init__(self, scope_level: int = 0, parent: "SymbolTable | None" = None):
        self.scope_level = scope_level
        self.parent = parent
        self.symbols: dict[str, Symbol] = {}

    def define(self, name: str, type_name: str) -> Symbol:
        if name in self.symbols:
            raise ValueError(f"Variable '{name}' already declared in this scope (Scope level {self.scope_level}).")
        sym = Symbol(name, type_name, self.scope_level)
        self.symbols[name] = sym
        return sym

    def lookup(self, name: str) -> Symbol | None:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

    def dump(self, indent: int = 0) -> str:
        prefix = "  " * indent
        res = f"{prefix}=== Scope Level {self.scope_level} ===\n"
        if not self.symbols:
            res += f"{prefix}  (empty)\n"
        else:
            for name, sym in self.symbols.items():
                res += f"{prefix}  {name} : {sym.type_name}\n"
        return res
