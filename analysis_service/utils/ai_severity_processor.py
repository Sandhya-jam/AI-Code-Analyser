def merge_ai_findings(ai_result, critical, high, medium, low):

    for bug in ai_result.get("logical_bugs", []):

        severity = bug.get("severity", "LOW").upper()

        formatted_bug = {
            "message": bug.get("issue"),
            "severity": severity,
            "rule": "AI_LOGICAL_ANALYSIS",
            "line": bug.get("line")
        }

        if severity == "CRITICAL":
            critical.append(formatted_bug)

        elif severity == "HIGH":
            high.append(formatted_bug)

        elif severity == "MEDIUM":
            medium.append(formatted_bug)

        else:
            low.append(formatted_bug)

    for sec in ai_result.get("security_issues", []):

        severity = sec.get("severity", "HIGH").upper()

        formatted_bug = {
            "message": sec.get("issue"),
            "severity": severity,
            "rule": "AI_SECURITY_ANALYSIS",
            "line": None
        }

        if severity == "CRITICAL":
            critical.append(formatted_bug)

        elif severity == "HIGH":
            high.append(formatted_bug)

        elif severity == "MEDIUM":
            medium.append(formatted_bug)

        else:
            low.append(formatted_bug)

    return critical, high, medium, low