# exprkit — Progress Tracking

## Session 4 Status

### Completed ✓
- [x] Operator support: lt (less than comparison)
- [x] Operator support: gt (greater than comparison)
- [x] Operator support: eq (equality comparison)
- [x] Evaluator support for lt, gt, eq
- [x] RPN support for lt, gt, eq
- [x] All prior operators (+ - * / neg pow) still work in both evaluate and to_rpn
- [x] Updated SPEC.md with comparison operators
- [x] Updated ARCHITECTURE.md operator matrix
- [x] Updated ARCHITECTURE.md module descriptions
- [x] Updated HISTORY.md with design decisions
- [x] Both evaluate() and to_rpn() handle comparison operators

## Session 3 Status

### Completed ✓
- [x] Operator support: pow (binary exponentiation)
- [x] Evaluator support for pow
- [x] RPN support for pow
- [x] All prior operators (+ - * / neg) still work in both evaluate and to_rpn
- [x] Updated SPEC.md with pow operator
- [x] Updated ARCHITECTURE.md operator matrix
- [x] Updated HISTORY.md with design decisions
- [x] Both evaluate() and to_rpn() handle pow operator

## Session 2 Status

### Completed ✓
- [x] Operator support: neg (unary negation)
- [x] Evaluator support for neg
- [x] RPN support for neg
- [x] Refactored evaluator.py to support operators with different arities
- [x] Refactored rpn.py to support operators with different arities
- [x] All prior operators (+ - * /) still work in both evaluate and to_rpn
- [x] Updated SPEC.md with neg operator
- [x] Updated ARCHITECTURE.md operator matrix
- [x] Updated HISTORY.md with design decisions
- [x] Both evaluate() and to_rpn() handle neg operator

## Session 1 Status

### Completed ✓
- [x] Operator support: * (binary multiplication)
- [x] Operator support: / (binary floor division)
- [x] Evaluator support for * and /
- [x] RPN support for * and /
- [x] Floor division semantics: (/ 7 2) == 3, (/ -7 2) == -4
- [x] ZeroDivisionError handling for division by zero
- [x] Updated SPEC.md with new operators
- [x] Updated ARCHITECTURE.md operator matrix
- [x] Updated HISTORY.md with design decisions
- [x] Both evaluate() and to_rpn() handle new operators

## Session 0 Status

### Completed ✓
- [x] Package structure: exprkit/ with multiple modules
- [x] parser.py: Tokenization and AST construction
- [x] evaluator.py: Recursive AST evaluation
- [x] rpn.py: RPN conversion from AST
- [x] __init__.py: Public API (evaluate, to_rpn)
- [x] Operator support: + (binary addition)
- [x] Operator support: - (binary subtraction)
- [x] Error handling: ValueError for malformed input
- [x] SPEC.md: Public API and syntax documentation
- [x] ARCHITECTURE.md: Module layout and operator matrix
- [x] HISTORY.md: Change log
- [x] Whitespace handling in tokenizer
- [x] Nested expression support
- [x] Integer atom parsing (positive and negative)

### Session 0 Deliverables
- exprkit/__init__.py: Public API exports
- exprkit/parser.py: Parsing and AST construction
- exprkit/evaluator.py: Evaluation visitor
- exprkit/rpn.py: RPN conversion visitor
- SPEC.md: Specification document
- ARCHITECTURE.md: Architecture and operator matrix
- HISTORY.md: Append-only change log
- PROGRESS.md: This file

### Known Limitations (By Design)
- Binary operators only (arity = 2)
- No unary operators in this session
- No floating-point arithmetic
- No variable binding or scoping
- No function definitions beyond built-in operators

### Future Sessions
- Additional operators (*, /, %, etc.)
- Unary operators (-, abs, etc.)
- Extended arithmetic functions
- Floating-point support (if needed)
