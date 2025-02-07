from tkinter import *
from tkinter import ttk
from FoodLists import *
from inflect import *

inflect_engine = inflect.engine()


class Gui:

    def __init__(self, master, ingredient_list, recipe_list):
        self.ingredient_list = ingredient_list or IngredientList()
        self.recipe_list = recipe_list or RecipeList()
        self.recipe_index = 0
        self.stock_taken = False
        self.error_on_screen = False
        self.master = master
        self.content = ttk.Frame(master, padding=(3, 3, 12, 12))

        self.main_menu()

    def clear_window(self):
        for child in self.content.winfo_children():
            child.destroy()

    def pad_window(self):
        for child in self.content.winfo_children():
            child.grid_configure(padx=10, pady=10)

    def display_error_message(self, message):
        if self.error_on_screen:
            self.error_message.destroy()
            self.error_on_screen = False

        window_height = len(self.content.grid_slaves(column=0))
        window_width = len(self.content.grid_slaves(row=0))

        self.error_message = ttk.Label(self.content, text=message)
        self.error_message.grid(
            column=0, row=(window_height + 1), columnspan=(window_width + 1)
        )
        self.error_on_screen = True

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
        prep_list_button = ttk.Button(
            self.content,
            text="Prep List",
            command=self.prep_list_menu,
        )

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
            self.content,
            listvariable=self.ingredients_var,
        )
        self.ingredient_list_box.grid(column=0, row=1, rowspan=3)

        edit_ingredient_button = ttk.Button(
            self.content,
            text="Edit ingredient",
            command=lambda: self.edit_ingredient_menu(
                self.ingredient_list.ingredient_list[
                    self.ingredient_list_box.curselection()[0]
                ]
            ),
        )
        edit_ingredient_button.grid(column=1, row=1)

        add_ingredient_button = ttk.Button(
            self.content,
            text="Add ingredient",
            command=self.add_ingredient_menu,
        )
        add_ingredient_button.grid(column=1, row=2)

        delete_ingredient_button = ttk.Button(
            self.content,
            text="Delete ingredient",
            command=lambda: self.ingredient_list.delete_ingredient_from_list(
                self, self.recipe_list
            ),
        )
        delete_ingredient_button.grid(column=1, row=3)

        back_button = ttk.Button(
            self.content,
            text="Back to Main Menu",
            command=lambda: self.main_menu(),
        )
        back_button.grid(column=0, row=4, sticky=(S, W))

        self.pad_window()

    def add_ingredient_menu(self):
        self.clear_window()

        add_ingredient_menu_label = ttk.Label(
            self.content, text="Add Ingredient"
        )
        add_ingredient_menu_label.grid(column=0, row=0, columnspan=3)

        ingredient_name_label = ttk.Label(
            self.content, text="Ingredient name:"
        )
        ingredient_name = StringVar()
        ingredient_name_entry = ttk.Entry(
            self.content, textvariable=ingredient_name, width=15
        )
        ingredient_name_label.grid(column=0, row=1, sticky=E)
        ingredient_name_entry.grid(column=1, row=1, sticky=W)

        ingredient_unit_label = ttk.Label(
            self.content, text="Ingredient unit (Leave blank if n/a):"
        )
        ingredient_unit = StringVar()
        ingredient_name_entry = ttk.Entry(
            self.content, textvariable=ingredient_unit, width=15
        )
        ingredient_unit_label.grid(column=0, row=2, sticky=E)
        ingredient_name_entry.grid(column=1, row=2, columnspan=2, sticky=W)

        submit_button = ttk.Button(
            self.content,
            text="Okay",
            command=lambda: self.ingredient_list.add_new_ingredient(
                self, ingredient_name.get(), ingredient_unit.get()
            ),
        )
        submit_button.grid(
            column=1,
            row=3,
        )

        back_button = ttk.Button(
            self.content, text="Back", command=self.ingredient_menu
        )
        back_button.grid(
            column=0,
            row=3,
        )

        self.pad_window()

    def edit_ingredient_menu(self, ingredient):
        self.clear_window()

        edit_ingredient_label = ttk.Label(self.content, text="Edit Ingredient")
        edit_ingredient_label.grid(row=0, column=0, columnspan=3)

        ingredient_name_label = ttk.Label(self.content, text="Name:")
        ingredient_name = StringVar()
        ingredient_name.set(ingredient.name)

        def on_name_change(event):
            ingredient.name = ingredient_name.get()

        ingredient_name_entry = ttk.Entry(
            self.content,
            textvariable=ingredient_name,
        )
        ingredient_name_entry.bind("<Return>", on_name_change)
        ingredient_name_entry.bind("<FocusOut>", on_name_change)
        ingredient_name_label.grid(row=1, column=0, sticky=W)
        ingredient_name_entry.grid(row=1, column=1, sticky=W)

        ingredient_unit_label = ttk.Label(self.content, text="Unit:")
        ingredient_unit = StringVar()
        ingredient_unit.set(ingredient.unit)

        def on_ingredient_unit_change(event):
            ingredient.unit = ingredient_unit.get()

        ingredient_unit_entry = ttk.Entry(
            self.content, textvariable=ingredient_unit
        )
        ingredient_unit_entry.bind("<Return>", on_ingredient_unit_change)
        ingredient_unit_entry.bind("<FocusOut>", on_ingredient_unit_change)
        ingredient_unit_label.grid(row=2, column=0, sticky=W)
        ingredient_unit_entry.grid(row=2, column=1, sticky=W)

        back_button = ttk.Button(
            self.content,
            text="Back to ingredients",
            command=lambda: self.ingredient_menu(),
        )
        back_button.grid(column=0, row=3, sticky=(S, W), columnspan=2)

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

        unit_label = ttk.Label(self.content, text="Unit:")
        unit = StringVar()
        unit.set(recipe.unit)

        def on_unit_change(event):
            recipe.edit_unit(unit.get())

        unit_entry = ttk.Entry(self.content, textvariable=unit)
        unit_entry.bind("<Return>", on_unit_change)
        unit_entry.bind("<FocusOut>", on_unit_change)
        unit_label.grid(row=1, column=0, sticky=(N, E))
        unit_entry.grid(row=1, column=1, sticky=W)

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
        desired_quantity_label.grid(row=3, column=0, sticky=(N, E))
        desired_quantity_entry.grid(row=3, column=1, sticky=W)

        ingredients_label = ttk.Label(self.content, text="Ingredients:")
        self.recipe_ingredients_var = StringVar(
            value=recipe.get_ingredient_amounts()
        )
        self.recipe_ingredient_list_box = Listbox(
            self.content, listvariable=self.recipe_ingredients_var, height=8
        )
        ingredients_label.grid(row=4, column=0, sticky=(N, E))
        self.recipe_ingredient_list_box.grid(
            column=1, row=4, rowspan=4, sticky=S
        )

        def new_ingredient_or_existing():
            answer = messagebox.askyesno(
                message="Would you like to create a new ingredient?",
                icon="question",
                title="Create new ingredient",
            )
            if answer:
                self.add_new_ingredient_to_recipe_menu(recipe)
            else:
                self.add_existing_ingredient_to_recipe_menu(recipe)

        add_ingredient_button = ttk.Button(
            self.content,
            text="Add ingredient",
            command=new_ingredient_or_existing,
        )
        add_ingredient_button.grid(column=0, row=5)

        edit_ingredient_button = ttk.Button(
            self.content,
            text="Edit ingredient",
            command=lambda: self.edit_recipe_ingredient_menu(
                recipe.ingredients[
                    self.recipe_ingredient_list_box.curselection()[0]
                ],
                recipe,
            ),
        )
        edit_ingredient_button.grid(column=0, row=6)

        remove_ingredient_button = ttk.Button(
            self.content,
            text="Remove ingredient",
            command=lambda: recipe.remove_ingredient_from_recipe(self),
        )
        remove_ingredient_button.grid(column=0, row=7)

        back_button = ttk.Button(
            self.content,
            text="Back to Recipes",
            command=lambda: self.recipe_menu(),
        )
        back_button.grid(column=0, row=8, sticky=(S, W))

        self.pad_window()

    def add_new_ingredient_to_recipe_menu(self, recipe):
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
        ingredient_unit_entry = ttk.Entry(
            self.content, textvariable=ingredient_unit
        )
        ingredient_unit_label.grid(column=0, row=2)
        ingredient_unit_entry.grid(column=1, row=2)

        ingredient_amount_label = ttk.Label(
            self.content, text=f"Amount of ingredient in {recipe.name}:"
        )
        ingredient_amount = StringVar()
        ingredient_amount_entry = ttk.Entry(
            self.content, textvariable=ingredient_amount
        )
        ingredient_amount_label.grid(column=0, row=3)
        ingredient_amount_entry.grid(column=1, row=3)

        submit_button = ttk.Button(
            self.content,
            text="Okay",
            command=lambda: recipe.add_new_ingredient(
                self,
                ingredient_name.get(),
                ingredient_unit.get(),
                ingredient_amount.get(),
                self.ingredient_list,
            ),
        )
        submit_button.grid(column=1, row=4)

        back_button = ttk.Button(
            self.content,
            text="Back",
            command=lambda: self.edit_recipe_menu(recipe),
        )
        back_button.grid(column=0, row=4)

        self.pad_window()

    def add_existing_ingredient_to_recipe_menu(self, recipe):
        self.clear_window()

        add_ingredient_menu_label = ttk.Label(
            self.content, text=f"Add Ingredient to {recipe.name.title()}"
        )
        add_ingredient_menu_label.grid(column=0, row=0, columnspan=4)

        self.ingredients_var = StringVar(
            value=self.ingredient_list.ingredient_list
        )
        self.ingredient_list_box = Listbox(
            self.content, listvariable=self.ingredients_var, height=10
        )
        self.ingredient_list_box.grid(column=0, row=1, columnspan=2, rowspan=2)

        submit_button = ttk.Button(
            self.content,
            text="Select ingredient",
            command=lambda: self.get_existing_ingredient_quantity(
                self.ingredient_list.ingredient_list[
                    self.ingredient_list_box.curselection()[0]
                ],
                recipe,
            ),
        )
        submit_button.grid(column=1, row=4)

        back_button = ttk.Button(
            self.content,
            text="Back",
            command=lambda: self.edit_recipe_menu(recipe),
        )
        back_button.grid(column=0, row=4)

        self.pad_window()

    def get_existing_ingredient_quantity(self, ingredient, recipe):
        self.clear_window()

        add_ingredient_menu_label = ttk.Label(
            self.content,
            text=f"Add {ingredient.name} to {recipe.name.title()}",
        )
        add_ingredient_menu_label.grid(column=0, row=0, columnspan=4)

        ingredient_quantity_label = ttk.Label(
            self.content, text=f"Amount of {ingredient.unit} to add:"
        )
        ingredient_quantity_label.grid(column=0, row=1)
        ingredient_quantity = StringVar()
        ingredient_quantity_entry = ttk.Entry(
            self.content, textvariable=ingredient_quantity
        )
        ingredient_quantity_entry.grid(column=1, row=1)

        submit_button = ttk.Button(
            self.content,
            text="Okay",
            command=lambda: recipe.add_existing_ingredient(
                self, ingredient_quantity.get(), ingredient
            ),
        )
        submit_button.grid(column=1, row=2)

        self.pad_window()

    def edit_recipe_ingredient_menu(self, ingredient, recipe):
        self.clear_window()

        ingredient_name_label = ttk.Label(self.content, text="Name:")
        ingredient_name = StringVar()
        ingredient_name.set(ingredient.name)

        def on_name_change(event):
            ingredient.name = ingredient_name.get()

        ingredient_name_entry = ttk.Entry(
            self.content,
            textvariable=ingredient_name,
        )
        ingredient_name_entry.bind("<Return>", on_name_change)
        ingredient_name_entry.bind("<FocusOut>", on_name_change)
        ingredient_name_label.grid(row=0, column=0, sticky=E)
        ingredient_name_entry.grid(row=0, column=1, sticky=W)

        ingredient_unit_label = ttk.Label(self.content, text="Unit:")
        ingredient_unit = StringVar()
        ingredient_unit.set(ingredient.unit)

        def on_ingredient_unit_change(event):
            ingredient.unit = ingredient_unit.get()

        ingredient_unit_entry = ttk.Entry(
            self.content, textvariable=ingredient_unit
        )
        ingredient_unit_entry.bind("<Return>", on_ingredient_unit_change)
        ingredient_unit_entry.bind("<FocusOut>", on_ingredient_unit_change)
        ingredient_unit_label.grid(row=1, column=0, sticky=(N, E))
        ingredient_unit_entry.grid(row=1, column=1, sticky=W)

        back_button = ttk.Button(
            self.content,
            text="Back to ingredients",
            command=lambda: self.edit_recipe_menu(recipe),
        )
        back_button.grid(column=0, row=6, sticky=(S, W))

        self.pad_window()

    def add_recipe_menu(self):
        self.clear_window()

        create_recipe_label = ttk.Label(self.content, text="Create New Recipe")
        create_recipe_label.grid(column=0, row=0, columnspan=2)

        name_entry_label = ttk.Label(self.content, text="Name:")
        name = StringVar()
        name_entry = ttk.Entry(self.content, textvariable=name)
        name_entry_label.grid(column=0, row=1, sticky=E)
        name_entry.grid(column=1, row=1)

        unit_entry_label = ttk.Label(
            self.content, text="Unit (leave blank if n/a):"
        )
        unit = StringVar()
        unit_entry = ttk.Entry(self.content, textvariable=unit)
        unit_entry_label.grid(column=0, row=2, sticky=E)
        unit_entry.grid(column=1, row=2)

        batch_size_label = ttk.Label(self.content, text="Batch size:")
        batch_size = StringVar()
        batch_size_entry = ttk.Entry(self.content, textvariable=batch_size)
        batch_size_label.grid(column=0, row=3, sticky=E)
        batch_size_entry.grid(column=1, row=3)

        desired_quantity_entry_label = ttk.Label(
            self.content, text="Desired Quantity:"
        )
        desired_quantity = StringVar()
        desired_quantity_entry = ttk.Entry(
            self.content, textvariable=desired_quantity
        )
        desired_quantity_entry_label.grid(column=0, row=4, sticky=E)
        desired_quantity_entry.grid(column=1, row=4)

        cancel_button = ttk.Button(
            self.content, text="Cancel", command=self.recipe_menu
        )
        cancel_button.grid(column=0, row=5)

        add_ingredients_button = ttk.Button(
            self.content,
            text="Add Ingredients",
            command=lambda: self.recipe_list.create_new_recipe(
                name=name.get(),
                desired_quantity=desired_quantity.get(),
                unit=unit.get(),
                batch_size=batch_size.get(),
                gui=self,
            ),
        )
        add_ingredients_button.grid(column=1, row=5)

        self.pad_window()

    def prep_list_menu(self):
        if not self.stock_taken:
            if self.stock_take_dialog():
                self.stock_take_menu()
                return
        self.recipe_list.create_prep_list()

        self.clear_window()
        current_date = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        prep_list_date = current_date + one_day
        prep_list_date = prep_list_date.strftime("%A %d %B")
        prep_list_label = ttk.Label(
            self.content, text=f"Prep list for {prep_list_date}"
        )
        prep_list_label.grid(column=0, row=0, columnspan=3)

        prep_list_var = StringVar()
        prep_list_var.set(self.recipe_list.printable_prep_list)
        self.prep_list_listbox = Listbox(
            self.content, listvariable=prep_list_var
        )
        self.prep_list_listbox.grid(column=0, row=1, rowspan=3, sticky=(N, W))

        view_recipe_button = Button(
            self.content,
            text="View Recipe",
            command=lambda: self.edit_recipe_menu(
                self.recipe_list.prep_list[
                    self.prep_list_listbox.curselection()[0]
                ]
            ),
        )
        view_recipe_button.grid(column=1, row=1, sticky=(N, W))

        edit_stock_button = Button(
            self.content, text="Edit Stock", command=self.stock_take_menu
        )
        edit_stock_button.grid(column=1, row=2, sticky=(N, W))

        back_button = ttk.Button(
            self.content, text="Back to Main Menu", command=self.main_menu
        )
        back_button.grid(column=0, row=4, sticky=(S, W))

        self.pad_window()

    def stock_take_dialog(self):
        return messagebox.askyesno(
            title="Take Stock",
            message="Would you like to take stock?",
            icon="question",
        )

    def stock_take_menu(self):
        self.clear_window()
        recipe = self.recipe_list.recipe_list[self.recipe_index]

        take_stock_label = ttk.Label(
            self.content, text=f"Take Stock of {recipe.name}"
        )
        take_stock_label.grid(column=0, row=0, columnspan=3)

        if recipe.unit:
            amount_label = ttk.Label(
                self.content,
                text=f"How many {(inflect_engine.plural(recipe.unit)).title()} of {recipe.name} in stock?",
            )
        else:
            amount_label = ttk.Label(
                self.contnet,
                text=f"How many {inflect_engine.plural(recipe.name)} in stock",
            )
        amount_label.grid(column=0, row=1)

        def on_entry_focus(event):
            event.widget.select_range(0, END)

        amount_in_stock = StringVar()
        amount_in_stock.set(recipe.quantity)
        amount_entry = ttk.Entry(
            self.content,
            textvariable=amount_in_stock,
        )
        amount_entry.grid(column=1, row=1, sticky=W)
        amount_entry.bind("<FocusIn>", on_entry_focus)
        amount_entry.focus_set()

        def on_confirm_button_click():
            recipe.change_quantity(amount_in_stock.get())
            recipe.get_priority()
            if self.recipe_index != len(self.recipe_list.recipe_list) - 1:
                self.recipe_index += 1
                self.stock_take_menu()
            else:
                self.recipe_index = 0
                self.stock_taken = True
                self.prep_list_menu()

        confirm_button = ttk.Button(
            self.content,
            text="Confirm",
            command=on_confirm_button_click,
        )
        confirm_button.grid(column=1, row=2)

        def on_previous_button_click():
            if self.recipe_index != 0:
                self.recipe_index -= 1
                self.stock_take_menu()
            else:
                pass

        previous_button = ttk.Button(
            self.content,
            text="Previous Recipe",
            command=on_previous_button_click,
        )
        previous_button.grid(column=0, row=2, sticky=E)

        cancel_button = ttk.Button(
            self.content, text="Cancel", command=self.main_menu
        )
        cancel_button.grid(column=0, row=2, sticky=W)

        self.pad_window()
