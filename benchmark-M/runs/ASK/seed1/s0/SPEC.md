# exprkit — Specification

## Public API

Located in `exprkit/__init__.py`:

```python
def evaluate(s: str) -> int
def to_rpn(s: str) -> list[str]
```

### `evaluate(s: str) -> int`
Parses and evaluates a prefix s-expression containing integer arithmetic operations.
Returns the computed integer result.
Raises `ValueError` for malformed input.

### `to_rpn(s: str) -> list[str]`
Parses a prefix s-expression and returns a list of string tokens in postfix (Reverse Polish Notation) order.
The result is a sequence of operands followed by operators.
Raises `ValueError` for malformed input.

## Syntax

### Integer Atoms
- Decimal integers: `42`, `-3`, `0`
- No float literals or other types

### Prefix Forms
- Expression format: `(OP ARG ...)`
- Operators appear first inside parentheses
- Arguments follow the operator
- Arguments may be atoms or nested expressions

## Supported Operators (This Session)

| Operator | Arity | Description |
|----------|-------|-------------|
| `+` | 2 | Binary addition: `(+ a b)` |
| `-` | 2 | Binary subtraction: `(- a b)` (evaluates to `a - b`) |

## Examples

### Evaluation
```
evaluate("(+ 3 4)") == 7
evaluate("(- (+ 1 2) 5)") == -2
evaluate("(- 10 3)") == 7
```

### RPN Conversion
```
to_rpn("(+ 3 4)") == ["3", "4", "+"]
to_rpn("(- 10 3)") == ["10", "3", "-"]
to_rpn("(- (+ 1 2) 5)") == ["1", "2", "+", "5", "-"]
```

## Error Handling

All invalid inputs raise `ValueError` with a descriptive message:
- Mismatched parentheses
- Invalid tokens
- Operators with incorrect number of arguments
- Empty expressions
- Undefined operators

## Design Decisions

1. **Module separation**: Parser, evaluator, and RPN converter are separate modules for clarity and testability.
2. **Prefix notation**: S-expressions naturally encode prefix notation, simplifying both parsing and evaluation.
3. **Type consistency**: All results and intermediate values are Python `int` (no float coercion).
4. **String tokens in RPN**: RPN output uses string tokens for consistency and ease of further processing.
5. **Error-first validation**: Parse errors are caught early before evaluation.
