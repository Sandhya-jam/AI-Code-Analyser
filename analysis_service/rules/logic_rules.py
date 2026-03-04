import ast

def check_infinite_loops(source_code):
    warnings = []

    try:
        tree = ast.parse(source_code)

        for node in ast.walk(tree):
            if isinstance(node, ast.While):
                # Check if condition is literally True
                is_true_condition = False

                if isinstance(node.test, ast.Constant):
                    if node.test.value in [True, 1]:
                        is_true_condition = True

                if is_true_condition:
                    # Check if there's a break inside loop
                    has_break = any(
                        isinstance(n, ast.Break)
                        for n in ast.walk(node)
                    )
                    if not has_break:
                        warnings.append({
                            "message": "Potential infinite loop detected",
                            "severity": "CRITICAL",
                            "rule": "INFINITE_LOOP",
                            "line": node.lineno
                        })

    except Exception:
        pass

    return warnings

def check_missing_return(source_code):

    findings = []
    tree = ast.parse(source_code)

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            has_return = False
            has_possible_path_without_return = False

            for child in ast.walk(node):

                if isinstance(child, ast.Return):
                    has_return = True

                if isinstance(child, ast.If):
                    if not any(isinstance(n, ast.Return) for n in ast.walk(child)):
                        has_possible_path_without_return = True

            if has_return and has_possible_path_without_return:

                findings.append({
                    "message": f"Function '{node.name}' may exit without returning a value",
                    "severity": "HIGH",
                    "rule": "MISSING_RETURN",
                    "line": node.lineno
                })

    return findings

def check_unused_variables(result):
    warnings=[]
    
    # Global Scope
    global_assigned=set(result.get("global_assigned",[]))
    global_used=set(result.get("global_used",[]))
    
    unused_globals=global_assigned-global_used
    
    for var in unused_globals:
        warnings.append({
            "message": f"Global variable '{var}' assigned but never used",
            "severity": "LOW",
            "rule": "UNUSED_VARIABLE",
            "line": None
        })
    
    # Function Scope
    function_assigned=result.get("function_assigned",{})
    function_used=result.get("function_used",{})
    
    for func in function_assigned:
        assigned=set(function_assigned.get(func,[]))
        used=set(function_used.get(func,[]))
        
        unused=assigned-used
        
        for var in unused:
            warnings.append({
                "message": f"Variable '{var}' assigned but never used in function '{func}'",
                "severity": "LOW",
                "rule": "UNUSED_VARIABLE",
                "line": None
            })
    return warnings

def check_constant_conditions(source_code):
    warnings=[]
    
    try:
        tree=ast.parse(source_code)
        
        for node in ast.walk(tree):
            if isinstance(node,ast.If):
                if isinstance(node.test,ast.Constant):
                    warnings.append({
                        "message": "Constant condition detected",
                        "severity": "MEDIUM",
                        "rule": "CONSTANT_CONDITION",
                        "line": node.lineno
                    })
                
                if isinstance(node.test,ast.Compare):
                    if isinstance(node.test.left,ast.Constant) and \
                        all(isinstance(comp,ast.Constant) for comp in node.test.comparators):
                            warnings.append({
                                "message": "Constant condition detected",
                                "severity": "MEDIUM",
                                "rule": "CONSTANT_CONDITION",
                                "line": node.lineno
                            })
    except:
        pass
    return warnings

def check_unreachable_code(source_code):
    warnings=[]
    try:
        tree=ast.parse(source_code)
        
        for node in ast.walk(tree):
            if hasattr(node,"body") and isinstance(node.body,list):
                for i,stmt in enumerate(node.body[:-1]):
                    if isinstance(stmt,(ast.Return,ast.Break,ast.Continue)):
                        warnings.append({
                            "message": "Unreachable code detected after control statement",
                            "severity": "HIGH",
                            "rule": "UNREACHABLE_CODE",
                            "line": stmt.lineno
                        })
    except:
        pass
    
    return warnings

def check_use_before_assignment(source_code):
    warnings = []

    try:
        tree = ast.parse(source_code)
        builtin_names = set()

        # Handle global scope
        assigned_global = set()

        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assigned_global.add(target.id)

            if isinstance(node, ast.Expr):
                for child in ast.walk(node):
                    if isinstance(child, ast.Name):
                        if isinstance(child.ctx, ast.Load):
                            if child.id not in assigned_global and child.id not in builtin_names:
                                warnings.append({
                                    "message": f"Variable '{node.id}' used before assignment",
                                    "severity": "HIGH",
                                    "rule": "USE_BEFORE_ASSIGNMENT",
                                    "line": node.lineno
                                })

            if isinstance(node, ast.FunctionDef):
                warnings += _check_function_scope(node, builtin_names)

    except:
        pass

    return warnings

def _check_function_scope(function_node, builtin_names):
    warnings = []

    assigned = set()
    params = {arg.arg for arg in function_node.args.args}

    for stmt in function_node.body:
        # Check variable usage first
        for child in ast.walk(stmt):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                if (
                    child.id not in assigned
                    and child.id not in params
                    and child.id not in builtin_names
                ):
                    warnings.append({
                        "message":f"Variable '{child.id}' used before assignment in function '{function_node.name}'",
                        "severity":"MEDIUM",
                        "rule":"USED BEFORE ASSIGNMENT(FUNCTION)",
                        "line":child.lineno
                    })

        # Then track assignments
        if isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name):
                    assigned.add(target.id)

    return warnings
