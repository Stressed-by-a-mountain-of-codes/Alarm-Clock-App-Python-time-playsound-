import tkinter as tk
from tkinter import messagebox
import time
import threading
from playsound import playsound
from datetime import datetime, timedelta

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("⏰ Alarm Clock with Snooze")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.alarm_active = False
        self.snooze_time = None

        tk.Label(root, text="Set Alarm (24-hour format)", font=("Arial", 14)).pack(pady=10)

        form = tk.Frame(root)
        form.pack(pady=10)

        tk.Label(form, text="Hour").grid(row=0, column=0)
        tk.Label(form, text="Minute").grid(row=0, column=2)
        tk.Label(form, text="Second").grid(row=0, column=4)

        self.hour_entry = tk.Entry(form, width=5)
        self.hour_entry.grid(row=1, column=0, padx=5)

        tk.Label(form, text=":").grid(row=1, column=1)

        self.min_entry = tk.Entry(form, width=5)
        self.min_entry.grid(row=1, column=2, padx=5)

        tk.Label(form, text=":").grid(row=1, column=3)

        self.sec_entry = tk.Entry(form, width=5)
        self.sec_entry.grid(row=1, column=4, padx=5)

        tk.Button(root, text="Set Alarm", font=("Arial", 12), command=self.set_alarm).pack(pady=10)

        self.snooze_btn = tk.Button(root, text="😴 Snooze 5 min", font=("Arial", 10), command=self.activate_snooze, state="disabled")
        self.snooze_btn.pack(pady=5)

        self.status = tk.Label(root, text="", font=("Arial", 10))
        self.status.pack(pady=10)

    def set_alarm(self):
        h = self.hour_entry.get()
        m = self.min_entry.get()
        s = self.sec_entry.get()

        try:
            alarm_time_str = f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
            self.alarm_time = alarm_time_str
            self.alarm_active = True
            self.snooze_time = None
            self.status.config(text=f"Alarm set for {alarm_time_str}", fg="green")
            threading.Thread(target=self.alarm_checker, daemon=True).start()
        except:
            messagebox.showerror("Invalid Input", "Please enter valid numbers (HH MM SS)")

    def alarm_checker(self):
        while self.alarm_active:
            now = time.strftime("%H:%M:%S")
            if self.snooze_time:
                if datetime.now() >= self.snooze_time:
                    self.ring_alarm()
                    break
            elif now == self.alarm_time:
                self.ring_alarm()
                break
            time.sleep(1)

    def ring_alarm(self):
        self.alarm_active = False
        self.status.config(text="🔔 Alarm ringing!", fg="red")
        self.snooze_btn.config(state="normal")

        try:
            playsound("alarm.mp3")
        except Exception as e:
            messagebox.showerror("Sound Error", f"Could not play sound:\n{e}")

    def activate_snooze(self):
        self.snooze_time = datetime.now() + timedelta(minutes=5)
        self.alarm_active = True
        self.status.config(text=f"😴 Snoozed until {self.snooze_time.strftime('%H:%M:%S')}", fg="blue")
        self.snooze_btn.config(state="disabled")
        threading.Thread(target=self.alarm_checker, daemon=True).start()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    AlarmClock(root)
    root.mainloop()
