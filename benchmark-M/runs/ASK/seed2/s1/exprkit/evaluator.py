from exprkit.parser import Atom, Call


def floor_divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    return int(a // b)


BINARY_OPS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": floor_divide,
}


def evaluate_ast(node) -> int:
    if isinstance(node, Atom):
        return node.value
    elif isinstance(node, Call):
        return evaluate_call(node)
    else:
        raise ValueError(f"Unknown AST node type: {type(node)}")


def evaluate_call(call: Call) -> int:
    op = call.op

    if op not in BINARY_OPS:
        raise ValueError(f"Unknown operator: {op}")

    if len(call.args) != 2:
        raise ValueError(f"Operator '{op}' expects 2 arguments, got {len(call.args)}")

    left = evaluate_ast(call.args[0])
    right = evaluate_ast(call.args[1])

    return BINARY_OPS[op](left, right)
