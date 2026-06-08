import os
import json
import pygetwindow as gw
import pyperclip
from datetime import datetime


class RiskManager:
    def __init__(self):
        self.current_risk = 0.0
        self.profile_path = "../logs/base_profile.json"
        self.recon_file = "../logs/recon.log"
        self.profile = self._load_profile()

    def _load_profile(self):
        if os.path.exists(self.profile_path):
            try:
                with open(self.profile_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[-] Error loading profile: {e}")
                return {}
        return {}

    def _update_risk(self, amount):
        self.current_risk += amount

        # Keep risk bounded between 0 and 100
        if self.current_risk < 0.0:
            self.current_risk = 0.0
        elif self.current_risk > 100.0:
            self.current_risk = 100.0

        print(f"[*] Current Risk Score: {round(self.current_risk, 1)}")
        self.check_thresholds()

    def evaluate_bi_gram(self, bi_gram, flight_time):
        # True biometric rhythm happens under 400ms.
        if flight_time > 0.4:
            return

        # Neutral stance on newly introduced words
        if bi_gram not in self.profile:
            self._update_risk(0.1)
            return

        stats = self.profile[bi_gram]
        mean = stats['mean']
        std = stats['std']

        std_floor = 0.05
        effective_std = max(std, std_floor)

        deviation = abs(flight_time - mean)

        if deviation <= (2.5 * effective_std):
            self._update_risk(-1.5)
        else:
            penalty = (deviation / effective_std) * 0.3

            max_penalty = 2.5
            if penalty > max_penalty:
                penalty = max_penalty

            self._update_risk(penalty)

    def check_thresholds(self):
        # 75 and 90 thresholds are handled dynamically in main.py
        # Here we only trigger the silent background recon at 50
        if self.current_risk >= 50:
            print("[!] RISK > 50: SUSPICIOUS ACTIVITY. SILENT RECON STARTED.")
            self.silent_recon()

    def silent_recon(self):
        # Gather intelligence on the intruder silently
        try:
            active_window = gw.getActiveWindow()
            window_title = active_window.title if active_window else "Unknown Window"

            try:
                clipboard_content = pyperclip.paste()
                # Don't save a massive copied image or text wall, truncate it safely
                if len(clipboard_content) > 50:
                    clipboard_content = clipboard_content[:50] + "... (truncated)"
            except Exception:
                clipboard_content = "Could not read clipboard"

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"[{timestamp}] Window: {window_title} | Clipboard: {clipboard_content}\n"

            # Ensure logs directory exists before writing
            if not os.path.exists("../logs"):
                os.makedirs("../logs")

            with open(self.recon_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)

        except Exception as e:
            print(f"[-] Recon failed: {e}")