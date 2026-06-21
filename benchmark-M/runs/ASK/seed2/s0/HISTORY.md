# exprkit — Change History

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
