# PHASE 1 REPORT: PROBLEM DEFINITION AND SYSTEM DESIGN

**Project Title**: MiniLang — A Compiler & Interpreter for a Simple Imperative Language  
**Course**: Compiler Design Laboratory  
**Document Type**: Phase 1 Deliverables Report (Review 1)  

---

## 1. Project Title
**MiniLang: An End-to-End Compiler and Virtual Machine Interpreter for a Simple Imperative Language**

---

## 2. Abstract
MiniLang is an individual Compiler Design Laboratory project that implements a modular, 5-phase compiler and execution engine for a custom imperative programming language. Built entirely in Python 3 using clean software engineering practices, MiniLang converts human-readable source code into tokens, constructs an Abstract Syntax Tree (AST) using recursive descent parsing, performs static type and scope resolution via a lexically-scoped Symbol Table, linearizes syntax trees into Three-Address Code (TAC) quadruples, performs compile-time constant folding optimization, and executes the resulting IR on a virtual machine environment. The project includes precise error detection with line and column tracking, a comprehensive 22-test automated test suite, and a command-line interface suitable for academic demonstration.

---

## 3. Problem Statement
Commercial and production compilers (such as GCC, Clang, or JVM) are highly complex software systems comprising millions of lines of code. For students learning Compiler Design, understanding how source code transitions through parsing, semantic analysis, intermediate representation, optimization, and execution is often hindered by the opacity of black-box parser generators or complex framework APIs (such as Lex/Yacc or LLVM).

**The Problem**: There is a need for a lightweight, fully transparent, modular, and self-contained end-to-end compiler implementation that demonstrates every classic compiler phase without external dependencies, allowing students to inspect, debug, and explain each transformation step clearly during laboratory reviews and viva examinations.

---

## 4. Motivation
Compiler Design is a foundational computer science discipline that integrates formal language theory, data structures, computer architecture, and software engineering. Developing a complete language processing system provides practical, hands-on exposure to:
1. Converting raw character streams into structured formal tokens.
2. Context-free grammar validation and tree representation.
3. Symbol table management and lexical scope isolation.
4. Quadruple-based intermediate code representation.
5. Code optimization techniques (constant folding & dead code elimination).
6. Virtual machine execution mechanics.

---

## 5. Objectives
The primary objectives of the MiniLang project are:
1. **Design a Formal Grammar**: Specify a clean BNF syntax for an imperative language supporting declarations, assignments, arithmetic/comparison operations, `if/else` conditionals, `while` loops, block scoping, and output statements.
2. **Implement Lexical Analysis**: Build a scanner to tokenize source text into structured token objects with line and column tracking.
3. **Implement Syntax Analysis**: Construct an LL(1) Recursive Descent Parser to build a hierarchical Abstract Syntax Tree (AST).
4. **Implement Semantic Analysis**: Build a tree-structured Symbol Table to enforce variable declaration before use, block scope isolation, and type safety.
5. **Generate Intermediate Code**: Translate AST nodes into Three-Address Code (TAC) quadruples with unique temporary registers and jump labels.
6. **Implement Code Optimization**: Build an optimization pass performing compile-time constant folding, constant propagation, and dead code elimination.
7. **Implement Virtual Machine Execution**: Create a TAC Interpreter that executes linear quadruples on a virtual machine environment.
8. **Provide Robust Error Handling**: Report clean, location-aware errors (`LexerError`, `ParserError`, `SemanticError`, `RuntimeError`) without Python stack traces.

---

## 6. Scope of the Project

### In-Scope Features:
- Integer variable declarations (`int x = 5;`)
- Variable assignments (`x = x + 1;`)
- Arithmetic operations (`+`, `-`, `*`, `/`, unary `-`) with mathematical precedence
- Comparison operations (`==`, `!=`, `<`, `>`, `<=`, `>=`)
- Control flow constructs (`if / else if / else` and `while` loops)
- Lexically-nested block scopes (`{ ... }`) with parent visibility and variable shadowing
- Output statements (`print(expr);`)
- CLI phase flags (`--tokens`, `--ast`, `--symtab`, `--tac`, `--opt`, `--all`)

### Out-of-Scope (Non-Goals):
- Floating-point numbers, strings, or boolean data types.
- User-defined functions, procedure call stacks, or recursion.
- Array data structures or pointer manipulation.
- Target machine code generation (e.g., x86-64 assembly).

---

## 7. Background Study
A review of classical compiler literature (Aho, Lam, Sethi, Ullman — *Compilers: Principles, Techniques, and Tools*) establishes the standard multi-phase translation pipeline:

1. **Scanner / Lexer**: Converts character streams to token streams using Regular Expressions / Finite Automata.
2. **Parser**: Translates token sequences into parse trees based on Context-Free Grammars (CFGs). Top-down recursive descent parsing is preferred for handwritten academic compilers due to its direct mapping to LL(1) grammars.
3. **Symbol Table**: Manages symbol attributes across nested scopes. Tree structures with parent pointers allow $O(1)$ block entry/exit and efficient lexical scope resolution.
4. **Three-Address Code (TAC)**: A linear intermediate representation where instructions have at most three operands. Quadruples (`op, arg1, arg2, result`) simplify optimization passes.
5. **Optimization**: Data-flow analysis techniques like constant folding simplify arithmetic expressions at compile time.

---

## 8. Compiler Design Concepts Involved

| Phase | Concept / Technique | Implementation in MiniLang |
|---|---|---|
| **Lexical Analysis** | Deterministic Finite Automata (DFA), Scanning, Line/Column Tracking | [`lexer.py`](file:///Users/lakshyasingh/.gemini/antigravity/scratch/MiniLang/lexer.py) |
| **Syntax Analysis** | Context-Free Grammar (CFG), LL(1) Recursive Descent Parsing, AST | [`parser.py`](file:///Users/lakshyasingh/.gemini/antigravity/scratch/MiniLang/parser.py), [`ast_nodes.py`](file:///Users/lakshyasingh/.gemini/antigravity/scratch/MiniLang/ast_nodes.py) |
| **Semantic Analysis** | Type Checking, Scope Resolution, Declaration Validation, Visitor Pattern | [`semantic.py`](file:///Users/lakshyasingh/.gemini/antigravity/scratch/MiniLang/semantic.py) |
| **Symbol Table** | Lexical Block Scoping, Parent-Pointer Scope Tree, Variable Shadowing | [`symbol_table.py`](file:///Users/lakshyasingh/.gemini/antigravity/scratch/MiniLang/symbol_table.py) |
| **Intermediate Code** | Three-Address Code (TAC) Quadruples, Temporary & Label Allocation | [`tac.py`](file:///Users/lakshyasingh/.gemini/antigravity/scratch/MiniLang/tac.py) |
| **Code Optimization** | Compile-time Constant Folding, Constant Propagation, Dead Code Elimination | [`tac_opt.py`](file:///Users/lakshyasingh/.gemini/antigravity/scratch/MiniLang/tac_opt.py) |
| **Code Execution** | Virtual Machine Model, Program Counter (PC), Memory Register Simulation | [`interpreter.py`](file:///Users/lakshyasingh/.gemini/antigravity/scratch/MiniLang/interpreter.py) |
| **Error Management** | Centralized Exception Hierarchy, Location-Aware Error Formatting | [`errors.py`](file:///Users/lakshyasingh/.gemini/antigravity/scratch/MiniLang/errors.py) |

---

## 9. Proposed Methodology

The project follows a structured, iterative implementation methodology:

```text
Step 1: Formal Grammar Definition & Token Spec
   │
   ▼
Step 2: Lexer & Lexical Error Handling Implementation
   │
   ▼
Step 3: AST Dataclass Hierarchy & Recursive Descent Parser
   │
   ▼
Step 4: Lexically Scoped Symbol Table & Semantic Analyzer
   │
   ▼
Step 5: TAC Quadruple Generator & Scope Name Mangling
   │
   ▼
Step 6: TAC Optimizer Pass (Constant Folding & DCE)
   │
   ▼
Step 7: TAC Virtual Machine Interpreter & Runtime Error Engine
   │
   ▼
Step 8: CLI Driver, Unittest Suite, & Project Documentation
```

---

## 10. System Architecture

```text
                  Source File (.mini)
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

## 11. Technology Stack

- **Implementation Language**: Python 3.10+ (Standard Library)
- **Zero External Dependencies**: Built without third-party parsing/scanning libraries (no Lex, Yacc, PLY, ANTLR).
- **Unit Testing Framework**: Python `unittest` standard module.
- **Version Control**: Git & GitHub ([https://github.com/laksh1357/MyOWN_Compiler](https://github.com/laksh1357/MyOWN_Compiler)).
- **Development Environment**: VS Code / Antigravity IDE on macOS.

---

## 12. Initial Prototype & Validation

An initial working prototype of MiniLang has been developed and validated:

### Sample Prototype Code (`examples/valid.mini`):
```mini
int sum = 0;
int i = 1;

while (i <= 5) {
    sum = sum + i;
    i = i + 1;
}

print(sum);
```

### Prototype Execution Command:
```bash
./minilang examples/valid.mini --all
```

### Verified Prototype Results:
- **Lexer**: Emits 45 typed tokens with exact line and column numbers.
- **Parser**: Builds `Program` AST node containing `WhileStmt` and `PrintStmt`.
- **Semantic Analyzer**: Confirms `sum` and `i` are declared in scope 0.
- **TAC Generator**: Emits 28 quadruples with labels `L1`, `L2` and temporaries `t1` to `t12`.
- **TAC Optimizer**: Folds constants at compile time.
- **Interpreter**: Executes quadruples and outputs `15` successfully.
