import os
import sys

# venv Tkinter Bug Fix
os.environ['TCL_LIBRARY'] = r"C:\Users\deimos\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\deimos\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

import customtkinter as ctk
from datetime import datetime


class HoneypotUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.log_dir = "../logs"
        self.panic_log = os.path.join(self.log_dir, "intruder_panic.log")

        self.title("Critical System Alert")

        # Get screen size according to Tkinter's internal scaling
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Lock geometry to these exact internal dimensions
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # Strip borders and bypass taskbar
        self.overrideredirect(True)
        self.attributes('-topmost', True)

        self.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.bind("<Escape>", self.dev_exit)

        self.configure(fg_color="#0a0a0a")
        self._build_ui()

    def _build_ui(self):
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")

        # Dynamically center the frame in the calculated space
        self.center_frame.pack(expand=True)

        self.warning_lbl = ctk.CTkLabel(self.center_frame, text="UNAUTHORIZED ACCESS DETECTED",
                                        font=("Courier", 35, "bold"), text_color="red")
        self.warning_lbl.pack(pady=20)

        self.info_lbl = ctk.CTkLabel(self.center_frame,
                                     text="System locked due to abnormal typing behavior.\nPlease enter your 2FA PIN to verify identity:",
                                     font=("Courier", 18), text_color="white")
        self.info_lbl.pack(pady=10)

        self.pin_entry = ctk.CTkEntry(self.center_frame, font=("Courier", 24), show="*", width=250, height=40)
        self.pin_entry.pack(pady=20)
        self.pin_entry.bind("<Return>", self.log_panic_attempt)

        self.submit_btn = ctk.CTkButton(self.center_frame, text="VERIFY", command=self.log_panic_attempt,
                                        fg_color="darkred", hover_color="#ff0000", height=40)
        self.submit_btn.pack(pady=10)

    def disable_event(self):
        pass

    def dev_exit(self, event=None):
        print("[*] Developer exit triggered. Closing honeypot.")
        self.destroy()

    def log_panic_attempt(self, event=None):
        attempt = self.pin_entry.get()
        self.pin_entry.delete(0, 'end')

        if not attempt:
            return

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] Panic PIN Attempt: {attempt}\n"

        with open(self.panic_log, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        print(f"[-] Blocked panic attempt: '{attempt}'")
        self.info_lbl.configure(text="INVALID PIN. INCIDENT LOGGED AND REPORTED.", text_color="red")


if __name__ == "__main__":
    print("[*] Deploying Tamper-Proof Honeypot UI...")
    app = HoneypotUI()
    app.mainloop()