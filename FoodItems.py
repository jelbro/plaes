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
