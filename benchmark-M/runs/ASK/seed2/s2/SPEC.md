# exprkit — Public API Specification

## Overview
`exprkit` is a Python package for evaluating and compiling prefix s-expression integer arithmetic using standard library only.

## Public API

### `evaluate(s: str) -> int`
Evaluates a prefix s-expression and returns the integer result.

**Examples:**
```python
evaluate("(+ 3 4)")           # Returns 7
evaluate("(- (+ 1 2) 5)")     # Returns -2
evaluate("42")                # Returns 42
evaluate("-3")                # Returns -3
```

**Error Handling:**
- Raises `ValueError` for malformed input (unbalanced parentheses, invalid operators, missing operands, etc.)

### `to_rpn(s: str) -> list`
Converts a prefix s-expression to Reverse Polish Notation (postfix) format.

Returns a list of token strings in postfix order (operands first, then operator).

**Examples:**
```python
to_rpn("(+ 3 4)")             # Returns ["3", "4", "+"]
to_rpn("(- 10 3)")            # Returns ["10", "3", "-"]
to_rpn("(+ (- 5 2) 3)")       # Returns ["5", "2", "-", "3", "+"]
```

**Error Handling:**
- Raises `ValueError` for malformed input.

## Syntax

### Integer Atoms
- Positive integers: `0`, `1`, `42`, `999`
- Negative integers: `-1`, `-3`, `-42`

### Prefix Forms
- Syntax: `(OP ARG ...)`
- Operators are symbols following `(`
- Arguments follow the operator (can be atoms or nested prefix forms)

### Whitespace
- Whitespace separates tokens
- Multiple spaces, tabs, and newlines are handled

## Supported Operators

| Operator | Arity | Description | Example |
|----------|-------|-------------|---------|
| `+` | 2 | Addition | `(+ 3 4)` → 7 |
| `-` | 2 | Subtraction | `(- 10 3)` → 7 |
| `*` | 2 | Multiplication | `(* 6 7)` → 42 |
| `/` | 2 | Floor division (integer) | `(/ 7 2)` → 3 |
| `neg` | 1 | Unary negation | `(neg 5)` → -5 |

## Key Design Decisions

1. **Prefix Notation**: All expressions must be in prefix (operator-first) notation within parentheses.
2. **Integer Arithmetic**: All operations work with 32-bit signed integers with Python's arbitrary precision.
3. **Floor Division**: The `/` operator performs floor division and returns an integer. For positive operands, `(/ 7 2)` yields `3`. For negative operands, floor division rounds toward negative infinity: `(/ -7 2)` yields `-4`. Division by zero raises `ZeroDivisionError`.
4. **Error Handling**: Any malformed input (unbalanced parens, invalid tokens, wrong operand count) raises `ValueError` with a descriptive message. Division by zero raises `ZeroDivisionError`.
5. **RPN Output**: Returns list of string tokens for compatibility with stack-based evaluation.
6. **Modular Design**: Implementation split across multiple modules (parser, evaluator, rpn) for clarity and maintainability.
