from rules.structural_rules import(
    check_deep_nesting,
    check_high_complexity,
    check_long_functions
)

from rules.logic_rules import(
    check_infinite_loops,
    check_missing_return,
    check_unused_variables
)

def apply_rules(result,source_code):
    warnings=[]
    critical=[]
    
    warnings+=check_deep_nesting(result)
    warnings+=check_high_complexity(result)
    warnings+=check_long_functions(result)
    warnings+=check_infinite_loops(source_code)
    warnings+=check_missing_return(result)
    warnings+=check_unused_variables(result)
    
    risk_score=100
    risk_score-=len(warnings)*10
    
    if risk_score<0:
        risk_score=0
    
    return {
        "warnings":warnings,
        "critical":critical,
        "risk_score":risk_score
    }