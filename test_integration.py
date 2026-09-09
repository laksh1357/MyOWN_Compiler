"""
End-to-End Integration Test Suite for MiniLang Compiler.

Validates the full pipeline:
Lexer -> Parser -> Semantic Analyzer -> TAC Generator -> TAC Optimizer -> Interpreter

Verifies:
1. All valid example files execute cleanly.
2. Unoptimized TAC execution and Optimized TAC execution produce identical outputs.
3. Lexical, Syntax, Semantic, and Runtime errors are caught at the exact expected pipeline phase.
4. Line and column numbers are reported on errors.
"""

from errors import LexerError, ParserError, SemanticError, RuntimeError
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from tac import TACGenerator
from tac_opt import optimize_tac
from interpreter import Interpreter


def run_pipeline(filename: str, source_code: str):
    """
    Executes the full compiler pipeline on source code and compares:
    - Output from executing unoptimized TAC
    - Output from executing optimized TAC
    """
    # Phase 1: Lexer
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    # Phase 2: Parser
    parser = Parser(tokens)
    ast = parser.parse()

    # Phase 3: Semantic Analyzer
    semantic = SemanticAnalyzer()
    symtab = semantic.analyze(ast)

    # Phase 4: TAC Generator
    tac_gen = TACGenerator()
    raw_tac = tac_gen.generate(ast)

    # Phase 4b: TAC Optimizer
    opt_tac = optimize_tac(raw_tac)

    # Phase 5: Execution of Unoptimized TAC
    vm_raw = Interpreter(raw_tac)
    raw_output = vm_raw.run()

    # Phase 5b: Execution of Optimized TAC
    vm_opt = Interpreter(opt_tac)
    opt_output = vm_opt.run()

    # Equivalence check
    assert raw_output == opt_output, (
        f"Optimization mismatch in {filename}!\n"
        f"Raw output: {raw_output}\n"
        f"Opt output: {opt_output}"
    )

    return raw_output


def test_integration():
    print("==================================================")
    print("      MINILANG END-TO-END INTEGRATION TEST        ")
    print("==================================================")

    # Test 1: valid.mini
    print("\n[1/7] Testing valid.mini...")
    with open("examples/valid.mini", "r") as f:
        out1 = run_pipeline("valid.mini", f.read())
    assert out1 == [15, 115], f"Unexpected output for valid.mini: {out1}"
    print("  ✓ valid.mini: Raw TAC and Opt TAC both produced [15, 115]")

    # Test 2: nested_scope.mini
    print("\n[2/7] Testing nested_scope.mini...")
    with open("examples/nested_scope.mini", "r") as f:
        out2 = run_pipeline("nested_scope.mini", f.read())
    assert out2 == [30, 200, 10], f"Unexpected output for nested_scope.mini: {out2}"
    print("  ✓ nested_scope.mini: Scope isolation & shadowing verified [30, 200, 10]")

    # Test 3: opt_test.mini
    print("\n[3/7] Testing opt_test.mini...")
    with open("examples/opt_test.mini", "r") as f:
        out3 = run_pipeline("opt_test.mini", f.read())
    assert out3 == [14, 40], f"Unexpected output for opt_test.mini: {out3}"
    print("  ✓ opt_test.mini: Constant folding verified [14, 40]")

    # Test 4: error_lexical.mini
    print("\n[4/7] Testing error_lexical.mini...")
    with open("examples/error_lexical.mini", "r") as f:
        src = f.read()
    try:
        run_pipeline("error_lexical.mini", src)
        assert False, "Expected LexerError"
    except LexerError as err:
        assert err.line == 6 and err.column == 9
        print(f"  ✓ error_lexical.mini: Caught LexerError at line {err.line}, col {err.column}")

    # Test 5: error_syntax.mini
    print("\n[5/7] Testing error_syntax.mini...")
    with open("examples/error_syntax.mini", "r") as f:
        src = f.read()
    try:
        run_pipeline("error_syntax.mini", src)
        assert False, "Expected ParserError"
    except ParserError as err:
        assert err.line == 6 and err.column == 1
        print(f"  ✓ error_syntax.mini: Caught ParserError at line {err.line}, col {err.column}")

    # Test 6: error_semantic.mini
    print("\n[6/7] Testing error_semantic.mini...")
    with open("examples/error_semantic.mini", "r") as f:
        src = f.read()
    try:
        run_pipeline("error_semantic.mini", src)
        assert False, "Expected SemanticError"
    except SemanticError as err:
        assert err.line == 6 and err.column == 1
        print(f"  ✓ error_semantic.mini: Caught SemanticError at line {err.line}, col {err.column}")

    # Test 7: error_runtime.mini
    print("\n[7/7] Testing error_runtime.mini...")
    with open("examples/error_runtime.mini", "r") as f:
        src = f.read()
    try:
        run_pipeline("error_runtime.mini", src)
        assert False, "Expected RuntimeError"
    except RuntimeError as err:
        assert "Division by zero" in err.message
        print(f"  ✓ error_runtime.mini: Caught RuntimeError: {err.message}")

    print("\n==================================================")
    print("✅ ALL 7 END-TO-END INTEGRATION TESTS PASSED 100%!")
    print("==================================================")


if __name__ == "__main__":
    test_integration()
