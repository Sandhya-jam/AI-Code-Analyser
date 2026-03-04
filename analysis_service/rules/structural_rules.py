def check_deep_nesting(result):
    warnings=[]
    if result.get("max_nesting_depth",0)>3:
        warnings.append({
            "message":"Deep nesting detected",
            "severity":"MEDIUM",
            "rule":"DEEP_NESTING",
            "line":None
        })
    return warnings

def check_high_complexity(result):
    warnings=[]
    if result.get("cyclomatic_complexity",1)>10:
        warnings.append({
            "message": "High cyclomatic complexity detected",
            "severity": "MEDIUM",
            "rule": "HIGH_COMPLEXITY",
            "line": None
        })
    return warnings

def check_long_functions(result):
    warnings=[]
    function_metrics=result.get("function_metrics",{})
    
    for func,metrics in function_metrics.items():
        if metrics.get("lines",0)>100:
            warnings.append({
                "message": f"Function '{func}' is too long (>50 lines)",
                "severity": "MEDIUM",
                "rule": "LONG_FUNCTION",
                "line": None
            })
    return warnings

def check_excessive_loops(result):
    warnings=[]
    
    if result.get("loops",0)>5:
        warnings.append({
            "message": "Excessive number of loops detected",
            "severity": "LOW",
            "rule": "EXCESSIVE_LOOPS",
            "line": None
        })
    return warnings

