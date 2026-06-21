"""Convert s-expressions to Reverse Polish Notation (RPN)."""


def to_rpn_ast(ast):
    """Convert an expression tree to RPN token list.

    Args:
        ast: Expression tree from parser.parse()

    Returns:
        List of string tokens in postfix order

    Raises:
        ValueError: If conversion fails
    """
    if isinstance(ast, str):
        # Atom
        return [ast]

    if not isinstance(ast, list) or len(ast) == 0:
        raise ValueError("Invalid expression")

    operator = ast[0]

    if operator in ('+', '-', '*', '/'):
        if len(ast) != 3:
            raise ValueError(f"Operator '{operator}' requires exactly 2 arguments")

        # Convert operands recursively
        left_rpn = to_rpn_ast(ast[1])
        right_rpn = to_rpn_ast(ast[2])

        # Append operator at the end (postfix)
        return left_rpn + right_rpn + [operator]

    else:
        raise ValueError(f"Unknown operator: {operator}")
