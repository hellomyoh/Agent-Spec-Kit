"""
Tokenization and AST construction.
"""

from .operators import get_registry


class AtomNode:
    """AST node for an integer atom."""

    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return f"AtomNode({self.value})"


class ExprNode:
    """AST node for a prefix expression (op arg1 arg2 ...)."""

    def __init__(self, op, args):
        self.op = op
        self.args = args

    def __repr__(self):
        return f"ExprNode({self.op}, {self.args})"


def tokenize(s):
    """Tokenize input string into atoms, operators, and parentheses.

    Returns a list of tokens.
    Raises ValueError for invalid tokens.
    """
    tokens = []
    i = 0
    s = s.strip()

    while i < len(s):
        if s[i].isspace():
            i += 1
        elif s[i] == '(':
            tokens.append('(')
            i += 1
        elif s[i] == ')':
            tokens.append(')')
            i += 1
        elif s[i] in '+-' and (i + 1 < len(s) and s[i + 1].isdigit()):
            # Negative number
            j = i + 1
            while j < len(s) and s[j].isdigit():
                j += 1
            tokens.append(s[i:j])
            i = j
        elif s[i].isdigit():
            # Positive integer
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            tokens.append(s[i:j])
            i = j
        elif s[i] in '+-*/%':
            # Operator (support future operators)
            tokens.append(s[i])
            i += 1
        elif s[i:i+3] == 'neg' and (i + 3 >= len(s) or not s[i+3].isalnum()):
            # Named operator 'neg'
            tokens.append('neg')
            i += 3
        elif s[i:i+3] == 'pow' and (i + 3 >= len(s) or not s[i+3].isalnum()):
            # Named operator 'pow'
            tokens.append('pow')
            i += 3
        elif s[i:i+2] == 'lt' and (i + 2 >= len(s) or not s[i+2].isalnum()):
            # Named operator 'lt'
            tokens.append('lt')
            i += 2
        elif s[i:i+2] == 'gt' and (i + 2 >= len(s) or not s[i+2].isalnum()):
            # Named operator 'gt'
            tokens.append('gt')
            i += 2
        elif s[i:i+2] == 'eq' and (i + 2 >= len(s) or not s[i+2].isalnum()):
            # Named operator 'eq'
            tokens.append('eq')
            i += 2
        else:
            raise ValueError(f"Invalid character: {s[i]}")

    return tokens


def parse(s):
    """Parse a tokenized input into an AST.

    Returns the root AST node.
    Raises ValueError for syntax errors.
    """
    tokens = tokenize(s)
    registry = get_registry()

    pos = [0]  # Use list to allow modification in nested function

    def parse_expr():
        if pos[0] >= len(tokens):
            raise ValueError("Unexpected end of input")

        token = tokens[pos[0]]

        if token == '(':
            pos[0] += 1
            if pos[0] >= len(tokens):
                raise ValueError("Unexpected end after '('")

            op_token = tokens[pos[0]]
            if not registry.is_operator(op_token):
                raise ValueError(f"Unknown operator: {op_token}")

            op = op_token
            pos[0] += 1

            args = []
            while pos[0] < len(tokens) and tokens[pos[0]] != ')':
                args.append(parse_expr())

            if pos[0] >= len(tokens):
                raise ValueError("Unclosed expression")

            pos[0] += 1  # Skip ')'

            # Validate arity
            expected_arity = registry.get_arity(op)
            if len(args) != expected_arity:
                raise ValueError(
                    f"Operator {op} expects {expected_arity} arguments, "
                    f"got {len(args)}"
                )

            return ExprNode(op, args)

        elif token.lstrip('-').isdigit():
            # Integer atom
            pos[0] += 1
            return AtomNode(token)

        elif token == ')':
            raise ValueError("Unexpected ')'")

        else:
            raise ValueError(f"Invalid token: {token}")

    ast = parse_expr()

    if pos[0] < len(tokens):
        raise ValueError("Extra tokens after expression")

    return ast
