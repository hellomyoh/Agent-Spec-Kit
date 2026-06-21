"""Tokenizer and parser for s-expression syntax."""


def tokenize(s):
    """Tokenize input string into a list of tokens.

    Args:
        s: Input string

    Returns:
        List of string tokens

    Raises:
        ValueError: If input is malformed
    """
    tokens = []
    current = ""
    i = 0

    while i < len(s):
        char = s[i]

        if char.isspace():
            if current:
                tokens.append(current)
                current = ""
            i += 1
        elif char == '(':
            if current:
                tokens.append(current)
                current = ""
            tokens.append('(')
            i += 1
        elif char == ')':
            if current:
                tokens.append(current)
                current = ""
            tokens.append(')')
            i += 1
        else:
            current += char
            i += 1

    if current:
        tokens.append(current)

    return tokens


def parse(tokens):
    """Parse tokens into an expression tree.

    Args:
        tokens: List of tokens from tokenize()

    Returns:
        Expression tree (nested lists/strings)

    Raises:
        ValueError: If tokens are malformed
    """
    if not tokens:
        raise ValueError("Empty expression")

    expr, idx = _parse_expr(tokens, 0)

    if idx != len(tokens):
        raise ValueError("Extra tokens after expression")

    return expr


def _parse_expr(tokens, idx):
    """Recursively parse an expression starting at idx.

    Args:
        tokens: List of tokens
        idx: Current position

    Returns:
        (expr, next_idx) tuple

    Raises:
        ValueError: If expression is malformed
    """
    if idx >= len(tokens):
        raise ValueError("Unexpected end of input")

    token = tokens[idx]

    if token == '(':
        # Parse a list form
        idx += 1
        if idx >= len(tokens):
            raise ValueError("Unclosed parenthesis")

        operator = tokens[idx]
        idx += 1

        args = []
        while idx < len(tokens) and tokens[idx] != ')':
            arg, idx = _parse_expr(tokens, idx)
            args.append(arg)

        if idx >= len(tokens):
            raise ValueError("Unclosed parenthesis")

        idx += 1  # Skip closing ')'
        return [operator] + args, idx

    elif token == ')':
        raise ValueError("Unexpected closing parenthesis")

    else:
        # Atom (number)
        try:
            int(token)
        except ValueError:
            raise ValueError(f"Invalid atom: {token}")
        return token, idx + 1
