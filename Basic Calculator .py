from tkinter import *

def click(value):
    current = entry.get()
    entry.delete(0, END)
    entry.insert(END, current + str(value))

def clear():
    entry.delete(0, END)

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, END)
        entry.insert(END, result)
    except:
        entry.delete(0, END)
        entry.insert(END, "Error")

root = Tk()
root.title("Simple Calculator")
root.geometry("320x420")
root.resizable(False, False)

entry = Entry(root, font=("Arial", 20), bd=10, justify="right")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

row = 1
col = 0

for button in buttons:
    if button == "=":
        Button(root, text=button, width=7, height=3,
               command=calculate).grid(row=row, column=col)
    else:
        Button(root, text=button, width=7, height=3,
               command=lambda b=button: click(b)).grid(row=row, column=col)

    col += 1
    if col > 3:
        col = 0
        row += 1

Button(root, text="Clear", width=30, height=2,
       command=clear).grid(row=5, column=0, columnspan=4, pady=10)

root.mainloop()
