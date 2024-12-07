from FoodItems import Recipe, Ingredient


def main():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    # print(toast.display_ingredients())
    print(toast)


if __name__ == "__main__":
    main()
