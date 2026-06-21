# exprkit — Architecture

## Module Layout

```
exprkit/
├── __init__.py          # Public API: evaluate(), to_rpn()
├── parser.py            # Tokenization & AST construction
├── evaluator.py         # AST evaluation to integer result
└── rpn.py               # AST conversion to RPN (postfix) format
```

## Module Responsibilities

### `parser.py`
- **Tokenize**: Convert input string into tokens (atoms, operators, parens)
- **Build AST**: Construct an abstract syntax tree (recursive, prefix-based)
- **Validate**: Check for malformed input (unbalanced parens, invalid tokens)
- **Exports**: `parse(s: str) -> ASTNode`

### `evaluator.py`
- **Evaluate AST**: Recursively compute the integer result
- **Operator Dispatch**: Handle `+` and `-` binary operations
- **Exports**: `evaluate_ast(ast: ASTNode) -> int`

### `rpn.py`
- **Convert to RPN**: Transform AST to postfix (Reverse Polish Notation)
- **Operator Dispatch**: Handle `+` and `-` in postfix context
- **Exports**: `ast_to_rpn(ast: ASTNode) -> list`

### `__init__.py`
- **Public API**: Expose `evaluate(s: str)` and `to_rpn(s: str)`
- **Orchestration**: Tie parser, evaluator, and rpn modules together

## Operator × Visitor Support Matrix

This matrix confirms that every supported operator is handled in both the `evaluate` (evaluator.py) and `to_rpn` (rpn.py) visitors.

| Operator | Arity | evaluate_ast | ast_to_rpn | Notes |
|----------|-------|--------------|-----------|-------|
| `+` | 2 | ✓ | ✓ | Binary addition; both visitors fully support |
| `-` | 2 | ✓ | ✓ | Binary subtraction; both visitors fully support |
| `*` | 2 | ✓ | ✓ | Binary multiplication; both visitors fully support |
| `/` | 2 | ✓ | ✓ | Floor division (integer); both visitors fully support; raises ZeroDivisionError on div by zero |
| `pow` | 2 | ✓ | ✓ | Exponentiation (power); both visitors fully support |
| `neg` | 1 | ✓ | ✓ | Unary negation; both visitors fully support |

**Legend:**
- ✓ = operator is implemented and tested
- Each row represents one operator
- Arity = number of arguments
- Both columns must have ✓ for an operator to be considered complete

**Update Procedure:**
Whenever a new operator (e.g., `*`, `/`, `%`) is added:
1. Update this matrix to add a new row
2. Implement the operator in `evaluator.py` (evaluate_ast function)
3. Implement the operator in `rpn.py` (ast_to_rpn function)
4. Add test cases in tests/ for both paths
5. Update HISTORY.md with the change

## Data Flow

### `evaluate(s: str) -> int`
```
Input: "(+ 3 4)"
  ↓ [parser.parse]
AST: Call("+", [Atom(3), Atom(4)])
  ↓ [evaluator.evaluate_ast]
Result: 7
```

### `to_rpn(s: str) -> list`
```
Input: "(+ 3 4)"
  ↓ [parser.parse]
AST: Call("+", [Atom(3), Atom(4)])
  ↓ [rpn.ast_to_rpn]
RPN: ["3", "4", "+"]
```

## AST Node Types

### `Atom`
- Represents a literal integer
- Fields: `value: int`

### `Call`
- Represents a function/operator call in prefix notation
- Fields: `op: str`, `args: list[ASTNode]`

## Error Handling Strategy

1. **Parser errors**: Syntax issues (unbalanced parens, invalid tokens)
2. **Evaluator errors**: Runtime issues (wrong arity, undefined operators)
3. **RPN errors**: Same as evaluator (same validation)

All errors raise `ValueError` with descriptive messages.
