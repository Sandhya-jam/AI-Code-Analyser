BUG_KEYWORDS = {
    "DIVISION_BY_ZERO": ["division by zero", "divide by zero","dividing by zero"],
    "UNUSED_VARIABLE": ["unused variable","variable is never used","variable is not used"],
    "REDUNDANT_ASSIGNMENT": ["redundant assignment", "unnecessary assignment","redundant variable assignment"],
    "DUPLICATE_CONDITION": ["duplicate condition","duplicated condition","same condition","repeated condition"],
    "SHADOWED_VARIABLE": ["shadowed variable","variable shadowing","shadowing variable","variable is shadowed"],
    "UNREACHABLE_CODE": ["unreachable code","code is unreachable","unreachable statement","unreachable statements"],
    "INDEX_OUT_OF_BOUNDS": ["index out of bounds","index out of range","array index out of bounds","list index out of range","invalid index"],
    "INFINITE_LOOP": ["infinite loop","infinite loop with no exit","endless loop",
        "non-terminating loop","non terminating loop","loop never terminates"],
    "MISSING_RETURN": ["missing return","missing return statement","no return statement",
        "function does not return","function doesn't return","not returning a value"],
    "CONSTANT_CONDITION": ["constant condition","condition is always true","condition is always false",
        "always true condition","always false condition","condition will always be true","condition will always be false"]
}


def filter_ai_results(ai_result, static_results):

    # collect static rule types
    static_rules = set()

    for category in ["critical", "high", "medium", "low"]:
        for bug in static_results.get(category, []):
            static_rules.add(bug.get("rule"))

    filtered_bugs = []

    for bug in ai_result.get("logical_bugs", []):

        issue = bug.get("issue", "").lower()

        duplicate = False

        for rule, keywords in BUG_KEYWORDS.items():

            if rule in static_rules:

                for keyword in keywords:
                    if keyword in issue:
                        duplicate = True
                        break

            if duplicate:
                break

        if not duplicate:
            filtered_bugs.append(bug)

    ai_result["logical_bugs"] = filtered_bugs

    return ai_result