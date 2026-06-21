def evaluate_ast(ast):
    """Evaluate an AST and return the result.

    Args:
        ast: Either an int (atom) or a tuple (op, arg1, arg2, ...)

    Returns:
        int: The result of evaluation.

    Raises:
        ValueError: If the AST is invalid.
    """
    if isinstance(ast, int):
        return ast

    if not isinstance(ast, tuple) or len(ast) < 3:
        raise ValueError("Invalid AST: operator must have at least 2 operands")

    op = ast[0]
    args = ast[1:]

    if op == '+':
        result = 0
        for arg in args:
            result += evaluate_ast(arg)
        return result
    elif op == '-':
        if len(args) == 1:
            return -evaluate_ast(args[0])
        result = evaluate_ast(args[0])
        for arg in args[1:]:
            result -= evaluate_ast(arg)
        return result
    else:
        raise ValueError(f"Unknown operator: {op}")
