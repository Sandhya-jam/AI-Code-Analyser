import ast
import operator
def get_condition_variables(node):
    vars = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Name):
            vars.add(n.id)
    return vars

def get_modified_variables(node):
    vars = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Assign):
            for target in n.targets:
                if isinstance(target, ast.Name):
                    vars.add(target.id)
        elif isinstance(n, ast.AugAssign):
            if isinstance(n.target, ast.Name):
                vars.add(n.target.id)
    return vars

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod
}

def evaluate_constant(node):
    # literal
    if isinstance(node, ast.Constant):
        return node.value

    # unary
    if isinstance(node, ast.UnaryOp):
        val = evaluate_constant(node.operand)

        if val is None:
            return None
        if isinstance(node.op, ast.USub):
            return -val
        if isinstance(node.op, ast.UAdd):
            return +val
    # binary
    if isinstance(node, ast.BinOp):
        left = evaluate_constant(node.left)
        right = evaluate_constant(node.right)

        if left is None or right is None:
            return None

        op_type = type(node.op)
        if op_type in OPS:
            try:
                return OPS[op_type](left, right)
            except:
                return None

    return None

def is_zero(node):

    if isinstance(node, ast.Constant):
        return node.value == 0

    if (
        isinstance(node, ast.UnaryOp)
        and isinstance(node.op, ast.USub)
        and isinstance(node.operand, ast.Constant)
    ):
        return node.operand.value == 0

    return False