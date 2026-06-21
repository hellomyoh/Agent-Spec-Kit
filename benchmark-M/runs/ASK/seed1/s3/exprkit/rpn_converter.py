"""
AST to RPN (postfix) conversion visitor.
"""

from .parser import AtomNode, ExprNode
from .operators import get_registry


class RPNConverter:
    """Visitor that converts an AST to RPN (Reverse Polish Notation) tokens."""

    def __init__(self):
        self.registry = get_registry()

    def to_rpn(self, node):
        """Convert an AST node to RPN and return a list of string tokens."""
        tokens = []
        self._collect_tokens(node, tokens)
        return tokens

    def _collect_tokens(self, node, tokens):
        """Recursively collect RPN tokens from an AST node."""
        if isinstance(node, AtomNode):
            self._collect_atom(node, tokens)
        elif isinstance(node, ExprNode):
            self._collect_expr(node, tokens)
        else:
            raise ValueError(f"Unknown node type: {type(node)}")

    def _collect_atom(self, node, tokens):
        """Collect tokens from an atom node (just the value)."""
        tokens.append(str(node.value))

    def _collect_expr(self, node, tokens):
        """Collect tokens from an expression node.

        In postfix notation, operands come first, then the operator.
        """
        op = node.op

        # Collect all operands in order
        for arg in node.args:
            self._collect_tokens(arg, tokens)

        # Then add the operator
        tokens.append(op)


def to_rpn_ast(ast):
    """Convert an AST to RPN and return a list of string tokens."""
    converter = RPNConverter()
    return converter.to_rpn(ast)
