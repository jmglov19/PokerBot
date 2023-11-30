from tkinter import *

from PIL import Image, ImageTk

root = Tk()
root.title("Poker GUI")

e = Entry(root, width=35, borderwidth=5)
e.grid(row=0, column=0, columnspan= 3)

button_quit =Button(root, text= "Exit", command=root.quit)
button_quit.pack()

root.mainloop()