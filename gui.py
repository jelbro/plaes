from tkinter import *
from tkinter import ttk
from FoodLists import *


class Gui:

    def __init__(self, master, ingredient_list, recipe_list):
        self.ingredient_list = ingredient_list or IngredientList()
        self.recipe_list = recipe_list or RecipeList()

        self.master = master
        self.content = ttk.Frame(master, padding=(3, 3, 12, 12))

        self.main_menu()

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

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

    def ingredient_menu(self):
        self.clear_window()

        ingredient_menu_label = ttk.Label(self.content, text="Ingredients")
        ingredient_menu_label.grid(column=0, row=0, columnspan=3)

        self.ingredients_var = StringVar(
            value=self.ingredient_list.ingredient_list
        )
        self.ingredient_list_box = Listbox(
            self.content, listvariable=self.ingredients_var, height=10
        )
        self.ingredient_list_box.grid(column=0, row=1, columnspan=2, rowspan=2)

        add_ingredient_button = ttk.Button(
            self.content,
            text="Add ingredient",
            command=self.add_ingredient_menu,
        )
        add_ingredient_button.grid(column=3, row=1, sticky=N)

        delete_ingredient_button = ttk.Button(
            self.content,
            text="Delete ingredient",
            command=lambda: self.ingredient_list.delete_ingredient_from_list(
                self
            ),
        )
        delete_ingredient_button.grid(column=3, row=1)

        back_button = ttk.Button(
            self.content,
            text="Back to Main Menu",
            command=lambda: self.main_menu(),
        )
        back_button.grid(column=0, row=3, sticky=(S, W))

        self.pad_window()

    def add_ingredient_menu(self):
        self.clear_window()

        add_ingredient_menu_label = ttk.Label(
            self.content, text="Add Ingredient"
        )
        add_ingredient_menu_label.grid(column=0, row=0, columnspan=2)

        ingredient_name_label = ttk.Label(
            self.content, text="Ingredient name:"
        )
        ingredient_name = StringVar()
        ingredient_name_entry = ttk.Entry(
            self.content, textvariable=ingredient_name
        )
        ingredient_name_label.grid(column=0, row=1)
        ingredient_name_entry.grid(column=1, row=1)

        ingredient_unit_label = ttk.Label(
            self.content, text="Ingredient unit (Leave blank if n/a):"
        )
        ingredient_unit = StringVar()
        ingredient_name_entry = ttk.Entry(
            self.content, textvariable=ingredient_unit
        )
        ingredient_unit_label.grid(column=0, row=2)
        ingredient_name_entry.grid(column=1, row=2)

        submit_button = ttk.Button(
            self.content,
            text="Okay",
            command=lambda: self.ingredient_list.add_new_ingredient(
                self, ingredient_name.get(), ingredient_unit.get()
            ),
        )
        submit_button.grid(column=1, row=3)

        back_button = ttk.Button(
            self.content,
            text="Back",
            command=self.ingredient_menu,
        )
        back_button.grid(column=0, row=3)

        self.pad_window()
