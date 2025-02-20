from FileHandling import *
from Gui import *
from tkinter import *


def main():
    ingredient_list, recipe_list = load_lists("plaes_lists.json")
    root = Tk()
    root.title("Plaes")
    root.geometry("500x600")
    gui = Gui(root, ingredient_list=ingredient_list, recipe_list=recipe_list)

    def on_closing():
        if messagebox.askyesno("Quit", "Do you want to save before quitting?"):
            save_lists(
                [gui.ingredient_list, gui.recipe_list], "plaes_lists.json"
            )
            root.destroy()
        else:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
