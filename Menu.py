import os
import sys
from FoodLists import *
from FileHandling import *


def clear():
    os.system("clear")


class Menu:
    """a class that displays various navigational menus"""

    def __init__(self, ingredient_list, recipe_list):
        os.system("clear")
        self.ingredient_list = ingredient_list or IngredientList()
        self.recipe_list = recipe_list or RecipeList()

    def print_menu(
        self, menu_type, verbose_options, clear=True, ignore_prefix=None
    ):
        """prints a menu and returns the user's selected option

        Parameters
        ----------
        menu_type : str
            the type of menu to display
        verbose_options : list
            a list of options to offer the user

        Returns
        -------
        str
            a str representing the user's choice
        """

        options = self.get_options(verbose_options, ignore_prefix)
        if menu_type != None:
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
        if len(options) % 2 == 1:
            print()
        return self.get_menu_choice(options)

    def get_menu_choice(self, options, clear=True):
        """asks the user for input from a selection of options

        Parameters
        ----------
        options : list
            a selection of options for the user to choose from
        clear : bool, optional
            clears the terminal if true, by default True

        Returns
        -------
        str
            the user's chosen char
        """
        while True:
            user_input = input().lower().strip()
            if user_input in options:
                return user_input
            else:
                print("Invalid Input")
                pass

    def get_options(self, verbose_options, ignore_prefix=None):
        """returns the first letter of each option given in a list

        Parameters
        ----------
        verbose_options : str
            a list of options to offer the user

        Returns
        -------
        list
            a list of single character options
        """
        options = []
        for option in verbose_options:
            if ignore_prefix != None:
                option = option.replace(f"{ignore_prefix} ", "")
                options.append(option[0])
            else:
                options.append(option[0])
        return options

    def display_main_menu(self):
        user_choice = self.print_menu(
            "main", ["ingredients", "recipes", "prep list", "quit"]
        )
        clear()

        match user_choice:
            case "i":
                self.display_ingredient_menu()
            case "r":
                self.display_recipe_menu()
            case "p":
                self.display_prep_list_menu()
            case "q":
                self.dsiplay_quit_menu()

    def display_ingredient_menu(self):
        user_choice = self.print_menu(
            "ingredient",
            [
                "view ingredients",
                "add ingredients",
                "delete ingredients",
                "back",
            ],
        )
        clear()

        match user_choice:
            case "v":
                self.ingredient_list.display_list()
            case "a":
                self.ingredient_list.add_new_ingredient()
            case "d":
                self.ingredient_list.delete_from_list()
            case "b":
                clear()
                self.display_main_menu()
        clear()
        self.display_ingredient_menu()

    def display_recipe_menu(self):
        user_choice = self.print_menu(
            "recipe",
            [
                "view recipes",
                "add recipe",
                "delete recipe",
                "back",
            ],
        )
        clear()

        match user_choice:
            case "v":
                self.view_recipes()
            case "a":
                self.recipe_list.add_new_recipe(self.ingredient_list)
            case "d":
                ...
                # RecipesList.delete_from_list()
            case "b":
                clear()
                self.display_main_menu()
        clear()
        self.display_recipe_menu()

    def view_recipes(self):
        self.recipe_list.display_list()
        user_choice = self.print_menu(
            None, ["view recipe", "back"], clear=False
        )
        clear()
        self.recipe_list.display_list()

        match user_choice:
            case "v":
                self.view_recipe()
            case "b":
                clear()
                self.display_recipe_menu()

    def view_recipe(self):
        recipe = self.recipe_list.search_and_display_recipe()
        clear()
        print(recipe)
        user_choice = self.print_menu(
            None, ["edit recipe", "back"], clear=False
        )

        match user_choice:
            case "e":
                self.display_edit_recipe(recipe)
            case "b":
                clear()
                self.view_recipes()

    def display_edit_recipe(self, recipe):
        clear()
        print(recipe)
        user_choice = self.print_menu(
            None,
            [
                "edit name",
                "edit ingredients",
                "edit desired quantity",
                "edit unit",
                "back",
            ],
            clear=False,
            ignore_prefix="edit",
        )
        clear()
        match user_choice:
            case "n":
                recipe.change_name(input(f"Change {recipe.name} to: "))
            case "i":
                self.display_edit_ingredients_menu(recipe)
            case "d":
                recipe.edit_desired(
                    int(input(f"Change desired quantity to: "))
                )
            case "u":
                while True:
                    try:
                        recipe.edit_unit(input(f"Change {recipe.unit} to: "))
                        break
                    except ValueError:
                        pass
            case "b":
                clear()
                self.view_recipes()
        clear()
        self.display_edit_recipe(recipe)

    def display_edit_ingredients_menu(self, recipe):
        clear()
        print(recipe.display_ingredients())
        user_choice = self.print_menu(
            None,
            [
                "add ingredient",
                "edit ingredient quantity",
                "delete ingredient",
                "back",
            ],
            clear=False,
        )
        match user_choice:
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
                self.display_edit_recipe(recipe)
            case "d":
                ...
            case "b":
                clear()
                self.display_edit_recipe(recipe)

    def display_prep_list_menu(self):
        user_choice = self.print_menu(
            "preperation list",
            [
                "take stock",
                "create prep list",
                "back",
            ],
        )

        match user_choice:
            case "t":
                ...
                # PreperationList.take_stock()
            case "c":
                ...
                # PreperationList.create_prep_list()
            case "b":
                self.display_main_menu()

    def dsiplay_quit_menu(self):
        clear()
        user_choice = self.print_menu(
            "quit",
            [
                "quit WITHOUT saving",
                "save & quit",
                "back",
            ],
        )
        clear()

        match user_choice:
            case "q":
                confirmation = input(
                    "Are you sure you want to quit without saving y/n? "
                )
                if confirmation.lower().strip() == "y":
                    clear()
                    sys.exit()
                else:
                    clear()
                    self.dsiplay_quit_menu()
            case "s":
                save_lists(
                    [self.ingredient_list, self.recipe_list],
                    "plaes_lists.json",
                )
                sys.exit()
            case "b":
                clear()
                self.display_main_menu()
