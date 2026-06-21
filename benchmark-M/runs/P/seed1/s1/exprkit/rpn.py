from . import parser


def to_rpn(s: str) -> list:
    """Convert an s-expression to Reverse Polish Notation (postfix form)."""
    ast = parser.parse(s)
    return ast_to_rpn(ast)


def ast_to_rpn(node) -> list:
    """Recursively convert an AST node to RPN tokens."""
    if isinstance(node, int):
        return [str(node)]

    if isinstance(node, dict):
        op = node['op']
        args = node['args']

        if op not in ['+', '-', '*', '/']:
            raise ValueError(f"Unknown operator: {op}")

        if len(args) != 2:
            raise ValueError(f"Operator '{op}' requires exactly 2 arguments, got {len(args)}")

        result = []
        result.extend(ast_to_rpn(args[0]))
        result.extend(ast_to_rpn(args[1]))
        result.append(op)

        return result

    raise ValueError(f"Invalid AST node: {node}")
