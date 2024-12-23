import os
import sys
from FoodLists import *


class Menu:
    """a class that displays various navigational menus"""

    def __init__(self, ingredient_list, recipe_list):
        os.system("clear")
        self.ingredient_list = ingredient_list
        self.recipe_list = recipe_list

    def menu_save_lists(self):
        save_lists(
            [self.ingredient_list, self.recipe_list], "plaes_lists.json"
        )

    def display_main_menu(self):
        print(
            "Main Menu\n",
            "Select an option\n",
            "i: Ingredients r: Recipes p: Prep List q: Quit",
        )
        choice = self.get_menu_choice(["i", "r", "p", "q"])
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
                if self.ingredient_list is None:
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
                ...
                # RecipesList.display_list()
            case "a":
                if self.recipe_list is None:
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
                self.menu_save_lists()
                sys.exit()
            case "b":
                self.display_main_menu()

    def get_menu_choice(self, options):
        while True:
            user_input = input().lower().strip()
            if user_input in options:
                os.system("clear")
                return user_input
            else:
                print("Invalid Input")
                pass
