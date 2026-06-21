"""exprkit — s-expression evaluator and RPN compiler."""

from .parser import tokenize, parse
from .evaluator import evaluate_ast
from .rpn import to_rpn_ast


def evaluate(s):
    """Evaluate a prefix s-expression string.

    Args:
        s: Input string with s-expression syntax

    Returns:
        Integer result

    Raises:
        ValueError: If input is malformed
    """
    tokens = tokenize(s)
    ast = parse(tokens)
    return evaluate_ast(ast)


def to_rpn(s):
    """Convert a prefix s-expression to Reverse Polish Notation.

    Args:
        s: Input string with s-expression syntax

    Returns:
        List of string tokens in postfix order

    Raises:
        ValueError: If input is malformed
    """
    tokens = tokenize(s)
    ast = parse(tokens)
    return to_rpn_ast(ast)


__all__ = ['evaluate', 'to_rpn']
