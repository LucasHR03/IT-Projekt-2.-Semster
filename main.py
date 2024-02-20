import tkinter as tk

data = ( (0,51), (1,50), (2,50), (3,50), (4,49), (5,48),
         (6,49),(7,51),(8,49),(9,51),(10,49))
'Få data ind fra en fil i stedet bla bla bla bla'
'jeg har skrevet en kommentar mere'
class Graf(tk.Frame):

    def __init__(self, h, w, data):
        super().__init__()

        self.master.title("Graf")
        self.pack(fill = tk.BOTH, expand = True)

        canvas = tk.Canvas(self)
        canvas.configure(bg="white")

        maxx, minx, maxy, miny, step= 12, -1, 70, 30, 5

        deltax = w / (maxx-minx)
        deltay = h / (maxy-miny)
        origox = -minx * deltax
        origoy = h +miny * deltay

        canvas.create_line(int(origox), 0, int(origox), h-1, fill="red")
        canvas.create_line(0, int(origoy), w-1, int(origoy), fill="red")
        for i in range((minx//step)*step,maxx, step):
            canvas.create_line(int(origox+i*deltax), int(origoy-5),
                int(origox+i*deltax), int(origoy+5), fill="red")
        for i in range((miny // step) * step, maxy, step):
            canvas.create_line(int(origox-5), int(origoy-i*deltay),
                int(origox+5), int(origoy-i*deltay), fill="red")
        for i in range(1,len(data)):
            x0 = int(data[i-1][0]*deltax+origox)
            y0 = int(origoy-(data[i-1][1]*deltay))
            x1 = int(data[i][0]*deltax+origox)
            y1 = int(origoy-(data[i][1]*deltay))
            canvas.create_line(x0, y0, x1, y1, fill="blue")

        canvas.pack(fill = tk.BOTH, expand = True)
def main():
    window = tk.Tk()
    h, w = 400, 400
    g = Graf(h, w, data)
    window.geometry(str(w) + "x" + str(h) + "+100+100")
    window.mainloop()


if __name__ == '__main__':
    main()