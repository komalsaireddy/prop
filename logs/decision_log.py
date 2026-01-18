import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "decision_log.txt")

def log_decision(intent, decision, action, reason):
    """
    Append a single, explainable decision record to disk.
    This function must NEVER crash the runtime.
    """

    try:
        # Ensure logs directory exists
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        entry = (
            f"[{timestamp}] "
            f"INTENT={intent} | "
            f"DECISION={decision} | "
            f"ACTION={action} | "
            f"REASON={reason}\n"
        )

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry)

    except Exception:
        # Logging must NEVER break execution
        pass
