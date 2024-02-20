import tkinter as tk

window = tk.Tk()

for i in range(10):
    window.columnconfigure(i, weight=1, minsize=75)
    window.rowconfigure(i, weight=1, minsize=50)
    for j in range(10):
        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=20
        )
        frame.grid(row=i, column=j, padx=5, pady=5)
        my_label = tk.Label(window, text="Måling 1")
        my_label.grid(row=1, column=1)
        my_label = tk.Label(window, text="Måling 2")
        my_label.grid(row=3, column=1)
        my_label = tk.Label(window, text="Opstilling af graf")
        my_label.grid(row=5, column=1)
        my_label = tk.Label(window, text="Graf 1")
        my_label.grid(row=3, column=5)
        my_label = tk.Label(window, text="Print data")
        my_label.grid(row=8, column=8)

window.mainloop()