# adapter/command_adapter.py

import time

# ---------- REAL ADAPTER (placeholder for MAVLink later) ----------

def get_adapter_status():
    """
    REAL hardware status only.
    No demos, no auto-connect.
    """
    return {
        "connected": False,   # ← stays False unless real drone code added
        "port": None,
        "mode": "REAL"
    }


def send_command(action):
    """
    REAL drone command (currently blocked)
    """
    print(f"[REAL ADAPTER] BLOCKED → {action}")
    return f"REAL:{action}"


# ---------- SIMULATOR ADAPTER ----------

def send_simulated_command(action):
    """
    Simulator-only command
    """
    print(f"[SIM ADAPTER] → {action}")
    return f"SIM:{action}"
