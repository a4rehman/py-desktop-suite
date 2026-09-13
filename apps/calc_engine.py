"""Pure arithmetic helpers shared by the desktop and web calculators."""

import ast
import math

_ALLOWED_BINOPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod)
_ALLOWED_UNOPS = (ast.UAdd, ast.USub)


def _is_arithmetic(expr):
    """True only when the expression is a plain arithmetic expression."""
    try:
        tree = ast.parse(expr, mode="eval")
    except (SyntaxError, ValueError):
        return False

    def check(node):
        if isinstance(node, ast.Expression):
            pass
        elif isinstance(node, (ast.operator, ast.unaryop)):
            pass  # kind validated by the parent BinOp/UnaryOp branch
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
                return False
        elif isinstance(node, ast.BinOp):
            if not isinstance(node.op, _ALLOWED_BINOPS):
                return False
        elif isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, _ALLOWED_UNOPS):
                return False
        else:
            return False
        return all(check(child) for child in ast.iter_child_nodes(node))

    return check(tree)


def evaluate(expr):
    """Evaluate a basic arithmetic expression string.

    Returns the result formatted as a string (whole floats become ints),
    or None when the expression is empty, invalid, or not plain arithmetic.
    """
    if not expr or not str(expr).strip():
        return None
    try:
        safe = str(expr).replace("×", "*").replace("÷", "/")
        if not _is_arithmetic(safe):
            return None
        result = eval(safe, {"__builtins__": {}}, {})
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return str(result)
    except Exception:
        return None


def sqrt(expr):
    """Square root of an already evaluated expression, formatted or None."""
    result = evaluate(expr)
    if result is None:
        return None
    try:
        val = float(result)
    except (TypeError, ValueError):
        return None
    if val < 0:
        return None
    return f"{math.sqrt(val):.6g}"