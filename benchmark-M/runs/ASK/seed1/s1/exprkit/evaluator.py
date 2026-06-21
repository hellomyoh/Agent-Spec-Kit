"""
AST evaluation visitor.
"""

from .parser import AtomNode, ExprNode
from .operators import get_registry


class Evaluator:
    """Visitor that evaluates an AST to an integer result."""

    def __init__(self):
        self.registry = get_registry()

    def evaluate(self, node):
        """Evaluate an AST node and return the integer result."""
        if isinstance(node, AtomNode):
            return self._eval_atom(node)
        elif isinstance(node, ExprNode):
            return self._eval_expr(node)
        else:
            raise ValueError(f"Unknown node type: {type(node)}")

    def _eval_atom(self, node):
        """Evaluate an atom node (just return its value)."""
        return node.value

    def _eval_expr(self, node):
        """Evaluate an expression node.

        Recursively evaluate all arguments, then apply the operator.
        """
        op = node.op
        args = [self.evaluate(arg) for arg in node.args]

        func = self.registry.get_func(op)
        try:
            result = func(*args)
        except Exception as e:
            raise ValueError(f"Error evaluating {op}: {e}")

        return int(result)


def evaluate_ast(ast):
    """Evaluate an AST and return the integer result."""
    evaluator = Evaluator()
    return evaluator.evaluate(ast)
