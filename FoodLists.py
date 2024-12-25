from FoodItems import *
import json
import inflect

inflect_engine = inflect.engine()


def load_list(file_path):
    if not file_path.lower().endswith(".json"):
        raise FileNotFoundError("file_path must be a valid .json file")
    try:
        file = open(file_path, mode="r")
    except FileNotFoundError:
        with open(file_path, mode="x"):
            pass
    with open(file_path, mode="r") as file:
        first_char = file.read(1)
        if not first_char:
            ingredient_list_obj = IngredientList()
            return ingredient_list_obj, RecipeList(
                ingredient_list=ingredient_list_obj
            )
        else:
            file.seek(0)
            list_file = json.load(file)

            for entry in list_file:
                if "ingredient_list" in entry:
                    ingredient_list = []
                    for ingredient in entry["ingredient_list"]:
                        ingredient_list.append(
                            Ingredient(
                                name=ingredient["name"],
                                quantity=ingredient["quantity"],
                                unit=ingredient["unit"],
                            )
                        )
                if "recipe_list" in entry:
                    recipe_list = []
                    for recipe in entry["recipe_list"]:
                        recipe_list.append(
                            Recipe(
                                name=recipe["name"],
                                ingredients=load_ingredients(recipe),
                                quantity=recipe["quantity"],
                                desired_quantity=recipe["desired_quantity"],
                                unit=recipe["unit"],
                            )
                        )
        ingredient_list_obj = IngredientList(ingredient_list)
        return ingredient_list_obj, RecipeList(
            ingredient_list=ingredient_list_obj, recipe_list=recipe_list
        )


def save_lists(lists, file_path):
    if not file_path.lower().endswith(".json"):
        raise FileNotFoundError("file_path must be a valid .json file path")
    merged_lists = []
    for food_list in lists:
        merged_lists.append(json.loads(food_list.save_list()))
    with open(file_path, mode="w") as file:
        json.dump(merged_lists, file, indent=4)


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

    def save_list(self):
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
        return self.to_json()

    def add_new_ingredient(self, name=None):
        """prompts the user for a name and unit, creates a new Ingredient with
        those values and adds it to the ingredient list
        """
        if not name:
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


class RecipeList:
    def __init__(self, ingredient_list=None, recipe_list=[]):
        """
        Parameters
        ----------
        ingredient_list : list
            a list of Ingredient objects
        """
        self.recipe_list = []
        for recipe in recipe_list:
            self.recipe_list.append(recipe)
        self.ingredient_list = ingredient_list

    def to_json(self):
        return json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=False, indent=4
        )

    def save_list(self):
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
        return self.to_json()

    def add_new_recipe(self):
        name = input("Recipe name: ")
        unit = input("Recipe unit: ")
        desired_quantity = int(
            input(f"Desired quantity of " f"{inflect_engine.plural(unit)}: ")
        )
        self.ingredient_list.display_list()
        ingredients = []
        while True:
            try:
                ingredients.append(self.get_ingredient(name))
            except EOFError:
                recipe = Recipe(
                    name=name,
                    unit=unit,
                    desired_quantity=desired_quantity,
                    ingredients=ingredients,
                )
                self.recipe_list.append(recipe)
                break

    def get_ingredient(self, recipe_name):
        while True:
            ingredient_name = input("Ingredient to add to recipe: ")
            # ingredient_list = ingredient_list_obj.ingredient_list
            if len(self.ingredient_list.ingredient_list) == 0:
                if self.create_new_ingredient():
                    self.ingredient_list.add_new_ingredient(ingredient_name)
                    for ingredient in self.ingredient_list.ingredient_list:
                        ingredient.quantity = self.get_ingredient_quantity(
                            ingredient, ingredient_name, recipe_name
                        )
                        return ingredient
                else:
                    continue

            for ingredient in self.ingredient_list.ingredient_list:
                if self.ingredient_in_list(ingredient_name, ingredient):
                    ingredient.quantity = self.get_ingredient_quantity(
                        ingredient, ingredient_name, recipe_name
                    )
                    return ingredient
                else:
                    pass

            if self.create_new_ingredient():
                self.ingredient_list.add_new_ingredient(ingredient_name)
                ingredient.quantity = self.get_ingredient_quantity(
                    ingredient, ingredient_name, recipe_name
                )
                return ingredient
            else:
                break

    def ingredient_in_list(self, ingredient_name, ingredient):
        if ingredient_name.lower() == ingredient.name.lower():
            return True
        else:
            return False

    def get_ingredient_quantity(
        self, ingredient, ingredient_name, recipe_name
    ):
        if not ingredient.unit:
            return int(
                input(
                    f"Amount of {inflect_engine.plural(ingredient_name)} in "
                    f"{recipe_name}? "
                )
            )
        else:
            return int(
                input(
                    f"{inflect_engine.plural(ingredient.unit)} of "
                    f"{ingredient.name} in {recipe_name}? "
                )
            )

    def create_new_ingredient(self):
        create = input(
            "Ingredient not in list would you like to create it? y/n "
        )
        if create.lower().strip() == "y":
            return True
        else:
            return False
