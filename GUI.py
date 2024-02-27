import tkinter as tk


class MyGUI:

    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Prototype-GUI")
        self.window.geometry("500x500")
        self.create_widgets()

        self.combobox_value = tk.StringVar()

    def create_widgets(self):
        # Ved ikke om der er behov for labels
        self.label_temp = tk.Label(self.window, text="Temp-Målng:", font= ('Arial', 17))
        self.label_temp.grid(row=0, column=0,  sticky=tk.W, pady=10)

        self.button_temp = tk.Button(self.window, text="Vis_Temp-Måling", font=('Arial', 17))
        self.button_temp.grid(row=0, column=1)

        self.label_puls = tk.Label(self.window, text="Puls-Måling:", font=('Arial', 17))
        self.label_puls.grid(row=1, column=0, sticky=tk.W, pady=10)

        self.button_puls = tk.Button(self.window, text="Vis_Puls-Måling", font=('Arial', 17))
        self.button_puls.grid(row=1, column=1)

        self.label_graf = tk.Label(self.window, text="Opstilling-graf:", font=('Arial', 17))
        self.label_graf.grid(row=2, column=0, sticky=tk.W, pady=10)

        self.button_graf = tk.Button(self.window, text="Vis_Opstilling-graf", font=('Arial', 17), command = self.show_graf)
        self.button_graf.grid(row=2, column=1)

        self.frame_graf = tk.Frame(self.window)
        self.frame_graf.grid(row=3, column=0, columnspan=2)
        self.frame_graf.grid_remove()

        self.label_boundaries = tk.Label(self.frame_graf, text="Indtast grænseværdier for temp:", font=('Arial', 17))
        self.label_boundaries.pack(padx=10, pady=10)

        self.entry_temp_high = tk.Entry(self.frame_graf, width=30)
        self.entry_temp_high.pack()
        self.entry_temp_low = tk.Entry(self.frame_graf, width=30)
        self.entry_temp_low.pack()
        self.entry_temp_ok = tk.Entry(self.frame_graf, width=30)
        self.entry_temp_ok.pack()

        self.label_boundaries = tk.Label(self.frame_graf, text="Indtast grænseværdier for puls:", font=('Arial', 17))
        self.label_boundaries.pack(padx=10, pady=10)

        self.entry_puls_high = tk.Entry(self.frame_graf, width=30)
        self.entry_puls_high.pack()
        self.entry_puls_low = tk.Entry(self.frame_graf, width=30)
        self.entry_puls_low.pack()
        self.entry_puls_ok = tk.Entry(self.frame_graf, width=30)
        self.entry_puls_ok.pack()


        self.button = tk.Button(self.window, text="Print Data", font=('Arial', 17))
        self.button.place(relx=1, rely=1, anchor=tk.SE)


    def show_graf(self):
        if self.frame_graf.winfo_ismapped():
            self.frame_graf.grid_remove()
        else:
            self.frame_graf.grid()
        self.window.update_idletasks()

    def mainloop(self):
        self.window.mainloop()


MyGUI().mainloop()