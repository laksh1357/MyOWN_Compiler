# MiniLang — A Compiler/Interpreter for a Simple Imperative Language

Compiler Design Laboratory Project

## 1. Overview

MiniLang is a lightweight imperative programming language and an end-to-end 5-phase compiler pipeline with:
- Integer variable declarations (`int x = 5;`)
- Assignment (`x = x + 1;`)
- Arithmetic (`+`, `-`, `*`, `/`) and comparison (`==`, `!=`, `<`, `>`, `<=`, `>=`) operators
- Control flow: `if / else` and `while` loops
- Output statement: `print(expr);`
- Nested block scoping (`{ ... }`)

## 2. Compiler Pipeline Architecture

```text
Source (.mini)
   │
   ▼
[1] Lexer (lexer.py)          -> Token stream, lexical error detection
   │
   ▼
[2] Parser (parser.py)        -> Abstract Syntax Tree (AST), syntax error detection
   │
   ▼
[3] Semantic Analyzer         -> Scope/type checking, symbol table (semantic.py, symbol_table.py)
   │
   ▼
[4] Intermediate Code Gen     -> Three-Address Code (tac.py) & Optimizer (tac_opt.py)
   │
   ▼
[5] Interpreter (interpreter.py) -> Executes TAC instructions, runtime error detection
```

## 3. Files

| File | Compiler Phase / Role |
|---|---|
| `lexer.py` | Lexical Analysis |
| `ast_nodes.py` | AST node definitions & dumper |
| `parser.py` | Syntax Analysis / Parsing |
| `symbol_table.py` | Symbol Table Management (lexically scoped) |
| `semantic.py` | Semantic Analysis |
| `tac.py` | Three-Address Code (TAC) Generation |
| `tac_opt.py` | TAC Optimization (Constant Folding & Dead Code Elimination) |
| `interpreter.py` | Execution Engine / Virtual Machine |
| `main.py` | CLI Driver |
| `examples/` | Test cases: valid, syntax error, semantic error, runtime error |

## 4. Grammar (BNF)

```ebnf
program    -> statement*
statement  -> varDecl | assign | printStmt | ifStmt | whileStmt | block
varDecl    -> 'int' ID '=' expr ';'
assign     -> ID '=' expr ';'
printStmt  -> 'print' '(' expr ')' ';'
ifStmt     -> 'if' '(' expr ')' block ('else' (ifStmt | block))?
whileStmt  -> 'while' '(' expr ')' block
block      -> '{' statement* '}'
expr       -> comparison
comparison -> addExpr (('=='|'!='|'<'|'>'|'<='|'>=') addExpr)*
addExpr    -> term (('+'|'-') term)*
term       -> factor (('*'|'/') factor)*
factor     -> NUMBER | ID | '(' expr ')' | '-' factor
```

## 5. How to Run

```bash
python3 main.py examples/valid.mini --all
```

Flags:
- `--tokens`  : Show token stream
- `--ast`     : Show parsed AST
- `--symtab`  : Show global symbol table
- `--tac`     : Show generated three-address code
- `--opt`     : Show optimized three-address code
- `--all`     : Show outputs of all compiler phases

## 6. Test Suite

| File | Purpose |
|---|---|
| `examples/valid.mini` | Loops + if/else, normal execution |
| `examples/error_syntax.mini` | Syntax error handling (missing semicolon) |
| `examples/error_semantic.mini` | Semantic error handling (undeclared variable) |
| `examples/error_runtime.mini` | Runtime error handling (division by zero) |
| `examples/opt_test.mini` | TAC constant folding optimization test |
