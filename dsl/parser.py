import re

ALLOWED_ACTIONS = {"HOVER", "STOP", "RETURN_HOME", "ABORT"}

class BehaviorLanguageError(Exception):
    def __init__(self, message, line=None, rule=None):
        self.message = message
        self.line = line
        self.rule = rule
        super().__init__(message)

def validate_ir(ir):
    if "name" not in ir:
        raise BehaviorLanguageError("Missing RULE declaration")

    if "event" not in ir:
        raise BehaviorLanguageError("Missing WHEN event", rule=ir.get("name"))

    if "action" not in ir:
        raise BehaviorLanguageError("Missing DO action", rule=ir.get("name"))

    if ir["action"] not in ALLOWED_ACTIONS:
        raise BehaviorLanguageError(
            f"Action '{ir['action']}' is forbidden",
            line=f"DO {ir['action']}",
            rule=ir.get("name")
        )

def compile_rule(rule_text):
    lines = [l.strip() for l in rule_text.strip().splitlines()]
    ir = {}

    for line in lines:
        if line.startswith("RULE"):
            ir["name"] = line.split()[1]

        elif line.startswith("WHEN"):
            ir["event"] = line.split()[1]

        elif line.startswith("IF"):
            m = re.match(r"IF (\w+)\s*([><=!]+)\s*([\d.]+)", line)
            if not m:
                raise BehaviorLanguageError("Invalid IF syntax", line=line)
            ir["condition"] = {
                "signal": m.group(1),
                "operator": m.group(2),
                "value": float(m.group(3))
            }

        elif line.startswith("DO"):
            ir["action"] = line.split()[1]

        else:
            raise BehaviorLanguageError("Unknown statement", line=line)

    validate_ir(ir)
    return ir
