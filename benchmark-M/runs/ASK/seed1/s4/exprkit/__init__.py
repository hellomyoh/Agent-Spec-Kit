"""
exprkit - Evaluate and compile prefix s-expression integer arithmetic.
"""

from .parser import parse
from .evaluator import evaluate_ast
from .rpn_converter import to_rpn_ast


def evaluate(s: str) -> int:
    """Evaluate a prefix s-expression and return the integer result.

    Supported operators: +, -, *, /, neg, pow, lt, gt, eq

    Division (/) is integer floor division returning int.
    Division by zero raises ZeroDivisionError.
    Comparison operators (lt, gt, eq) return 1 for true, 0 for false.

    Examples:
        evaluate("(+ 3 4)") == 7
        evaluate("(* 6 7)") == 42
        evaluate("(/ 7 2)") == 3
        evaluate("(- (+ 1 2) 5)") == -2
        evaluate("(neg 5)") == -5
        evaluate("(neg (- 2 9))") == 7
        evaluate("(pow 2 5)") == 32
        evaluate("(pow (+ 1 1) (- 4 1))") == 8
        evaluate("(lt 3 4)") == 1
        evaluate("(gt 3 4)") == 0
        evaluate("(eq 4 4)") == 1
        evaluate("(eq (* 2 3) (+ 5 1))") == 1

    Args:
        s: String containing a prefix s-expression

    Returns:
        Integer result of evaluation

    Raises:
        ValueError: If input is malformed or contains unsupported operators
        ZeroDivisionError: If division by zero is attempted
    """
    ast = parse(s)
    return evaluate_ast(ast)


def to_rpn(s: str) -> list:
    """Convert a prefix s-expression to RPN (postfix) notation.

    Returns a list of string tokens in postfix order.

    Examples:
        to_rpn("(+ 3 4)") == ["3", "4", "+"]
        to_rpn("(- 10 3)") == ["10", "3", "-"]
        to_rpn("(neg 5)") == ["5", "neg"]
        to_rpn("(neg (+ 1 2))") == ["1", "2", "+", "neg"]
        to_rpn("(pow 2 3)") == ["2", "3", "pow"]
        to_rpn("(lt 3 4)") == ["3", "4", "lt"]
        to_rpn("(eq (* 2 3) (+ 5 1))") == ["2", "3", "*", "5", "1", "+", "eq"]

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
