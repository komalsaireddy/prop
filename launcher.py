"""
Single entry point for the Drone Platform.
This will become the final EXE.
"""

import subprocess
import time
from config import AUTO_START_FIRMWARE


def is_px4_running():
    try:
        result = subprocess.check_output(
            ["wsl", "pgrep", "px4"],
            stderr=subprocess.DEVNULL
        )
        return bool(result.strip())
    except subprocess.CalledProcessError:
        return False


def start_px4():
    if is_px4_running():
        print("[LAUNCHER] PX4 already running")
        return

    print("[LAUNCHER] Starting PX4 firmware...")

    subprocess.Popen(
        [
            "wsl",
            "bash",
            "-c",
            "cd ~/PX4-Autopilot && make px4_sitl_default none"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    time.sleep(6)

def stop_px4():
    print("[LAUNCHER] Stopping PX4 firmware...")
    subprocess.call(
        [
            "wsl",
            "bash",
            "-lc",
            "pkill -9 -f px4 || true"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )



def start_gui():
    from gui.app import GDBLCompilerGUI
    import tkinter as tk

    root = tk.Tk()

    def on_close():
        stop_px4()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    GDBLCompilerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    if AUTO_START_FIRMWARE:
        start_px4()

    start_gui()
