from Menu import *
from FileHandling import *
from gui import *
from tkinter import *


def main():
    ingredient_list, recipe_list = load_lists("plaes_lists.json")
    # menu = Menu(ingredient_list=ingredient_list, recipe_list=recipe_list)
    root = Tk()
    root.title("Plaes")
    gui = Gui(root, ingredient_list=ingredient_list, recipe_list=recipe_list)
    root.mainloop()
    # menu.display_main_menu()


if __name__ == "__main__":
    main()
