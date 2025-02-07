from FoodItems import *
import os
import json
import inflect
import datetime
from tkinter import *
from tkinter import ttk, messagebox

inflect_engine = inflect.engine()


def clear():
    os.system("clear")


class IngredientList:
    """
    A class to represent a list of Ingredient objects

    Attributes
    ----------
    ingredient_list : list
        a list of Ingredient objects

    Methods
    -------
    save_list()
        saves this IngredientList to a .json file
    add_new_ingredient()
        prompts the user for a name and unit and then creates a new Ingredient
        adding it to the ingredient list
    delete_from_list()
        displays the ingredient list and then prompts the user for the name
        of an ingredient to remove
    display_list()
        prints the ingredient list enumerating each entry
    """

    def __init__(self, ingredient_list=[]):
        """
        Parameters
        ----------
        ingredient_list : list
            a list of Ingredient objects
        """
        self.ingredient_list = []
        for ingredient in ingredient_list:
            self.ingredient_list.append(ingredient)

    def to_json(self):
        return json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=False, indent=4
        )

    def save_list(self):
        """saves this List to a .json file

        Parameters
        ----------
        file_path : str
            a file path to a .json file

        Raises
        ------
        FileNotFoundError
            if passed an invalid .json file path
        """
        return self.to_json()

    def search_for_ingredient(self, prompt, error=None):
        while True:
            ingredient = input(prompt)
            try:
                ingredient = self.find_ingredient(ingredient)
                return ingredient
            except ValueError:
                if error == "add":
                    if self.create_new_ingredient():
                        self.add_new_ingredient(
                            name=ingredient,
                        )
                    return self.find_ingredient(ingredient)
                else:
                    print("Invalid ingredient name")

    def find_ingredient(self, ingredient_to_find):
        for ingredient in self.ingredient_list:
            if ingredient_to_find.lower() == ingredient.name.lower():
                return ingredient
            else:
                pass
        raise ValueError

    def create_new_ingredient(self):
        """Prompts the user to ask if they would like to add the ingredient
        to the list

        Returns
        -------
        boolean
            True if answer is equal to 'y'
        """
        response = input(
            "Ingredient not in list would you like to create it? y/n "
        )
        return response.lower().strip() == "y"

    def clear_ingredient_quantitys(self):
        for ingredient in self.ingredient_list:
            ingredient.quantity = 0

    def add_new_ingredient(self, gui, name=None, unit=None):
        """prompts the user for a name and unit, creates a new Ingredient with
        those values and appends it to the ingredient list
        """

        if self.valid_ingredient_name(name=name, gui=gui):
            ingredient = Ingredient(
                name=name.title().strip(), quantity=0, unit=unit
            )
            self.ingredient_list.append(ingredient)
            gui.ingredient_menu()
        else:
            pass

    def valid_ingredient_name(self, name, gui):
        valid_name = True
        if not name:
            gui.display_error_message("No Name given.")
            valid_name = False
        for ingredient in self.ingredient_list:
            if name.lower().strip() == ingredient.name.lower().strip():
                gui.display_error_message("Duplicate name given.")
                valid_name = False
            else:
                pass
        stripped_name = name.replace(" ", "")
        if not stripped_name.isalpha():
            gui.display_error_message("Invalid Name given.")
            valid_name = False
        return valid_name

    def delete_from_list(self, recipe_list):
        """displays the ingredient list then prompts the user for the ingredient
        to remove
        """
        self.display_list(wait=False)
        ingredient = self.search_for_ingredient(
            "Name of ingredient to remove: "
        )
        if self.confirm_deletion(ingredient.name, recipe_list):
            self.ingredient_list.remove(ingredient)
            for recipe in recipe_list.recipe_list:
                if ingredient in recipe.ingredients:
                    recipe.ingredients.remove(ingredient)
            clear()
            self.display_list()
        else:
            pass

    def delete_ingredient_from_list(self, gui, recipe_list):
        index = gui.ingredient_list_box.curselection()[0]
        ingredient_to_remove = self.ingredient_list[index]
        if self.confirm_deletion(ingredient_to_remove.name, recipe_list):
            self.ingredient_list.remove(ingredient_to_remove)
            for recipe in recipe_list.recipe_list:
                for ingredient in recipe.ingredients:
                    if (
                        ingredient.name.lower()
                        == ingredient_to_remove.name.lower()
                    ):
                        recipe.ingredients.remove(ingredient)
            gui.ingredients_var.set(self.ingredient_list)
        else:
            pass

    def confirm_deletion(self, name, recipe_list):
        recipes_used_in = []
        for recipe in recipe_list.recipe_list:
            for ingredient in recipe.ingredients:
                if name == ingredient.name:
                    recipes_used_in.append(recipe.name.title())
                else:
                    pass
        recipes_text = ""
        for recipe_name in recipes_used_in:
            if recipe_name == recipes_used_in[0]:
                recipes_text += recipe_name
            else:
                recipes_text += f", {recipe_name}"
        if recipes_text == "":
            recipes_text += "no recipes"

        message_text = (
            f"Are you sure you want to delete {name.title()}? "
            f"This ingredient is used in {recipes_text}."
        )
        return messagebox.askyesno(
            message=message_text, icon="question", title="Delete Ingredient"
        )

    def display_list(self, wait=True):
        """prints the list enumerating each entry

        Parameters
        ----------
        wait : bool, optional
            if True wait for user input before continuing, by default True
        """
        num = 1
        for ingredient in self.ingredient_list:
            print(f"{num}: {ingredient.name.title()}, unit: {ingredient.unit}")
            num += 1
        if wait:
            input("Press enter to continue...")


class RecipeList:
    """
    a class to represent a list of Recipe objects

    Attributes
    ----------
    recipe_list : list
        a list of Recipe objects

    Methods
    -------
    save_list()
        saves this list to a .json file
    add_new_recipe(IngredientList)
        Prompts the user for a name, unit, desired quantity, ingredients
        and ingredient quantitys and creates a Recipe with these values adding
        it to this RecipeLists recipe_list
    get_ingredient(recipe_name, IngredientList, Recipe)
        prompts the user for ingredients until ctrl+d is input (EOFError)
        appending these to the Recipe's ingredient list
    ingredient_in_list(ingredient_name, ingredient)
        returns True if the ingredient already exists in the IngredientList
    get_ingredient_quantity(ingredient, ingredient_name, recipe_name)
        returns the quantity of the ingredient the user wishes to add to the
        recipe as an int
    create_new_ingredient()
        prompts the user to create a new ingredient if the current ingredient
        is not in the IngredientList
    """

    def __init__(self, recipe_list=[]):
        """
        Parameters
        ----------
        ingredient_list : list
            a list of Ingredient objects
        """
        self.recipe_list = []
        for recipe in recipe_list:
            self.recipe_list.append(recipe)

        self.prep_list = []
        self.prep_ingredient_list = []
        self.printable_prep_list = []

    def to_json(self):
        return json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=False, indent=4
        )

    def save_list(self):
        """saves this List to a .json file

        Parameters
        ----------
        file_path : str
            a file path to a .json file

        Raises
        ------
        FileNotFoundError
            if passed an invalid .json file path
        """
        return self.to_json()

    def display_list(self, wait=False):
        """prints this RecipeList"""
        num = 1
        for recipe in self.recipe_list:
            print(f"{num}: {recipe.name}, unit: {recipe.unit}")
            num += 1
            if wait:
                input("Press enter to continue...")

    """def delete_from_list(self):
        self.display_list(wait=False)
        recipe = self.search_for_recipe("Name of recipe to remove: ")
        if self.confirm_deletion(recipe.name):
            self.recipe_list.remove(recipe)
            for ingredient in recipe.ingredients:
                ingredient.used_in.pop(recipe.name)
            clear()
            self.display_list()
        else:
            pass
        """

    def delete_from_list(self, gui):
        index = gui.recipes_list_box.curselection()[0]
        recipe_to_remove = self.recipe_list[index]
        if self.confirm_deletion(recipe_to_remove.name):
            self.recipe_list.remove(recipe_to_remove)
            gui.recipes_var.set(self.recipe_list)
        else:
            pass

    def confirm_deletion(self, name):
        return messagebox.askyesno(
            title="Delete Recipe",
            message=(f"Are you sure you want to delete {name.title()}?"),
            icon="question",
        )

    def search_for_recipe(self, prompt):
        while True:
            try:
                recipe = self.find_recipe(input(prompt))
                return recipe
            except ValueError:
                print("Invalid recpie name")

    def find_recipe(self, recipe_to_find):
        for recipe in self.recipe_list:
            if recipe_to_find.lower() == recipe.name.lower():
                return recipe
            else:
                pass
        raise ValueError

    def add_new_recipe(self, ingredient_list_obj):
        """prompts the user for a name, unit, desired quantity constructs a new
        recipe from this and then asks the user for the ingredients in this
        recipe

        Parameters
        ----------
        ingredient_list_obj : IngredientList
            the current IngredientList to reference for existing ingredients
        """
        name = input("Recipe name: ")
        unit = input("Recipe unit: ")
        desired_quantity = int(
            input(f"Desired quantity of " f"{inflect_engine.plural(unit)}: ")
        )
        batch_size = int(
            input(
                f"How many {inflect_engine.plural(unit)} of {name} "
                "does one batch make: "
            )
        )
        new_recipe = Recipe(
            name=name,
            unit=unit,
            desired_quantity=desired_quantity,
            batch_size=batch_size,
        )

        while True:
            try:
                ingredient_list_obj.display_list(wait=False)
                new_recipe.add_ingredient(
                    self.get_ingredient(name, ingredient_list_obj, new_recipe)
                )
            except EOFError:
                self.recipe_list.append(new_recipe)
                print("\n")
                break

    def valid_recipe(self, name, desired_quantity, unit, batch_size, gui):

        if (
            self.valid_recipe_name(name, gui)
            and self.valid_desired_quantity(desired_quantity, gui)
            and self.valid_unit(unit, gui)
            and self.valid_batch_size(batch_size, gui)
        ):
            return True
        else:
            return False

    def valid_batch_size(self, batch_size, gui):
        valid_batch_size = True

        if not batch_size.isnumeric():
            gui.display_error_message("Batch Size is not a positive number.")
            valid_batch_size = False

        return valid_batch_size

    def valid_unit(self, unit, gui):
        valid_unit = True

        if not unit.isalnum() and len(unit) > 0:
            valid_unit = False
            gui.display_error_message("Invalid Unit Entered.")

        return valid_unit

    def valid_desired_quantity(self, desired_quantity, gui):
        valid_desired_quantity = True

        if not desired_quantity.isnumeric():
            gui.display_error_message(
                "Desired Quantity is not a positive number."
            )
            valid_desired_quantity = False

        return valid_desired_quantity

    def valid_recipe_name(self, name, gui):
        valid_name = True

        if not name:
            gui.display_error_message("Recipe must have a name.")
            valid_name = False

        for recipe in self.recipe_list:
            if name.lower().strip() == recipe.name.lower().strip():
                gui.display_error_message("Recipe already exists.")
                valid_name = False
            else:
                pass

        trimmed_name = name.replace(" ", "")
        if not trimmed_name.isalpha():
            gui.display_error_message("Recipe is not alphabetic.")
            valid_name = False

        return valid_name

    def create_new_recipe(self, name, desired_quantity, unit, batch_size, gui):
        if self.valid_recipe(name, desired_quantity, unit, batch_size, gui):
            new_recipe = Recipe(
                name=name,
                desired_quantity=int(desired_quantity),
                unit=unit,
                batch_size=int(batch_size),
                ingredients=[],
            )
            self.recipe_list.append(new_recipe)
            gui.edit_recipe_menu(new_recipe)
        else:
            pass

    def get_ingredient(self, recipe_name, ingredient_list_obj, recipe_obj):
        """asks the user for the name of the ingredient, checks if it is already
        in the ingredient list if it is not creates that ingredient. Then asks
        the user for the quantity of ingredient to use in the recipe

        Parameters
        ----------
        recipe_name : str
            the user inputted name for the recipe
        ingredient_list_obj : IngredientList
            the current IngredientList to reference
        recipe_obj : Recipe
            the newly created Recipe to add ingredients to

        Returns
        -------
        Ingredient
            returns a fully initialised Ingredient object
        """
        while True:
            ingredient_name = input("Ingredient to add to recipe: ")

            if len(ingredient_list_obj.ingredient_list) == 0:
                if self.create_new_ingredient():
                    ingredient_list_obj.add_new_ingredient(ingredient_name)
                    for ingredient in ingredient_list_obj.ingredient_list:
                        ingredient.add_ingredient_to_recipe(
                            recipe_obj,
                            self.get_ingredient_quantity(
                                ingredient, ingredient_name, recipe_name
                            ),
                        )
                        return ingredient
                else:
                    continue
            else:
                for ingredient in ingredient_list_obj.ingredient_list:
                    if self.ingredient_in_list(ingredient_name, ingredient):
                        ingredient.add_ingredient_to_recipe(
                            recipe_obj,
                            self.get_ingredient_quantity(
                                ingredient, ingredient_name, recipe_name
                            ),
                        )
                        return ingredient
                    else:
                        pass
                if self.create_new_ingredient():
                    ingredient_list_obj.add_new_ingredient(ingredient_name)
                    for ingredient in ingredient_list_obj.ingredient_list:
                        if self.ingredient_in_list(
                            ingredient_name, ingredient
                        ):
                            ingredient.add_ingredient_to_recipe(
                                recipe_obj,
                                self.get_ingredient_quantity(
                                    ingredient, ingredient_name, recipe_name
                                ),
                            )
                            return ingredient
                        else:
                            pass
                else:
                    break

    def ingredient_in_list(self, ingredient_name, ingredient):
        """checks to see if the user inputted ingredient name matches the name
        of the current ingredient

        Parameters
        ----------
        ingredient_name : str
            a user inputted ingredient name
        ingredient : Ingredient
            the current Ingredient object the name is being checked against

        Returns
        -------
        boolean
            True if the names are equal
        """
        return ingredient_name.lower() == ingredient.name.lower()

    def get_ingredient_quantity(
        self, ingredient, ingredient_name, recipe_name
    ):
        """prompts the user for the amount of the current ingredient to add
        to the recipe

        Parameters
        ----------
        ingredient : Ingredient
            the current ingredient to add to the recipe
        ingredient_name : str
            the user input ingredient name
        recipe_name : str
            the name of the Recipe that is currently being created

        Returns
        -------
        int
            an int representing the amount of Ingredient in Recipe
        """
        if not ingredient.unit:
            return int(
                input(
                    f"Amount of {inflect_engine.plural(ingredient_name)} in "
                    f"{recipe_name}? "
                )
            )
        else:
            return int(
                input(
                    f"{inflect_engine.plural(ingredient.unit)} of "
                    f"{ingredient.name} in {recipe_name}? "
                )
            )

    def create_new_ingredient(self):
        """Prompts the user to ask if they would like to add the ingredient
        to the list

        Returns
        -------
        boolean
            True if answer is equal to 'y'
        """
        response = input(
            "Ingredient not in list would you like to create it? y/n "
        )
        return response.lower().strip() == "y"

    def take_stock(self):
        for recipe in self.recipe_list:
            recipe.change_quantity(
                int(
                    input(
                        f"How many {inflect_engine.plural(recipe.unit)} "
                        f"of {recipe.name} are in stock? "
                    )
                )
            )
            recipe.get_priority()

    def create_prep_list(self):
        self.prep_list.clear()
        for recipe in self.recipe_list:
            if recipe.needed:
                self.prep_list.append(recipe)
            else:
                pass
        self.sort_by_priority()
        self.create_prep_ingredient_list()
        self.make_printable_prep_list()

    def make_printable_prep_list(self):
        self.printable_prep_list.clear()
        for recipe in self.prep_list:
            self.printable_prep_list.append(
                f"Make {recipe.amount_to_make()}x {recipe.name}"
            )

    def sort_by_priority(self):
        self.prep_list = sorted(
            self.prep_list, key=lambda recipe: recipe.priority
        )

    def display_prep_list(self):
        current_date = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        prep_list_date = current_date + one_day
        prep_list_date = prep_list_date.strftime("%A %d %B")

        print(f"Prep list for {prep_list_date}")
        self.draw_underline(len(prep_list_date), 14)

        for recipe in self.prep_list:
            print(f"Make {recipe.amount_to_make()}x {recipe.name}")
        self.draw_underline(len(prep_list_date), 14)

        print("Ingredients needed:")
        for ingredient in self.prep_ingredient_list:
            if not ingredient.unit:
                print(
                    f"- {ingredient.quantity} "
                    f"{inflect_engine.plural(ingredient.name)}"
                )
            else:
                print(
                    f"- {ingredient.quantity}"
                    f"{inflect_engine.plural(ingredient.unit)} {ingredient.name}"
                )
        self.draw_underline(len(prep_list_date), 14)
        input("Press enter to continue...")

    def create_prep_ingredient_list(self):

        self.prep_ingredient_list.clear()
        for recipe in self.prep_list:
            for ingredient in recipe.ingredients:
                if ingredient in self.prep_ingredient_list:
                    ingredient.quantity += (
                        recipe.amount_to_make()
                        * ingredient.used_in[recipe.name]
                    )
                else:
                    self.prep_ingredient_list.append(ingredient)
                    ingredient.quantity += (
                        recipe.amount_to_make()
                        * ingredient.used_in[recipe.name]
                    )

    def draw_underline(self, date_length, string_length):
        total_length = date_length + string_length

        for i in range(total_length):
            print("-", end="")
        print()
