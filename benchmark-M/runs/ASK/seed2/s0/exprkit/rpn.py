from exprkit.parser import Atom, Call


SUPPORTED_OPS = {"+", "-"}


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

    if op not in SUPPORTED_OPS:
        raise ValueError(f"Unknown operator: {op}")

    if len(call.args) != 2:
        raise ValueError(f"Operator '{op}' expects 2 arguments, got {len(call.args)}")

    visit_rpn(call.args[0], result)
    visit_rpn(call.args[1], result)
    result.append(op)
