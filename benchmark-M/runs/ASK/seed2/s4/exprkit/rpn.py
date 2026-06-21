from exprkit.parser import Atom, Call


BINARY_OPS = {"+", "-", "*", "/", "pow", "lt", "gt", "eq"}
UNARY_OPS = {"neg"}


def ast_to_rpn(node) -> list:
    result = []
    visit_rpn(node, result)
    return result


def visit_rpn(node, result: list):
    if isinstance(node, Atom):
        result.append(str(node.value))
    elif isinstance(node, Call):
        visit_call_rpn(node, result)
    else:
        raise ValueError(f"Unknown AST node type: {type(node)}")


def visit_call_rpn(call: Call, result: list):
    op = call.op

    if op in BINARY_OPS:
        if len(call.args) != 2:
            raise ValueError(f"Operator '{op}' expects 2 arguments, got {len(call.args)}")
        visit_rpn(call.args[0], result)
        visit_rpn(call.args[1], result)
        result.append(op)
    elif op in UNARY_OPS:
        if len(call.args) != 1:
            raise ValueError(f"Operator '{op}' expects 1 argument, got {len(call.args)}")
        visit_rpn(call.args[0], result)
        result.append(op)
    else:
        raise ValueError(f"Unknown operator: {op}")
