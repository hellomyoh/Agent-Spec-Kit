# exprkit — Change History

## Session 1 (2026-06-21)

### Operators Added
- `*` (binary multiplication)
- `/` (binary integer floor division)

### Key Decisions
1. **Floor division semantics**: The `/` operator performs integer floor division (Python's `//`), returning an `int`. Examples: `(/ 7 2)` evaluates to `3`, `(/ -7 2)` evaluates to `-4` (floor of `-3.5`).
2. **Division by zero**: Raises `ZeroDivisionError` for clarity and consistency with Python's built-in behavior.
3. **Operator registry extension**: Both operators registered with arity 2 in `operators.py`.
4. **Visitor compatibility**: The generic evaluator and RPN converter already handle all binary operators via the operator registry, so no visitor changes were needed — both `evaluate` and `to_rpn` work automatically.

### Files Modified
- `exprkit/operators.py` — Registered `*` and `/` in `_register_builtins()`; added `_floor_divide()` helper method for integer division
- `exprkit/__init__.py` — Updated docstrings in `evaluate()` and `to_rpn()` to document new operators
- `SPEC.md` — Added `*` and `/` to operator table; added examples for both operators
- `ARCHITECTURE.md` — Updated operator × visitor matrix to include new operators
- `HISTORY.md` — This session record
- `PROGRESS.md` — Updated task status

### Testing
- Implementation tested against spec examples:
  - `evaluate("(* 6 7)") == 42` ✓
  - `evaluate("(/ 7 2)") == 3` ✓
  - `to_rpn("(* 6 7)") == ["6", "7", "*"]` ✓
  - `to_rpn("(/ (* 6 4) (+ 1 2))") == ["6", "4", "*", "1", "2", "+", "/"]` ✓
  - Floor division with negatives (e.g., `(/ -7 2)` == `-4`) ✓
  - All prior operators (`+`, `-`) still working in both `evaluate` and `to_rpn` ✓

## Session 0 (2026-06-21)

### Initial Build
- Created Python package `exprkit/` (standard library only)
- Implemented public API: `evaluate(s: str) -> int` and `to_rpn(s: str) -> list[str]`
- Modular architecture: parser, operators, evaluator, rpn_converter
- Support for prefix s-expression integer arithmetic

### Operators Implemented
- `+` (binary addition)
- `-` (binary subtraction)

### Key Decisions
1. **Modular design**: Separated parsing, evaluation, and RPN conversion into distinct modules for clarity and extensibility
2. **AST-based approach**: Built an intermediate AST representation to decouple parsing from evaluation/conversion
3. **Visitor pattern**: Implemented separate visitor classes for evaluation and RPN conversion to handle AST traversal
4. **Error handling**: All invalid inputs raise `ValueError` with descriptive messages
5. **Operator registry**: Centralized operator definitions for consistency and ease of adding new operators
6. **String tokens for RPN**: RPN output uses string tokens for consistency and ease of further processing

### Files Created
- `SPEC.md` — Public API specification and syntax
- `ARCHITECTURE.md` — Module layout and operator × visitor support matrix
- `HISTORY.md` — This file
- `PROGRESS.md` — Task completion status
- `exprkit/__init__.py` — Public API
- `exprkit/parser.py` — Tokenization and AST construction
- `exprkit/operators.py` — Operator registry and definitions
- `exprkit/evaluator.py` — AST evaluation visitor
- `exprkit/rpn_converter.py` — AST to RPN conversion visitor

### Testing
- Implementation tested against spec examples:
  - `evaluate("(+ 3 4)") == 7` ✓
  - `evaluate("(- (+ 1 2) 5)") == -2` ✓
  - `to_rpn("(+ 3 4)") == ["3", "4", "+"]` ✓
  - `to_rpn("(- 10 3)") == ["10", "3", "-"]` ✓
  - Nested expressions ✓
  - Error handling for malformed input ✓
