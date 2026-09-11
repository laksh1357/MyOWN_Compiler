# REVIEW 1: PROJECT PROPOSAL & DESIGN REVIEW DEFENSE GUIDE

**Project Title**: Sudarshan: An End-to-End Compiler and Virtual Machine  
**Course**: Compiler Design Laboratory  
**Evaluation Rubric**: Review 1 (20 Marks Total)  

---

## 📊 Review 1 Evaluation Rubric & Marks Mapping

| Evaluation Criteria | What Evaluators Look For | Sudarshan Defense / Proof | Marks |
|---|---|---|---|
| **1. Topic Selection** | Relevance to Compiler Design | Implements full 5-phase compiler pipeline (Lexer, Parser, Symbol Table, TAC IR, VM Interpreter). | **3 / 3** |
| **2. Problem Statement** | Clarity and significance | Solves the opacity problem of black-box parser generators by providing a transparent, 100% handwritten pipeline. | **3 / 3** |
| **3. Objectives** | Clearly defined objectives | 8 specific functional & technical objectives for language processing. | **2 / 2** |
| **4. Technical Feasibility** | Possibility of implementation | 100% complete, functional, type-hinted Python 3 implementation with 22 automated unittests. | **4 / 4** |
| **5. Compiler Concepts** | Appropriate concepts identified | DFAs, LL(1) Recursive Descent Parsing, AST Visitor, Lexical Scope Trees, TAC Quadruples, Constant Folding. | **3 / 3** |
| **6. System Architecture** | Quality of design | Clean modular design with strict single-responsibility files (`lexer.py`, `parser.py`, `semantic.py`, etc.). | **4 / 4** |
| **7. Innovation** | Originality | **TAC Constant Folding & DCE Optimizer Pass**, **AST Tree Dumper**, and **Scope Name Mangling**. | **2 / 2** |
| **8. Prototype** | Initial implementation | Working CLI prototype `./sudarshan` & `python3 main.py` running live programs. | **3 / 3** |
| **9. Viva** | Individual understanding | Complete technical understanding and viva preparation questions script. | **Evaluated** |
| **TOTAL** | | | **20 / 20** |

---

## 🎙️ Step-by-Step Presentation Script for Review 1 Panel

### 1. Topic Selection & Title (3 Marks)
> *"Good morning respected faculty panel. My project for the Compiler Design Laboratory is titled **Sudarshan: An End-to-End Compiler and Virtual Machine**. It is a complete, modular compiler implementation written in Python 3 that covers all fundamental concepts of Compiler Design."*

### 2. Problem Statement (3 Marks)
> *"Industrial compilers like GCC, Clang, or JVM are millions of lines of code and rely on black-box tools like Lex, Yacc, or LLVM. This makes it difficult for students to observe how source code transforms through each intermediate phase. The goal of Sudarshan is to create a 100% transparent, self-contained, 5-phase compiler where every single phase—from scanning and recursive descent parsing to Three-Address Code generation, optimization, and virtual machine execution—is handwritten without any third-party dependencies."*

### 3. Objectives & Scope (2 Marks)
> *"The key objectives of Sudarshan are:
> 1. Design a formal BNF grammar supporting variables, arithmetic/comparison ops, `if/else`, `while` loops, block scoping, and `print`.
> 2. Build a Lexer with line and column error tracking.
> 3. Build a Recursive Descent Parser emitting an Abstract Syntax Tree (AST).
> 4. Build a Tree-structured Symbol Table enforcing static declaration before use and lexical block scoping.
> 5. Generate Three-Address Code (TAC) quadruples.
> 6. Implement a TAC Optimizer pass performing compile-time Constant Folding.
> 7. Implement a Virtual Machine Interpreter to execute TAC instructions."*

### 4. Compiler Design Concepts & Technical Feasibility (4 + 3 = 7 Marks)
> *"Sudarshan demonstrates all core compiler concepts:
> - **Phase 1 (Lexer)**: DFA-based token scanning with line/col metadata.
> - **Phase 2 (Parser)**: LL(1) Top-Down Recursive Descent parsing with operator precedence.
> - **Phase 3 (Semantics)**: Lexical scope resolution via parent-pointer scope trees.
> - **Phase 4 (Intermediate Code)**: TAC Quadruples (`op, arg1, arg2, result`) with temporary register allocation (`t1`, `t2`).
> - **Phase 4b (Optimizer)**: Data-flow constant folding (`2 + 3 * 4` -> `14`).
> - **Phase 5 (Execution)**: Von Neumann Virtual Machine with a program counter (PC) and register memory mapping."*

### 5. System Architecture (4 Marks)
```text
Source Code (.mini)
        │
        ▼
Phase 1: Lexical Analysis (lexer.py & errors.py)      ──► Token Stream (Line & Col tracking)
        │
        ▼
Phase 2: Syntax Analysis (parser.py & ast_nodes.py)   ──► Abstract Syntax Tree (AST)
        │
        ▼
Phase 3: Semantic Analysis (semantic.py & symbol_table.py) ──► Lexically Scoped Symbol Table
        │
        ▼
Phase 4: Intermediate Code Generation (tac.py)        ──► Three-Address Code (Quadruples)
        │
        ▼
Phase 4b: TAC Optimization (tac_opt.py)               ──► Constant Folding & DCE
        │
        ▼
Phase 5: Virtual Machine Execution (interpreter.py)   ──► Code Execution & Output
```

### 6. Innovation & Originality (2 Marks)
> *"To go beyond basic compiler requirements:
> 1. **TAC Constant Folding Optimizer Pass**: Evaluates arithmetic expressions and constant jumps at compile time.
> 2. **AST Tree Visualizer (`dump_ast`)**: Formats syntax tree hierarchies into readable indented ASCII trees.
> 3. **Scope Name Mangling**: Resolves variable shadowing in linear TAC instructions without flattening scope metadata."*

### 7. Working Prototype Demonstration (3 Marks)
> *"I will now demonstrate our working prototype live in terminal."*

Run the following command during Review 1:
```bash
./sudarshan examples/valid.mini --all
```

---

## 🎯 Review 1 Panel Viva Preparation Q&A

### Q1: Why did you choose Python for implementing a compiler?
**A**: Python is an officially recommended language in Section 20 of our lab manual. Its standard library (`dataclasses`, `enum`, `typing`, `unittest`) allows us to write clean, type-hinted object-oriented code without needing external dependencies like PLY or ANTLR.

### Q2: How does your parser implement operator precedence?
**A**: Through grammar rule hierarchy in recursive descent: `comparison` calls `addExpr` (`+`/`-`), which calls `term` (`*`/`/`), which calls `factor` (literals, variables, parentheses). Higher precedence operators sit deeper in the AST.

### Q3: What is the deliverable status of Phase 1?
**A**: Phase 1 is 100% complete. All 12 deliverables specified in Section 8.3 are fully documented in [`Phase1_Report.md`](file:///Users/lakshyasingh/.gemini/antigravity/scratch/MiniLang/Phase1_Report.md) and [`Phase1_Report.pdf`](file:///Users/lakshyasingh/.gemini/antigravity/scratch/MiniLang/Phase1_Report.pdf), and the working prototype is live on GitHub at `https://github.com/laksh1357/MyOWN_Compiler`.
