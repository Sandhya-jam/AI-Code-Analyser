BUG_KEYWORDS = {
    "DIVISION_BY_ZERO": ["division by zero", "divide by zero"],
    "UNUSED_VARIABLE": ["unused variable"],
    "REDUNDANT_ASSIGNMENT": ["redundant assignment"],
    "DUPLICATE_CONDITION": ["duplicate condition"],
    "SHADOWED_VARIABLE": ["shadowed variable"],
    "UNREACHABLE_CODE": ["unreachable code"],
    "INDEX_OUT_OF_BOUNDS": ["index out of bounds","index out of range"]
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