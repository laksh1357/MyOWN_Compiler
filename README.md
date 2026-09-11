# Sudarshan — An End-to-End Compiler and Virtual Machine

**Compiler Design Laboratory Individual Project**  
**Student Name**: Lakshya Singh | **Reg No.**: 24BDS0054  

---

## 1. Project Overview

**Sudarshan** is a small imperative programming language and a complete, end-to-end compiler pipeline implemented in Python 3.

The project demonstrates all classic compiler construction phases:
- **Lexical Analysis** (scanning & tokenization)
- **Syntax Analysis** (recursive descent parsing & AST construction)
- **Semantic Analysis** (scope resolution & static type checking)
- **Intermediate Code Generation** (Three-Address Code quadruples)
- **Intermediate Code Optimization** (constant folding, constant propagation & dead code elimination)
- **Virtual Machine Execution** (linear TAC interpretation & runtime error handling)

Designed specifically for Compiler Design Laboratory requirements, the codebase is modular, zero-dependency, type-hinted, and easy to explain during a viva examination.

---

## 2. Key Features

- **Integer Variables & Declaration**: `int x = 5;`
- **Variable Assignment**: `x = x + 1;`
- **Arithmetic Operators**: `+`, `-`, `*`, `/`, unary `-` with mathematical precedence
- **Comparison Operators**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Control Flow**: `if / else if / else` conditionals and `while` loops
- **Block Scoping**: Lexically nested `{ ... }` blocks with parent scope visibility and variable shadowing
- **Output Statement**: `print(expr);`
- **Centralized Error Hierarchy**: Detailed error location (line and column) without Python tracebacks
- **TAC Optimizer Pass**: Compile-time constant folding and dead code elimination
- **Built-in Test Suite**: 22 unit & integration tests using Python's native `unittest`

---

## 3. Compiler Pipeline Architecture

```text
                  Source Code (.mini)
                           │
                           ▼
Phase 1: Lexical Analyzer (lexer.py & errors.py) ──► Token Stream (Line & Col tracking)
                           │
                           ▼
Phase 2: Syntax Analyzer (parser.py & ast_nodes.py) ──► Abstract Syntax Tree (AST)
                           │
                           ▼
Phase 3: Semantic Analyzer (semantic.py & symbol_table.py) ──► Scoped Symbol Table
                           │
                           ▼
Phase 4: Intermediate Code Generator (tac.py) ──► Three-Address Code (Quadruples)
                           │
                           ▼
Phase 4b: TAC Optimizer (tac_opt.py) ──► Constant Folding & DCE
                           │
                           ▼
Phase 5: Virtual Machine Interpreter (interpreter.py) ──► Code Execution & Output
```

---

## 4. Project Directory Structure

```text
Sudarshan/
├── README.md                 # Project documentation & Viva Q&A
├── main.py                   # Command-line driver & CLI interface
├── sudarshan                 # Executable CLI wrapper
├── errors.py                 # Centralized exception hierarchy (SudarshanError)
├── lexer.py                  # Phase 1: Scanner & Tokenizer
├── ast_nodes.py              # Phase 2: AST node classes & dump_ast() dumper
├── parser.py                 # Phase 2: Recursive Descent Parser
├── symbol_table.py           # Phase 3: Lexically Scoped Symbol Table
├── semantic.py               # Phase 3: Static Semantic Analyzer
├── tac.py                    # Phase 4: Three-Address Code Generator
├── tac_opt.py                # Phase 4b: TAC Optimizer Pass
├── interpreter.py            # Phase 5: TAC Virtual Machine Interpreter
├── examples/                 # Sample Sudarshan programs
│   ├── valid.mini            # Loops, logic, arithmetic, print
│   ├── nested_scope.mini     # Nested blocks & variable shadowing
│   ├── opt_test.mini         # Constant folding optimization test
│   ├── error_lexical.mini    # Lexical error test (@)
│   ├── error_syntax.mini     # Syntax error test (missing ;)
│   ├── error_semantic.mini   # Semantic error test (undeclared variable)
│   └── error_runtime.mini    # Runtime error test (division by zero)
└── tests/                    # Unittest test suite (22 unit & integration tests)
    ├── __init__.py
    ├── test_lexer.py
    ├── test_parser.py
    ├── test_semantic.py
    ├── test_tac.py
    ├── test_optimizer.py
    └── test_interpreter.py
```

---

## 5. Sudarshan Grammar (BNF Syntax)

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
comparison -> addExpr (('==' | '!=' | '<' | '>' | '<=' | '>=') addExpr)*
addExpr    -> term (('+' | '-') term)*
term       -> factor (('*' | '/') factor)*
factor     -> NUMBER | ID | '(' expr ')' | '-' factor
```

---

## 6. Token Types

| Token Type | Category | Lexemes / Examples |
|---|---|---|
| `INT` | Keyword | `int` |
| `IF` | Keyword | `if` |
| `ELSE` | Keyword | `else` |
| `WHILE` | Keyword | `while` |
| `PRINT` | Keyword | `print` |
| `ID` | Identifier | `x`, `count`, `sum`, `total1` |
| `NUMBER` | Literal | `0`, `5`, `100` |
| `PLUS`, `MINUS`, `STAR`, `SLASH` | Arithmetic Operators | `+`, `-`, `*`, `/` |
| `ASSIGN` | Assignment Operator | `=` |
| `EQ`, `NEQ`, `LT`, `GT`, `LE`, `GE` | Comparison Operators | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| `LPAREN`, `RPAREN`, `LBRACE`, `RBRACE`, `SEMICOLON` | Punctuation | `(`, `)`, `{`, `}`, `;` |
| `EOF` | Control | End of File sentinel |

---

## 7. AST Design

Defined in [`ast_nodes.py`](ast_nodes.py):
- **Base Class**: `ASTNode(line, column)`
- **Expressions**: `IntegerLiteral`, `Variable`, `UnaryExpr`, `BinaryExpr`
- **Statements**: `VarDecl`, `Assignment`, `PrintStmt`, `IfStmt`, `WhileStmt`, `Block`
- **Root**: `Program`
- **Visual Dumper**: `dump_ast(node)` prints indented tree output.

---

## 8. Symbol Table and Lexical Scoping

Defined in [`symbol_table.py`](symbol_table.py):
- **`Symbol`**: Holds `name`, `type_name` (`"int"`), `line`, `column`, `scope_level`.
- **`Scope`**: Dict of symbols + reference to `parent` scope.
  - `declare(symbol)`: Adds symbol to current scope (detects duplicates).
  - `lookup(name)`: Searches current scope, then traverses up `parent` scope links.
- **`SymbolTable`**: Maintains active scope stack (`enter_scope()`, `exit_scope()`).

---

## 9. Semantic Analysis Rules

Enforced in [`semantic.py`](semantic.py):
1. **Declaration Before Use**: Variables must be declared before assignment or reference.
2. **Duplicate Declaration**: Declaring the same variable twice in the same scope throws `SemanticError`.
3. **Variable Shadowing**: Declaring a variable in a child block that shares a name with an outer variable is permitted.
4. **Scope Isolation**: Variables declared inside a block vanish when the block exits.
5. **Type Safety**: Arithmetic and comparison operations require integer operands.

---

## 10. Three-Address Code (TAC) Architecture

Generated in [`tac.py`](tac.py):
- Quadruple structure: `TACInstruction(op, arg1, arg2, result)`
- **Temporaries**: `t1`, `t2`, `t3`, ...
- **Labels**: `L1`, `L2`, `L3`, ...
- **Scope Mangling**: Name mangling (`x_s1`) guarantees variable shadowing operates cleanly in linear register memory.

---

## 11. TAC Optimization

Implemented in [`tac_opt.py`](tac_opt.py):
- **Constant Folding**: Evaluates constant math (`2 + 3 * 4` $\rightarrow$ `14`) and comparisons (`2 < 5` $\rightarrow$ `1`) at compile time.
- **Constant Propagation**: Substitutes known constants into subsequent instructions.
- **Dead Code Elimination**: Removes unreachable quadruples following unconditional `GOTO` jumps.
- **Safety**: Zero-division is NOT folded at compile time, preserving runtime error checks.

---

## 12. Interpreter Architecture

Implemented in [`interpreter.py`](interpreter.py):
- **Virtual Machine Model**: Executes linear TAC quadruples.
- **Components**: Memory map (`self.memory`), Program Counter (`self.pc`), Label map (`self.label_map`).
- **Runtime Error Detection**: Catches division by zero and undefined variable accesses.

---

## 13. Error Handling Hierarchy

Defined in [`errors.py`](errors.py):
- `SudarshanError` (with `MiniLangError` alias)
  - `LexerError`
  - `ParserError`
  - `SemanticError`
  - `RuntimeError`

---

## 14. Installation & Requirements

- **Python Version**: Python 3.10+ (Tested on Python 3.14)
- **Dependencies**: **None** (Uses Python Standard Library only)

---

## 15. How to Run

Navigate to the project root:
```bash
cd MiniLang
python3 main.py examples/valid.mini
# Or using executable CLI wrapper:
./sudarshan examples/valid.mini --all
```

---

## 16. CLI Options

| Flag | Purpose |
|---|---|
| `--tokens` | Display token stream from Lexer |
| `--ast` | Display parsed Abstract Syntax Tree |
| `--symtab` | Display global Symbol Table |
| `--tac` | Display unoptimized Three-Address Code |
| `--opt` | Display optimized Three-Address Code |
| `--explain` | Display detailed educational explanation of all phases |
| `--all` | Display output from all compiler phases |

---

## 17. Example Programs & Outputs

### 1. `examples/valid.mini`
```mini
int sum = 0;
int i = 1;

while (i <= 5) {
    sum = sum + i;
    i = i + 1;
}

print(sum);

if (sum >= 15) {
    int bonus = 100;
    print(sum + bonus);
} else {
    print(0);
}
```
**Output:**
```text
15
115
```

### 2. `examples/nested_scope.mini`
```mini
int x = 10;
{
    int y = 20;
    print(x + y);
}
{
    int x = 200;
    print(x);
}
print(x);
```
**Output:**
```text
30
200
10
```

---

## 18. Testing Instructions

Run the 22-test unittest suite:
```bash
python3 -m unittest discover -s tests
```
**Output:**
```text
......................
----------------------------------------------------------------------
Ran 22 tests in 0.001s

OK
```

---

## 19. Compiler Phases Explanation

1. **Lexical Analysis**: Reads raw characters and outputs tokens with line/column metadata.
2. **Syntax Analysis**: Enforces grammar rules and constructs a hierarchical AST.
3. **Semantic Analysis**: Ensures symbol declaration before usage and validates types.
4. **Intermediate Code Generation**: Linearizes tree structures into flat 3-Address quadruples.
5. **Intermediate Optimization**: Performs compile-time constant simplification.
6. **Code Interpretation**: Runs the linearized quadruples on a virtual machine environment.

---

## 20. Limitations

- Supports only `int` data type.
- No support for functions, arrays, floating-point numbers, or string literals.
- Simple single-file compilation.

---

## 21. Possible Future Improvements

- Add support for `float`, `bool`, and `string` data types.
- Implement functions with parameters and call stack frames.
- Add array declarations and indexing.
- Generate target assembly code (e.g., x86-64 or RISC-V).

---

## 22. Viva Questions and Answers

### Q1: What is lexical analysis?
**A**: Lexical analysis is the first phase of a compiler. It converts a raw sequence of source characters into a stream of meaningful tokens (keywords, identifiers, literals, operators) while tracking line and column information and stripping whitespace and comments.

### Q2: What is parsing?
**A**: Parsing (syntax analysis) takes the stream of tokens from the lexer and verifies whether they conform to the language's formal grammar rules, producing a hierarchical Abstract Syntax Tree (AST).

### Q3: Why use a recursive descent parser?
**A**: Recursive descent parsing is a top-down parsing technique where each non-terminal grammar rule is implemented as a function. It is easy to write by hand, readable, efficient, and direct to debug without external tools.

### Q4: What is an Abstract Syntax Tree (AST)?
**A**: An AST is a tree representation of the structural syntax of source code, omitting redundant punctuation (such as parentheses and semicolons) to focus strictly on operational logic.

### Q5: What is semantic analysis?
**A**: Semantic analysis checks static rules that cannot be captured by context-free grammars alone, such as verifying variable declaration before use, checking scope visibility, and ensuring type consistency.

### Q6: What is a symbol table?
**A**: A symbol table is a data structure used by the compiler to store information about identifiers (such as variable name, type, scope level, and declaration location) during compilation.

### Q7: What is lexical scope?
**A**: Lexical scope means that the visibility and lifetime of a variable are determined by its physical position in the source code blocks (`{ ... }`). Child blocks can access outer variables, but outer blocks cannot access child variables.

### Q8: What is variable shadowing?
**A**: Variable shadowing occurs when a variable declared within an inner block scope has the same name as a variable in an outer block scope, temporarily hiding the outer variable within the inner block.

### Q9: What is Three-Address Code (TAC)?
**A**: TAC is an intermediate representation (IR) where each instruction has at most three operands (typically two inputs and one result). It simplifies target code generation and optimization.

### Q10: Why use temporary variables in TAC?
**A**: Temporary variables (`t1`, `t2`, ...) break down complex nested expressions into flat, step-by-step linear quadruples that mirror hardware register operations.

### Q11: What is constant folding?
**A**: Constant folding is an optimization technique where constant mathematical expressions (e.g. `2 + 3 * 4`) are evaluated at compile time rather than runtime.

### Q12: What is dead code elimination?
**A**: Dead code elimination is an optimization pass that identifies and removes code that can never be executed (e.g. code following an unconditional `GOTO` jump).

### Q13: Why interpret TAC instead of executing the AST directly?
**A**: Interpreting TAC verifies that intermediate code generation works correctly and proves that the linear IR is complete and executable, demonstrating the full compiler back-end pipeline.

### Q14: What is the difference between syntax errors and semantic errors?
**A**: Syntax errors occur when code violates grammar rules (e.g. missing semicolon). Semantic errors occur when code is syntactically valid but violates static rules (e.g. using an undeclared variable).

### Q15: What is the difference between compile-time errors and runtime errors?
**A**: Compile-time errors (lexical, syntax, semantic) are detected before code execution begins. Runtime errors (e.g. division by zero) occur while the program is running.

### Q16: How are while loops represented in Three-Address Code?
**A**: A `while` loop is represented using two labels and conditional jumps: a start label (`L1`), a condition evaluation, a conditional jump (`IF_FALSE GOTO L2`), the loop body, an unconditional jump (`GOTO L1`), and an end label (`L2`).

### Q17: How is if/else represented in Three-Address Code?
**A**: `if/else` is represented using a condition evaluation, a `JUMP_IF_FALSE` to the `else` label (`L1`), the `then` branch statements, an unconditional `GOTO` to the end label (`L2`), the `else` label (`L1`), the `else` branch statements, and the end label (`L2`).

### Q18: How is division by zero handled in Sudarshan?
**A**: During TAC optimization, division by zero is safely skipped to avoid compile-time crashes. During execution, the Interpreter checks if the divisor is `0` and raises a `RuntimeError`.

### Q19: How is operator precedence implemented in your parser?
**A**: Operator precedence is implemented via grammar rule hierarchy: `comparison` methods call `addExpr` (`+`/`-`), which call `term` (`*`/`/`), which call `factor` (literals, variables, parentheses), ensuring higher precedence operators bind tighter in the AST.

### Q20: What are the main limitations of Sudarshan?
**A**: Sudarshan supports only integer variables and single-file programs without functions, arrays, floating-point numbers, or target assembly code generation.
