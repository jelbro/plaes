from FoodItems import Recipe, Ingredient


def main():
    toast = Recipe(
        "Toast",
        [Ingredient("Bread", 1, "slice")],
        0,
        1,
        "slice",
    )

    toast.add_ingredient(Ingredient("Bread", 2, "slices"))
    print(toast.display_ingredients)


if __name__ == "__main__":
    main()
