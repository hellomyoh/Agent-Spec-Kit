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
| `*` | 2 | Binary multiplication: `(* a b)` |
| `/` | 2 | Binary floor division: `(/ a b)` (integer division returning int) |
| `neg` | 1 | Unary negation: `(neg a)` (evaluates to `-a`) |
| `pow` | 2 | Binary exponentiation: `(pow a b)` (evaluates to `a ** b`) |
| `lt` | 2 | Binary less-than comparison: `(lt a b)` (returns 1 if true, 0 if false) |
| `gt` | 2 | Binary greater-than comparison: `(gt a b)` (returns 1 if true, 0 if false) |
| `eq` | 2 | Binary equality comparison: `(eq a b)` (returns 1 if true, 0 if false) |

## Examples

### Evaluation
```
evaluate("(+ 3 4)") == 7
evaluate("(* 6 7)") == 42
evaluate("(/ 7 2)") == 3
evaluate("(- (+ 1 2) 5)") == -2
evaluate("(- 10 3)") == 7
evaluate("(neg 5)") == -5
evaluate("(neg (- 2 9))") == 7
evaluate("(pow 2 5)") == 32
evaluate("(pow (+ 1 1) (- 4 1))") == 8
evaluate("(lt 3 4)") == 1
evaluate("(gt 3 4)") == 0
evaluate("(eq 4 4)") == 1
evaluate("(eq (* 2 3) (+ 5 1))") == 1
```

### RPN Conversion
```
to_rpn("(+ 3 4)") == ["3", "4", "+"]
to_rpn("(* 6 7)") == ["6", "7", "*"]
to_rpn("(/ (* 6 4) (+ 1 2))") == ["6", "4", "*", "1", "2", "+", "/"]
to_rpn("(- 10 3)") == ["10", "3", "-"]
to_rpn("(- (+ 1 2) 5)") == ["1", "2", "+", "5", "-"]
to_rpn("(neg 5)") == ["5", "neg"]
to_rpn("(neg (+ 1 2))") == ["1", "2", "+", "neg"]
to_rpn("(pow 2 3)") == ["2", "3", "pow"]
to_rpn("(lt 3 4)") == ["3", "4", "lt"]
to_rpn("(eq (* 2 3) (+ 5 1))") == ["2", "3", "*", "5", "1", "+", "eq"]
```

## Error Handling

All invalid inputs raise `ValueError` with a descriptive message:
- Mismatched parentheses
- Invalid tokens
- Operators with incorrect number of arguments
- Empty expressions
- Undefined operators

Division by zero raises `ZeroDivisionError`.

## Design Decisions

1. **Module separation**: Parser, evaluator, and RPN converter are separate modules for clarity and testability.
2. **Prefix notation**: S-expressions naturally encode prefix notation, simplifying both parsing and evaluation.
3. **Type consistency**: All results and intermediate values are Python `int` (no float coercion).
4. **String tokens in RPN**: RPN output uses string tokens for consistency and ease of further processing.
5. **Error-first validation**: Parse errors are caught early before evaluation.
