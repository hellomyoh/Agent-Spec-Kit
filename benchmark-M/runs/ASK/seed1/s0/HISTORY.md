# exprkit — Change History

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
