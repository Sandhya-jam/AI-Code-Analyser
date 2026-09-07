from rules.structural_rules import(
    check_deep_nesting,
    check_high_complexity,
    check_long_functions,
    check_excessive_loops
)

from rules.logic_rules import(
    check_infinite_loops,
    check_missing_return,
    check_unused_variables,
    check_constant_conditions,
    check_unreachable_code,
)

from rules.logic_rules2 import(
    check_duplicate_conditions,
    check_redundant_assignment,
    check_shadowed_variables,
    check_too_many_parameters,
)

from rules.logic_rules3 import(
    check_division_by_zero,
    check_index_out_of_bounds
)

def apply_rules(result,source_code):
    warnings=[]
    critical=[]
    # structural rules
    warnings+=check_deep_nesting(result)
    warnings+=check_high_complexity(result)
    warnings+=check_long_functions(result)
    warnings+=check_excessive_loops(result)
    # Logical rules1
    warnings+=check_infinite_loops(source_code)
    warnings+=check_missing_return(source_code)
    warnings+=check_unused_variables(result)
    warnings+=check_constant_conditions(source_code)
    warnings+=check_unreachable_code(source_code)
    # Logical rules2
    warnings+=check_duplicate_conditions(source_code)
    warnings+=check_redundant_assignment(source_code)
    warnings+=check_shadowed_variables(result)
    warnings+=check_too_many_parameters(source_code)
    warnings+=check_division_by_zero(source_code)
    warnings+=check_index_out_of_bounds(source_code)
    
    return warnings

def calculate_risk_score(result, critical, high, medium, low):

    total_lines = max(result.get("total_lines", 1), 1)
    complexity = max(result.get("cyclomatic_complexity", 1), 1)

    severity_points = (
        len(critical) * 10 +
        len(high) * 6 +
        len(medium) * 3 +
        len(low) * 1
    )

    # Maximum severity contribution
    severity_penalty = min(severity_points, 60)

    complexity_penalty = max(complexity - 10, 0) * 1.5
    complexity_penalty = min(complexity_penalty, 20)

    total_bugs = (
        len(critical) +
        len(high) +
        len(medium) +
        len(low)
    )

    bugs_per_100_lines = (total_bugs / total_lines) * 100

    density_penalty = min(bugs_per_100_lines * 2, 20)

    risk_score = (
        100
        - severity_penalty
        - complexity_penalty
        - density_penalty
    )

    return max(min(round(risk_score), 100), 0)
