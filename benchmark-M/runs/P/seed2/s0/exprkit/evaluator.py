def eval_ast(ast):
    if ast.get('type') == 'num':
        return ast['value']

    op = ast['op']
    args = ast['args']

    results = [eval_ast(arg) for arg in args]

    if op == '+':
        return sum(results)
    elif op == '-':
        result = results[0]
        for val in results[1:]:
            result -= val
        return result
    else:
        raise ValueError(f"Unknown operator: {op}")
