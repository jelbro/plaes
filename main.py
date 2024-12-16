from FoodItems import Recipe, Ingredient, load_recipe, load_ingredients
import json


def main():
    """
    chicken_salad = Recipe(
        name="Chicken Salad",
        quantity=0,
        desired_quantity=1,
        unit="4litre",
    )

    chicken_salad.add_ingredient(Ingredient("Chicken Breast", 5, "kg"))
    chicken_salad.add_ingredient(Ingredient("Mayo", 1, "kg"))
    chicken_salad.add_ingredient(Ingredient("Lemon", 3))
    chicken_salad.add_ingredient(Ingredient("White Wine Vinegar", 50, "ml"))
    print(chicken_salad)


    chicken_salad.save_recipe(
        "test.json",
    )
    """
    chicken_salad = load_recipe("test.json")
    print(chicken_salad)


if __name__ == "__main__":
    main()
