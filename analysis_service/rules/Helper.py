import ast

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
