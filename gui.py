from tkinter import *
from tkinter import ttk
from FoodLists import *


class Gui:

    def __init__(self, ingredient_list, recipe_list):
        self.ingredient_list = ingredient_list or IngredientList()
        self.recipe_list = recipe_list or RecipeList()

        self.root = Tk()
        self.root.title("Plaes")
        self.content = ttk.Frame(self.root, padding=(3, 3, 12, 12))
        self.main_menu()
        self.root.mainloop()

    def clear_window(self):
        for child in self.content.winfo_children():
            child.destroy()

    def pad_window(self):
        for child in self.content.winfo_children():
            child.grid_configure(padx=10, pady=10)

    def main_menu(self):
        self.clear_window()

        main_menu_label = ttk.Label(self.content, text="Main Menu")
        ingredients_button = ttk.Button(
            self.content,
            text="Ingredients",
            command=lambda: self.ingredient_menu(),
        )
        recipes_button = ttk.Button(self.content, text="Recipes")
        prep_list_button = ttk.Button(self.content, text="Prep List")

        self.content.grid(column=0, row=0)
        main_menu_label.grid(sticky=N, column=0, row=0, columnspan=2)
        ingredients_button.grid(column=0, row=1)
        recipes_button.grid(column=1, row=1)
        prep_list_button.grid(column=0, row=3, columnspan=2)

        self.pad_window()

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def ingredient_menu(self):

        self.clear_window()

        ingredient_menu_label = ttk.Label(self.content, text="Ingredients")
        ingredient_menu_label.grid(column=0, row=0, columnspan=3)

        ingredients_var = StringVar(value=self.ingredient_list.ingredient_list)
        ingredient_list_box = Listbox(
            self.content, listvariable=ingredients_var, height=10
        )
        ingredient_list_box.grid(column=0, row=1, columnspan=2, rowspan=2)

        add_ingredient_button = ttk.Button(self.content, text="Add ingredient")
        add_ingredient_button.grid(column=3, row=1, sticky=N)

        delete_ingredient_button = ttk.Button(
            self.content,
            text="Delete ingredient",
        )
        delete_ingredient_button.grid(column=3, row=1)

        back_button = ttk.Button(
            self.content,
            text="Back to Main Menu",
            command=lambda: self.main_menu(),
        )
        back_button.grid(column=0, row=3, sticky=(S, W))

        self.pad_window()
