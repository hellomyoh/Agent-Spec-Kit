def to_rpn_ast(ast):
    """Convert an AST to Reverse Polish Notation (postfix form).

    Args:
        ast: Either an int (atom) or a tuple (op, arg1, arg2, ...)

    Returns:
        list: Token strings in postfix order.

    Raises:
        ValueError: If the AST is invalid.
    """
    if isinstance(ast, int):
        return [str(ast)]

    if not isinstance(ast, tuple) or len(ast) < 2:
        raise ValueError("Invalid AST: operator must have at least 1 operand")

    op = ast[0]
    args = ast[1:]

    result = []
    for arg in args:
        result.extend(to_rpn_ast(arg))

    result.append(op)
    return result
