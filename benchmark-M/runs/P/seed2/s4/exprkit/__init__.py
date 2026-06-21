from .parser import parse
from .evaluator import eval_ast
from .rpn import ast_to_rpn


def evaluate(s):
    ast = parse(s)
    return eval_ast(ast)


def to_rpn(s):
    ast = parse(s)
    return ast_to_rpn(ast)


__all__ = ['evaluate', 'to_rpn']
