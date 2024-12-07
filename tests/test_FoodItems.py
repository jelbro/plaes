import sys

sys.path.append("/home/josh/documents/development/repos/plaes")
from FoodItems import Recipe, Ingredient


def test_Ingredient_init():
    apple = Ingredient("Apple", 1)

    assert apple.name == "Apple"
    assert apple.quantity == 1
    assert apple.unit == None

    mayo = Ingredient("Mayo", 1, "kg")

    assert mayo.name == "Mayo"
    assert mayo.quantity == 1
    assert mayo.unit == "kg"


def test_Ingredient_str():
    apple = Ingredient("Apple", 1)

    assert apple.__str__() == "1 Apple"

    mayo = Ingredient("Mayo", 1, "kg")

    assert mayo.__str__() == "1kg of Mayo"


def test_Ingredient_repr():
    apple = Ingredient("Apple", 1)

    assert apple.__repr__() == "Ingredient(name: Apple, quantity: 1, unit: None)"

    mayo = Ingredient("Mayo", 1, "kg")

    assert mayo.__repr__() == "Ingredient(name: Mayo, quantity: 1, unit: kg)"


def test_Recipe_init():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    assert toast.name == "Toast"
    assert toast.display_ingredients() == "1 slice of Bread\n10 g of Butter\n"
    assert toast.quantity == 0
