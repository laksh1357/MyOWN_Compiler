"""
Unit Test Suite for MiniLang Symbol Table (symbol_table.py).
Verifies symbol declaration, scope nesting, parent resolution, duplicate detection, and variable shadowing.
"""

from symbol_table import SymbolTable, Symbol, Scope


def test_declaration_and_lookup():
    st = SymbolTable()
    st.declare("a", "int", line=1, column=5)
    st.declare("b", "int", line=2, column=5)

    sym_a = st.lookup("a")
    assert sym_a is not None and sym_a.name == "a" and sym_a.scope_level == 0
    assert st.lookup("c") is None
    print("  ✓ Test 1 Passed: Basic declaration & lookup")


def test_nested_scope_and_parent_lookup():
    st = SymbolTable()
    st.declare("global_var", "int", line=1, column=1)

    st.enter_scope()  # Scope 1
    st.declare("local_var", "int", line=3, column=5)

    # local_var found in current scope
    assert st.lookup("local_var").scope_level == 1
    # global_var found via parent lookup
    assert st.lookup("global_var").scope_level == 0

    st.exit_scope()  # Back to Scope 0
    assert st.lookup("local_var") is None
    assert st.lookup("global_var") is not None
    print("  ✓ Test 2 Passed: Nested scope & parent lookup")


def test_duplicate_declaration_error():
    st = SymbolTable()
    st.declare("x", "int", line=1, column=1)

    try:
        st.declare("x", "int", line=2, column=1)
        assert False, "Expected ValueError on duplicate declaration"
    except ValueError as err:
        assert "Variable 'x' is already declared" in str(err)
        print("  ✓ Test 3 Passed: Duplicate declaration in same scope caught")


def test_variable_shadowing():
    st = SymbolTable()
    st.declare("x", "int", line=1, column=1)

    st.enter_scope()
    # Shadow x in scope 1
    st.declare("x", "int", line=5, column=9)
    assert st.lookup("x").line == 5
    assert st.lookup("x").scope_level == 1

    st.exit_scope()
    # x reverts to scope 0 version
    assert st.lookup("x").line == 1
    assert st.lookup("x").scope_level == 0
    print("  ✓ Test 4 Passed: Variable shadowing in nested scope")


def run_all_tests():
    print("=== Running MiniLang Symbol Table Unit Test Suite ===")
    test_declaration_and_lookup()
    test_nested_scope_and_parent_lookup()
    test_duplicate_declaration_error()
    test_variable_shadowing()
    print("\n✅ All 4 Symbol Table Test Cases Passed Successfully!")


if __name__ == "__main__":
    run_all_tests()
