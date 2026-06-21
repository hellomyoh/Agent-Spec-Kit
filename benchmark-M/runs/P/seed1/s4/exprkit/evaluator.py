from . import parser


def evaluate(s: str) -> int:
    """Evaluate an s-expression and return the result."""
    ast = parser.parse(s)
    return eval_ast(ast)


def eval_ast(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, int):
        return node

    if isinstance(node, dict):
        op = node['op']
        args = node['args']

        if op == '+':
            if len(args) != 2:
                raise ValueError(f"Operator '{op}' requires exactly 2 arguments, got {len(args)}")
            return eval_ast(args[0]) + eval_ast(args[1])

        elif op == '-':
            if len(args) != 2:
                raise ValueError(f"Operator '{op}' requires exactly 2 arguments, got {len(args)}")
            return eval_ast(args[0]) - eval_ast(args[1])

        elif op == '*':
            if len(args) != 2:
                raise ValueError(f"Operator '{op}' requires exactly 2 arguments, got {len(args)}")
            return eval_ast(args[0]) * eval_ast(args[1])

        elif op == '/':
            if len(args) != 2:
                raise ValueError(f"Operator '{op}' requires exactly 2 arguments, got {len(args)}")
            left = eval_ast(args[0])
            right = eval_ast(args[1])
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left // right

        elif op == 'neg':
            if len(args) != 1:
                raise ValueError(f"Operator '{op}' requires exactly 1 argument, got {len(args)}")
            return -eval_ast(args[0])

        elif op == 'pow':
            if len(args) != 2:
                raise ValueError(f"Operator '{op}' requires exactly 2 arguments, got {len(args)}")
            return eval_ast(args[0]) ** eval_ast(args[1])

        elif op == 'lt':
            if len(args) != 2:
                raise ValueError(f"Operator '{op}' requires exactly 2 arguments, got {len(args)}")
            return 1 if eval_ast(args[0]) < eval_ast(args[1]) else 0

        elif op == 'gt':
            if len(args) != 2:
                raise ValueError(f"Operator '{op}' requires exactly 2 arguments, got {len(args)}")
            return 1 if eval_ast(args[0]) > eval_ast(args[1]) else 0

        elif op == 'eq':
            if len(args) != 2:
                raise ValueError(f"Operator '{op}' requires exactly 2 arguments, got {len(args)}")
            return 1 if eval_ast(args[0]) == eval_ast(args[1]) else 0

        else:
            raise ValueError(f"Unknown operator: {op}")

    raise ValueError(f"Invalid AST node: {node}")
