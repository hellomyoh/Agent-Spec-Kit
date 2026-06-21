#!/usr/bin/env python3
"""Final verification that public API matches specification."""

import sys
sys.path.insert(0, '.')

from exprkit import evaluate, to_rpn

print("FINAL VERIFICATION - PUBLIC API")
print("=" * 50)

# Verify function signatures and return types
print("\n1. Testing evaluate(s: str) -> int")
result = evaluate("(+ 3 4)")
assert isinstance(result, int), f"Expected int, got {type(result)}"
assert result == 7, f"Expected 7, got {result}"
print("   [PASS] evaluate() returns int")
print("   [PASS] evaluate('(+ 3 4)') == 7")

print("\n2. Testing to_rpn(s: str) -> list")
result = to_rpn("(+ 3 4)")
assert isinstance(result, list), f"Expected list, got {type(result)}"
assert all(isinstance(t, str) for t in result), f"Expected list of strings"
assert result == ["3", "4", "+"], f"Expected ['3', '4', '+'], got {result}"
print("   [PASS] to_rpn() returns list of strings")
print("   [PASS] to_rpn('(+ 3 4)') == ['3', '4', '+']")

print("\n3. Testing error handling")
try:
    evaluate("invalid")
    print("   [FAIL] Should have raised ValueError")
    sys.exit(1)
except ValueError:
    print("   [PASS] Raises ValueError for invalid input")

print("\n4. Testing all spec examples")
spec_examples = [
    ("(+ 3 4)", 7, ["3", "4", "+"]),
    ("(- (+ 1 2) 5)", -2, ["1", "2", "+", "5", "-"]),
    ("(- 10 3)", 7, ["10", "3", "-"]),
]

for expr, expected_eval, expected_rpn in spec_examples:
    eval_result = evaluate(expr)
    rpn_result = to_rpn(expr)
    assert eval_result == expected_eval, f"evaluate('{expr}') failed"
    assert rpn_result == expected_rpn, f"to_rpn('{expr}') failed"
    print(f"   [PASS] '{expr}' passes both evaluate and to_rpn")

print("\n" + "=" * 50)
print("PUBLIC API VERIFICATION: PASSED")
print("=" * 50)
print("\nAll requirements met:")
print("- evaluate(s: str) -> int")
print("- to_rpn(s: str) -> list[str]")
print("- Both functions handle +, - operators")
print("- Error handling with ValueError")
print("- All specification examples pass")
