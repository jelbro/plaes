from FoodItems import *
import json
import inflect

inflect_engine = inflect.engine()


def load_list(file_path):
    """a method which loads a RecipeList and IngredientList from a .json file

    Parameters
    ----------
    file_path : str
        a .json file path

    Returns
    -------
    tuple(IngredientList, RecipeList)
        returns an initalised IngredientList and RecipeList from the .json file

    Raises
    ------
    FileNotFoundError
        if file_path is not a valid .json file
    """
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
            return ingredient_list_obj, RecipeList()
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
                                used_in=ingredient["used_in"],
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
        return IngredientList(ingredient_list), RecipeList(
            recipe_list=recipe_list
        )


def save_lists(lists, file_path):
    """a function to save the IngredientList and RecipeList to the given .json
    file_path

    Parameters
    ----------
    lists : list(IngredientList, RecipeList)
        a list of an IngredientList and a RecipeList
    file_path : str
        a valid .json file path

    Raises
    ------
    FileNotFoundError
        if file_path is not a valid .json file path
    """
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
    save_list()
        saves this IngredientList to a .json file
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

    def add_new_ingredient(self, name=None, unit=None):
        """prompts the user for a name and unit, creates a new Ingredient with
        those values and appends it to the ingredient list
        """
        if not name:
            name = input("Ingredient name: ")
        if not unit:
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
            print(f"{num}: {ingredient.name}, unit: {ingredient.unit}")
            num += 1


class RecipeList:
    """
    a class to represent a list of Recipe objects

    Attributes
    ----------
    recipe_list : list
        a list of Recipe objects

    Methods
    -------
    save_list()
        saves this list to a .json file
    add_new_recipe(IngredientList)
        Prompts the user for a name, unit, desired quantity, ingredients
        and ingredient quantitys and creates a Recipe with these values adding
        it to this RecipeLists recipe_list
    get_ingredient(recipe_name, IngredientList, Recipe)
        prompts the user for ingredients until ctrl+d is input (EOFError)
        appending these to the Recipe's ingredient list
    ingredient_in_list(ingredient_name, ingredient)
        returns True if the ingredient already exists in the IngredientList
    get_ingredient_quantity(ingredient, ingredient_name, recipe_name)
        returns the quantity of the ingredient the user wishes to add to the
        recipe as an int
    create_new_ingredient()
        prompts the user to create a new ingredient if the current ingredient
        is not in the IngredientList
    """

    def __init__(self, recipe_list=[]):
        """
        Parameters
        ----------
        ingredient_list : list
            a list of Ingredient objects
        """
        self.recipe_list = []
        for recipe in recipe_list:
            self.recipe_list.append(recipe)

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

    def display_list(self):
        """prints this RecipeList"""
        num = 1
        for recipe in self.recipe_list:
            print(f"{num}: {recipe.name}, unit: {recipe.unit}")
            num += 1

    def add_new_recipe(self, ingredient_list_obj):
        """prompts the user for a name, unit, desired quantity constructs a new
        recipe from this and then asks the user for the ingredients in this
        recipe

        Parameters
        ----------
        ingredient_list_obj : IngredientList
            the current IngredientList to reference for existing ingredients
        """
        name = input("Recipe name: ")
        unit = input("Recipe unit: ")
        desired_quantity = int(
            input(f"Desired quantity of " f"{inflect_engine.plural(unit)}: ")
        )
        new_recipe = Recipe(
            name=name, unit=unit, desired_quantity=desired_quantity
        )

        while True:
            try:
                ingredient_list_obj.display_list()
                new_recipe.add_ingredient(
                    self.get_ingredient(name, ingredient_list_obj, new_recipe)
                )
            except EOFError:
                self.recipe_list.append(new_recipe)
                print("\n")
                break

    def get_ingredient(self, recipe_name, ingredient_list_obj, recipe_obj):
        """asks the user for the name of the ingredient, checks if it is already
        in the ingredient list if it is not creates that ingredient. Then asks
        the user for the quantity of ingredient to use in the recipe

        Parameters
        ----------
        recipe_name : str
            the user inputted name for the recipe
        ingredient_list_obj : IngredientList
            the current IngredientList to reference
        recipe_obj : Recipe
            the newly created Recipe to add ingredients to

        Returns
        -------
        Ingredient
            returns a fully initialised Ingredient object
        """
        while True:
            ingredient_name = input("Ingredient to add to recipe: ")

            if len(ingredient_list_obj.ingredient_list) == 0:
                if self.create_new_ingredient():
                    ingredient_list_obj.add_new_ingredient(ingredient_name)
                    for ingredient in ingredient_list_obj.ingredient_list:
                        ingredient.add_ingredient_to_recipe(
                            recipe_obj,
                            self.get_ingredient_quantity(
                                ingredient, ingredient_name, recipe_name
                            ),
                        )
                        return ingredient
                else:
                    continue
            else:
                for ingredient in ingredient_list_obj.ingredient_list:
                    if self.ingredient_in_list(ingredient_name, ingredient):
                        ingredient.add_ingredient_to_recipe(
                            recipe_obj,
                            self.get_ingredient_quantity(
                                ingredient, ingredient_name, recipe_name
                            ),
                        )
                        return ingredient
                    else:
                        pass
                if self.create_new_ingredient():
                    ingredient_list_obj.add_new_ingredient(ingredient_name)
                    for ingredient in ingredient_list_obj.ingredient_list:
                        if self.ingredient_in_list(
                            ingredient_name, ingredient
                        ):
                            ingredient.add_ingredient_to_recipe(
                                recipe_obj,
                                self.get_ingredient_quantity(
                                    ingredient, ingredient_name, recipe_name
                                ),
                            )
                            return ingredient
                        else:
                            pass
                else:
                    break

    def ingredient_in_list(self, ingredient_name, ingredient):
        """checks to see if the user inputted ingredient name matches the name
        of the current ingredient

        Parameters
        ----------
        ingredient_name : str
            a user inputted ingredient name
        ingredient : Ingredient
            the current Ingredient object the name is being checked against

        Returns
        -------
        boolean
            True if the names are equal
        """
        return ingredient_name.lower() == ingredient.name.lower()

    def get_ingredient_quantity(
        self, ingredient, ingredient_name, recipe_name
    ):
        """prompts the user for the amount of the current ingredient to add
        to the recipe

        Parameters
        ----------
        ingredient : Ingredient
            the current ingredient to add to the recipe
        ingredient_name : str
            the user input ingredient name
        recipe_name : str
            the name of the Recipe that is currently being created

        Returns
        -------
        int
            an int representing the amount of Ingredient in Recipe
        """
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
        """Prompts the user to ask if they would like to add the ingredient
        to the list

        Returns
        -------
        boolean
            True if answer is equal to 'y'
        """
        response = input(
            "Ingredient not in list would you like to create it? y/n "
        )
        return response.lower().strip() == "y"
