from FoodItems import Recipe, Ingredient


def main():
    apple = Ingredient("Apple", 1)
    cabbage = Ingredient("Cabbage", 1)

    appage = Recipe("Appage", [apple, cabbage], 1, 2, "2l")

    print(apple)
    print(cabbage)
    print(appage)


if __name__ == "__main__":
    main()
