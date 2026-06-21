# Session 0 Handoff Notes

## Implementation Complete
Built exprkit package with prefix s-expression integer arithmetic support.

## Architecture
- `parser.py`: Tokenizes input and recursively parses prefix notation into an AST
  - Handles integer atoms (including negatives)
  - Validates operator count (minimum 2 arguments required)
  - Returns dict-based AST: `{'op': op, 'args': [ast...]}` for expressions, `{'type': 'num', 'value': int}` for atoms
  
- `evaluator.py`: Walks AST and computes results
  - Addition: sums all arguments
  - Subtraction: left-associative (arg0 - arg1 - arg2 - ...)
  
- `rpn.py`: Converts AST to postfix notation
  - Recursively processes arguments first, then appends operator
  - Returns list of string tokens
  
- `__init__.py`: Public API exports `evaluate(s)` and `to_rpn(s)`

## Supported Operators (Session 0)
- Binary `+` (addition)
- Binary `-` (subtraction, left-associative)

## Test Coverage (manual verification)
- `evaluate("(+ 3 4)") == 7` ✓
- `evaluate("(- (+ 1 2) 5)") == -2` ✓
- `to_rpn("(+ 3 4)") == ["3","4","+"]` ✓
- `to_rpn("(- 10 3)") == ["10","3","-"]` ✓
- Malformed input raises ValueError ✓

## Next Steps
Future sessions may extend with:
- Additional binary operators (*, /, %)
- Unary operators (-, abs, etc.)
- Nested expression depth optimization
- Full test suite
