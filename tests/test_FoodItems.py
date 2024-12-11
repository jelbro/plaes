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

    assert apple.__repr__() == (
        "Ingredient(name: Apple, " "quantity: 1, unit: None)"
    )

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
    assert toast.needed == True


def test_Recipe_str():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    assert toast.__str__() == (
        "0 slice of Toasts\n"
        "1 slice of Bread\n"
        "10 g of Butter\n"
        "0 slice out of 1 slice in stock"
    )


def test_Recipe_repr():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    assert toast.__repr__() == (
        "Recipe(name: Toast, quantity: 0, desired_quantity: 1, unit: slice, "
        "needed: True,\n"
        "ingredients: [Ingredient(name: Bread, quantity: 1, unit: slice), "
        "Ingredient(name: Butter, quantity: 10, unit: g)])"
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


def test_Recipe_remove_from_ingredient_not_in_list():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.remove_from_ingredient("Cheese", 1)


def test_Recipe_add_to_ingredient_correct_useage():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    toast.add_to_ingredient("Butter", 5)
    assert toast.display_ingredients() == "1 slice of Bread\n15 g of Butter"


def test_Recipe_add_to_ingredient_with_zero():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.add_to_ingredient("Butter", 0)


def test_Recipe_add_to_ingredient_with_negative_number():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.add_to_ingredient("Butter", -5)


def test_Recipe_add_to_ingredient_with_invalid_amount():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.add_to_ingredient("Butter", "Butter")


def test_Recipe_add_to_ingredient_not_in_list():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.add_to_ingredient("Cheese", 10)


def test_Recipe_edit_ingredient_amount_correct_useage_to_add():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    toast.edit_ingredient_amount("Bread", "+", 1)
    assert toast.display_ingredients() == "2 slice of Bread\n10 g of Butter"


def test_Recipe_edit_ingredient_amount_correct_useage_to_subtract():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 2, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    toast.edit_ingredient_amount("Bread", "-", 1)
    assert toast.display_ingredients() == "1 slice of Bread\n10 g of Butter"


def test_Recipe_edit_ingredient_amount_invalid_operator():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.edit_ingredient_amount("Bread", 1, 1)
    with pytest.raises(Exception) as e_info:
        toast.edit_ingredient_amount("Bread", "add", 1)


def test_Recipe_remove_correct_useage():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        2,
        1,
        "slice",
    )

    toast.remove(1)
    assert toast.quantity == 1

    toast.remove(1)
    assert toast.quantity == 0


def test_Recipe_remove_less_than_zero():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        2,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.remove(0)


def test_Recipe_remove_result_lower_than_zero():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        2,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.remove(3)


def test_Recipe_remove_invalid_amount():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        2,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.remove("two")


def test_Recipe_add_correct_useage():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        2,
        1,
        "slice",
    )

    toast.add(1)
    assert toast.quantity == 3


def test_Recipe_add_less_than_zero():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        2,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.add(0)


def test_Recipe_add_invalid_amount():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        2,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.add("two")


def test_Recipe_edit_desired_correct_useage():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        2,
        1,
        "slice",
    )

    toast.edit_desired(3)
    assert toast.desired_quantity == 3
    assert toast.needed == True


def test_Recipe_edit_desired_less_than_zero():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        2,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.edit_desired(-2)


def test_Recipe_edit_desired_invalid_value():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        2,
        1,
        "slice",
    )

    with pytest.raises(Exception) as e_info:
        toast.edit_desired("two")


def test_Recipe_need_to_make_start_false():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        2,
        1,
        "slice",
    )

    assert toast.needed == False

    toast.remove(1.5)

    assert toast.needed == True

    toast.add(3)

    assert toast.needed == False


def test_Recipe_need_to_make_start_true():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    assert toast.needed == True

    toast.add(1)

    assert toast.needed == False

    toast.remove(1)

    assert toast.needed == True


def test_Recipe_add_ingredient_correct_useage_start_with_two():
    toast = Recipe(
        "Toast",
        (Ingredient("Bread", 1, "slice"), Ingredient("Butter", 10, "g")),
        0,
        1,
        "slice",
    )

    toast.add_ingredient(Ingredient("Jam", 5, "g"))

    assert toast.display_ingredients() == (
        "1 slice of Bread\n" "10 g of Butter\n" "5 g of Jam"
    )


def test_Recipe_add_ingredient_correct_useage_start_with_one():
    toast = Recipe(
        "Toast",
        [Ingredient("Bread", 1, "slice")],
        0,
        1,
        "slice",
    )

    toast.add_ingredient(Ingredient("Butter", 10, "g"))

    assert toast.display_ingredients() == ("1 slice of Bread\n10 g of Butter")


def test_Recipe_add_ingredient_invalid_name():
    toast = Recipe(
        "Toast",
        [Ingredient("Bread", 1, "slice")],
        0,
        1,
        "slice",
    )

    with pytest.raises(Exception):
        toast.add_ingredient(Ingredient("Butter2", 10, "g"))


def test_Recipe_add_ingredient_invalid_unit():
    toast = Recipe(
        "Toast",
        [Ingredient("Bread", 1, "slice")],
        0,
        1,
        "slice",
    )

    with pytest.raises(Exception):
        toast.add_ingredient(Ingredient("Butter", 10, "5"))


def test_Recipe_add_ingredient_invalid_quantity():
    toast = Recipe(
        "Toast",
        [Ingredient("Bread", 1, "slice")],
        0,
        1,
        "slice",
    )

    with pytest.raises(Exception):
        toast.add_ingredient(Ingredient("Butter", 0, "g"))
    with pytest.raises(Exception):
        toast.add_ingredient(Ingredient("Butter", -2, "g"))
    with pytest.raises(Exception):
        toast.add_ingredient(Ingredient("Butter", "two", "g"))
