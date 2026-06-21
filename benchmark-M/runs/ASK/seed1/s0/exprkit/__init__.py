"""
exprkit - Evaluate and compile prefix s-expression integer arithmetic.
"""

from .parser import parse
from .evaluator import evaluate_ast
from .rpn_converter import to_rpn_ast


def evaluate(s: str) -> int:
    """Evaluate a prefix s-expression and return the integer result.

    Supported operators: +, -

    Examples:
        evaluate("(+ 3 4)") == 7
        evaluate("(- (+ 1 2) 5)") == -2

    Args:
        s: String containing a prefix s-expression

    Returns:
        Integer result of evaluation

    Raises:
        ValueError: If input is malformed or contains unsupported operators
    """
    ast = parse(s)
    return evaluate_ast(ast)


def to_rpn(s: str) -> list:
    """Convert a prefix s-expression to RPN (postfix) notation.

    Returns a list of string tokens in postfix order.

    Examples:
        to_rpn("(+ 3 4)") == ["3", "4", "+"]
        to_rpn("(- 10 3)") == ["10", "3", "-"]

    Args:
        s: String containing a prefix s-expression

    Returns:
        List of string tokens in postfix order

    Raises:
        ValueError: If input is malformed or contains unsupported operators
    """
    ast = parse(s)
    return to_rpn_ast(ast)


__all__ = ['evaluate', 'to_rpn']
