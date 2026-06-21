def parse(s: str):
    """Parse a prefix s-expression string into an AST.

    Returns:
        A nested structure: either an int (atom) or a tuple (op, arg1, arg2, ...)

    Raises:
        ValueError: If the input is malformed.
    """
    s = s.strip()
    if not s:
        raise ValueError("Empty expression")

    tokens = tokenize(s)
    ast, pos = parse_expr(tokens, 0)

    if pos != len(tokens):
        raise ValueError("Extra tokens after expression")

    return ast


def tokenize(s: str):
    """Tokenize a prefix s-expression string."""
    tokens = []
    i = 0
    while i < len(s):
        if s[i].isspace():
            i += 1
        elif s[i] in '()':
            tokens.append(s[i])
            i += 1
        elif s[i:i+3] == 'neg' and (i+3 >= len(s) or s[i+3].isspace() or s[i+3] in '()'):
            # Keyword operator 'neg'
            tokens.append('neg')
            i += 3
        elif s[i:i+3] == 'pow' and (i+3 >= len(s) or s[i+3].isspace() or s[i+3] in '()'):
            # Keyword operator 'pow'
            tokens.append('pow')
            i += 3
        elif s[i] in '+-' and (i + 1 < len(s) and s[i + 1].isdigit()):
            # Negative or positive number
            j = i + 1
            while j < len(s) and s[j].isdigit():
                j += 1
            tokens.append(s[i:j])
            i = j
        elif s[i].isdigit():
            # Positive number
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            tokens.append(s[i:j])
            i = j
        elif s[i] in '+-*/':
            # Operator
            tokens.append(s[i])
            i += 1
        else:
            raise ValueError(f"Unexpected character: {s[i]}")

    return tokens


def parse_expr(tokens, pos):
    """Parse a single expression starting at position pos.

    Returns:
        (ast, new_pos)
    """
    if pos >= len(tokens):
        raise ValueError("Unexpected end of expression")

    token = tokens[pos]

    if token == '(':
        # Prefix form: (OP ARG ...)
        pos += 1
        if pos >= len(tokens):
            raise ValueError("Expected operator after '('")

        op = tokens[pos]
        if op not in ['+', '-', '*', '/', 'neg', 'pow']:
            raise ValueError(f"Unknown operator: {op}")

        pos += 1
        args = []

        while pos < len(tokens) and tokens[pos] != ')':
            arg, pos = parse_expr(tokens, pos)
            args.append(arg)

        if pos >= len(tokens):
            raise ValueError("Expected ')'")

        pos += 1
        return (op, *args), pos

    elif token in '+-*/':
        raise ValueError(f"Unexpected operator: {token}")

    else:
        # Atom (integer)
        try:
            value = int(token)
            return value, pos + 1
        except ValueError:
            raise ValueError(f"Invalid integer: {token}")
