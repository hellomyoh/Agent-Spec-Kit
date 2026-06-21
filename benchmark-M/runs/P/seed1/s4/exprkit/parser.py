import re


def tokenize(s: str) -> list:
    """Tokenize an s-expression string into a list of tokens."""
    tokens = []
    i = 0
    s = s.strip()

    while i < len(s):
        if s[i].isspace():
            i += 1
        elif s[i] in '()':
            tokens.append(s[i])
            i += 1
        else:
            match = re.match(r'-?\d+|[+\-*/]|neg|pow|lt|gt|eq', s[i:])
            if match:
                tokens.append(match.group(0))
                i += len(match.group(0))
            else:
                raise ValueError(f"Invalid token at position {i}: {s[i]}")

    return tokens


def parse(s: str):
    """Parse an s-expression string into an AST."""
    tokens = tokenize(s)
    ast, pos = parse_tokens(tokens, 0)

    if pos != len(tokens):
        raise ValueError("Unexpected tokens after expression")

    return ast


def parse_tokens(tokens, pos):
    """Recursively parse tokens starting at position pos."""
    if pos >= len(tokens):
        raise ValueError("Unexpected end of input")

    token = tokens[pos]

    if token == '(':
        pos += 1

        if pos >= len(tokens):
            raise ValueError("Unexpected end of input after '('")

        op = tokens[pos]
        if op not in ['+', '-', '*', '/', 'neg', 'pow', 'lt', 'gt', 'eq']:
            raise ValueError(f"Unknown operator: {op}")

        pos += 1
        args = []

        while pos < len(tokens) and tokens[pos] != ')':
            arg, pos = parse_tokens(tokens, pos)
            args.append(arg)

        if pos >= len(tokens):
            raise ValueError("Missing closing ')'")

        pos += 1
        return {'op': op, 'args': args}, pos

    else:
        try:
            num = int(token)
            return num, pos + 1
        except ValueError:
            raise ValueError(f"Invalid number: {token}")
