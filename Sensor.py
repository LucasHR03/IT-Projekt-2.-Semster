import random
import time


class HealthMonitor:
    def __init__(self, name):
        self.name = name

    def measure(self):
        raise NotImplementedError("Subclasses must implement measure method")


class PulseMonitor(HealthMonitor):
    def __init__(self, name):
        super().__init__(name)
        self.current_pulse = 60  # Initial pulse rate

    def measure(self):
        while True:
            self.current_pulse += random.randint(-5, 5)  # Simulate slight variation
            self.current_pulse = max(40, min(self.current_pulse, 120))  # Bound pulse rate
            print(f"{self.name}'s pulse rate: {self.current_pulse} bpm")
            time.sleep(2)  # Delay for 2 seconds


# Example usage
if __name__ == "__main__":
    person_name = "John"

    pulse_monitor = PulseMonitor(person_name)
    pulse_monitor.measure()