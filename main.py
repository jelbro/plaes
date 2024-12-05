from FoodItems import Recipe, Ingredient


def main():
    chicken = Ingredient("Chicken Breast", 5, "kg")
    mayonaise = Ingredient("Mayonaise", 1, "kg")
    lemon = Ingredient("Lemon", 3)
    white_wine_vinegar = Ingredient("White wine vinegar", 50, "ml")

    chicken_salad = Recipe(
        "Chicken Salad",
        [chicken, mayonaise, lemon, white_wine_vinegar],
        2,
        4,
        "4 Litres",
    )

    print(chicken_salad)


if __name__ == "__main__":
    main()
