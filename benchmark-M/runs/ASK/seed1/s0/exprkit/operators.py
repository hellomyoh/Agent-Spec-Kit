"""
Operator registry and implementations.
"""


class OperatorRegistry:
    """Central registry for supported operators."""

    def __init__(self):
        self._operators = {}
        self._register_builtins()

    def _register_builtins(self):
        """Register built-in operators."""
        self.register('+', 2, lambda a, b: a + b)
        self.register('-', 2, lambda a, b: a - b)

    def register(self, name, arity, func):
        """Register an operator.

        Args:
            name: Operator symbol (e.g., '+', '-')
            arity: Number of arguments expected
            func: Callable that implements the operation
        """
        self._operators[name] = {
            'arity': arity,
            'func': func
        }

    def get_arity(self, op):
        """Get the arity of an operator.

        Raises ValueError if operator not found.
        """
        if op not in self._operators:
            raise ValueError(f"Unknown operator: {op}")
        return self._operators[op]['arity']

    def get_func(self, op):
        """Get the evaluation function for an operator.

        Raises ValueError if operator not found.
        """
        if op not in self._operators:
            raise ValueError(f"Unknown operator: {op}")
        return self._operators[op]['func']

    def is_operator(self, token):
        """Check if a token is a registered operator."""
        return token in self._operators

    def operators(self):
        """Return all operator names."""
        return list(self._operators.keys())


# Global operator registry
_registry = OperatorRegistry()


def get_registry():
    """Get the global operator registry."""
    return _registry
