def ast_to_rpn(ast):
    if ast.get('type') == 'num':
        return [str(ast['value'])]

    op = ast['op']
    args = ast['args']

    result = []
    for arg in args:
        result.extend(ast_to_rpn(arg))
    result.append(op)

    return result
