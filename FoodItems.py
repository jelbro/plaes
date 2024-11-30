class FoodItem:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    def add_item(self, n):
        self.quantity += n

    def remove_item(self, n):
        self.quantity -= n

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def name(self, quantity):
        self._quantity = quantity

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit):
        self._unit = unit


class Recipe(FoodItem):
    def __init__(self, ingredients, desired_quantity):
        self.ingredients = []
        self.desired_quantity = desired_quantity

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