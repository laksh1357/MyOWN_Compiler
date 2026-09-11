"""
Pure Python 3 PDF Generator for MiniLang Compiler Project Documentation.
No external dependencies or pip packages required. Generates standard PDF 1.4 file.
"""

import sys
import os

class SimplePDFWriter:
    """A pure Python class to generate valid PDF 1.4 documents."""

    def __init__(self, filename: str):
        self.filename = filename
        self.objects = []
        self.pages = []
        self.content_streams = []
        self.page_width = 595  # A4 width in points
        self.page_height = 842 # A4 height in points
        self.margin = 40
        self.y_cursor = self.page_height - self.margin
        self.current_stream = []
        self.page_number = 0

    def _add_object(self, content: str) -> int:
        self.objects.append(content)
        return len(self.objects)

    def new_page(self):
        if self.current_stream:
            self.content_streams.append("\n".join(self.current_stream))
            self.current_stream = []
        self.page_number += 1
        self.y_cursor = self.page_height - self.margin - 20
        # Draw header / line
        self.current_stream.append("0.2 0.2 0.2 RG 0.5 w")
        self.current_stream.append(f"40 {self.page_height - 35} m 555 {self.page_height - 35} l S")
        self.current_stream.append("BT /F1 9 Tf 0.3 0.3 0.3 rg 40 " + str(self.page_height - 30) + " Td (Sudarshan Compiler Design Laboratory Documentation) Tj ET")
        self.current_stream.append("BT /F1 9 Tf 0.3 0.3 0.3 rg 480 " + str(self.page_height - 30) + " Td (Page " + str(self.page_number) + ") Tj ET")

    def add_title(self, text: str):
        self._check_space(50)
        self.current_stream.append("BT /F2 20 Tf 0.1 0.2 0.5 rg 40 " + str(self.y_cursor) + " Td (" + self._escape(text) + ") Tj ET")
        self.y_cursor -= 30

    def add_heading1(self, text: str):
        self._check_space(35)
        self.y_cursor -= 10
        self.current_stream.append("BT /F2 14 Tf 0.13 0.31 0.55 rg 40 " + str(self.y_cursor) + " Td (" + self._escape(text) + ") Tj ET")
        self.y_cursor -= 20
        # Underline
        self.current_stream.append("0.13 0.31 0.55 RG 1 w")
        self.current_stream.append(f"40 {self.y_cursor + 15} m 555 {self.y_cursor + 15} l S")

    def add_heading2(self, text: str):
        self._check_space(25)
        self.y_cursor -= 5
        self.current_stream.append("BT /F2 11 Tf 0.2 0.2 0.2 rg 40 " + str(self.y_cursor) + " Td (" + self._escape(text) + ") Tj ET")
        self.y_cursor -= 16

    def add_paragraph(self, text: str):
        lines = self._wrap_text(text, font_size=10, max_width=515)
        for line in lines:
            self._check_space(14)
            self.current_stream.append("BT /F1 10 Tf 0.1 0.1 0.1 rg 40 " + str(self.y_cursor) + " Td (" + self._escape(line) + ") Tj ET")
            self.y_cursor -= 13
        self.y_cursor -= 4

    def add_code_block(self, code_text: str):
        lines = code_text.strip().split("\n")
        block_height = len(lines) * 12 + 12
        self._check_space(min(block_height, 200))

        start_y = self.y_cursor
        # Background box
        box_top = self.y_cursor + 5
        box_bottom = self.y_cursor - (len(lines) * 12) - 5
        self.current_stream.append(f"0.95 0.95 0.96 rg 40 {box_bottom} 515 {box_top - box_bottom} re f")
        self.current_stream.append(f"0.8 0.8 0.85 RG 0.5 w 40 {box_bottom} 515 {box_top - box_bottom} re s")

        self.y_cursor -= 8
        for line in lines:
            self._check_space(12)
            self.current_stream.append("BT /F3 9 Tf 0.15 0.15 0.25 rg 48 " + str(self.y_cursor) + " Td (" + self._escape(line) + ") Tj ET")
            self.y_cursor -= 12
        self.y_cursor -= 8

    def _check_space(self, needed: float):
        if self.y_cursor - needed < self.margin + 20:
            self.new_page()

    def _wrap_text(self, text: str, font_size: int, max_width: int) -> list[str]:
        words = text.split(" ")
        lines = []
        current_line = []
        # Rough char width estimate: 0.5 * font_size
        char_width = font_size * 0.52
        max_chars = int(max_width / char_width)

        for word in words:
            test_line = " ".join(current_line + [word])
            if len(test_line) <= max_chars:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
        return lines

    def _escape(self, text: str) -> str:
        return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    def save(self):
        if self.current_stream:
            self.content_streams.append("\n".join(self.current_stream))

        # Build PDF structure
        # Obj 1: Catalog
        # Obj 2: Outlines
        # Obj 3: Pages
        # Obj 4: Font F1 (Helvetica)
        # Obj 5: Font F2 (Helvetica-Bold)
        # Obj 6: Font F3 (Courier)
        # Obj 7..N: Content streams & Page objects

        num_pages = len(self.content_streams)

        pdf_bytes = bytearray()
        pdf_bytes.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")

        offsets = {}

        # 1. Catalog
        offsets[1] = len(pdf_bytes)
        pdf_bytes.extend(b"1 0 obj\n<< /Type /Catalog /Pages 3 0 R >>\nendobj\n")

        # 2. Outlines
        offsets[2] = len(pdf_bytes)
        pdf_bytes.extend(b"2 0 obj\n<< /Type /Outlines /Count 0 >>\nendobj\n")

        # Fonts
        offsets[4] = len(pdf_bytes)
        pdf_bytes.extend(b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")

        offsets[5] = len(pdf_bytes)
        pdf_bytes.extend(b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n")

        offsets[6] = len(pdf_bytes)
        pdf_bytes.extend(b"6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>\nendobj\n")

        # Page object IDs start after fonts + streams
        page_obj_ids = []
        stream_obj_ids = []

        next_obj_id = 7
        for i in range(num_pages):
            stream_obj_ids.append(next_obj_id)
            next_obj_id += 1
            page_obj_ids.append(next_obj_id)
            next_obj_id += 1

        # 3. Pages object
        offsets[3] = len(pdf_bytes)
        pages_kids = " ".join(f"{pid} 0 R" for pid in page_obj_ids)
        pdf_bytes.extend(f"3 0 obj\n<< /Type /Pages /Count {num_pages} /Kids [{pages_kids}] >>\nendobj\n".encode("utf-8"))

        # Streams and Pages
        for i in range(num_pages):
            sid = stream_obj_ids[i]
            pid = page_obj_ids[i]
            stream_content = self.content_streams[i].encode("utf-8")

            # Stream object
            offsets[sid] = len(pdf_bytes)
            stream_header = f"{sid} 0 obj\n<< /Length {len(stream_content)} >>\nstream\n".encode("utf-8")
            pdf_bytes.extend(stream_header)
            pdf_bytes.extend(stream_content)
            pdf_bytes.extend(b"\nendstream\nendobj\n")

            # Page object
            offsets[pid] = len(pdf_bytes)
            page_dict = (
                f"{pid} 0 obj\n"
                f"<< /Type /Page /Parent 3 0 R /MediaBox [0 0 595 842] "
                f"/Contents {sid} 0 R /Resources << /Font << /F1 4 0 R /F2 5 0 R /F3 6 0 R >> >> >>\n"
                f"endobj\n"
            ).encode("utf-8")
            pdf_bytes.extend(page_dict)

        # XRef table
        xref_offset = len(pdf_bytes)
        total_objs = max(offsets.keys()) + 1
        pdf_bytes.extend(f"xref\n0 {total_objs}\n0000000000 65535 f \n".encode("utf-8"))
        for oid in range(1, total_objs):
            off = offsets.get(oid, 0)
            pdf_bytes.extend(f"{off:010d} 00000 n \n".encode("utf-8"))

        # Trailer
        pdf_bytes.extend(
            f"trailer\n<< /Size {total_objs} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n".encode("utf-8")
        )

        with open(self.filename, "wb") as f:
            f.write(pdf_bytes)
        print(f"✅ Generated PDF document: {self.filename} ({len(pdf_bytes)} bytes, {num_pages} pages)")


def generate_doc_pdf(output_path: str):
    pdf = SimplePDFWriter(output_path)
    pdf.new_page()

    # Title
    pdf.add_title("Sudarshan Compiler Design Laboratory")
    pdf.add_paragraph("Comprehensive Technical Specification & Viva Examination Documentation")
    pdf.add_paragraph("Author: Lakshya Singh (Reg No.: 24BDS0054) | Repository: https://github.com/laksh1357/MyOWN_Compiler")

    # Section 1: Overview
    pdf.add_heading1("1. Project Overview & Architecture")
    pdf.add_paragraph(
        "Sudarshan is a clean, modular imperative programming language implemented in Python 3. "
        "The compiler architecture strictly implements all 5 classic compiler pipeline phases: "
        "Lexical Analysis, Syntax Analysis (AST), Semantic Analysis (Symbol Table), Three-Address Code (TAC) Generation & Optimization, and Virtual Machine Execution."
    )

    pdf.add_code_block(
        "Source Code (.mini)\n"
        "        │\n"
        "Phase 1: Lexer (lexer.py)              ──► Token Stream (Line/Col info)\n"
        "        │\n"
        "Phase 2: Parser (parser.py & ast_nodes.py) ──► Abstract Syntax Tree (AST)\n"
        "        │\n"
        "Phase 3: Semantic Analyzer (semantic.py)──► Scoped Symbol Table\n"
        "        │\n"
        "Phase 4: TAC Generator (tac.py & tac_opt.py)──► 3-Address Code Quadruples\n"
        "        │\n"
        "Phase 5: Virtual Machine (interpreter.py)──► Execution & Output"
    )

    pdf.add_heading2("Key Technical Innovations")
    pdf.add_paragraph("1. Multi-Pass Constant Folding & Propagation: Evaluates math & comparison logic at compile time.")
    pdf.add_paragraph("2. Static Branch Pruning & DCE: Converts constant branches (IF_FALSE 0 -> JUMP) and eliminates dead quadruples.")
    pdf.add_paragraph("3. Scope Name Mangling: Preserves block scope isolation (x_s1) in flat register TAC memory.")
    pdf.add_paragraph("4. AST ASCII Visualizer: Formats syntax tree hierarchies into clean ASCII trees without third-party tools.")
    pdf.add_paragraph("5. Zero-Dependency Handwritten Pipeline: 100% handwritten scanner, parser, symbol table, TAC IR, VM.")

    # Section 2: Complete Walkthrough
    pdf.add_heading1("2. End-to-End Program Transformation Walkthrough")
    pdf.add_paragraph("Sample Sudarshan Program:")
    pdf.add_code_block("int x = 5;\nwhile (x < 10) {\n    print(x);\n    x = x + 1;\n}")

    pdf.add_heading2("Phase 1: Lexical Analysis (lexer.py)")
    pdf.add_paragraph("Scans source string character by character. Converts text into a stream of typed Token objects with precise line and column tracking.")
    pdf.add_code_block(
        "[Token(INT, 'int', L1:C1), Token(ID, 'x', L1:C5), Token(ASSIGN, '=', L1:C7),\n"
        " Token(NUMBER, 5, L1:C9), Token(SEMICOLON, ';', L1:C10),\n"
        " Token(WHILE, 'while', L2:C1), Token(LPAREN, '(', L2:C7), Token(ID, 'x', L2:C8),\n"
        " Token(LT, '<', L2:C10), Token(NUMBER, 10, L2:C12), Token(RPAREN, ')', L2:C14),\n"
        " Token(LBRACE, '{', L2:C16), Token(PRINT, 'print', L3:C5), Token(ID, 'x', L3:C11),\n"
        " Token(SEMICOLON, ';', L3:C13), Token(ID, 'x', L4:C5), Token(ASSIGN, '=', L4:C7),\n"
        " Token(ID, 'x', L4:C9), Token(PLUS, '+', L4:C11), Token(NUMBER, 1, L4:C13),\n"
        " Token(SEMICOLON, ';', L4:C14), Token(RBRACE, '}', L5:C1), Token(EOF, 'EOF', L5:C2)]"
    )

    pdf.add_heading2("Phase 2: Syntax Analysis (parser.py)")
    pdf.add_paragraph("LL(1) Recursive Descent parser enforcing mathematical operator precedence to construct the hierarchical Abstract Syntax Tree.")
    pdf.add_code_block(
        "Program:\n"
        "  VarDecl (int x):\n"
        "    IntegerLiteral(5)\n"
        "  WhileStmt:\n"
        "    Condition:\n"
        "      BinaryExpr ('<'):\n"
        "        Variable(x)\n"
        "        IntegerLiteral(10)\n"
        "    Body:\n"
        "      Block:\n"
        "        PrintStmt:\n"
        "          Variable(x)\n"
        "        Assignment (x =):\n"
        "          BinaryExpr ('+'):\n"
        "            Variable(x)\n"
        "            IntegerLiteral(1)"
    )

    pdf.add_heading2("Phase 3: Semantic Analysis (semantic.py & symbol_table.py)")
    pdf.add_paragraph("Performs AST Visitor traversal to verify variable declaration before use, prevent duplicate declarations in the same scope, and manage lexical scope hierarchies.")
    pdf.add_code_block("=== Scope Level 0 ===\n  Symbol(x: int, Scope 0 (L1:C1))")

    pdf.add_heading2("Phase 4: Intermediate Code Generation (tac.py)")
    pdf.add_paragraph("Translates AST nodes into linear 3-Address Code quadruples (op, arg1, arg2, result) with unique temporary registers and jump labels.")
    pdf.add_code_block(
        " 1:   t1 = 5\n"
        " 2:   x = t1\n"
        " 3: L1:\n"
        " 4:   t2 = 10\n"
        " 5:   t3 = x LT t2\n"
        " 6:   IF_FALSE t3 GOTO L2\n"
        " 7:   PRINT x\n"
        " 8:   t4 = 1\n"
        " 9:   t5 = x ADD t4\n"
        "10:   x = t5\n"
        "11:   GOTO L1\n"
        "12: L2:"
    )

    pdf.add_heading2("Phase 5: Code Execution / Virtual Machine (interpreter.py)")
    pdf.add_paragraph("Executes TAC quadruples on a virtual machine environment with a program counter and memory map.")
    pdf.add_code_block("Program Execution Output:\n5\n6\n7\n8\n9\n\nExecution finished successfully.")

    # Section 3: Viva Q&A
    pdf.add_heading1("3. Viva Examination Questions & Answers (20 Key Questions)")

    viva_qas = [
        ("Q1: What is lexical analysis?", "Lexical analysis is the first compiler phase. It converts raw source characters into meaningful tokens while tracking line/column information and stripping comments/whitespace."),
        ("Q2: What is parsing?", "Parsing (syntax analysis) takes the token stream from the lexer and verifies whether it conforms to the formal BNF grammar, constructing an Abstract Syntax Tree (AST)."),
        ("Q3: Why recursive descent parsing?", "Recursive descent parsing is a top-down technique where each non-terminal grammar rule is written as a clean, deterministic Python function. It requires zero external tools."),
        ("Q4: What is an AST?", "An Abstract Syntax Tree (AST) is a hierarchical tree representation of source code logic, omitting syntactic noise like semicolons and parentheses."),
        ("Q5: What is semantic analysis?", "Semantic analysis checks static rules that context-free grammars cannot capture, such as declaration before use, block scope visibility, and type consistency."),
        ("Q6: What is a symbol table?", "A symbol table is a data structure storing identifier metadata (name, type, scope level, declaration location) during compilation."),
        ("Q7: What is lexical scope?", "Lexical scope means variable visibility is determined by physical position in block structures ({ ... }). Child blocks access parent variables, but not vice-versa."),
        ("Q8: What is variable shadowing?", "Variable shadowing occurs when an inner block declares a variable with the same name as an outer variable, temporarily hiding the outer declaration."),
        ("Q9: What is Three-Address Code (TAC)?", "TAC is an intermediate representation where each quadruple has at most 3 operands, breaking complex logic into flat, register-like hardware steps."),
        ("Q10: Why use temporary variables in TAC?", "Temporary variables (t1, t2, ...) break down nested AST expressions into linear step-by-step instructions."),
        ("Q11: What is constant folding?", "Constant folding evaluates constant expressions (e.g. 2 + 3 * 4 -> 14) at compile time to save runtime computation."),
        ("Q12: What is dead code elimination?", "Dead code elimination removes unreachable instructions (e.g. quadruples following an unconditional GOTO jump)."),
        ("Q13: Why interpret TAC instead of AST directly?", "Interpreting TAC proves that intermediate code generation works correctly and demonstrates a complete 5-phase compiler pipeline."),
        ("Q14: Difference between syntax and semantic errors?", "Syntax errors violate grammar rules (e.g. missing semicolon). Semantic errors violate static logic rules (e.g. using an undeclared variable)."),
        ("Q15: Difference between compile-time and runtime errors?", "Compile-time errors (lexical, syntax, semantic) are caught before execution. Runtime errors (e.g. division by zero) occur during VM execution."),
        ("Q16: How are while loops represented in TAC?", "Using two labels and jumps: a start label L1, condition evaluation, IF_FALSE GOTO L2, body quadruples, GOTO L1, and end label L2."),
        ("Q17: How is if/else represented in TAC?", "Condition evaluation, IF_FALSE GOTO L1 (else), then-branch quadruples, GOTO L2 (end), label L1, else-branch quadruples, label L2."),
        ("Q18: How is division by zero handled?", "Skipped during compile-time constant folding to avoid compiler crashes; caught during VM execution by raising a clean RuntimeError."),
        ("Q19: How is operator precedence implemented?", "Through grammar method hierarchy: comparison -> addExpr (+/-) -> term (*//) -> factor, ensuring higher precedence operators bind deeper in AST."),
        ("Q20: What are the main limitations of Sudarshan?", "Sudarshan supports only integer variables and single-file programs without functions, arrays, floats, or target assembly code generation.")
    ]

    for q, a in viva_qas:
        pdf.add_heading2(q)
        pdf.add_paragraph(a)

    pdf.save()

if __name__ == "__main__":
    out_file = "SUDARSHAN_Compiler_Documentation.pdf"
    generate_doc_pdf(out_file)
