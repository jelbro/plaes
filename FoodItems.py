class Recipe():
    """
    A class used to represent a Recipe

    Attributes
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

    Methods
    -------
    remove_ingredient(ingredients)
        removes Ingredient from ingredients list
    add_ingredient(ingredients)
        adds Ingredient to the ingredients list
    withdraw(quantity)
        removes n from quantity
    deposit(quantity)
        add n to quantity
    edit_desired(desired_quantity)
        changes desired quantity to n
    need_to_make(quantity, desired_quantity)
        returns wether the recipe needs to be made to meet the desired quantity
    """

    def __init__(self, name=None, ingredients=[], quantity=0, desired_quantity=0, unit=None):
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
        self.ingredients.append(ingredients)
        self.quantity = quantity
        self.desired_quantity = desired_quantity
        self.unit = unit

    @property
    def ingredients(self):
        return self._ingredients
    
    @ingredients.setter
    def ingredients(self, ingredients)
        self._ingredients = ingredients

    @property
    def desired_quantity(self):
        return self._desired_quantity
    
    @desired_quantity.setter
    def desired_quantity(self, desired_quantity):
        self._desired_quantity = desired_quantity

class Ingredient(FoodItem):
    ...