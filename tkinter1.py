import tkinter
 
print(dir(tkinter))


def fct_knop1_druk_event(x):
    print(x)
    mijn_label1["text"] = x
    mijn_label1["bg"] = "yellow" if x == "On" else "red"
    
    

window = tkinter.Tk()
window.geometry("800x400")
window.title("test scherm")

mijn_label1 = tkinter.Label(window, text="G T")
mijn_label1.place(x=100, y=100)

mijn_knop1 = tkinter.Button(window, text="On", command=lambda : fct_knop1_druk_event("Off"))
mijn_knop1.place(x=200, y=100)

dir(mijn_knop1) 


window.mainloop()