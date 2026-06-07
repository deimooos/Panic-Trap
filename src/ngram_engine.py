import json
import os
import numpy as np
from collections import defaultdict


class NGramModel:
    def __init__(self):
        self.bi_grams = defaultdict(list)
        self.baseline_profile = {}
        self.log_dir = "../logs"

    def load_raw_data(self, file_name="raw_keystrokes.json"):
        file_path = os.path.join(self.log_dir, file_name)
        if not os.path.exists(file_path):
            print(f"[!] Error: {file_path} not found. You need to run listener.py first.")
            return False

        # Added utf-8 encoding to prevent crashes with special chars
        with open(file_path, 'r', encoding='utf-8') as f:
            self.typing_data = json.load(f)
        return True

    def extract_bi_grams(self):
        # We need at least 2 keys to form a bi-gram
        if len(self.typing_data) < 2:
            print("[!] Not enough keystroke data to analyze.")
            return

        for i in range(len(self.typing_data) - 1):
            current_key = self.typing_data[i]['key']
            next_key = self.typing_data[i + 1]['key']

            flight_time = self.typing_data[i + 1]['flight_time']

            # Ignore pauses longer than 1.5s (probably stopped to think or sip coffee)
            if flight_time < 1.5:
                bi_gram_key = f"{current_key}{next_key}"
                self.bi_grams[bi_gram_key].append(flight_time)

    def build_profile(self):
        print("[*] Building N-Gram baseline profile...")

        for bi_gram, times in self.bi_grams.items():
            # We need at least 2 samples to calculate standard deviation properly
            if len(times) > 1:
                mean_time = np.mean(times)
                std_dev = np.std(times)

                # Smoothing: if std_dev is exactly 0, it will cause division by zero later
                # Just give it a tiny tolerance hack
                if std_dev == 0.0:
                    std_dev = 0.01

                self.baseline_profile[bi_gram] = {
                    'mean': round(float(mean_time), 4),
                    'std': round(float(std_dev), 4),
                    'samples': len(times)
                }

        self._save_profile()

    def _save_profile(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        profile_path = os.path.join(self.log_dir, 'base_profile.json')
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(self.baseline_profile, f, indent=4)

        print(f"[+] Profile successfully generated! Total unique bi-grams: {len(self.baseline_profile)}")
        print(f"[+] Saved to: {profile_path}")


if __name__ == '__main__':
    engine = NGramModel()
    if engine.load_raw_data():
        engine.extract_bi_grams()
        engine.build_profile()