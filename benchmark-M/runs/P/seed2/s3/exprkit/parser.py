import re


def tokenize(s):
    tokens = re.findall(r'\(|\)|[+-]?\d+|[+\-*/]|neg|pow', s)
    return tokens


def parse(s):
    tokens = tokenize(s)
    if not tokens:
        raise ValueError("Empty input")

    result, idx = parse_expr(tokens, 0)
    if idx != len(tokens):
        raise ValueError("Extra tokens after expression")
    return result


def parse_expr(tokens, idx):
    if idx >= len(tokens):
        raise ValueError("Unexpected end of input")

    token = tokens[idx]

    if token == '(':
        idx += 1
        if idx >= len(tokens):
            raise ValueError("Unexpected end of input after '('")

        op = tokens[idx]
        if op not in ('+', '-', '*', '/', 'neg', 'pow'):
            raise ValueError(f"Unknown operator: {op}")
        idx += 1

        args = []
        while idx < len(tokens) and tokens[idx] != ')':
            arg, idx = parse_expr(tokens, idx)
            args.append(arg)

        if idx >= len(tokens) or tokens[idx] != ')':
            raise ValueError("Missing closing ')'")
        idx += 1

        if op == 'neg':
            if len(args) != 1:
                raise ValueError(f"Operator {op} requires exactly 1 argument, got {len(args)}")
        elif op == 'pow':
            if len(args) != 2:
                raise ValueError(f"Operator {op} requires exactly 2 arguments, got {len(args)}")
        else:
            if len(args) < 2:
                raise ValueError(f"Operator {op} requires at least 2 arguments, got {len(args)}")

        return {'op': op, 'args': args}, idx

    else:
        try:
            num = int(token)
            return {'type': 'num', 'value': num}, idx + 1
        except ValueError:
            raise ValueError(f"Invalid token: {token}")
