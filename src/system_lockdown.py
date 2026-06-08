import os
import platform
import time


class LockdownManager:
    def __init__(self):
        self.os_type = platform.system()

    def isolate_network(self):
        print("[!!!] INITIATING NETWORK ISOLATION...")
        if self.os_type == "Windows":
            # Quick and elegant hack to drop IP address without needing Admin rights
            # Effectively kills internet access instantly to prevent data exfiltration
            os.system("ipconfig /release > nul")
            print("[-] Network connection dropped (IP released).")
        else:
            print("[-] Network kill not implemented for non-Windows OS yet.")

    def lock_workstation(self):
        print("[!!!] INITIATING WORKSTATION LOCK...")
        if self.os_type == "Windows":
            import ctypes
            # Direct call to Windows API to lock the screen instantly
            ctypes.windll.user32.LockWorkStation()
            print("[-] Workstation locked.")
        else:
            print("[-] Screen lock not implemented for non-Windows OS yet.")

    def trigger_nuke(self):
        print("\n" + "=" * 50)
        print("[X] RISK LEVEL 90 REACHED: EXECUTING NUCLEAR OPTION")
        print("=" * 50)

        self.isolate_network()

        # Give the system 1 second to drop the network before locking the screen
        time.sleep(1)

        self.lock_workstation()


if __name__ == "__main__":
    print("[*] Lockdown Manager initialized.")
    # WARNING: Uncommenting the code below will immediately cut your internet and lock your PC!

    nuke = LockdownManager()
    nuke.trigger_nuke()

    print("[*] Test execution is commented out for safety. Remove the # symbols to test.")