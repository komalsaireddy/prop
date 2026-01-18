from ai.signals import get_ai_signal

def get_intent_from_ir(ir):
    """
    Generate behavior intent from compiled IR and AI signals.

    RETURNS (intent, ai_signal)
    This contract MUST NOT change.
    """

    # 1. Get AI signal (simulated, source-agnostic)
    ai_signal = get_ai_signal()

    print("AI Signal:", ai_signal)
    print("Using IR:", ir)

    # 2. Event mismatch → no intent
    if ai_signal.get("event") != ir.get("event"):
        return "STOP", ai_signal

    # 3. Evaluate condition (if present)
    condition = ir.get("condition")

    if condition:
        signal_name = condition["signal"]
        operator = condition["operator"]
        threshold = condition["value"]

        signal_value = ai_signal.get(signal_name)

        # Missing signal → safe default
        if signal_value is None:
            return "STOP", ai_signal

        if operator == ">" and not (signal_value > threshold):
            return "STOP", ai_signal

        if operator == "<" and not (signal_value < threshold):
            return "STOP", ai_signal

        if operator == ">=" and not (signal_value >= threshold):
            return "STOP", ai_signal

        if operator == "<=" and not (signal_value <= threshold):
            return "STOP", ai_signal

        if operator == "==" and not (signal_value == threshold):
            return "STOP", ai_signal

    # 4. Condition passed → return declared intent
    return ir["action"], ai_signal
