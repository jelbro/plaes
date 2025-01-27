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
            command=self.ingredient_menu,
        )
        recipes_button = ttk.Button(
            self.content, text="Recipes", command=self.recipe_menu
        )
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
                self, self.recipe_list
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
        add_ingredient_menu_label.grid(column=0, row=0, columnspan=4)

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

    def recipe_menu(self):
        self.clear_window()

        recipe_menu_label = ttk.Label(self.content, text="Recipes")
        recipe_menu_label.grid(column=0, row=0, columnspan=4)

        self.recipes_var = StringVar(value=self.recipe_list.recipe_list)
        self.recipes_list_box = Listbox(
            self.content, listvariable=self.recipes_var, height=10
        )
        self.recipes_list_box.grid(column=0, row=1, columnspan=2, rowspan=3)

        edit_recipe_button = ttk.Button(
            self.content,
            text="Edit recipe",
            command=lambda: self.edit_recipe_menu(
                self.recipe_list.recipe_list[
                    self.recipes_list_box.curselection()[0]
                ]
            ),
        )
        edit_recipe_button.grid(column=3, row=1)

        add_recipe_button = ttk.Button(
            self.content,
            text="Add recipe",
            command=self.add_recipe_menu,
        )
        add_recipe_button.grid(column=3, row=2)

        delete_recipe_button = ttk.Button(
            self.content,
            text="Delete recipe",
            command=lambda: self.recipe_list.delete_from_list(self),
        )
        delete_recipe_button.grid(column=3, row=3)

        back_button = ttk.Button(
            self.content,
            text="Back to Main Menu",
            command=lambda: self.main_menu(),
        )
        back_button.grid(column=0, row=4, sticky=(S, W))

        self.pad_window()

    def edit_recipe_menu(self, recipe):
        self.clear_window()
        # recipe = self.recipe_list.recipe_list[index]

        recipe_name_label = ttk.Label(self.content, text="Name:")
        recipe_name = StringVar()
        recipe_name.set(recipe.name)

        def on_name_change(event):
            recipe.change_name(recipe_name.get())

        recipe_name_entry = ttk.Entry(
            self.content,
            textvariable=recipe_name,
        )
        recipe_name_entry.bind("<Return>", on_name_change)
        recipe_name_entry.bind("<FocusOut>", on_name_change)
        recipe_name_label.grid(row=0, column=0, sticky=E)
        recipe_name_entry.grid(row=0, column=1, sticky=W)

        desired_quantity_label = ttk.Label(
            self.content, text="Desired Quantity:"
        )
        desired_quantity = StringVar()
        desired_quantity.set(recipe.desired_quantity)

        def on_desired_quantity_change(event):
            recipe.edit_desired(desired_quantity.get())

        desired_quantity_entry = ttk.Entry(
            self.content, textvariable=desired_quantity
        )
        desired_quantity_entry.bind("<Return>", on_desired_quantity_change)
        desired_quantity_entry.bind("<FocusOut>", on_desired_quantity_change)
        desired_quantity_label.grid(row=1, column=0, sticky=(N, E))
        desired_quantity_entry.grid(row=1, column=1, sticky=W)

        batch_size_label = ttk.Label(self.content, text="Batch Size:")
        batch_size = StringVar()
        batch_size.set(recipe.batch_size)

        def on_batch_size_change(event):
            recipe.edit_batch_size(batch_size.get())

        batch_size_entry = ttk.Entry(self.content, textvariable=batch_size)
        batch_size_entry.bind("<Return>", on_batch_size_change)
        batch_size_entry.bind("<FocusOut>", on_batch_size_change)
        batch_size_label.grid(row=2, column=0, sticky=(N, E))
        batch_size_entry.grid(row=2, column=1, sticky=W)

        unit_label = ttk.Label(self.content, text="Unit:")
        unit = StringVar()
        unit.set(recipe.unit)

        def on_unit_change(event):
            recipe.edit_unit(unit.get())

        unit_entry = ttk.Entry(self.content, textvariable=unit)
        unit_entry.bind("<Return>", on_unit_change)
        unit_entry.bind("<FocusOut>", on_unit_change)
        unit_label.grid(row=3, column=0, sticky=(N, E))
        unit_entry.grid(row=3, column=1, sticky=W)

        ingredients_label = ttk.Label(self.content, text="Ingredients:")
        self.recipe_ingredients_var = StringVar(
            value=recipe.get_ingredient_amounts()
        )
        self.recipe_ingredient_list_box = Listbox(
            self.content, listvariable=self.recipe_ingredients_var, height=8
        )
        ingredients_label.grid(row=4, column=0, sticky=(N, E))
        self.recipe_ingredient_list_box.grid(column=1, row=4)

        add_ingredient_button = ttk.Button(
            self.content,
            text="Add ingredient",
            command=lambda: self.add_ingredient_to_recipe_menu(recipe),
        )
        add_ingredient_button.grid(column=0, row=4)

        remove_ingredient_button = ttk.Button(
            self.content,
            text="Remove ingredient",
            command=lambda: recipe.remove_ingredient_from_recipe(self),
        )
        remove_ingredient_button.grid(column=0, row=4, sticky=(S))

        back_button = ttk.Button(
            self.content,
            text="Back to Recipes",
            command=lambda: self.recipe_menu(),
        )
        back_button.grid(column=0, row=6, sticky=(S, W))

        self.pad_window()

    def add_ingredient_to_recipe_menu(self, recipe):
        self.clear_window()

        add_ingredient_menu_label = ttk.Label(
            self.content, text=f"Add Ingredient to {recipe.name.title()}"
        )
        add_ingredient_menu_label.grid(column=0, row=0, columnspan=4)

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

        ingredient_amount_label = ttk.Label(
            self.content, text=f"Amount of ingredient in {recipe.name}:"
        )
        ingredient_amount = StringVar()
        ingredient_amount_entry = ttk.Entry(
            self.content, textvariable=ingredient_amount
        )
        ingredient_amount_label.grid(column=0, row=2)
        ingredient_amount_entry.grid(column=1, row=2)

        submit_button = ttk.Button(
            self.content,
            text="Okay",
            command=lambda: recipe.add_new_ingredient(
                self,
                ingredient_name.get(),
                ingredient_unit.get(),
                ingredient_amount.get(),
            ),
        )
        submit_button.grid(column=1, row=4)

        back_button = ttk.Button(
            self.content,
            text="Back",
            command=self.edit_recipe_menu(recipe),
        )
        back_button.grid(column=0, row=4)

        self.pad_window()

    def add_recipe_menu(self): ...
