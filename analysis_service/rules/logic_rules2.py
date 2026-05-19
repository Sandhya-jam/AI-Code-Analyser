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
    try:
        tree = ast.parse(source_code)
        def process_block(stmts):
            last_assignment = {}
            used_since = set()

            for stmt in stmts:

                # detect variable usage FIRST
                for node in ast.walk(stmt):
                    if (
                        isinstance(node, ast.Name) and
                        isinstance(node.ctx, ast.Load)
                    ):
                        used_since.add(node.id)
                # assignment handling
                if isinstance(stmt, ast.Assign):

                    for target in stmt.targets:

                        if isinstance(target, ast.Name):
                            var = target.id
                            if (
                                var in last_assignment and
                                var not in used_since
                            ):
                                findings.append({
                                    "message":
                                    f"Redundant assignment to '{var}'",
                                    "severity": "LOW",
                                    "rule": "REDUNDANT_ASSIGNMENT",
                                    "line": last_assignment[var]
                                })

                            last_assignment[var] = stmt.lineno
                            # reset use tracking
                            if var in used_since:
                                used_since.remove(var)

                # recurse into nested blocks
                for field in ["body", "orelse"]:
                    if hasattr(stmt, field):
                        process_block(getattr(stmt, field))

        process_block(tree.body)

    except:
        pass
    return findings

def check_too_many_parameters(source_code):
    warnings=[]
    
    try:
        tree=ast.parse(source_code)
        
        for node in ast.walk(tree):
            if isinstance(node,ast.FunctionDef):
                param_count=(
                    len(node.args.args)+len(node.args.kwonlyargs)
                )
                if node.args.vararg:param_count+=1
                if node.args.kwarg:param_count+=1
                if param_count>5:
                    severity=(
                        "MEDIUM"
                        if param_count>=8
                        else "LOW"
                    )
                    warnings.append({
                        "message":f"Function '{node.name}' has {param_count} parameters, which may reduce readability",
                        "severity": severity,
                        "rule":"TOO_MANY_PARAMETERS",
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


                    