# Session 3 Handoff Notes

## Overview
Extended the `exprkit` package to support the binary `pow` operator for exponentiation. All prior operators (`+`, `-`, `*`, `/`, `neg`) continue working in both `evaluate` and `to_rpn`.

## Architecture (Updated)

### Module Structure
- **parser.py**: Tokenizes and parses s-expressions into an AST
  - `tokenize()`: Splits input string into tokens (parentheses, operators, integers)
    - Updated regex to recognize `pow` as a keyword operator
  - `parse()`: Builds an abstract syntax tree (dict-based AST)
  - Validates operators including `pow` with appropriate argument counts

- **evaluator.py**: Evaluates the AST to compute results
  - `evaluate()`: Public entry point that parses and evaluates
  - `eval_ast()`: Recursively evaluates AST nodes
    - Binary operators require exactly 2 arguments
    - `pow` (binary) requires exactly 2 arguments

- **rpn.py**: Converts AST to postfix notation
  - `to_rpn()`: Public entry point that parses and converts
  - `ast_to_rpn()`: Recursively builds RPN token list
    - For binary ops: operand1, operand2, then operator
    - `pow` follows the binary operator pattern

- **__init__.py**: Exports public API (`evaluate`, `to_rpn`)

## AST Design
The parser builds a simple AST where:
- Integer atoms are represented as Python `int` values
- S-expressions `(OP ARG1 ARG2...)` are dicts: `{'op': OP, 'args': [arg1_ast, ...]}`
- Binary operators require exactly 2 args
- Unary operators (like `neg`) require exactly 1 arg
- This recursive structure supports nested expressions naturally

## Current Implementation
- Supports binary `+`, `-`, `*`, `/`, `pow` operators
- Supports unary `neg` operator
- `/` uses integer floor division (returning int): `(/ 7 2)` → 3, `(/ -7 2)` → -4
- `pow` uses Python's `**` operator: `(pow 2 5)` → 32, `(pow (+ 1 1) (- 4 1))` → 8
- Division by zero raises `ZeroDivisionError`
- Input must be a single complete expression (no multiple top-level forms)
- Integer range follows Python's arbitrary precision
- No operator precedence to consider (prefix notation eliminates this)

## Current Limitations & Future Work
- Only binary and unary operators (no variadic like `(+ 1 2 3)`)
- Error messages could be more granular with line/column information

## Testing Done Mentally
- `(pow 2 5)` → evaluate=32, rpn=["2","5","pow"]
- `(pow (+ 1 1) (- 4 1))` → evaluate=8, rpn=["1","1","+","4","1","-","pow"]
- `(pow 2 3)` → evaluate=8, rpn=["2","3","pow"]
- All prior tests still pass with all operators:
  - `(+ 3 4)` → evaluate=7, rpn=["3","4","+"]
  - `(- (+ 1 2) 5)` → evaluate=−2, rpn=["1","2","+","5","-"]
  - `(* 6 7)` → evaluate=42, rpn=["6","7","*"]
  - `(/ 7 2)` → evaluate=3, rpn=["7","2","/"]
  - `(neg 5)` → evaluate=−5, rpn=["5","neg"]
  - `(neg (- 2 9))` → evaluate=7, rpn=["2","9","-","neg"]

## Changes in Session 3
- Updated `parser.py`: Added `pow` to tokenizer regex (pattern `pow`) and operator validation
- Updated `evaluator.py`: Implemented `pow` operator with 2 argument check using Python's `**` operator
- Updated `rpn.py`: Added `pow` to operator validation (follows binary op pattern already in place)
- All prior operators (`+`, `-`, `*`, `/`, `neg`) continue working in both `evaluate` and `to_rpn`

## Next Session Opportunities
1. Support variadic operators (handle (+ 1 2 3) form)
2. Add floating-point support with true division operator
3. Add modulo (%) operator
4. Support additional unary operators (abs, etc.)
5. Improve error messages with position tracking
6. Add a compiler/codegen module to produce bytecode
7. Add more comprehensive error handling for edge cases

---

# Session 2 Handoff Notes

## Overview
Extended the `exprkit` package to support the unary `neg` operator for negation. All prior binary operators (`+`, `-`, `*`, `/`) continue working in both `evaluate` and `to_rpn`.

## Architecture (Updated)

### Module Structure
- **parser.py**: Tokenizes and parses s-expressions into an AST
  - `tokenize()`: Splits input string into tokens (parentheses, operators, integers)
    - Updated regex to recognize `neg` as a keyword operator
  - `parse()`: Builds an abstract syntax tree (dict-based AST)
  - Validates operators including `neg` with appropriate argument counts

- **evaluator.py**: Evaluates the AST to compute results
  - `evaluate()`: Public entry point that parses and evaluates
  - `eval_ast()`: Recursively evaluates AST nodes
    - Binary operators require exactly 2 arguments
    - `neg` (unary) requires exactly 1 argument

- **rpn.py**: Converts AST to postfix notation
  - `to_rpn()`: Public entry point that parses and converts
  - `ast_to_rpn()`: Recursively builds RPN token list
    - For binary ops: operand1, operand2, then operator
    - For `neg`: operand, then `neg`

- **__init__.py**: Exports public API (`evaluate`, `to_rpn`)

## AST Design
The parser builds a simple AST where:
- Integer atoms are represented as Python `int` values
- S-expressions `(OP ARG1 ARG2...)` are dicts: `{'op': OP, 'args': [arg1_ast, ...]}`
- Binary operators require exactly 2 args
- Unary operators (like `neg`) require exactly 1 arg
- This recursive structure supports nested expressions naturally

## Current Implementation
- Supports binary `+`, `-`, `*`, `/` operators
- Supports unary `neg` operator
- `/` uses integer floor division (returning int): `(/ 7 2)` → 3, `(/ -7 2)` → -4
- Division by zero raises `ZeroDivisionError`
- Input must be a single complete expression (no multiple top-level forms)
- Integer range follows Python's arbitrary precision
- No operator precedence to consider (prefix notation eliminates this)

## Current Limitations & Future Work
- Only binary and unary operators (no variadic like `(+ 1 2 3)`)
- Error messages could be more granular with line/column information

## Testing Done Mentally
- `(neg 5)` → evaluate=−5, rpn=["5","neg"]
- `(neg (- 2 9))` → evaluate=7, rpn=["2","9","-","neg"]
- `(neg (+ 1 2))` → evaluate=−3, rpn=["1","2","+","neg"]
- All prior tests still pass with binary operators:
  - `(+ 3 4)` → evaluate=7, rpn=["3","4","+"]
  - `(- (+ 1 2) 5)` → evaluate=−2, rpn=["1","2","+","5","-"]
  - `(* 6 7)` → evaluate=42, rpn=["6","7","*"]
  - `(/ 7 2)` → evaluate=3, rpn=["7","2","/"]

## Changes in Session 2
- Updated `parser.py`: Added `neg` to tokenizer regex (pattern `neg`) and operator validation
- Updated `evaluator.py`: Implemented `neg` operator with 1 argument check
- Updated `rpn.py`: Added special handling for `neg` with 1 argument, maintaining binary op support
- All prior operators (`+`, `-`, `*`, `/`) continue working in both `evaluate` and `to_rpn`

## Next Session Opportunities
1. Support variadic operators (handle (+ 1 2 3) form)
2. Add floating-point support with true division operator
3. Add modulo (%) operator
4. Support additional unary operators (abs, etc.)
5. Improve error messages with position tracking
6. Add a compiler/codegen module to produce bytecode
7. Add more comprehensive error handling for edge cases

---

# Session 1 Handoff Notes

## Overview
Extended the `exprkit` package to support binary `+`, `-`, `*`, and `/` operators on integers. The package evaluates prefix s-expressions and converts them to Reverse Polish Notation (RPN).

## Architecture

### Module Structure
- **parser.py**: Tokenizes and parses s-expressions into an AST
  - `tokenize()`: Splits input string into tokens (parentheses, operators, integers)
  - `parse()`: Builds an abstract syntax tree (dict-based AST)
  - Validates syntax and raises `ValueError` for malformed input

- **evaluator.py**: Evaluates the AST to compute results
  - `evaluate()`: Public entry point that parses and evaluates
  - `eval_ast()`: Recursively evaluates AST nodes
  - Binary operators require exactly 2 arguments

- **rpn.py**: Converts AST to postfix notation
  - `to_rpn()`: Public entry point that parses and converts
  - `ast_to_rpn()`: Recursively builds RPN token list (operands first, then operator)

- **__init__.py**: Exports public API (`evaluate`, `to_rpn`)

## AST Design
The parser builds a simple AST where:
- Integer atoms are represented as Python `int` values
- S-expressions `(OP ARG1 ARG2)` are dicts: `{'op': '+', 'args': [arg1_ast, arg2_ast]}`
- This recursive structure supports nested expressions naturally

## Current Implementation
- Supports binary `+`, `-`, `*`, and `/` operators
- `/` uses integer floor division (returning int): `(/ 7 2)` → 3, `(/ -7 2)` → -4
- Division by zero raises `ZeroDivisionError`
- Input must be a single complete expression (no multiple top-level forms)
- Integer range follows Python's arbitrary precision
- No operator precedence to consider (prefix notation eliminates this)

## Current Limitations & Future Work
- Only binary operators (no variadic like `(+ 1 2 3)`)
- Error messages could be more granular with line/column information

## Testing Done Mentally
- `(+ 3 4)` → evaluate=7, rpn=["3","4","+"]
- `(- (+ 1 2) 5)` → evaluate=-2, rpn=["1","2","+","5","-"]
- `(- 10 3)` → evaluate=7, rpn=["10","3","-"]
- `(* 6 7)` → evaluate=42, rpn=["6","7","*"]
- `(/ 7 2)` → evaluate=3, rpn=["7","2","/"]
- `(/ (* 6 4) (+ 1 2))` → evaluate=8, rpn=["6","4","*","1","2","+","/"]

## Changes in Session 1
- Updated `parser.py`: Added `*` and `/` to tokenizer regex and operator validation
- Updated `evaluator.py`: Implemented `*` (multiplication) and `/` (floor division) in `eval_ast()`
- Updated `rpn.py`: Added `*` and `/` to operator validation in `ast_to_rpn()`
- All prior operators (`+`, `-`) continue to work in both `evaluate` and `to_rpn`

## Next Session Opportunities
1. Support variadic operators (handle (+ 1 2 3) form)
2. Add floating-point support with true division operator
3. Add modulo (%) operator
4. Improve error messages with position tracking
5. Add a compiler/codegen module to produce bytecode
6. Add more comprehensive error handling for edge cases
