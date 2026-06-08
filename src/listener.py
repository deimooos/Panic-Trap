import time
import json
import os
from pynput import keyboard


class KeystrokeLogger:
    def __init__(self):
        self.typing_data = []
        self.last_press_time = None
        self.log_dir = "../logs"
        self.active_keys = set()  # To prevent Windows held-key auto-repeat spam

    def on_press(self, key):
        try:
            char = key.char
        except AttributeError:
            char = str(key).replace('Key.', '')

        # Ignore if key is being held down (auto-repeat)
        if char in self.active_keys:
            return

        self.active_keys.add(char)
        current_time = time.time()

        # Calculate chronological Press-to-Press (P2P) flight time
        flight_time = 0.0
        if self.last_press_time is not None:
            flight_time = current_time - self.last_press_time

        self.last_press_time = current_time

        # Append exactly when pressed to preserve TRUE chronological typing order!
        self.typing_data.append({
            'key': char,
            'flight_time': round(flight_time, 4)
        })

    def on_release(self, key):
        try:
            char = key.char
        except AttributeError:
            char = str(key).replace('Key.', '')

        # Remove key from active list when actually released
        if char in self.active_keys:
            self.active_keys.remove(char)

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