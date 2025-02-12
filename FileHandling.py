from FoodLists import *


def load_lists(file_path):
    """a function which loads a RecipeList and IngredientList from a .json file

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
                ingredient_list_obj = IngredientList(ingredient_list)

                if "recipe_list" in entry:
                    recipe_list = []
                    for recipe in entry["recipe_list"]:
                        recipe_list.append(
                            Recipe(
                                name=recipe["name"],
                                ingredients=load_ingredients(
                                    recipe, ingredient_list_obj
                                ),
                                quantity=recipe["quantity"],
                                desired_quantity=recipe["desired_quantity"],
                                unit=recipe["unit"],
                                batch_size=recipe["batch_size"],
                            )
                        )
        return ingredient_list_obj, RecipeList(recipe_list=recipe_list)


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
        merged_lists.append(json.loads(food_list.to_json()))
    with open(file_path, mode="w") as file:
        json.dump(merged_lists, file, indent=4)


def load_recipe(file_path):
    """helper function to load a recipe from .json

    Parameters
    ----------
    file_path : str
        file path of a valid .json file

    Returns
    -------
    Recipe
        a Recipe object from the imported .json

    Raises
    ------
    FileNotFoundError
        if file path does not return a valid .json file
    """
    if not file_path.lower().endswith(".json"):
        raise FileNotFoundError("file_path must be a valid .json file path")
    with open(file_path, mode="r") as file:
        recipe = json.loads(file.read())
    return Recipe(
        name=recipe["name"],
        ingredients=load_ingredients(recipe),
        quantity=recipe["quantity"],
        desired_quantity=recipe["desired_quantity"],
        unit=recipe["unit"],
        batch_size=recipe["batch_size"],
    )


def load_ingredients(recipe, ingredient_list_obj=[]):
    """a helper function that creates Ingredient objects from imported .json

    Parameters
    ----------
    recipe : Recipe
        Recipe object imported from .json file

    Returns
    -------
    List of Ingredients
        returns a list of Ingredient objects with its values taken from the .json
    """
    ingredient_list = []

    for ingredient in recipe["ingredients"]:
        ingredient_in_list = False
        for ing in ingredient_list_obj.ingredient_list:
            if ingredient["name"] == ing.name:
                ingredient_list.append(ing)
                ingredient_in_list == True
                break
            else:
                pass
    return ingredient_list
