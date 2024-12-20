from FoodItems import *


class IngredientList:
    def __init__(self, ingredient_list=[]):
        self.ingredient_list = []
        for ingredient in ingredient_list:
            self.ingredient_list.append(ingredient)

    def add_new_ingredient(self):
        name = input("Ingredient name: ")
        unit = input("Ingredient unit: ")
        ingredient = Ingredient(name=name, quantity=0, unit=unit)
        self.ingredient_list.append(ingredient)

    def display_list(self):
        num = 1
        for ingredient in self.ingredient_list:
            print(f"{num}:{ingredient.name}, unit: {ingredient.unit}")
            num += 1
