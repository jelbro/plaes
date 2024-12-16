from FoodItems import Recipe, Ingredient
import json


def load_recipe(file_path):
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
    ingredient_list = []
    for ingredient in recipe["ingredients"]:
        ingredient_list.append(
            Ingredient(
                name=ingredient["name"],
                quantity=ingredient["quantity"],
                unit=ingredient["unit"],
            )
        )
    return ingredient_list


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
