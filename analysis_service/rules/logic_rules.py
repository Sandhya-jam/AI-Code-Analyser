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
                        warnings.append(
                            "Potential infinite loop: 'while True' without break"
                        )

    except Exception:
        pass

    return warnings

def check_missing_return(result):
    warnings = []

    function_returns = result.get("function_returns", {})
    function_metrics = result.get("function_metrics", {})

    for func in function_metrics:
        lines = function_metrics[func].get("lines", 0)

        # Ignore empty or very small functions
        if lines <= 1:
            continue

        if not function_returns.get(func, False):
            warnings.append(
                f"Function '{func}' does not have a return statement"
            )

    return warnings

def check_unused_variables(result):
    warnings=[]
    
    # Global Scope
    global_assigned=set(result.get("global_assigned",[]))
    global_used=set(result.get("global_used",[]))
    
    unused_globals=global_assigned-global_used
    
    for var in unused_globals:
        warnings.append(f"Global variable '{var}' is assigned but never used")
    
    # Function Scope
    function_assigned=result.get("function_assigned",{})
    function_used=result.get("function_used",{})
    
    for func in function_assigned:
        assigned=set(function_assigned.get(func,[]))
        used=set(function_used.get(func,[]))
        
        unused=assigned-used
        
        for var in unused:
            warnings.append(
                f"Variable '{var}' in function '{func}' is assigned but never used"
            )
    return warnings

def check_constant_conditions(source_code):
    warnings=[]
    
    try:
        tree=ast.parse(source_code)
        
        for node in ast.walk(tree):
            if isinstance(node,ast.If):
                if isinstance(node.test,ast.Constant):
                    warnings.append("Constant condition detected in if statement")
                
                if isinstance(node.test,ast.Compare):
                    if isinstance(node.test.left,ast.Constant) and \
                        all(isinstance(comp,ast.Constant) for comp in node.test.comparators):
                            warnings.append("Always-true or Always-false comparision detected")
    except:
        pass
    return warnings
