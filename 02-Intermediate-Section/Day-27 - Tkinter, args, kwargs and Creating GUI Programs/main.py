from tkinter import *

window = Tk()
window.title("My first GUI Program")
window.minsize(width=500, height=300)

def button_clicked():
    print("I got clicked.")
    new_text = entry_input.get()
    my_label.config(text=new_text)

# Label
my_label = Label(text="I am a label.", font=("Arial", 16, "bold"))
my_label.config(text="I am the New Label")
my_label.grid(column=0, row=0)
window.config(padx=20, pady=20)

# Button
button = Button(text="Click me", command=button_clicked)
button.grid(column=1, row=1)

# New_Button
button = Button(text="Click me", command=button_clicked)
button.grid(column=2, row=0)

# Entry
entry_input = Entry(width=10)
print(entry_input.get())
entry_input.grid(column=3, row=2)









window.mainloop()
