import tkinter as tk
from tkinter import messagebox



class MyGUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Prototype-GUI")
        self.window.geometry("500x300")

        self.create_widgets()

    def create_widgets(self):
        # Opretter labels og button for temp
        self.label_temp = tk.Label(self.window, text="Temp-Måling:", font=('Arial', 14))
        self.label_temp.grid(row=0, column=0, padx=10, pady=5)

        self.button_temp = tk.Button(self.window, text="Vis Temp-Måling", font=('Arial', 12), command=self.show_temp)
        self.button_temp.grid(row=0, column=1, padx=10, pady=5)

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
        self.button_boundaries_temp = tk.Button(self.frame_graf, text="Indtast grænseværdier for temperatur:", font=('Arial', 12), bg="lightblue", fg="black", command=self.show_boundaries_temp)
        self.button_boundaries_temp.pack(padx=10, pady=5)

        self.button_boundaries_puls = tk.Button(self.frame_graf, text="Indtast grænseværdier for puls:", font=('Arial', 12), bg="lightblue", fg="black", command=self.show_boundaries_puls)
        self.button_boundaries_puls.pack(padx=10, pady=5)

    def show_boundaries_temp(self):
        # Opret et nyt toplevel-vindue for grænseværdier
        new_window = tk.Toplevel(self.window)
        new_window.title("Grænseværdier")

        # Opretter en label til at vise beskeden
        label = tk.Label(new_window, text="Indtast grænseværdier her for temperatur!", font=('Arial', 12))
        label.pack(padx=10, pady=5)

    def show_boundaries_puls(self):
        # Opret et nyt toplevel-vindue for grænseværdier
        new_window = tk.Toplevel(self.window)
        new_window.title("Grænseværdier")

        # Opretter en label til at vise beskeden
        label = tk.Label(new_window, text="Indtast grænseværdier her for puls!", font=('Arial', 12))
        label.pack(padx=10, pady=5)

    def show_temp(self):


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