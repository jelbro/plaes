import sys
import pytest

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

    assert mayo.__str__() == "1 kg of Mayo"


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
    assert toast.display_ingredients() == "1 slice of Bread\n10 g of Butter"
    assert toast.quantity == 0
    assert toast.desired_quantity == 1
    assert toast.unit == "slice"


def test_Recipe_str():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    assert (
        toast.__str__()
        == "0 slice of Toasts\n1 slice of Bread\n10 g of Butter\n0 slice out of 1 slice in stock"
    )


def test_Recipe_repr():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    assert (
        toast.__repr__()
        == """Recipe(name: Toast, quantity: 0, desired_quantity: 1, unit: slice,
needed: False, ingredients: (Ingredient(name: Bread, quantity: 1, unit: slice), Ingredient(name: Butter, quantity: 10, unit: g)))"""
    )


def test_Recipe_remove_from_ingredient_correct_useage():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    toast.remove_from_ingredient("Butter", 5)
    assert toast.display_ingredients() == "1 slice of Bread\n5 g of Butter"


def test_Recipe_remove_from_ingredient_removing_to_zero():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.remove_from_ingredient("Butter", 10)


def test_Recipe_remove_from_ingredient_removing_past_zero():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.remove_from_ingredient("Butter", 20)


def test_Recipe_remove_from_ingredient_removing_negative_number():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.remove_from_ingredient("Butter", -10)


def test_Recipe_remove_from_ingredient_invalid_amount():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.remove_from_ingredient("Butter", "Butter")
