from FoodItems import *
import os
import json
import inflect
import datetime
from decimal import *
from tkinter import *
from tkinter import ttk, messagebox

inflect_engine = inflect.engine()

getcontext().prec = 100
TWO_PLACES = Decimal("0.01")


def limit_decimal_places(value):
    decimal_value = Decimal(value).quantize(TWO_PLACES)
    if decimal_value % 1 != 0:
        return decimal_value
    else:
        return decimal_value.quantize(Decimal("1"))


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
        self.printable_prep_ingredient_list = []

    def to_json(self):
        for recipe in self.recipe_list:
            recipe.quantity = str(recipe.quantity)
            recipe.priority = str(recipe.priority)
            recipe.desired_quantity = str(recipe.desired_quantity)
            recipe.batch_size = str(recipe.batch_size)
        return json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=False, indent=4
        )

    def delete_recipe_from_list(self, gui, recipe_to_remove):
        if gui.question_box(
            title="Delete Recipe",
            message=f"Are you sure you want to delete {recipe_to_remove.name.title()}?",
        ):
            self.recipe_list.remove(recipe_to_remove)
            gui.recipes_var.set(self.recipe_list)
        else:
            pass

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
        self.make_printable_ingredient_prep_list()

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

    def create_prep_ingredient_list(self):
        self.prep_ingredient_list.clear()
        for recipe in self.prep_list:
            for ingredient in recipe.ingredients:
                if ingredient in self.prep_ingredient_list:
                    ingredient.quantity += limit_decimal_places(
                        recipe.amount_to_make()
                    ) * Decimal(ingredient.used_in[recipe.name])
                else:
                    self.prep_ingredient_list.append(ingredient)
                    ingredient.quantity += limit_decimal_places(
                        Decimal(recipe.amount_to_make())
                        * Decimal(ingredient.used_in[recipe.name])
                    )

    def make_printable_ingredient_prep_list(self):
        self.printable_prep_ingredient_list.clear()
        for ingredient in self.prep_ingredient_list:
            if ingredient.unit:
                self.printable_prep_ingredient_list.append(
                    f"{ingredient.quantity}"
                    f"{inflect_engine.plural(ingredient.unit,
                                            ingredient.quantity)} "
                    f"of {ingredient.name.title()}"
                )
            else:
                self.printable_prep_ingredient_list.append(
                    f"{ingredient.quantity} "
                    f"{inflect_engine.plural(ingredient.name.title(),
                                            ingredient.quantity)}"
                )


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
        for ingredient in self.ingredient_list:
            ingredient.quantity = str(ingredient.quantity)
        return json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=False, indent=4
        )

    def clear_ingredient_quantitys(self):
        for ingredient in self.ingredient_list:
            ingredient.quantity = 0

    def add_new_ingredient(self, gui, name=None, unit=None):
        """prompts the user for a name and unit, creates a new Ingredient with
        those values and appends it to the ingredient list
        """

        if self.valid_ingredient_name(name=name, gui=gui) and self.valid_unit(
            unit, gui
        ):
            ingredient = Ingredient(
                name=name.title().strip(), quantity=0, unit=unit
            )
            self.ingredient_list.append(ingredient)
            gui.ingredient_menu()
        else:
            pass

    def valid_unit(self, unit, gui):
        if unit:
            if not unit.isalnum():
                gui.display_error_message("Invalid Unit given.")
                return False
            else:
                return True
        else:
            return True

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

    def delete_ingredient_from_list(self, gui, recipe_list):
        index = gui.ingredient_list_box.curselection()[0]
        ingredient_to_remove = self.ingredient_list[index]
        if self.confirm_deletion(ingredient_to_remove.name, recipe_list, gui):
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

    def confirm_deletion(self, name, recipe_list, gui):
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
        return gui.question_box(
            message=message_text, title="Delete Ingredient"
        )

    def reset_ingredient_quantity(self):
        for ingredient in self.ingredient_list:
            ingredient.quantity = 0
