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
