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

        processed=set()
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.If)
                and id(node) not in processed
            ):
                seen=set()
                current=node
                while isinstance(current, ast.If):
                    processed.add(id(current))
                    cond=ast.dump(current.test)

                    if cond in seen:
                        warnings.append({
                            "message":
                            "Duplicate condition detected in if/elif chain",
                            "severity":"MEDIUM",
                            "rule":"DUPLICATE_CONDITION",
                            "line": current.lineno
                        })

                    seen.add(cond)
                    if (
                        current.orelse and
                        len(current.orelse)==1 and
                        isinstance(current.orelse[0], ast.If)
                    ):
                        current=current.orelse[0]
                    else:
                        break

    except:
        pass
    return warnings
