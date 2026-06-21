#!/usr/bin/env python3
"""Test negative number handling."""

import sys
sys.path.insert(0, '.')

from exprkit import evaluate, to_rpn

print('Test with negative numbers:')
result = evaluate('(+ -3 5)')
print(f'evaluate("(+ -3 5)") = {result} (expected 2)')

result = evaluate('(- 5 -3)')
print(f'evaluate("(- 5 -3)") = {result} (expected 8)')

rpn = to_rpn('(+ -3 5)')
print(f'to_rpn("(+ -3 5)") = {rpn} (expected ["-3", "5", "+"])')
