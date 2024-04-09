import tkinter as tk
from tkinter import messagebox
import serial
import queue
import threading

class TemperatureSensor:
    def __init__(self, port):
        # Initialiserer klassen med den angivne port og opretter en tom liste til temperaturdata
        self.port = port
        self.temperature_data = []

        # Opretter en kø til at gemme temperaturmålinger
        self.temperature_queue = queue.Queue()

        # Opretter en tråd til at læse temperaturdata fra sensoren i baggrunden
        self.reading_thread = threading.Thread(target=self._read_temperature, daemon=True)
        self.reading_thread.start()  # Starter tråden

        # Initialiserer grænseværdier fro temperatur og puls
        self.temperature_thresholds = {'low': None, 'high': None}
        self.pulse_thresholds = {'low': None, 'high': None}


    # Metode til at læse temperaturdata fra sensoren og gemme dem i køen
    def _read_temperature(self):
        while True:
            try:
                # Åbner seriel forbindelse til sensoren
                with serial.Serial(self.port, 9600, timeout=1) as ser:
                    while True:
                        # Læser en linje fra sensoren og dekoder den fra bytes til streng
                        temperature_reading = ser.readline().decode('utf-8').strip()
                        # Kontrollerer om strengen er tom, hvis ikke, konverterer den til float
                        if temperature_reading:
                            temperature_value = temperature_reading.strip('+').rstrip('C')
                            self.temperature_queue.put(float(temperature_value))
            except serial.SerialException as e:
                # Viser en fejlmeddelelse, hvis der opstår en fejl med seriel forbindelse
                messagebox.showerror("Error", f"Serial port error: {e}")

    # Metode til at hente den seneste temperaturmåling fra køen
    def get_latest_temperature(self):
        if not self.temperature_queue.empty():
            # Hvis køen ikke er tom, hentes og returneres den seneste temperaturmåling
            return self.temperature_queue.get()
        return None  # Returnerer None, hvis køen er tom

    # Metode til at indstille grænseværdier for temperatur
    def set_temperature_thresholds(self, low, high):
        self.temperature_thresholds['low'] = low
        self.temperature_thresholds['high'] = high

    # Metode til at indstille grænseværdier for puls
    def set_pulse_thresholds(self, low, high):
        self.pulse_thresholds['low'] = low
        self.pulse_thresholds['high'] = high

    # Metode til at hente grænseværdier for temperatur
    def get_temperature_thresholds(self):
        return self.temperature_thresholds


class MyGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Prototype-GUI")
        self.window.geometry("500x300")

        self.temperature_sensor = TemperatureSensor('COM3')

        self.create_widgets()
        self.update_temperature()  # Start opdatering af temperaturen

    def create_widgets(self):
        # Opretter labels for temp
        self.label_temp = tk.Label(self.window, text="Temp-Måling:", font=('Arial', 14))
        self.label_temp.grid(row=0, column=0, padx=10, pady=5)

        # Opretter label til at vise temperaturen
        self.label_temperature_value = tk.Label(self.window, text="", font=('Arial', 14))
        self.label_temperature_value.grid(row=0, column=1, padx=10, pady=5)

        # Opretter labels og button for puls
        self.label_puls = tk.Label(self.window, text="Puls-Måling:", font=('Arial', 14))
        self.label_puls.grid(row=1, column=0, padx=10, pady=5)

        self.button_puls = tk.Button(self.window, text="Vis Puls-Måling", font=('Arial', 12))
        self.button_puls.grid(row=1, column=1, padx=10, pady=5)

        # Labels og button for graf
        self.label_graf = tk.Label(self.window, text="Opstilling-graf:", font=('Arial', 14))
        self.label_graf.grid(row=2, column=0, padx=10, pady=5)

        self.button_graf = tk.Button(self.window, text="Vis Opstilling-graf", font=('Arial', 12), command=self.show_graf)
        self.button_graf.grid(row=2, column=1, padx=10, pady=5)

        # Knap til at udskrive data
        self.button_data = tk.Button(self.window, text="Print Data", font=('Arial', 12), command=self.print_data)
        self.button_data.grid(row=5, column=1, padx=10, pady=10, sticky=tk.SE)

        # Når man trykker på graf opstilling er der en ramme
        self.frame_graf = tk.Frame(self.window)
        self.frame_graf.grid(row=4, column=0, columnspan=2)
        self.frame_graf.grid_remove()

        # Nedenstående oprettes grænseværdier (kritisk høj/lav og normal) MÅSKE ændre til at der popper en fane op
        self.button_boundaries_temp = tk.Button(self.frame_graf, text="Indtast grænseværdier for temperatur:", font=('Arial', 12), bg="lightblue", fg="black", command=self.set_temp_thresholds)
        self.button_boundaries_temp.pack(padx=10, pady=5)

        self.button_boundaries_puls = tk.Button(self.frame_graf, text="Indtast grænseværdier for puls:", font=('Arial', 12), bg="lightblue", fg="black", command=self.set_pulse_thresholds)
        self.button_boundaries_puls.pack(padx=10, pady=5)

     def set_temp_thresholds(self):
            # Indtastning af grænseværdier for temperatur
            low_temp = simpledialog.askfloat("Grænseværdier for temperatur", "Indtast den lave grænseværdi for temperatur:")
            high_temp = simpledialog.askfloat("Grænseværdier for temperatur", "Indtast den høje grænseværdi for temperatur:")
            self.temperature_sensor.set_temperature_thresholds(low_temp, high_temp)
            messagebox.showinfo("Grænseværdier for temperatur", f"Grænseværdier for temperatur er blevet indstillet:\nLav: {low_temp}\nHøj: {high_temp}\n")



    def show_boundaries_puls(self):
        # Opret et nyt toplevel-vindue for grænseværdier
        new_window = tk.Toplevel(self.window)
        new_window.title("Grænseværdier")

        # Opretter en label til at vise beskeden
        label = tk.Label(new_window, text="Indtast grænseværdier her for puls!", font=('Arial', 12))
        label.pack(padx=10, pady=5)

    def update_temperature(self):
        # Opdaterer temperaturen
        temperature = self.temperature_sensor.get_latest_temperature()
        if temperature is not None:
            # Opdaterer label med den seneste temperaturmåling
            self.label_temperature_value.config(text=f"{temperature} °C")
        self.window.after(1000, self.update_temperature)  # Kalder metoden igen efter 1 sekund for at opdatere temperaturen kontinuerligt

    def show_graf(self):
        if self.frame_graf.winfo_ismapped():
            self.frame_graf.grid_remove()
        else:
            self.frame_graf.grid()
        self.window.update_idletasks()

    def print_data(self):
        messagebox.showinfo("Data", "Dette er dataen du ønsker at vise.")

    def mainloop(self):
        self.window.mainloop()

# Start programmet
MyGUI().mainloop()
