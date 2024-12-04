"""a Module including the Recipe and Ingredient classes

Classes
-------
Recipe
    a class to represent a Recipe, it includes a list of ingredients
Ingredient
    a class to represent an Ingredient
"""


class Recipe:
    """
    A class used to represent a Recipe

    Attributes
    ----------
    name : str
        the name of the Recipe
    ingredients : list of Ingredients
        the list of Ingredients that make up the Recipe
    quantity : float
        the current quantity of this Recipe in unit
    desired_quantity : float
        the desired quantity of this Recipe to have in stock in unit
    unit : str
        the unit of storage used for this Recipe

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
    need_to_make(quantity, desired_quantity)
        returns wether the recipe needs to be made to meet the desired quantity
    """

    def __init__(
        self, name=None, ingredients=[], quantity=0, desired_quantity=0, unit=None
    ):
        """
        Parameters
        ----------
        name : str
            the name of the Recipe
        ingredients : list
            the list of Ingredients that make up the Recipe
        quantity : float
            the current quantity of this Recipe in unit
        desired_quantity : float
            the desired quantity of this Recipe to have in stock in unit
        unit : str
            the unit of storage used for this Recipe
        """

        self.name = name
        self.ingredients.extend(ingredients)
        self.quantity = quantity
        self.desired_quantity = desired_quantity
        self.unit = unit

    def remove_ingredient(self, ingredient, amount):
        """remove an amount of Ingredient from this Recipe's ingredient list

        Parameters
        ----------
        ingredient : Ingredient
            an Ingredient object that should be present in this Recipes ingredient list
        amount : float
            an amount to remove from the ingredient

        Raises
        ------
        ValueError
            if trying to remove all ingredients, use delete_ingredient instead
        ValueError
            if the ingredient does not exist in this Recipes ingredient list
        """
        if ingredient.name in self.ingredients:
            if (ingredient.amount - amount) <= 0:
                raise ValueError(
                    "Cannot remove_ingredient() all ingredients, try delete_ingredient instead"
                )
            self.ingredients[ingredient.remove(amount)]
        else:
            raise ValueError(f"{ingredient} does not exist in ingredients list")

    def add_ingredient(self, ingredient, amount):
        """add an amount of Ingredient to this Recipes ingredient list

        Parameters
        ----------
        ingredient : Ingredient
            an Ingredient object that should already exist in this Recipes ingredient list
        amount : float
            an amount to add of this Ingredient

        Raises
        ------
        ValueError
            if amount to add is less than 1
        ValueError
            if the ingredient to be added to doesn't exist in this Recipes ingredient list
        """
        if ingredient.name in self.ingredients:
            if amount <= 0:
                raise ValueError("Amount to add must be greater than zero")
            self.ingredients[ingredient.add(amount)]
        else:
            raise ValueError(f"{ingredient} does not exist in ingredients list")

    def remove(self, amount):
        """remove amount from this Recipes quantity

        Parameters
        ----------
        amount : float
            amount to remove from this Recipes quantity

        Raises
        ------
        ValueError
            if trying to remove an amount less than or equal to zero
        ValueError
            if amount would result in quantity being less than or equal to zero
        """
        if amount <= 0:
            raise ValueError("Amount to remove must be greater than zero")
        elif self.quantity - amount <= 0:
            raise ValueError("Amount cannot result in quantity being less than zero")
        else:
            self.remove -= amount

    def add(self, amount): ...

    def edit_desired(self, new_desired): ...

    def need_to_make(self): ...


class Ingredient:
    """
    A class used to represent an Ingredient

    Attributes
    ----------
    name : str
        the name of the Ingredient
    quantity : float
        the current quantity of this Ingredient in unit
    unit : str
        the unit of storage used for this Ingredient

    Methods
    -------
    remove(quantity)
        removes n from quantity
    add(quantity)
        add n to quantity
    """

    def __init__(self, name=None, quantity=0, unit=None):
        """Ingredient Initialisation Function

        Parameters
        ----------
        name : str
            the name of the Ingredient, by default None
        quantity : float
            the quantity of the Ingredient, by default 0
        unit : str
            the unit of the Ingredient, by default None
        """
        self.name = name
        self.quantity = quantity
        self.unit = unit

    def remove(self, amount):
        """Remove amount from this Ingredient

        Parameters
        ----------
        amount : float
            a positive float to remove from this Ingredient's quantity

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
        amount : float
            a positive float to add to this Ingredient's quantity

        Raises
        ------
        ValueError
            if amount is a negative number
        """
        if amount < 0:
            raise ValueError("Amount to add can not be negative")
        else:
            self.quantity += amount
