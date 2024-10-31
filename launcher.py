import tkinter as tk
import subprocess
import os
import signal

class LauncherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Launcher")

        self.first_process = None
        self.second_process = None

        self.start_first_button = tk.Button(self, text="Start First", command=self.start_first)
        self.start_first_button.pack()

        self.stop_first_button = tk.Button(self, text="Stop First", command=self.stop_first)
        self.stop_first_button.pack()

        self.start_second_button = tk.Button(self, text="Start Second", command=self.start_second)
        self.start_second_button.pack()

        self.stop_second_button = tk.Button(self, text="Stop Second", command=self.stop_second)
        self.stop_second_button.pack()

    def start_first(self):
        if self.first_process is None:
            self.first_process = subprocess.Popen(["python", "first.py"])

    def stop_first(self):
        if self.first_process is not None:
            os.kill(self.first_process.pid, signal.SIGTERM)
            self.first_process = None

    def start_second(self):
        if self.second_process is None:
            self.second_process = subprocess.Popen(["python", "second.py"])

    def stop_second(self):
        if self.second_process is not None:
            os.kill(self.second_process.pid, signal.SIGTERM)
            self.second_process = None

if __name__ == "__main__":
    app = LauncherApp()
    app.mainloop()