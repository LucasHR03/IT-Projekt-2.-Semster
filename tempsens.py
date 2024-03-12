# uge12 del a og b
import serial
import io
import sys

ser = serial.Serial('/dev/cu.usbserial-110', 9600, timeout=1)
sio = io.TextIOWrapper(io.BufferedReader(ser))

filnavn = "Uge12temp.txt"

print("Tænder temperatursensor!")
run = True
ser.setDTR(run)

# Åbn filen i append-tilstand
fil = open(filnavn, "a")

while run:
    try:
        l = sio.readline()
        if l:
            l = float(l[1:-2])
            print(l)

            # Skriv strengen til filen (f-string)
            fil.write(f"{round(l)}\n")
        else:
            print(".", end=" ")
            sys.stdout.flush()
    except KeyboardInterrupt:
        run = False

print("\n Slukker temperatursensor")
ser.setDTR(run)
ser.close()
fil.close()