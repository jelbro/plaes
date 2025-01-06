import os
import sys
from FoodLists import *
from FileHandling import *


class Menu:
    """a class that displays various navigational menus"""

    def __init__(self, ingredient_list, recipe_list):
        os.system("clear")
        self.ingredient_list = ingredient_list or IngredientList()
        self.recipe_list = recipe_list or RecipeList()

    def print_menu(self, menu_type, verbose_options, options):
        print(f"{menu_type.title()} Menu")
        print(f"Select an option")
        for option_num in range(len(options)):
            if (option_num % 2) == 1:
                print(
                    f"{options[option_num]}: {verbose_options[option_num].title()}"
                )
            else:
                print(
                    f"{options[option_num]}: {verbose_options[option_num].title()}",
                    end="   ",
                )
        return self.get_menu_choice(options)

    def display_main_menu(self):
        os.system("clear")
        choice = self.print_menu(
            "main",
            ["ingredients", "recipes", "prep list", "quit"],
            ["i", "r", "p", "q"],
        )

        match choice:
            case "i":
                self.display_ingredient_menu()
            case "r":
                self.display_recipe_menu()
            case "p":
                self.display_prep_list_menu()
            case "q":
                self.dsiplay_quit_menu()

    def display_ingredient_menu(self):
        print(
            "Ingredient Menu\n",
            "Select an option\n",
            "v: View Ingredients a: Add Ingredient d: Delete Ingredient b: Back",
        )
        choice = self.get_menu_choice(["v", "a", "d", "b"])
        match choice:
            case "v":
                self.ingredient_list.display_list()
                input("Press enter to continue...")
                self.display_ingredient_menu()
            case "a":
                if not self.ingredient_list:
                    self.ingredient_list = IngredientList()
                    self.ingredient_list.add_new_ingredient()
                else:
                    self.ingredient_list.add_new_ingredient()
                self.display_ingredient_menu()
            case "d":
                self.ingredient_list.delete_from_list()
                self.display_ingredient_menu()
            case "b":
                self.display_main_menu()

    def display_recipe_menu(self):
        print(
            "Recipe Menu\n",
            "Select an option\n",
            "v: View Recipes a: Add Recipe d: Delete Recipe b: Back",
        )
        choice = self.get_menu_choice(["v", "a", "d", "b"])
        match choice:
            case "v":
                self.view_recipes()
            case "a":
                if not self.recipe_list:
                    self.recipe_list = RecipeList()
                    self.recipe_list.add_new_recipe(self.ingredient_list)
                else:
                    self.recipe_list.add_new_recipe(self.ingredient_list)
                self.display_recipe_menu()
            case "d":
                ...
                # RecipesList.delete_from_list()
            case "b":
                self.display_main_menu()

    def view_recipes(self):
        self.recipe_list.display_list()
        print("Select an option\n", "v: View Recipe b: Back")
        choice = self.get_menu_choice(["v", "b"], clear=False)
        match choice:
            case "v":
                self.view_recipe()
            case "b":
                self.display_recipe_menu()

    def view_recipe(self):
        recipe_name = input("Select a recipe to view it: ")
        recipe_found = False
        for recipe in self.recipe_list.recipe_list:
            if recipe_name.lower() == recipe.name.lower():
                print(recipe)
                recipe_found = True
            else:
                pass
        if not recipe_found:
            print("Invalid recipe name")
            self.view_recipes()
        else:
            print("Select an option\n", "e: Edit Recipe b: Back")
            choice = self.get_menu_choice(["e", "b"], clear=False)
            match choice:
                case "e":
                    for recipe in self.recipe_list.recipe_list:
                        if recipe_name.lower() == recipe.name.lower():
                            self.display_edit_recipe(recipe)
                        else:
                            pass
                case "b":
                    self.view_recipes()

    def display_edit_recipe(self, recipe):
        print(recipe)
        print(
            "Select an option\n",
            "n: Edit Name i: Edit Ingredients d: Edit Desired Quantity ",
            "u: Edit Unit b: Back",
        )
        choice = self.get_menu_choice(["n", "i", "d", "u", "b"], clear=False)
        match choice:
            case "n":
                recipe.change_name(input(f"Change {recipe.name} to: "))
                self.view_recipes()
            case "i":
                self.display_edit_ingredients_menu(recipe)
            case "d":
                recipe.edit_desired(
                    int(input(f"Change desired quantity to: "))
                )
                self.view_recipes()
            case "u":
                while True:
                    try:
                        recipe.edit_unit(input(f"Change {recipe.unit} to: "))
                        break
                    except ValueError:
                        pass
                self.view_recipes()
            case "b":
                self.view_recipes()

    def display_edit_ingredients_menu(self, recipe):
        recipe.display_ingredients()
        print(
            "Select an option\n"
            "a: Add Ingredient e: Edit Ingredient Quantity "
            "d: Delete Ingredient"
        )
        choice = self.get_menu_choice(["a", "e", "d"], clear=False)
        recipe.display_ingredients()
        match choice:
            case "a":
                ingredient_name = input("Ingredient to add to recipe: ")
                self.ingredient_list.add_new_ingredient(ingredient_name)
                for ingredient in self.ingredient_list.ingredient_list:
                    if ingredient_name == ingredient.name:
                        ingredient.add_ingredient_to_recipe(
                            recipe,
                            self.recipe_list.get_ingredient_quantity(
                                ingredient, ingredient_name, recipe.name
                            ),
                        )
                        recipe.add_ingredient(ingredient)
                    else:
                        pass

                self.display_edit_recipe(recipe)
            case "e":
                ingredient_name = input("Ingredient to edit: ")
                for ingredient in self.ingredient_list.ingredient_list:
                    if ingredient_name == ingredient.name:
                        recipe.change_used_in_quantity(
                            ingredient,
                            self.recipe_list.get_ingredient_quantity(
                                ingredient, ingredient_name, recipe.name
                            ),
                        )

                    else:
                        pass
                self.view_recipes()
            case "d":
                ...

    def display_prep_list_menu(self):
        print(
            "Preperation List Menu\n",
            "Select an option\n",
            "t: Take stock c: Create Prep list b: Back",
        )
        choice = self.get_menu_choice(["t", "c", "b"])
        match choice:
            case "t":
                ...
                # PreperationList.take_stock()
            case "c":
                ...
                # PreperationList.create_prep_list()
            case "b":
                self.display_main_menu()

    def dsiplay_quit_menu(self):
        print(
            "Quit\n",
            "Select an option\n",
            "q: Quit WITHOUT saving s: Save & Quit b: Back",
        )
        choice = self.get_menu_choice(["q", "s", "b"])
        match choice:
            case "q":
                confirmation = input(
                    "Are you sure you want to quit without saving y/n?"
                )
                if confirmation.lower().strip() == "y":
                    sys.exit()
                else:
                    os.system("clear")
                    self.dsiplay_quit_menu()
            case "s":
                save_lists(
                    [self.ingredient_list, self.recipe_list],
                    "plaes_lists.json",
                )
                sys.exit()
            case "b":
                self.display_main_menu()

    def get_menu_choice(self, options, clear=True):
        while True:
            user_input = input().lower().strip()
            if user_input in options:
                if clear:
                    os.system("clear")
                return user_input
            else:
                print("Invalid Input")
                pass
