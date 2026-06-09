import requests
import json
import os


class TelegramAlert:
    def __init__(self):
        self.token = ""
        self.chat_id = ""
        self._load_config()

    def _load_config(self):
        # Go up one directory to find config.json in the root folder
        config_path = "../config.json"

        if not os.path.exists(config_path):
            print(f"[!] Warning: {config_path} not found. Telegram alerts are disabled.")
            return

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.token = config.get("telegram_token", "")
                self.chat_id = config.get("telegram_chat_id", "")
        except Exception as e:
            print(f"[-] Error parsing config.json: {e}")

    def send_alert(self, message):
        if not self.token or not self.chat_id:
            print("[!] Cannot send alert: Missing Telegram credentials in config.json.")
            return False

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            # Short timeout so it doesn't freeze the main program if internet is down
            response = requests.post(url, json=payload, timeout=5)

            if response.status_code == 200:
                print("[+] Real-time Telegram alert delivered successfully.")
                return True
            else:
                print(f"[-] Failed to send Telegram alert. HTTP Status: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"[-] Network connection error while sending alert: {e}")
            return False


if __name__ == "__main__":
    print("[*] Testing Telegram API connection...")
    bot = TelegramAlert()

    test_msg = "🚨 *PANIC-TRAP TEST ALERT* 🚨\nIf you are reading this on your phone, the API integration is fully operational!"
    bot.send_alert(test_msg)