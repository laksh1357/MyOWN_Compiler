"""
Generates Review1_Defense_Guide.pdf for Sudarshan Compiler Project Review 1 Evaluation.
Uses pure Python 3 without external dependencies.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from generate_pdf import SimplePDFWriter

def generate_review1_pdf():
    out_path = os.path.join(os.path.dirname(__file__), "Review1_Defense_Guide.pdf")
    pdf = SimplePDFWriter(out_path)
    pdf.new_page()

    # Header & Title
    pdf.add_title("REVIEW 1: PROJECT PROPOSAL & DESIGN REVIEW DEFENSE GUIDE")
    pdf.add_paragraph("Course: Compiler Design Laboratory | Review 1 Evaluation (20 Marks)")
    pdf.add_paragraph("Student Name: Lakshya Singh | Reg No.: 24BDS0054")
    pdf.add_paragraph("Project Title: Sudarshan: An End-to-End Compiler and Virtual Machine")
    pdf.add_paragraph("Repository: https://github.com/laksh1357/MyOWN_Compiler")

    # 1. Evaluation Rubric
    pdf.add_heading1("1. Review 1 Marks Breakdown (20/20 Marks)")
    pdf.add_code_block(
        "Criteria                       What Evaluators Look For            Marks\n"
        "-------------------------------------------------------------------------\n"
        "1. Topic Selection             Compiler Design Relevance           3 / 3\n"
        "2. Problem Statement           Clarity & Significance              3 / 3\n"
        "3. Objectives                  Clearly Defined Objectives          2 / 2\n"
        "4. Technical Feasibility       Implementation Feasibility          4 / 4\n"
        "5. Compiler Concepts           Appropriate Concepts Identified     3 / 3\n"
        "6. System Architecture         Quality of Design & Data Flow       4 / 4\n"
        "7. Innovation                  Originality (Optimization/DCE)      2 / 2\n"
        "8. Prototype                   Initial Working Implementation      3 / 3\n"
        "-------------------------------------------------------------------------\n"
        "TOTAL MARKS                                                       20 / 20"
    )

    # 2. Presentation Script
    pdf.add_heading1("2. Panel Presentation Script & System Architecture")
    pdf.add_paragraph(
        "Problem Statement: Production compilers (GCC, Clang) are black boxes comprising millions of lines. "
        "Sudarshan provides a transparent, zero-dependency 5-phase compiler pipeline in Python 3."
    )
    pdf.add_code_block(
        "Source Code (.mini)\n"
        "        │\n"
        "Phase 1: Lexical Analysis (lexer.py)              ──► Token Stream (Line/Col info)\n"
        "        │\n"
        "Phase 2: Syntax Analysis (parser.py & ast_nodes.py) ──► Abstract Syntax Tree (AST)\n"
        "        │\n"
        "Phase 3: Semantic Analysis (semantic.py)          ──► Scoped Symbol Table\n"
        "        │\n"
        "Phase 4: Intermediate Code Generator (tac.py)     ──► 3-Address Code Quadruples\n"
        "        │\n"
        "Phase 4b: Code Optimization Pass (tac_opt.py)     ──► Constant Folding & DCE\n"
        "        │\n"
        "Phase 5: Virtual Machine Interpreter (interpreter.py) ──► Code Execution & Output"
    )

    # 3. Prototype Demonstration
    pdf.add_heading1("3. Working Prototype Demonstration")
    pdf.add_paragraph("Demonstrate live CLI in terminal during Review 1:")
    pdf.add_code_block(
        "./sudarshan examples/valid.mini --all"
    )

    pdf.save()

if __name__ == "__main__":
    generate_review1_pdf()
