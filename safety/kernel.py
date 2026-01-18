def evaluate(intent, context):
    if intent == "ABORT":
        return "FORCED", "ABORT", "Manual abort"

    if context["battery"] is None:
        return "WAIT", "HOVER", "Waiting for real battery data"

    return "ALLOW", intent, "All checks passed"
