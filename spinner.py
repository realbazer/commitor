import sys
import threading
import time

class CLISpinner:
    def __init__(self, message: str = "Processing..."):
        self.message = message
        self.stop_event = threading.Event()
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.thread = threading.Thread(target=self._spin, daemon=True)

    def _spin(self):
        idx = 0
        while not self.stop_event.is_set():
            sys.stdout.write(f"\r\033[36m{self.frames[idx]}\033[0m {self.message}")
            sys.stdout.flush()
            idx = (idx + 1) % len(self.frames)
            time.sleep(0.08)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_event.set()
        self.thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 4) + "\r")
        sys.stdout.flush()
