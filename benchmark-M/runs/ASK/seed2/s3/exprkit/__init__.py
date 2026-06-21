from exprkit.parser import parse
from exprkit.evaluator import evaluate_ast
from exprkit.rpn import ast_to_rpn


def evaluate(s: str) -> int:
    ast = parse(s)
    return evaluate_ast(ast)


def to_rpn(s: str) -> list:
    ast = parse(s)
    return ast_to_rpn(ast)


__all__ = ["evaluate", "to_rpn"]
