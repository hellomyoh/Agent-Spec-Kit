# exprkit — Progress Report

## Session 4 Status: COMPLETE

### Completed Tasks

- [x] Added `lt` (binary less-than comparison) operator
  - [x] Registered in operator registry with arity 2
  - [x] Added tokenization support in parser for named operator `lt`
  - [x] Evaluator support (generic visitor, no changes needed)
  - [x] RPN converter support (generic visitor, no changes needed)
- [x] Added `gt` (binary greater-than comparison) operator
  - [x] Registered in operator registry with arity 2
  - [x] Added tokenization support in parser for named operator `gt`
  - [x] Evaluator support (generic visitor, no changes needed)
  - [x] RPN converter support (generic visitor, no changes needed)
- [x] Added `eq` (binary equality comparison) operator
  - [x] Registered in operator registry with arity 2
  - [x] Added tokenization support in parser for named operator `eq`
  - [x] Evaluator support (generic visitor, no changes needed)
  - [x] RPN converter support (generic visitor, no changes needed)
- [x] Updated SPEC.md
  - [x] Added `lt`, `gt`, `eq` to operator table
  - [x] Added examples for both `evaluate` and `to_rpn`
- [x] Updated ARCHITECTURE.md
  - [x] Updated operator × visitor matrix for comparison operators
- [x] Updated HISTORY.md
  - [x] Recorded new operators and design decisions
  - [x] Documented test results
- [x] Updated PROGRESS.md

### Tested Examples

All specification examples pass:
- ✓ `evaluate("(lt 3 4)") == 1`
- ✓ `evaluate("(gt 3 4)") == 0`
- ✓ `evaluate("(eq 4 4)") == 1`
- ✓ `evaluate("(eq (* 2 3) (+ 5 1))") == 1`
- ✓ `to_rpn("(lt 3 4)") == ["3", "4", "lt"]`
- ✓ Prior operators (`+`, `-`, `*`, `/`, `neg`, `pow`) still working in both `evaluate` and `to_rpn`

## Session 3 Status: COMPLETE

### Completed Tasks

- [x] Added `pow` (binary exponentiation) operator
  - [x] Registered in operator registry with arity 2
  - [x] Added tokenization support in parser for named operator `pow`
  - [x] Evaluator support (generic visitor, no changes needed)
  - [x] RPN converter support (generic visitor, no changes needed)
- [x] Updated SPEC.md
  - [x] Added `pow` to operator table
  - [x] Added examples for both `evaluate` and `to_rpn`
- [x] Updated ARCHITECTURE.md
  - [x] Updated operator × visitor matrix for `pow`
- [x] Updated HISTORY.md
  - [x] Recorded new operator and design decisions
  - [x] Documented test results
- [x] Updated PROGRESS.md

### Tested Examples

All specification examples pass:
- ✓ `evaluate("(pow 2 5)") == 32`
- ✓ `evaluate("(pow (+ 1 1) (- 4 1))") == 8`
- ✓ `to_rpn("(pow 2 3)") == ["2", "3", "pow"]`
- ✓ Prior operators (`+`, `-`, `*`, `/`, `neg`) still working in both `evaluate` and `to_rpn`

## Session 2 Status: COMPLETE

### Completed Tasks

- [x] Added `neg` (unary negation) operator
  - [x] Registered in operator registry with arity 1
  - [x] Added tokenization support in parser for named operator `neg`
  - [x] Evaluator support (generic visitor, no changes needed)
  - [x] RPN converter support (generic visitor, no changes needed)
- [x] Updated SPEC.md
  - [x] Added `neg` to operator table
  - [x] Added examples for both `evaluate` and `to_rpn`
- [x] Updated ARCHITECTURE.md
  - [x] Updated operator × visitor matrix for `neg`
- [x] Updated HISTORY.md
  - [x] Recorded new operator and design decisions
  - [x] Documented test results
- [x] Updated PROGRESS.md

### Tested Examples

All specification examples pass:
- ✓ `evaluate("(neg 5)") == -5`
- ✓ `evaluate("(neg (- 2 9))") == 7`
- ✓ `to_rpn("(neg 5)") == ["5", "neg"]`
- ✓ `to_rpn("(neg (+ 1 2))") == ["1", "2", "+", "neg"]`
- ✓ Prior operators (`+`, `-`, `*`, `/`) still working in both `evaluate` and `to_rpn`

## Session 1 Status: COMPLETE

### Completed Tasks

- [x] Added `*` (multiplication) operator
  - [x] Registered in operator registry
  - [x] Evaluator support (generic visitor)
  - [x] RPN converter support (generic visitor)
- [x] Added `/` (integer floor division) operator
  - [x] Registered in operator registry
  - [x] Implemented `_floor_divide()` method with ZeroDivisionError handling
  - [x] Evaluator support (generic visitor)
  - [x] RPN converter support (generic visitor)
- [x] Updated SPEC.md
  - [x] Added `*` and `/` to operator table
  - [x] Added examples for both operators and nested expressions
  - [x] Documented division by zero error
- [x] Updated ARCHITECTURE.md
  - [x] Updated operator × visitor matrix for `*` and `/`
- [x] Updated HISTORY.md
  - [x] Recorded new operators and design decisions
  - [x] Floor division design decision documented
- [x] Updated PROGRESS.md

### Tested Examples

All specification examples pass:
- ✓ `evaluate("(* 6 7)") == 42`
- ✓ `evaluate("(/ 7 2)") == 3`
- ✓ `evaluate("(/ -7 2)") == -4` (floor division)
- ✓ `to_rpn("(* 6 7)") == ["6", "7", "*"]`
- ✓ `to_rpn("(/ (* 6 4) (+ 1 2))") == ["6", "4", "*", "1", "2", "+", "/"]`
- ✓ Prior operators (`+`, `-`) still working
- ✓ Error handling for division by zero

## Session 0 Status: COMPLETE

### Completed Tasks

- [x] Created package structure (`exprkit/`)
- [x] Implemented parser module
  - [x] Tokenization
  - [x] AST construction
  - [x] Syntax validation
- [x] Implemented operators module
  - [x] Operator registry
  - [x] Binary `+` definition
  - [x] Binary `-` definition
- [x] Implemented evaluator module
  - [x] AST visitor for evaluation
  - [x] Operator dispatch
  - [x] Error handling
- [x] Implemented RPN converter module
  - [x] AST visitor for postfix conversion
  - [x] Token collection
  - [x] Error handling
- [x] Created public API in `exprkit/__init__.py`
  - [x] `evaluate(s: str) -> int`
  - [x] `to_rpn(s: str) -> list[str]`
- [x] Created documentation
  - [x] SPEC.md
  - [x] ARCHITECTURE.md
  - [x] HISTORY.md
  - [x] PROGRESS.md

### Tested Examples

All specification examples pass:
- ✓ `evaluate("(+ 3 4)") == 7`
- ✓ `evaluate("(- (+ 1 2) 5)") == -2`
- ✓ `to_rpn("(+ 3 4)") == ["3", "4", "+"]`
- ✓ `to_rpn("(- 10 3)") == ["10", "3", "-"]`
- ✓ Nested expressions
- ✓ Negative integers
- ✓ Error handling for malformed input

### Remaining Work

None for Session 0. The specification is complete.

Future sessions may extend with:
- Additional operators (`*`, `/`, `%`, unary operators, etc.)
- Advanced features (variable substitution, functions, etc.)
- Optimization passes
- Extended error reporting
