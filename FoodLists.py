from FoodItems import *
import json


def load_list(file_path="ingredient_list.json"):
    if not file_path.lower().endswith(".json"):
        raise FileNotFoundError("file_path must be a valid .json file")
    with open(file_path, mode="r") as file:
        ingredient_list_file = json.loads(file.read())
        if len(ingredient_list_file) == 0:
            return IngredientList()
        else:
            ingredient_list = []
            for ingredient in ingredient_list_file["ingredient_list"]:
                ingredient_list.append(
                    Ingredient(
                        name=ingredient["name"],
                        quantity=ingredient["quantity"],
                        unit=ingredient["unit"],
                    )
                )
            return IngredientList(ingredient_list)


class IngredientList:
    """
    A class to represent a list of Ingredient objects

    Attributes
    ----------
    ingredient_list : list
        a list of Ingredient objects

    Methods
    -------
    add_new_ingredient()
        prompts the user for a name and unit and then creates a new Ingredient
        adding it to the ingredient list
    delete_from_list()
        displays the ingredient list and then prompts the user for the name
        of an ingredient to remove
    display_list()
        prints the ingredient list enumerating each entry
    """

    def __init__(self, ingredient_list=[]):
        """
        Parameters
        ----------
        ingredient_list : list
            a list of Ingredient objects
        """
        self.ingredient_list = []
        for ingredient in ingredient_list:
            self.ingredient_list.append(ingredient)

    def to_json(self):
        return json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=False, indent=4
        )

    def save_list(self, file_path):
        """saves this List to a .json file

        Parameters
        ----------
        file_path : str
            a file path to a .json file

        Raises
        ------
        FileNotFoundError
            if passed an invalid .json file path
        """
        if not file_path.lower().endswith(".json"):
            raise FileNotFoundError(
                "file_path must be a valid .json file path"
            )
        with open(file_path, mode="w") as file:
            file.write(self.to_json())

    def add_new_ingredient(self):
        """prompts the user for a name and unit, creates a new Ingredient with
        those values and adds it to the ingredient list
        """
        name = input("Ingredient name: ")
        unit = input("Ingredient unit: ")
        ingredient = Ingredient(name=name, quantity=0, unit=unit)
        self.ingredient_list.append(ingredient)

    def delete_from_list(self):
        """displays the ingredient list then prompts the user for the ingredient
        to remove
        """
        self.display_list()
        name = input("Name of ingredient to remove: ")
        name = name.lower().strip()
        for ingredient in self.ingredient_list:
            if ingredient.name == name:
                self.ingredient_list.remove(ingredient)
        self.display_list()
        input("Press enter to continue...")

    def display_list(self):
        """prints the list enumerating each entry"""
        num = 1
        for ingredient in self.ingredient_list:
            print(f"{num}:{ingredient.name}, unit: {ingredient.unit}")
            num += 1
