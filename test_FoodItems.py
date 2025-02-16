import pytest
from FoodItems import *
from FoodLists import *
from Gui import *

ingredient_list = IngredientList()
recipe_list = RecipeList()
root = Tk()
root.title("Plaes")
root.geometry("500x600")
gui = Gui(root, ingredient_list=ingredient_list, recipe_list=recipe_list)


def test_recipe_init():
    chicken_salad = Recipe(
        name="chicken salad", desired_quantity=2, unit="4l", batch_size=2
    )

    assert chicken_salad.name == "Chicken Salad"
    assert chicken_salad.ingredients == []
    assert chicken_salad.quantity == 0
    assert chicken_salad.desired_quantity == 2
    assert chicken_salad.batch_size == 2
    assert chicken_salad.priority == 10000000000000000
    assert chicken_salad.unit == "4l"
    assert chicken_salad.needed == True


def test_recipe_str():
    chicken_salad = Recipe(
        name="chicken salad", desired_quantity=2, unit="4l", batch_size=2
    )

    assert chicken_salad.__str__() == "Chicken Salad"


def test_recipe_repr():
    chicken_salad = Recipe(
        name="chicken salad", desired_quantity=2, unit="4l", batch_size=2
    )
    chicken_salad.add_new_ingredient(
        gui=gui,
        name="chicken breast",
        unit="kg",
        amount=5,
        ingredient_list=ingredient_list,
    )

    assert chicken_salad.__repr__() == (
        "Recipe(name: Chicken Salad, quantity: 0, "
        "desired_quantity: 2, unit: 4l, "
        "needed: True,\n"
        "ingredients: [Ingredient(name: Chicken Breast, quantity: 0, unit: kg)])"
    )


def test_recipe_sort_ingredients():
    chicken_salad = Recipe(
        name="chicken salad", desired_quantity=2, unit="4l", batch_size=2
    )
    chicken_salad.add_new_ingredient(
        gui=gui,
        name="chicken breast",
        unit="kg",
        amount=5,
        ingredient_list=ingredient_list,
    )
    chicken_salad.add_new_ingredient(
        gui=gui,
        name="mayo",
        unit="kg",
        amount=1,
        ingredient_list=ingredient_list,
    )
    chicken_salad.add_new_ingredient(
        gui=gui,
        name="avacado",
        unit="g",
        amount=50,
        ingredient_list=ingredient_list,
    )
    chicken_salad.sort_ingredients(sort_by="name")

    assert chicken_salad.__repr__() == (
        "Recipe(name: Chicken Salad, quantity: 0, "
        "desired_quantity: 2, unit: 4l, "
        "needed: True,\n"
        "ingredients: [Ingredient(name: Avacado, quantity: 0, unit: g), "
        "Ingredient(name: Chicken Breast, quantity: 0, unit: kg), "
        "Ingredient(name: Mayo, quantity: 0, unit: kg)])"
    )


def test_recipe_change_name():
    chicken_salad = Recipe(
        name="chicken salad", desired_quantity=2, unit="4l", batch_size=2
    )

    chicken_salad.change_name("chicken_mayo")
