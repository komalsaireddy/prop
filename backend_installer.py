import subprocess
import sys


def run(cmd, description, fatal=True):
    print(f"\n[SETUP] {description}")
    print(f"[CMD] {cmd}")

    result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        if fatal:
            print(f"\n[ERROR] Failed: {description}")
            sys.exit(1)
        else:
            return False

    return True


# -------------------------------
# WSL HANDLING
# -------------------------------

def wsl_exists():
    return run(
        "wsl --status",
        "Checking WSL availability",
        fatal=False
    )


def install_wsl():
    print("\n[INFO] WSL not found. Installing WSL + Ubuntu...")
    run(
        "wsl --install -d Ubuntu",
        "Installing WSL and Ubuntu"
    )
    print("\n[IMPORTANT] Reboot required.")
    print("Run this installer again after reboot.")
    sys.exit(0)


# -------------------------------
# PX4 HANDLING
# -------------------------------

def px4_exists():
    return run(
        "wsl test -d ~/PX4-Autopilot",
        "Checking PX4 firmware presence",
        fatal=False
    )


def install_px4():
    print("\n[INFO] PX4 not found. Cloning PX4 repository...")
    run(
        "wsl git clone https://github.com/PX4/PX4-Autopilot.git ~/PX4-Autopilot",
        "Cloning PX4 firmware"
    )


def install_px4_deps():
    print("\n[INFO] Installing PX4 dependencies (this may take time)...")
    run(
        'wsl bash -lc "cd ~/PX4-Autopilot && ./Tools/setup/ubuntu.sh"',
        "Installing PX4 dependencies"
    )


# -------------------------------
# MAIN ENTRY
# -------------------------------

def main():
    print("===================================")
    print(" Drone Platform Backend Setup")
    print("===================================")

    # Step 1: WSL
    if not wsl_exists():
        install_wsl()
    print("[OK] WSL detected")

    # Step 2: PX4 source
    if not px4_exists():
        install_px4()
    else:
        print("[OK] PX4 already installed")

    # Step 3: PX4 dependencies
    install_px4_deps()

    print("\n===================================")
    print(" Backend setup COMPLETE")
    print(" You can now run DronePlatform.exe")
    print("===================================")


if __name__ == "__main__":
    main()
