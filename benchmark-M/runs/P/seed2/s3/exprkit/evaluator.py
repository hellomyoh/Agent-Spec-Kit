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
    elif op == '*':
        result = results[0]
        for val in results[1:]:
            result *= val
        return result
    elif op == '/':
        if len(results) < 2:
            raise ValueError(f"Operator {op} requires at least 2 arguments")
        result = results[0]
        for val in results[1:]:
            if val == 0:
                raise ZeroDivisionError("Division by zero")
            result = int(result // val)
        return result
    elif op == 'neg':
        return -results[0]
    elif op == 'pow':
        return results[0] ** results[1]
    else:
        raise ValueError(f"Unknown operator: {op}")
