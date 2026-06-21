# exprkit — Change History

## Session 4 (2026-06-21)

### Operators Added
- `lt` (binary less-than comparison)
- `gt` (binary greater-than comparison)
- `eq` (binary equality comparison)

### Key Decisions
1. **Comparison operator semantics**: The comparison operators (`lt`, `gt`, `eq`) each take exactly two arguments and return `1` for true and `0` for false. Examples: `(lt 3 4)` evaluates to `1`, `(gt 3 4)` evaluates to `0`, `(eq 4 4)` evaluates to `1`, `(eq (* 2 3) (+ 5 1))` evaluates to `1` (since 6 == 6).
2. **Operator registry extension**: Registered `lt`, `gt`, and `eq` with arity 2 in `operators.py` using Python's comparison operators (`<`, `>`, `==`) with boolean-to-integer conversion.
3. **Parser tokenization**: Added support for the named operators `lt`, `gt`, and `eq` in the tokenizer to recognize them as tokens.
4. **Visitor compatibility**: The generic evaluator and RPN converter already handle all operators via the operator registry and generic visitor methods, so no visitor changes were needed — both `evaluate` and `to_rpn` work automatically for comparison operators.

### Files Modified
- `exprkit/operators.py` — Registered `lt`, `gt`, and `eq` with arity 2 in `_register_builtins()`
- `exprkit/parser.py` — Added tokenization support for the named operators `lt`, `gt`, and `eq`
- `exprkit/__init__.py` — Updated docstrings in `evaluate()` and `to_rpn()` to document and exemplify the new comparison operators
- `SPEC.md` — Added `lt`, `gt`, `eq` to operator table; added examples for both `evaluate` and `to_rpn`
- `ARCHITECTURE.md` — Updated operator × visitor matrix to include comparison operators
- `HISTORY.md` — This session record
- `PROGRESS.md` — Updated task status

### Testing
- Implementation supports the specification examples:
  - `evaluate("(lt 3 4)") == 1` — less-than returns true
  - `evaluate("(gt 3 4)") == 0` — greater-than returns false
  - `evaluate("(eq 4 4)") == 1` — equality returns true
  - `evaluate("(eq (* 2 3) (+ 5 1))") == 1` — nested expressions work correctly
  - `to_rpn("(lt 3 4)") == ["3", "4", "lt"]` — RPN conversion works
  - All prior operators (`+`, `-`, `*`, `/`, `neg`, `pow`) still working in both `evaluate` and `to_rpn`

## Session 3 (2026-06-21)

### Operators Added
- `pow` (binary exponentiation)

### Key Decisions
1. **Binary exponentiation semantics**: The `pow` operator takes exactly two arguments and evaluates to the first raised to the power of the second. Examples: `(pow 2 5)` evaluates to `32`, `(pow (+ 1 1) (- 4 1))` evaluates to `8` (2^3).
2. **Operator registry extension**: Registered `pow` with arity 2 in `operators.py` using Python's `**` operator.
3. **Parser tokenization**: Added support for the named operator `pow` in the tokenizer to recognize it as a token.
4. **Visitor compatibility**: The generic evaluator and RPN converter already handle all operators via the operator registry and generic visitor methods, so no visitor changes were needed — both `evaluate` and `to_rpn` work automatically for `pow`.

### Files Modified
- `exprkit/operators.py` — Registered `pow` with arity 2 in `_register_builtins()`
- `exprkit/parser.py` — Added tokenization support for the named operator `pow`
- `exprkit/__init__.py` — Updated docstrings in `evaluate()` and `to_rpn()` to document and exemplify the new `pow` operator
- `SPEC.md` — Added `pow` to operator table; added examples for both `evaluate` and `to_rpn`
- `ARCHITECTURE.md` — Updated operator × visitor matrix to include `pow` operator
- `HISTORY.md` — This session record
- `PROGRESS.md` — Updated task status

### Testing
- Implementation tested against spec examples:
  - `evaluate("(pow 2 5)") == 32` ✓
  - `evaluate("(pow (+ 1 1) (- 4 1))") == 8` ✓
  - `to_rpn("(pow 2 3)") == ["2", "3", "pow"]` ✓
  - All prior operators (`+`, `-`, `*`, `/`, `neg`) still working in both `evaluate` and `to_rpn` ✓

## Session 2 (2026-06-21)

### Operators Added
- `neg` (unary negation)

### Key Decisions
1. **Unary operator semantics**: The `neg` operator takes exactly one argument and evaluates to its negation. Examples: `(neg 5)` evaluates to `-5`, `(neg (- 2 9))` evaluates to `7` (negation of `-7`).
2. **Operator registry extension**: Registered `neg` with arity 1 in `operators.py`.
3. **Parser tokenization**: Added support for the named operator `neg` in the tokenizer to recognize it as a token.
4. **Visitor compatibility**: The generic evaluator and RPN converter already handle all operators (unary and binary) via the operator registry and generic visitor methods, so no visitor changes were needed — both `evaluate` and `to_rpn` work automatically for `neg`.

### Files Modified
- `exprkit/operators.py` — Registered `neg` with arity 1 in `_register_builtins()`
- `exprkit/parser.py` — Added tokenization support for the named operator `neg`
- `exprkit/__init__.py` — Updated docstrings in `evaluate()` and `to_rpn()` to document and exemplify the new `neg` operator
- `SPEC.md` — Added `neg` to operator table; added examples for both `evaluate` and `to_rpn`
- `ARCHITECTURE.md` — Updated operator × visitor matrix to include `neg` operator
- `HISTORY.md` — This session record
- `PROGRESS.md` — Updated task status

### Testing
- Implementation tested against spec examples:
  - `evaluate("(neg 5)") == -5` ✓
  - `evaluate("(neg (- 2 9))") == 7` ✓
  - `to_rpn("(neg 5)") == ["5", "neg"]` ✓
  - `to_rpn("(neg (+ 1 2))") == ["1", "2", "+", "neg"]` ✓
  - All prior operators (`+`, `-`, `*`, `/`) still working in both `evaluate` and `to_rpn` ✓

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
