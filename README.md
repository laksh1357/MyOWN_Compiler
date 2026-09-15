# Sudarshan — An End-to-End Compiler and Virtual Machine

[![Compiler Design Laboratory](https://img.shields.io/badge/Course-Compiler_Design_Laboratory-1B365D?style=for-the-badge)](https://github.com/laksh1357/MyOWN_Compiler)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Build Status](https://img.shields.io/badge/Tests-22%20Passed-success?style=for-the-badge)](tests/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

**Compiler Design Laboratory Individual Project**  
**Student Name**: Lakshya Singh | **Reg No.**: 24BDS0054  
**Project Title**: Sudarshan: An End-to-End Compiler and Virtual Machine  
**GitHub Repository**: [https://github.com/laksh1357/MyOWN_Compiler](https://github.com/laksh1357/MyOWN_Compiler)

---

## 1. Project Overview

**Sudarshan** is an imperative programming language and an end-to-end compiler pipeline implemented in Python 3.

The project implements all classic compiler construction phases:
- **Lexical Analysis**: DFA scanner & location-aware tokenizer ([`src/lexer.py`](src/lexer.py))
- **Syntax Analysis**: LL(1) recursive descent parser & AST visualizer ([`src/parser.py`](src/parser.py), [`src/ast_nodes.py`](src/ast_nodes.py))
- **Semantic Analysis**: Lexical block scope & symbol table validator ([`src/semantic.py`](src/semantic.py), [`src/symbol_table.py`](src/symbol_table.py))
- **Intermediate Code Generation**: Three-Address Code (TAC) quadruples with register allocation ([`src/tac.py`](src/tac.py))
- **Intermediate Code Optimization**: Multi-pass constant folding, constant propagation & dead code elimination ([`src/tac_opt.py`](src/tac_opt.py))
- **Virtual Machine Execution**: Linear TAC quadruples interpreter & runtime VM ([`src/interpreter.py`](src/interpreter.py))

Designed specifically for Compiler Design Laboratory evaluation, the codebase is modular, zero-dependency, type-hinted, and presentation-ready.

---

## 2. Key Features & Technical Innovations

1. **Multi-Pass Constant Folding & Propagation**: Evaluates complex compile-time arithmetic (`2 + 3 * 4` $\rightarrow$ `14`) and comparison expressions dynamically before Virtual Machine execution.
2. **Static Branch Pruning & Dead Code Elimination**: Converts constant conditional jumps (`IF_FALSE 0 GOTO L1` $\rightarrow$ `JUMP L1`) and removes unreachable quadruples following unconditional `GOTO` jumps.
3. **Scope Name Mangling for Register Isolation**: Resolves variable shadowing in flat register-based Three-Address Code by appending scope depth suffixes (`x_s1`), preserving lexical block isolation without complex stack frame overhead.
4. **AST ASCII Visualizer (`dump_ast`)**: Generates clean, hierarchical ASCII tree visualizations of Abstract Syntax Trees directly in terminal without third-party graphing dependencies.
5. **Zero-Dependency 100% Handwritten 5-Phase Architecture**: Fully handwritten scanner, parser, symbol table manager, TAC IR generator, optimizer pass, and VM interpreter built strictly with Python 3 standard library.
6. **Interactive Educational CLI Explainer (`--explain`)**: Built-in CLI flag providing step-by-step educational analysis showing transformation metrics across all 5 compiler phases.

---

## 3. Project Directory Structure

```text
MyOWN_Compiler/
├── src/                          # Phase-by-phase Compiler Source Code
│   ├── __init__.py
│   ├── errors.py                 # Centralized exception hierarchy (SudarshanError)
│   ├── lexer.py                  # Phase 1: Scanner & Tokenizer
│   ├── ast_nodes.py              # Phase 2: AST Node definitions & dump_ast() dumper
│   ├── parser.py                 # Phase 2: LL(1) Recursive Descent Parser
│   ├── symbol_table.py           # Phase 3: Lexically-scoped Symbol Table
│   ├── semantic.py               # Phase 3: Static Semantic Analyzer
│   ├── tac.py                    # Phase 4: Three-Address Code Generator
│   ├── tac_opt.py                # Phase 4b: TAC Constant Folding & DCE Optimizer
│   ├── interpreter.py            # Phase 5: Virtual Machine Interpreter
│   └── main.py                   # Central CLI Driver & Entry Point
├── tests/                        # Automated Unittest Test Suite
│   ├── test_lexer.py             # Lexer unit tests
│   ├── test_parser.py            # Parser unit tests
│   ├── test_semantic.py          # Semantic & Symbol Table unit tests
│   ├── test_tac.py               # TAC generator unit tests
│   ├── test_optimizer.py         # Constant Folding & DCE unit tests
│   └── test_interpreter.py       # Virtual Machine execution tests
├── examples/                     # Sudarshan Source Code Files (.mini)
│   ├── valid.mini                # Complete feature test (while loop, if/else, arithmetic)
│   ├── syntax_error.mini         # Syntax error handling demonstration
│   ├── semantic_error.mini       # Scope & undeclared variable error test
│   └── opt_demo.mini             # Optimization & constant folding test
├── docs/                         # Project Reports & Document Generators
│   ├── generate_pdf.py           # Pure Python PDF generator engine
│   ├── generate_phase1_pdf.py    # Generator for Phase1_Report.pdf
│   ├── generate_review1_pdf.py   # Generator for Review1_Defense_Guide.pdf
│   ├── generate_docx.py          # Generator for Phase1_Project_Report.docx
│   ├── SUDARSHAN_Compiler_Documentation.pdf
│   ├── Phase1_Report.pdf
│   ├── Review1_Defense_Guide.pdf
│   └── Phase1_Project_Report.docx
├── sudarshan                     # Executable CLI launcher script
├── README.md                     # Comprehensive documentation & Viva Q&A
└── .gitignore
```

---

## 4. Compiler Pipeline Architecture

```text
                  Source Code (.mini)
                           │
                           ▼
Phase 1: Lexical Analyzer (src/lexer.py & src/errors.py) ──► Token Stream (Line & Col tracking)
                           │
                           ▼
Phase 2: Syntax Analyzer (src/parser.py & src/ast_nodes.py) ──► Abstract Syntax Tree (AST)
                           │
                           ▼
Phase 3: Semantic Analyzer (src/semantic.py & src/symbol_table.py) ──► Scoped Symbol Table
                           │
                           ▼
Phase 4: Intermediate Code Generator (src/tac.py) ──► Three-Address Code (Quadruples)
                           │
                           ▼
Phase 4b: TAC Optimizer Pass (src/tac_opt.py) ──► Constant Folding & DCE
                           │
                           ▼
Phase 5: Virtual Machine Interpreter (src/interpreter.py) ──► Code Execution & Output
```

---

## 5. Sudarshan Formal Grammar (BNF Syntax)

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

## 6. How to Run & CLI Usage

### Quick Start
Execute the compiler using the `./sudarshan` wrapper script or `python3 src/main.py`:

```bash
# Run program execution
./sudarshan examples/valid.mini

# Display output across all compiler phases
./sudarshan examples/valid.mini --all

# Run complete automated unittest suite (22 tests)
python3 -m unittest discover -s tests
```

### Command Line Flags

| Flag | Description |
|---|---|
| `--tokens` | Display token stream generated by Lexer |
| `--ast` | Display parsed Abstract Syntax Tree |
| `--symtab` | Display global Symbol Table |
| `--tac` | Display unoptimized Three-Address Code quadruples |
| `--opt` | Display optimized Three-Address Code quadruples |
| `--explain` | Display detailed educational explanation of all phases |
| `--all` | Display output from all compiler phases |

---

---

## 8. Viva Examination Questions & Answers (20 Key Questions)

### Q1: What is lexical analysis?
**A**: Lexical analysis is the first compiler phase. It converts raw source characters into meaningful tokens while tracking line/column information and stripping comments/whitespace.

### Q2: What is parsing?
**A**: Parsing (syntax analysis) takes the token stream from the lexer and verifies whether it conforms to the formal BNF grammar, constructing an Abstract Syntax Tree (AST).

### Q3: Why recursive descent parsing?
**A**: Recursive descent parsing is a top-down technique where each non-terminal grammar rule is written as a clean, deterministic Python function. It requires zero external tools.

### Q4: What is an AST?
**A**: An Abstract Syntax Tree (AST) is a hierarchical tree representation of source code logic, omitting syntactic noise like semicolons and parentheses.

### Q5: What is semantic analysis?
**A**: Semantic analysis checks static rules that context-free grammars cannot capture, such as declaration before use, block scope visibility, and type consistency.

### Q6: What is a symbol table?
**A**: A symbol table is a data structure storing identifier metadata (name, type, scope level, declaration location) during compilation.

### Q7: What is lexical scope?
**A**: Lexical scope means variable visibility is determined by physical position in block structures (`{ ... }`). Child blocks access parent variables, but not vice-versa.

### Q8: What is variable shadowing?
**A**: Variable shadowing occurs when an inner block declares a variable with the same name as an outer variable, temporarily hiding the outer declaration.

### Q9: What is Three-Address Code (TAC)?
**A**: TAC is an intermediate representation where each quadruple has at most 3 operands, breaking complex logic into flat, register-like hardware steps.

### Q10: Why use temporary variables in TAC?
**A**: Temporary variables (`t1`, `t2`, ...) break down nested AST expressions into linear step-by-step instructions.

### Q11: What is constant folding?
**A**: Constant folding evaluates constant expressions (e.g. `2 + 3 * 4` $\rightarrow$ `14`) at compile time to save runtime computation.

### Q12: What is dead code elimination?
**A**: Dead code elimination removes unreachable instructions (e.g. quadruples following an unconditional `GOTO` jump).

### Q13: Why interpret TAC instead of AST directly?
**A**: Interpreting TAC proves that intermediate code generation works correctly and demonstrates a complete 5-phase compiler pipeline.

### Q14: Difference between syntax and semantic errors?
**A**: Syntax errors violate grammar rules (e.g. missing semicolon). Semantic errors violate static logic rules (e.g. using an undeclared variable).

### Q15: Difference between compile-time and runtime errors?
**A**: Compile-time errors (lexical, syntax, semantic) are caught before execution. Runtime errors (e.g. division by zero) occur during VM execution.

### Q16: How are while loops represented in TAC?
**A**: Using two labels and jumps: a start label `L1`, condition evaluation, `IF_FALSE GOTO L2`, body quadruples, `GOTO L1`, and end label `L2`.

### Q17: How is if/else represented in TAC?
**A**: Condition evaluation, `IF_FALSE GOTO L1` (else), then-branch quadruples, `GOTO L2` (end), label `L1`, else-branch quadruples, label `L2`.

### Q18: How is division by zero handled?
**A**: Skipped during compile-time constant folding to avoid compiler crashes; caught during VM execution by raising a clean `RuntimeError`.

### Q19: How is operator precedence implemented?
**A**: Through grammar method hierarchy: comparison $\rightarrow$ addExpr (`+`/`-`) $\rightarrow$ term (`*`/`/`) $\rightarrow$ factor, ensuring higher precedence operators bind deeper in AST.

### Q20: What are the main limitations of Sudarshan?
**A**: Sudarshan supports only integer variables and single-file programs without functions, arrays, floats, or target assembly code generation.

---

## 9. Documentation & Reports

Generated documentation reports are available in the [`docs/`](docs/) directory:
- [`docs/SUDARSHAN_Compiler_Documentation.pdf`](docs/SUDARSHAN_Compiler_Documentation.pdf) — Complete technical specification & viva documentation
- [`docs/Phase1_Report.pdf`](docs/Phase1_Report.pdf) — Executive phase 1 summary report
- [`docs/Review1_Defense_Guide.pdf`](docs/Review1_Defense_Guide.pdf) — Panel presentation & defense guide
- [`docs/Phase1_Project_Report.docx`](docs/Phase1_Project_Report.docx) — Formal Microsoft Word laboratory submission report

---

## 10. License

This project is open-source under the MIT License.
