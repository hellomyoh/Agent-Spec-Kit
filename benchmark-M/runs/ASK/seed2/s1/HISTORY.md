# exprkit — Change History

## Session 1 (Multiplication and Floor Division) — 2026-06-21

### Added
- **Operators**: `*` (binary multiplication) and `/` (binary floor division)
- **Floor division semantics**: `/` returns integer result using floor division (rounds toward negative infinity)
  - Examples: `(/ 7 2)` → `3`, `(/ -7 2)` → `-4`
  - Division by zero raises `ZeroDivisionError`
- **Evaluator support**: Both new operators implemented in `evaluator.py` with proper dispatch
- **RPN support**: Both new operators supported in `rpn.py` for postfix conversion
- **Documentation**: Updated SPEC.md, ARCHITECTURE.md, and PROGRESS.md

### Design Decisions
- **Floor Division**: `/` operator uses Python's `//` operator internally but ensures integer result via explicit cast. This provides consistent behavior with negative operands across all platforms.
- **Error Handling**: Division by zero raises `ZeroDivisionError` (not caught as generic ValueError), allowing callers to distinguish arithmetic errors from syntax/parsing errors.

### Examples
```python
from exprkit import evaluate, to_rpn

evaluate("(* 6 7)")                    # 42
evaluate("(/ 7 2)")                    # 3
evaluate("(/ -7 2)")                   # -4
to_rpn("(* 6 7)")                      # ["6", "7", "*"]
to_rpn("(/ (* 6 4) (+ 1 2))")          # ["6", "4", "*", "1", "2", "+", "/"]
```

## Session 0 (Initial Build) — 2026-06-21

### Added
- **Core package structure**: exprkit/ with parser, evaluator, rpn modules
- **Public API**: `evaluate(s: str) -> int` and `to_rpn(s: str) -> list`
- **Parser**: Tokenization and AST construction for prefix s-expressions
- **Evaluator**: Recursive AST evaluation with operator dispatch
- **RPN converter**: AST to postfix notation conversion
- **Operators supported**: `+` (binary addition), `-` (binary subtraction)
- **Error handling**: ValueError for malformed input
- **Documentation**: SPEC.md, ARCHITECTURE.md, PROGRESS.md
- **Operator × Visitor matrix**: Tracking coverage of operators in evaluate and to_rpn

### Features
- Integer atoms (positive and negative)
- Prefix s-expression syntax
- Nested expressions
- Whitespace handling
- Comprehensive error messages

### Example Usage
```python
from exprkit import evaluate, to_rpn

evaluate("(+ 3 4)")                # 7
evaluate("(- (+ 1 2) 5)")          # -2
to_rpn("(+ 3 4)")                  # ["3", "4", "+"]
```
