import ast

def check_shadowed_variables(result):
    warnings=[]
    
    global_vars=set(result.get("global_assigned",[]))
    function_assigned=result.get("function_assigned",{})
    
    for func,vars_set in function_assigned.items():
        for var in vars_set:
            if var in global_vars:
                warnings.append({
                    "message": f"Variable '{var}' in function '{func}' shadows global variable",
                    "severity": "MEDIUM",
                    "rule": "SHADOWED_VARIABLE",
                    "line": None
                })
    return warnings

def check_redundant_assignment(source_code):

    findings = []
    tree = ast.parse(source_code)

    # track assignments per scope
    global_assignments = set()

    for node in tree.body:

        # GLOBAL SCOPE
        if isinstance(node, ast.Assign):

            for target in node.targets:

                if isinstance(target, ast.Name):

                    var = target.id

                    if var in global_assignments:

                        findings.append({
                            "message": f"Redundant assignment detected for variable '{var}'",
                            "severity": "LOW",
                            "rule": "REDUNDANT_ASSIGNMENT",
                            "line": node.lineno
                        })

                    global_assignments.add(var)

        # FUNCTION SCOPE
        if isinstance(node, ast.FunctionDef):

            local_assignments = set()

            for child in ast.walk(node):

                if isinstance(child, ast.Assign):

                    for target in child.targets:

                        if isinstance(target, ast.Name):

                            var = target.id

                            if var in local_assignments:

                                findings.append({
                                    "message": f"Redundant assignment detected for variable '{var}' in function '{node.name}'",
                                    "severity": "LOW",
                                    "rule": "REDUNDANT_ASSIGNMENT",
                                    "line": child.lineno
                                })

                            local_assignments.add(var)

    return findings

def check_too_many_parameters(source_code):
    warnings=[]
    
    try:
        tree=ast.parse(source_code)
        
        for node in ast.walk(tree):
            if isinstance(node,ast.FunctionDef):
                if len(node.args.args)>5:
                    warnings.append({
                        "message": f"Function '{node.name}' has too many parameters",
                        "severity": "LOW",
                        "rule": "TOO_MANY_PARAMETERS",
                        "line": node.lineno
                    })
    except:
        pass
    
    return warnings

def check_duplicate_conditions(source_code):
    warnings=[]
    
    try:
        tree=ast.parse(source_code)
        
        for node in ast.walk(tree):
            if isinstance(node,ast.If):
                seen_conditions=[]
                
                current=node
                while isinstance(current,ast.If):
                    condition_str=ast.dump(current.test)
                    
                    if condition_str in seen_conditions:
                        warnings.append({
                            "message": "Duplicate condition detected in if/elif chain",
                            "severity": "LOW",
                            "rule": "DUPLICATE_CONDITION",
                            "line": current.lineno
                        })
                    
                    seen_conditions.append(condition_str)
                    
                    if current.orelse and isinstance(current.orelse[0],ast.If):
                        current=current.orelse[0]
                    else:
                        break
    except:
        pass
    return warnings

def check_division_by_zero(source_code):
    warnings = []

    try:
        tree = ast.parse(source_code)

        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp):
                if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
                    if isinstance(node.right, ast.Constant) and node.right.value == 0:
                        warnings.append({
                            "message": "Division by zero detected",
                            "severity": "CRITICAL",
                            "rule": "DIVISION_BY_ZERO",
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


                    