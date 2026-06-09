import time
import threading
from pynput import keyboard
from risk_manager import RiskManager
from telegram_alert import TelegramAlert
from system_lockdown import LockdownManager
from honeypot_ui import HoneypotUI

# Global variables for cross-thread communication
last_key_time = None
last_key = None
honeypot_triggered = False
nuke_triggered = False
honeypot_already_seen = False

# Initialize core modules
risk_engine = RiskManager()
telegram = TelegramAlert()
nuke = LockdownManager()


def on_press(key):
    global last_key_time, last_key, honeypot_triggered, nuke_triggered, honeypot_already_seen

    # Stop processing keystrokes if the system is already nuked
    if nuke_triggered:
        return

    if honeypot_triggered:
        return

    try:
        if hasattr(key, 'char') and key.char is not None:
            current_key = key.char.lower()
        else:
            current_key = str(key).replace('Key.', '')
    except Exception:
        return

    current_time = time.time()

    if last_key is not None and last_key_time is not None:
        flight_time = current_time - last_key_time

        # Filter out pauses longer than 1.5s (user drinking coffee, thinking, etc.)
        if flight_time < 1.5:
            bi_gram = f"{last_key}{current_key}"

            # Feed LIVE data to the Risk Engine
            risk_engine.evaluate_bi_gram(bi_gram, flight_time)

            # Check State Machine for 90 Threshold (Nuke)
            if risk_engine.current_risk >= 90 and not nuke_triggered:
                nuke_triggered = True
                msg = "🚨 *CRITICAL ALERT* 🚨\nRisk > 90! Nuclear option triggered. System locked and network isolated."
                telegram.send_alert(msg)
                nuke.trigger_nuke()

            # Check State Machine for 75 Threshold (Honeypot)
            elif risk_engine.current_risk >= 75 and not honeypot_already_seen:
                honeypot_triggered = True
                honeypot_already_seen = True
                msg = "⚠️ *WARNING* ⚠️\nRisk > 75! Suspicious typing detected. Honeypot UI deployed."
                telegram.send_alert(msg)

    last_key = current_key
    last_key_time = current_time


def keyboard_listener_thread():
    # Runs in the background, constantly feeding data to on_press
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("[*] PANIC-TRAP BEHAVIORAL BIOMETRICS ENGINE")
    print("[*] Initializing core modules...")
    print("=" * 50)

    if not risk_engine.profile:
        print("[!] FATAL: No baseline profile found. Run ngram_engine.py first to generate base_profile.json")
        exit(1)

    print("[+] Profile loaded. System ARMED and monitoring keystrokes.")
    print("[+] Try typing normally, then try typing erratically to spike the risk.")

    # Start the keylogger in a daemon thread so it runs silently in the background
    listener = threading.Thread(target=keyboard_listener_thread, daemon=True)
    listener.start()

    try:
        while True:
            # Main thread only cares about deploying UI when triggered
            if honeypot_triggered and not nuke_triggered:
                print("[!!!] Deploying Honeypot Interface in Main Thread...")

                app = HoneypotUI()
                app.mainloop()

                # Once closed via ESC, reactivate the listener
                honeypot_triggered = False
                print("\n[*] Developer exit triggered. Closing honeypot.")
                print(f"[*] Resuming monitoring. Current Risk Score: {round(risk_engine.current_risk, 1)}")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n[*] System shutting down safely. Goodbye.")