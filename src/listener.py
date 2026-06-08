import time
import json
import os
from pynput import keyboard


class KeystrokeLogger:
    def __init__(self):
        self.key_press_times = {}
        self.typing_data = []
        self.last_release_time = None
        self.log_dir = "../logs"

    def on_press(self, key):
        try:
            char = key.char
        except AttributeError:
            char = str(key)

        self.key_press_times[char] = time.time()

    def on_release(self, key):
        try:
            char = key.char
        except AttributeError:
            char = str(key)

        if char in self.key_press_times:
            press_time = self.key_press_times.pop(char)
            release_time = time.time()
            dwell_time = release_time - press_time

            flight_time = 0
            if self.last_release_time:
                flight_time = press_time - self.last_release_time

            self.last_release_time = release_time

            self.typing_data.append({
                'key': char,
                'dwell_time': round(dwell_time, 4),
                'flight_time': round(flight_time, 4)
            })

        if key == keyboard.Key.esc:
            print("\n[!] ESC pressed. Saving data and stopping listener...")
            self.save_data()
            return False

    def save_data(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        file_path = os.path.join(self.log_dir, 'raw_keystrokes.json')
        with open(file_path, 'w', encoding="utf-8") as f:
            json.dump(self.typing_data, f, indent=4, ensure_ascii=False)
        print(f"[+] Successfully saved {len(self.typing_data)} keystrokes to {file_path}")


if __name__ == '__main__':
    print("[*] Listener started. Type something to test.")
    print("[*] Press ESC to stop the listener and generate the log file.")

    logger = KeystrokeLogger()

    with keyboard.Listener(on_press=logger.on_press, on_release=logger.on_release) as listener:
        listener.join()