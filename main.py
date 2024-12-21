from FoodItems import Recipe, Ingredient, load_recipe, load_ingredients
from Menu import *


def main():
    ingredient_list = load_list()
    instance = Menu(ingredient_list=ingredient_list)
    instance.display_main_menu()


if __name__ == "__main__":
    main()
