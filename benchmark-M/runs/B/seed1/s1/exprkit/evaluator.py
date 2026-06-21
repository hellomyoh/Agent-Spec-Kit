"""Evaluator for s-expression arithmetic."""


def evaluate_ast(ast):
    """Evaluate an expression tree.

    Args:
        ast: Expression tree from parser.parse()

    Returns:
        Integer result

    Raises:
        ValueError: If evaluation fails
    """
    if isinstance(ast, str):
        # Atom
        return int(ast)

    if not isinstance(ast, list) or len(ast) == 0:
        raise ValueError("Invalid expression")

    operator = ast[0]

    if operator == '+':
        if len(ast) != 3:
            raise ValueError(f"Operator '{operator}' requires exactly 2 arguments")
        left = evaluate_ast(ast[1])
        right = evaluate_ast(ast[2])
        return left + right

    elif operator == '-':
        if len(ast) != 3:
            raise ValueError(f"Operator '{operator}' requires exactly 2 arguments")
        left = evaluate_ast(ast[1])
        right = evaluate_ast(ast[2])
        return left - right

    elif operator == '*':
        if len(ast) != 3:
            raise ValueError(f"Operator '{operator}' requires exactly 2 arguments")
        left = evaluate_ast(ast[1])
        right = evaluate_ast(ast[2])
        return left * right

    elif operator == '/':
        if len(ast) != 3:
            raise ValueError(f"Operator '{operator}' requires exactly 2 arguments")
        left = evaluate_ast(ast[1])
        right = evaluate_ast(ast[2])
        if right == 0:
            raise ZeroDivisionError("division by zero")
        return int(left // right)

    else:
        raise ValueError(f"Unknown operator: {operator}")
