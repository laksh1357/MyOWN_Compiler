"""
MiniLang Driver Program (CLI).
Integrates Lexer, Parser, Semantic Analyzer, TAC Generator, Optimizer, and Interpreter.
"""

import argparse
import sys
import os

from lexer import Lexer, LexicalError
from parser import Parser, SyntaxError
from semantic import SemanticAnalyzer, SemanticError
from tac import TACGenerator, dump_tac
from tac_opt import TACOptimizer
from interpreter import Interpreter, RuntimeError


def main():
    cli_parser = argparse.ArgumentParser(
        description="MiniLang Compiler & Interpreter Driver",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py examples/valid.mini --all
  python3 main.py examples/valid.mini --tokens --ast
  python3 main.py examples/error_syntax.mini
"""
    )
    cli_parser.add_argument("filename", help="Path to the .mini source file")
    cli_parser.add_argument("--tokens", action="store_true", help="Print lexer token stream")
    cli_parser.add_argument("--ast", action="store_true", help="Print parsed Abstract Syntax Tree (AST)")
    cli_parser.add_argument("--symtab", action="store_true", help="Print symbol table")
    cli_parser.add_argument("--tac", action="store_true", help="Print generated Three-Address Code (TAC)")
    cli_parser.add_argument("--opt", action="store_true", help="Print optimized Three-Address Code")
    cli_parser.add_argument("--all", action="store_true", help="Show output of all compiler phases")

    args = cli_parser.parse_args()

    if args.all:
        args.tokens = True
        args.ast = True
        args.symtab = True
        args.tac = True
        args.opt = True

    if not os.path.exists(args.filename):
        print(f"Error: File '{args.filename}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(args.filename, "r", encoding="utf-8") as f:
        source_code = f.read()

    print(f"=== [Phase 1] Lexical Analysis: {args.filename} ===")
    try:
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        if args.tokens:
            print("Tokens:")
            for tok in tokens:
                print(f"  {tok}")
            print()
    except LexicalError as e:
        print(f"\n❌ {e}", file=sys.stderr)
        sys.exit(1)

    print("=== [Phase 2] Syntax Analysis ===")
    try:
        parser = Parser(tokens)
        ast = parser.parse()
        if args.ast:
            print("Abstract Syntax Tree (AST):")
            print(ast.dump())
    except SyntaxError as e:
        print(f"\n❌ {e}", file=sys.stderr)
        sys.exit(1)

    print("=== [Phase 3] Semantic Analysis ===")
    try:
        semantic = SemanticAnalyzer()
        symtab = semantic.analyze(ast)
        if args.symtab:
            print("Symbol Table:")
            print(symtab.dump())
    except SemanticError as e:
        print(f"\n❌ {e}", file=sys.stderr)
        sys.exit(1)

    print("=== [Phase 4] Intermediate Code Generation (TAC) ===")
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    if args.tac:
        print("Generated Three-Address Code (TAC):")
        print(dump_tac(tac_instructions))
        print()

    tac_opt = TACOptimizer(tac_instructions)
    opt_instructions = tac_opt.optimize()
    if args.opt:
        print("Optimized Three-Address Code (TAC):")
        print(dump_tac(opt_instructions))
        print()

    print("=== [Phase 5] Execution / Interpretation ===")
    try:
        interpreter = Interpreter(opt_instructions)
        print("Program Output:")
        interpreter.execute()
        print("\n✅ Execution completed successfully.")
    except RuntimeError as e:
        print(f"\n❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
