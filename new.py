import tkinter as tk
from tkinter import messagebox, simpledialog
import serial
import queue
import threading
import matplotlib.pyplot as plt
import random
import sqlite3

class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect("pulstemp1.db")
        self.cursor = self.connection.cursor()

    def create_tables(self):
        # Create a table for temperature data
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS TemperatureData (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    temperature REAL,
                                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )''')

        # Create a table for pulse data
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS PulseData (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    pulse REAL,
                                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )''')

        self.connection.commit()

    def insert_temperature_data(self, temperature):
        try:
            self.cursor.execute('''INSERT INTO TemperatureData (temperature) VALUES (?)''', (temperature,))
            self.connection.commit()
        except sqlite3.Error as e:
            print("Fejl ved indsættelse af temperaturdata:", e)

    def insert_pulse_data(self, pulse):
        try:
            self.cursor.execute('''INSERT INTO PulseData (pulse) VALUES (?)''', (pulse,))
            self.connection.commit()
        except sqlite3.Error as e:
            print("Fejl ved indsættelse af pulsdata:", e)

    def close(self):
        self.connection.close()


class Pulsmaaling():
    def __init__(self, start_Puls, Puls_min, Puls_max, Puls_delta):
        self.start_Puls = start_Puls
        self.Puls_min = Puls_min
        self.Puls_max = Puls_max
        self.Puls_delta = Puls_delta
        self.puls_data = []
        self.puls_queue = queue.Queue()
        self.pulse_thresholds = {'low': None, 'high': None}


    def getPuls(self):
        c = round(random.randint(-self.Puls_delta, self.Puls_delta), 2)
        self.start_Puls += c
        if self.start_Puls < self.Puls_min:
            self.start_Puls = self.Puls_min
        elif self.start_Puls > self.Puls_max:
            self.start_Puls = self.Puls_max

        pulse = round(self.start_Puls, 2)
        self.puls_data.append(pulse)  # Tilføjelse: Opdater puls_data-listen
        return pulse
    def get_pulse_thresholds(self):
        return self.pulse_thresholds  # Opdateret linje
    def set_pulse_thresholds(self, low, high):
        self.pulse_thresholds['low'] = low
        self.pulse_thresholds['high'] = high
class TemperatureSensor:
    def __init__(self, port):
        self.port = port
        self.temperature_data = []
        self.temperature_queue = queue.Queue()
        self.reading_thread = threading.Thread(target=self._read_temperature, daemon=True)
        self.reading_thread.start()
        self.temperature_thresholds = {'low': None, 'high': None}
        self.pulse_thresholds = {'low': None, 'high': None}


    def _read_temperature(self):
        while True:
            try:
                with serial.Serial(self.port, 9600, timeout=1) as ser:
                    while True:
                        temperature_reading = ser.readline().decode('utf-8').strip()
                        if temperature_reading:
                            temperature_value = temperature_reading.strip('+').rstrip('C')
                            self.temperature_queue.put(float(temperature_value))
            except serial.SerialException as e:
                messagebox.showerror("Error", f"Serial port error: {e}")

    def get_latest_temperature(self):
        if not self.temperature_queue.empty():
            return self.temperature_queue.get()
        return None

    def set_temperature_thresholds(self, low, high):
        self.temperature_thresholds['low'] = low
        self.temperature_thresholds['high'] = high


    def get_temperature_thresholds(self):
        return self.temperature_thresholds

class MyGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Prototype-GUI")
        self.window.geometry("500x300")

        self.database_manager = DatabaseManager()
        self.database_manager.create_tables()
        # Temp port ændres her
        self.temperature_sensor = TemperatureSensor('/dev/cu.usbserial-110')
        self.puls_maaling = Pulsmaaling(start_Puls=70, Puls_min=60, Puls_max=100, Puls_delta=5)

        self.create_widgets()
        self.update_temperature()
        self.update_pulse()  # Tilføjelse: Start opdatering af puls
        self.temperature_thresholds = {'low': None, 'high': None}
        self.pulse_thresholds = {'low': None, 'high': None}



    def create_widgets(self):
        self.label_temp = tk.Label(self.window, text="Temp-Måling:", font=('Arial', 14))
        self.label_temp.grid(row=0, column=0, padx=10, pady=5)

        self.label_temperature_value = tk.Label(self.window, text="", font=('Arial', 14))
        self.label_temperature_value.grid(row=0, column=1, padx=10, pady=5)

        self.label_puls = tk.Label(self.window, text="Puls-Måling:", font=('Arial', 14))
        self.label_puls.grid(row=1, column=0, padx=10, pady=5)

        self.label_puls_value = tk.Label(self.window, text="", font=('Arial', 14))
        self.label_puls_value.grid(row=1, column=1, padx=10, pady=5)

        self.label_graf = tk.Label(self.window, text="Opstilling-graf:", font=('Arial', 14))
        self.label_graf.grid(row=2, column=0, padx=10, pady=5)

        self.button_graf = tk.Button(self.window, text="Vis Temp-graf", font=('Arial', 12), command=self.show_temp_graf)
        self.button_graf.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        self.button_graf_puls = tk.Button(self.window, text="Vis Puls-graf", font=('Arial', 12), command=self.show_puls_graf)
        self.button_graf_puls.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        self.frame_graf = tk.Frame(self.window)
        self.frame_graf.grid(row=4, column=0, columnspan=2)
        self.frame_graf.grid_remove()

        self.button_boundaries_temp = tk.Button(self.frame_graf, text="Indtast grænseværdier for temperatur:", font=('Arial', 12), bg="lightblue", fg="black", command=self.set_temp_thresholds)
        self.button_boundaries_temp.pack(padx=10, pady=5)

        self.button_boundaries_puls = tk.Button(self.frame_graf, text="Indtast grænseværdier for puls:", font=('Arial', 12), bg="lightblue", fg="black", command=self.set_pulse_thresholds)
        self.button_boundaries_puls.pack(padx=10, pady=5)

    def show_puls(self):
        try:
            pulse = self.puls_maaling.getPuls()
            self.label_puls_value.config(text=f"{pulse} BPM")

            # Insert pulse data into the database
            self.database_manager.insert_pulse_data(pulse)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error occurred while inserting pulse data: {e}")

    def update_pulse(self):
        self.show_puls()
        self.window.after(1000, self.update_pulse)  # Opdater hvert sekund

    def set_temp_thresholds(self):
        # Indtastning af grænseværdier for temperatur
        low_temp = simpledialog.askfloat("Grænseværdier for temperatur", "Indtast den lave grænseværdi for temperatur:")
        high_temp = simpledialog.askfloat("Grænseværdier for temperatur", "Indtast den høje grænseværdi for temperatur:")
        if low_temp < 36:
            messagebox.showwarning("Advarsel", "Temperaturen er under 36°C, hvilket er unormalt lavt!")
        if high_temp > 39:
            messagebox.showwarning("Advarsel", "Temperaturen overstiger 39°C, hvilket er unormalt højt!")

        self.temperature_sensor.set_temperature_thresholds(low_temp, high_temp)
        messagebox.showinfo("Grænseværdier for temperatur", f"Grænseværdier for temperatur er blevet indstillet:\nLav: {low_temp}\nHøj: {high_temp}\n")

    def set_pulse_thresholds(self):
        # Indtastning af grænseværdier for puls
        low_pulse = simpledialog.askfloat("Grænseværdier for puls", "Indtast den lave grænseværdi for puls:")
        high_pulse = simpledialog.askfloat("Grænseværdier for puls", "Indtast den høje grænseværdi for puls:")

        if low_pulse < 50:
            messagebox.showwarning("Advarsel",
                                   "Hvilepulsen er under 50 BPM, hvilket er unormalt lavt!")
        if high_pulse > 100:
            messagebox.showwarning("Advarsel", "Hvilepulsen er over 100 BPM, hvilket er unormalt højt!")


        self.temperature_sensor.set_pulse_thresholds(low_pulse, high_pulse)
        messagebox.showinfo("Grænseværdier for puls", f"Grænseværdier for puls er blevet indstillet:\nLav: {low_pulse}\nHøj: {high_pulse}\n")


    def update_temperature(self):
        temperature = self.temperature_sensor.get_latest_temperature()
        if temperature is not None:
            self.label_temperature_value.config(text=f"{temperature} °C")
            self.temperature_sensor.temperature_data.append(temperature)
            self.database_manager.insert_temperature_data(temperature)
            thresholds = self.temperature_sensor.get_temperature_thresholds()
            if thresholds['low'] is not None and temperature < thresholds['low']:
                messagebox.showwarning("Advarsel", f"Temperaturen er under den lave grænseværdi: {thresholds['low']} °C")
            if thresholds['high'] is not None and temperature > thresholds['high']:
                messagebox.showwarning("Advarsel", f"Temperaturen er over den høje grænseværdi: {thresholds['high']} °C")
        self.window.after(1000, self.update_temperature)

    def show_temp_graf(self):
        if self.frame_graf.winfo_ismapped():
            self.frame_graf.grid_remove()
        else:
            self.frame_graf.grid()
            self.plot_temperature_graph()
        self.window.update_idletasks()

    def show_puls_graf(self):
        if self.frame_graf.winfo_ismapped():
            self.frame_graf.grid_remove()
        else:
            self.frame_graf.grid()
            self.plot_pulse_graph()
        self.window.update_idletasks()

    def plot_temperature_graph(self):
        thresholds = self.temperature_sensor.get_temperature_thresholds()
        plt.figure(figsize=(8, 6))
        plt.plot(self.temperature_sensor.temperature_data, marker='o', linestyle='-')
        plt.title('Temperature Over Time')
        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.grid(True)
        if thresholds['low'] is not None:
            plt.axhline(y=thresholds['low'], color='r', linestyle='--', label=f'Low Threshold: {thresholds["low"]} °C')
        if thresholds['high'] is not None:
            plt.axhline(y=thresholds['high'], color='g', linestyle='--', label=f'High Threshold: {thresholds["high"]} °C')
        plt.legend()
        plt.show()

    def plot_pulse_graph(self):
        thresholds = self.puls_maaling.get_pulse_thresholds()  # Opdateret linje
        plt.figure(figsize=(8, 6))
        plt.plot(self.puls_maaling.puls_data, marker='o', linestyle='-')
        plt.title('Pulse Over Time')
        plt.xlabel('Time')
        plt.ylabel('Pulse (BPM)')
        plt.grid(True)
        if thresholds['low'] is not None:
            plt.axhline(y=thresholds['low'], color='r', linestyle='--', label=f'Low Threshold: {thresholds["low"]} BPM')
        if thresholds['high'] is not None:
            plt.axhline(y=thresholds['high'], color='g', linestyle='--',
                        label=f'High Threshold: {thresholds["high"]} BPM')
        plt.legend()
        plt.show()


    def mainloop(self):
        self.window.mainloop()

MyGUI().mainloop()

