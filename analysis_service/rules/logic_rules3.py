import ast
from rules.Helper import (is_zero,evaluate_constant)

def check_division_by_zero(source_code):
    warnings=[]
    try:
        tree=ast.parse(source_code)

        zero_vars=set()

        # track x=0
        for stmt in ast.walk(tree):
            if isinstance(stmt, ast.Assign):
                if (
                    len(stmt.targets)==1 and
                    isinstance(stmt.targets[0], ast.Name) and
                    is_zero(stmt.value)
                ):
                    zero_vars.add(
                        stmt.targets[0].id
                    )

        # division checks
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp):
                if isinstance(
                    node.op,
                    (ast.Div, ast.FloorDiv, ast.Mod)
                ):
                    denom_val = evaluate_constant(
                        node.right
                    )

                    if denom_val == 0:
                        warnings.append({
                            "message":
                            "Division by zero detected",
                            "severity":"CRITICAL",
                            "rule":"DIVISION_BY_ZERO",
                            "line": node.lineno
                        })
    except:
        pass

    return warnings

def check_index_out_of_bounds(source_code):
    warnings = []
    try:
        tree = ast.parse(source_code)
        list_sizes = {}

        for node in ast.walk(tree):
            # Track list definitions
            if isinstance(node, ast.Assign):
                if isinstance(node.value, ast.List):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            list_sizes[target.id] = len(node.value.elts)

            # Check indexing
            if isinstance(node, ast.Subscript):
                if isinstance(node.value, ast.Name) and isinstance(node.slice, ast.Constant):
                    var_name = node.value.id
                    index_value = node.slice.value

                    if var_name in list_sizes:
                        if isinstance(index_value, int):
                            if index_value >= list_sizes[var_name] or index_value < 0:
                                warnings.append({
                                    "message": f"Index out of bounds for list '{var_name}'",
                                    "severity": "HIGH",
                                    "rule": "INDEX_OUT_OF_BOUNDS",
                                    "line": node.lineno
                                })

    except:
        pass
    return warnings
                   