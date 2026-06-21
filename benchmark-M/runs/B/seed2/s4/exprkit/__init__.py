from .parser import parse
from .evaluator import evaluate_ast
from .rpn import to_rpn_ast


def evaluate(s: str) -> int:
    """Evaluate a prefix s-expression string.

    Args:
        s: A prefix s-expression (e.g., "(+ 3 4)")

    Returns:
        int: The result of the evaluation.

    Raises:
        ValueError: If the input is malformed.
    """
    ast = parse(s)
    return evaluate_ast(ast)


def to_rpn(s: str) -> list:
    """Convert a prefix s-expression to Reverse Polish Notation.

    Args:
        s: A prefix s-expression (e.g., "(+ 3 4)")

    Returns:
        list: Token strings in postfix order (e.g., ["3", "4", "+"])

    Raises:
        ValueError: If the input is malformed.
    """
    ast = parse(s)
    return to_rpn_ast(ast)


__all__ = ['evaluate', 'to_rpn']
