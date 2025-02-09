"""a Module including the Recipe and Ingredient classes

Classes
-------
Recipe
    a class to represent a Recipe, it includes a list of ingredients
Ingredient
    a class to represent an Ingredient
"""

from FoodLists import *
import inflect
from decimal import *
import json
from tkinter import *
from tkinter import messagebox

# create an instance of the inflect engine
inflect_engine = inflect.engine()

# set decimal precision to 2 places
getcontext().prec = 2


class Recipe:
    """
    A class used to represent a Recipe

    Attributes
    ----------
    name : str
        the name of the Recipe
    ingredients : list of Ingredients
        the list of Ingredients that make up the Recipe
    quantity : Decimal
        the current quantity of this Recipe
    desired_quantity : Decimal
        the desired quantity of this Recipe to have in stock
    unit : str
        the unit of storage used for this Recipe
    needed : boolean
        True if this recipe needs to be made, initialised as False

    Methods
    -------
    remove_ingredient(ingredients)
        removes Ingredient from ingredients list
    delete_ingredient(ingredients)
        deletes the ingredient from the ingredients list
    add_ingredient(ingredients)
        adds Ingredient to the ingredients list
    add_new_ingredient(ingredients)
        add a new ingredient to the ingredients list
    remove(quantity)
        removes n from quantity
    add(quantity)
        add n to quantity
    edit_desired(desired_quantity)
        changes desired quantity to n
    requires_making(quantity, desired_quantity)
        returns wether the recipe needs to be made to meet the desired quantity
    """

    def __init__(
        self,
        name=None,
        ingredients=[],
        quantity=0,
        desired_quantity=0,
        unit=None,
        batch_size=0,
    ):
        """
        Parameters
        ----------
        name : str
            the name of the Recipe
        ingredients : list
            the list of Ingredients that make up the Recipe
        quantity : Decimal
            the current quantity of this Recipe
        desired_quantity : Decimal
            the desired quantity of this Recipe to have in stock
        unit : str
            the unit of storage used for this Recipe
        """
        self.name = name
        self.ingredients = []
        for ingredient in ingredients:
            self.ingredients.append(ingredient)
        self.quantity = Decimal(quantity)
        self.desired_quantity = Decimal(desired_quantity)
        self.batch_size = Decimal(batch_size)
        self.get_priority()
        self.unit = unit
        self.needed = self.requires_making()

    def __str__(self):
        return self.name.title()

    def __repr__(self):
        return (
            f"Recipe(name: {self.name}, quantity: {self.quantity}, "
            f"desired_quantity: {self.desired_quantity}, unit: {self.unit}, "
            f"needed: {self.needed},\n"
            f"ingredients: {self.ingredients})"
        )

    def to_json(self):
        """converts the recipe to JSON format

        Returns
        -------
        json.dumps
            the Recipe serialized to JSON
        """
        return json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=False, indent=4
        )

    def save_recipe(self, file_path):
        """saves this Recipe to a .json file

        Parameters
        ----------
        file_path : str
            a file path to a .json file

        Raises
        ------
        FileNotFoundError
            if passed an invalid .json file path
        """
        if not file_path.lower().endswith(".json"):
            raise FileNotFoundError(
                "file_path must be a valid .json file path"
            )
        with open(file_path, mode="a") as file:
            file.write(self.to_json())

    def sort_ingredients(self, sort_by="name"):
        """sorts this Recipes ingredient list by either name or quantity

        Parameters
        ----------
        sort_by : str, optional
            the value to sort the ingredients by, by default "name"

        Raises
        ------
        ValueError
            if passed an invalid sort_by parameter
        """
        if sort_by == "name":
            self.ingredients = sorted(
                self.ingredients, key=lambda ingredient: ingredient.name
            )
        elif sort_by == "quantity":
            self.ingredients = sorted(
                self.ingredients, key=lambda ingredient: ingredient.quantity
            )
        else:
            raise ValueError("invalid sort_by parameter")

    def change_name(self, new_name):
        old_name = self.name
        self.name = new_name
        for ingredient in self.ingredients:
            ingredient.used_in[new_name] = ingredient.used_in.pop(old_name)

    def change_used_in_quantity(self, ingredient, new_quantity):
        ingredient.used_in[self.name] = new_quantity

    def add_existing_ingredient(self, gui, amount, ingredient):
        ingredient.add_ingredient_to_recipe(self, amount)
        self.ingredients.append(ingredient)
        gui.edit_recipe_menu(self)

    def add_new_ingredient(self, gui, name, unit, amount, ingredient_list):
        new_ingredient = Ingredient(name=name.title(), unit=unit)
        ingredient_list.ingredient_list.append(new_ingredient)
        new_ingredient.add_ingredient_to_recipe(self, amount)
        self.ingredients.append(new_ingredient)
        gui.edit_recipe_menu(self)

    def change_quantity(self, quantity):
        self.quantity = Decimal(quantity)
        self.needed = self.requires_making()

    def edit_desired(self, new_desired, gui):
        """Override this Recipes desired_quantity

        Parameters
        ----------
        new_desired : Decimal
            the number to replace this Recipes desired quantity with

        Raises
        ------
        ValueError
            if the new desired quantity would be zero or less
        """
        try:
            new_desired = Decimal(new_desired)
        except InvalidOperation:
            gui.display_error_message(f"Desired quantity must be a number")
        else:
            if new_desired < 0:
                gui.display_error_message(
                    "Desired quantity cannot be less than zero"
                )
            else:
                self.desired_quantity = Decimal(new_desired)
                self.needed = self.requires_making()

    def edit_batch_size(self, new_batch_size, gui):
        try:
            new_batch_size = Decimal(new_batch_size)
        except InvalidOperation:
            gui.display_error_message("Batch size must be a number")
        else:
            if new_batch_size < 0:
                gui.display_error_message(
                    "Batch size cannot be less than zero"
                )
            else:
                self.batch_size = Decimal(new_batch_size)

    def edit_unit(self, new_unit, gui):
        if len(new_unit) == 0:
            self.unit = new_unit
        elif new_unit.isalnum():
            self.unit = new_unit
        else:
            gui.display_error_message("Unit must be alphanumeric or None")

    def amount_to_make(self):
        quantity = self.quantity
        amount_of_batches = 0
        while quantity < self.desired_quantity:
            if quantity + self.batch_size >= self.desired_quantity:
                if quantity == 0:
                    amount_of_batches += 1
                    return amount_of_batches
                else:
                    amount_of_batches += 1
                    return amount_of_batches
            else:
                amount_of_batches += 1
                quantity += self.batch_size
        return amount_of_batches

    def get_priority(self):
        # the greater the difference of the desired quantity and the quantity
        # the higher the priority to make
        difference = self.desired_quantity - self.quantity
        if self.quantity == 0:
            self.priority = 10000000000000000
        else:
            self.priority = difference

    def requires_making(self):
        """calculate if this recipe is needing to be made."""
        if self.quantity < self.desired_quantity:
            return True
        else:
            return False

    def get_ingredient_amounts(self):
        ingredients_with_amounts = []
        for ingredient in self.ingredients:
            ingredients_with_amounts.append(
                self.pluralise_ingredient(ingredient)
            )
        return ingredients_with_amounts

    def ingredient_is_plural(self, ingredient):
        if ingredient.used_in[self.name] != 1:
            return True
        else:
            return False

    def pluralise_ingredient(self, ingredient):
        if len(ingredient.unit) == 0:
            if self.ingredient_is_plural(ingredient):
                return f"{ingredient.used_in[self.name]} {inflect_engine.plural(ingredient.name.title())}"
            else:
                return f"{ingredient.used_in[self.name]} {ingredient.name.title()}"
        else:
            if self.ingredient_is_plural(ingredient):
                return (
                    f"{ingredient.used_in[self.name]} {inflect_engine.plural(ingredient.unit)} "
                    f"of {ingredient.name.title()}"
                )
            else:
                return f"{ingredient.used_in[self.name]} {ingredient.unit} of {ingredient.name.title()}"

    def remove_ingredient_from_recipe(self, gui):
        index = gui.recipe_ingredient_list_box.curselection()[0]
        ingredient_to_remove = self.ingredients[index]
        if gui.question_box(
            title="Remove Ingredient",
            message=(
                f"Are you sure you want to remove "
                f"{ingredient_to_remove.name.title} from {self.name.title()}?",
            ),
        ):
            self.ingredients.remove(ingredient_to_remove)
            gui.recipe_ingredients_var.set(self.get_ingredient_amounts())
        else:
            pass


class Ingredient:
    """
    A class used to represent an Ingredient

    Attributes
    ----------
    name : str
        the name of the Ingredient
    quantity : Decimal
        the current quantity of this Ingredient in unit in stock
    unit : str
        the unit of storage used for this Ingredient
    used_in : dict
        a dictionary containing the name's of the Recipes using
        this ingredient and their quantitys

    Methods
    -------
    remove(quantity)
        removes n from quantity
    add(quantity)
        add n to quantity
    """

    def __init__(self, name=None, quantity=0, unit=None, used_in={}):
        """
        Parameters
        ----------
        name : str
            the name of the Ingredient, by default None
        quantity : decimal
            the quantity of the Ingredient, by default 0
        unit : str
            the unit of the Ingredient, by default None
        """
        if name == None:
            raise ValueError("Ingredient must have a name")
        else:
            self.name = name

        if quantity < 0:
            raise ValueError("Ingredient must have a positive quantity")
        else:
            self.quantity = quantity

        self.unit = unit
        self.used_in = used_in

    def set_used_in(self, recipe, amount):
        self.used_in[recipe.name] = amount

    def is_plural(self):
        if self.quantity != 1:
            return True
        else:
            return False

    def __str__(self):
        return self.name.title()

    def __repr__(self):
        return (
            f"Ingredient(name: {self.name}, "
            f"quantity: {self.quantity}, unit: {self.unit})"
        )

    def remove(self, amount):
        """Remove amount from this Ingredient

        Parameters
        ----------
        amount : decimal
            a positive decimal to remove from this Ingredient's quantity

        Raises
        ------
        ValueError
            if trying to remove more Ingredients than exist
        ValueError
            if trying to remove a negative amount
        """
        if (self.quantity - amount) < 0:
            raise ValueError(f"Not enough {self.name} to remove {amount}")
        elif amount < 0:
            raise ValueError("Amount to remove can not be negative")
        else:
            self.quantity -= amount

    def add(self, amount):
        """Add amount to this Ingredient's quantity

        Parameters
        ----------
        amount : decimal
            a positive decimal to add to this Ingredient's quantity

        Raises
        ------
        ValueError
            if amount is a negative number
        """
        if amount < 0:
            raise ValueError("Amount to add can not be negative")
        else:
            self.quantity += amount

    def add_ingredient_to_recipe(self, recipe, ingredient_quantity):
        if not self.used_in:
            self.used_in = {recipe.name: ingredient_quantity}
        else:
            if recipe in self.used_in:
                self.used_in[recipe.name] = ingredient_quantity
            else:
                self.used_in[recipe.name] = ingredient_quantity
