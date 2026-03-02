def check_deep_nesting(result):
    warnings=[]
    if result.get("max_nesting_depth",0)>3:
        warnings.append("Deep nesting detected")
    return warnings

def check_high_complexity(result):
    warnings=[]
    if result.get("cyclomatic_complexity",1)>10:
        warnings.append("High cyclomatic complexity")
    return warnings

def check_long_functions(result):
    warnings=[]
    function_metrics=result.get("function_metrics",{})
    
    for func,metrics in function_metrics.items():
        if metrics.get("lines",0)>100:
            warnings.append(f"Function '{func}' is too long (>100 lines)")
    return warnings

def check_excessive_loops(result):
    warnings=[]
    
    if result.get("loops",0)>5:
        warnings.append("Excessive number of loops detected (>5)")
    return warnings

