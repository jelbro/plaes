from FoodItems import Recipe, Ingredient, load_recipe, load_ingredients
from Menu import *


def main():
    ingredient_list, recipe_list = load_list("plaes_lists.json")
    instance = Menu(ingredient_list=ingredient_list, recipe_list=recipe_list)
    instance.display_main_menu()


if __name__ == "__main__":
    main()
