# Ground-truth oracle for the exprkit M-pilot (single file; agents build a multi-file package).
# s-expression calculator: integers + prefix ops. Two per-op visitors: evaluate, to_rpn.
import re
_BIN = {"+", "-", "*", "/", "pow", "lt", "gt", "eq"}   # binary ops; "neg" is unary

def _tok(s):
    return re.findall(r'\(|\)|[^\s()]+', s)

def _parse(s):
    toks = _tok(s); i = 0
    def p():
        nonlocal i
        if i >= len(toks): raise ValueError("unexpected end")
        t = toks[i]; i += 1
        if t == '(':
            if i >= len(toks): raise ValueError("unexpected end")
            op = toks[i]; i += 1
            args = []
            while i < len(toks) and toks[i] != ')':
                args.append(p())
            if i >= len(toks): raise ValueError("unbalanced")
            i += 1  # consume ')'
            return (op, args)
        if t == ')': raise ValueError("unexpected )")
        if not re.fullmatch(r'-?\d+', t): raise ValueError(f"bad atom {t!r}")
        return ("num", int(t))
    n = p()
    if i != len(toks): raise ValueError("trailing tokens")
    return n

def _ev(n):
    if n[0] == "num": return n[1]
    op, args = n
    if op == "neg":
        if len(args) != 1: raise ValueError("arity")
        return -_ev(args[0])
    if op not in _BIN: raise ValueError(f"unknown op {op}")
    if len(args) != 2: raise ValueError("arity")
    a, b = _ev(args[0]), _ev(args[1])
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if op == "/":
        if b == 0: raise ZeroDivisionError()
        return a // b                 # DECISION (S1): floor division -> int
    if op == "pow": return a ** b
    if op == "lt": return 1 if a < b else 0
    if op == "gt": return 1 if a > b else 0
    if op == "eq": return 1 if a == b else 0

def _rpn(n):
    if n[0] == "num": return [str(n[1])]
    op, args = n
    out = []
    for a in args: out += _rpn(a)
    out.append(op)
    return out

def evaluate(s): return _ev(_parse(s))
def to_rpn(s): return _rpn(_parse(s))
