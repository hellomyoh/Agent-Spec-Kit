# Session 2 Handoff Notes

## Implementation Complete
Extended exprkit package with unary `neg` operator for negation.

## Changes Made
- Updated `tokenizer()` in parser.py to recognize `neg` token
- Updated operator validation in parser.py to accept `neg` as unary operator (exactly 1 argument)
- Added negation handler in evaluator.py (returns `-results[0]`)
- RPN conversion works without modification (generic operator handling)

## Supported Operators (Session 2)
- Binary `+` (addition)
- Binary `-` (subtraction, left-associative)
- Binary `*` (multiplication, left-associative)
- Binary `/` (integer floor division, left-associative, raises ZeroDivisionError)
- Unary `neg` (negation, takes exactly 1 argument)

## Test Coverage
- `evaluate("(neg 5)") == -5` ✓
- `evaluate("(neg (- 2 9))") == 7` ✓
- `to_rpn("(neg (+ 1 2))") == ["1","2","+","neg"]` ✓
- All prior operators (+, -, *, /) continue to work in both evaluate and to_rpn ✓

## Next Steps
Future sessions may extend with:
- Additional unary operators (abs, etc.)
- Additional binary operators (%, **)
- Nested expression depth optimization
- Full test suite

---

# Session 1 Handoff Notes

## Implementation Complete
Extended exprkit package with multiplication and division operators.

## Changes Made
- Updated `tokenizer()` in parser.py to recognize `*` and `/` tokens
- Updated operator validation in parser.py to accept `*` and `/`
- Added multiplication handler in evaluator.py (left-associative: arg0 * arg1 * arg2 * ...)
- Added division handler in evaluator.py (left-associative integer floor division, raises ZeroDivisionError on division by zero)
- RPN conversion works without modification (generic operator handling)

## Supported Operators (Session 1)
- Binary `+` (addition)
- Binary `-` (subtraction, left-associative)
- Binary `*` (multiplication, left-associative)
- Binary `/` (integer floor division, left-associative, raises ZeroDivisionError)

## Test Coverage
- `evaluate("(* 6 7)") == 42` ✓
- `evaluate("(/ 7 2)") == 3` ✓
- `evaluate("(/ -7 2)") == -4` ✓
- `to_rpn("(* 6 7)") == ["6","7","*"]` ✓
- `to_rpn("(/ (* 6 4) (+ 1 2))") == ["6","4","*","1","2","+","/"]` ✓
- Division by zero raises ZeroDivisionError ✓
- All prior operators (+, -) continue to work in both evaluate and to_rpn ✓

## Next Steps
Future sessions may extend with:
- Additional unary operators (-, abs, etc.)
- Additional binary operators (%, **)
- Nested expression depth optimization
- Full test suite

---

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
