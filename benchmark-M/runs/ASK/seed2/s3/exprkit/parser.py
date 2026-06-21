class ASTNode:
    pass


class Atom(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Atom({self.value})"


class Call(ASTNode):
    def __init__(self, op, args):
        self.op = op
        self.args = args

    def __repr__(self):
        return f"Call({self.op}, {self.args})"


def tokenize(s: str) -> list:
    tokens = []
    current_token = ""

    for char in s:
        if char in " \t\n\r":
            if current_token:
                tokens.append(current_token)
                current_token = ""
        elif char in "()":
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
        else:
            current_token += char

    if current_token:
        tokens.append(current_token)

    return tokens


def parse(s: str) -> ASTNode:
    tokens = tokenize(s)
    ast, idx = parse_expr(tokens, 0)

    if idx != len(tokens):
        raise ValueError("Unexpected tokens after expression")

    return ast


def parse_expr(tokens: list, idx: int):
    if idx >= len(tokens):
        raise ValueError("Unexpected end of input")

    token = tokens[idx]

    if token == "(":
        return parse_call(tokens, idx + 1)
    elif token == ")":
        raise ValueError("Unexpected closing parenthesis")
    else:
        try:
            value = int(token)
            return Atom(value), idx + 1
        except ValueError:
            raise ValueError(f"Invalid token: {token}")


def parse_call(tokens: list, idx: int):
    if idx >= len(tokens):
        raise ValueError("Unexpected end of input in function call")

    op_token = tokens[idx]

    if op_token == "(":
        raise ValueError("Expected operator, got '('")
    elif op_token == ")":
        raise ValueError("Expected operator, got ')'")

    op = op_token
    idx += 1
    args = []

    while idx < len(tokens) and tokens[idx] != ")":
        arg, idx = parse_expr(tokens, idx)
        args.append(arg)

    if idx >= len(tokens):
        raise ValueError("Unclosed parenthesis")

    return Call(op, args), idx + 1
