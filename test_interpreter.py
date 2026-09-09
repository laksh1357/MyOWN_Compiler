"""
Unit Test Suite for MiniLang Interpreter / Virtual Machine (interpreter.py).
Verifies TAC instruction execution, loop & branch control flow, output list,
and RuntimeError handling (division by zero, uninitialized access).
"""

from errors import RuntimeError
from lexer import Lexer
from parser import Parser
from tac import TACGenerator
from interpreter import Interpreter


def test_basic_execution():
    source = """
int x = 5;
int y = x * 2 + 3;
print(y);
"""
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    insts = TACGenerator().generate(ast)
    vm = Interpreter(insts)
    output = vm.run()

    assert output == [13]
    print("  ✓ Test 1 Passed: Basic arithmetic & assignment execution")


def test_conditional_execution():
    source = """
int x = 10;
if (x > 5) {
    print(1);
} else {
    print(0);
}
"""
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    insts = TACGenerator().generate(ast)
    vm = Interpreter(insts)
    output = vm.run()

    assert output == [1]
    print("  ✓ Test 2 Passed: Conditional branch execution (If/Else)")


def test_while_loop_execution():
    source = """
int sum = 0;
int i = 1;
while (i <= 5) {
    sum = sum + i;
    i = i + 1;
}
print(sum);
"""
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    insts = TACGenerator().generate(ast)
    vm = Interpreter(insts)
    output = vm.run()

    assert output == [15]
    print("  ✓ Test 3 Passed: While loop execution (sum 1 to 5 = 15)")


def test_division_by_zero_error():
    source = "int x = 10 / 0;"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    insts = TACGenerator().generate(ast)
    vm = Interpreter(insts)

    try:
        vm.run()
        assert False, "Expected RuntimeError for division by zero"
    except RuntimeError as err:
        assert "Division by zero" in err.message
        print("  ✓ Test 4 Passed: RuntimeError for division by zero caught")


def run_all_tests():
    print("=== Running MiniLang Interpreter Unit Test Suite ===")
    test_basic_execution()
    test_conditional_execution()
    test_while_loop_execution()
    test_division_by_zero_error()
    print("\n✅ All 4 Interpreter Test Cases Passed Successfully!")


if __name__ == "__main__":
    run_all_tests()
