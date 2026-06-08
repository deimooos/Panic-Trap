import json
import os
import pygetwindow as gw
import pyperclip
from datetime import datetime


class RiskManager:
    def __init__(self):
        self.current_risk = 0.0
        self.log_dir = "../logs"
        self.recon_file = os.path.join(self.log_dir, "recon.log")

        # Load the profile to compare against
        self.profile = self.load_profile()

    def load_profile(self):
        profile_path = os.path.join(self.log_dir, 'base_profile.json')
        if not os.path.exists(profile_path):
            print("[!] Profile not found. Cannot start risk engine.")
            return {}

        with open(profile_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def evaluate_bi_gram(self, bi_gram, flight_time):
        # If the user types a completely unknown bi-gram, give a small penalty
        if bi_gram not in self.profile:
            self._update_risk(2.0)
            return

        stats = self.profile[bi_gram]
        mean = stats['mean']
        std = stats['std']

        # Calculate how many standard deviations away the input is
        deviation = abs(flight_time - mean)

        # If it's within 1.5 std devs, it's probably the real owner. Decrease risk.
        if deviation <= (2.5 * std):
            self._update_risk(-1.5)
        # If it's further away, increase risk proportionally.
        # Someone typing completely different will spike the score fast.
        else:
            penalty = (deviation / std) * 1.0
            self._update_risk(penalty)

    def _update_risk(self, amount):
        self.current_risk += amount

        # Keep risk bounded between 0 and 100
        if self.current_risk < 0:
            self.current_risk = 0.0
        elif self.current_risk > 100:
            self.current_risk = 100.0

        print(f"[*] Current Risk Score: {round(self.current_risk, 1)}")
        self.check_thresholds()

    def check_thresholds(self):
        # Cascading thresholds: If risk spikes to 100 instantly, do ALL of them.

        if self.current_risk >= 50:
            print("[!] RISK > 50: SUSPICIOUS ACTIVITY. SILENT RECON STARTED.")
            self.silent_recon()

        if self.current_risk >= 75:
            print("[!!] RISK > 75: HONEYPOT 2FA TRIGGERED!")
            # Will be implemented in Issue 3 & 4

        if self.current_risk >= 90:
            print("[!!!] RISK > 90: NUCLEAR OPTION TRIGGERED (Network Kill & Lock)!")
            # Will be implemented in Issue 5

    def silent_recon(self):
        # Gather intelligence on the intruder
        try:
            active_window = gw.getActiveWindow()
            window_title = active_window.title if active_window else "Unknown Window"

            try:
                clipboard_content = pyperclip.paste()
                # Don't save a massive copied image or text wall, truncate it
                if len(clipboard_content) > 50:
                    clipboard_content = clipboard_content[:50] + "... (truncated)"
            except Exception:
                clipboard_content = "Could not read clipboard"

            log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Window: {window_title} | Clipboard: {clipboard_content}\n"

            with open(self.recon_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)

        except Exception as e:
            print(f"[-] Recon failed: {e}")


# Fake a scenario to test the engine without typing
if __name__ == '__main__':
    print("[*] Testing Risk Engine thresholds...")
    rm = RiskManager()

    if rm.profile:
        # Get a random known bi-gram from the profile
        test_bi_gram = list(rm.profile.keys())[0]

        print("\n--- Simulating Intruder (Bad Flight Times) ---")
        for i in range(15):
            # Pass a terrible flight time (like 1 full second) to spike the risk
            rm.evaluate_bi_gram(test_bi_gram, 1.2)