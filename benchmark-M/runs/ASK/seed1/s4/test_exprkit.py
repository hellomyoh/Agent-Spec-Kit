#!/usr/bin/env python3
"""Test suite for exprkit."""

import sys
sys.path.insert(0, '.')

from exprkit import evaluate, to_rpn

def test_evaluate():
    """Test evaluate function."""
    test_cases = [
        ("(+ 3 4)", 7),
        ("(- (+ 1 2) 5)", -2),
        ("(- 10 3)", 7),
    ]

    print("=== Testing evaluate() ===")
    for expr, expected in test_cases:
        result = evaluate(expr)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status}: evaluate('{expr}') = {result} (expected {expected})")

def test_to_rpn():
    """Test to_rpn function."""
    rpn_test_cases = [
        ("(+ 3 4)", ["3", "4", "+"]),
        ("(- 10 3)", ["10", "3", "-"]),
        ("(- (+ 1 2) 5)", ["1", "2", "+", "5", "-"]),
    ]

    print("\n=== Testing to_rpn() ===")
    for expr, expected in rpn_test_cases:
        result = to_rpn(expr)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status}: to_rpn('{expr}') = {result} (expected {expected})")

def test_error_handling():
    """Test error handling."""
    print("\n=== Testing error handling ===")
    error_cases = [
        "(",
        ")",
        "(+)",
        "(+ 1)",
        "(+ 1 2 3)",
        "(unknown 1 2)",
        "1 2",
    ]

    for expr in error_cases:
        try:
            evaluate(expr)
            print(f"FAIL: evaluate('{expr}') should raise ValueError")
        except ValueError as e:
            print(f"PASS: evaluate('{expr}') raises ValueError")

if __name__ == '__main__':
    test_evaluate()
    test_to_rpn()
    test_error_handling()
    print("\n=== All tests completed ===")
