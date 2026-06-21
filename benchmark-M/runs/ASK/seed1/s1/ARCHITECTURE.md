# exprkit — Architecture

## Module Layout

```
exprkit/
├── __init__.py           # Public API: evaluate(), to_rpn()
├── parser.py             # Tokenization and AST construction
├── evaluator.py          # Evaluate AST to integer result
├── rpn_converter.py      # Convert AST to RPN (postfix) token list
└── operators.py          # Operator definitions and dispatch
```

### Module Responsibilities

#### `__init__.py`
- Exports `evaluate(s: str) -> int`
- Exports `to_rpn(s: str) -> list[str]`
- Orchestrates parser → evaluator/converter pipeline

#### `parser.py`
- Tokenizes input string (handles integers, operators, parentheses)
- Builds abstract syntax tree (AST) from tokens
- Validates structural correctness
- Raises `ValueError` for parse errors

#### `operators.py`
- Defines operator registry with metadata (name, arity)
- Provides function implementations for evaluation
- Maps operator symbols to their handlers

#### `evaluator.py`
- Implements AST visitor for evaluation
- Recursively computes integer results
- Applies operator semantics
- Raises `ValueError` for evaluation errors

#### `rpn_converter.py`
- Implements AST visitor for RPN conversion
- Traverses AST in postfix order
- Collects operands before operators
- Returns list of string tokens

## Operator × Visitor Support Matrix

The following matrix confirms that every supported operator is handled in both the evaluation visitor and the RPN converter visitor.

| Operator | Arity | Evaluator | RPN Converter | Notes |
|----------|-------|-----------|---------------|-------|
| `+` | 2 | ✓ | ✓ | Binary addition |
| `-` | 2 | ✓ | ✓ | Binary subtraction |
| `*` | 2 | ✓ | ✓ | Binary multiplication |
| `/` | 2 | ✓ | ✓ | Binary integer floor division |

**Legend:**
- ✓ = Implemented and tested
- This matrix must be updated whenever a new operator is added

## Design Principles

### Separation of Concerns
- Parsing, evaluation, and RPN conversion are independent
- Each visitor can be extended without affecting others
- Operators are centralized for consistency

### AST Representation
The parser builds an AST with two node types:

```python
class AtomNode:
    def __init__(self, value: int):
        self.value = value

class ExprNode:
    def __init__(self, op: str, args: list):
        self.op = op
        self.args = args  # list of AtomNode or ExprNode
```

### Visitor Pattern
Both evaluator and RPN converter follow the visitor pattern:
- Dispatch on node type (AtomNode or ExprNode)
- Recursively process child nodes
- Accumulate results or side effects

### Error Handling
- Parser validates syntax and arity
- Evaluator validates operator definitions and argument counts
- Both raise `ValueError` with context

## Extension Points

To add a new operator (future sessions):
1. Add entry to operator registry in `operators.py`
2. Implement evaluation logic in `evaluator.py` (handle_<op> method)
3. Implement RPN logic in `rpn_converter.py` (handle_<op> method or generic handler)
4. Update the Operator × Visitor Support Matrix above
5. Add test cases for both `evaluate` and `to_rpn`
