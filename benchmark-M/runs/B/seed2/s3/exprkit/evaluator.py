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

    if not isinstance(ast, tuple) or len(ast) < 2:
        raise ValueError("Invalid AST: operator must have at least 1 operand")

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
    elif op == '*':
        result = 1
        for arg in args:
            result *= evaluate_ast(arg)
        return result
    elif op == '/':
        if len(args) != 2:
            raise ValueError("Division requires exactly 2 operands")
        dividend = evaluate_ast(args[0])
        divisor = evaluate_ast(args[1])
        if divisor == 0:
            raise ZeroDivisionError("Division by zero")
        return int(dividend // divisor)
    elif op == 'neg':
        if len(args) != 1:
            raise ValueError("Negation requires exactly 1 operand")
        return -evaluate_ast(args[0])
    elif op == 'pow':
        if len(args) != 2:
            raise ValueError("Power requires exactly 2 operands")
        base = evaluate_ast(args[0])
        exponent = evaluate_ast(args[1])
        return int(base ** exponent)
    else:
        raise ValueError(f"Unknown operator: {op}")
