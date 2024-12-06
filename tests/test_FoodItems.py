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
