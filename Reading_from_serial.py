import serial, time
ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
from tkinter import *
import _thread as thread



def fct_toggle_on_off():
    print("hi from fct_toggle_on_off")
    ser.write(b"toggle_on_off\n")
    state = ser.readline()
    print(state)
    if "state" in state.decode("ASCII"):
        toggle_on_off_button["text"] = state.decode("ASCII")
        
window = Tk()
window.geometry("800x400")
window.title("CVO FOCUS RP1 GUI")

toggle_on_off_button = Button(window, text ="toggle_on_off", command=fct_toggle_on_off)
toggle_on_off_button.place(x=300,y=100)

target_temp_label = Label(window, text="init")
target_temp_label.place(x=300,y=200)

current_temp_label = Label(window, text="init")
current_temp_label.place(x=300,y=300)


def update_label():
    global window
    serial_output = ser.readline()
    print("loop")
    print(serial_output.decode("ASCII"))
    if "target_temp" in serial_output.decode("ASCII"):
        print(serial_output)
        target_temp_label["text"] = serial_output.decode("ASCII")
        print(serial_output.decode("ASCII"))
        
    if "current_temp" in serial_output.decode("ASCII"):
        print(serial_output)
        current_temp_label["text"] = serial_output.decode("ASCII")
        print(serial_output.decode("ASCII"))
    
    window.after(1, update_label)

window.after(1000, update_label)

window.mainloop()

