from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Plaes")

content = ttk.Frame(root, padding=(3, 3, 12, 12))
plaes_label = ttk.Label(content, text="Plaes")
ingredients_button = ttk.Button(content, text="Ingredients")
recipes_button = ttk.Button(content, text="Recipes")
prep_list_button = ttk.Button(content, text="Prep List")

content.grid(column=0, row=0)
plaes_label.grid(sticky=N, column=0, row=0, columnspan=2)
ingredients_button.grid(column=0, row=1)
recipes_button.grid(column=1, row=1)
prep_list_button.grid(column=0, row=3, columnspan=2)

for child in content.winfo_children():
    child.grid_configure(padx=10, pady=10)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()
