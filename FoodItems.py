"""a Module including the Recipe and Ingredient classes

Classes
-------
Recipe
    a class to represent a Recipe, it includes a list of ingredients
Ingredient
    a class to represent an Ingredient
"""

import inflect
from decimal import *
import json

# create an instance of the inflect engine
inflect_engine = inflect.engine()

# set decimal precision to 2 places
getcontext().prec = 2


def load_recipe(file_path):
    """helper function to load a recipe from .json

    Parameters
    ----------
    file_path : str
        file path of a valid .json file

    Returns
    -------
    Recipe
        a Recipe object from the imported .json

    Raises
    ------
    FileNotFoundError
        if file path does not return a valid .json file
    """
    if not file_path.lower().endswith(".json"):
        raise FileNotFoundError("file_path must be a valid .json file path")
    with open(file_path, mode="r") as file:
        recipe = json.loads(file.read())
    return Recipe(
        name=recipe["name"],
        ingredients=load_ingredients(recipe),
        quantity=recipe["quantity"],
        desired_quantity=recipe["desired_quantity"],
        unit=recipe["unit"],
    )


def load_ingredients(recipe):
    """a helper function that creates Ingredient objects from imported .json

    Parameters
    ----------
    recipe : Recipe
        Recipe object imported from .json file

    Returns
    -------
    List of Ingredients
        returns a list of Ingredient objects with its values taken from the .json
    """
    ingredient_list = []
    for ingredient in recipe["ingredients"]:
        ingredient_list.append(
            Ingredient(
                name=ingredient["name"],
                quantity=ingredient["quantity"],
                unit=ingredient["unit"],
                used_in=ingredient["used_in"],
            )
        )
    return ingredient_list


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
        if name == None:
            raise ValueError("Recipe must have a name")
        else:
            self.name = name

        self.ingredients = []
        for ingredient in ingredients:
            self.ingredients.append(ingredient)

        if quantity < 0:
            raise ValueError("Recipe must have a positive quantity")
        else:
            self.quantity = quantity

        if desired_quantity < 0:
            raise ValueError("Recipe must have a positive desired quantity")
        else:
            self.desired_quantity = desired_quantity

        self.unit = unit
        self.needed = self.requires_making()

    def is_plural(self):
        if self.quantity != 1:
            return True
        else:
            return False

    def __str__(self):
        if self.is_plural():
            return (
                f"{self.quantity} {inflect_engine.plural(self.unit)} of "
                f"{self.name}\n"
                f"{self.display_ingredients()}\n"
                f"{self.quantity} {inflect_engine.plural(self.unit)} out of "
                f"{self.desired_quantity} "
                f"{inflect_engine.plural(self.unit, self.desired_quantity)} in stock"
            )

        else:
            return (
                f"{self.quantity} {self.unit} of "
                f"{self.name}\n"
                f"{self.display_ingredients()}\n"
                f"{self.quantity} {self.unit} out of "
                f"{self.desired_quantity} {self.unit} in stock"
            )

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

    def display_ingredients(self, end="\n"):
        """return this Recipe's ingredient list in a readable way

        Parameters
        ---------
        end : str
            a string to end each line with, be default a new line

        Returns
        -------
        str
            a string of ingredients with the final escape removed
        """
        output_string = ""
        for ingredient in self.ingredients:
            if len(ingredient.unit) == 0:
                output_string += (
                    f"{ingredient.used_in[self.name]} "
                    f"{inflect_engine.plural(ingredient.name, ingredient.used_in[self.name])}{end}"
                )
            else:

                output_string += (
                    f"{ingredient.used_in[self.name]} "
                    f"{inflect_engine.plural(ingredient.unit, ingredient.used_in[self.name])} "
                    f"of {ingredient.name}{end}"
                )
        return output_string.rstrip(end)

    def ingredient_is_valid(self, ingredient):
        """check wether Ingredient has valid values

        Parameters
        ----------
        ingredient : Ingredient
            an object of type Ingredient to be validated

        Returns
        -------
        boolean
            True Ingredient is valid

        Raises
        ------
        ValueError
            Ingredient name is not alphabetic
        ValueError
            Ingredient unit is not alphabetic
        ValueError
            Ingredient quantity is less than or equal to zero
        """
        ingredient_name = ingredient.name.replace(" ", "")
        if not len(ingredient.unit) == 0:
            ingredient_unit = ingredient.unit.replace(" ", "")
        else:
            ingredient_unit = "None"
        if not ingredient_name.isalpha():
            raise ValueError("Ingredient name is not alphabetic")
        elif not ingredient_unit.isalnum():
            raise ValueError(
                f"{ingredient_unit}: Ingredient unit is not alphanumeric"
            )
        elif ingredient.quantity < 0:
            raise ValueError(
                f"Ingredient quantity: {ingredient.quantity} is "
                "less than or equal to zero"
            )
        else:
            return True

    def add_ingredient(self, ingredient):
        """add an Ingredient to this Recipes ingredient list

        Parameters
        ----------
        ingredient : Ingredient
            an object of type Ingredient to add to this Recipes ingredient list

        Raises
        ------
        ValueError
            if trying to add a duplicate ingredient
        """
        for current_ingredient in self.ingredients:
            if current_ingredient.name == ingredient.name:
                raise ValueError(
                    "Recipe ingredients must not contain duplicates"
                )
        if self.ingredient_is_valid(ingredient):
            self.ingredients.append(ingredient)

    def delete_ingredient(self, ingredient_name):
        """delete an ingredient from this Recipes ingredient list

        Parameters
        ----------
        ingredient_name : str
            the name of the ingredient to delete

        Raises
        ------
        ValueError
            the ingredient to delete is not in this Recipes ingredient list
        """
        for ingredient in self.ingredients:
            if ingredient_name == ingredient.name:
                self.ingredients.remove(ingredient)
                return
        raise ValueError("Ingredient is not in ingredients list")

    def edit_ingredient_quantity(self, ingredient_name, operator, amount):
        """add or remove from an ingredient in this Recipe's ingredient list

        Parameters
        ----------
        ingredient_name : str
            the name of the ingredient you wish to edit
        operator : str
            either '+' or '-'
        amount : decimal
            amount to change ingredient.amount by

        Raises
        ------
        ValueError
            if given any value other than '+' or '-' for operator'
        """
        if operator == "+":
            self.add_to_ingredient(ingredient_name, amount)
        elif operator == "-":
            self.remove_from_ingredient(ingredient_name, amount)
        else:
            raise ValueError(f"{operator} is not a valid operator")

    def remove_from_ingredient(self, ingredient_name, amount):
        """remove an amount of Ingredient from this Recipe's ingredient list

        Parameters
        ----------
        ingredient_name : Ingredient
            an Ingredient name that should be present in
            this Recipes ingredient list
        amount : Decimal
            an amount to remove from the ingredient

        Raises
        ------
        ValueError
            if trying to remove all ingredients, use delete_ingredient instead
        ValueError
            if the ingredient does not exist in this Recipes ingredient list
        """
        if amount <= 0:
            raise ValueError("Amount must not be less than or equal to zero")
        try:
            Decimal(amount)
        except ValueError:
            print("{amount} is not a valid decimal")

        else:
            for current_ingredient in self.ingredients:
                if current_ingredient.name == ingredient_name:
                    if (current_ingredient.quantity - amount) <= 0:
                        raise ValueError(
                            "Cannot remove_ingredient() all ingredients, "
                            "try delete_ingredient instead"
                        )
                    else:
                        current_ingredient.remove(amount)
                        return
            else:
                raise ValueError(
                    f"{ingredient_name} does not exist in ingredients list"
                )

    def add_to_ingredient(self, ingredient_name, amount):
        """add an amount of Ingredient to this Recipes ingredient list

        Parameters
        ----------
        ingredient : Ingredient
            an Ingredient object that should already exist in
            this Recipes ingredient list
        amount : decimal
            an amount to add of this Ingredient

        Raises
        ------
        ValueError
            if amount to add is less than 1
        ValueError
            if the ingredient to be added to doesn't exist in
            this Recipes ingredient list
        """
        if amount <= 0:
            raise ValueError("Amount must not be less than or equal to zero")
        try:
            Decimal(amount)
        except ValueError:
            print("{amount} is not a valid decimal")

        for current_ingredient in self.ingredients:
            if current_ingredient.name == ingredient_name:
                current_ingredient.add(amount)
                return
        else:
            raise ValueError(
                f"{ingredient_name} does not exist in ingredients list"
            )

    def remove(self, amount):
        """remove amount from this Recipes quantity

        Parameters
        ----------
        amount : Decimal
            amount to remove from this Recipes quantity

        Raises
        ------
        ValueError
            if trying to remove an amount less than or equal to zero
        ValueError
            if amount would result in quantity being less than or equal to zero
        """
        try:
            amount = Decimal(amount)
        except ValueError:
            print(f"{amount} is not a valid decimal")
        if amount <= 0:
            raise ValueError("Amount to remove must be greater than zero")
        elif self.quantity - amount < 0:
            raise ValueError(
                "Amount cannot result in quantity being less than zero"
            )
        else:
            self.quantity -= amount
            self.needed = self.requires_making()

    def add(self, amount):
        """add amount to this Recipes quantity

        Parameters
        ----------
        amount : Decimal
            amount to add to this Recipes quantity

        Raises
        ------
        ValueError
            if amount to be added is less than or equal to zero
        """
        try:
            amount = Decimal(amount)
        except ValueError:
            print(f"{amount} is not a valid decimal")
        if amount <= 0:
            raise ValueError("Amount to add must be greater than zero")
        else:
            self.quantity += amount
            self.needed = self.requires_making()

    def edit_desired(self, new_desired):
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
        except ValueError:
            print(f"{new_desired} is not a valid decimal")
        if new_desired < 0:
            raise ValueError("desired_quantity cannot be zero or less")
        else:
            self.desired_quantity = new_desired
            self.needed = self.requires_making()

    def requires_making(self):
        """calculate if this recipe is needing to be made."""
        if self.quantity < self.desired_quantity:
            return True
        else:
            return False


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

    def is_plural(self):
        if self.quantity != 1:
            return True
        else:
            return False

    def __str__(self):
        if len(self.unit) == 0:
            if self.is_plural():
                return f"{self.quantity} {inflect_engine.plural(self.name)}"
            else:
                return f"{self.quantity} {self.name}"
        else:
            if self.is_plural():
                return (
                    f"{self.quantity} {inflect_engine.plural(self.unit)} "
                    f"of {self.name}"
                )
            else:
                return f"{self.quantity} {self.unit} of {self.name}"

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
